from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import private

# To send Email inn case of errors
def SendMail(subject="NSE BSE Alerts", body=None, other_recipients=None, table=None):

    username = private.sender
    password = private.pwd

    recipients = private.receiver
    if isinstance(other_recipients, list):
        recipients = recipients + other_recipients

    toaddrs = ", ".join(recipients)

    msg = MIMEMultipart('alternative')

    msg['To'] = toaddrs
    msg['Subject'] = subject

    text = MIMEText(body, 'plain')
    msg.attach(text)

    if table:
        html = MIMEText(table, 'html')
        msg.attach(html)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    server.sendmail(username, recipients, msg.as_string())
    server.quit()
