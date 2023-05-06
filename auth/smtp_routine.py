from .auth_utils import smtplib

def send_email(message, reciever):
    sender = "denisnepovis@mail.ru"
    password = "d5pVbceLH1pnpwzNn3ay"
    server = smtplib.SMTP("smtp.mail.ru", 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, reciever, message)
