import tkinter
import sqlite3
from user_actions import *
from product_actions import *

def login():
    global session
    global login_cnt
    user=txt_user.get()
    pas=txt_pass.get() 
    result=user_login(user,pas)
    if result:
        lbl_msg.configure(text="welcome to your account",fg="green")
        btn_login.configure(state="disabled") 
        txt_user.delete(0,"end")
        txt_pass.delete(0,"end")
        btn_logout.configure(state="active")
        btn_shop.configure(state="active")
        btn_admin.configure(state="active")
        login_cnt=3
        session=result
        
        access=accessibility(session)
        if not access:
            btn_submit.configure(state="disabled")
            btn_shop.configure(state="disabled")
            btn_admin.configure(state="disabled")
            lbl_msg2.configure(text="no access number",fg="red")

        elif int(access[1])==0 :
            btn_shop.configure(state="disabled")
            btn_admin.configure(state="disabled")
            lbl_msg2.configure(text="The login,submit,logout buttons are available",fg="yellow")

        elif int(access[1])==1 :
            btn_shop.configure(state="active")
            btn_admin.configure(state="disabled")
            lbl_msg2.configure(text="The login, submit, logout and shop buttons are available",fg="yellow")

        elif int(access[1])==2 :
            btn_shop.configure(state="active")
            btn_admin.configure(state="active")
            lbl_msg2.configure(text="all buttons are available",fg="yellow")
            
    else:
        lbl_msg.configure(text="wrong username or password",fg="red")
        login_cnt-=1
        if login_cnt==0 :
            btn_login.configure(state="disabled")
            lbl_msg.configure(text="3 times error occurred! login disabled!",fg="red")

def submit():
    user=txt_user.get()
    pas=txt_pass.get()
    result,errormsg=validation(user,pas)
    if result:
        user_submit(user,pas) 
        lbl_msg.configure(text="submit done!",fg="green") 
    else:
        lbl_msg.configure(text=errormsg ,fg="red")
    
def logout():
    btn_login.configure(state="active")
    btn_logout.configure(state="disabled")
    lbl_msg.configure(text="you are logged out now",fg="blue")
    btn_shop.configure(state="disabled")

def shop():
    def buy():
        pid=pidtxt.get()
        qnt=pqnttxt.get()
        if pid=="" or qnt=="":
            lbl_msg2.configure(text="fill the inputs",fg="red")
            return
        result=get_single_product(pid)
        if not result:
            lbl_msg2.configure(text="wrong product id",fg="red")
            return
        
        if int(qnt)>result[3]:
            lbl_msg2.configure(text="not enough products",fg="red")
            return
        
        if int(qnt) <= 0:
            lbl_msg2.configure(text="quantity should be at least 1",fg="red")
            return
        
        save_to_cart(pid,session,qnt)
        lbl_msg2.configure(text="add to cart successfully",fg="green")
        pidtxt.delete(0,"end")
        pqnttxt.delete(0,"end")

        edit_quantity(qnt,pid)
        lst.delete(0,"end")
        products=get_product()
        for product in products:
            text=f"ID={product[0]} , NAME={product[1]} , PRICE={product[2]} , QUANTITY={product[3]}"
            lst.insert("end",text)          
        
    win_shop=tkinter.Toplevel(win)
    win_shop.geometry("400x400")
    win_shop.title("shopping panel")
    
    lst=tkinter.Listbox(win_shop,width=50)
    lst.pack()  
    
    
    pidlbl=tkinter.Label(win_shop,text="ID: ")
    pidlbl.pack()
    pidtxt=tkinter.Entry(win_shop)
    pidtxt.pack()
    
    pqntlbl=tkinter.Label(win_shop,text="Quantity: ")
    pqntlbl.pack()
    
    pqnttxt=tkinter.Entry(win_shop)
    pqnttxt.pack()
    
    lbl_msg2=tkinter.Label(win_shop,text="")
    lbl_msg2.pack()
    
    btn_buy=tkinter.Button(win_shop,text="BUY", command=buy)
    btn_buy.pack()
    
    win_shop.mainloop()


