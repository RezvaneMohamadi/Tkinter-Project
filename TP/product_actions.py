import sqlite3

cnt=sqlite3.connect("shop.db")

def get_product():
    sql=''' SELECT * FROM products '''
    result=cnt.execute(sql)
    rows=result.fetchall()
    return rows

def get_single_product(id1):
    sql=''' SELECT * FROM products WHERE id=? '''
    result=cnt.execute(sql,(id1,))
    row=result.fetchone()
    return row

def save_to_cart(pid,uid,qnt):
    sql=''' INSERT INTO cart(pid,uid,qnt)
            VALUES(?,?,?) '''
    cnt.execute(sql,(pid,uid,qnt))
    cnt.commit()

def edit_quantity(qnt,pid):
    result=get_single_product(pid)
    lst=list(result)
    x=lst[3] - int(qnt)

    sql=''' UPDATE products SET qnt=? WHERE id=? '''
    cnt.execute(sql,(x,pid))
    cnt.commit()
    print ("database has been updated !!!")

def add_product(pname,price,qnt):
    sql=''' INSERT INTO products(pname,price,qnt)
            VALUES(?,?,?) '''
    cnt.execute(sql,(pname,price,qnt))
    cnt.commit()