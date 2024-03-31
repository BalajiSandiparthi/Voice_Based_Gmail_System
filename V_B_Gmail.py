from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import speech_recognition as sr
import pyttsx3
import smtplib
import mysql.connector
import email
import imaplib
import time
from datetime import datetime, timedelta
import threading
import imapfeat
import drafts
import implement
import s_s

smtp_port = 587                 # Standard secure SMTP port
smtp_server = "smtp.gmail.com"  # Google SMTP Server

r=sr.Recognizer()

engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
engine.setProperty('rate',125)

server=smtplib.SMTP(smtp_server,smtp_port)
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
            str="Sorry could not recognize what you said, could you please say that again."
            speak(str)
            text=listen()
            return text
    
def log():
    print("              --------------")
    str="------------> | Login Page |"
    speak(str)
    print("              --------------")
    
    conn=mysql.connector.connect(host="localhost", user="root",password="", database="python")
    curr=conn.cursor()
    while True:
        str="\n>Please Speak your Email ID : "
        speak(str)
        unm=listen() #speak your username
        unm=unm.replace("at",'@')
        #unm=unm.replace('dot','.')
        unm=unm.replace(' ','')
        speak(unm)
        str=f"\nAre you sure that your gmail id is {unm}, if it is not say no to spell that again"
        speak(str)
        ch=listen()
        if "s" in ch:
            break
    while True:
        str="\n>Please Speak your short password : "
        speak(str)
        w=listen() #speak your short password
        w=w.replace(' ','')
        w=w.lower()
        speak(w)
        str=f"\nAre you sure that your short password is {w}, if it is not say no to say that again\n"
        speak(str)
        ch=listen()
        if "yes" in ch:
            str="You have chosen yes"
            speak(str)
            break
    query3="SELECT * FROM users WHERE email=%s AND shortpass=%s"
    val=(unm,w)
    curr.execute(query3,val)
    tab=curr.fetchall()
    if(len(tab)==1):
        if tab[0][1]==unm and tab[0][3]==w:
            pwd=tab[0][2]
            size=len(unm)
            print(" "*14+"-"*(size+15))
            str=f"------------> |Logged in to {unm}|"
            speak(str)
            print(" "*14+"-"*(size+15))
            home(unm,pwd)
    else:
        str="!!!Please Check the entered credentials!!!"
        speak(str)
        str="You entered wrong credentials, so we are going to enter section."
        speak(str)
        enter()        
    curr.close()
    conn.close()

def register():
    print("              ---------------------------")
    print("------------> | Welcome to Registration |")
    print("              ---------------------------")
    str="Welcome to Registration"
    speak(str)
    conn=mysql.connector.connect(host="localhost", user="root",password="", database="python")
  
    while True:
        str="\n>Please Speak your Email ID : "
        speak(str)
        unm=listen()
        unm=unm.replace("at",'@')
        unm=unm.replace(' ','')
        speak(unm)
        str=f"Are you sure that your gmail id is {unm}, if not say no to say that again"
        speak(str)
        ch=listen()
        if "yes" in ch:
            break
        
    str="\n>Please Speak your password : "
    speak(str)
    pwd=listen()
    pwd=pwd.replace(' ','')
    pwd=pwd.lower()
    speak(pwd)
    str="\nSince the password is difficult to recognize, you can take the help of some trusted person to enter your password."
    speak(str)
    str="Speak YES or NO"
    speak(str)
    g=listen()
    g=g.lower()
    if "s" in g:
        str="Enter your password : "
        speak(str)
        pwd=input()
        pwd=pwd.lower()
    else:
        str="Ok Continue"
        speak(str)
    try:
        server=smtplib.SMTP(smtp_server,smtp_port)
        server.starttls()
        server.login(unm,pwd)
        server.close()
    except smtplib.SMTPAuthenticationError:
        str="Check your Gmail id or password.You might have entered them wrong.Please Register again with a valid Gmail and Password."
        speak(str)
        enter()

    str="\nBoth mail and password are valid, now move further..."
    speak(str)
    str="\n>Please Speak a short password so that u can login to your account easily : "
    speak(str)
    st=listen()
    st=st.replace(' ','')
    st=st.lower()
    speak(st)
    curr=conn.cursor()
    query1="INSERT INTO `users`(`email`,`password`,`shortpass`) VALUES(%s,%s,%s)"
    val=(unm,pwd,st)
    curr.execute(query1,val)
    conn.commit()
    curr.close()
    conn.close()
    str="Registration Succesful..."
    speak(str)
    str="\n-----> Speak Login to log into your Gmail\n-----> Speak Back to go back"
    speak(str)
    f=listen()
    if "login" in f:
        str="\n>You said login\n"
        speak(str)
        log()
    elif "back" in f:
        str="You chose to go back, so we are going back"
        speak(str)
        enter()
    else:
        str="Your choice is Wrong...We are going back"
        speak(str)
        enter()

