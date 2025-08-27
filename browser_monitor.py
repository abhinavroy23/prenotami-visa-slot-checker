#!/usr/bin/env python3
"""
VISA Slot Monitor - Uses Existing Browser Session

This script connects to your already logged-in browser and monitors
the VISA booking page directly without any cookie extraction needed.
"""

import os
import time
import logging
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import subprocess

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('visa_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BrowserVisaMonitor:
    def __init__(self):
        """Initialize the browser-based VISA monitor."""
        load_dotenv()
        
        self.booking_url = "https://prenotami.esteri.it/Services/Booking/4755"
        self.services_url = "https://prenotami.esteri.it/Services/"
        
        # Email configuration
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD') 
        self.receiver_email = os.getenv('RECEIVER_EMAIL')
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        
        # Monitoring configuration with responsible usage enforcement
        requested_interval = int(os.getenv('CHECK_INTERVAL', 300))
        minimum_interval = 300  # 5 minutes minimum for server respect
        
        if requested_interval < minimum_interval:
            logger.warning(f"⚠️ Requested interval {requested_interval}s is too aggressive!")
            logger.warning(f"🤝 Enforcing minimum {minimum_interval}s (5 minutes) for server respect")
            logger.warning("📖 Please read the README about responsible usage")
            self.check_interval = minimum_interval
        else:
            self.check_interval = requested_interval
            
        logger.info(f"⏰ Check interval set to {self.check_interval} seconds ({self.check_interval//60} minutes)")
        self.driver = None

    def setup_browser(self):
        """Connect to existing browser or create new session."""
        try:
            logger.info("🌐 Setting up browser connection...")
            logger.info("⚙️ Configuring Chrome options...")
            
            chrome_options = Options()
            chrome_options.add_argument("--user-data-dir=/tmp/chrome-visa-monitor")
            chrome_options.add_argument("--no-first-run")
            chrome_options.add_argument("--no-default-browser-check")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument("--no-sandbox")  # Help prevent crashes
            chrome_options.add_argument("--disable-dev-shm-usage")  # Help prevent crashes
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_experimental_option("detach", True)  # Keep browser open when script ends
            
            logger.info("🔍 Attempting to connect to ChromeDriver...")
            
            # Try to use system Chrome first
            try:
                service = Service("/opt/homebrew/bin/chromedriver")
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                logger.info("✅ Using system ChromeDriver at /opt/homebrew/bin/chromedriver")
            except Exception as e1:
                logger.info(f"ℹ️ System ChromeDriver failed: {str(e1)}")
                try:
                    # Try without explicit service path
                    self.driver = webdriver.Chrome(options=chrome_options)
                    logger.info("✅ Using Chrome with automatic driver detection")
                except Exception as e2:
                    logger.info(f"ℹ️ Automatic detection failed: {str(e2)}")
                    # Clear webdriver-manager cache and try again
                    logger.info("🧹 Clearing ChromeDriver cache...")
                    try:
                        import shutil
                        cache_path = os.path.expanduser("~/.wdm")
                        if os.path.exists(cache_path):
                            shutil.rmtree(cache_path)
                            logger.info("✅ Cache cleared")
                    except Exception as cache_error:
                        logger.warning(f"⚠️ Could not clear cache: {cache_error}")
                    
                    # Try webdriver-manager with fresh download
                    logger.info("🔄 Downloading fresh ChromeDriver...")
                    try:
                        driver_path = ChromeDriverManager().install()
                        logger.info(f"📍 Downloaded driver to: {driver_path}")
                        
                        # Verify the downloaded file is executable
                        if os.path.exists(driver_path) and os.access(driver_path, os.X_OK):
                            service = Service(driver_path)
                            self.driver = webdriver.Chrome(service=service, options=chrome_options)
                            logger.info("✅ Using downloaded ChromeDriver")
                        else:
                            logger.error(f"❌ Downloaded driver is not executable: {driver_path}")
                            raise Exception("ChromeDriver not executable")
                    except Exception as wdm_error:
                        logger.error(f"❌ WebDriver Manager failed: {wdm_error}")
                        # Final fallback - try to find Chrome in common locations
                        chrome_locations = [
                            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                            "/usr/bin/google-chrome",
                            "/usr/local/bin/chromedriver"
                        ]
                        
                        logger.info("🔍 Trying alternative Chrome locations...")
                        for location in chrome_locations:
                            if os.path.exists(location):
                                logger.info(f"📍 Found Chrome at: {location}")
                                break
                        
                        raise Exception("All ChromeDriver methods failed")
            
            # Configure browser to avoid detection
            logger.info("🛡️ Applying anti-detection measures...")
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # Set window size to prevent issues
            self.driver.set_window_size(1200, 800)
            
            # Navigate to prenotami homepage
            logger.info("🌐 Opening Prenotami website...")
            self.driver.get("https://prenotami.esteri.it/")
            logger.info("✅ Browser setup complete")
            
            # Add a small delay to ensure page loads
            time.sleep(2)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to setup browser: {str(e)}")
            if hasattr(self, 'driver') and self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
            return False

    def ensure_logged_in(self):
        """Check if user is logged in, if not prompt them to login."""
        try:
            # Check if browser is still alive
            if not self.driver:
                logger.error("❌ Browser driver is not available")
                return False
                
            # Test if browser window is still open
            try:
                current_handles = self.driver.window_handles
                if not current_handles:
                    logger.error("❌ Browser window has been closed")
                    return False
            except Exception as e:
                logger.error(f"❌ Cannot access browser window: {str(e)}")
                logger.info("� The browser window may have been closed manually")
                return False
            
            logger.info("�🔍 Checking login status...")
            logger.info(f"📍 Navigating to: {self.services_url}")
            
            # Navigate to services page
            self.driver.get(self.services_url)
            time.sleep(3)
            
            # Get current URL safely
            try:
                current_url = self.driver.current_url
                if current_url:
                    current_url = current_url.lower()
                    logger.info(f"📍 Current URL: {self.driver.current_url}")
                else:
                    logger.error("❌ Could not get current URL - browser may be in bad state")
                    return False
            except Exception as e:
                logger.error(f"❌ Failed to get current URL: {str(e)}")
                return False
            
            # Get page content safely
            try:
                page_content = self.driver.page_source
                if page_content:
                    page_content = page_content.lower()
                else:
                    logger.error("❌ Could not get page content - browser may be in bad state")
                    return False
            except Exception as e:
                logger.error(f"❌ Failed to get page content: {str(e)}")
                return False
            
            logger.info("🔍 Analyzing page for login indicators...")
            
            # Check for login indicators
            login_indicators = ['services', 'prenota', 'book', 'logout']
            logged_in_signs = [indicator for indicator in login_indicators if indicator in page_content]
            logger.info(f"✅ Login indicators found: {', '.join(logged_in_signs) if logged_in_signs else 'None'}")
            
            # Check if we're on login page
            not_logged_indicators = ['login', 'accedi', 'sign in']
            not_logged_signs = [indicator for indicator in not_logged_indicators if indicator in page_content or indicator in current_url]
            logger.info(f"❌ Not-logged indicators found: {', '.join(not_logged_signs) if not_logged_signs else 'None'}")
            
            is_logged_in = len(logged_in_signs) > 0 and len(not_logged_signs) == 0
            
            if not is_logged_in:
                logger.info("⚠️ Not logged in - please login manually")
                print("\n" + "="*60)
                print("🔐 LOGIN REQUIRED")
                print("="*60)
                print("Please login to Prenotami in the browser window that just opened:")
                print("1. Complete the login process")
                print("2. Navigate to Services page")
                print("3. Verify you can see your available services")
                print("4. Come back here and press Enter when ready")
                print("="*60)
                
                input("Press Enter when you have completed login...")
                
                # Recheck after user confirms
                logger.info("🔄 Rechecking login status after user confirmation...")
                self.driver.refresh()
                time.sleep(3)
                
                page_content = self.driver.page_source.lower()
                logged_in_signs = [indicator for indicator in login_indicators if indicator in page_content]
                
                if len(logged_in_signs) > 0:
                    logger.info(f"✅ Login confirmed! Found: {', '.join(logged_in_signs)}")
                    return True
                else:
                    logger.error("❌ Still not logged in")
                    return False
            else:
                logger.info("✅ Already logged in!")
                logger.info(f"🎯 Confirmed by: {', '.join(logged_in_signs)}")
                return True
                
        except Exception as e:
            logger.error(f"❌ Error checking login: {str(e)}")
            logger.info("💡 This often happens when the browser window is closed")
            return False

    def check_visa_slots(self):
        """Check if VISA slots are available."""
        try:
            logger.info("🎯 Checking VISA booking slots...")
            logger.info(f"📍 Navigating to: {self.booking_url}")
            
            # Navigate to booking page
            start_time = time.time()
            self.driver.get(self.booking_url)
            
            logger.info("⏳ Waiting for page to load...")
            time.sleep(3)
            load_time = time.time() - start_time
            
            current_url = self.driver.current_url.lower()
            logger.info(f"📍 Final URL: {self.driver.current_url}")
            logger.info(f"⌛ Page load time: {load_time:.1f}s")
            
            # Get page title for additional context
            try:
                page_title = self.driver.title
                logger.info(f"📄 Page title: {page_title}")
            except:
                logger.warning("⚠️ Could not get page title")
            
            # Check if we stayed on the booking page
            if "booking/4755" in current_url:
                logger.info("✅ Stayed on booking page - analyzing for slots...")
                
                # Look for booking form elements
                try:
                    logger.info("🔍 Analyzing page content for booking form...")
                    
                    # Wait a bit for page to fully load
                    time.sleep(2)
                    
                    # Look for form elements
                    form_elements = self.driver.find_elements(By.TAG_NAME, "form")
                    input_elements = self.driver.find_elements(By.TAG_NAME, "input")
                    submit_buttons = self.driver.find_elements(By.CSS_SELECTOR, "input[type='submit'], button[type='submit'], .btn-submit")
                    
                    logger.info(f"📋 Found {len(form_elements)} form(s)")
                    logger.info(f"📝 Found {len(input_elements)} input field(s)")
                    logger.info(f"🔘 Found {len(submit_buttons)} submit button(s)")
                    
                    # Look for typical booking form fields
                    name_fields = self.driver.find_elements(By.CSS_SELECTOR, "input[name*='name'], input[name*='Name'], input[id*='name'], input[id*='Name']")
                    email_fields = self.driver.find_elements(By.CSS_SELECTOR, "input[type='email'], input[name*='email'], input[name*='Email']")
                    phone_fields = self.driver.find_elements(By.CSS_SELECTOR, "input[name*='phone'], input[name*='Phone'], input[type='tel']")
                    
                    logger.info(f"👤 Found {len(name_fields)} name field(s)")
                    logger.info(f"📧 Found {len(email_fields)} email field(s)")
                    logger.info(f"📞 Found {len(phone_fields)} phone field(s)")
                    
                    # Check for booking-specific text
                    page_text = self.driver.page_source.lower()
                    booking_keywords = ['book', 'prenota', 'appointment', 'appuntamento', 'slot', 'available']
                    found_keywords = [word for word in booking_keywords if word in page_text]
                    logger.info(f"🔤 Booking keywords found: {', '.join(found_keywords) if found_keywords else 'None'}")
                    
                    has_booking_form = (
                        len(form_elements) > 0 and 
                        len(input_elements) > 3 and  # More than just basic inputs
                        (len(submit_buttons) > 0 or len(name_fields) > 0 or len(email_fields) > 0)
                    )
                    
                    if has_booking_form:
                        logger.info("🎉 SLOTS AVAILABLE! Booking form detected!")
                        logger.info("📊 Form analysis:")
                        logger.info(f"   • Forms: {len(form_elements)}")
                        logger.info(f"   • Inputs: {len(input_elements)}")  
                        logger.info(f"   • Buttons: {len(submit_buttons)}")
                        logger.info(f"   • Name fields: {len(name_fields)}")
                        logger.info(f"   • Email fields: {len(email_fields)}")
                        
                        # Take a screenshot for verification
                        try:
                            screenshot_path = f"slot_available_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                            self.driver.save_screenshot(screenshot_path)
                            logger.info(f"📸 Screenshot saved: {screenshot_path}")
                        except Exception as e:
                            logger.warning(f"⚠️ Could not save screenshot: {str(e)}")
                        
                        return True
                    else:
                        logger.info("❌ On booking page but no booking form detected")
                        logger.info("📊 Analysis summary:")
                        logger.info(f"   • Forms: {len(form_elements)} (need > 0)")
                        logger.info(f"   • Inputs: {len(input_elements)} (need > 3)")
                        logger.info(f"   • Submit buttons: {len(submit_buttons)}")
                        logger.info(f"   • Booking fields: {len(name_fields) + len(email_fields)}")
                        return False
                        
                except Exception as e:
                    logger.warning(f"⚠️ Error checking form elements: {str(e)}")
                    # Fallback: check page content
                    logger.info("🔄 Falling back to content-based detection...")
                    page_content = self.driver.page_source.lower()
                    form_indicators = ['first name', 'last name', 'email', 'phone', 'submit', 'confirm', 'book']
                    
                    found_indicators = []
                    for indicator in form_indicators:
                        if indicator in page_content:
                            found_indicators.append(indicator)
                    
                    logger.info(f"🔤 Content indicators found: {', '.join(found_indicators) if found_indicators else 'None'}")
                    
                    has_form = len(found_indicators) >= 2  # Need at least 2 indicators
                    
                    if has_form:
                        logger.info("🎉 SLOTS AVAILABLE! (Detected via page content)")
                        logger.info(f"📊 Found indicators: {', '.join(found_indicators)}")
                        return True
                    else:
                        logger.info("❌ No booking form detected in page content")
                        logger.info(f"📊 Only found: {', '.join(found_indicators) if found_indicators else 'No booking indicators'}")
                        return False
            
            # Check if redirected to services page (no slots)
            elif "services" in current_url:
                logger.info("❌ Redirected to services page - No slots available")
                logger.info("🔍 Analyzing redirect reason...")
                
                # Look for the "all booked" message
                try:
                    page_content = self.driver.page_source.lower()
                    no_slots_messages = [
                        'all appointments', 'fully booked', 'no availability',
                        'non ci sono', 'tutto prenotato', 'esaurito', 'disponibilità'
                    ]
                    
                    found_messages = []
                    for msg in no_slots_messages:
                        if msg in page_content:
                            found_messages.append(msg)
                    
                    if found_messages:
                        logger.info(f"💬 No-slots messages found: {', '.join(found_messages)}")
                        logger.info("✅ Confirmed: All appointments currently booked")
                    else:
                        logger.info("📄 No specific 'booked' message found")
                        logger.info("💭 Redirect likely means no availability")
                        
                    # Check page title for additional context
                    try:
                        page_title = self.driver.title
                        if 'service' in page_title.lower():
                            logger.info(f"📄 Services page confirmed: {page_title}")
                    except:
                        pass
                        
                except Exception as e:
                    logger.warning(f"⚠️ Could not analyze services page: {str(e)}")
                
                return False
            
            else:
                logger.warning(f"⚠️ Unexpected redirect to: {self.driver.current_url}")
                logger.warning("🤔 This URL pattern was not expected")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error checking slots: {str(e)}")
            return False

    def send_alert(self, slots_available=True):
        """Send email alert about slot availability."""
        try:
            if not all([self.sender_email, self.sender_password, self.receiver_email]):
                logger.warning("⚠️ Email not configured - skipping notification")
                return False
            
            logger.info("📧 Preparing email notification...")
            
            if slots_available:
                subject = "🎉 VISA SLOTS AVAILABLE - Book Now!"
                body = f"""
                <html>
                <body>
                    <h2 style="color: green;">🎉 VISA APPOINTMENT SLOTS AVAILABLE!</h2>
                    
                    <p><strong>⏰ Detection Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S PST')}</p>
                    <p><strong>🎯 Booking URL:</strong> <a href="{self.booking_url}">Click here to book immediately</a></p>
                    
                    <h3>🚨 URGENT ACTION REQUIRED:</h3>
                    <ol>
                        <li><strong>Go to your browser window (should already be open)</strong></li>
                        <li><strong>The booking form should be visible</strong></li>
                        <li><strong>Fill out and submit immediately</strong></li>
                    </ol>
                    
                    <p><strong>💡 Tips:</strong></p>
                    <ul>
                        <li>The monitor already navigated to the booking page</li>
                        <li>Form should be ready to fill</li>
                        <li>Have your passport and details ready</li>
                        <li>Submit quickly - slots disappear in minutes!</li>
                    </ul>
                    
                    <hr>
                    <p><small>🤖 VISA Slot Monitor - Browser Session<br>
                    Alert time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small></p>
                </body>
                </html>
                """
            else:
                subject = "⚠️ VISA Monitor Needs Attention"
                body = f"""
                <html>
                <body>
                    <h2>⚠️ Monitor Session Issue</h2>
                    <p>Your VISA slot monitor has detected a session issue.</p>
                    <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S PST')}</p>
                    <p><strong>Action:</strong> Please check the browser window and ensure you're still logged in.</p>
                </body>
                </html>
                """
            
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.receiver_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html'))
            
            logger.info(f"📤 Connecting to {self.smtp_server}:{self.smtp_port}...")
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            logger.info("🔐 Authenticating...")
            server.login(self.sender_email, self.sender_password)
            
            text = msg.as_string()
            server.sendmail(self.sender_email, self.receiver_email, text)
            server.quit()
            
            logger.info(f"✅ Alert sent successfully to {self.receiver_email}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to send alert: {str(e)}")
            return False

    def run_monitor(self):
        """Run the continuous monitoring loop."""
        logger.info("🚀 Starting Browser-Based VISA Monitor")
        logger.info(f"🎯 Target: VISA booking slots (ID: 4755)")
        logger.info(f"⏰ Check interval: {self.check_interval} seconds ({self.check_interval//60} minutes)")
        logger.info(f"📧 Notifications: {'Enabled' if self.sender_email else 'Disabled'}")
        logger.info(f"📧 Email: {self.sender_email} → {self.receiver_email}")
        
        consecutive_errors = 0
        max_errors = 3
        check_count = 0
        
        try:
            while True:
                check_count += 1
                current_time = datetime.now().strftime('%H:%M:%S')
                logger.info(f"🔍 Check #{check_count} at {current_time}")
                
                # Periodically verify we're still logged in
                if consecutive_errors > 0:
                    logger.info("🔄 Verifying login status due to previous errors...")
                    if not self.ensure_logged_in():
                        consecutive_errors += 1
                        logger.error(f"❌ Login verification failed (error {consecutive_errors}/{max_errors})")
                        if consecutive_errors >= max_errors:
                            logger.error("❌ Too many login failures - sending alert")
                            self.send_alert(slots_available=False)
                            break
                        logger.info(f"⏳ Waiting {self.check_interval} seconds before retry...")
                        time.sleep(self.check_interval)
                        continue
                
                # Check for slots
                try:
                    logger.info("🎯 Starting slot availability check...")
                    slots_available = self.check_visa_slots()
                    
                    if slots_available:
                        logger.info("🎉 SLOTS DETECTED! Sending alert...")
                        alert_sent = self.send_alert(slots_available=True)
                        
                        if alert_sent:
                            logger.info("✅ Alert sent successfully")
                        else:
                            logger.warning("⚠️ Alert sending failed")
                        
                        # Desktop notification
                        try:
                            logger.info("🖥️ Showing desktop notification...")
                            subprocess.run([
                                'osascript', '-e',
                                'display notification "VISA slots available! Check browser window!" with title "🎉 VISA SLOTS FOUND!"'
                            ])
                            logger.info("✅ Desktop notification sent")
                        except Exception as e:
                            logger.warning(f"⚠️ Desktop notification failed: {str(e)}")
                            print('\a' * 5)  # System beep fallback
                        
                        # Keep browser on booking page for user
                        logger.info("🖥️ Browser is ready for booking - check the window!")
                        
                        # Wait longer after finding slots
                        wait_time = self.check_interval * 3
                        logger.info(f"⏳ Waiting {wait_time} seconds ({wait_time//60} minutes) after alert...")
                        time.sleep(wait_time)
                    else:
                        logger.info("❌ No slots available at this time")
                        consecutive_errors = 0  # Reset on successful check
                        
                except Exception as e:
                    consecutive_errors += 1
                    logger.error(f"❌ Slot check failed (error {consecutive_errors}/{max_errors}): {str(e)}")
                    if consecutive_errors >= max_errors:
                        logger.error("❌ Too many consecutive errors - sending alert")
                        self.send_alert(slots_available=False)
                        break
                
                # Wait before next check
                next_check = datetime.now() + timedelta(seconds=self.check_interval)
                logger.info(f"⏳ Next check #{check_count + 1} at {next_check.strftime('%H:%M:%S')} (in {self.check_interval} seconds)")
                logger.info("=" * 60)
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            logger.info("🛑 Monitor stopped by user (Ctrl+C)")
        except Exception as e:
            logger.error(f"❌ Fatal error: {str(e)}")
            self.send_alert(slots_available=False)
        finally:
            if self.driver:
                logger.info("🔒 Keeping browser open for manual use")
                # Don't close the driver - keep it open for user

def main():
    """Main function."""
    print("🎯 VISA Slot Monitor - Browser Session")
    print("=" * 50)
    print()
    
    monitor = BrowserVisaMonitor()
    
    # Setup browser
    if not monitor.setup_browser():
        print("❌ Failed to setup browser")
        return
    
    print("🌐 Browser connected!")
    print()
    
    # Ensure user is logged in
    if not monitor.ensure_logged_in():
        print("❌ Login required - please login and try again")
        return
    
    print("✅ Login confirmed!")
    print()
    print("🎯 Starting continuous monitoring...")
    print("📋 Peak times: 3 PM, 10-11 PM, 7-9 AM Pacific")
    print("🔄 Also monitoring for cancelled slots (available anytime)")
    print("🖥️ Keep this terminal and browser window open")
    print()
    
    # Start monitoring
    monitor.run_monitor()

if __name__ == "__main__":
    main()
