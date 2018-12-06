import imaplib
import email
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders

our_email = "e-mail"
password = "password"
text ="""
Your text wich will send
"""

def extract_body(payload):
    if isinstance(payload,str):
        return payload
    else:
        return '\n'.join([extract_body(part.get_payload()) for part in payload])

def send_email(em):
    msg = MIMEMultipart()#attaching file 10.pdf
    msg["From"] = our_email
    msg["TO"] = email_g
    msg["Subject"] = "Headline"
    msg.attach(MIMEText(text, 'plain'))

    filename = "file"#your file
    attachment = open(filename, 'rb')

    part = MIMEBase('application', "octet-stream")
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename= '+filename)
    msg.attach(part)
    txt = msg.as_string()
    
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)#starting
    smtpObj.starttls()
    try:
        smtpObj.login(our_email, password)#login
    except:
        print("[FATAL ERROR]Problems with login")
        exit()
    try:
        smtpObj.sendmail(our_email, em, txt)
        print("Send")
    except:
        print("[ERROR]Problems with email sending")
    smtpObj.quit()

print("[AT]Script is ON!")

while True:
    conn = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    try:
        conn.login(email_g, password)
    except:
        print("[FATAL ERROR]Failed to login")
        break
    conn.select()
    typ, data = conn.search(None, 'UNSEEN')
    try:
        for num in data[0].split():
            typ, msg_data = conn.fetch(num, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    try:
                        msg = email.message_from_string(response_part[1].decode())
                        subject=msg['subject']                   
                        print(subject)
                        payload=msg.get_payload()
                        body=extract_body(payload)
                        body = base64.b64decode(body).decode("utf-8").split("\n")
                        if(body[5] == '<b>Request details:</b><br><br>'):
                            name = body[6].split(" ")[1].split("<br>")[0]
                            email_g = body[7].split(" ")[1].split("<br>")[0]
                            print("Sending to {0}".format(name))
                            send_email(email_g)
                    except:
                        print("[AT]Enother e-mail")
            typ, response = conn.store(num, '+FLAGS', r'(\Seen)')
    finally:
        try:
            conn.close()
        except:
            pass
        conn.logout()