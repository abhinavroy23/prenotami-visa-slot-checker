# 🎯 Browser-Based VISA Monitor

## 🚀 **Super Simple Setup**

**No cookies to extract! Just login manually and let the monitor run.**

### **Quick Start**

```bash
# 1. Start the monitor (opens browser automatically)
python3 browser_monitor.py

# 2. Login to Prenotami in the browser window
# 3. Press Enter in terminal when logged in
# 4. Monitor starts automatically!
```

## 🎯 **How It Works**

1. **Script opens Chrome** with your existing session
2. **You login manually** (one time) 
3. **Monitor takes over** and checks every 5 minutes
4. **When slots appear** → Instant email alert + browser shows booking form
5. **You book immediately** in the same browser window

## 📋 **What You'll See**

```
🎯 VISA Slot Monitor - Browser Session
==================================================

🌐 Browser connected!

🔍 Checking login status...
⚠️ Not logged in - please login manually
============================================================
🔐 LOGIN REQUIRED  
============================================================
Please login to Prenotami in the browser window that just opened:
1. Complete the login process
2. Navigate to Services page  
3. Verify you can see your available services
4. Come back here and press Enter when ready
============================================================

Press Enter when you have completed login...
```

After login:
```
✅ Login confirmed!

🎯 Starting continuous monitoring...
📋 Peak times: 3 PM, 10-11 PM, 7-9 AM Pacific
🔄 Also monitoring for cancelled slots (available anytime)
🖥️ Keep this terminal and browser window open

🔍 Checking at 13:15:30
🎯 Checking VISA booking slots...
📍 Current URL: https://prenotami.esteri.it/Services/
❌ Redirected to services page - No slots available
⏳ Next check in 300 seconds...
```

## 🎉 **When Slots Are Found**

```
🔍 Checking at 15:00:15
🎯 Checking VISA booking slots...
📍 Current URL: https://prenotami.esteri.it/Services/Booking/4755
🎉 SLOTS AVAILABLE! Booking form detected!
📸 Screenshot saved: slot_available_20250826_150015.png
🎉 SLOTS DETECTED! Sending alert...
📧 Alert sent to your_email@gmail.com
🖥️ Browser is ready for booking - check the window!
```

**Plus:**
- 📧 **Email alert** with booking instructions
- 🖥️ **Desktop notification** (macOS popup)
- 📸 **Screenshot** saved as proof
- 🌐 **Browser stays on booking page** ready to fill

## ⚡ **Key Benefits**

- ✅ **No cookie extraction** - just login manually
- ✅ **Uses your real browser session** - no bot detection
- ✅ **Continuous monitoring** - catches cancelled slots anytime
- ✅ **Smart detection** - knows when booking form appears
- ✅ **Instant alerts** - email + desktop notifications
- ✅ **Ready to book** - browser stays on booking page
- ✅ **Peak time aware** - monitors embassy release schedule

## 🔧 **Requirements**

- Python 3.9+ (already installed ✅)
- Chrome browser (already installed ✅)
- Email configured in `.env` (already configured ✅)

## 📧 **Email Setup**

Your `.env` already has:
```bash
SENDER_EMAIL=abhinav.roy23@gmail.com
SENDER_PASSWORD=qksz lvij xior hfbu
RECEIVER_EMAIL=abhinav.roy23@gmail.com
CHECK_INTERVAL=300  # 5 minutes
```

## 🎯 **Peak Monitoring Times**

- **🌅 7:00-9:00 AM Pacific** - Morning releases
- **🌞 3:00 PM Pacific** - Main afternoon batch  
- **🌙 10:00-11:00 PM Pacific** - Evening batch
- **🔄 24/7 Continuous** - Cancelled slots (anytime)

## 💡 **Pro Tips**

1. **Keep both windows open** - Terminal + Browser
2. **Have booking info ready** - Passport, dates, etc.
3. **Act fast on alerts** - Slots disappear in 2-5 minutes
4. **Monitor runs 24/7** - Catches cancelled slots anytime
5. **Browser auto-navigates** - Just fill the form when alerted

## 🚀 **Alternative Launcher**

For even easier startup:
```bash
python3 launch_monitor.py
```

This opens Chrome automatically and guides you through login.

---

### 🎉 **Ready to Monitor?**

```bash
python3 browser_monitor.py
```

**The monitor will:**
1. Open Chrome browser
2. Wait for your manual login
3. Start monitoring automatically  
4. Alert you instantly when slots appear
5. Keep browser ready for booking

**No cookie extraction, no complex setup - just login and go!** 🎯
