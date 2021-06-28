from flask_mail import Message

from Backend import app, mail


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=json,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)
