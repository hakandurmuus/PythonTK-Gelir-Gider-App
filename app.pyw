from tkinter import *
import ttkbootstrap as tb
from dbmanager import DbManager
from tkinter import messagebox



class App:
    # Login penceresi
    def __init__(self):
        self.db = DbManager()
        self.loginwindow = tb.Window(themename="cosmo")
        self.loginwindow.geometry("700x480+700+300")
        self.loginwindow.title("Gelir-Gider App")
        self.loginwindow.resizable(0,0)
        
        self.main_frame = tb.Frame(self.loginwindow)
        self.main_frame.pack(fill=X)
        
        #İLK ALAN
        welcome_frm = tb.Frame(self.main_frame,padding=25)
        welcome_frm.pack(fill=X,pady=(15,0))

        welcome_lbl = tb.Label(welcome_frm, text="HOŞGELDİNİZ",bootstyle="danger",font=("Arial",25))
        welcome_lbl.pack()

        #İKİNCİ ALAN
        login_lblfrm = tb.Labelframe(self.main_frame,text="Giriş",bootstyle="info")
        login_lblfrm.pack(pady=30,padx=50,fill=X)

        self.username_label = tb.Label(login_lblfrm,text="Kullanıcı Adı")
        self.username_label.grid(row=0,column=0,sticky="w",padx=10)

        self.username_entry = tb.Entry(login_lblfrm,width=50)
        self.username_entry.grid(row=0,column=1,pady=5)
        
        self.password_label = tb.Label(login_lblfrm,text="Şifre")
        self.password_label.grid(row=1,column=0,sticky="w",padx=10)

        self.password_entry = tb.Entry(login_lblfrm,width=50,show="*")
        self.password_entry.grid(row=1,column=1,pady=5)

        btn_frame = tb.Frame(login_lblfrm)
        btn_frame.grid(row=2,column=1,sticky="w")

        self.login_btn = tb.Button(btn_frame,text="Giriş Yap",bootstyle="success",command=self.login)
        self.login_btn.grid(row=0,column=0,sticky="w",pady=5)

        self.register_btn = tb.Button(btn_frame,text="Kayıt Ol",bootstyle="primary",command=self.register)
        self.register_btn.grid(row=0,column=1,padx=10)


        self.loginwindow.mainloop()

    def clear_frame(self,frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def login(self):
        success = self.db.login(self.username_entry.get(),self.password_entry.get())
        if success:
            self.username = self.username_entry.get()
            self.password = self.password_entry.get()
            self.clear_frame(self.main_frame)
            self.open_main_window()             

    def register(self):
        if len(self.username_entry.get()) == 0 or len(self.password_entry.get()) == 0:
            messagebox.showerror("HATA","Kullanıcı adı ve şifre boş olamaz")
        elif len(self.username_entry.get()) < 5:
            messagebox.showerror("HATA","Kullanıcı adı en az 5 karakter olmalı")
        else:
            self.db.register(self.username_entry.get(),self.password_entry.get())
            self.username_entry.delete(0,END)
            self.password_entry.delete(0,END)
    
    def selectItem(self,e):
        selected_item = self.tvw.focus()
        item = self.tvw.item(selected_item)["values"]
        self.ad_entry.delete(0,END)
        self.tutar_entry.delete(0,END)
        self.tarih_entry.delete(0,END)
        self.ad_entry.insert(0,item[1])
        self.tutar_entry.insert(0,item[2])
        self.tarih_entry.insert(0,item[3])

    # ------------------ Ana Menü ---------------------  
    def open_main_window(self):
        self.new_frame = tb.Frame(self.main_frame,bootstyle="primary")
        self.new_frame.pack(fill=X,padx=(5,28))

        income_btn = tb.Button(self.new_frame,text="Gelirler",command=self.income)
        income_btn.pack(side=LEFT,padx=(30,10))

        expenses_btn = tb.Button(self.new_frame,text="Giderler",command=self.expenses)
        expenses_btn.pack(side=LEFT,padx=10)

        fixed_income_btn = tb.Button(self.new_frame,text="Sabit Gelirler",command=self.fixedincome)
        fixed_income_btn.pack(side=LEFT,padx=10)

        fixed_expenses_btn = tb.Button(self.new_frame,text="Sabit Giderler",command=self.fixedexpenses)
        fixed_expenses_btn.pack(side=LEFT,padx=10)

        report_btn = tb.Button(self.new_frame,text="Rapor",command=self.report)
        report_btn.pack(side=RIGHT,padx=5)

        self.table_frm = tb.Frame(self.loginwindow,bootstyle="light")
        self.table_frm.pack(fill=X)

        self.action_frm = tb.Frame(self.loginwindow,bootstyle="light")
        self.action_frm.pack(fill=X)

        self.table()
        
    #Aksiyon Alanı
    def find_userid(self):
        self.userid = self.db.finduserid(self.username,self.password)
        return self.userid
    
    def table(self):
        self.clear_frame(self.table_frm)
        self.clear_frame(self.action_frm)

        self.table_scroll = Scrollbar(self.table_frm,orient="vertical")
        self.table_scroll.pack(fill=Y,side=RIGHT)

        self.tvw = tb.Treeview(self.table_frm,show="headings",height=10,bootstyle='primary',yscrollcommand=self.table_scroll.set)
        self.tvw.pack(fill=X,padx=5,pady=5)

        self.tvw.bind("<ButtonRelease-1>",self.selectItem)

        self.table_scroll.config(command=self.tvw.yview)

        self.tvw["columns"] = ("id","ad","tutar","tarih","gelirtürü","userid")
        self.tvw["displaycolumns"] = ("ad","tutar","tarih")

        self.tvw.column("ad",width=50,minwidth=30)
        self.tvw.column("tutar",width=50,minwidth=30)
        self.tvw.column("tarih",width=50,minwidth=30)

        self.tvw.heading("ad",text="ad",anchor="w")
        self.tvw.heading("tutar",text="tutar",anchor="w")
        self.tvw.heading("tarih",text="tarih",anchor="w")

        self.btn_frm = tb.Frame(self.action_frm,bootstyle="ligth",width=200)
        self.btn_frm.grid(row=3,column=1,sticky="w")

    def income(self):
        self.table()
        self.tvw.delete(*self.tvw.get_children())
        self.clear_frame(self.btn_frm)

        for result in self.db.get_income(self.find_userid()):
            self.tvw.insert("",END,values=(result[0],result[1],result[2],result[3],result[4],result[5]))

        self.ad_lbl = tb.Label(self.action_frm,text="Ad",bootstyle="inverse-light")
        self.ad_lbl.grid(row=0,column=0,sticky="w",padx=5)
        self.ad_entry = tb.Entry(self.action_frm,width=75)
        self.ad_entry.grid(row=0,column=1,sticky="w",padx=10,pady=5)

        self.tutar_lbl = tb.Label(self.action_frm,text="Tutar",bootstyle="inverse-light")
        self.tutar_lbl.grid(row=1,column=0,sticky="w",padx=5)
        self.tutar_entry = tb.Entry(self.action_frm,width=75)
        self.tutar_entry.grid(row=1,column=1,sticky="w",padx=10,pady=5)

        self.tarih_lbl = tb.Label(self.action_frm,text="Tarih",bootstyle="inverse-light")
        self.tarih_lbl.grid(row=2,column=0,sticky="w",padx=5)
        self.tarih_entry = tb.Entry(self.action_frm,width=75)
        self.tarih_entry.grid(row=2,column=1,sticky="w",padx=10,pady=5)

        self.ekle_btn = tb.Button(self.btn_frm,text="Ekle",bootstyle="success",command=self.addItem_income)
        self.ekle_btn.grid(row=0,column=0,sticky="w",padx=(10,5),pady=5)

        self.güncelle_btn = tb.Button(self.btn_frm,text="Güncelle",bootstyle="success",command=self.editItem_income)
        self.güncelle_btn.grid(row=0,column=1,sticky="w",padx=5)

        self.sil_btn = tb.Button(self.btn_frm,text="Sil",bootstyle="success",command=self.deleteItem_income)
        self.sil_btn.grid(row=0,column=2,sticky="w",padx=5)

        self.clear_btn = tb.Button(self.btn_frm,text="Temizle",bootstyle="success",command=self.clear_entry)
        self.clear_btn.grid(row=0,column=3,sticky="w",padx=5)

        self.hesapla_btn = tb.Button(self.btn_frm,text="Hesapla",bootstyle="info",command=self.calculate_income)
        self.hesapla_btn.grid(row=0,column=4,sticky="e",padx=(100,30))

        self.hesapla_lbl = tb.Label(self.btn_frm,text="")
        self.hesapla_lbl.grid(row=0,column=5,sticky="e")

    def expenses(self):
        self.table()
        self.tvw.delete(*self.tvw.get_children())
        self.clear_frame(self.btn_frm)
    
        for result in self.db.get_expenses(self.find_userid()):
            self.tvw.insert("",END,values=(result[0],result[1],result[2],result[3],result[4],result[5]))

        self.ad_lbl = tb.Label(self.action_frm,text="Ad",bootstyle="inverse-light")
        self.ad_lbl.grid(row=0,column=0,sticky="w",padx=5)
        self.ad_entry = tb.Entry(self.action_frm,width=75)
        self.ad_entry.grid(row=0,column=1,sticky="w",padx=10,pady=5)

        self.tutar_lbl = tb.Label(self.action_frm,text="Tutar",bootstyle="inverse-light")
        self.tutar_lbl.grid(row=1,column=0,sticky="w",padx=5)
        self.tutar_entry = tb.Entry(self.action_frm,width=75)
        self.tutar_entry.grid(row=1,column=1,sticky="w",padx=10,pady=5)

        self.tarih_lbl = tb.Label(self.action_frm,text="Tarih",bootstyle="inverse-light")
        self.tarih_lbl.grid(row=2,column=0,sticky="w",padx=5)
        self.tarih_entry = tb.Entry(self.action_frm,width=75)
        self.tarih_entry.grid(row=2,column=1,sticky="w",padx=10,pady=5)

        self.ekle_btn = tb.Button(self.btn_frm,text="Ekle",bootstyle="success",command=self.addItem_expenses)
        self.ekle_btn.grid(row=0,column=0,sticky="w",padx=(10,5),pady=5)

        self.güncelle_btn = tb.Button(self.btn_frm,text="Güncelle",bootstyle="success",command=self.editItem_expenses)
        self.güncelle_btn.grid(row=0,column=1,sticky="w",padx=5)

        self.sil_btn = tb.Button(self.btn_frm,text="Sil",bootstyle="success",command=self.deleteItem_expenses)
        self.sil_btn.grid(row=0,column=2,sticky="w",padx=5)

        self.clear_btn = tb.Button(self.btn_frm,text="Temizle",bootstyle="success",command=self.clear_entry)
        self.clear_btn.grid(row=0,column=3,sticky="w",padx=5)

        self.hesapla_btn = tb.Button(self.btn_frm,text="Hesapla",bootstyle="info",command=self.calculate_expenses)
        self.hesapla_btn.grid(row=0,column=3,sticky="e",padx=(100,30))

        self.hesapla_lbl = tb.Label(self.btn_frm,text="")
        self.hesapla_lbl.grid(row=0,column=4,sticky="e")

    def fixedincome(self):
        self.table()
        self.tvw.delete(*self.tvw.get_children())
        self.clear_frame(self.btn_frm)
    
        for result in self.db.get_fixedincome(self.find_userid()):
            self.tvw.insert("",END,values=(result[0],result[1],result[2],result[3],result[4],result[5]))

        self.ad_lbl = tb.Label(self.action_frm,text="Ad",bootstyle="inverse-light")
        self.ad_lbl.grid(row=0,column=0,sticky="w",padx=5)
        self.ad_entry = tb.Entry(self.action_frm,width=75)
        self.ad_entry.grid(row=0,column=1,sticky="w",padx=10,pady=5)

        self.tutar_lbl = tb.Label(self.action_frm,text="Tutar",bootstyle="inverse-light")
        self.tutar_lbl.grid(row=1,column=0,sticky="w",padx=5)
        self.tutar_entry = tb.Entry(self.action_frm,width=75)
        self.tutar_entry.grid(row=1,column=1,sticky="w",padx=10,pady=5)

        self.tarih_lbl = tb.Label(self.action_frm,text="Tarih",bootstyle="inverse-light")
        self.tarih_lbl.grid(row=2,column=0,sticky="w",padx=5)
        self.tarih_entry = tb.Entry(self.action_frm,width=75)
        self.tarih_entry.grid(row=2,column=1,sticky="w",padx=10,pady=5)

        self.ekle_btn = tb.Button(self.btn_frm,text="Ekle",bootstyle="success",command=self.addItem_fixedincome)
        self.ekle_btn.grid(row=0,column=0,sticky="w",padx=(10,5),pady=5)

        self.güncelle_btn = tb.Button(self.btn_frm,text="Güncelle",bootstyle="success",command=self.editItem_fixedincome)
        self.güncelle_btn.grid(row=0,column=1,sticky="w",padx=5)

        self.sil_btn = tb.Button(self.btn_frm,text="Sil",bootstyle="success",command=self.deleteItem_fixedincome)
        self.sil_btn.grid(row=0,column=2,sticky="w",padx=5)

        self.clear_btn = tb.Button(self.btn_frm,text="Temizle",bootstyle="success",command=self.clear_entry)
        self.clear_btn.grid(row=0,column=3,sticky="w",padx=5)

        self.hesapla_btn = tb.Button(self.btn_frm,text="Hesapla",bootstyle="info",command=self.calculate_fixedincome)
        self.hesapla_btn.grid(row=0,column=3,sticky="e",padx=(100,30))

        self.hesapla_lbl = tb.Label(self.btn_frm,text="")
        self.hesapla_lbl.grid(row=0,column=4,sticky="e")

    def fixedexpenses(self):
        self.table()
        self.tvw.delete(*self.tvw.get_children())
        self.clear_frame(self.btn_frm)

        for result in self.db.get_fixedexpenses(self.find_userid()):
            self.tvw.insert("",END,values=(result[0],result[1],result[2],result[3],result[4],result[5]))

        self.ad_lbl = tb.Label(self.action_frm,text="Ad",bootstyle="inverse-light")
        self.ad_lbl.grid(row=0,column=0,sticky="w",padx=5)
        self.ad_entry = tb.Entry(self.action_frm,width=75)
        self.ad_entry.grid(row=0,column=1,sticky="w",padx=10,pady=5)

        self.tutar_lbl = tb.Label(self.action_frm,text="Tutar",bootstyle="inverse-light")
        self.tutar_lbl.grid(row=1,column=0,sticky="w",padx=5)
        self.tutar_entry = tb.Entry(self.action_frm,width=75)
        self.tutar_entry.grid(row=1,column=1,sticky="w",padx=10,pady=5)

        self.tarih_lbl = tb.Label(self.action_frm,text="Tarih",bootstyle="inverse-light")
        self.tarih_lbl.grid(row=2,column=0,sticky="w",padx=5)
        self.tarih_entry = tb.Entry(self.action_frm,width=75)
        self.tarih_entry.grid(row=2,column=1,sticky="w",padx=10,pady=5)

        self.ekle_btn = tb.Button(self.btn_frm,text="Ekle",bootstyle="success",command=self.addItem_fixedexpenses)
        self.ekle_btn.grid(row=0,column=0,sticky="w",padx=(10,5),pady=5)

        self.güncelle_btn = tb.Button(self.btn_frm,text="Güncelle",bootstyle="success",command=self.editItem_fixedexpenses)
        self.güncelle_btn.grid(row=0,column=1,sticky="w",padx=5)

        self.sil_btn = tb.Button(self.btn_frm,text="Sil",bootstyle="success",command=self.deleteItem_fixedexpenses)
        self.sil_btn.grid(row=0,column=2,sticky="w",padx=5)

        self.clear_btn = tb.Button(self.btn_frm,text="Temizle",bootstyle="success",command=self.clear_entry)
        self.clear_btn.grid(row=0,column=3,sticky="w",padx=5)

        self.hesapla_btn = tb.Button(self.btn_frm,text="Hesapla",bootstyle="info",command=self.calculate_fixedexpenses)
        self.hesapla_btn.grid(row=0,column=3,sticky="e",padx=(100,30))

        self.hesapla_lbl = tb.Label(self.btn_frm,text="")
        self.hesapla_lbl.grid(row=0,column=4,sticky="w")

    def report(self):
        self.clear_frame(self.table_frm)
        self.clear_frame(self.action_frm)

        tarih_frm = tb.Frame(self.table_frm)
        tarih_frm.pack(fill=X)

        self.rapor_frm = tb.Frame(self.table_frm,bootstyle="light")
        self.rapor_frm.pack(fill=X)

        yazi_lbl = tb.Label(tarih_frm,text="Lütfen raporlamak istediğiniz tarih aralığını giriniz")
        yazi_lbl.grid(row=0,column=1,sticky="n",padx=80,pady=(5,50))
        ilk_tarih_lbl = tb.Label(tarih_frm,text="İlk Tarih")
        ilk_tarih_lbl.grid(row=1,column=0,sticky="w",padx=10)
        self.ilk_tarih_entry = tb.Entry(tarih_frm)
        self.ilk_tarih_entry.grid(row=1,column=1,sticky="w",pady=5)

        ikinci_tarih_lbl = tb.Label(tarih_frm,text="İkinci Tarih")
        ikinci_tarih_lbl.grid(row=2,column=0,sticky="w",padx=10)
        self.ikinci_tarih_entry = tb.Entry(tarih_frm)
        self.ikinci_tarih_entry.grid(row=2,column=1,sticky="w",pady=5)

        getir_btn = tb.Button(tarih_frm,text="Raporla",command=self.getReport)
        getir_btn.grid(row=3,column=1,sticky="w",pady=5)

    def clear_entry(self):
        self.ad_entry.delete(0,END)
        self.tutar_entry.delete(0,END)
        self.tarih_entry.delete(0,END)

    # Ekleme Fonksiyonları
    def addItem_income(self):
        id = " "
        ad = self.ad_entry.get()
        tutar = self.tutar_entry.get()
        tarih = self.tarih_entry.get()
        tür = "d"
        userid = self.db.finduserid(self.username,self.password)

        self.tvw.insert("",END,values=(id,ad,tutar,tarih,tür,userid))
        self.db.addItem_income(ad,tutar,tarih,tür,userid)

        self.clear_entry()
    
    def addItem_expenses(self):
        id = " "
        ad = self.ad_entry.get()
        tutar = self.tutar_entry.get()
        tarih = self.tarih_entry.get()
        tür = "d"
        userid = self.db.finduserid(self.username,self.password)

        self.tvw.insert("",END,values=(id,ad,tutar,tarih,tür,userid))
        self.db.addItem_expenses(ad,tutar,tarih,tür,userid)

        self.clear_entry()

    def addItem_fixedincome(self):
        id = " "
        ad = self.ad_entry.get()
        tutar = self.tutar_entry.get()
        tarih = self.tarih_entry.get()
        tür = "s"
        userid = self.db.finduserid(self.username,self.password)

        self.tvw.insert("",END,values=(id,ad,tutar,tarih,tür,userid))
        self.db.addItem_fixedincome(ad,tutar,tarih,tür,userid)

        self.clear_entry()

    def addItem_fixedexpenses(self):
        id = " "
        ad = self.ad_entry.get()
        tutar = self.tutar_entry.get()
        tarih = self.tarih_entry.get()
        tür = "s"
        userid = self.db.finduserid(self.username,self.password)

        self.tvw.insert("",END,values=(id,ad,tutar,tarih,tür,userid))
        self.db.addItem_fixedexpenses(ad,tutar,tarih,tür,userid)

        self.clear_entry()

        
    # Güncelle Fonksiyonları
    def editItem_income(self):
        selected_item = self.tvw.focus()
        id = self.tvw.item(selected_item)["values"][0]
        tür = self.tvw.item(selected_item)["values"][4]
        userid = self.tvw.item(selected_item)["values"][5]
        ad = self.ad_entry.get()
        tutar = self.tutar_entry.get()
        tarih = self.tarih_entry.get()

        self.tvw.item(selected_item,text="",values=(id,ad,tutar,tarih,tür,userid))
        self.db.editItem_income(id,ad,tutar,tarih,tür,userid)

        self.clear_entry()

    def editItem_expenses(self):
        selected_item = self.tvw.focus()
        id = self.tvw.item(selected_item)["values"][0]
        tür = self.tvw.item(selected_item)["values"][4]
        userid = self.tvw.item(selected_item)["values"][5]
        ad = self.ad_entry.get()
        tutar = self.tutar_entry.get()
        tarih = self.tarih_entry.get()

        self.tvw.item(selected_item,text="",values=(id,ad,tutar,tarih,tür,userid))
        self.db.editItem_expenses(id,ad,tutar,tarih,tür,userid)

        self.clear_entry()

    def editItem_fixedincome(self):
        selected_item = self.tvw.focus()
        id = self.tvw.item(selected_item)["values"][0]
        tür = self.tvw.item(selected_item)["values"][4]
        userid = self.tvw.item(selected_item)["values"][5]
        ad = self.ad_entry.get()
        tutar = self.tutar_entry.get()
        tarih = self.tarih_entry.get()

        self.tvw.item(selected_item,text="",values=(id,ad,tutar,tarih,tür,userid))
        self.db.editItem_fixedincome(id,ad,tutar,tarih,tür,userid)

        self.clear_entry()

    def editItem_fixedexpenses(self):
        selected_item = self.tvw.focus()
        id = self.tvw.item(selected_item)["values"][0]
        tür = self.tvw.item(selected_item)["values"][4]
        userid = self.tvw.item(selected_item)["values"][5]
        ad = self.ad_entry.get()
        tutar = self.tutar_entry.get()
        tarih = self.tarih_entry.get()

        self.tvw.item(selected_item,text="",values=(id,ad,tutar,tarih,tür,userid))
        self.db.editItem_fixedexpenses(id,ad,tutar,tarih,tür,userid)

        self.clear_entry()


    # Sil Fonksiyonları
    def deleteItem_income(self):
        selected_item = self.tvw.focus()
        delete_id = self.tvw.item(selected_item)["values"][0]

        self.tvw.delete(selected_item)
        self.db.deleteItem_income(delete_id)

        self.clear_entry()

    def deleteItem_expenses(self):
        selected_item = self.tvw.focus()
        delete_id = self.tvw.item(selected_item)["values"][0]

        self.tvw.delete(selected_item)
        self.db.deleteItem_expenses(delete_id)

        self.clear_entry()

    def deleteItem_fixedincome(self):
        selected_item = self.tvw.focus()
        delete_id = self.tvw.item(selected_item)["values"][0]

        self.tvw.delete(selected_item)
        self.db.deleteItem_fixedincome(delete_id)

        self.clear_entry()

    def deleteItem_fixedexpenses(self):
        selected_item = self.tvw.focus()
        delete_id = self.tvw.item(selected_item)["values"][0]

        self.tvw.delete(selected_item)
        self.db.deleteItem_fixedexpenses(delete_id)

        self.clear_entry()

    
    # Hesapla Fonksiyonları
    def calculate_income(self):
        list = self.db.get_income(self.db.finduserid(self.username,self.password))
        tutar_list = []
        for item in list:
            tutar_list.append(item[2])
        self.hesapla_lbl.config(text=f"{sum(tutar_list)} TL")
    
    def calculate_expenses(self):
        list = self.db.get_expenses(self.db.finduserid(self.username,self.password))
        tutar_list = []
        for item in list:
            tutar_list.append(item[2])
        self.hesapla_lbl.config(text=f"{sum(tutar_list)} TL")
    
    def calculate_fixedincome(self):
        list = self.db.get_fixedincome(self.db.finduserid(self.username,self.password))
        tutar_list = []
        for item in list:
            tutar_list.append(item[2])
        self.hesapla_lbl.config(text=f"{sum(tutar_list)} TL")
    
    def calculate_fixedexpenses(self):
        list = self.db.get_fixedexpenses(self.db.finduserid(self.username,self.password))
        tutar_list = []
        for item in list:
            tutar_list.append(item[2])
        self.hesapla_lbl.config(text=f"{sum(tutar_list)} TL")

    # Rapor Bölümü
    def getReport(self):
        self.toplam_gelir = self.db.getReport_income(self.ilk_tarih_entry.get(),self.ikinci_tarih_entry.get(),self.db.finduserid(self.username,self.password))
        self.toplam_gider = self.db.getReport_expenses(self.ilk_tarih_entry.get(),self.ikinci_tarih_entry.get(),self.db.finduserid(self.username,self.password))
        self.bilanco = (self.toplam_gelir - self.toplam_gider)

        self.clear_frame(self.rapor_frm)

        self.toplam_gelir_lbl = tb.Label(self.rapor_frm,text=f"Toplam Gelir: {self.toplam_gelir}")
        self.toplam_gelir_lbl.grid(row=0,column=0,sticky="w",padx=5,pady=(50,5))

        self.toplam_gider_lbl = tb.Label(self.rapor_frm,text=f"Toplam Gider: {self.toplam_gider}")
        self.toplam_gider_lbl.grid(row=1,column=0,sticky="w",padx=5)

        self.toplam_bilanco_lbl = tb.Label(self.rapor_frm,text=f"Toplam Gelir-Gider: {self.bilanco}")
        self.toplam_bilanco_lbl.grid(row=2,column=0,sticky="w",padx=5,pady=30)


    



app = App()