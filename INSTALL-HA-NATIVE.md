# Install Porcupine "Albert" Directly on Home Assistant

This guide shows how to install Wyoming Porcupine directly on your Home Assistant system (not Docker on Unraid).

## Why Install on Home Assistant?

- ✅ **CPU-only**: Porcupine doesn't need GPU
- ✅ **Lightweight**: ~50MB RAM, <1% CPU
- ✅ **Low latency**: No network overhead
- ✅ **Simpler**: No separate Docker container to manage
- ✅ **Built-in integration**: Auto-discovered by Home Assistant

## Prerequisites

1. **Home Assistant OS or Supervised** (not Core or Container)
2. **Picovoice Access Key** - Get from https://console.picovoice.ai/
3. **Custom Wake Word Model** - Train "Albert" at Picovoice Console

## Method 1: Install Wyoming Porcupine Add-on (Recommended)

### Step 1: Check if Add-on Repository is Available

1. Open Home Assistant: https://ha.racoon.lu
2. Go to **Settings** → **Add-ons**
3. Click **Add-on Store** (bottom right)
4. Search for: `wyoming porcupine`

### Step 2A: If Add-on is Found

If you see "Wyoming Porcupine" in the add-on store:

1. Click on **Wyoming Porcupine**
2. Click **Install** (may take 2-5 minutes)
3. Wait for installation to complete
4. Continue to **Configuration** section below

### Step 2B: If Add-on is NOT Found

Add the Wyoming add-on repository manually:

1. Go to **Settings** → **Add-ons**
2. Click **Add-on Store** → **⋮ (three dots)** → **Repositories**
3. Add this repository: `https://github.com/rhasspy/hassio-addons`
4. Click **Add** → **Close**
5. Refresh the add-on store
6. Search again for `wyoming porcupine`
7. Click **Install**

### Step 3: Configure the Add-on

After installation:

1. Click on **Wyoming Porcupine** in your add-ons list
2. Go to **Configuration** tab
3. Add your configuration:

```yaml
# Picovoice Access Key (REQUIRED)
access_key: "YOUR_PICOVOICE_ACCESS_KEY_HERE"

# Wake words (use built-in for testing)
keywords:
  - computer

# Or use custom wake word (after uploading albert.ppn)
# keyword_paths:
#   - /share/porcupine/albert.ppn

# Detection sensitivity (0.0-1.0)
sensitivity: 0.5

# Debug mode
debug: false
```

4. Click **Save**
5. Go to **Info** tab
6. Toggle **Start on boot** to ON
7. Click **Start**
8. Check **Logs** tab for:
   ```
   Starting Wyoming Porcupine...
   Porcupine initialized successfully
   ```

### Step 4: Upload Custom "Albert" Wake Word

To use your custom "Albert" wake word:

