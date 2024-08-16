from tkinter import *
import re
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog as fd
from tkcalendar import Calendar, DateEntry
import random
from email.message import EmailMessage
import smtplib
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mysql.connector
import math
import os
from plyer import notification
import time
from datetime import date

mycon = mysql.connector.connect(user='root',host='localhost',passwd='SQL_Password',database='Supermarket')
cur=mycon.cursor()

tables=['Baby_products', 'Books', 'Cooking_supplements', 'Cosmetics', 'Food', 'Fruits_vegetables', 'Stationery', 'Toys']
QTY={'baby_products':[25, 50, 10, 45, 50, 45, 50, 45, 35],
     'books':[6, 12, 10, 30, 30, 30, 30, 25, 23],
     'cooking_supplements':[30, 35, 20, 20, 25, 60, 10, 15, 15],
     'cosmetics':[25, 20, 40, 35, 50, 45, 40, 40, 35],
     'food':[6, 12, 25, 15, 10, 20, 20, 20, 20],
     'fruits_vegetables':[30, 35, 20, 20, 25, 60, 60, 70, 80],
     'stationery':[50, 50, 20, 30, 15, 20, 70, 50, 50],
     'toys':[20, 20, 20, 20, 20, 20, 20, 20, 20]}

aaj = date.today().strftime("%B %d")
if aaj in ['January 1','February 1','March 1','April 1','May 1','June 1','July 1','August 1','September 1','October 1','November 1','December 1']:
    for i in range(len(tables)):
        cur.execute(f"select Name from {tables[i]}")
        data=cur.fetchall()
        names=[]
        for name in data:
            names.append(name[0])
        for j in range(len(names)):
            exe=f'update {tables[i]} SET QTY_Available = {QTY[str(tables[i]).lower()][j]} where Name = "{names[j]}"'
            print(exe)
            cur.execute(exe)
            mycon.commit()

