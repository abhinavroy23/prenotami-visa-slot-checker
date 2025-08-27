# VISA Slot Monitor 🎯

Browser-based monitor for Italian embassy VISA appointments on prenotami.esteri.it.

**Simple approach: You login manually, the monitor runs in your browser session!**

## 🚀 Quick Start

```bash
# 1. Run the monitor (opens browser automatically)
python3 browser_monitor.py

# 2. Login manually in the browser window
# 3. Press Enter when logged in
# 4. Monitor starts automatically!
```

## ✨ Features

- ✅ **No bot detection** - Uses your real browser session
- ✅ **Manual login** - You login once, monitor takes over
- ✅ **24/7 monitoring** - Checks every 5 minutes automatically  
- ✅ **Instant alerts** - Email + desktop notifications
- ✅ **Peak time aware** - Knows embassy release schedule
- ✅ **Smart detection** - Detects when booking form appears
- ✅ **Ready to book** - Browser stays on booking page when slots found

## 📋 How It Works

1. **Script opens Chrome** with your session
2. **You login manually** (just once)
3. **Monitor checks booking page** every 5 minutes
4. **When slots appear** → Booking form detected → Instant alert
5. **You book immediately** in the same browser window

## ⚡ Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Email Notifications
Edit `.env` file:
```bash
SENDER_EMAIL=your_gmail@gmail.com
SENDER_PASSWORD=your_app_password  # Gmail App Password
RECEIVER_EMAIL=your_email@gmail.com
CHECK_INTERVAL=300  # 5 minutes
```

### 3. Run Monitor
```bash
python3 browser_monitor.py
```

## 📧 Email Setup (Gmail)

1. Enable 2-Factor Authentication
2. Generate App Password: [Google App Passwords](https://myaccount.google.com/apppasswords)  
3. Use app password in `SENDER_PASSWORD`
4. Test with: `python3 test_email.py`

## ⏰ Peak Release Times (Pacific)

- **🌅 7:00-9:00 AM** - Morning batch
- **🌞 3:00 PM** - Main afternoon release  
- **🌙 10:00-11:00 PM** - Evening batch
- **🔄 24/7** - Cancelled slots (available anytime)

## 🎯 What Happens When Slots Are Found

```
🎉 SLOTS AVAILABLE! Booking form detected!
📧 Alert sent to your_email@gmail.com
🖥️ Browser is ready for booking - check the window!
```

**You get:**
- 📧 **Email alert** with booking instructions
- 🖥️ **Desktop notification** (macOS popup)
- 🌐 **Browser on booking page** ready to fill
- 📸 **Screenshot** saved as proof

## 🔧 Files

- `browser_monitor.py` - Main monitoring script
- `launch_monitor.py` - Alternative launcher with guided setup
- `test_email.py` - Test email notifications
- `BROWSER_MONITOR_GUIDE.md` - Detailed setup guide
- `.env` - Configuration file

## 💡 Pro Tips

- **Keep terminal and browser open** while monitoring
- **Have booking info ready** (passport, dates, etc.)
- **Act fast on alerts** - Slots disappear in 2-5 minutes
- **Monitor runs 24/7** - Catches cancelled slots anytime
- **Browser auto-navigates** - Just fill form when alerted

## 🚀 Alternative Launcher

For guided setup:
```bash
python3 launch_monitor.py
```

This opens Chrome with debug mode and walks you through login.

---

**Ready to catch those VISA slots?** 🎯

```bash
python3 browser_monitor.py
```
