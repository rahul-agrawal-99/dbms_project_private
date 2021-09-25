from flask import Flask , render_template , redirect ,request

import db
app = Flask(__name__)

@app.route("/",methods=['POST','GET'])
def hello_world():
    if request.method=='POST':
        print('Post Success ***********************************')
        foo = request.form['foo']
        print(foo ,"**************foo")
    return render_template('index.html' , status=False)


@app.route("/log",methods=['POST','GET'])    
def log():
   if request.method == 'POST':
        i = request.form['id']   
        p = request.form['pass']
        valid=db.check_login(i,p)
        if valid=="yes":
            return 'login success'
        elif valid=='no':
            stat=f"Wrong password enterd for userID : {i} please Enter correct credential"
            return render_template('index.html' , status=True)
        else:
            return render_template('index.html' , status="invalidID")
           
        
@app.route("/newuser",methods=['POST','GET'])    
def newuser():
   return render_template('newuser.html' , status=" ")
    
@app.route("/admin",methods=['POST','GET'])    
def admin():
   return render_template('admin.html' , status=" ")
    
@app.route("/adminlog",methods=['POST','GET'])    
def adminlog():
    if request.method == 'POST':
        i = request.form['id']   
        p = request.form['pass']
    if(i=='root' and p=='rahul'):
        return render_template('login_table.html' , val=db.login())    
    return ' unsuccess'
    
    
    
    
    
    
    
       
@app.route("/newusersubmit",methods=['POST','GET'])    
def newuserlogin():
    if request.method=='POST':
      name = request.form['name']
      email = request.form['email']
      phone = request.form['phone']
      bday=request.form['birthday']
      userid = request.form['userid']
      pas = request.form['pas']
      print(name,email,phone,bday,userid,pas)
      status=db.insert_new_user(name,email,phone,bday,userid,pas)
    if status=='blanku':
        return render_template('newuser.html' , status='Blank UserID Not allowed')
    if status=='blankp':
        return render_template('newuser.html' , status='Password id Blank')
    if status=='exist':
        return render_template('newuser.html' , status='UserID already Exist Please enter another')
    if status=='blankbday':
        return render_template('newuser.html' , status='Enter Birth Date')
    if status=='blankname':
        return render_template('newuser.html' , status='Enter Name')
    return render_template('index.html' , status='new')
       
app.run(debug=True)  