cpy=''
udata=''
def new_acc():
    global ws_main
    ws = Tk()
    ws.title('Super Market')
    ws.geometry('1000x800')
    ws.config(bg="blue")
    def nxt():
        def plogin():
            p_h=phone.get()
            f_name=fname.get()
            l_name=lname.get()
            e_m=em.get()
            u_name=uname.get()
            d_b=str(dob.get_date())
            passwd=pwd.get()
            cur.execute('select count(*) from uinfo')
            dn = cur.fetchall()
            
            try:
                u_i_d=dn[0][0]+1
                ins=f'insert into ukey Values({u_i_d},"{u_name}","{passwd}")'

                cur.execute(ins)
                mycon.commit()
            except:
                messagebox.showerror('','Please pick another username')
                return
            ins=f'insert into uinfo Values({u_i_d},"{f_name}","{l_name}","{d_b}","{p_h}","{e_m}")'
            
            cur.execute(ins)
            mycon.commit()
            try:
                folder=f'./UserData/{u_i_d}'
                os.mkdir(folder)
            except:
                pass
            clear = [f'./UserData/{u_i_d}/Cart_Baby_products.txt',f'./UserData/{u_i_d}/Cart_Books.txt',f'./UserData/{u_i_d}/Cart_Cooking_supplements.txt',f'./UserData/{u_i_d}/Cart_Cosmetics.txt',f'./UserData/{u_i_d}/Cart_Food.txt',f'./UserData/{u_i_d}/Cart_Fruits_vegetables.txt',f'./UserData/{u_i_d}/Cart_Stationery.txt',f'./UserData/{u_i_d}/Cart_Toys.txt']
            for file in clear:
                x = open(file,"w+")
                x.close()
            ws.destroy()
            wsn.destroy()
            login()
        ws.withdraw()
        wsn = Tk()
        wsn.title('Super Market')
        wsn.geometry('1000x800')
        wsn.config(bg="blue")
        frame = Frame(wsn, padx=20, pady=20)
        frame.place(x=350,y=50)

        Label(frame, text="Some More Details..",font=("Times", "24", "bold")).grid(row=0, columnspan=3, pady=10)
        Label(wsn, text='Full Residential Address :', font=("Times", "22"),wraplength=250).place(x=50,y=350)
        Label(wsn, text='Phone Number :', font=("Times", "24")).place(x=50,y=550)
        Label(wsn, text='Date Of Birth :', font=("Times", "24")).place(x=50,y=250)
        Label(wsn, text='Pick your Username :', font=("Times", "24"),wraplength=250).place(x=50,y=650)
        
        add = Text(wsn, height=8, width=40,font=('Times New Roman',14))
        add.place(x=300,y=350)
        phone = Entry(wsn, width=12,font=('Arial',24))
        phone.place(x=300,y=550)
        dob = DateEntry(wsn,date_pattern='dd-mm-yyyy', width= 12,font =('Arial',24),background= "magenta3", foreground= "white",bd=2)
        dob.place(x=300,y=250)
        uname = Entry(wsn, width=20,font=('Arial',24))
        uname.place(x=300,y=650)
        loginb = Button(wsn, text="Proceed to login", padx=20, pady=10, relief=SOLID, font=("Times", "14", "bold"), command=plogin).place(x=700,y=700)
        wsn.mainloop()
    def back():
        ws_main.deiconify()
        ws.destroy()
    def e_verify():
        sender = "supermarketnoreply7@gmail.com"
        receiver = em.get()
        password = "rclmapnajqpuqglh"
        msg_body = f'Hi {fname.get()} {lname.get()}. Thanks for registering with SuperMarket.\nYour e-mail ID is {em.get()} and password is {pwd.get()}'
        msg = EmailMessage()
        msg['subject'] = 'Registeration Successfull For SuperMarket.'   
        msg['From'] = formataddr(('SuperMarket', 'supermarketnoreply7@gmail.com'))
        msg['to'] = receiver
        msg.set_content(msg_body)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(sender,password)
        s.send_message(msg)
    def sendOtp():
        cur.execute("Select email from uinfo")
        existing_user_chk=cur.fetchall()
        for i in existing_user_chk:
            if em.get().lower() in i or em.get() in i:
                messagebox.showerror('',"Account already exists")
                em.delete(0,END)
                break
        else:
            global cpy
            cpy=''
            otp_no = str(random.randint(1000, 9999))   
            cpy += otp_no
            sender = "supermarketnoreply7@gmail.com"
            receiver = em.get()
            password = "rclmapnajqpuqglh"
            msg_body = f'Hi {fname.get()} {lname.get()}, your OTP for the app is {cpy}.\nDo NOT share with anyone.'
            msg = EmailMessage()
            msg['subject'] = 'OTP'   
            msg['From'] = formataddr(('SuperMarket', 'supermarketnoreply7@gmail.com'))
            msg['to'] = receiver
            msg.set_content(msg_body)
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(sender,password)
            s.send_message(msg)
            
            
            return cpy

    def regis():
        enteredOtp = str(otp.get())
        expectedOtp = str(cpy)
        check_count = 0

        if fname.get() == "":
            warn = "First name can't be empty!"
        else:
            check_count += 1
        if lname.get() == "":
            warn = "Last name can't be empty!"
        else:
            check_count += 1
        if em.get() == "":
            warn = "Email can't be empty!"
        else:
            check_count += 1
        if pwd.get() == "":
            warn = "Password can't be empty!"
        else:
            check_count += 1
        if otp.get() == "":
            warn = "Otp can't be empty!"
        else:
            check_count += 1
        if pwd.get()!=pwdr.get():
            warn="Passwords Don't Match."
        else:
            check_count+=1

        if check_count == 6:
            if (expectedOtp == enteredOtp):
                reg.destroy()
                ext.destroy()
                nxtb = Button(frame, text="Next", padx=20, pady=10, relief=SOLID, font=("Times", "14", "bold"), command=nxt)
                nxtb.grid(row=10, column=0, pady=20)
                Label(frame, text='OTP Verified successfully.', font=("Times", "14")).grid(row=10, column=1, pady=5)
                fname.config(state='disabled')
                lname.config(state='disabled')
                em.config(state='disabled')
                otp.config(state='disabled')
                pwd.config(state='disabled')
                pwdr.config(state='disabled')
                otpp.config(state='disabled')
                e_verify()

            else:
                messagebox.showerror('','Incorrect Otp')
        else:
            messagebox.showerror('', warn)

    frame = Frame(ws, padx=20, pady=20)
    frame.pack(expand=True)

    Label(frame, text="Create New Account",font=("Times", "24", "bold")).grid(row=0, columnspan=3, pady=10)
    Label(frame, text='First Name', font=("Times", "14")).grid(row=1, column=0, pady=5)
    Label(frame, text='Last Name', font=("Times", "14")).grid(row=2, column=0, pady=5)
    Label(frame, text='Email Address', font=("Times", "14")).grid(row=3, column=0, pady=5)
    Label(frame, text='Password', font=("Times", "14")).grid(row=5, column=0, pady=5)
    Label(frame, text='Re-enter Password', font=("Times", "14")).grid(row=6, column=0, pady=5)
    Label(frame, text='Enter OTP', font=("Times", "14")).grid(row=4, column=0, pady=5)

    fname = Entry(frame, width=30)
    
    lname = Entry(frame, width=30)
    em = Entry(frame, width=30)
    otp = Entry(frame, width=30)
    pwd = Entry(frame, width=30,show='*')
    passwd=pwd.get()
    pwdr = Entry(frame, width=30,show='*')
    
    fname.grid(row=1, column=1)
    lname.grid(row=2, column=1)
    em.grid(row=3, column=1)
    otp.grid(row=4, column=1)
    pwd.grid(row=5, column=1)
    pwdr.grid(row=6, column=1)

    reg = Button(frame, text="Register", padx=20, pady=10, relief=SOLID, font=("Times", "14", "bold"), command=regis)
    ext = Button(frame, text="Back", padx=20, pady=10, relief=SOLID, font=("Times", "14", "bold"), command=back)
    otpp = Button(frame, text="Send OTP", padx=10, relief=RAISED, font=("Times", "10", "bold"), command=sendOtp)
    otpp.grid(row=3, column=2, pady=20)
    ext.grid(row=10, column=0, pady=20)
    reg.grid(row=10, column=2)

    ws.mainloop()

