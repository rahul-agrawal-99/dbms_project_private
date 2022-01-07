# import sqlite3

# connection = sqlite3.connect("project.db")
# cursor = connection.cursor()
# # cursor.execute("CREATE TABLE project_login( id TEXT PRIMARY KEY,password  TEXT,name TEXT ,email TEXT,phone TEXT ,bday date ,age  INTEGER )")

# # cursor.execute("CREATE TABLE product_details(pid INTEGER PRIMARY KEY,pname TEXT ,stock INTEGER, price INTEGER , CHECK (stock>=0) )")
# # cursor.execute("CREATE TABLE card_details(cid TEXT PRIMARY KEY,card_no BIGINT NOT NULL , cvv INTEGER NOT NULL , card_balance INTEGER , FOREIGN KEY (cid) REFERENCES project_login(id) ) ")
# # cursor.execute("CREATE TABLE complate_orders (order_id INTEGER , product_id INTEGER )")
# # cursor.execute("CREATE TABLE transaction_history (order_id INTEGER PRIMARY KEY,cid TEXT , total_amount INTEGER  ,transaction_time TEXT )")
# # cursor.execute("CREATE TABLE card_history(card_no INTEGER , updated_balance INTEGER , transaction_time TEXT, by_user TEXT )")

# # cursor.execute("INSERT INTO product_details values (1,'fogg deo',78,45)")
# # cursor.execute("INSERT INTO product_details values (2,'himalaya pimple clear',9,75)")
# # cursor.execute("INSERT INTO product_details values (3,'parachute coconut oil',60,80)")
# # cursor.execute("INSERT INTO product_details values (4,'pears soap',70,20)")
# # cursor.execute("INSERT INTO product_details values (5,'pepsodent paste',12,65)")
# # cursor.execute("INSERT INTO product_details values (6,'ponds powder',8,55)")
# # cursor.execute("INSERT INTO product_details values (7,'toothbrush ',89,15)")
# # cursor.execute("INSERT INTO product_details values (8,'corn flakes',7,145)")
# # cursor.execute("INSERT INTO product_details values (9,'indo noodles 500g pack',3,225)")
# # cursor.execute("INSERT INTO product_details values (10,'coca-cola 500ml',32,65)")

# # connection.commit()

# # cursor.execute("CREATE TRIGGER amount_deduct AFTER UPDATE on card_details BEGIN INSERT INTO card_history values(new.card_no,new.card_balance,current_timestamp ,new.cid )END;")



# rows = cursor.execute("select * from product_details").fetchall()
# print(rows)
