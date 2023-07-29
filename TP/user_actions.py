import sqlite3

cnt=sqlite3.connect("shop.db")

def user_login(user,pas):
    sql=''' SELECT * FROM users WHERE user=? and pass=?'''
    result=cnt.execute(sql,(user,pas))
    rows=result.fetchall()
    if len(rows)<1:
        return False
    else:
        return rows[0][0]
    
def validation(user,pas):
    if user=="" or pas=="" :
        return False,"fill the inputs"

    if len(pas) < 8 :
        return False,"password length error !!!"

    if pas.isalpha() or pas.isdigit():
        return False,"password combination error !!!"

    sql=''' SELECT * FROM users WHERE user=? '''
    result=cnt.execute(sql,(user,))
    rows=result.fetchall()
    if len(rows) > 0 :
        return False,"username already exist !"

    else:
        return True,""

def user_submit(user,pas):
    sql=''' INSERT INTO users(user,pass) VALUES(?,?) '''
    cnt.execute(sql,(user,pas))
    cnt.commit()

def get_user():
    sql=''' SELECT * FROM users '''
    result=cnt.execute(sql)
    rows=result.fetchall()
    return rows
    
def get_users(uid):
    sql=''' SELECT * FROM users WHERE id=? '''
    result=cnt.execute(sql,(uid,))
    row=result.fetchone()
    return row

def users_access(uid,acc):
    sql=''' INSERT INTO access(uid,acc) VALUES(?,?) '''
    cnt.execute(sql,(uid,acc))
    cnt.commit()

def accessibility(id):
    sql=''' SELECT * FROM access WHERE uid=? '''
    result=cnt.execute(sql,(id,))
    row=result.fetchone()
    return row