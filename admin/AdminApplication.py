# Import modules
from pydoc import text
from tkinter import *
import datetime 
from tkinter import ttk 
from tkinter import messagebox
import tkinter

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="attnd"
)

def check_loggedin():
    f = open("user_id.txt", "r")
    return (f.read())

def register(): 
    name = name_input2.get()
    username = username_input2.get()
    password = password_input2.get()
    cpassword = cpassword_input2.get()
    mycursor = mydb.cursor()
    checkUserNamesql = f'SELECT * FROM user WHERE username ="{username}"'
    mycursor.execute(checkUserNamesql)
    myresult = mycursor.fetchall()
    if (len(myresult) == 0):
        if (password == cpassword):
            sql = "INSERT INTO user (name, username, password) VALUES (%s, %s, %s)"
            val = (name, username, password)
            mycursor.execute(sql, val)
            mydb.commit()
            getLoggedInsql = f'SELECT * FROM user WHERE username ="{username}" AND password="{password}"'
            mycursor.execute(getLoggedInsql)
            myresult = mycursor.fetchall()
            if (len(myresult) == 1): 
                f = open("user_id.txt", "a")
                f.write(f'{myresult[0][0]}')
                f.close()
                login_form.pack_forget()
                register_form.pack_forget()
                home_page.pack()
                messagebox.showinfo("showinfo", "Registration successfull.")
        else: 
            messagebox.showerror("showerror", "Password and confirm password need to be same.")
    else: 
        messagebox.showinfo("showerror", "Username already registered.")

def login():
    username = username_input.get()
    password = password_input.get()
    mycursor = mydb.cursor()
    getLoggedInsql = f'SELECT * FROM user WHERE username ="{username}" AND password="{password}"'
    mycursor.execute(getLoggedInsql)
    myresult = mycursor.fetchall()
    if (len(myresult) == 1): 
        f = open("user_id.txt", "a")
        f.write(f'{myresult[0][0]}')
        f.close()
        login_form.pack_forget()
        register_form.pack_forget()
        home_page.pack()
        messagebox.showinfo("showinfo", "Login successfull.")
    else:
        messagebox.showinfo("showerror", "Wrong credentials.")