def sendmail(unm,pwd):
    print("              -----------------------")
    str="------------> | Welcome to Send Section |"
    speak(str)
    print("              -----------------------")

    while True:
        str="\nPlease speak the recipient Email ID:"
        speak(str)
        rec=listen()
        rec=rec.replace("at",'@')
        rec=rec.replace(' ','')
        speak(rec)
        str=f"\nAre you sure that the recepient mail id is {rec}, Do you want to say that again?"
        speak(str)
        str="say yes or no"
        speak(str)
        ch=listen()
        if "no" in ch:
            break
    while True:
        str="\nPlease speak the subject of the email"
        speak(str)
        subject=listen()
        str=f"\nThe subject you have said is {subject}, Do you want to say that again?"
        speak(str)
        str="say yes or no"
        speak(str)
        ch=listen()
        if "no" in ch:
            str="You have chosen no"
            speak(str)
            break
    while True:
        str="\nPlease speak the body of the email"
        speak(str)
        body=listen()
        str=f"\nThe body of the mail that you have said is : {body}, Do you want to say that again?"
        speak(str)
        str="say yes or no"
        speak(str)
        ch=listen()
        if "no" in ch:
            str="You have chosen no"
            speak(str)
            break
    str="\nDo you want to save this email as a draft?"
    speak(str)
    str="Yes or No"
    speak(str)
    ch=listen()
    if "yes" in ch:
        drafts.draft(subject,unm,rec,body,pwd)
        str="The Email is saved in Drafts"
        speak(str)
        str="Now, you are going back"
        speak(str)
    else:
        str="\nYou have chosen no, so proceeding further."
        speak(str)
        str="\nDo you want to schedule this mail for later??"
        speak(str)
        str="\nSay yes to schedule a mail or no to send the mail now itself."
        speak(str)
        str="Say yes or no"
        speak(str)
        ch=listen()
        if "yes" in ch:
            str="You have chosen to send your mail at a particular time, please give the exact time and date to schedule the mail."
            speak(str)
            while True:
                str="\nPlease speak the year"
                speak(str)
                year=listen()
                str=f"Year : {year}"
                speak(str)
                str="\nPlease speak the month"
                speak(str)
                mon=listen()
                str=f"Month : {mon}"
                speak(str)
                str="\nPlease speak the day"
                speak(str)
                day=listen()
                str=f"Day : {day}"
                speak(str)
                str="\nPlease speak the hour"
                speak(str)
                hr=listen()
                str=f"Hour : {hr}"
                speak(str)
                str="\nPlease speak the min"
                speak(str)
                min=listen()
                str=f"Minutes : {min}"
                speak(str)
                str="\nPlease speak the seconds"
                speak(str)
                sec=listen()
                str=f"Seconds : {sec}"
                speak(str)
                str="\nDo you want to speak that again?"
                speak(str)
                str="\nSay yes or no"
                speak(str)
                ch=listen()
                if "no" in ch:
                    str="You have chosen no"
                    speak(str)
                    break
            send_time=datetime.strptime(f'{year}-{mon}-{day} {hr}:{min}:{sec}', '%Y-%m-%d %H:%M:%S')
            t = threading.Thread(target=s_s.send_email_thread, args=(rec, subject, body, unm, pwd,send_time))
            t.start()
            str=f"\nThe Email will be sent at {send_time}"
            speak(str)
            str="\nGoing back"
            speak(str)
        else:
            try:
                server.starttls()
                server.login(unm,pwd)
                server.sendmail(unm,rec,body)
                server.quit()
                print("---------------------")
                str=f"\nEmail sent to:{rec}"
                speak(str)
                print("----------------------")
                str="\nGoing back to home page..."
                speak(str)
            except smtplib.SMTPAuthenticationError:
                str="Check your Gmail id or password.You might have entered them wrong.Please Register again with a valid Gmail and Password."
                speak(str)

