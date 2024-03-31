import imaplib
import email
import pyttsx3
import smtplib
import speech_recognition as sr
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
            str="Sorry could not recognize what you said, say that again."
            speak(str)
            text=listen()
            return text
            exit(1)
def features(username,password,reqfeat):
    all_features={
        "bin":"[Gmail]/Bin",
        "drafts":"[Gmail]/Drafts",
        "important":"[Gmail]/Important",
        "sent":"[Gmail]/Sent Mail",
        "spam":"[Gmail]/Spam",
        "starred":"[Gmail]/Starred",
    }
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username, password)

    if reqfeat=='sent':
        mailbox = imaplib.IMAP4._quote(imaplib.IMAP4, all_features[reqfeat])
        mail.select(mailbox)
        status, data = mail.search(None, f'FROM {username}')
    else:
        mail.select(all_features[reqfeat])
        status, data = mail.search(None, 'ALL')
    str=f"\nThe emails that are present in {reqfeat} are as follows"
    speak(str)
    i=0
    for num in data[0].split():
        i+=1
        status, data = mail.fetch(num, '(RFC822)')
    
        msg = email.message_from_bytes(data[0][1])
    
        sender = msg['From']
        subject = msg['Subject']
        recep=msg['To']
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True).decode('utf-8')
                    break
        else:
            body = msg.get_payload(decode=True).decode('utf-8')
    
        if reqfeat=="sent":
            str=f"The mail is From: {sender}\nThe mail is To: {recep}\nThe Subject of the mail is: {subject}\nThe Body of the mail is: {body}\n"
            speak(str)
        else:
            str=f"The mail is From: {sender}\nThe Subject of the mail is: {subject}\nThe Body of the mail is: {body}\n"
            speak(str)
        str="\nDo you want to read the next mail?"
        speak(str)
        str="Say yes or no"
        speak(str)
        ch=listen()
        if "yes" in ch:
            continue
        else:
            break
        
    if i==len(data[0]):
        str=f"\nAll the mails present in {reqfeat} got completed"
        speak(str)
    str="\nGoing back"
    speak(str)
    mail.close()
    mail.logout()


