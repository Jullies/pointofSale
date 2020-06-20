#!/usr/bin/env python3.5.2
# -*- coding: utf-8 -*-
"""
Project started on Mon September 24 10:09:41 2018

@author: Jullies Onyango
"""
from tkinter import *
from tkinter import messagebox as sysdialog
import datetime
import sqlite3
import datetime
import time
import os
import mysql.connector
from tkinter import ttk
import ast
from datetime import timedelta
from reportlab.pdfgen import canvas as replayout
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import hashlib as julliesencrypt
import threading

styles = getSampleStyleSheet()
styleN = styles['Normal']
styleH = styles['Heading1']
styleHs = styles['Heading5']

current_system_path = os.getcwd()
c_path = str(current_system_path)
syspic = c_path + "\sysimages\syslogo.ico"

class license_check:
    def __init__(self, app):
        self.conn = app.conn
        self.dbcursor  = app.dbcursor    
        self.connsq = app.connsq
        try:
            dbquii=self.connsq.execute("SELECT sysuser, syspass FROM sysinfo WHERE sysuser =?", ("client",));
            connsq.commit()
            for row in dbquii:
                user = row[0]
                spass=row[1]   
            varch = spass[::-1]
        except:
            varch=""        
        newvarchar = varch[::-1]
        sfirstcharacter = newvarchar[::-2]
        fencrypt=sfirstcharacter[::-1]
        salt = "d7m27y1995"
        cryp_x = 0
        crypt_value = ""
        for row in fencrypt:
            crypt_value = crypt_value + row + salt[cryp_x]
            cryp_x = cryp_x + 1
        try:
            self.dbcursor.execute("SELECT inst_date FROM sysinfo")
            sysdbdate = self.dbcursor.fetchall()
            sddate = sysdbdate[0][0]
            cyp = sddate
        except Exception as err:
            print(err)
        cypt_date = cyp.strftime('%m%Y')
        fin_crpt_value=""
        cryp_y = 0
        for row in crypt_value:
            try:
                pck_date = cypt_date[cryp_y]
            except:
                pck_date=""
            fin_crpt_value = fin_crpt_value + row + pck_date
            cryp_y = cryp_y + 1
        
        nwcrypt_value = fin_crpt_value.encode('ascii')
        coll_cyp_v = julliesencrypt.sha256()
        coll_cyp_v.update(nwcrypt_value)
        show_coll_cyp_v = coll_cyp_v.hexdigest()
        cyp_user = show_coll_cyp_v[:16]
        cyp_for_user = cyp_user[::-1]
        cyp_auoth = ""
        st_a = 1
        dnt_length = len(cyp_for_user)
        for row in cyp_for_user:
            if dnt_length > st_a:
                if st_a%4 ==0:
                    cyp_auoth = cyp_auoth + row + "-"
                else:
                    cyp_auoth = cyp_auoth + row         
            else:
                cyp_auoth = cyp_auoth + row  
            st_a = st_a + 1
        permit_code = cyp_auoth

islic_active = "rub_still_due"

