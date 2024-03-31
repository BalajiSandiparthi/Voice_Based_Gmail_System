import imaplib
import speech_recognition as sr
import easyimap as e
import pyttsx3
import email

r=sr.Recognizer()
engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
engine.setProperty('rate',130)

def speak(str):
    if str=="" or str=="None":
        str="You did not enter anything, so we are exiting"
        speak(str)
        exit(1)
    print(str)
    str.strip()
    str=str.replace('>','')
    engine.say(str)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=0.2)
        r.pause_threshold=1
        str="Speak Now: "
        speak(str)
        audio=r.listen(source)
        try:
            text=r.recognize_google(audio)
            text=text.lower()
            return text
        except:
            str="\nSorry could not recognize what you said, say that again."
            speak(str)
            text=listen()
            return text

# Connect to Gmail's IMAP server
def del_mail(username,password,recepient):

    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username, password)

    # Select the mailbox/folder where the email is located
    mail.select('inbox')

    # Search for the email you want to delete
    status, data = mail.search(None, f'FROM {recepient}')
    str=f"\nThe mails from {recepient} are as follows..."
    speak(str)
    # Iterate through the list of email IDs returned
    i=0
    for email_id in data[0].split():
        i+=1
        status, data = mail.fetch(email_id, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])
        sender = msg['From']
        subject = msg['Subject']
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True).decode('utf-8')
                    break
        else:
            body = msg.get_payload(decode=True).decode('utf-8')
    
        str=f"The mail is From: {sender}\nThe Subject of the mail is: {subject}\nThe Body of the mail is: {body}\n"
        speak(str)
        str="\nDo you want to delete this Email?"
        speak(str)
        str="Say yes or no"
        speak(str)
        ch=listen()
        if "s" in ch:
            mail.store(email_id, "+FLAGS", "\\Deleted")
            mail.store(email_id, "+X-GM-LABELS", "\\Trash")
            message="The email is deleted, it will be present in Bin"
            speak(message)

        str=f"Do you want to delete other emails of {recepient}"
        speak(str)
        str="Yes or No"
        speak(str)
        ch=listen()
        if "yes" in ch:
            continue
        else:
            break

    if i!=0 and i==len(data[0]):
        str=f"\nAll the mails from {recepient} got completed"
        speak(str)
    mail.close()
    mail.logout()

def star_mail(username,password,recipient):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username, password)

    mail.select('inbox')

    status, data = mail.search(None, f'FROM {recipient}')
    str=f"\nThe mails from {recipient} are as follows..."
    speak(str)
    i=0
    for email_id in data[0].split():
        i+=1
        status, data = mail.fetch(email_id, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])
        sender = msg['From']
        subject = msg['Subject']
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True).decode('utf-8')
                    break
        else:
            body = msg.get_payload(decode=True).decode('utf-8')
    
        str=f"\nThe mail is From: {sender}\nThe Subject of the mail is: {subject}\nThe Body of the mail is: {body}\n"
        speak(str)
        
        str="\nDo you want to star this Email?"
        speak(str)
        str="Say yes or no"
        speak(str)
        ch=listen()
        if "s" in ch:
            mail.store(email_id, '+FLAGS', '\\Flagged')
            message="This mail is starred as per your request"
            speak(message)
        str=f"Do you want to star other emails of {recipient}"
        speak(str)
        str="Yes or No"
        speak(str)

        ch=listen()
        if "yes" in ch:
            continue
        else:
            break
    if i!=0 and i==len(data[0]):
        str=f"\nAll mails from {recipient} got completed"
        speak(str)
    mail.close()
    mail.logout()
