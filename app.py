from flask import Flask , render_template , redirect ,request

import db
app = Flask(__name__)

cid={}

@app.route("/",methods=['POST','GET'])
def hello_world():
    # if request.method=='POST':
    #     print('Post Success ***********************************')
    #     foo = request.form['foo']
    #     print(foo ,"**************foo")
    return render_template('index.html' , status=False)


@app.route("/log",methods=['POST','GET'])    
def log():
   if request.method == 'POST':
        i = request.form['id']   
        p = request.form['pass']
        valid=db.check_login(i,p)
        if valid=="yes":
            cid['id']=i
            cid['name']=db.get_name(i)
            return render_template('customer_login.html' , cid=cid['id'] ,cname=cid['name'])
        elif valid=='no':
            stat=f"Wrong password enterd for userID : {i} please Enter correct credential"
            return render_template('index.html' , status=True)
        else:
            return render_template('index.html' , status="invalidID")
           
        
@app.route("/newuser",methods=['POST','GET'])    
def newuser():
   return render_template('newuser.html' , status=" ")
    
@app.route("/card",methods=['POST','GET'])    
def card():
    i=cid['id']
    print(i)
    c =db.get_card_details(i)
    if (len(c)==0):
        s="No card added Yet"
        return render_template('cards.html' , status=s)
    return render_template('cards.html' , status=c)
    
@app.route("/admin",methods=['POST','GET'])    
def admin():
   return render_template('admin.html' , status=" ")
    
@app.route("/get_acc_deatils",methods=['POST','GET'])    
def get_acc_deatils():
    i=cid['id']
    acc=db.get_accound(i)
    return render_template('get_acc_deatils.html' , status=acc)
    
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
        return render_template('newuser.html' , status='Namespace is Blank Please Enter Name')
    return render_template('index.html' , status='new')
       
       


@app.route("/pay",methods=['POST','GET'])    
def pay():
    if request.method=='POST':
        cvv= request.form['cvv']
        otp= request.form['otp']
    if otp=="1234":
        return render_template('success.html' , total_pay = 400 , card_balance = 200) 
    print(cvv,otp)
    return render_template('payment_page.html' , cid=cid[0] , card_no=4645 ,total_amount=465, order_id =46645 ,stat = "Wrong Otp Entered")


@app.route("/add_card_render",methods=['POST','GET'])    
def add_card_r():
    return render_template('add_card.html' )


@app.route("/add_card",methods=['POST','GET'])    
def add_card():
    if request.method=='POST':
        cno= request.form['cno']
        cvv= request.form['cvv']
        bal= request.form['bal']
    if len(cno)!=16:
        return render_template('add_card.html' ,status="Please check card No . You Have entered Wrong Card No.") 
    if len(cvv)!=3:
        return render_template('add_card.html' ,status="Enter correct CVV of 3 digits only") 
    i=cid['id']
    db.insert_new_card(i,cno,cvv,bal)
    c =db.get_card_details(i)
    if (len(c)==0):
        s="No card added Yet"
        return render_template('cards.html' , status=s)
    return render_template('cards.html' , status=c)




app.run(debug=True)  