import mysql
from  mysql import connector
import _mysql_connector
from mysql.connector import Error
import pandas as pd
import random
from datetime import datetime
import time

u="root"
p="rahul"
db="mini"   # no change


def get_datetime_today():
    date=str(datetime.today()).split()[0]
    time=str(datetime.today()).split()[1][:8]
    return date,time

def get_age(b):
    d=get_datetime_today()
    by=int(b[:4])
    dy=int(d[0][:4])
    age=dy-by
    bm=int(b[5:7])
    dm=int(d[0][5:7])
    m=dm-bm
    bd=int(b[8:])
    dd= int(d[0][8:])
    if (m < 0 or (m == 0 and dd < bd)):
        age=age-1
    return age;

def connect(hname,uname,upassword,dbname):
    connection=None
    try:
        connection=mysql.connector.connect(host=hname,user=uname,password=upassword,database=dbname,auth_plugin='mysql_native_password')
        print("connection Successful")
    except Error as e:
        print(f"Error ocuured {e}")
    return connection

def execute_query(connection,query):
    c=connection.cursor()
    try:
        c.execute(query)
        print("query executed As: ",query)
        commit(connection)
    except Error as e:
        print(e)

def commit(connection):
    try:
        connection.commit()
        print("commited success")
    except Error as e:
        print(e)
        

def print_val(c,q):
    c1=c.cursor()
    try:
        c1.execute(q)
        r=c1.fetchall()
        return r
        # print("query executed As: ",query)
    except Error as e:
        print(e)
        
def login():     
    db="mini"
    c=connect("localhost",'root','rahul',db)
    q='select * from project_login'
    r=print_val(c,q)
    return r
  
        
def check_login(i,pas):  #data stored in  Flask_data 

    c=connect("localhost",u,p,db)
    q=f"select password from project_login where id='{i}'"
    actual_pass=print_val(c,q)
    if (len(actual_pass) == 0):
        return f"no user found as {i} , please create one "
    actual_pass=actual_pass[0][0]
    if pas==actual_pass:
        status="yes"
    else:
        status="no"
        
    return status


def insert_new_user(name,email,phone,bday,userid,pas):  #data stored in  Flask_data 
    c=connect("localhost",u,p,db)
    q=f"select id from project_login where id='{userid}'"
    status=print_val(c,q)
    if(len(name)==0):
        return 'blankname'
    
    if(len(bday)==0):
        return 'blankbday'
    
    if(userid==""):
        return 'blanku'
    if(pas==""):
        return 'blankp'
    if(len(status)!=0):
        print('userID already exist ')
        return 'exist'
    age=get_age(bday)
    print('age is',age)
    q=f"insert into project_login values ('{userid}','{pas}','{name}','{email}','{phone}','{bday}',{age})"
   
    execute_query(connect("localhost",u,p,db),q)
    commit(connect("localhost",u,p,db))
    
