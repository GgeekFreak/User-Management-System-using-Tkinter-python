import MySQLdb
from tkinter import messagebox as mg
import sys
class DbManger:

    def __init__(self):
      self.error_exist = True
      while True:
        try:

                self.conn = MySQLdb.connect(host='127.0.0.1',  # thats where you put host name
                                    user='root',  # thats where you put sql user
                                    passwd='root',  # thats where you put sql password
                                    db='UserDB')  # thats where you put sql database name


                self.cur = self.conn.cursor()

                self.cur.execute("SELECT user_name FROM users_user ")
                break

        except Exception as e:
            self.error_exist = False
            mg.showerror('Fatal Error','Please Select Database and try again')
            self.error_exist = True
            if self.error_exist == True:
                quit()




if __name__ == "__main__":
    db = DbManger()