def login():
    global udata
    global ws_main
    def home():
        ws_main.deiconify()
        wsl.destroy()
    cur.execute('select first_name,last_name,email,password,username,ukey.UID from uinfo,ukey where uinfo.UID=ukey.UID;')
    data=cur.fetchall()
    udata=''
    def auth():
        global udata
        for i in data:
            if (em.get() in i or em.get().lower()in i) and pwd.get() in i:
                udata=i
                
                ws_main.destroy()
                wsl.destroy()
                try:
                    os.mkdir("./UserData")
                except:
                    pass
                try:
                    os.mkdir(f"./UserData/{udata[-1]}")
                except:
                    pass
                for i in tables:
                    try:
                        file_user=open(f'./UserData/{udata[-1]}/Cart_{i}.txt',"r")
                        file_user.close()
                    except:
                        file_user=open(f'./UserData/{udata[-1]}/Cart_{i}.txt',"w+")
                        file_user.close()
                app()
                return
            elif ((em.get() in i or em.get().lower()in i) and pwd.get() not in i):
                messagebox.showerror('','Login Credentials are incorrect.')
                em.delete(0,END)
                pwd.delete(0,END)
                break
            else:
                continue
        else:
            messagebox.showerror('','Account Does not exist.')
            em.delete(0,END)
            pwd.delete(0,END)
    
    wsl = Tk()
    wsl.title('Super Market')
    wsl.geometry('1000x800')
    wsl.config(bg="blue")

    frame = Frame(wsl, padx=20, pady=20)
    frame.pack(expand=True)

    Label(frame, text="Login",font=("Times", "24", "bold")).grid(row=0, columnspan=3, pady=10)
    Label(frame, text='Email Address', font=("Times", "14")).grid(row=3, column=0, pady=5)
    Label(frame, text='Password', font=("Times", "14")).grid(row=5, column=0, pady=5)

    em = Entry(frame, width=30)
    pwd = Entry(frame, width=30,show='*')
    em.grid(row=3, column=1)
    pwd.grid(row=5, column=1)

    back = Button(frame, text="Home", padx=20, pady=10, relief=SOLID, font=("Times", "14", "bold"), command=home)
    back.grid(row=10, column=0)
    login = Button(frame, text="Login", padx=20, pady=10, relief=SOLID, font=("Times", "14", "bold"), command=auth)
    login.grid(row=10, column=2)
    wsl.mainloop()
    