class run_db_setup():
    def __init__(self):        
        self.connsq = sqlite3.connect('dll/thumbs.db')
        try:
            dbquii=self.connsq.execute("SELECT sysuser, syspass FROM sysinfo WHERE sysuser =?", ("client",));
            self.connsq.commit()
            for row in dbquii:
                user = row[0]
                spass=row[1]   
            self.kalopass = spass[::-1]
        except:
            self.kalopass=""      
            
        print("Initiating a connection")
        self.conn = mysql.connector.connect(host="localhost", user="root", passwd=self.kalopass)
        self.dbcursor = self.conn.cursor()   
        print("Successful created a connection")
        self.permit_code =""
        self.updateTables()
        
    def updateTables(self):
        self.dbcursor.execute("CREATE SCHEMA IF NOT EXISTS juluepos")
        
        self.conn = mysql.connector.connect(host="localhost", user="root", passwd=self.kalopass, database="juluepos")
        self.dbcursor = self.conn.cursor()
        sysinfoTable =''' CREATE TABLE IF NOT EXISTS sysinfo(
                          sys_id INT AUTO_INCREMENT PRIMARY KEY,
                          sys_name VARCHAR(32),
                          sys_info VARCHAR(32),
                          inst_date DATE,
                          client VARCHAR(32),
                          outlet VARCHAR(32),
                          last_modified DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
                          )'''
        
        sysuserTable = '''CREATE TABLE IF NOT EXISTS sysuser(
                          id INT AUTO_INCREMENT PRIMARY KEY,
                          usern VARCHAR(32),
                          user_pass VARCHAR(255),
                          user_level VARCHAR(32),
                          reg_date DATE,
                          last_modified DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
                          )'''
        
        supplierTable = '''CREATE TABLE IF NOT EXISTS suppliers(
                          supplier_id INT AUTO_INCREMENT PRIMARY KEY,
                          suplier_name VARCHAR(32),
                          s_address VARCHAR(255),
                          s_telephone VARCHAR(255),
                          last_modified DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
                          )'''            
        
        productsTable = '''CREATE TABLE IF NOT EXISTS products_main(
                           item_id INT AUTO_INCREMENT PRIMARY KEY,
                           itemCode VARCHAR(255),
                           iname VARCHAR(255),
                           description VARCHAR(255),
                           barcode VARCHAR(255),
                           cost_price FLOAT,
                           selling_price FLOAT,
                           start_stock INT,
                           VAT FLOAT,
                           alert_quantity FLOAT,
                           supplier_id INT,
                           last_modified DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
                           )'''
        
        banking_table = '''CREATE TABLE IF NOT EXISTS banking(
                          banking_id INT AUTO_INCREMENT PRIMARY KEY,
                          td_date DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6),
                          slipno VARCHAR(255),
                          slipdate VARCHAR(255),
                          bamount FLOAT,
                          slip_user VARCHAR(255),
                          last_modified DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
                          )'''
        
        expenditureTable = '''CREATE TABLE  IF NOT EXISTS expenditure(
                              exp_id INT AUTO_INCREMENT PRIMARY KEY,
                              exdate DATE,
                              extime TIME,
                              expdecrip VARCHAR(1255),
                              expamount FLOAT,
                              exp_user VARCHAR(255),
                              last_modified DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
                              )'''
        
        new_supply = '''CREATE TABLE  IF NOT EXISTS new_supply(
                        id INT(255),
                        itemCode VARCHAR(255),
                        iquant FLOAT,
                        supply_date DATE,
                        nw_date  DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6),
                        c_user VARCHAR(255),
                        supplier_id INT,
                        last_modified DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
                        )'''
        
        productStock = '''CREATE TABLE IF NOT EXISTS product_stock(
                           item_id INT AUTO_INCREMENT PRIMARY KEY,
                           itemCode VARCHAR(255),
                           item_quant FLOAT,
                           last_modified DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
                           FOREIGN KEY (item_id) REFERENCES products_main(item_id)
                           )'''
        
        posReciepts = '''CREATE TABLE IF NOT EXISTS pos_reciepts(
                         receipt_id INT AUTO_INCREMENT PRIMARY KEY,
                         receipt_code VARCHAR(255),
                         nw_date  DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6),
                         cuser VARCHAR(32),
                         last_modified DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
                         )'''
        
        posRecieptsItems = '''CREATE TABLE IF NOT EXISTS reciept_items(
                         id INT AUTO_INCREMENT PRIMARY KEY,
                         receipt_id INT,
                         item_id INT,
                         item_quant FLOAT,
                         item_discount FLOAT,
                         vat FLOAT,
                         item_total FLOAT,
                         last_modified DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
                         FOREIGN KEY (item_id) REFERENCES products_main(item_id),
                         FOREIGN KEY (receipt_id) REFERENCES pos_reciepts(receipt_id)
                         )'''   
        
        listOfTables = [sysinfoTable, supplierTable, sysuserTable, productsTable, banking_table, banking_table, expenditureTable,
                        new_supply, productStock, posReciepts, posRecieptsItems]
        for t in listOfTables:
            table = t
            self.dbcursor.execute(table)
        self.conn.commit()

