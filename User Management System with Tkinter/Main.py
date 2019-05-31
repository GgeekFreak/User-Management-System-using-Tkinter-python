import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as mg
import os
from ManageDB import DbManger
import gc
from foowidget import EditableTreeview
from PIL import Image , ImageTk
state = 0

#make stacked widget here :)
class myApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.DbManger = DbManger()
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1 , minsize = 600)
        container.grid_columnconfigure(0, weight=1 , minsize = 800)
        self.mainFoo = container
        self.frames = {}
        for F in (StartPage, PageOne,PageTwo, PageThree,PageFour):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")


        self.show_frame("StartPage")

    def hello_world(self):
        self.show_frame("StartPage")


        self.frames['PageOne'] = None
        gc.collect()
        self.frames['PageOne'] = PageOne(self.mainFoo, self)
        #self.show_frame("PageOne")
        self.frames['PageOne'].grid(row=0, column=0, sticky="nsew")

        self.frames['PageOne'].menubar.entryconfig(1, state=NORMAL)

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.DbManger = DbManger()
        title = tk.Label(self, text="Adminstrator Login",font=("Helvetica", 16))
        title.grid(row = 0 , column = 0 , sticky = E)
        title.place(relx=0.5,rely=0.1,anchor=CENTER)
        name1 =  tk.Label(self, text="User Name",font=("Helvetica", 10))
        password = tk.Label(self, text="Password",font=("Helvetica", 10))
        name1.grid(row = 0 , column = 0 , sticky = W)
        name1.place(relx=0.1,rely=0.28)
        password.grid(row = 1 , column = 0, sticky = W)
        password.place(relx=0.1 , rely=0.38)

        self.e1 = tk.Entry(self,width=40)
        self.e2 = tk.Entry(self, show='*',width = 40)

        self.e1.grid(row = 0 , column = 1 , padx = 10 , pady = 10)
        self.e2.grid(row = 1 , column = 1 , padx = 10 , pady = 10)

        button1 = tk.Button(self,width=20, text="Login",font=("Helvetica", 12),
                            command=lambda:self.login_clicked(controller))
        button1.grid(columnspan = 2 , sticky = W)
        button2 = tk.Button(self,width=20, text="Add User",font=("Helvetica", 12),
                            command= lambda : controller.show_frame("PageTwo"))
        button2.grid(columnspan=2 , sticky=W)
        button1.config(bd=2)
        button2.config(bd=2)
        self.e1.place(relx=0.5, rely=0.3, anchor=CENTER)
        self.e2.place(relx = 0.5 , rely = 0.4 , anchor=CENTER)
        self.e1.config(bd= 5)
        self.e2.config(bd= 5)
        button1.place(relx = 0.5 , rely = 0.55 , anchor=CENTER)
        button2.place(relx=0.5, rely=0.65, anchor=CENTER)

    def login_clicked(self , controller):
        username = self.e1.get()
        pw = self.e2.get()
        query = '''SELECT user_username , user_password FROM users_user WHERE user_username LIKE "{}" 
                  AND user_password LIKE "{}"'''.format(username,pw)

        self.DbManger.cur.execute(query)
        self.DbManger.conn.commit()

        if(self.DbManger.cur.execute(query) and len(username) > 0):

            controller.show_frame("PageOne")

            obj = PageOne(self,controller)
            obj.menubar.entryconfig(1, state=NORMAL)

        else:
            mg.showinfo("ERROR","Invalid username or password")

