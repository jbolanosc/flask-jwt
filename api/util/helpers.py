from flask import url_for
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from api import app

def send_async_email(msg):
    with app.app_context():
        mail.send(msg)

#def send_email(subject, recipients):
    #msg = Message(subject, recipients=recipients)
    #msg.html = '<h1>THis is the message</h1>'
    #thr = Thread(target=send_async_email, args=[msg])
    #thr.start()


def send_confirmation_email(user_email, url):
    confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    confirm_url = url_for(
        url,
        token=confirm_serializer.dumps(user_email, salt='email-confirmation-salt'),
        _external=True)

    html = render_template(
        'email_confirmation.html',
        confirm_url=confirm_url)

    send_email('Confirm Your Email Address', [user_email], html)


def send_password_reset_email(user_email):
    password_reset_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    password_reset_url = url_for(
        'user.reset_with_token',
        token = password_reset_serializer.dumps(user_email, salt='password-reset-salt'),
        _external=True)

    #html = render_template(
       # 'email_password_reset.html',
       # password_reset_url=password_reset_url)

    #send_email('Password Reset Requested', [user_email])