class start_login(Frame):
    def __init__(self, app):
        super().__init__(bg="wheat")
        self.conn = app.conn
        self.dbcursor  = app.dbcursor   
        self.current_user = app.current_user
        self.loginset = app.loginset
        self.app = app
        
        self.logtittle = Label(self, text="LOGIN HERE", bg="wheat", fg="blue", font="bold")
        self.logtittle.pack()   
        
        self.logcontent = Frame(self, bg="wheat")
        self.logcontent.pack()
        self.userlabel = Label(self.logcontent, text="Username:", bg="wheat")
        self.userlabel.grid(row=0, column=0)
        
        self.usernamegt =StringVar()
        self.userentry = Entry(self.logcontent, textvariable=self.usernamegt)
        self.userentry.grid(row=0, column=1)
        
        self.passlabel = Label(self.logcontent, text="Password:", bg="wheat")
        self.passlabel.grid(row=1, column=0)
        
        self.passwordgt =StringVar()
        self.passentry = Entry(self.logcontent, textvariable=self.passwordgt, show="*")
        self.passentry.grid(row=1, column=1)
        
        self.logbtframe = Frame(self, bg="wheat")
        self.logbtframe.pack()
        self.logbutt = Button(self.logbtframe, text="Sign In", bg="green", fg="white", command=self.userlogin)
        self.logbutt.pack()                
        
        self.pack()
    
    def userlogin(self):
        userpick = self.usernamegt.get()
        passcpick = self.passwordgt.get()
        self.current_user = userpick
        duser = "Admin"
        dpassword = "@dminJULU18"        
        if userpick == "" or passcpick == "":        
            sysdialog.showerror('Login Error', 'Username or Password cannot be left blank')
        else:
            if userpick == duser and passcpick == dpassword:
                self.current_user = "Admin_Developer"
                user_level_pass = "super_admin"
                nwdate = datetime.datetime.now()
                log_msg = str(nwdate) + " " + str(self.current_user) +" " + " Logged in Successfull" +"\n"
                log_write = open('activities/logs.text','a+')
                log_write.write('SUCCESS LOGIN \n')
                log_write.write(log_msg)
                log_write.close()
                sysdialog.showinfo('SUCCESS LOGIN', 'You are logged in successful')
                
                self.app.current_user = self.current_user
                self.app.sysmenyu = sysmenyu(self.app)
                self.destroy()
            else:
                try:
                    login_sql_verify = self.dbcursor.execute("SELECT usern, user_pass, user_level FROM sysuser WHERE usern = %s",(userpick,))
                    quii = self.dbcursor.fetchall() 
                    for row in quii:
                        log_user = row[0]
                        log_code = row[1]
                        user_level_pass = row[2]
                    if userpick == log_user and passcpick == log_code:
                        self.current_user = log_user
                        nwdate = datetime.datetime.now()
                        log_msg = str(nwdate) + " " + str(self.current_user) +" " + " Logged in Successfull" +"\n"
                        log_write = open('activities/logs.text','a+')
                        log_write.write('SUCCESS LOGIN \n')
                        log_write.write(log_msg)
                        log_write.close()
                        sysdialog.showinfo('SUCCESS LOGIN', 'You are logged in successful')                            
                        
                        self.app.current_user = self.current_user
                        self.app.sysmenyu = sysmenyu(self.app)
                        self.destroy()
                    else:
                        self.current_user = userpick
                        nwdate = datetime.datetime.now()
                        log_msg = str(nwdate) + " " + str(self.current_user) +" " + " Logged in Failed" +"\n"
                        log_write = open('activities/logs.text','a+')
                        log_write.write('ACCESS DENIED\n')
                        log_write.write(log_msg)
                        log_write.close()                                
                        sysdialog.showerror('Login Error', 'Username/Password is incorrect, contact your system administrator/Vendor!')                                   
                except Exception as err:
                    print(err)
                    self.current_user = userpick
                    nwdate = datetime.datetime.now()
                    log_msg = str(nwdate) + " " + str(self.current_user) +" " + " Logged in Failed" +"\n"
                    log_write = open('activities/logs.text','a+')
                    log_write.write('ACCESS DENIED\n')
                    log_write.write(log_msg)
                    log_write.close()                        
                    sysdialog.showerror('Login Error', 'Username/Password is incorrect, contact your system administrator or Vendor')
            