def app():
    def restart():
        global ws_main
        wsa.destroy()
        ws_main = Tk()
        ws_main.title('Super Market')
        ws_main.geometry('1000x800')
        ws_main.config(bg='green')
        try:
            img=PhotoImage(file="./Local/sbg.png")
            label = Label(ws_main,image=img)
            label.place(x=0,y=0)
        except:
            pass
        frame = Frame(ws_main, padx=50, pady=50)
        frame.pack(expand=True)

        Label(frame, text="Welcome to Supermarket!",font=("Times", "24", "bold")).grid(row=0, columnspan=3, pady=10)

        new = Button(frame, text="Create Account", padx=20, pady=10, relief=SOLID, font=("Times", "14", "bold"), command=pnew_acc)
        new.grid(row=18, column=0,pady=10)

        old = Button(frame, text="Login", padx=20, pady=10, relief=SOLID, font=("Times", "14", "bold"), command=blogin)
        old.grid(row=18, column=1,pady=10)

        ext = Button(frame, text="Exit", padx=20, pady=10, relief=SOLID, font=("Times", "14", "bold"), command=lambda:ws_main.destroy())
        ext.grid(row=18, column=3,pady=10)
        ws_main.mainloop()
    def pro():
       
       
        
        if var.get()!=0:
            wsa.destroy()
            final_screen(var.get())
        else:
            messagebox.showerror('',"Please select an option")
    def show():
        def hide():
            f2.destroy()
            m2 = Button(wsa, text="Show Menu", padx=20, pady=10,width =10,height =1, relief=SOLID, font=("Times", "14", "bold"),command=show).place(x=50,y=100)
        m = Button(wsa, text="Hide Menu", padx=20, pady=10,width =10,height =1, relief=SOLID, font=("Times", "14", "bold"),command=hide).place(x=50,y=100)
        f2 = Frame(wsa, padx=1, pady=1,bg="yellow")
        f2.place(x=40,y=170)
        '''update = Button(f2, text="Update Details", padx=20, pady=10,width =10,height =1, relief=SOLID, font=("Times", "14", "bold"),command=lambda:wsa.destroy())
        update.pack(padx=10,pady=10)'''
        cart = Button(f2, text="Go to cart", padx=20, pady=10,width =10,height =1, relief=SOLID, font=("Times", "14", "bold"),command=Cart)
        cart.pack(padx=10,pady=10)
        log = Button(f2, text="Logout", padx=20, pady=10,width =10,height =1, relief=SOLID, font=("Times", "14", "bold"),command=restart)
        log.pack(padx=10,pady=10)
    def Cart():
        def bta():
            wsc.destroy()
            wsa.deiconify()
        wsa.withdraw()
        wsc = Tk()
        wsc.title('Cart')
        wsc.geometry('800x600')
        wsc.config(bg="orange")
        text =Text(wsc,width=35,height=30)
        text.place(x=50,y=1)
        text2 =Text(wsc,width=30,height=30)
        text2.place(x=325,y=1)
        text3 =Text(wsc,width=25,height=30)
        text3.place(x=500,y=1)
        clear = [f'./UserData/{udata[-1]}/Cart_Baby_products.txt',f'./UserData/{udata[-1]}/Cart_Books.txt',f'./UserData/{udata[-1]}/Cart_Cooking_supplements.txt',f'./UserData/{udata[-1]}/Cart_Cosmetics.txt',f'./UserData/{udata[-1]}/Cart_Food.txt',f'./UserData/{udata[-1]}/Cart_Fruits_vegetables.txt',f'./UserData/{udata[-1]}/Cart_Stationery.txt',f'./UserData/{udata[-1]}/Cart_Toys.txt']
        
        for file in clear[0:3]:
            try:
                f = open(file)
                for i in f:
                    text.insert(INSERT,i)
                text.insert(INSERT,'\n')
            except:
                continue
        for file2 in clear[3:6]:
            try:
                f2 = open(file2)
                for j in f2:
                    text2.insert(INSERT,j)
                text2.insert(INSERT,'\n')
            except:
                continue
        for file3 in clear[6::]:
            try:
                f3 = open(file3)
                for k in f3:
                    text3.insert(INSERT,k)
                text3.insert(INSERT,'\n')
            except:
                continue
        text.config(state='disabled')
        text2.config(state='disabled')
        text3.config(state='disabled')
        ext = Button(wsc, text="Back", padx=20, pady=10,width =10,height =1, relief=SOLID, font=("Times", "14", "bold"),command=bta).place(x=625,y=535)
        gb= Button(wsc, text="Get Bill", padx=20, pady=10,width =10,height =1, relief=SOLID, font=("Times", "14", "bold"),command=bill).place(x=50,y=535)
    wsa = Tk()
    wsa.title('Super Market')
    wsa.geometry('1100x600')
    wsa.config(bg="aqua")
    frame = Frame(wsa, padx=20, pady=20)
    frame.pack(pady=20, padx=10)
    Label(wsa, text= f'Hi {udata[0]} {udata[1]},', font= ('Lucida 15 italic'),background="aqua").place(x=5,y=10)
    Label(frame, text="Welcome to Supermarket!",font=("Times", "24", "bold")).grid(row=0, columnspan=3, pady=10)
    Label(wsa, text= "What would you like to purchase today?", font= ('Helvetica 20 bold'),background="aqua").place(x=280,y=150)
    var = IntVar()

    C1 = Radiobutton(wsa, text="Food",font = ('Times 14 bold'), relief = RAISED ,width=21, anchor="w",bg='white',variable = var,value=1).place(x=280,y=200)
    C2 = Radiobutton(wsa, text = "Cosmetics", font = ('Times 14 bold'), relief = RAISED ,width=21, anchor="w",bg='white',variable = var,value=2).place(x=280,y=230)
    C3 = Radiobutton(wsa, text = "Baby Products", font = ('Times 14 bold'), relief = RAISED ,width=21, anchor="w",bg='white',variable = var,value=3).place(x=280,y=260)
    C4 = Radiobutton(wsa, text = "Toys",font = ('Times 14 bold'), relief = RAISED ,width=21, anchor="w",bg='white',variable = var,value=4).place(x=280,y=290)
    C5 = Radiobutton(wsa, text="Fruits And Vegetables",font = ('Times 14 bold'), relief = RAISED ,width=21, anchor="w",bg='white',variable = var,value=5).place(x=550,y=200)
    C6 = Radiobutton(wsa, text = "Cooking Supplements", font = ('Times 14 bold'), relief = RAISED ,width=21, anchor="w",bg='white',variable = var,value=6).place(x=550,y=230)
    C7 = Radiobutton(wsa, text = "Stationery", font = ('Times 14 bold'), relief = RAISED ,width=21, anchor="w",bg='white',variable = var,value=7).place(x=550,y=260)
    C8 = Radiobutton(wsa, text = "Books",font = ('Times 14 bold'), relief = RAISED ,width=21, anchor="w",bg='white',variable = var,value=8).place(x=550,y=290)
    ext = Button(wsa, text="PROCEED", padx=20, pady=10,width =10,height =1, relief=SOLID, font=("Times", "14", "bold"),command=pro).place(x=625,y=435)
    menu = Button(wsa, text="Show Menu", padx=20, pady=10,width =10,height =1, relief=SOLID, font=("Times", "14", "bold"),command=show).place(x=50,y=100)
    wsa.mainloop()