def admin():
    def update_products():
        pname=pntxt.get()
        price=pprtxt.get()
        qnt=pqnt1txt.get()
        if pname=="" or price=="" or qnt=="" :
            lbl_msg2.configure(text="input should not be null",fg="red")
            return
        
        products=get_product()
        for product in products:
            if product[1] == pname :
                lbl_msg2.configure(text="product already exist",fg="red")
                return
        
        if not price.isdigit() or not qnt.isdigit():
            lbl_msg2.configure(text="please enter a number for price and quantity inputs",fg="red")
            return
        
        if int(price)<=0 or int(qnt)<=0 :
            lbl_msg2.configure(text="the price and quantity cannot be 0 or less",fg="red")
            return
        
        add_product(pname,price,qnt)
        lbl_msg2.configure(text="product successfully added",fg="green")
        pntxt.delete(0,"end")
        pprtxt.delete(0,"end")
        pqnt1txt.delete(0,"end")

    def users_accessibility():
        def access():
            uid=idtxt.get()
            ac=acctxt.get()
            if uid=="" or ac=="" :
                lbl_msg2.configure(text="input should not be null",fg="red")
                return
            
            if not uid.isdigit() or not ac.isdigit():
                lbl_msg2.configure(text="please enter a number for inputs",fg="red")
                return
            
            result=get_users(uid)
            if not result:
                lbl_msg2.configure(text="wrong user id",fg="red")
                return
            
            check=accessibility(uid)
            if check:
                lbl_msg2.configure(text="access level has been already set for this id !!!",fg="red")
                return
            
            if not (int(ac)==0 or int(ac)==1 or int(ac)==2) :
                lbl_msg2.configure(text="access level must be from 0 to 2",fg="red")
                return
            
            users_access(uid,ac)
            lbl_msg2.configure(text="accessability confirmed",fg="green")
            idtxt.delete(0,"end")
            acctxt.delete(0,"end")

        win_access=tkinter.Toplevel(win_admin)
        win_access.geometry("500x500")
        win_access.title("users access")

        lbl_msg=tkinter.Label(win_access,text="determine users access",fg="blue")
        lbl_msg.pack()

        lst_user=tkinter.Listbox(win_access,width=50)
        lst_user.pack()
        users=get_user()
        for user in users:
            text=f"ID={user[0]},NAME={user[1]},SCORE={user[4]}"
            lst_user.insert("end",text)

        lst_ac=tkinter.Listbox(win_access,width=50,height=3)
        lst_ac.pack()
        lst=["ac 0 : The login, submit and logout buttons are available",
            "ac 1 : The login, submit, logout and shop buttons are available",
            "ac 2 : The login, submit, logout, shop buttons and accessability are available"]
        for item in lst:
            lst_ac.insert("end",item)

        idlbl=tkinter.Label(win_access,text="user id: ")
        idlbl.pack()
        idtxt=tkinter.Entry(win_access)
        idtxt.pack()

        acclbl=tkinter.Label(win_access,text="user access: ")
        acclbl.pack()
        acctxt=tkinter.Entry(win_access)
        acctxt.pack()

        lbl_msg2=tkinter.Label(win_access,text="")
        lbl_msg2.pack()

        btn_confirm=tkinter.Button(win_access,text="Done",command=access)
        btn_confirm.pack()

    win_admin=tkinter.Toplevel(win)
    win_admin.geometry("300x300")
    win_admin.title("admin panel")

    pnlbl=tkinter.Label(win_admin,text="product name: ")
    pnlbl.pack()
    pntxt=tkinter.Entry(win_admin)
    pntxt.pack()
    
    pprlbl=tkinter.Label(win_admin,text="product price: ")
    pprlbl.pack()
    pprtxt=tkinter.Entry(win_admin)
    pprtxt.pack()

    pqnt1lbl=tkinter.Label(win_admin,text="product quantity: ")
    pqnt1lbl.pack()
    pqnt1txt=tkinter.Entry(win_admin)
    pqnt1txt.pack()

    lbl_msg2=tkinter.Label(win_admin,text="")
    lbl_msg2.pack()

    btn_buy=tkinter.Button(win_admin,text="add product",command=update_products)
    btn_buy.pack()

    btn_access=tkinter.Button(win_admin,text="users access",command=users_accessibility)
    btn_access.pack()

    win_admin.mainloop()
# ----------------------------------------------------------
session=""
login_cnt=3

win=tkinter.Tk()
win.geometry("400x400")

lbl_user=tkinter.Label(win,text="username: ")
lbl_user.pack()
txt_user=tkinter.Entry(win)
txt_user.pack()

lbl_pass=tkinter.Label(win,text="password: ")
lbl_pass.pack()
txt_pass=tkinter.Entry(win)
txt_pass.pack()

lbl_msg=tkinter.Label(win,text="")
lbl_msg.pack()

lbl_msg2=tkinter.Label(win,text="")
lbl_msg2.pack()

btn_login=tkinter.Button(win,text="Login",command=login)
btn_login.pack()

btn_submit=tkinter.Button(win,text="Submit",command=submit)
btn_submit.pack()

btn_logout=tkinter.Button(win,text="Logout",state="disabled", command=logout)
btn_logout.pack()

btn_shop=tkinter.Button(win,text="shop",state="disabled", command=shop)
btn_shop.pack()

btn_admin=tkinter.Button(win,text="admin",state="disabled",command=admin)
btn_admin.pack()

win.mainloop()