def operation(arr):
    global pageHeading
    def switchOperation21():
        show.pack_forget()
        switchOperation2()
    def switchOperation11():
        show.pack_forget()
        switchOperation1()
    def switchOperation31():
        show.pack_forget()
        switchOperation3()
    
    def switchOperation41():
        show.pack_forget()
        switchOperation4()

    def addTeacher():
        name = add_teacher_name_input.get()
        teacher_id = add_teacher_teacher_id_input.get()
        password = add_teacher_password_input.get()
        status = n.get()
        if (status == "Active"):
            status = "1"
        else:
            status = "0"
        user_id = check_loggedin()
        sql = f"SELECT * FROM teacher WHERE teacher_id = {int(teacher_id)} AND userid = {int(user_id)}"
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        if (len(myresult) == 0):
            sql = f"INSERT INTO teacher (name, teacher_id, password, status, userid) VALUES ('{name}', {int(teacher_id)}, '{password}', '{status}', {int(user_id)});"
            mycursor = mydb.cursor()
            mycursor.execute(sql)
            mydb.commit()
            messagebox.showinfo("showinfo", "1 teacher added successfull.")
            add_teacher_name_input.delete(0, END)
            add_teacher_teacher_id_input.delete(0, END)
            add_teacher_password_input.delete(0, END)
            n.set("")
        else:
            messagebox.showinfo("showerror", "Teacher id already exist.")
            add_teacher_teacher_id_input.delete(0, END)
    def addStudent():
        year = datetime.datetime.now().year
        name = add_student_name_input.get()
        student_class = add_student_class_input.get()
        student_roll = add_student_roll_no_input.get()
        status = n.get()
        if (status == "Active"):
            status = "1"
        else:
            status = "0"
        user_id = check_loggedin()
        sql = f"SELECT * FROM student WHERE roll_no = {int(student_roll)} AND userid = {int(user_id)} AND class = {int(student_class)}"
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        if (len(myresult) > 0):
            messagebox.showinfo("showerror", "Student roll no already exist.")
            add_student_roll_no_input.delete(0, END)
        else:
            sql = f"INSERT INTO student (name, class, year, roll_no, status, userid) VALUES ('{name}', {int(student_class)}, {int(year)}, {int(student_roll)}, '{status}', {int(user_id)});"
            mycursor = mydb.cursor()
            mycursor.execute(sql)
            mydb.commit()
            messagebox.showinfo("showinfo", "1 student added successfull.")
            add_student_name_input.delete(0, END)
            add_student_class_input.delete(0, END)
            add_student_roll_no_input.delete(0, END)
            n.set("")



    # Show teacher frame 
    show = Frame(window)
    if (len(arr) == 2): 
        Sql = arr[1]
        mycursor = mydb.cursor()
        mycursor.execute(Sql)
        myresult = mycursor.fetchall()
        if (len(myresult) > 0):
            home_page.pack_forget()
            show.pack()

            button_frame = Frame(show)
            button_frame.pack()
            if (arr[0] == 'show teacher'):
                pageHeading.set("View Teacher")
                Button(button_frame, text="View Teacher", bg="red").grid(row=0, column=0)
                Button(button_frame, text="View Student", bg="lightgreen", command=switchOperation21).grid(row=0, column=1)
                Button(button_frame, text="Add Teacher", bg="lightgreen", command=switchOperation31).grid(row=0, column=2)
                Button(button_frame, text="Add Student", bg="lightgreen", command=switchOperation41).grid(row=0, column=3)
                myscrollbar=Scrollbar(show)
                myscrollbar.pack(side="right",fill = Y)
                name = Text(show, width=20, height=18, wrap = NONE, yscrollcommand=myscrollbar.set)
                name.insert(END,'---------------------------------------------')
                for val in myresult:
                    if (val[4] == '1'):
                        name.insert(END,f'\n Name: {val[1]}\n Teacher ID: {val[2]}\n Status: Active\n')
                        name.insert(END,'---------------------------------------------')
                    else:
                        name.insert(END,f'\n Name: {val[1]}\n Teacher ID: {val[2]}\n Status: Inactive')
                        name.insert(END,'---------------------------------------------')

                name.pack(side=TOP, fill=X)
                myscrollbar.config(command=name.yview)
            elif (arr[0] == 'show student'):
                pageHeading.set("View Student")
                Button(button_frame, text="View Teacher", bg="lightgreen", command=switchOperation11).grid(row=0, column=0)
                Button(button_frame, text="View Student", bg="red").grid(row=0, column=1)
                Button(button_frame, text="Add Teacher", bg="lightgreen", command=switchOperation31).grid(row=0, column=2)
                Button(button_frame, text="Add Student", bg="lightgreen", command=switchOperation41).grid(row=0, column=3)
                myscrollbar=Scrollbar(show)
                myscrollbar.pack(side="right",fill = Y)
                name = Text(show, width=20, height=18, wrap = NONE, yscrollcommand=myscrollbar.set)
                name.insert(END,'---------------------------------------------')
                for i in myresult:
                    if (i[5] == '1'):
                        name.insert(END,f'\n Name: {i[1]}\n Student Roll No: {i[4]}\n Class: {i[3]}\n Year: {i[2]}\n Status: Active\n')
                        name.insert(END,'---------------------------------------------')
                    else:
                        name.insert(END,f'\n Name: {i[1]}\n Student Roll No: {i[4]}\n Class: {i[3]}\n Year: {i[2]}\n Status: Inactive\n')
                        name.insert(END,'---------------------------------------------')
                name.pack(side=TOP, fill=X)
                myscrollbar.config(command=name.yview)
        else: 
            show.pack_forget()
            home_page.pack()
            messagebox.showinfo("showinfo", "No data found. Add some data first.")
    else:
        home_page.pack_forget()
        show.pack()
        button_frame = Frame(show)
        button_frame.pack()
        if(arr[0] == 'add teacher'):
            pageHeading.set("Add Teacher")
            Button(button_frame, text="View Teacher", bg="lightgreen", command=switchOperation11).grid(row=0, column=0)
            Button(button_frame, text="View Student", bg="lightgreen", command=switchOperation21).grid(row=0, column=1)
            Button(button_frame, text="Add Teacher", bg="red").grid(row=0, column=2)
            Button(button_frame, text="Add Student", bg="lightgreen", command=switchOperation41).grid(row=0, column=3)
            add_teacher_form = Frame(show)
            add_teacher_form.pack()

            add_teacher_name_label = Label(add_teacher_form, text="Full Name  ")
            add_teacher_name_label.grid(row=0, column=0, pady=10)
            add_teacher_name_input = Entry(add_teacher_form, bd=1, width=35)
            add_teacher_name_input.grid(row=0, column=1, pady=10)
            
            add_teacher_teacher_id_label = Label(add_teacher_form, text="Teacher ID  ")
            add_teacher_teacher_id_label.grid(row=1, column=0, pady=5)
            add_teacher_teacher_id_input = Entry(add_teacher_form, bd=1, width=35)
            add_teacher_teacher_id_input.grid(row=1, column=1, pady=5)

            add_teacher_password_label = Label(add_teacher_form, text="Password  ")
            add_teacher_password_label.grid(row=2, column=0, pady=5)
            add_teacher_password_input = Entry(add_teacher_form, bd=1, width=35, show="*")
            add_teacher_password_input.grid(row=2, column=1, pady=5)

            add_teacher_status_label = Label(add_teacher_form, text="Status  ")
            add_teacher_status_label.grid(row=3, column=0, pady=5)
            n = tkinter.StringVar() 
            status = ttk.Combobox(add_teacher_form, width = 27, textvariable = n)
            status['values'] = ('Active', 'Inactive') 
            status.grid(row=3, column=1, pady=5)

            add_teacher_button = Button(add_teacher_form, text="Add Teacher", bg="green", font=("Courier", 12), command=addTeacher)
            add_teacher_button.grid(row=4, column=1, pady=5)
        else:
            pageHeading.set("Add Student")
            Button(button_frame, text="View Teacher", bg="lightgreen", command=switchOperation11).grid(row=0, column=0)
            Button(button_frame, text="View Student", bg="lightgreen", command=switchOperation21).grid(row=0, column=1)
            Button(button_frame, text="Add Teacher", bg="lightgreen", command=switchOperation31).grid(row=0, column=2)
            Button(button_frame, text="Add Student", bg="red").grid(row=0, column=3)
            add_student_form = Frame(show)
            add_student_form.pack()

            add_student_name_label = Label(add_student_form, text="Full Name  ")
            add_student_name_label.grid(row=0, column=0, pady=10)
            add_student_name_input = Entry(add_student_form, bd=1, width=35)
            add_student_name_input.grid(row=0, column=1, pady=10)
            
            add_student_class_label = Label(add_student_form, text="Class ")
            add_student_class_label.grid(row=1, column=0, pady=5)
            add_student_class_input = Entry(add_student_form, bd=1, width=35)
            add_student_class_input.grid(row=1, column=1, pady=5)

            add_student_roll_no_label = Label(add_student_form, text="Roll No  ")
            add_student_roll_no_label.grid(row=2, column=0, pady=5)
            add_student_roll_no_input = Entry(add_student_form, bd=1, width=35)
            add_student_roll_no_input.grid(row=2, column=1, pady=5)

            add_student_status_label = Label(add_student_form, text="Status  ")
            add_student_status_label.grid(row=3, column=0, pady=5)
            n = tkinter.StringVar() 
            status = ttk.Combobox(add_student_form, width = 27, textvariable = n)
            status['values'] = ('Active', 'Inactive') 
            status.grid(row=3, column=1, pady=5)

            add_student_button = Button(add_student_form, text="Add Student", bg="green", font=("Courier", 12), command=addStudent)
            add_student_button.grid(row=4, column=1, pady=5)

            

          
    