def final_screen(arg):
    def cart(c,q1,q2,q3,q4,q5,q6,q7,q8,q9):
        Label(wsp, text= "Added to Cart.", font= ('Lucida 53 bold'),background="purple").place(x=550,y=550)
        spinboxes = [s1,s2,s3,s4,s5,s6,s7,s8,s9]
        for obj in spinboxes:
            obj.config(state='disabled')
        wd=[]
        Lq=[q1,q2,q3,q4,q5,q6,q7,q8,q9]
        for i in range(0,len(L)):
            if Lq[i].get()!='0':
                wd.append([L[i],Lq[i].get()])
        
        cfile=open(f'./UserData/{udata[-1]}/Cart_{c}.txt',"w+")
        for i in wd:
            for j in i:
                cfile.write(j+'\t')
            cfile.write('\n')
        cfile.flush()
    def prev():
        wsp.destroy()
        app()
    wsp = Tk()
    wsp.title('Super Market')
    wsp.geometry('1400x700')
    wsp.config(bg="purple")
    Qty1=StringVar(value=0)
    Qty2=StringVar(value=0)
    Qty3=StringVar(value=0)
    Qty4=StringVar(value=0)
    Qty5=StringVar(value=0)
    Qty6=StringVar(value=0)
    Qty7=StringVar(value=0)
    Qty8=StringVar(value=0)
    Qty9=StringVar(value=0)
    if arg ==1:
        table_name='Food'
    elif arg ==2:
        table_name='Cosmetics'
    elif arg ==3:
        table_name='Baby_Products'
    elif arg ==4:
        table_name='Toys'
    elif arg ==5:
        table_name='Fruits_vegetables'
    elif arg ==6:
        table_name='Cooking_supplements'
    elif arg ==7:
        table_name='Stationery'
    elif arg ==8:
        table_name='Books'
    wsp.title(f'{table_name}')
    cur.execute(f'select name from {table_name}')
    names=cur.fetchall()
    L=[]
    for i in names:
        L.append(i[0])
    Label(wsp, text= f"{table_name}", font= ('Lucida 25 bold underline'),background="aqua").place(x=550,y=30)
    if table_name in ('Food','Fruits_vegetables'):
        Label(wsp, text= " Note: All Quantities are in kg", font= ('Lucida 25 bold underline'),background="aqua").place(x=360,y=400)
    else:
        Label(wsp, text= " Note: Quantity corresponds to respective 1 unit of product. ", font= ('Lucida 25 bold underline'),background="aqua").place(x=360,y=400)
    Label(wsp, text= f'{L[0]}', font= ('Lucida 16 italic'),background="aqua",wraplength=180).place(x=5,y=100)
    s1 = Spinbox(wsp,from_ = 0,to =50,textvariable=Qty1,font =('Lucida 15 italic'))
    s1.place(x=200,y=100)
    Label(wsp, text= f'{L[1]}', font= ('Lucida 16 italic'),background="aqua",wraplength=180).place(x=5,y=200)
    s2 = Spinbox(wsp,from_ = 0,to =50,textvariable=Qty2,font =('Lucida 15 italic'))
    s2.place(x=200,y=200)
    Label(wsp, text= f'{L[2]}', font= ('Lucida 16 italic'),background="aqua",wraplength=180).place(x=5,y=300)
    s3 = Spinbox(wsp,from_ = 0,to =50,textvariable=Qty3,font =('Lucida 15 italic'))
    s3.place(x=200,y=300)
    
    Label(wsp, text= f'{L[3]}', font= ('Lucida 15 italic'),background="aqua",wraplength=180).place(x=470,y=100)
    s4= Spinbox(wsp,from_ = 0,to =50,textvariable=Qty4,font =('Lucida 15 italic'))
    s4.place(x=665,y=100)
    Label(wsp, text= f'{L[4]}', font= ('Lucida 15 italic'),background="aqua",wraplength=180).place(x=470,y=200)
    s5 = Spinbox(wsp,from_ = 0,to =50,textvariable=Qty5,font =('Lucida 15 italic'))
    s5.place(x=665,y=200)
    Label(wsp, text= f'{L[5]}', font= ('Lucida 15 italic'),background="aqua",wraplength=180).place(x=470,y=300)
    s6 = Spinbox(wsp,from_ = 0,to =50,textvariable=Qty6,font =('Lucida 15 italic'))
    s6.place(x=665,y=300)
    
    Label(wsp, text= f'{L[6]}', font= ('Lucida 15 italic'),background="aqua",wraplength=180).place(x=935,y=100)
    s7= Spinbox(wsp,from_ = 0,to =50,textvariable=Qty7,font =('Lucida 15 italic'))
    s7.place(x=1110,y=100)
    Label(wsp, text= f'{L[7]}', font= ('Lucida 15 italic'),background="aqua",wraplength=180).place(x=935,y=200)
    s8 = Spinbox(wsp,from_ = 0,to =50,textvariable=Qty8,font =('Lucida 15 italic'))
    s8.place(x=1110,y=200)
    Label(wsp, text= f'{L[8]}', font= ('Lucida 15 italic'),background="aqua",wraplength=180).place(x=935,y=300)
    s9 = Spinbox(wsp,from_ = 0,to =50,textvariable=Qty9,font =('Lucida 15 italic'))
    s9.place(x=1110,y=300)
    
    atc = Button(wsp, text="Add to Cart", padx=20, pady=10,width =10,height =1, relief=SOLID, font=("Times", "23", "bold"),command=lambda:cart(f'{table_name}',Qty1,Qty2,Qty3,Qty4,Qty5,Qty6,Qty7,Qty8,Qty9)).place(x=550,y=550)
    back = Button(wsp, text="Back", padx=20, pady=10,width =10,height =1, relief=SOLID, font=("Times", "23", "bold"),command=prev).place(x=150,y=550)

    spinboxes = [s1,s2,s3,s4,s5,s6,s7,s8,s9]
    for obj in spinboxes:
        obj.config(state='readonly')
    wsp.mainloop()

