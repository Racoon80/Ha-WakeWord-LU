# Quick Setup Guide: Albert Wake Word

Step-by-step guide to get "Albert" wake word working in 10 minutes.

## Prerequisites Checklist

- [ ] Unraid server running
- [ ] Network br0.106 configured (or adjust in docker-compose)
- [ ] Internet connection
- [ ] Web browser

## Step 1: Create Picovoice Account (2 minutes)

1. Go to: https://console.picovoice.ai/
2. Click **Sign Up**
3. Enter email and create password
4. Verify email
5. Log in to Picovoice Console

## Step 2: Get Access Key (1 minute)

1. In Picovoice Console, click **Account** (top right)
2. Go to **Access Keys** tab
3. Click **Create New Key**
4. Name it: `homeassistant`
5. Click **Create**
6. **Copy the key** (looks like: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)
7. Save it somewhere safe

## Step 3: Train "Albert" Wake Word (5 minutes)

1. In Picovoice Console, click **Porcupine** in sidebar
2. Click **Train Wake Word** button
3. Fill in the form:
   - **Wake Phrase**: `albert`
   - **Language**: English (or select "Other" for Luxembourgish)
   - **Training Type**: Automatic (default)
4. Click **Train Wake Word**
5. Wait 3-5 minutes for training to complete
6. When done, click **Download** to get `albert.ppn` file
7. Save to your Downloads folder

## Step 4: Deploy to Unraid (5 minutes)

### Option A: Using the Deployment Script

```bash
# On your local machine
cd L:\Projects\Ha-WakeWord-LU

# Set your access key
export PORCUPINE_ACCESS_KEY="paste_your_key_here"

# Copy albert.ppn to models directory
mkdir -p models
cp ~/Downloads/albert.ppn ./models/

# Run deployment script
./deploy.sh
```

### Option B: Manual Deployment

```bash
# 1. SSH to Unraid
ssh root@192.168.1.XXX

# 2. Create project directory
cd /mnt/user/appdata/ai
mkdir -p ha-wakeword-albert/models

# 3. On your local machine, copy files
scp -r L:\Projects\Ha-WakeWord-LU\porcupine-wakeword root@192.168.1.XXX:/mnt/user/appdata/ai/ha-wakeword-albert/
scp L:\Projects\Ha-WakeWord-LU\docker-compose-porcupine.yml root@192.168.1.XXX:/mnt/user/appdata/ai/ha-wakeword-albert/docker-compose.yml
scp L:\Projects\Ha-WakeWord-LU\models\albert.ppn root@192.168.1.XXX:/mnt/user/appdata/ai/ha-wakeword-albert/models/

# 4. Back on Unraid, create .env file
cd /mnt/user/appdata/ai/ha-wakeword-albert
echo "PORCUPINE_ACCESS_KEY=paste_your_key_here" > .env

# 5. Deploy
docker-compose up -d

# 6. Check logs
docker logs -f ha-wakeword-albert
```

## Step 5: Verify It's Working (1 minute)

### Check Container Status

```bash
# On Unraid
docker ps | grep albert

# Should show:
# ha-wakeword-albert   Up X minutes   0.0.0.0:10400->10400/tcp
```

### Check Logs

```bash
docker logs ha-wakeword-albert

# Should show:
# Starting Porcupine wake word detection...
# Wake words: albert
# Found custom wake word model: /app/models/albert.ppn
# Using custom wake word models
# Porcupine initialized successfully
# Starting Wyoming Porcupine server on 0.0.0.0:10400
```

### Test Connection

```bash
# From any machine on network
nc -zv 192.168.106.20 10400

# Should show:
# Connection to 192.168.106.20 10400 port [tcp/*] succeeded!
```

## Step 6: Add to Home Assistant (2 minutes)

### Method 1: Via UI (Recommended)

