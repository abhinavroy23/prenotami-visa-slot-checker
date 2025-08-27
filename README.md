# 🎯 VISA Slot Monitor

**Browser-based monitor for Italian embassy VISA appointments on prenotami.esteri.it**

**✨ Super Simple Approach:** You login manually, the monitor runs in your browser session - no cookies, no bot detection!

## ⚠️ **IMPORTANT: Responsible Usage Warning**

**🚨 PLEASE READ BEFORE USING:**

- **📊 DEFAULT: 5-minute intervals** - Do NOT decrease below 5 minutes to avoid server overload
- **🤝 BE RESPECTFUL** - The embassy servers are shared resources for everyone
- **📈 REASONABLE LIMITS** - Excessive requests can hurt everyone's access
- **🔄 CONSIDER OTHERS** - Other applicants also need access to the system
- **⚖️ YOUR RESPONSIBILITY** - You are responsible for complying with the website's terms of service
- **🚫 NO SPAMMING** - This tool is for legitimate monitoring, not server abuse

**Recommended Settings:**
- ✅ **CHECK_INTERVAL=300** (5 minutes) - Default and recommended
- ✅ **CHECK_INTERVAL=600** (10 minutes) - Even more considerate  
- ❌ **CHECK_INTERVAL<300** - Please avoid shorter intervals

**⚖️ Legal Notice:** This tool is for educational purposes. Users must comply with prenotami.esteri.it's terms of service and applicable laws. Use responsibly and respectfully.

---

## 🚀 Quick Start

```bash
# 1. Start the monitor (opens browser automatically)
python3 browser_monitor.py

# 2. Login manually in the browser window that opens
# 3. Press Enter in terminal when logged in  
# 4. Monitor starts automatically checking every 5 minutes!
```

## ✨ Key Features

- ✅ **No bot detection** - Uses your real browser session
- ✅ **Manual login** - You login once, monitor takes over
- ✅ **24/7 monitoring** - Checks every 5 minutes automatically  
- ✅ **Instant alerts** - Email + desktop notifications + screenshots
- ✅ **Peak time aware** - Knows embassy release schedule
- ✅ **Smart detection** - Detects when booking form appears
- ✅ **Ready to book** - Browser stays on booking page when slots found
- ✅ **Continuous operation** - Catches cancelled slots anytime

## 📋 How It Works

1. **Script opens Chrome** with your session (no cookies needed!)
2. **You login manually** in the browser window (just once)
3. **Monitor takes over** and checks booking page every 5 minutes
4. **When slots appear** → Booking form detected → Instant alerts sent
5. **You book immediately** in the same browser window that's ready

## ⚡ Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Email Notifications
Edit `.env` file with your Gmail settings:
```bash
SENDER_EMAIL=your_gmail@gmail.com
SENDER_PASSWORD=your_app_password  # Gmail App Password (see below)
RECEIVER_EMAIL=your_email@gmail.com
CHECK_INTERVAL=300  # 5 minutes - RECOMMENDED MINIMUM (do not go lower)
```

**⚠️ CHECK_INTERVAL Guidelines:**
- ✅ **300 (5 minutes)** - Default, recommended minimum
- ✅ **600 (10 minutes)** - More considerate, still effective  
- ✅ **900 (15 minutes)** - Very respectful for off-peak monitoring
- ❌ **<300 (<5 minutes)** - Please avoid to prevent server overload

