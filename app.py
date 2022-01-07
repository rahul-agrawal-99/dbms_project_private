import os
from flask import Flask , render_template , redirect ,request
from werkzeug.utils import secure_filename
import db as db
app = Flask(__name__)

cid={}   # stores current user id 
total_p =0   # total purchase amount by user


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
        return render_template('admin_login.html' )    
  
    return ' <h1 style="text-align:center"> Authentication Failed </h1>'

@app.route("/project_login_table",methods=['POST','GET'])    
def proadminlog():
    return render_template('login_table.html' , val=db.login())    
  
@app.route("/go_back",methods=['POST','GET'])    
def back():
    return render_template('admin_login.html' )   
  
@app.route("/product_admin",methods=['POST','GET'])    
def adminprod():
    products = db.get_product_name()
    pid = products[len(products)-1][3]+1
    if request.method == 'POST':
        pname = request.form['pname']   
        price = request.form['price']   
        quanity = request.form['quantity']  
        img = request.files.get('imagefile', '')
        path =r'\static\assets\images'
        img.save(os.path.join(os.getcwd() + path , secure_filename(f'{pid}' + '.jpg')))
        db.insert_new_product(pid , pname , price , quanity)  
    return render_template('add_product.html' , prod = db.get_product_name())   

 
@app.route("/add_product",methods=['POST','GET'])    
def addprod():
    products = db.get_product_name()
    pid = products[len(products)-1][3]+1
    return render_template('add_new_prod.html' , pid = pid)    
  
@app.route('/update_prod/<int:id>')
def update_prod(id):
    pr =db.get_product_details_by_id(id)
    return render_template('update_prod.html' , pid = id ,pname =pr[0] , price = pr[2] ,stock =pr[1])


@app.route('/success_update/<int:id>' ,methods=['POST','GET'])
def update_prod_success(id):
    pid =id
    if request.method == 'POST':
        uprice = request.form['uprice']   
        uquanity = request.form['ustock'] 
        db.update_prod(pid,uprice ,uquanity)
    return redirect("/product_admin")

@app.route('/transaction')
def trans():
 
    return render_template('transaction.html' , t=db.get_transaction_details())    




           
tp=[]   # total price corresponding to p[]

p=[]   # it has list of products in cart , index +1 represents corresponding pid quantity 

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
        counter=0
        for i in prod:
            p.append(i)
            # print("total_p is ",p)
            if(i!=0):
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
    order_id.append(db.generate_order_id())
    return render_template('payment_page.html' , cid=cid['id'] , card_no=crd[0][1] ,total_amount=tpl, order_id =order_id[len(order_id)-1] )


    
@app.route("/payment",methods=['POST','GET'])    
def payment():
    l=len(tp)
    tpl=tp[l-1]
    crd=db.get_card_details(cid['id'])
    if request.method=='POST':
        cvv= request.form['cvv']
        otp= request.form['otp']
    actual_cvv = db.get_cvv(crd[0][1])
    if (actual_cvv !=int(cvv)):
        return render_template('payment_page.html' , cid=cid['id'] , card_no=crd[0][1] ,total_amount=tpl, order_id =order_id[len(order_id)-1] ,stat = "CVV Entered is Wrong")  
    if otp=="1234":
        new_bal = db.make_payment(crd[0][1] , tpl)
        if new_bal==False:
            return "Your Card Dont Have Enough Balance "
        db.transaction(order_id[len(order_id)-1],cid['id'],tpl)
        o=order_id[len(order_id)-1]
        db.update_orders(p,o)
        products =db.purchased_products(p)
        print("taken products :",products)
        return render_template('success.html' , total_pay = tpl , card_balance = new_bal ,order_id =order_id[len(order_id)-1] ,card_no=crd[0][1] ,products = products ) 
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


if __name__ == "__main__":
    app.run(debug=True, port=8000)

# app.run()            # for Production
# app.run(debug=True)          # for testing