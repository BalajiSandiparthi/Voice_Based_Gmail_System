import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import threading

def send_email(to, subject, body, from_address, password):
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_address, password)
        server.sendmail(from_address, to, msg.as_string())
        server.quit()
    except Exception as e:
        print("Error: " + str(e))
        

def send_email_thread(to, subject, body, from_address, password, send_time):
    now = datetime.now()
    send_time = datetime.strptime(send_time, '%Y-%m-%d %H:%M:%S')
    delay = (send_time - now).total_seconds()
    if delay < 0:
        print("Error: send time is in the past.")
    else:
        time.sleep(delay)
        send_email(to, subject, body, from_address, password)