def readmail(unm,pwd):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(unm, pwd)
    mail.select('INBOX')
    status, data = mail.search(None, 'UNSEEN')
    str="\nThe messages that are unread are as follows...\n"
    speak(str)
    i=0
    for num in data[0].split():
        i+=1
        status, data = mail.fetch(num, '(RFC822)')
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

        str="\nDo you want to star this Email?"
        speak(str)
        str="Say yes or no"
        speak(str)
        ch=listen()
        if "s" in ch:
            mail.store(num, '+FLAGS', '\\Flagged')
            message="This mail is starred as per your request"
            speak(message)

        str="\nDo you want to delete this Email?"
        speak(str)
        str="Say yes or no"
        speak(str)
        ch=listen()
        if "s" in ch:
            mail.store(num, "+FLAGS", "\\Deleted")
            mail.store(num, "+X-GM-LABELS", "\\Trash")
            message="The email is deleted, it will be present in Bin"
            speak(message)
        
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
        str="All the mails got completed."
        speak(str)
    str="Going Back"
    speak(str)
    mail.close()
    mail.logout()
    
def inbox_filtering(unm,pwd):
    imap_server = 'imap.gmail.com'
    imap_port = 993
    str="\n----> Welcome to inbox filtering..."
    speak(str)
    str="\nWhose mails do you want, say their name, that is sufficient..."
    speak(str)
    message=listen()
    speak(message)
    specific_words = message.split()
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(unm, pwd)
    mail.select('inbox')
    type, data = mail.search(None, 'ALL')
    result_mails=[]
    for num in data[0].split():
        type, data = mail.fetch(num, '(RFC822)')
        email_message = email.message_from_bytes(data[0][1])
        email_subject = email_message['subject']
        email_from = email_message['from']
        email_text = ''
        part_mail=""
        if any(word in email_from.lower() for word in specific_words):
            required_mail=email_from
            if email_message.is_multipart():
                for part in email_message.walk():
                    if part.get_content_type() == 'text/plain':
                        email_text = part.get_payload(decode=True).decode('utf-8')
                        break
            else:
                email_text = email_message.get_payload(decode=True).decode('utf-8')
            
            part_mail+=f"\nThe subject of the mail is {email_subject}\n"
            part_mail+=f"The mail is from {email_from}\n"
            part_mail+=f"The body of the mail is {email_text}"
            result_mails.append((num,part_mail))
    message=f"\nThere are {len(result_mails)} mails from {required_mail}."
    speak(message)
    message="\nDo you want to read them?"
    speak(message)
    str="Say yes or no"
    speak(str)
    ans=listen()
    if "yes" in ans:
        for i in range(len(result_mails)-1,-1,-1):
            print("----------------------------------------------------")
            message=result_mails[i][1]
            speak(message)
            print("----------------------------------------------------")

            message="\nDo you want to star this email?"
            speak(message)
            message="Yes or No"
            speak(message)
            ch=listen()
            if "yes" in ch:
                mail.store(result_mails[i][0], '+FLAGS', '\\Flagged')
                
            message="\nDo you want to delete this Email?"
            speak(message)
            message="Yes or No"
            speak(message)
            ch=listen()
            if "s" in ch:
                mail.store(result_mails[i][0], "+FLAGS", "\\Deleted")
                mail.store(result_mails[i][0], "+X-GM-LABELS", "\\Trash")
                message="\nThe email is deleted, it will be presented in Bin"
                speak(message)
            if i==0:
                break
            message=f"\nDo you want to read another mail from {required_mail}"
            speak(message)
            str="say yes or no"
            speak(str)
            ans=listen()
            if "yes" in ans:
                continue
            else:
                break
        if(i==-1):
            message="\nAll the mails got completed"
            speak(message)
        else:
            message="\nOk, You are going back"
            speak(message)
    else:
        message="\nGoing back"
        speak(message)
    
    mail.close()
    mail.logout()