def bill():
    def notif():
        title="Order Recieved"
        message=f'Dear {udata[0]},your order has been received. You will receive a confirmation mail shortly. Keep Shopping!'
        notification.notify(title= title,message= message,timeout= 30)
        '''os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(message, title))'''
    def em_send():
        body= f'Hello {udata[0]} {udata[1]}, Thank you for placing an order.\nPlease find your attached bill.\nWe would love to see you again.'
        sender_address = 'supermarketnoreply7@gmail.com'
        sender_pass = 'rclmapnajqpuqglh'
        receiver_address = udata[2]
        msg = MIMEMultipart()
        msg['From'] = formataddr(('SuperMarket', 'supermarketnoreply7@gmail.com'))
        msg['To'] = receiver_address
        msg['Subject'] = 'Bill'
        msg.attach(MIMEText(body, 'plain'))
        attach_file_name = "Bill.txt"
        attach_file = open("./Local/Bill.txt",'rb')
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload)
        payload.add_header('Content-Disposition', 'attachment', filename=attach_file_name)
        msg.attach(payload)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(sender_address, sender_pass)
        text = msg.as_string()
        s.sendmail(sender_address, receiver_address, text)
        s.quit()
        order_save = f'insert into all_orders(UID,username,Total_Bill_Amt) Values({udata[-1]},"{udata[-2]}",{math.ceil(sum(price))})'
        
        cur.execute(order_save)
        mycon.commit()
        privacy=open("./Local/Bill.txt","w+")
        privacy.close()
        clear = [f'./UserData/{udata[-1]}/Cart_Baby_products.txt',f'./UserData/{udata[-1]}/Cart_Books.txt',f'./UserData/{udata[-1]}/Cart_Cooking_supplements.txt',f'./UserData/{udata[-1]}/Cart_Cosmetics.txt',f'./UserData/{udata[-1]}/Cart_Food.txt',f'./UserData/{udata[-1]}/Cart_Fruits_vegetables.txt',f'./UserData/{udata[-1]}/Cart_Stationery.txt',f'./UserData/{udata[-1]}/Cart_Toys.txt']
        for file in clear:
            x = open(file,"w+")
            x.close()
        
        return
    items=[]
    quantities=[]
    price=[]
    Total=[]
    clear = [f'./UserData/{udata[-1]}/Cart_Baby_products.txt',f'./UserData/{udata[-1]}/Cart_Books.txt',f'./UserData/{udata[-1]}/Cart_Cooking_supplements.txt',f'./UserData/{udata[-1]}/Cart_Cosmetics.txt',f'./UserData/{udata[-1]}/Cart_Food.txt',f'./UserData/{udata[-1]}/Cart_Fruits_vegetables.txt',f'./UserData/{udata[-1]}/Cart_Stationery.txt',f'./UserData/{udata[-1]}/Cart_Toys.txt']
    for indx in range(len(clear)):
        try:
            file_obj=open(clear[indx])
        except:
            continue
        for item in file_obj:
            s=''
            for x in range(0,len(item.split())-1):
                s+=str(item.split()[x])+' '
            items.append(s)
            quantities.append(item.split()[-1])
            q=f"select price from {tables[indx]} where name = '{s.rstrip()}'"
            cur.execute(q)
            get_price=cur.fetchall()
            price.append(get_price[0][0])
            Total.append(int(item.split()[-1])*get_price[0][0])
            up=f"update {tables[indx]} SET QTY_Available = QTY_Available - {int(item.split()[-1])} WHERE Name='{s.rstrip()}'"
            cur.execute(up)
            
  
    f = open("./Local/Bill.txt","w+")
    f.write(f'Hi {udata[0]} {udata[1]}, \n')
    f.write("Your bill is as follows: \n\n")
    heading = str("Item Name"+' '*24+'Quantitiy\tPrice Per Item\tTotal\n')
    f.write(heading)
    for i in range(len(items)):
        line = str(f'{items[i]}'+" "*(35-len(items[i]))+f'{quantities[i]}\t\t{price[i]}\t\t{Total[i]}\n')
        f.write(line)
    else:
        f.write('\n')
        f.write(f'Subtotal[inclusive of taxes]:\t\t{math.ceil(sum(Total))}')
        f.close()
    notif()
    em_send()