def switchOperation1():
    user_id = check_loggedin()
    operation(["show teacher", f'SELECT * FROM teacher WHERE userid = "{int(user_id)}" ORDER BY teacher_id'])

def switchOperation2():
    user_id = check_loggedin()
    operation(["show student",f'SELECT * FROM student WHERE userid = "{int(user_id)}" ORDER BY class, roll_no'])

def switchOperation3():
    operation(["add teacher"])

def switchOperation4():
    operation(["add student"])

def changeFrame(): 
    global pageHeading
    heading = pageHeading.get()
    if (heading == "Login Page"):
        pageHeading.set("Register Page")
        login_form.pack_forget()
        register_form.pack()
    else: 
        pageHeading.set("Login Page")
        register_form.pack_forget()
        login_form.pack()

# Creating window
window = Tk()
window.title('Attendance System')
window.geometry('600x400')

# Declaration of components

# Heading for login page
heading = Label(window, text="Attendance System Admin Panel", font=("Courier", 18)).pack()

# Login page heading
pageHeading = StringVar()
pageHeading.set("Login Page")
heading_for_login = Label(
    window, textvariable=pageHeading, font=("Courier", 12)).pack()

# Login form
login_form = Frame(window)
login_form.pack()
# username field 
username_label = Label(login_form, text="User Name  ")
username_label.grid(row=0, column=0, pady=5)
username_input = Entry(login_form, bd=1, width=35)
username_input.grid(row=0, column=1, pady=5)
# password field 
password_label = Label(login_form, text="Password  ")
password_label.grid(row=1, column=0, pady=5)
password_input = Entry(login_form, bd=1, width=35, show="*")
password_input.grid(row=1, column=1, pady=5)
# login button 
login_button = Button(login_form, text="Login", bg="green", font=("Courier", 12), command=login)
login_button.grid(row=2, column=0, pady=5)
# register button 
register_button = Button(login_form, text="Register", bg="blue", font=("Courier", 12), command=changeFrame)
register_button.grid(row=2, column=1, pady=5)