def send_email_with_attachment(unm,pwd):
    print("              ---------------------------------")
    str="------------> | Welcome to Send an Attachment |"
    speak(str)
    print("              ---------------------------------")
    email_from = unm
    while True:
        str="\nPlease speak the recipient Email ID:"
        speak(str)
        email_to=listen()
        email_to=email_to.replace("at",'@')
        email_to=email_to.replace(' ','')
        speak(email_to)
        str=f"\nAre you sure that the recipient email id is {email_to}, Do you want to say that again?"
        speak(str)
        str="say yes or no"
        speak(str)
        ch=listen()
        if "no" in ch:
            str="You have chosen no"
            speak(str)
            break
    while True:
        str="\nPlease speak the subject of the email"
        speak(str)
        subject=listen()
        str=f"\nThe subject you have said is {subject}, Do you want to say that again?"
        speak(str)
        str="say yes or no"
        speak(str)
        ch=listen()
        if "no" in ch:
            str="You have chosen no"
            speak(str)
            break
    while True:
        str="\nPlease speak the body of the email"
        speak(str)
        body=listen()
        str=f"\nThe body of the mail that you have said is : {body}, Do you want to say that again?"
        speak(str)
        str="say yes or no"
        speak(str)
        ch=listen()
        if "no" in ch:
            str="You have chosen no"
            speak(str)
            break

    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    while True:
        str="\nPlease speak the name of the file that is to be attached."
        speak(str)   
        filename = listen()
        filename.replace("underscore","_")
        filename.replace(' ','')
        filename.replace("dot",'.')
        str=f"\nThe file which you want to attach is {filename}, is that correct?"
        speak(str)
        str="Say Yes or No"
        speak(str)
        ch=listen()
        if "yes" in ch:
            str="\nYou have chosen yes"
            speak(str)
            break
    try:
        attachment= open(filename, 'rb')
    except FileNotFoundError:
        str=f"\nThe requested file {filename} is not present in your system. So we are going back"
        speak(str)
        home(unm,pwd)

    attachment_package = MIMEBase('application', 'octet-stream')
    attachment_package.set_payload((attachment).read())
    encoders.encode_base64(attachment_package)
    attachment_package.add_header('Content-Disposition', "attachment; filename= " + filename)
    msg.attach(attachment_package)
    text = msg.as_string()
    TIE_server = smtplib.SMTP(smtp_server, smtp_port)
    TIE_server.starttls()
    TIE_server.login(email_from, pwd)
    str=f"\n{filename} is Attached"
    speak(str)
    str="\nDo you want to save this email as a draft?"
    speak(str)
    str="\nYes or No"
    speak(str)
    ch=listen()
    if "yes" in ch:
        str="\nYou have chosen yes"
        speak(str)
        drafts.draft(subject,unm,email_to,msg,pwd)
        str="\nEmail is saved in Drafts"
        speak(str)
        str="\nNow, you will be going back"
        speak(str)
    else:
        str=f"\nSending email to: {email_to}..."
        speak(str)
        TIE_server.sendmail(email_from, email_to, text)
        str=f"\nEmail sent to: {email_to}"
        speak(str)
        print()
    TIE_server.quit()

def feat_func(unm,pwd):
    str="""
    1 Bin
    2 Draft
    3 Important
    4 Sent
    5 Spam
    6 Starred
    7 Back
    """
    speak(str)
    flag=0
    str="Choose one of the above features"
    speak(str)
    ch=listen()
    ch.replace(' ','')
    if "bin" in ch:
        answer="bin"
    elif "draft" in ch:
        answer="drafts"
    elif "important" in ch:
        answer="important"
    elif "sent" in ch:
        answer="sent"
    elif "spam" in ch:
        answer="spam"
    elif "star" in ch:
        answer="starred"
    else:
        flag=1
        str="\nGoing back to home"
        speak(str)
    if flag==0:
        imapfeat.features(unm,pwd,answer)
  