def pnew_acc():
    ws_main.withdraw()
    new_acc()
def blogin():
    ws_main.withdraw()
    login()
ws_main = Tk()
ws_main.title('Super Market')
ws_main.geometry('1000x800')
ws_main.config(bg='green')
try:
    img=PhotoImage(file="./Local/sbg.png")
    label = Label(ws_main,image=img)
    label.place(x=0,y=0)
except:
    pass
try:
    os.mkdir("./Local")
except:
    pass
frame = Frame(ws_main, padx=50, pady=50)
frame.pack(expand=True)

Label(frame, text="Welcome to Supermarket!",font=("Times", "24", "bold")).grid(row=0, columnspan=3, pady=10)

new = Button(frame, text="Create Account", padx=20, pady=10, relief=SOLID, font=("Times", "14", "bold"), command=pnew_acc)
new.grid(row=18, column=0,pady=10)

old = Button(frame, text="Login", padx=20, pady=10, relief=SOLID, font=("Times", "14", "bold"), command=blogin)
old.grid(row=18, column=1,pady=10)

ext = Button(frame, text="Exit", padx=20, pady=10, relief=SOLID, font=("Times", "14", "bold"), command=lambda:ws_main.destroy())
ext.grid(row=18, column=3,pady=10)
ws_main.mainloop()