# register form
register_form = Frame(window)

# username field 
name_label = Label(register_form, text="Name  ")
name_label.grid(row=0, column=0, pady=5)
name_input2 = Entry(register_form, bd=1, width=35)
name_input2.grid(row=0, column=1, pady=5)

# username field 
username_label = Label(register_form, text="User Name  ")
username_label.grid(row=1, column=0, pady=5)
username_input2 = Entry(register_form, bd=1, width=35)
username_input2.grid(row=1, column=1, pady=5)
# password field 
password_label = Label(register_form, text="Password  ")
password_label.grid(row=2, column=0, pady=5)
password_input2 = Entry(register_form, bd=1, width=35, show="*")
password_input2.grid(row=2, column=1, pady=5)
# confirm password field 
cpassword_label = Label(register_form, text="Confirm Password  ")
cpassword_label.grid(row=3, column=0, pady=5)
cpassword_input2 = Entry(register_form, bd=1, width=35, show="*")
cpassword_input2.grid(row=3, column=1, pady=5)
# register button 
register_button = Button(register_form, text="Login", bg="lightgreen", font=("Courier", 12), command=changeFrame)
register_button.grid(row=4, column=0, pady=5)
# register button 
register_button = Button(register_form, text="Register", bg="lightblue", font=("Courier", 12), command=register)
register_button.grid(row=4, column=1, pady=5)

# Home page 
home_page = Frame(window)

view_teacher_button = Button(home_page, text="View Teachers", bg="lightgreen", font=("Courier", 12), height=3, width=15, command=switchOperation1)
view_teacher_button.grid(row=0, column=0, pady=10)

view_student_button = Button(home_page, text="View Student", bg="lightblue", font=("Courier", 12), height=3, width=15, command=switchOperation2)
view_student_button.grid(row=0, column=1, padx=10, pady=10)


add_teacher_button = Button(home_page, text="Add Teachers", bg="green", font=("Courier", 12), height=3, width=15, command=switchOperation3)
add_teacher_button.grid(row=1, column=0, pady=10)

add_student_button = Button(home_page, text="Add Student", bg="deepskyblue", font=("Courier", 12), height=3, width=15, command=switchOperation4)
add_student_button.grid(row=1, column=1, padx=10, pady=10)




# Checking if already loggedin or not
user_id = check_loggedin()
if (int(user_id) != 0):
    pageHeading.set("Home Page")
    login_form.pack_forget()
    register_form.pack_forget()
    home_page.pack()



# Starting window
window.mainloop()