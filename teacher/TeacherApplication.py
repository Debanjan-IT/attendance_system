# Import modules
from pydoc import text
from tkinter import *
import datetime 
from tkinter import ttk 
from tkinter import messagebox
import tkinter
from turtle import color

import mysql.connector


num = 0

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="attnd"
)

def check_loggedin():
    user_data = []
    f = open("teacher_id.txt", "r")
    user_data.append(f.read())
    f.close()
    f = open("user_id.txt", "r")
    user_data.append(f.read())
    f.close()
    return (user_data)

def login():
    username = username_input.get()
    password = password_input.get()
    mycursor = mydb.cursor()
    getLoggedInsql = f'SELECT * FROM teacher WHERE teacher_id ="{username}" AND password="{password}"'
    mycursor.execute(getLoggedInsql)
    myresult = mycursor.fetchall()
    if (len(myresult) == 1): 
        f = open("teacher_id.txt", "a")
        f.write(f'{myresult[0][0]}')
        f.close()
        f = open("user_id.txt", "a")
        f.write(f'{myresult[0][5]}')
        f.close()
        login_form.pack_forget()
        home_page.pack()
        pageHeading.set("Home Page")
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
    def present(id):
        global num
        num = num + 1
        classSelected()


    def classSelected():
        user_id = check_loggedin()
        student_sql = f"SELECT * FROM student WHERE userid = {int(user_id[1])} AND class = {int(class_combo.get())} LIMIT 1 OFFSET {int(num)}"
        mycursor = mydb.cursor()
        mycursor.execute(student_sql)
        myresult = mycursor.fetchall()
        if (len(myresult) > 0):
            id_student = myresult[0][0]
            def closeFrame():
                attendance.pack_forget()
            class_select_frame.pack_forget()
            attendance = Frame(show)
            attendance.pack()
            Label(attendance, text="Name:   "+myresult[0][1], font=("Courier", 12)).pack(pady=10)
            present_button = Button(attendance, text="Present", background='lightgreen', command=lambda: [closeFrame(),present(id_student)])
            present_button.pack(pady=10)
            absent_button = Button(attendance, text="Absent", background='red')
            absent_button.pack(pady=10)
        else:
            messagebox.showinfo("showerror", "No more students.")
            show.pack_forget()
            home_page.pack()
            pageHeading.set("Home Page")




        

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
            if (arr[0] == 'add attendance'):
                pageHeading.set("Add Attendance")
                Button(button_frame, text="Add Attendance", bg="red").grid(row=0, column=0)
                Button(button_frame, text="Promote Student", bg="lightgreen", command=switchOperation21).grid(row=0, column=1)

                class_select_frame = Frame(show)
                class_select_frame.pack()
                Label(class_select_frame, text="Select a class  ").pack(pady=5)

                n = tkinter.StringVar() 
                class_combo = ttk.Combobox(class_select_frame, width = 27, textvariable = n)
                classes = []
                for i in myresult:
                    classes.append(i[0])
                class_combo['values'] = classes
                class_combo.pack(pady=5)

                choose_class_button = Button(class_select_frame,  text="Select Class", bg="lightgreen", command=classSelected)
                choose_class_button.pack(pady=5)


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
    operation(["add attendance", f'SELECT DISTINCT class FROM student WHERE userid = "{int(user_id[1])}" ORDER BY class'])

def switchOperation2():
    user_id = check_loggedin()
    operation(["promote student",f'SELECT * FROM student WHERE userid = "{int(user_id)}" ORDER BY class, roll_no'])

# Creating window
window = Tk()
window.title('Attendance System')
window.geometry('600x400')

# Declaration of components

# Heading for login page
heading = Label(window, text="Attendance System Teacher Panel", font=("Courier", 18)).pack()

# Login page heading
pageHeading = StringVar()
pageHeading.set("Login Page")
heading_for_login = Label(
    window, textvariable=pageHeading, font=("Courier", 12)).pack()

# Login form
login_form = Frame(window)
login_form.pack()
# username field 
username_label = Label(login_form, text="Teacher ID  ")
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

note = Label(login_form, text="*For registration, please contact the admin.", fg="red", font=("Courier", 10))
note.grid(row=2, column=1, pady=5)


# Home page 
home_page = Frame(window)

add_attendance_button = Button(home_page, text="Add Attendance", bg="lightgreen", font=("Courier", 12), height=3, width=15, command=switchOperation1)
add_attendance_button.grid(row=0, column=0, pady=10)

promote_student_button = Button(home_page, text="Promote Student", bg="lightblue", font=("Courier", 12), height=3, width=15, command=switchOperation2)
promote_student_button.grid(row=0, column=1, padx=10, pady=10)





# Checking if already loggedin or not
user_id = check_loggedin()
if (int(user_id[0]) != 0 and int(user_id[1]) != 0):
    pageHeading.set("Home Page")
    login_form.pack_forget()
    home_page.pack()



# Starting window
window.mainloop()