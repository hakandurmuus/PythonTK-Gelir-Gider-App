import mysql.connector
import datetime
import os
from dotenv import load_dotenv
from tkinter import messagebox

class DbManager:
    def database(self):
        load_dotenv()
        self.connection = mysql.connector.connect(
            host = os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        self.cursor = self.connection.cursor()

    def login(self,username,password):
        self.database()
        sql = "SELECT * FROM userinfo WHERE username = %s and password = %s"
        values = (username,password)
        self.cursor.execute(sql,values)
        user = self.cursor.fetchone()
        if user:
            messagebox.showinfo("BAŞARILI","Giriş Başarılı")
            self.connection.close()
            return True
        else:
            messagebox.showerror("HATA","Kullanıcı adı veya şifre hatalı!")
            self.connection.close()

    def register(self,username,password):
        self.database()
        sql1 = "SELECT username from userinfo WHERE username=%s"
        value = (username,)
        self.cursor.execute(sql1,value)
        results = self.cursor.fetchall()
        if len(results) == 0:
            date = datetime.date.today()
            sql2 = "INSERT INTO userinfo(username,password,registrationdate) VALUES (%s,%s,%s)"
            values = (username,password,date)
            self.cursor.execute(sql2,values)
            self.connection.commit()
            self.connection.close()
            messagebox.showinfo("BAŞARILI","Kayıt başarılı bir şekilde gerçekleşti")
            return True
        else:
            messagebox.showinfo("HATA","Kullanıcı adı kullanılıyor. Farklı bir kullanıcı adı deneyin.")
    
    def finduserid(self,username,password):
        self.database()
        sql = "SELECT * from userinfo WHERE username=%s and password=%s"
        values = (username,password)
        self.cursor.execute(sql,values)
        result = self.cursor.fetchone()
        self.connection.close()
        return result[0]
        
    # DB Getir Fonksiyonları
    def get_fixedexpenses(self,userid):
        self.database()
        sql = "SELECT * from fixedexpenses WHERE userid=%s"
        value = (userid,)
        self.cursor.execute(sql,value)
        results = self.cursor.fetchall()
        self.connection.close()
        return results
        
    def get_fixedincome(self,userid):
        self.database()
        sql = "SELECT * FROM fixedincome WHERE userid=%s"
        value = (userid,)
        self.cursor.execute(sql,value)
        results = self.cursor.fetchall()
        self.connection.close()
        return results    
    
    def get_income(self,userid):
        self.database()
        sql = "SELECT * FROM income WHERE userid=%s"
        value = (userid,)
        self.cursor.execute(sql,value)
        results = self.cursor.fetchall()
        self.connection.close()
        return results    
    
    def get_expenses(self,userid):
        self.database()
        sql = "SELECT * FROM expenses WHERE userid=%s"
        value = (userid,)
        self.cursor.execute(sql,value)
        results = self.cursor.fetchall()
        self.connection.close()
        return results    

    # DB Ekle Fonksiyonları
    def addItem_income(self,ad,tutar,tarih,tür,userid):
        tarih = self.format_date(tarih)
        self.database()
        id = self.cursor.lastrowid
        sql = "INSERT INTO income(id,geliradı,tutar,tarih,gelirtürü,userid) VALUES (%s,%s,%s,%s,%s,%s)"
        values = (id,ad,tutar,tarih,tür,userid)
        self.cursor.execute(sql,values)
        self.connection.commit()
        self.connection.close()

    def addItem_expenses(self,ad,tutar,tarih,tür,userid):
        tarih = self.format_date(tarih)
        self.database()
        id = self.cursor.lastrowid
        sql = "INSERT INTO expenses(id,gideradı,tutar,tarih,gidertürü,userid) VALUES (%s,%s,%s,%s,%s,%s)"
        values = (id,ad,tutar,tarih,tür,userid)
        self.cursor.execute(sql,values)
        self.connection.commit()
        self.connection.close()

    def addItem_fixedincome(self,ad,tutar,tarih,tür,userid):
        tarih = self.format_date(tarih)
        self.database()
        id = self.cursor.lastrowid
        sql = "INSERT INTO fixedincome(id,geliradı,tutar,tarih,gelirtürü,userid) VALUES (%s,%s,%s,%s,%s,%s)"
        values = (id,ad,tutar,tarih,tür,userid)
        self.cursor.execute(sql,values)
        self.connection.commit()
        self.connection.close()

    def addItem_fixedexpenses(self,ad,tutar,tarih,tür,userid):
        tarih = self.format_date(tarih)
        self.database()
        id = self.cursor.lastrowid
        sql = "INSERT INTO fixedexpenses(id,gideradı,tutar,tarih,gidertürü,userid) VALUES (%s,%s,%s,%s,%s,%s)"
        values = (id,ad,tutar,tarih,tür,userid)
        self.cursor.execute(sql,values)
        self.connection.commit()
        self.connection.close()

    # DB Güncelle Fonksiyonları
    def editItem_income(self,id,ad,tutar,tarih,tür,userid):
        tarih = self.format_date(tarih)
        self.database()
        sql = "UPDATE income SET geliradı=%s,tutar=%s,tarih=%s,gelirtürü=%s,userid=%s WHERE id=%s"
        values = (ad,tutar,tarih,tür,userid,id)
        self.cursor.execute(sql,values)
        self.connection.commit()
        self.connection.close()

    def editItem_expenses(self,id,ad,tutar,tarih,tür,userid):
        tarih = self.format_date(tarih)
        self.database()
        sql = "UPDATE expenses SET gideradı=%s,tutar=%s,tarih=%s,gidertürü=%s,userid=%s WHERE id=%s"
        values = (ad,tutar,tarih,tür,userid,id)
        self.cursor.execute(sql,values)
        self.connection.commit()
        self.connection.close()

    def editItem_fixedincome(self,id,ad,tutar,tarih,tür,userid):
        tarih = self.format_date(tarih)
        self.database()
        sql = "UPDATE fixedincome SET geliradı=%s,tutar=%s,tarih=%s,gelirtürü=%s,userid=%s WHERE id=%s"
        values = (ad,tutar,tarih,tür,userid,id)
        self.cursor.execute(sql,values)
        self.connection.commit()
        self.connection.close()

    def editItem_fixedexpenses(self,id,ad,tutar,tarih,tür,userid):
        tarih = self.format_date(tarih)
        self.database()
        sql = "UPDATE fixedexpenses SET gideradı=%s,tutar=%s,tarih=%s,gidertürü=%s,userid=%s WHERE id=%s"
        values = (ad,tutar,tarih,tür,userid,id)
        self.cursor.execute(sql,values)
        self.connection.commit()
        self.connection.close()


    # DB Sil Fonksiyonları
    def deleteItem_income(self,id):
        self.database()
        sql = "DELETE FROM income WHERE id=%s"
        value = (id,)
        self.cursor.execute(sql,value)
        self.connection.commit()
        self.connection.close()

    def deleteItem_expenses(self,id):
        self.database()
        sql = "DELETE FROM expenses WHERE id=%s"
        value = (id,)
        self.cursor.execute(sql,value)
        self.connection.commit()
        self.connection.close()

    def deleteItem_fixedincome(self,id):
        self.database()
        sql = "DELETE FROM fixedincome WHERE id=%s"
        value = (id,)
        self.cursor.execute(sql,value)
        self.connection.commit()
        self.connection.close()

    def deleteItem_fixedexpenses(self,id):
        self.database()
        sql = "DELETE FROM fixedexpenses WHERE id=%s"
        value = (id,)
        self.cursor.execute(sql,value)
        self.connection.commit()
        self.connection.close()

    def getReport_income(self,ilktarih,ikincitarih,userid):
        ilktarih = self.format_date(ilktarih)
        ikincitarih = self.format_date(ikincitarih)
        list = []
        self.database()
        sql1 = "SELECT tutar FROM income WHERE DATE(tarih) BETWEEN %s and %s and userid = %s"
        value1 = (ilktarih,ikincitarih,userid)
        self.cursor.execute(sql1,value1)
        for x in self.cursor.fetchall():
            list.append(x[0])

        sql2 = "SELECT tutar FROM fixedincome WHERE DATE(tarih) BETWEEN %s and %s and userid = %s"
        value2 = (ilktarih,ikincitarih,userid)
        self.cursor.execute(sql2,value2)
        for i in self.cursor.fetchall():
            list.append(i[0])
        self.connection.close()
        return sum(list)

    def getReport_expenses(self,ilktarih,ikincitarih,userid):
        ilktarih = self.format_date(ilktarih)
        ikincitarih = self.format_date(ikincitarih)
        list = []
        self.database()
        sql1 = "SELECT tutar FROM expenses WHERE DATE(tarih) BETWEEN %s and %s and userid = %s"
        value1 = (ilktarih,ikincitarih,userid)
        self.cursor.execute(sql1,value1)
        for x in self.cursor.fetchall():
            list.append(x[0])

        sql2 = "SELECT tutar FROM fixedexpenses WHERE DATE(tarih) BETWEEN %s and %s and userid = %s"
        value2 = (ilktarih,ikincitarih,userid)
        self.cursor.execute(sql2,value2)
        for i in self.cursor.fetchall():
            list.append(i[0])
        self.connection.close()
        return sum(list)

    def format_date(self,tarih):
        ayraçlar = ['.', '-', '/',',']
        for a in ayraçlar:
            if a in tarih:
                parça = tarih.split(a)
                break
        else:
            return None

        if len(parça) == 3:
            if len(parça[0]) == 4:
                yil = parça[0]
                ay = parça[1]
                gun = parça[2]
            else:
                gun = parça[0]
                ay = parça[1]
                yil = parça[2]
        else:
            return None

        try:
            return datetime.datetime(int(yil), int(ay), int(gun)).strftime("%Y-%m-%d")
        except ValueError:
            return None
