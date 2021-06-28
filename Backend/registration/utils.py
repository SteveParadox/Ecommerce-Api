import os
import secrets

from flask import url_for, current_app
from flask_mail import Message

from Backend import mail



def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@email.com',
                  recipients=[user.email])
    msg.body = f"""To reset your password, click the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request, then please ignore this email and no changes will be made.    
"""
    mail.send(msg)
