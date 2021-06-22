from flask import Flask, request, render_template, session, make_response, redirect, abort
from PIL import Image, ImageDraw, ImageFont
import random, string
#import secrets
from verifyCaptcha import Captcha
import traceback
import sys,logging
from io import BytesIO
from flask_mail import Mail, Message
from user_data import *
from mySQL import *
import os
from os import urandom
app = Flask("__main__", static_url_path="" )
#app.config["SECRET_KEY"] = secrets.token_urlsafe(16)
app.config["SECRET_KEY"] = os.urandom(12).hex()
app.config.update(
    #  hotmail的設置
    MAIL_SERVER='smtp.live.com',
    MAIL_PROT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='',
    MAIL_PASSWORD=''
    )
mail = Mail(app)
mail.init_app(app) ## 傳送mail

def abort_msg(e):
    """500 bad request for exception

    Returns:
        500 and msg which caused problems
    """
    error_class = e.__class__.__name__ # 引發錯誤的 class
    detail = e.args[0] # 得到詳細的訊息
    cl, exc, tb = sys.exc_info() # 得到錯誤的完整資訊 Call Stack
    lastCallStack = traceback.extract_tb(tb)[-1] # 取得最後一行的錯誤訊息
    fileName = lastCallStack[0] # 錯誤的檔案位置名稱
    lineNum = lastCallStack[1] # 錯誤行數 
    funcName = lastCallStack[2] # function 名稱
    errMsg = "Exception raise in file: {}, line {}, in {}: [{}] {}. Please contact the member who is the person in charge of project!".format(fileName, lineNum, funcName, error_class, detail)
    # return 500 code
    abort(500, errMsg)
def sendMail( user ) :
     #  try
    try :
    	print( user.user_msg() )
    	msg_title = 's'
    #  寄件者，若參數有設置就不需再另外設置
    	msg_sender = ''
    #  收件者，格式為list，否則報錯
    	print(user.email)
    	msg_recipients = [ user.email ]
    #  郵件內容
    	msg_body = user.name + "先生/小姐"  + "您的報名編號是" + str(user.serial) + "\n"
    	msg_body += ""
    #  也可以使用html
    #  msg_html = '<h1>Hey,Flask-mail Can Use HTML</h1>'
    	msg = Message(msg_title,
                  sender=msg_sender,
                  recipients=msg_recipients)
    	msg.body = msg_body
    	mail.send(msg)
    	return True
    except Exception as e :
    	return False 

@app.route("/", methods = ["GET", "POST"])
def index():
    try :
        index_url = "/index.html"
        session["username"] = "guest"
        if request.method == "GET":  
        	#return "hello"   
            return render_template( index_url )

        elif request.method == "POST":
            verify_code = session.get("verify")
            union_pip = request.form.get("union_pip", "")
            co_type = request.form.get("co_type", "")
            company = request.form.get("company", "")
            name_c =  request.form.get("name_c", "")
            title =  request.form.get("title", "")
            contact_tel_o = request.form.get("contact_tel_o", "")
            email =  request.form.get("email", "")
            txt_vCode = request.form.get("txt_vCode", "" )
            user = User_Obj(
               union_pip, co_type,company,name_c,title,contact_tel_o,email
            )
            logging.error(user.user_msg())

            if user.check_if_sqlinject() == True :
                return "請聯絡網管"
            if verify_code == txt_vCode:
                mySQL_create = mySQL_ccisa("127.0.0.1",3306)
                mySQL_create.connectDB( "ccisa_webfrom")
                serial = mySQL_create.insert_db_data(user)
                mySQL_create.deconnectDB()
                user.setserial( serial )
                if sendMail(user) == True :
                	msg = "報名成功，請去信箱收信，您的報名編號為" + str(serial)
                	return msg
                else :
                	return "報名失敗 資料有誤 請重新確認"


            msg_verify_error = "驗證碼錯了，咩噗！"
            return render_template( index_url, info = msg_verify_error )
    except Exception as e :
        abort_msg(e)
        return "報名失敗 資料有誤 請重新確認"



@app.route("/verify/" )
def verify():
    text, image = Captcha.gene_graph_captcha()
    session["verify"] = text
    out = BytesIO()
    image.save(out, "png")
    out.seek(0)
    resp = make_response(out.read()) 
    resp.content_type = "image/png" 
    return resp
if __name__=="__main__":
	app.run("0.0.0.0", 9000,debug = True)    
