from flask import *
from flask import Flask, render_template, request
import pymysql

app = Flask(__name__, template_folder='template')
app.secret_key = '1234567886'

@app.route("/hello")
def home():
    return "HELLO"

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']

        if len(password) < 8:
            return render_template('signup.html' , error = 'password must be 8 characters')
        else:
            conn = pymysql.connect(host='localhost' ,user='root', password='' , database='bakery')
            cursor=conn.cursor()
            cursor.execute('insert into users(name,email,password,confirm) values(%s,%s,%s,%s)',(name,email,password,confirm))
            conn.commit()
            return render_template('login.html', msg = "saved successfully")
    else:
        return render_template('signup.html')

@app.route('/login',methods =['GET','POST'])
def login():
    if request.method =='POST':
        conn = pymysql.connect(host='localhost' ,user='root', password='' , database='bakery')
        cursor = conn.cursor()
        email = request.form['email']
        password = request.form['password']
        cursor.execute('select * from login where email =%s and password =%s',(email,password))
        if cursor.rowcount == 0:
            return render_template('login.html',error = 'wrong credentials')
        else:
            session['key'] = password
            return redirect('/Home')
    else:
        return render_template('login.html')

@app.route("/Order",methods =['GET','POST'])
def Order():
    if request.method == 'POST':
       fullname = request.form['fullName']
       email = request.form['email']
       phone = request.form['phone']
       product = request.form['product']
       quantity = request.form['quantity'] 
       comments = request.form['comments']

       conn = pymysql.connect(host='localhost' ,user='root', password='' , database='order')
       cursor=conn.cursor() 
       cursor.execute('INSERT INTO `order` (fullname, email, phone, product, quantity, comments) VALUES (%s, %s, %s, %s, %s, %s)',
               (fullname, email, phone, product, quantity, comments))

       
       conn.commit()
      

      

    return render_template('Order.html')


if __name__=='__main__':
    app.run(debug=True)