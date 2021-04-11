from flask import Flask, session
from flask import request
from flask import render_template
from flask import url_for
from flask import redirect
import mysql.connector
import json
from urllib.request import urlretrieve

app=Flask(
    __name__,
    static_folder="public",
    static_url_path="/"
)

app.secret_key = b'p83129'

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="qaz4545112",
  database="website"
)

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/signup", methods=["POST"])
def signup():
    Name=request.form["txtName"]
    Account=request.form["txtAccount"]
    Password=request.form["txtPassword"]

    #print(Name+"," + Account + "," + Password)

    with mydb.cursor() as cursor:
        # 查詢資料SQL語法
        sql = "Select * From user Where username = '"  + Account + "'"
        # 執行指令
        cursor.execute(sql)
        # 取得所有資料
        result = cursor.fetchall()
        #print(len(result))       

        if len(result) == 0:
            sql = "Insert Into user (name,username,password) Values(%s, %s, %s)" 
            val = (Name, Account, Password)   
            cursor.execute(sql, val)
            mydb.commit()
            return redirect(url_for('index'))
        else:   
            value = "帳號已經被註冊"
            return redirect(url_for('error',message=value))


@app.route("/singin",methods=["POST"])
def singin():
    Account=request.form["txtAccount1"]
    Password=request.form["txtPassword1"]
    
    with mydb.cursor() as cursor:
        sql = "Select name From user Where username = '"  + Account + "' And password = '" + Password + "'"
        cursor.execute(sql)
        result = cursor.fetchall()   
        for row in result:
            #print ("%s" ,(row[0]))            
            if len(result)==1:
                session['sucess'] = '已登入' 
                return redirect(url_for('member',name=row[0]))
        if(len(result)==0):   
            #return redirect(url_for('error'))
            #name=request.form["txtAccount1"]
            value = "帳號或密碼輸入錯誤"            
            return redirect(url_for('error',message=value))

@app.route("/member/")
def member(): 
        member_info = request.args.get('name')
        if session['sucess'] == '已登入':
            return render_template("member.html",name=member_info)
        else:
            return redirect(url_for('index'))

@app.route("/error")
def error(): 
    errmag = request.args.get("message","帳號已經被註冊")
    if  errmag == "帳號已經被註冊":
        #print("***",name)
        return render_template("error.html",message=errmag)
    else:      
        return render_template("error.html",message=errmag)

@app.route("/signout", methods=["GET"])
def aaa():
    session['sucess'] = '未登入'  
    print(session['sucess'])  
    return redirect(url_for('index'))

@app.route("/api/users",methods=["GET"])
def api():
    with mydb.cursor() as cursor:
        search = request.args.get('username')
        sql = "Select id, name, username From user Where username = '" + search + "'"
        cursor.execute(sql)
        result = cursor.fetchall()
        if session['sucess'] == '未登入': #要求一
            if len(result)==1:
                for row in result:
                    id =  str(row[0])
                    name = str(row[1])
                    username = str(row[2])
                data_info = {'data':{'id':int(id),'name':name,'username':username}}
                jsObj = json.dumps(data_info)   
                return jsObj
            else:
                null = None 
                data_info = {'data':null}
                jsObj = json.dumps(data_info)
                return jsObj
        else: #要求二
            if len(result)==1:
                for row in result:
                    sqlname = str(row[1])
                    username = str(row[2])
                return sqlname + " ("+ username +") "
            else:
                return "無此使用者"           

    
app.run(port=3000,debug=True)   