import smtplib
from email.message import EmailMessage
def send_mail(sndSubject, sndMessage):
    # import smtplib
    msg = EmailMessage()
    msg['Subject'] = sndSubject
    msg['From'] = 'ryanez@bmsmanagement.com'
    msg['To'] = 'ryanez@bmsmanagement.com'
    msg.set_content(sndMessage)
 
    server = smtplib.SMTP('10.100.2.50')
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.send_message(msg)
    server.quit()

def main():
    send_mail("Test Subject", "This is a test message")
if __name__ == "__main__":
    main()