### 3. Gmail App Password Setup
1. **Enable 2-Factor Authentication** on your Google account
2. **Generate App Password**: Visit [Google App Passwords](https://myaccount.google.com/apppasswords)  
3. **Use app password** (not your regular password) in `SENDER_PASSWORD`
4. **Test email**: Run `python3 test_email.py` to verify setup

### 4. Start Monitoring
```bash
python3 browser_monitor.py
```

## 📱 What You'll See

### Initial Startup
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

### During Monitoring
```
✅ Login confirmed!

🎯 Starting continuous monitoring...
📋 Peak times: 3 PM, 10-11 PM, 7-9 AM Pacific
🔄 Also monitoring for cancelled slots (available anytime)
🖥️ Keep this terminal and browser window open

🔍 Check #1 at 13:15:30
🎯 Checking VISA booking slots...
📍 Navigating to: https://prenotami.esteri.it/Services/Booking/4755
❌ On booking page but no booking form detected
⏳ Next check #2 at 13:20:30 (in 300 seconds)
================================================================
```

### 🎉 When Slots Are Found!
```
🔍 Check #47 at 15:00:15
🎯 Checking VISA booking slots...
📍 Stayed on booking page - analyzing for slots...
🎉 SLOTS AVAILABLE! Booking form detected!
📊 Form analysis:
   • Forms: 1
   • Inputs: 8  
   • Buttons: 2
   • Name fields: 1
   • Email fields: 1
📸 Screenshot saved: slot_available_20250826_150015.png
🎉 SLOTS DETECTED! Sending alert...
📧 Alert sent successfully to your_email@gmail.com
🖥️ Desktop notification sent
🖥️ Browser is ready for booking - check the window!
```

**You'll get:**
- 📧 **Detailed email alert** with booking instructions
- 🖥️ **Desktop notification** (macOS popup)
- 🌐 **Browser positioned** on booking page ready to fill
- 📸 **Screenshot saved** as proof of availability

## ⏰ Embassy Release Schedule (Pacific Time)

Based on monitoring patterns:

- **🌅 7:00-9:00 AM** - Morning batch releases
- **🌞 3:00 PM** - Main afternoon release (highest activity)
- **🌙 10:00-11:00 PM** - Evening batch releases  
- **🔄 24/7 Continuous** - Cancelled appointments (can appear anytime)

**Pro Tip:** Peak times have more competition, but cancelled slots during off-hours are easier to grab!

## 🔧 Available Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| **`browser_monitor.py`** | Main monitoring script | `python3 browser_monitor.py` |
| **`start_monitor.py`** | Environment wrapper | `python3 start_monitor.py` |  
| **`launch_monitor.py`** | Guided setup launcher | `python3 launch_monitor.py` |
| **`run_monitor.sh`** | Shell script wrapper | `./run_monitor.sh` |
| **`test_email.py`** | Email configuration test | `python3 test_email.py` |

### Alternative Launchers

**For guided setup with debug mode:**
```bash
python3 launch_monitor.py
```
This opens Chrome in debug mode and walks you through the login process.

**For environment consistency:**
```bash
python3 start_monitor.py
```
This ensures correct Python environment and dependency handling.

## 🛠️ Troubleshooting

### Chrome/ChromeDriver Issues
- **Cache cleared automatically** when webdriver-manager fails
- **Multiple fallbacks** - System ChromeDriver → Auto-detection → Fresh download
- **Better error messages** for debugging

### Common Issues
1. **"Exec format error"** - Fixed automatically by clearing corrupted cache
2. **"Browser window closed"** - Restart monitor, don't close Chrome manually  
3. **"Not logged in"** - Login in browser window and press Enter in terminal
4. **Email not sending** - Run `python3 test_email.py` to verify Gmail setup

## 💡 Pro Tips

1. **Keep both windows open** - Terminal + Browser window
2. **Have booking info ready** - Passport details, preferred dates, contact info
3. **Act fast on alerts** - Slots typically disappear within 2-5 minutes
4. **Monitor 24/7** - Cancelled slots can appear at any time, even 3 AM
5. **Browser auto-navigates** - Just fill the form when you get an alert
6. **Multiple time zones** - Embassy releases follow Rome time but monitor shows Pacific
7. **Form validation** - Monitor confirms actual booking form elements, not just page loads

## 🔒 Privacy & Security

- **No credential storage** - You login manually each session
- **Local browser session** - Uses your existing Chrome profile
- **Email only** - Notifications go only to your configured email
- **Screenshot proof** - Automatic screenshots saved locally for verification
- **Open source** - All code visible and auditable

## 📊 Success Tips

**Preparation:**
- Have all documents scanned and ready
- Know your preferred appointment dates and times  
- Keep passport and contact information handy
- Set up multiple notification methods (email + phone notifications)

**During Monitoring:**
- Don't close the browser window or terminal
- Check email/notifications regularly during peak times
- Be ready to fill form within 2-3 minutes of alert
- Have backup dates in case first choice fills up

**When Slots Appear:**
- Click immediately when you get the alert
- Fill form completely and accurately  
- Double-check all information before submitting
- Take screenshots of confirmation page

## 🤝 Ethical Usage & Server Respect

**This tool comes with responsibility. Please:**

### 🌐 **Server Etiquette:**
- **Use default 5-minute intervals** - Shorter intervals stress embassy servers
- **Monitor during off-peak hours** when possible (late night, early morning)
- **Stop monitoring** once you successfully book an appointment
- **Don't run multiple instances** of the monitor simultaneously

### ⚖️ **Legal & Ethical Guidelines:**
- **Educational purpose** - This tool is for learning automation concepts
- **Terms of service** - You must comply with prenotami.esteri.it's terms
- **Fair access** - Don't monopolize server resources
- **Legitimate use only** - Only monitor for appointments you actually need

### 🚨 **What NOT to Do:**
- ❌ Don't set CHECK_INTERVAL below 300 seconds (5 minutes)
- ❌ Don't run multiple monitors for the same appointment type
- ❌ Don't continue monitoring after booking successfully  
- ❌ Don't share accounts or use this for commercial purposes
- ❌ Don't modify the code to make more aggressive requests

### 🌟 **Best Practices:**
- ✅ Use longer intervals during busy periods (10-15 minutes)
- ✅ Focus monitoring during known release times
- ✅ Stop the monitor when you don't need it
- ✅ Help others learn responsible automation practices
- ✅ Report any issues or improvements to the community

**Remember:** Embassy systems serve thousands of applicants. Your respectful usage helps ensure the system remains accessible for everyone. 🙏

---

## 🎯 Ready to Start?

**1. Test email configuration:**
```bash
python3 test_email.py
```

**2. Start monitoring:**
```bash  
python3 browser_monitor.py
```

**3. Login when prompted and press Enter**

**4. Let the monitor run 24/7 - it will alert you when slots appear!**

---

### 📞 Support

If you encounter issues:
1. Check the terminal output for detailed error messages
2. Verify email setup with `test_email.py`  
3. Ensure Chrome is updated to latest version
4. Review the `visa_monitor.log` file for debugging info

**Happy slot hunting!** 🎯✨
