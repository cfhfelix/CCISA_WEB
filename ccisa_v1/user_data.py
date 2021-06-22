class User_Obj():
    def __init__(self,accept_receive,sign_up,company,name,title,phone,email) :
        if accept_receive == "a01" : self.accept_receive = "同意"
        else : 
            self.accept_receive = "不同意"
        
        if sign_up == "a01" : self.sign_up = "上午"
        elif sign_up == "a02" : self.sign_up = "下午"
        elif sign_up == "a03" : self.sign_up = "整天"
        else :
             self.sign_up = "整天"
        self.company = company
        self.name = name
        self.title = title
        self.phone = phone 
        self.email = email
        self.serial = "" 
    def check_if_sqlinject(self):
        msg = self.accept_receive + self.sign_up + self.company + self.name + self.title + self.phone + self.email 
        check_attack = [ 'union', 'select', 'CONCAT', 'schema_name', 'OR 1 = 1', 
            'ascii', 'substr', 'mid', 'eval', 'exec']
        for a in check_attack :
            if a in msg : 
                return True
        return False
    def user_msg(self):
        msg = "報名編號" + str(self.serial)
        msg += "同意嗎" + self.accept_receive
        msg += '\n' + "報名場次： " + self.sign_up
        msg += '\n' + "公司：" + self.company
        msg += '\n' + "名子：" + self.name
        msg += '\n' + "部門：" + self.title
        msg += '\n' + "聯絡電話：" + self.phone
        msg += '\n' + "Email：" + self.email + "\n"
        return msg
    def setserial(self, num) :
        self.serial = str(num)