class reriept:
    def __init__(self, app):
        global widthcrcp
        global heightrcp
        
        self.rcp_change = app.rcp_change
        self.rcp_customer = app.rcp_customer    
        cart = app.cart
        self.current_user = app.current_user
        self.soft_info = "Sales Receipt"
        self.conn = app.conn
        self.dbcursor  = app.dbcursor  
        self.rcp_total=app.total
        
        widthcrcp=250
        heightrcp =200
        for row in cart:
            heightrcp = heightrcp + 10
        
        self.dbcursor.execute("SELECT max(receipt_id) FROM pos_reciepts")
        pos_reciep_id = (self.dbcursor.fetchall())[0][0]
            
        def create_doc(doc):
            global heightrcp         
            
            rcp_total = 0
            
            x =230
            y = heightrcp - 20
            rc_code = "Reciept No: " + str(pos_reciep_id)
            nw_dtime = " Date: " + str(time.ctime())
            doc.setFont("Helvetica", 12)
            doc.drawString(90, y, self.soft_info)
            doc.setFont("Helvetica", 9)
            y = y -30
            doc.drawString(10, y, rc_code)
            doc.drawString(110, y, nw_dtime)
            y = y -30
            doc.setFont("Helvetica", 8)
            doc.drawString(20, y, "CODE")
            doc.drawString(80, y, "PRODUCT")
            doc.drawString(150, y, "QUANTITY")
            doc.drawString(200, y, "SUBTOTAL")
            y = y -15
            for row in cart:
                rcp_icode = row
                rcp_icode = str(rcp_icode)
                rcp_iname = cart[row][0]
                rcp_iname = str(rcp_iname)
                rcp_quant = cart[row][1]
                rcp_quant = str(rcp_quant)
                rcp_sub = cart[row][2]
                rcp_total = rcp_total + rcp_sub
                rcp_sub = str(rcp_sub)
                
                doc.drawString(20, y, rcp_icode)
                doc.setFont("Helvetica", 7.5)
                doc.drawString(65, y, rcp_iname)
                doc.setFont("Helvetica", 8)
                doc.drawString(155, y, rcp_quant)
                doc.drawString(205, y, rcp_sub)
                y = y -10
            
            rcp_total = str(self.rcp_total)
            rcp_change = str(self.rcp_change)
            rcp_customer = str(self.rcp_customer)
            
            y = y -30
            doc.drawString(10, y, "Total: ")
            doc.drawString(32, y, rcp_total)
            doc.drawString(78, y, "You issued: ")
            doc.drawString(120, y, rcp_customer)
            doc.drawString(160, y, "Change: ")
            doc.drawString(190, y, rcp_change)
            y = y -25
            doc.drawString(70, y, "You were Served by: ")
            doc.drawString(150, y, self.current_user)
            y = y -15
            doc.drawString(65, y, "Thank You and Welcome Back: ")


        doc = replayout.Canvas("reciept.pdf", pagesize=(widthcrcp, heightrcp))
        create_doc(doc)
        doc.showPage()
        doc.save()
        os.startfile("reciept.pdf", "print")


