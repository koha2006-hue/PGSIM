from tkinter import *
from tkinter import messagebox
import pyodbc

root=Tk()
root.title("Login")
root.geometry("925x500+300+200")
root.configure(bg='#fff')
root.resizable(False, False)

img=PhotoImage(file="PGSIM-main\PGSIM-main\PGSIM\Interface\login.png")
label=Label(root, image=img, border=0)
label.place(x=50, y=50)

frame=Frame(root,width=350,height=350,bg="white")
frame.place(x=480,y=50)


heading=Label(frame, text= "Sign In", font= ('Microsoft YaHei UI Light',23,'bold'), bg="white")
heading.place(x=120, y=5)

def on_enter1(e):
    if user.get() == "Username":
        user.delete(0, END)
def on_enter2(e):
    if password.get() == "Password":
        password.delete(0, END)
#---------------------------------------------------------------------------------------------
user=Entry(frame, width=45, border=0, bg="White",font=('Microsoft YaHei UI Light', 11))
user.place(x=30, y=80)
user.insert(0, "Username")
user.bind("<FocusIn>", on_enter1)


Frame(frame, width=350, height=2, bg="black").place(x=30, y=110)

#---------------------------------------------------------------------------------------------
password=Entry(frame, width=45, border=0, bg="White",font=('Microsoft YaHei UI Light', 11))
password.place(x=30, y=150)
password.insert(0, "Password")
password.bind("<FocusIn>", on_enter2)

Frame(frame, width=350, height=2, bg="black").place(x=30, y=180)
#---------------------------------------------------------------------------------------------

Button(frame,width=30, pady=7,text="Login", bg="#00B0F0", fg="white", font=('Microsoft YaHei UI Light', 11,'bold'), command=lambda: check_credentials(user.get(), password.get())).place(x=30, y=220)

#---------------------------------------------------------------------------------------------



def check_credentials(username, password):
    # Check if the connection exists in the database
    connection_string = f"Driver={{SQL Server}};Server=localhost;Database=users;Uid=username;Pwd=password;"
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM connections WHERE connection_name = ?", (username,))
    connection_count = cursor.fetchone()[0]

    if connection_count == 0:
        print("Connection does not exist. Would you like to sign up?")
        choice = input("Enter 'yes' to sign up or 'no' to exit: ")
        if choice.lower() == "yes":
            # Add connection to the database
            cursor.execute("INSERT INTO connections VALUES (?, ?)", (username, password))
            conn.commit()
            print("Sign up successful!")
        else:
            print("Exiting...")
    else:
        # Check correctness of username and password
        cursor.execute("SELECT COUNT(*) FROM connections WHERE connection_name = ? AND connection_password = ?", (username, password))
        credentials_count = cursor.fetchone()[0]

        if credentials_count == 0:
            messagebox.showerror("Error", "Incorrect username or password.")
        else:
            messagebox.showinfo("Success", "Login successful.")

    cursor.close()
    conn.close()


root.mainloop()