1. Download `albert.ppn` from Picovoice Console (see training guide below)
2. In Home Assistant, go to **Settings** → **Add-ons** → **File Editor** (install if needed)
3. Navigate to `/share/porcupine/` (create directory if it doesn't exist)
4. Upload `albert.ppn` to this directory
5. Edit Wyoming Porcupine configuration:

```yaml
access_key: "YOUR_KEY_HERE"

# Comment out keywords, use keyword_paths instead
# keywords:
#   - computer

keyword_paths:
  - /share/porcupine/albert.ppn

sensitivity: 0.5
debug: false
```

6. Save and restart the add-on

## Method 2: Install as Custom Integration (Alternative)

If the add-on method doesn't work, install as a custom integration:

### Using Terminal & SSH Add-on

1. Install **Terminal & SSH** add-on if not already installed
2. Open the Terminal
3. Run these commands:

```bash
# Create directory for Wyoming services
mkdir -p /usr/share/hassio/homeassistant/wyoming

# Create Porcupine directory
cd /usr/share/hassio/homeassistant/wyoming
mkdir porcupine
cd porcupine

# Install Python dependencies
apk add --no-cache python3 py3-pip
pip3 install wyoming pvporcupine

# Create startup script
cat > run.sh << 'EOF'
#!/usr/bin/env bash
set -e

ACCESS_KEY="${PORCUPINE_ACCESS_KEY}"
KEYWORDS="${KEYWORDS:-computer}"
SENSITIVITY="${SENSITIVITY:-0.5}"

if [ -z "$ACCESS_KEY" ]; then
    echo "ERROR: PORCUPINE_ACCESS_KEY not set!"
    exit 1
fi

python3 -m wyoming_porcupine \
    --uri tcp://0.0.0.0:10400 \
    --access-key "$ACCESS_KEY" \
    --keywords $KEYWORDS \
    --sensitivity $SENSITIVITY
EOF

chmod +x run.sh

# Create environment file
cat > .env << 'EOF'
PORCUPINE_ACCESS_KEY=your_access_key_here
KEYWORDS=computer
SENSITIVITY=0.5
EOF

echo "Installation complete!"
echo "Edit .env file with your Picovoice access key"
echo "Then run: source .env && ./run.sh"
```

## Training "Albert" Wake Word

### Step 1: Sign Up for Picovoice

1. Go to: https://console.picovoice.ai/
2. Click **Sign Up** (or Sign In if you have account)
3. Verify your email

### Step 2: Get Access Key

1. In Picovoice Console, click **Account** (top right)
2. Go to **Access Keys** tab
3. Click **Create New Key**
4. Name it: `homeassistant-albert`
5. Click **Create**
6. **Copy the access key** and save it

### Step 3: Train "Albert" Wake Word

1. In Picovoice Console, click **Porcupine** in the sidebar
2. Click **Train Wake Word** button
3. Fill in the training form:
   - **Wake Phrase**: `albert`
   - **Language**: English (or select "Other" for Luxembourgish)
   - **Training Type**: Keep default (Automatic)
4. Click **Train Wake Word**
5. Wait 3-5 minutes for training to complete
6. When ready, click **Download**
7. Save `albert.ppn` to your computer

## Home Assistant Integration

Once Porcupine is running (via add-on or custom install):

### Auto-Discovery

1. Go to **Settings** → **Devices & Services**
2. You should see a discovered **Wyoming** integration
3. Click **Configure**
4. It should auto-detect the Porcupine service
5. Click **Submit**

### Manual Configuration

If not auto-discovered:

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search: `wyoming`
4. Select **Wyoming Protocol**
5. Enter:
   - **Host**: `core-wyoming-porcupine` (if add-on) or `localhost`
   - **Port**: `10400`
6. Click **Submit**

## Configure Voice Assistant

1. Go to **Settings** → **Voice Assistants**
2. Edit your assistant (or create new)
3. Configure:
   - **Conversation agent**: Home Assistant
   - **Speech-to-text**: Luxembourgish Whisper STT
   - **Text-to-speech**: Luxembourgish Fish Speech TTS
   - **Wake word**: **albert** (or **computer** if testing)
4. Click **Update**

## Testing

### Test Wake Word Detection

1. Go to **Settings** → **Voice Assistants**
2. Click your assistant
3. Click **Debug**
4. Say: **"Albert"** (or "Computer" if testing)
5. Should see: `Wake word detected: albert`

### Test Full Pipeline

1. Say: **"Albert"**
2. Wait for confirmation (beep/LED)
3. Say: **"Wéi speet ass et?"** (What time is it?)
4. Should respond in Luxembourgish

## Troubleshooting

### Add-on Won't Start

**Check logs:**
1. Settings → Add-ons → Wyoming Porcupine → Logs

**Common issues:**
- Missing access key: Add to configuration
- Invalid access key: Regenerate at console.picovoice.ai
- Port conflict: Another service using 10400

**Fix:**
```yaml
# In add-on configuration
port: 10401  # Change if 10400 is taken
```

### Wake Word Not Detected

1. **Increase sensitivity:**
   ```yaml
   sensitivity: 0.7  # was 0.5
   ```
2. **Check microphone**: Settings → System → Audio → Input
3. **Test with built-in word first**: Use `computer` before `albert`
4. **Check logs**: Should show "Porcupine initialized successfully"

### Custom Wake Word Not Loading

1. **Verify file exists:**
   ```bash
   ls -la /share/porcupine/albert.ppn
   ```
2. **Check file permissions:**
   ```bash
   chmod 644 /share/porcupine/albert.ppn
   ```
3. **Verify path in config:**
   ```yaml
   keyword_paths:
     - /share/porcupine/albert.ppn  # Must match exactly
   ```

### Integration Not Discovered

**Manual steps:**
1. Settings → Devices & Services → Add Integration
2. Search: `wyoming protocol`
3. Add manually with host and port

**Check if service is running:**
```bash
# In Terminal add-on
netstat -tuln | grep 10400

# Should show:
# tcp 0 0 0.0.0.0:10400 0.0.0.0:* LISTEN
```

## File Locations on Home Assistant

```
/usr/share/hassio/homeassistant/
├── share/
│   └── porcupine/
│       └── albert.ppn           # Custom wake word model
├── addons/
│   └── core_wyoming_porcupine/  # Add-on installation
└── configuration.yaml           # HA config
```

## Comparison: Add-on vs Docker on Unraid

| Feature | HA Add-on | Docker on Unraid |
|---------|-----------|------------------|
| **Setup** | Very easy | Manual |
| **Latency** | Lower (local) | Higher (network) |
| **Maintenance** | Auto-updates | Manual |
| **Resources** | Uses HA CPU | Uses Unraid CPU |
| **Integration** | Auto-discovered | Manual config |
| **Recommended** | ✅ Yes | Only if HA resource constrained |

## Performance

Running on Home Assistant:
- **CPU**: <1% on modern CPU
- **RAM**: ~50MB
- **Latency**: <50ms (vs ~100-150ms on Unraid)
- **Network**: No network overhead

## Updating

### Update Add-on

1. Settings → Add-ons → Wyoming Porcupine
2. If update available, click **Update**
3. Wait for completion
4. Restart add-on

### Update Custom Wake Word

1. Retrain at Picovoice Console (if needed)
2. Download new `albert.ppn`
3. Replace file in `/share/porcupine/`
4. Restart Wyoming Porcupine add-on

## Resources

- **Picovoice Console**: https://console.picovoice.ai/
- **Wyoming Add-ons**: https://github.com/rhasspy/hassio-addons
- **Porcupine Docs**: https://picovoice.ai/docs/porcupine/
- **Home Assistant Voice**: https://www.home-assistant.io/voice_control/

## Next Steps

After installation:
1. ✅ Train "Albert" wake word
2. ✅ Install Wyoming Porcupine add-on
3. ✅ Upload albert.ppn
4. ✅ Configure Home Assistant integration
5. ✅ Test wake word detection
6. ✅ Integrate with Luxembourgish STT/TTS pipeline
7. 🎉 Enjoy hands-free Luxembourgish voice control!

---

**Installation Time**: ~10-15 minutes
**Difficulty**: Easy (if using add-on)
**Recommended**: ✅ Install directly on Home Assistant for best performance
