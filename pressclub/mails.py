import json
import requests

from flask import url_for
from itsdangerous import Serializer

from . import app
from .models import Users


def send_mail(email, subject, body, link) -> bool:
    reqUrl = 'https://sfanp6h6gu3lvo3acrfjdyb4ly0smyme.lambda-url.us-east-1.on.aws/'
    headersList = {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "subject": subject,
        "email": email,
        "body": body,
        "link": link
    })

    response = requests.request("POST", reqUrl, data=payload, headers=headersList)

    return True


def send_mail_to_create_user(email):
    s = Serializer(app.config['SECRET_KEY'])
    token = s.dumps(email, salt='register')
    link = url_for('register', token=token, _external=True)
    subject = 'Welcome to Press Club'
    body = f"Congratulations! You have been added to Press Club. Click on the link below to create an account. {link}"
    send_mail(email, subject, body, link)
    return True





