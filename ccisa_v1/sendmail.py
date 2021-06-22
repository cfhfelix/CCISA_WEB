from flask import Flask, request, render_template, session, make_response, redirect, abort
from flask_mail import Mail
from flask_mail import Mail
from flask_mail import Message

class mailServer():
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config.update(
    #  hotmail的設置
            MAIL_SERVER='smtp.live.com',
            MAIL_PROT=587,
            MAIL_USE_TLS=True,
            MAIL_USERNAME='',
            MAIL_PASSWORD=''
        )
        self.mail = Mail(self.app)
        self.mail.init_app(self.app) ## 傳送mail
    def sendMail( self, Email ):
        msg_title = 'Hello It is Flask-Mail'
        msg_sender = 'ccisaWebForm@hotmail.com'
        msg_recipients = [Email]
        msg_body = 'NMSL'
        msg = Message(msg_title,
            sender=msg_sender,
            recipients=msg_recipients)
        msg.body = msg_body
        self.mail.send(msg)