def home(unm,pwd):
    print("                                                                                       ----------------")
    str="                                                                                       |   HOME PAGE  |"
    speak(str)
    print("                                                                                       ----------------")
    
    str="\nWhat do you want to do?"
    speak(str)
    str="\n-----> Speak SEND to Send mails\n-----> Speak READ to Read mails\n-----> Speak FEATURES to access all other Features\n-----> Speak IMPLEMENT to delete or star mails\n-----> Speak LOGOUT to LogOut\n"
    speak(str)
    ch=listen()
    ch.replace(' ','')
    if "send" in ch:
        str="\nYou have chosen to send an email"
        speak(str)
        str="\nDo you want to attach any file??"
        speak(str)
        str="Say yes or no"
        speak(str)
        ans=listen()
        if "yes" in ans:
            str=f"\nYou have chosen yes, you can add an attachment"
            speak(str)
            send_email_with_attachment(unm,pwd)
        else:
            str=f"You have chosen no, so going with the normal text mail"
            speak(str)
            sendmail(unm,pwd)
        home(unm,pwd)
    elif "read" in ch:
        str="\nYou have chosen to read emails"
        speak(str)
        str="\nThere are two options"
        speak(str)
        str="\n-----> Read the unread messages\n-----> Filtering of Inbox using a particular sender\n"
        speak(str)
        str="Choose one of the above options"
        speak(str)
        ch=listen()
        if "1" in ch:
            readmail(unm,pwd)
        elif "2" in ch:
            inbox_filtering(unm,pwd)
        home(unm,pwd)
    elif "feat" in ch:
        feat_func(unm,pwd)
        home(unm,pwd)
    elif "imp" in ch:
        str="\n-----> Delete mails\n-----> Star the mails\n"
        speak(str)
        str="\nChoose any of the above options"
        speak(str)
        ch=listen()
        if "delete" in ch:
            str="\nYou have chosen to delete"
            speak(str)
            str="\nWhose messages do you want to delete, say the recepient mail id"
            speak(str)
            rec=listen()
            rec=rec.replace("at",'@')
            rec=rec.replace(" ",'')
            rec=rec.replace('dot','.')
            speak(rec)
            implement.del_mail(unm,pwd,rec)
            str="\nGoing back"
            speak(str)
        elif "star" in ch:
            str="\nYou chose to star a message"
            speak(str)
            str="\nWhose messages do you want to star"
            speak(str)
            rec=listen()
            rec=rec.replace("at",'@')
            rec=rec.replace(" ",'')
            rec=rec.replace('dot','.')
            speak(rec)
            implement.star_mail(unm,pwd,rec)
            str="\nGoing back"
            speak(str)
        else:
            str="\nWrong Choice, going back"
            speak(str)
        home(unm,pwd)
    elif "log" in ch:
        str="\nYou have chosen to logout, Logging out"
        speak(str)
        enter()
    else:
        str="\nInvalid choice..."
        speak(str)
        speak(ch)
        home(unm,pwd)

def enter():
    print("                                                                      ------------------------------------------------------")
    str="                                                                      |             LOG IN OR REGISTER TO ENTER            |"
    speak(str)
    print("                                                                      ------------------------------------------------------")
    str="\nIf you are visiting here for the first time, then please REGISTER...Otherwise LOGIN..."
    speak(str)
    str="\n-----> Speak Register to register\n-----> Speak Login to log into your Account\n-----> Speak Exit to Exit\n"
    speak(str)
    ch=listen()
    if "r" in ch or "are" in ch:
        str="\n------->You have chosen to Register\n"
        speak(str)
        register()
    elif "login" in ch:
        str="\n------->You have chosen to Login\n"
        speak(str)
        log()
    elif "e" in ch:
        str="\nYou have chosen to exit...Bye Bye..."
        speak(str)
        exit(1)
    else:
        str="Invalid Choice...Please try again\n"
        speak(str)
        enter()

print("---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
str="                                                                                 Welcome to Voice Based Gmail System"
speak(str)
print("---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
enter()


    


    
    