# add , edit and listing page
class PageOne(tk.Frame):
    foo = []

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.DbManger = DbManger()
        self.controller = controller
        self.menubar = tk.Menu(self)
        self.filemenu = Menu(self.menubar, tearoff=0)

        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Add User",
                                  command=lambda: self.btncreate_clicked(controller))
        self.filemenu.add_command(label="Edit User",
                             command= lambda :controller.show_frame("PageFour"))
        self.filemenu.add_command(label="Delete User",
                             command=lambda : self.deleteItem(controller))
        self.filemenu.add_command(label="User Listing",
                                  command=lambda :controller.show_frame("PageOne"))
        self.filemenu.add_command(label="Change Password",
                                  command=lambda: controller.show_frame("PageThree"))
        self.filemenu.add_command(label="Logout",
                             command=lambda: self.logout_clicked(controller))
        controller.config(bd=5,menu=self.menubar)
        self.menubar.entryconfig(1, state=DISABLED)


        self.tv = EditableTreeview(self)
        self.tv['columns'] = ('Sr.No.','User ID','User Level','Name','Email','Mobile','DateOfBirth')
        self.tv.heading("#0", text='Sr.No.', anchor='w')
        self.tv.column("Sr.No.", anchor="center",width=65)
        self.tv.heading("#1", text='User ID', anchor='w')
        self.tv.column("User ID", anchor="center", width=65)
        self.tv.heading('#2',text='Name',anchor='w')
        self.tv.column('User Level',anchor='center', width=65)
        self.tv.heading('#3', text='User Level', anchor='w')
        self.tv.column('Name', anchor='center', width=65)
        self.tv.heading('#4', text='Email',anchor='w')
        self.tv.column('Email', anchor='center',width=65)
        self.tv.heading('#5', text='Mobile',anchor='w')
        self.tv.column('Mobile', anchor='center', width=65)
        self.tv.heading('#6', text='DateOfBirth',anchor='w')
        self.tv.column('DateOfBirth', anchor='center', width=65)
        self.grid_rowconfigure(0,weight = 1)
        self.tv.grid(row = 0 , sticky='ns')
        self.tv.bind('<ButtonRelease-1>',self.selectItem)
        self.LoadTable()
        self.curItem = None
        self.state = 0


    def __updateWnds(self, event=None):

        if not self._curfocus:
            return
        item = self._curfocus
        cols = self.__get_display_columns()
        for col in cols:
            if col in self._inplace_widgets:
                wnd = self._inplace_widgets[col]
                bbox = ''
                if self.exists(item):
                    bbox = self.bbox(item, column=col)
                if bbox == '':
                    wnd.place_forget()
                elif col in self._inplace_widgets_show:
                    wnd.place(x=bbox[0], y=bbox[1],
                              width=bbox[2], height=bbox[3])


    def btncreate_clicked(self,controller):
        controller.show_frame("PageTwo")

    def selectItem(self,a):

        self.curItem = self.tv.selection()[0]
        x = self.tv.item(self.curItem).copy()
        PageOne.foo.append(x)

        self.userid_item = self.tv.item(self.curItem)['values'][0]
        id = self.userid_item

        query = '''SELECT user_image FROM users_user WHERE user_id LIKE ('{}')'''.format(id)
        self.DbManger.cur.execute(query)
        self.DbManger.conn.commit()
        self.savedpic = [i[0] for i in self.DbManger.cur.fetchall()]
        self.image = Image.open(",".join(self.savedpic))


        self.image = self.image.resize((128,128),Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.label = Label(self, image=self.photo, anchor='nw')
        self.label.place(relx=0.92, rely=0.113, anchor=CENTER)
        self.label.config(bd=7)

    def deleteItem(self,controller):
        self.state = 1

        selected_items = PageOne.foo[-1]
        id = selected_items['values'][0]
        obj = PageOne(self,controller)
        query = '''DELETE FROM users_user WHERE user_id LIKE ('{}')'''.format(id)
        if(self.DbManger.cur.execute(query)):
            self.DbManger.conn.commit()



        self.controller.hello_world()


    def logout_clicked(self,controller):

        obj = PageOne(self, controller)
        controller.show_frame("StartPage")
        obj.menubar.entryconfig(1, state=DISABLED)

    def LoadTable(self):
        self.DbManger.cur.execute("""SELECT * FROM users_user""")
        counter = 0  # Counter representing the ID of your code.

        self.DbManger.conn.commit()

        counter__ = 0
        self.tv.insert('', 'end',iid='foo')
        for row in self.DbManger.cur:

            self.tv.insert('', 'end', iid = "ff"+str(counter__), text=str(counter), values=(row[0],row[4],row[1],row[5],row[6],row[8]))
            counter__ +=1
            counter += 1  # increment the ID

#adding new user page
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.DbManger = DbManger()
        self.controller = controller

        self.name_field = tk.Entry(self,width= 40)
        self.name_field.place(relx=0.26,rely=0.17,anchor=CENTER)
        self.name_label = Label(self,text = 'First name',font=("Helvetica", 11))
        self.name_label.place(relx=0.11,rely=0.11,anchor=CENTER)
        self.name_field.config(bd=5)

        self.lname_field = tk.Entry(self,width=40)
        self.lname_field.place(relx=0.26,rely=0.29,anchor=CENTER)
        self.lname_label = Label(self, text='Username',font=("Helvetica", 11))
        self.lname_label.place(relx=0.11, rely=0.23, anchor=CENTER)
        self.lname_field.config(bd=5)

        self.pass_field = tk.Entry(self, show='*', width=40)
        self.pass_field.place(relx=0.26, rely=0.41, anchor=CENTER)
        self.pass_label = Label(self, text='Password',font=("Helvetica", 11))
        self.pass_label.place(relx=0.11, rely=0.35, anchor=CENTER)
        self.pass_field.config(bd=5)

        self.mobile_field = tk.Entry(self ,width=40)
        self.mobile_field.place(relx=0.70, rely=0.07, anchor=CENTER)
        self.mobile_label = Label(self, text='Mobile',font=("Helvetica", 11))
        self.mobile_label.place(relx=0.54, rely=0.03, anchor=CENTER)
        self.mobile_field.config(bd=5)

        self.dob_field = tk.Entry(self, width=40)
        self.dob_field.insert(0, 'dd/mm/yyyy')
        self.dob_field.place(relx=0.70, rely=0.17, anchor=CENTER)
        self.dob_label = Label(self, text='Date OF Birth', font=("Helvetica", 11))
        self.dob_label.place(relx=0.57, rely=0.11, anchor=CENTER)
        self.dob_field.config(bd=5)

        self.email_field = tk.Entry(self , width=40)
        self.email_field.place(relx=0.70 , rely = 0.29 , anchor=CENTER)
        self.email_label = Label(self,text = 'Email Address', font=("Helvetica", 11))
        self.email_label.place(relx =0.57, rely=0.23,anchor=CENTER)
        self.email_field.config(bd=5)

        self.address1_field = tk.Entry(self, width=40)
        self.address1_field.place(relx=0.70, rely=0.41, anchor=CENTER)
        self.address1_label = Label(self, text='User Address1', font=("Helvetica", 11))
        self.address1_label.place(relx=0.57, rely=0.35, anchor=CENTER)
        self.address1_field.config(bd=5)

        self.address2_field = tk.Entry(self, width=40)
        self.address2_field.place(relx=0.70, rely=0.51, anchor=CENTER)
        self.address2_label = Label(self, text='User Address2 * Optional', font=("Helvetica", 11))
        self.address2_label.place(relx=0.61, rely=0.45, anchor=CENTER)
        self.address2_field.config(bd=5)

        query = '''SELECT country_name FROM country;'''

        self.DbManger.cur.execute(query)
        self.DbManger.conn.commit()
        country_data = self.DbManger.cur.fetchall()
        self.country_var = StringVar(self)
        self.country_var.set("choose country")
        self.country_field = OptionMenu(self,self.country_var,*country_data)
        self.country_field.place(relx=0.26, rely=0.58, anchor=CENTER)
        self.country_field.config(bd=5,width=25,font=("Helvetica", 11))
        query1 = '''SELECT city_name FROM city;'''
        self.DbManger.cur.execute(query1)
        self.DbManger.conn.commit()
        city_data =self.DbManger.cur.fetchall()
        self.city_var = StringVar(self)
        self.city_var.set("choose city")
        self.city_field = OptionMenu(self, self.city_var,*city_data)
        self.city_field.place(relx=0.26, rely=0.70, anchor=CENTER)
        self.city_field.config(bd=5, width=25,font=("Helvetica", 11))

        query2 = '''SELECT state_name FROM state;'''
        self.DbManger.cur.execute(query2)
        self.DbManger.conn.commit()
        state_data = self.DbManger.cur.fetchall()

        self.state_var = StringVar(self)
        self.state_var.set("choose state")
        self.state_field = OptionMenu(self, self.state_var,*state_data)
        self.state_field.place(relx=0.70, rely=0.58, anchor=CENTER)
        self.state_field.config(bd=5, width=25, font=("Helvetica", 11))

        query3 = '''SELECT level_title FROM level;'''
        self.DbManger.cur.execute(query3)
        self.DbManger.conn.commit()
        level_data = self.DbManger.cur.fetchall()

        self.lvl_var = StringVar(self)
        self.lvl_var.set("choose Level")
        self.lvl_field = OptionMenu(self, self.lvl_var,*level_data)
        self.lvl_field.place(relx=0.70, rely=0.70, anchor=CENTER)
        self.lvl_field.config(bd=5, width=25, font=("Helvetica", 11))

        self.var_male = IntVar(self)
        self.gc_label = Label(self,text = 'Gender', font=("Helvetica", 11))
        self.gc_label.place(relx=0.11,rely=0.81 , anchor=CENTER)
        self.gc = Checkbutton(self, text = "Male",variable = self.var_male)
        self.gc.place(relx = 0.26 , rely = 0.81, anchor=CENTER)
        self.gc.config(bd=5)
        self.var_female = IntVar(self)
        self.gc1 = Checkbutton(self, text="Femele",variable = self.var_female)
        self.gc1.place(relx=0.36, rely=0.81, anchor=CENTER)
        self.gc1.config(bd=5)

        self.lbrowse_btn = Label(self, text='Upload Picture', font=("Helvetica", 11))
        self.lbrowse_btn.place(relx=0.15,rely=0.91 , anchor=CENTER)

        self.browse_btn = Button(self, text="Browse", command=lambda: self.browse_image(controller))
        self.browse_btn.place(relx=0.32,rely=0.91,anchor=CENTER)
        self.submitbtn = Button(self,text="Submit" , command=lambda :self.submit_clicked(controller))
        self.submitbtn.place(relx = 0.5,rely= 0.97,anchor=CENTER)
        self.submitbtn.config(bd=2,width=70)
        self.state = 0
        self.quit()
    def browse_image(self , controller):

        FILEOPENOPTIONS = dict(defaultextension='.png',
                               filetypes=[('All files', '*.*'), ('PNG file', '*.png'), ('JPG file', '*.jpg')])

        self.file = filedialog.askopenfilename(title='Choose a Picture', **FILEOPENOPTIONS)
        self.file, ext = os.path.splitext(self.file)

        if self.file:
            if(ext == ".jpg" or ext == ".png"):
                self.state = 1
                mg.showinfo("Information", "Succesfully uploading picture")
                self.savedpic = "{}{}".format(self.file,ext)

            else:
                mg.showinfo("ERROR","Only Picture Are Allowed, Please Select jpg or png")
    def submit_clicked(self,controller):
        obj = PageOne(self, controller)
        self.check_male = self.var_male.get()
        self.check_femele = self.var_female.get()
        name = self.name_field.get()
        username = self.lname_field.get()
        ppass = self.pass_field.get()
        mobile = self.mobile_field.get()
        dob = self.dob_field.get()
        mail = self.email_field.get()
        add1 = self.address1_field.get()
        add2 = self.address2_field.get()

        country = self.country_var.get()
        state = self.state_var.get()
        city = self.city_var.get()
        level = self.lvl_var.get()
        try:
            subCountry = country[country.index("'") + 1:]
            subCountry = subCountry[:subCountry.index("'")]

            substate = state[state.index("'") + 1:]
            substate = substate[:substate.index("'")]

            subcity = city[city.index("'") + 1:]
            subcity = subcity[:subcity.index("'")]

            sublevel = level[level.index("'") + 1:]
            sublevel = sublevel[:sublevel.index("'")]
        except Exception:
            mg.showerror("Error", "Some of fields are missing")

        query = '''SELECT country_id FROM country WHERE country_name LIKE "{}" '''.format(subCountry)


        self.DbManger.cur.execute(query)
        self.DbManger.conn.commit()
        country_id = self.DbManger.cur.fetchall()
        country_id = [x[0] for x in country_id]


        query1 = '''SELECT state_id FROM state WHERE state_name LIKE "{}"'''.format(substate)
        self.DbManger.cur.execute(query1)
        self.DbManger.conn.commit()
        state_id = self.DbManger.cur.fetchall()

        state_id = [x[0] for x in state_id]

        query2 = '''SELECT city_id FROM city WHERE city_name LIKE "{}"'''.format(subcity)
        self.DbManger.cur.execute(query2)
        self.DbManger.conn.commit()
        city_id = self.DbManger.cur.fetchall()
        city_id = [x[0] for x in city_id]

        query3 = '''SELECT level_id FROM level WHERE level_title LIKE "{}"'''.format(sublevel)
        self.DbManger.cur.execute(query3)
        self.DbManger.conn.commit()
        level_id = self.DbManger.cur.fetchall()
        level_id = [x[0] for x in level_id]

        if(self.check_male == 1):
            check = "Male"
        elif(self.check_femele == 1):
            check = "femele"
        if(self.state ==1):
            pic = self.savedpic

            if(name and add1 and mail and username and ppass and dob and mobile and check
                    and pic and state and city and level and country):
                gender = check

                query1 = '''INSERT INTO users_user(user_username,user_password,user_name
                                  ,user_email,user_mobile,user_dob,user_image,user_gender
                                  ,user_add1,user_add2,user_country,user_state,user_city,user_level_id) 
                                  VALUES ('{}','{}','{}','{}','{}','{}'
                                  ,'{}','{}','{}','{}','{}','{}','{}','{}')'''.format(username, ppass,
                                  name, mail, mobile, dob, str(pic),gender,add1
                                  ,add2,country_id[0],state_id[0],city_id[0],level_id[0])



                if self.DbManger.cur.execute(query1):
                    mg.showinfo("Information"," You Are Successfully Registered , Please restart app to display changes")
                    self.DbManger.conn.commit()


                    controller.show_frame("StartPage")

                else:

                    mg.showinfo("ERROR","You must complete registration")
            else:
                    mg.showinfo("ERORR","Some of fields are missing")
        else:
            mg.showinfo("error","all fields must be filled")
class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.DbManger = DbManger()
        oldpass = tk.Label(self, text="Old Password", font=("Helvetica", 10))
        newpass = tk.Label(self, text="New Password", font=("Helvetica", 10))
        oldpass.grid(row=0, column=0, sticky=W)
        oldpass.place(relx=0.1, rely=0.28)
        newpass.grid(row=1, column=0, sticky=W)
        newpass.place(relx=0.1, rely=0.38)

        self.upw = tk.Entry(self, width=40)
        self.new_pw = tk.Entry(self, width=40)

        self.upw.grid(row=0, column=1, padx=10, pady=10)
        self.new_pw.grid(row=1, column=1, padx=10, pady=10)

        button1 = tk.Button(self, width=20, text="Apply Change", font=("Helvetica", 12),
                            command=lambda : self.apply_clicked(controller))
        button1.grid(columnspan=2, sticky=W)
        self.upw.place(relx=0.5, rely=0.3, anchor=CENTER)
        self.new_pw.place(relx=0.5, rely=0.4, anchor=CENTER)
        self.upw.config(bd=5)
        self.new_pw.config(bd=5)
        button1.place(relx=0.5, rely=0.55, anchor=CENTER)
    def apply_clicked(self , controller):
        upw = self.upw.get()
        newpw = self.new_pw.get()
        query = '''UPDATE users_user SET user_password = {} WHERE user_password = {}'''.format(newpw,upw)

        if(self.DbManger.cur.execute(query)):
            self.DbManger.conn.commit()


            controller.show_frame("StartPage")
        else:
            mg.showinfo("ERROR","Invalid Password")

class PageFour(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.DbManger = DbManger()
        self.controller = controller

        self.name_field = tk.Entry(self, width=50)
        self.name_field.place(relx=0.5, rely=0.27, anchor=CENTER)
        self.name_label = Label(self, text='First name', font=("Helvetica", 11))
        self.name_label.place(relx=0.5, rely=0.21, anchor=CENTER)
        self.name_field.config(bd=5)

        self.name_btn = Button(self, text="Upadate name", command=lambda : self.namebtn_clicked(controller))
        self.name_btn.place(relx=0.85, rely=0.27, anchor=CENTER)
        self.name_btn.config(bd=2, width=10)

        self.lname_field = tk.Entry(self, width=50)
        self.lname_field.place(relx=0.5, rely=0.39, anchor=CENTER)
        self.lname_label = Label(self, text='email', font=("Helvetica", 11))
        self.lname_label.place(relx=0.5, rely=0.33, anchor=CENTER)
        self.lname_field.config(bd=5)

        self.mail_btn = Button(self, text="Upadate email", command=lambda : self.mailbtn_clicked(controller))
        self.mail_btn.place(relx=0.85, rely=0.39, anchor=CENTER)
        self.mail_btn.config(bd=2, width=10)

        self.mobile_field = tk.Entry(self, width=50)
        self.mobile_field.place(relx=0.5, rely=0.51, anchor=CENTER)
        self.mobile_label = Label(self, text='Mobile', font=("Helvetica", 11))
        self.mobile_label.place(relx=0.5, rely=0.45, anchor=CENTER)
        self.mobile_field.config(bd=5)

        self.mobile_btn = Button(self, text="Upadate mobile", command=lambda : self.mobilebtn_clicked(controller))
        self.mobile_btn.place(relx=0.85, rely=0.51, anchor=CENTER)
        self.mobile_btn.config(bd=2, width=10)

    def namebtn_clicked(self,controller):
        obj = PageOne(self, controller)
        name = self.name_field.get()
        print(obj.foo[-1]['values'][1])
        if name:
            query = '''UPDATE users_user SET user_name= '{}' WHERE user_name = '{}' '''.format(name, obj.foo[-1]['values'][1])

            if (self.DbManger.cur.execute(query)):
                self.DbManger.conn.commit()
                mg.showinfo("Information", "Name Updated successfully you must restart app to display changes")
    def mailbtn_clicked(self,controller):
        obj = PageOne(self, controller)
        usermail = self.lname_field.get()
        print(usermail)
        print(obj.foo[-1]['values'][3])
        if usermail:
            query = '''UPDATE users_user SET user_email= '{}' WHERE user_email = '{}' '''.format(usermail, obj.foo[-1]['values'][3])

            if (self.DbManger.cur.execute(query)):
                self.DbManger.conn.commit()
                mg.showinfo("Information", "Mail Updated successfully you must restart app to display changes")
    def mobilebtn_clicked(self,controller):
        mobile = self.mobile_field.get()
        obj = PageOne(self, controller)
        print(obj.foo[-1]['values'][4])
        if mobile:
            query = '''UPDATE users_user SET user_mobile= {} WHERE user_mobile = {}'''.format(mobile, obj.foo[-1]['values'][4])

            if (self.DbManger.cur.execute(query)):
                self.DbManger.conn.commit()
                mg.showinfo("Information","Mobile Updated successfully you must restart app to display changes")

if __name__ == "__main__":

    app = myApp()

    app.mainloop()