class sysmenyu(Frame):
    def __init__(self, app):
        super().__init__(bg="wheat")
        self.conn = app.conn
        self.dbcursor  = app.dbcursor   
        self.loginset = app.loginset
        self.app = app  
        self.current_user = self.app.current_user
        self.app.app.title("Universal E- Point_of_Sale Software")
        
        self.pos_holder = Frame(self, bg="wheat")
        self.pos_holder.pack()

        self.pos_content = Frame(self.pos_holder, bg="wheat")
        self.pos_content.pack() 
        self.william_titlef = Frame(self.pos_content, bg="wheat")
        self.william_titlef.pack()
        self.postitle = Label(self.william_titlef, bg="wheat", fg="blue", font="bold", text ="POINT OF SALE")
        self.postitle.pack()
        
        self.william_content = Frame(self.pos_content, bg="wheat")
        self.william_content.pack()
        
        self.reciept_label = Label(self.william_content, text="      Reciept No: ", bg="wheat")
        self.reciept_label.grid(row=0, column=0)
        self.reciept_value = Label(self.william_content, bg="wheat", fg="green")
        self.reciept_value.grid(row=0, column=1)
        self.rcp()
        
        self.date_label = Label(self.william_content, text="     Date: ", bg="wheat")
        self.date_label.grid(row=0, column=2)
        self.date_nw= datetime.date.today()
        self.config_date = Label(self.william_content, text=self.date_nw, bg="wheat", fg="green")
        self.config_date.grid(row=0, column=3)
        
        self.time_label = Label(self.william_content, text="    Time: ", bg="wheat")
        self.time_label.grid(row=0, column=4)
        self.time_text = Label(self.william_content, bg="wheat")
        self.time_text.grid(row=0, column=5)
        self.tmer()
        
        self.saler_text = Label(self.william_content, text="    Saler: ", bg="wheat")
        self.saler_text.grid(row=0, column=6)
        self.saler_value = Label(self.william_content, text=self.current_user, bg="wheat", fg="green")
        self.saler_value.grid(row=0, column=7)
        
        self.space = Label(self.pos_content, text="", bg="wheat")
        self.space.pack()
        self.items_frame = Frame(self.pos_content, bg="wheat")
        self.items_frame.pack()
        self.space = Label(self.pos_content, text="", bg="wheat")
        self.space.pack()
        
        self.item_clabel = Label(self.items_frame, text=" Item Code: ", bg="wheat")
        self.item_clabel.grid(row=0, column=0)
        self.item_code = StringVar()
        self.item_c = Entry(self.items_frame, textvariable=self.item_code, fg="green")
        self.item_c.grid(row=0, column=1)
        
        item_nlabel = Label(self.items_frame, text=" Name: ", bg="wheat")
        item_nlabel.grid(row=0, column=2)
        
        self.item_name = StringVar()
        self.item_n = ttk.Combobox(self.items_frame, width=25, textvariable=self.item_name)
        self.dbcursor.execute("SELECT iname FROM products_main")
        self.pos_items_name= (self.dbcursor.fetchall())[0]
        self.item_n['values'] = self.pos_items_name
        self.item_n.grid(row=0, column=3)
        self.item_n.bind("<Key>", self.clickonpos)
        
        
        self.item_qlabel = Label(self.items_frame, text=" Quantity: ", bg="wheat")
        self.item_qlabel.grid(row=0, column=4)
        self.item_quantity = IntVar()
        self.item_q = Entry(self.items_frame, textvariable=self.item_quantity, fg="green")
        self.item_q.grid(row=0, column=5)
        
        self.buttonfme = Frame(self.pos_content, bg="wheat")
        self.buttonfme.pack()   
        self.posaddbt = Button(self.buttonfme, text = "Add +", bg="green", fg="white", command=self.posAddItem)
        self.posaddbt.grid(row=0, column=0)
        self.poscompletebt = Button(self.buttonfme, text = "Complete", bg="steelblue", fg="white", command=self.poscomplete)
        self.poscompletebt.grid(row=0, column=1)
        self.posclearbt = Button(self.buttonfme, text = "Delete -", bg="darkred", fg="white", command=self.clear_particular)
        self.posclearbt.grid(row=0, column=2)
        self.posresetbt = Button(self.buttonfme, text = "Reset", bg="red", fg="white", command=self.posreset)
        self.posresetbt.grid(row=0, column=3)
        
        self.space = Label(self.pos_content, text="", bg="wheat")
        self.space.pack()
        self.amtbtyframe = Frame(self.pos_content, bg="wheat")
        self.amtbtyframe.pack()
        
        amtbycuslaabel = Label(self.amtbtyframe, text="Amount given by customer: ", bg="wheat", fg="blue", font="bold")
        amtbycuslaabel.grid(row=0, column=0)
        
        self.amtbycust= IntVar()
        self.amtlabe = Entry(self.amtbtyframe, textvariable=self.amtbycust, fg="blue", relief=RAISED, font="bold")
        self.amtlabe.grid(row=0, column=1)
        
        self.space = Label(self.pos_content, text="", bg="wheat")
        self.space.pack()
        
        self.itemsfme = Frame(self.pos_holder, bg="wheat")
        self.itemsfme.pack()         
        
        self.pack()
        
        self.cart= {}
        self.total = 0
    
    def poscomplete(self):
        if self.total == 0:
            sysdialog.showerror('Error Report', 'Cart is empty!')
        else:
            amntissued = self.amtbycust.get()
            changet =int(amntissued) - int(self.total)
            if changet < 0:
                error_amount =0 - changet
                suct_error_data = 'Amount given by customer is less by: ' + str(error_amount) + "!"
                sysdialog.showerror('Change error', suct_error_data)
            else:            
                mtinfo = "Return amount : " + str(changet) + " to customer"
                sysdialog.showinfo('Return Change', mtinfo)
                self.rcp_change = changet
                self.rcp_customer = amntissued 
                self.save_cartrcp()
                reriept(self)
                self.posreset()
                self.rcp()
                self.poseditf()
                
        
    def clear_particular(self):
        code = self.item_code.get()
        iname = self.item_name.get()
        
        try:
            self.dbcursor.execute("SELECT id FROM products_main WHERE iname = '%s'"% (iname))
            queryid_sql = self.dbcursor.fetchall()
            for row in queryid_sql:
                itemid = row[0]
                itemid = int(itemid)
            code = itemid
            item_c.config(value=code)            
        except:
            pass            
        
        try:
            self.total = int(self.total) - int(self.cart[code][2])
            del self.cart[code]
            self.clear_poscontent()
            self.poseditf()
        except Exception as err:
            print(err)
            sysdialog.showerror('Error Report', 'Item of/with that code dont exist in shopping cart')                    
    
    def posreset(self):
        self.total = 0 
        self.cart = {}
        
        self.clear_poscontent() 
        self.poseditf()
        
    def clear_poscontent(self):
        for widget in self.itemsfme.winfo_children():
            widget.destroy()    
    
    def posAddItem(self):
        icode = self.item_code.get()
        iname = self.item_name.get()
        iquantity = self.item_quantity.get()
        
        try:
            self.dbcursor.execute("SELECT id FROM products_main WHERE iname = '%s'"%(iname))
            queryid_sql = self.dbcursor.fetchall()
            for row in queryid_sql:
                itemid = row[0]
                itemid = int(itemid)
            icode = itemid
            self.item_c.config(textvariable=icode, value=icode)            
        except Exception as err:
            print(err)
            pass
        
        if icode == "" or iquantity == "":
            sysdialog.showerror('Blank Inputs!', 'Check your data, error on blank input')         
            
        else:
            
            try:
                sql_query = "SELECT id, iname, selling_price FROM products_main WHERE id = %s"
                search_id = (icode,)
                self.dbcursor.execute(sql_query, search_id)
                name_query = self.dbcursor.fetchall()
                
                for row in name_query:
                    pr_id = row[0]
                    pr_name = row[1]   
                    pr_sellingp = row[2]
                
                iname = pr_name 
                cost = int(pr_sellingp)
                price = int(iquantity) * int(cost)        
                self.total = int(self.total) + int(price)  
                
                if iquantity == 0 or iquantity =="":
                    sysdialog.showerror('Error Report', 'Quantity cannot be zero!!!')
                    
                else:
                    try:
                        (list(self.cart.keys())).index(icode)
                        self.cart[icode][1] = self.cart[icode][1]+ iquantity
                        self.cart[icode][2] = self.cart[icode][2]+ price
                    except:
                        self.cart[icode] =[iname, iquantity, price];
                    self.poseditf() 
            except Exception as err:
                print(err)
                sysdialog.showerror('Error Report!', 'Product of that code or name dont exist in your database!')   
    
    def save_cartrcp(self):
        self.dbcursor.execute('INSERT INTO `pos_reciepts` (`cuser`) VALUES("%s")'%(self.current_user))
        cart = self.cart
        for row in cart:
            itcode = row
            iquan = cart[row][1]
            itotal = cart[row][2]
            self.dbcursor.execute("SELECT id, iquant FROM product_stock WHERE id = %s", (itcode,));
            verify_quanity_query = self.dbcursor.fetchall() 
            for row in verify_quanity_query:
                prd_quantity = row[1]
            updt_quantity = int(prd_quantity) - int(iquan)
            self.dbcursor.execute("UPDATE product_stock SET iquant=%s WHERE id=%s;", (updt_quantity, itcode));
            self.dbcursor.execute('''INSERT INTO `reciept_items`(`receipt_id`,`item_id`,`item_quant`,`item_total`)
                                      VALUES((SELECT max(receipt_id) FROM pos_reciepts), "%s","%s","%s")'''%(itcode, iquan, itotal))
        self.conn.commit()            

    def poseditf(self):
        self.total_Frame =  Frame(self.itemsfme, bg="wheat")
        self.total_Frame.grid(row=0, column=0)
        self.insert_frame = Frame(self.itemsfme, bg="wheat")
        self.insert_frame.grid(row=1, column=0)
        self.spacing_frame = Frame(self.itemsfme, bg="wheat")
        self.spacing_frame.grid(row=2, column=0)            
        
        if self.total > 0:
            try:                 
                self.products_label =Label(self.insert_frame, bg="wheat", text="Shopping Cart", fg="chocolate", font="bold")
                self.products_label.pack()
                self.bar_scroll = Scrollbar(self.insert_frame, bg="wheat")
                self.bar_scroll.pack(side=RIGHT, fill=Y)
                
                self.mylist = Listbox(self.insert_frame, width=80, relief=SUNKEN, bg="whitesmoke", fg="black",height=13, yscrollcommand = self.bar_scroll.set )
                
                x = 1
                cart = self.cart
                for row in cart:
                    inumbering = "|."+str(x) +".|"
                    icode = "    Item Code: " + str(row) + ","
                    iname = "  Name: " + str(cart[row][0])+ ","
                    iquant = "  Quant: " +str(cart[row][1])+ ","
                    isubtotatl = "  Subtotal => " +str(cart[row][2])
                    idata = inumbering + icode + iname + iquant + isubtotatl
                    self.mylist.insert(END, (idata))
                    x = x + 1
                    
                self.mylist.pack( side = LEFT, fill = BOTH )
                self.bar_scroll.config( command = self.mylist.yview)
                
                self.ltlabel = Label(self.total_Frame, text="Grand Total", bg="wheat", font="bold", fg="blue")
                self.ltlabel.grid(row=1, column=0)
                
                self.ltentr = Label(self.total_Frame, text=self.total, fg="green", bg="wheat", font="bold")
                self.ltentr.grid(row=1, column=1)  
                
                self.space = Label(self.total_Frame, text="", bg="wheat")
                self.space.grid(row=2, column=0)
                
                self.space = Label(self.spacing_frame, text="", bg="wheat")
                self.space.pack()                   
            
            except Exception as err:
                print(err)
                
        else:
            pass        
    
    def rcp(self):
        global pos_reciep_id
        try:
            recieptno_query = self.dbcursor.execute("SELECT MAX(receipt_id) FROM pos_reciepts")
            quii = self.dbcursor.fetchall()     
            for row in quii:
                maxid = row[0]
                suggest = int(maxid) + 1
                pos_reciep_id = suggest
                self.reciept_value.config(text=suggest)
        except:
            suggest = 1
            pos_reciep_id = suggest
            self.reciept_value.config(text=suggest)
    
    def tmer(self):
        def tmsetter():
            ctime = time.strftime("%H : %M : %S")
            self.time_text.config(text=ctime, fg="blue")
            self.time_text.after(1000, tmsetter)
        tmsetter()             
    
    def clickonpos(self, key):
        user_value = self.item_name.get()
        # print the key that was pressed
        data = key.char
        list_after_filter = []
        a = length_usr_value = len(user_value)
        if length_usr_value > 0:
            x = 0
            for row in self.pos_items_name:
                output = row[:a]
                outputlow = output.lower()
                outputupp = output.upper()
                if user_value == output or user_value == outputlow:
                    list_after_filter = list_after_filter + [self.pos_items_name[x]]
                x = x + 1
        else:
            list_after_filter = self.pos_items_name
        self.item_n.config(values=list_after_filter)        
        
class startMain:
    def __init__(self):
        connection = run_db_setup()
        self.conn = connection.conn
        self.dbcursor  = connection.dbcursor
        self.connsq = connection.connsq
        self.current_user = "Guest"
        self.loginset = False
        #license_check(self)
        
        self.app = Tk()
        self.app.title("Login Here")
        self.app.resizable(0, 0)
        
        self.loginFrame = start_login(self) 
        
        self.app.mainloop()

if __name__ == "__main__":
    startMain()