1. Open Home Assistant
2. Go to **Settings** → **Devices & Services**
3. Click **+ Add Integration** (bottom right)
4. Search for: `wyoming`
5. Click **Wyoming Protocol**
6. Enter:
   - **Host**: `192.168.106.20`
   - **Port**: `10400`
7. Click **Submit**
8. Integration should appear as **Wyoming (albert)**

### Method 2: Via Configuration File

Edit `configuration.yaml`:
```yaml
wyoming:
  - uri: tcp://192.168.106.20:10400
```

Restart Home Assistant.

## Step 7: Configure Voice Assistant Pipeline (2 minutes)

1. In Home Assistant, go to **Settings** → **Voice Assistants**
2. Click on your assistant (or create new one)
3. Set these options:
   - **Conversation agent**: Home Assistant
   - **Speech-to-text**: Luxembourgish Whisper STT *(your existing one)*
   - **Text-to-speech**: Luxembourgish Fish Speech TTS *(your existing one)*
   - **Wake word**: **albert** *(the new one!)*
4. Click **Save**

## Step 8: Test It! (1 minute)

### Test via Home Assistant

1. Go to **Settings** → **Voice Assistants**
2. Click your assistant
3. Click **Debug** button
4. Say: **"Albert"**
5. Should see: `Wake word detected: albert`
6. Then say: **"Wéi speet ass et?"** *(What time is it?)*
7. Should respond with current time in Luxembourgish

### Test via Device

If using a voice satellite (ESPHome, Android app, etc.):

1. Say: **"Albert"**
2. Wait for confirmation beep/light
3. Say your command in Luxembourgish
4. Should respond

## Troubleshooting Quick Fixes

### ❌ Container won't start

```bash
# Check access key is set
cat .env

# Rebuild
docker-compose down
docker-compose up --build -d
```

### ❌ "No custom models found"

```bash
# Check file exists
ls -la models/albert.ppn

# If missing, copy it again
scp ~/Downloads/albert.ppn root@unraid:/mnt/user/appdata/ai/ha-wakeword-albert/models/
docker-compose restart
```

### ❌ Wake word not detected

1. Increase sensitivity in docker-compose.yml:
   ```yaml
   - SENSITIVITY=0.7  # was 0.5
   ```
2. Restart: `docker-compose restart`
3. Test again

### ❌ Home Assistant can't connect

```bash
# Check firewall
iptables -L | grep 10400

# Test from HA host
nc -zv 192.168.106.20 10400

# Check network
docker exec ha-wakeword-albert ip addr show
```

## Complete! 🎉

You now have:
- ✅ Porcupine wake word engine running
- ✅ "Albert" custom wake word active
- ✅ Wyoming protocol server on port 10400
- ✅ Home Assistant integration configured
- ✅ Ready to use in Luxembourgish

**Total time**: ~15-20 minutes

## Next Steps

### Improve Accuracy
- Increase sensitivity if Albert is not detected consistently
- Retrain wake word with more voice samples
- Adjust microphone gain in Home Assistant

### Add More Wake Words
- Train additional wake words (e.g., "Moien", "Computer")
- Deploy multiple words simultaneously
- Use different wake words for different assistants

### Monitor Performance
```bash
# Watch logs in real-time
docker logs -f --tail 50 ha-wakeword-albert

# Check resource usage
docker stats ha-wakeword-albert
```

## Environment File Template

Save as `.env`:
```bash
# Picovoice Access Key (required)
PORCUPINE_ACCESS_KEY=your_access_key_here

# Optional: Override defaults
# KEYWORDS=albert
# SENSITIVITY=0.5
# PORT=10400
```

## File Checklist

After setup, you should have:

```
/mnt/user/appdata/ai/ha-wakeword-albert/
├── porcupine-wakeword/
│   ├── wyoming_porcupine.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── start.sh
├── models/
│   └── albert.ppn              ← Your trained model
├── docker-compose.yml
└── .env                        ← Your access key
```

---

**Questions?** Check README-PORCUPINE.md for detailed documentation.
