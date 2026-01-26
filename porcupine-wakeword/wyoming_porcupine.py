#!/usr/bin/env python3
"""Wyoming protocol server for Porcupine wake word detection."""
import argparse
import asyncio
import logging
import wave
from pathlib import Path
from typing import Optional

import pvporcupine
from wyoming.audio import AudioChunk, AudioStart, AudioStop
from wyoming.event import Event
from wyoming.info import Describe, Info, WakeModel, WakeProgram, Attribution
from wyoming.server import AsyncEventHandler, AsyncTcpServer
from wyoming.wake import Detect, Detection

_LOGGER = logging.getLogger("wyoming_porcupine")


class PorcupineEventHandler(AsyncEventHandler):
    """Event handler for Porcupine wake word detection."""

    def __init__(
        self,
        reader,
        writer,
        porcupine: pvporcupine.Porcupine,
        info: Info,
        keyword_names: list[str],
    ) -> None:
        super().__init__(reader, writer)
        self.porcupine = porcupine
        self._info = info
        self._keyword_names = keyword_names
        self._audio_buffer = bytearray()
        self._is_detecting = False

    async def handle_event(self, event: Event) -> bool:
        """Handle events from Wyoming protocol."""
        if Describe.is_type(event.type):
            # Send info about this wake word service
            await self.write_event(self._info.event())
            return True

        if Detect.is_type(event.type):
            # Start detection
            _LOGGER.debug("Starting wake word detection")
            self._is_detecting = True
            self._audio_buffer.clear()
            return True

        if AudioStart.is_type(event.type):
            # Audio stream started
            _LOGGER.debug("Audio stream started")
            return True

        if AudioChunk.is_type(event.type):
            # Process audio chunk
            if self._is_detecting:
                chunk = AudioChunk.from_event(event)
                await self._process_audio_chunk(chunk)
            return True

        if AudioStop.is_type(event.type):
            # Audio stream stopped
            _LOGGER.debug("Audio stream stopped")
            self._is_detecting = False
            self._audio_buffer.clear()
            return True

        return True

    async def _process_audio_chunk(self, chunk: AudioChunk) -> None:
        """Process audio chunk for wake word detection."""
        # Add audio to buffer
        self._audio_buffer.extend(chunk.audio)

        # Porcupine expects 16-bit PCM at 16kHz
        # frame_length = 512 samples (32ms at 16kHz)
        frame_length_bytes = self.porcupine.frame_length * 2  # 2 bytes per sample

        while len(self._audio_buffer) >= frame_length_bytes:
            # Extract one frame
            frame_bytes = self._audio_buffer[:frame_length_bytes]
            self._audio_buffer = self._audio_buffer[frame_length_bytes:]

            # Convert bytes to int16 array
            import struct
            frame = struct.unpack(
                f"{self.porcupine.frame_length}h",
                frame_bytes
            )

            # Process frame
            keyword_index = self.porcupine.process(frame)

            if keyword_index >= 0:
                # Wake word detected!
                keyword_name = self._keyword_names[keyword_index]
                _LOGGER.info(f"Wake word detected: {keyword_name}")

                # Send detection event
                detection = Detection(
                    name=keyword_name,
                    timestamp=0  # You could add proper timestamp if needed
                )
                await self.write_event(detection.event())


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Wyoming protocol server for Porcupine wake word detection"
    )
    parser.add_argument("--host", default="0.0.0.0", help="Bind address")
    parser.add_argument("--port", type=int, default=10400, help="Bind port")
    parser.add_argument(
        "--keywords",
        nargs="+",
        default=["computer"],
        help="Wake words to detect (e.g., computer, jarvis, alexa)",
    )
    parser.add_argument(
        "--access-key",
        required=True,
        help="Picovoice Access Key (get from https://console.picovoice.ai/)",
    )
    parser.add_argument(
        "--sensitivity",
        type=float,
        default=0.5,
        help="Detection sensitivity (0.0-1.0, default: 0.5)",
    )
    parser.add_argument(
        "--model-path",
        help="Path to custom Porcupine model file (.pv)",
    )
    parser.add_argument(
        "--keyword-paths",
        nargs="+",
        help="Paths to custom keyword files (.ppn)",
    )
    return parser


async def main_async() -> None:
    args = _build_arg_parser().parse_args()
    logging.basicConfig(level=logging.INFO)

    _LOGGER.info("Initializing Porcupine wake word engine...")

    # Prepare keywords
    if args.keyword_paths:
        # Custom keyword files
        keyword_paths = [Path(p) for p in args.keyword_paths]
        keywords = None
        keyword_names = [p.stem for p in keyword_paths]
    else:
        # Built-in keywords
        keywords = [k.lower() for k in args.keywords]
        keyword_paths = None
        keyword_names = keywords

    _LOGGER.info(f"Wake words: {', '.join(keyword_names)}")

    # Create sensitivity list (one per keyword)
    sensitivities = [args.sensitivity] * len(keyword_names)

    # Initialize Porcupine
    try:
        porcupine = pvporcupine.create(
            access_key=args.access_key,
            keywords=keywords,
            keyword_paths=keyword_paths,
            model_path=args.model_path,
            sensitivities=sensitivities,
        )
        _LOGGER.info(f"Porcupine initialized successfully")
        _LOGGER.info(f"Sample rate: {porcupine.sample_rate} Hz")
        _LOGGER.info(f"Frame length: {porcupine.frame_length} samples")
    except Exception as e:
        _LOGGER.error(f"Failed to initialize Porcupine: {e}")
        raise

    # Create Wyoming info
    info = Info(
        wake=[
            WakeProgram(
                name="porcupine",
                description="Porcupine wake word detection",
                attribution=Attribution(
                    name="Picovoice",
                    url="https://picovoice.ai/",
                ),
                installed=True,
                version=pvporcupine.__version__,
                models=[
                    WakeModel(
                        name=name,
                        description=f"Porcupine wake word: {name}",
                        attribution=Attribution(
                            name="Picovoice",
                            url="https://picovoice.ai/",
                        ),
                        installed=True,
                        version=pvporcupine.__version__,
                        languages=["en"],  # Adjust based on keyword
                    )
                    for name in keyword_names
                ],
            )
        ]
    )

    # Create server
    server = AsyncTcpServer(args.host, args.port)

    def handler_factory(reader, writer):
        return PorcupineEventHandler(reader, writer, porcupine, info, keyword_names)

    _LOGGER.info(f"Starting Wyoming Porcupine server on {args.host}:{args.port}")
    _LOGGER.info(f"Listening for wake words: {', '.join(keyword_names)}")

    try:
        await server.run(handler_factory)
    finally:
        porcupine.delete()


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
