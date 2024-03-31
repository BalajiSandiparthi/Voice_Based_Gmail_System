import imaplib
import email
import smtplib
from email.message import EmailMessage
import time

def draft(subject,email_from,email_to,body,passw):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email_from
    msg['To'] = email_to
    msg.set_content(body)

    imap_server = 'imap.gmail.com'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    username = email_from
    password = passw
    mail = imaplib.IMAP4_SSL(imap_server)
    server = smtplib.SMTP(smtp_server, smtp_port)

    mail.login(username, password)
    server.starttls()
    server.login(username, password)

    mail.select('[Gmail]/Drafts')
    server.send_message(msg)
    mail.append('[Gmail]/Drafts', '', imaplib.Time2Internaldate(time.time()), str(msg).encode('utf-8'))

    mail.close()
    mail.logout()
    server.quit()

