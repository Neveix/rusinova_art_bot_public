import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class MailManager:
    def __init__(self, email_sender: str, email_password: str):
        self.email_sender = email_sender
        self.email_password = email_password
    def send_default(self, email_receiver: str, subject: str, body: str):
        msg = MIMEMultipart()
        msg['From'] = self.email_sender
        msg['To'] = email_receiver
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        with smtplib.SMTP('smtp.yandex.ru', 587) as server:
            server.starttls()
            server.login(self.email_sender, self.email_password)
            server.send_message(msg)
