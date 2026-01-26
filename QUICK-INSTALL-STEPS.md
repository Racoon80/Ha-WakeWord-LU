# Quick Install: Wyoming Porcupine on Home Assistant

## 5-Minute Installation Guide

Since Porcupine only needs CPU, install it directly on your Home Assistant at **https://ha.racoon.lu**

### Step 1: Add Wyoming Repository (1 minute)

1. Open https://ha.racoon.lu
2. Go to **Settings** → **Add-ons** → **Add-on Store**
3. Click **⋮** (three dots, top right) → **Repositories**
4. Paste this URL: `https://github.com/rhasspy/hassio-addons`
5. Click **Add**
6. Click **Close**

### Step 2: Install Wyoming Porcupine (2 minutes)

1. Still in Add-on Store, click **Reload** (if repository just added)
2. Scroll down or search for: **Wyoming Porcupine**
3. Click on **Wyoming Porcupine**
4. Click **Install** (will take 1-2 minutes)
5. Wait for "Successfully installed" message

### Step 3: Configure (1 minute)

1. After installation, click **Configuration** tab
2. You'll see:

```yaml
# Add your config here
```

3. For now, use a built-in wake word for testing. Add this:

```yaml
keywords:
  - computer
sensitivity: 0.5
debug: true
```

4. Click **Save**

### Step 4: Start the Add-on (30 seconds)

1. Go to **Info** tab
2. Turn on **Start on boot**
3. Click **Start**
4. Go to **Log** tab
5. Should see:
   ```
   [INFO] Starting Wyoming Porcupine
   [INFO] Porcupine initialized
   [INFO] Ready
   ```

### Step 5: Add to Home Assistant (1 minute)

1. Go to **Settings** → **Devices & Services**
2. You should see **Wyoming discovered** notification
3. Click **Configure**
4. Click **Submit**

OR if not auto-discovered:

1. Click **+ Add Integration**
2. Search: `wyoming`
3. Select **Wyoming Protocol**
4. Enter:
   - Host: `core-wyoming-porcupine`
   - Port: `10400`
5. Click **Submit**

### Step 6: Test It! (30 seconds)

1. Go to **Settings** → **Voice Assistants**
2. Edit your assistant:
   - **Wake word**: Select **computer**
3. Click **Update**
4. Click **Debug** button
5. Say: **"Computer"**
6. Should see: ✅ `Wake word detected: computer`

## ✅ Installation Complete!

Your Home Assistant now has wake word detection running locally!

---

## Next Step: Train "Albert" Custom Wake Word

### Get Picovoice Access Key

1. Go to: https://console.picovoice.ai/
2. Sign up (free)
3. Account → Access Keys → Create New Key
4. Copy the key (save it!)

### Train "Albert"

1. In Picovoice Console, click **Porcupine**
2. Click **Train Wake Word**
3. Enter:
   - Wake Phrase: `albert`
   - Language: English
4. Click **Train**
5. Wait 3-5 minutes
6. Click **Download** → save `albert.ppn`

### Upload to Home Assistant

1. In Home Assistant, install **File Editor** add-on (if not installed)
   - Settings → Add-ons → Add-on Store → File Editor → Install
2. Open File Editor
3. Click folder icon → Navigate to `/share`
4. Create folder: `porcupine`
5. Click into `porcupine` folder
6. Upload `albert.ppn` file

### Update Wyoming Porcupine Configuration

1. Settings → Add-ons → Wyoming Porcupine → Configuration
2. Replace the config with:

```yaml
access_key: "YOUR_PICOVOICE_ACCESS_KEY_HERE"
keyword_paths:
  - /share/porcupine/albert.ppn
sensitivity: 0.5
debug: false
```

3. Click **Save**
4. Go to **Info** tab → Click **Restart**
5. Check **Log** tab → Should see "Loaded custom keyword: albert"

### Update Voice Assistant

1. Settings → Voice Assistants → Edit your assistant
2. Change **Wake word** to: **albert**
3. Click **Update**

### Test "Albert"

1. Say: **"Albert"**
2. Then say: **"Wéi speet ass et?"**
3. Should respond with time in Luxembourgish! 🎉

---

## Troubleshooting

### "Computer" doesn't detect
- Increase sensitivity to 0.7
- Check microphone in Settings → System → Audio

### Can't find Wyoming Porcupine
- Make sure you added repository: https://github.com/rhasspy/hassio-addons
- Refresh the add-on store
- Search for "wyoming"

### Albert.ppn not working
- Verify file uploaded to /share/porcupine/
- Check access key is correct
- Restart add-on after config change
- Check logs for errors

### Need Help?
Check the full guide: `INSTALL-HA-NATIVE.md`

---

**Total time**: 5-10 minutes for built-in wake word
**+10 minutes**: To train and deploy custom "Albert" wake word
**Difficulty**: Easy ⭐
**Recommended**: ✅ This is the best method for Porcupine!
