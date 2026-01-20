# Wake Word Training Status

## ✅ PHASE 1 COMPLETE - "Ronaldo" Wake Word ACTIVE

### What's Working NOW
- **Wake Word Model**: Ronaldo
- **Service**: tcp://192.168.106.20:10400
- **Status**: ✅ ACTIVE and READY
- **Container**: ha-wakeword-lu on Unraid
- **Model File**: ronaldo.tflite (202 KB)

### Test It Now!
1. Configure Home Assistant Wyoming integration:
   - Host: `192.168.106.20`
   - Port: `10400`

2. Say "**Ronaldo**" to trigger the wake word

3. The service will detect it and activate your Home Assistant voice assistant

---

## ⏳ PHASE 2 IN PROGRESS - "Roberto" Custom Training

### Training Options for "Roberto"

#### Option A: Manual Recording (MOST RELIABLE) ⭐
Use the collection script I created:

```bash
cd L:\Projects\Ha-WakeWord-LU\training
pip install -r requirements.txt
python collect_samples.py
```

**Process:**
1. Script will prompt you to record samples
2. Record 100-200 times saying "Roberto"
3. Record 500-1000 background/other speech samples
4. Script saves to data/positive and data/negative
5. Run training: `python train_roberto.py --train`

**Pros:**
- Your actual Luxembourgish pronunciation
- Best accuracy
- Proven method

**Cons:**
- Time-consuming (1-2 hours of recording)

#### Option B: TTS Automated Training (NEEDS API FIX)
I created `automated_roberto_training.py` that would:
1. Generate 200 "Roberto" samples from Fish-Speech TTS
2. Generate 1000 negative samples
3. Automatically train the model

**Status:** Framework ready, but Fish-Speech TTS API endpoint needs discovery

**To Fix:**
1. Find the correct port and API endpoint for Fish-Speech TTS at 192.168.106.15
2. Update the TTS_URL and API format in automated_roberto_training.py
3. Run: `/mnt/user/appdata/ai/roberto-training/start_training.sh`

#### Option C: Hybrid Approach (RECOMMENDED)
1. **Quick Test** (30 minutes):
   - Record 20 samples manually
   - Use existing openWakeWord pre-trained embeddings
   - Train quick test model

2. **Refine Over Time**:
   - Add more samples gradually
   - Retrain monthly
   - Improve accuracy iteratively

#### Option D: Community Model Fine-Tuning
Use similar models as starting point:
- "Ronaldo" (already deployed - most similar)
- "Bartolo" (available from community)
- "Alfred" (available from community)

Fine-tune with a few "Roberto" samples in Luxembourgish.

---

## 📊 Current Setup Summary

### Deployed Models
1. **Ronaldo** (Active)
   - Location: /mnt/user/appdata/ai/roberto-models/ronaldo.tflite
   - Status: Loaded and working
   - Phonetically similar to "Roberto"

### Training Infrastructure (Ready)
- **Scripts**:
  - `collect_samples.py` - Manual recording
  - `train_roberto.py` - Model training
  - `automated_roberto_training.py` - TTS-based automation (needs API fix)

- **Unraid Paths**:
  - Project: /mnt/user/appdata/ai/Ha-WakeWord-LU
  - Models: /mnt/user/appdata/ai/roberto-models
  - Training: /mnt/user/appdata/ai/roberto-training

- **GPU Training**: Docker compose configured with NVIDIA GPU support

---

## 🚀 Recommended Next Steps

### Immediate (You Can Do Now)
1. **Test Ronaldo** wake word with Home Assistant
   - Add Wyoming integration
   - Configure voice assistant
   - Say "Ronaldo" to test

2. **Decide on Roberto Training Approach**:
   - Option A (manual) - Most reliable
   - Option B (automated) - Fix TTS API first
   - Option C (hybrid) - Best of both

### Short Term (This Week)
1. If using manual recording:
   - Run `collect_samples.py`
   - Record 50-100 "Roberto" samples
   - Record 200-300 negative samples
   - Train initial model
   - Test and iterate

2. If fixing automated TTS:
   - SSH to Unraid: `ssh root@192.168.10.100`
   - Check Fish-Speech container logs
   - Find correct API port and endpoint
   - Update `automated_roberto_training.py`
   - Run training in background

### Long Term (Continuous Improvement)
1. Collect more samples over time
2. Retrain monthly with additional data
3. Test in different environments
4. Adjust threshold for sensitivity
5. Add more voices (family members)

---

## 🔧 Training Commands Reference

### Manual Recording
```bash
cd L:\Projects\Ha-WakeWord-LU\training
python collect_samples.py
```

### Train Model (After Collecting Samples)
```bash
cd L:\Projects\Ha-WakeWord-LU\training
python train_roberto.py --train
```

### Deploy Trained Model to Unraid
```bash
# Copy model file
scp training/models/roberto_lb.tflite root@192.168.10.100:/mnt/user/appdata/ai/roberto-models/

# SSH to Unraid
ssh root@192.168.10.100

# Restart container
cd /mnt/user/appdata/ai/Ha-WakeWord-LU
docker-compose restart

# Check logs
docker logs ha-wakeword-lu
```

### Automated Training (Once TTS API Fixed)
```bash
# SSH to Unraid
ssh root@192.168.10.100

# Run training
/mnt/user/appdata/ai/roberto-training/start_training.sh

# Monitor progress
tail -f /mnt/user/appdata/ai/roberto-training/training.log
```

---

## 📝 Fish-Speech TTS API Discovery

To fix automated training, find the correct API:

```bash
# SSH to Unraid
ssh root@192.168.10.100

# Check Fish-Speech container
docker logs Luxembourgish-FishSpeech-TTS | grep -i port
docker logs Luxembourgish-FishSpeech-TTS | grep -i api
docker logs Luxembourgish-FishSpeech-TTS | head -50

# Test common ports
curl http://192.168.106.15:5000
curl http://192.168.106.15:8000
curl http://192.168.106.15:8080
curl http://192.168.106.15:3000

# Check what's listening
docker exec Luxembourgish-FishSpeech-TTS netstat -tuln
```

Once you find the correct endpoint, update line 28 in `automated_roberto_training.py`:
```python
TTS_URL = "http://192.168.106.15:CORRECT_PORT"
```

---

## ✅ What's Complete

- ✅ Wyoming wake word service running
- ✅ Ronaldo model deployed and working
- ✅ Manual training scripts created
- ✅ Automated training framework created
- ✅ GPU training environment configured
- ✅ Deployment infrastructure ready
- ✅ Documentation complete

## ⏳ What's Pending

- ⏳ Fish-Speech TTS API endpoint discovery
- ⏳ Roberto sample collection (manual or automated)
- ⏳ Roberto model training
- ⏳ Home Assistant integration configuration

---

**Last Updated**: 2026-01-20
**Current Wake Word**: Ronaldo (working)
**Target Wake Word**: Roberto (training ready)
