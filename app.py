from flask import Flask , render_template , redirect ,request
from flask.helpers import url_for

import db
app = Flask(__name__)

cid={}
total_p =0


@app.route("/",methods=['POST','GET'])
def hello_world():
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
    
@app.route("/product_page",methods=['POST','GET'])    
def product_page():
    s=db.get_product_name()
    print(s)
    return render_template('product.html' , jk=s )
    
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




           
tp=[]

p=[]

@app.route("/cart",methods=['POST','GET'])    
def cart():
    prod=[]
    p.clear()
    if request.method == 'POST':
        for i in range(len(db.get_product_name())):
            prod.append(int(request.form[f"{i+1}"]) )   
    s=db.get_product_name()    
    c=prod.count(0)
    if c==len(prod):
        return render_template('empty_cart.html' )
    else:
        total_p=0
        # print("prod is ",prod)
        counter=0
        for i in prod:
            p.append(i)
            # print("total_p is ",total_p)
            if(i!=0):
                # print(" ***** adding ",s[counter][2]*i)
                total_p = total_p+s[counter][2]*i 
                counter=counter+1
            else:
                counter=counter+1 
            tp.append(total_p)    
        return render_template('cart.html' , prod=prod ,jk=s ,total=total_p)  

order_id=[]

@app.route("/pay",methods=['POST','GET'])    
def pay():
    l=len(tp)
    tpl=tp[l-1]
    crd=db.get_card_details(cid['id']) 
    print(crd)
    if (len(crd)==0):
         return render_template('add_card.html' ,status="Please add Card , You Didnt saved any card")
    print("Using  card no :",crd[0][1])
    # print("tp is ",tp)
    order_id.append(db.generate_order_id())
    return render_template('payment_page.html' , cid=cid['id'] , card_no=crd[0][1] ,total_amount=tpl, order_id =order_id[len(order_id)-1] )


    
@app.route("/payment",methods=['POST','GET'])    
def payment():
    l=len(tp)
    tpl=tp[l-1]
    crd=db.get_card_details(cid['id'])
    # print("card i crd:",crd)
    if request.method=='POST':
        cvv= request.form['cvv']
        otp= request.form['otp']
    actual_cvv = db.get_cvv(crd[0][1])
    # print("get cvv is",actual_cvv)
    # print("eneter cvv is",cvv)
 
    if (actual_cvv !=int(cvv)):
        return render_template('payment_page.html' , cid=cid['id'] , card_no=crd[0][1] ,total_amount=tpl, order_id =order_id[len(order_id)-1] ,stat = "CVV Entered is Wrong")  
    if otp=="1234":
        new_bal = db.make_payment(crd[0][1] , tpl)
        if new_bal==False:
            return "Your Card Dont Have Enough Balance "
        db.transaction(order_id[len(order_id)-1],cid['id'],tpl)
        o=order_id[len(order_id)-1]
        db.update_orders(p,o)
        return render_template('success.html' , total_pay = tpl , card_balance = new_bal ,order_id =order_id[len(order_id)-1] ,card_no=crd[0][1] ) 
    print(cvv,otp)
    return render_template('payment_page.html' , cid=cid['id'] , card_no=crd[0][1] ,total_amount=tpl, order_id =order_id[len(order_id)-1] ,stat = "Wrong Otp Entered")
    
       
@app.route("/newusersubmit",methods=['POST','GET'])    
def newuserlogin():
    if request.method=='POST':
      name = request.form['name']
      email = request.form['email']
      phone = request.form['phone']
      bday=request.form['birthday']
      userid = request.form['userid']
      pas = request.form['pas']
    #   print(name,email,phone,bday,userid,pas)
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
    if status=='noage':
        return render_template('newuser.html' , status='Check Birthdate , You should be atleast 15 yaers old to eligible to create account')
    return render_template('index.html' , status='new')
       
       




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
    return render_template('customer_login.html' , status=c)




app.run(debug=True)  