from tkinter import *
from tkinter import messagebox
import sqlite3
root = Tk()

#Intiatializing the title to the GUI
root.geometry('600x400')
root.title("Registration Form")


#This function to clear the username, password, and multi-line text box values
def clear() :
    password_entry.delete(0,END)
    username_entry.delete(0,END)
    multitextbox.delete(0,END)
    multitextbox.focus()
    

#This function to save the username and password into the database
def save_in_db():
    
    #To get the entered textbox value
    username=username_entry.get();
    password=password_entry.get();
    
    #To check the user has entered value for username and password
    if(len(username)>0 and len(password)>0):
        
           #Checks if password is more than of 8 characters and has digits in it
          if(len(password) < 8 or any(chr.isdigit() for chr in password)==False):
               messagebox.showwarning("error","Password does not meet the requirements")        
          else:
            conn = sqlite3.connect('Users.db')
            cursor=conn.cursor()
            
            #to create a table 
            cursor.execute("""CREATE TABLE IF NOT EXISTS User (id INTEGER PRIMARY KEY,
                              username TEXT,password TEXT)""")
               
            cursor.execute("SELECT username FROM User WHERE username = ?", (username,))
            results=cursor.fetchone()
            #print(results)
            
            #insert into database only if given user does not exists
            if(results==[] or results==None):
                cursor.execute('INSERT INTO User (username,password) VALUES(?,?)',(username,password))
                conn.commit()  
                cursor.close()
                conn.close()
                messagebox.showinfo("message","User added Successfully.")
               
            else:   
                messagebox.showwarning("error","User already exists in database.")
    else:
       messagebox.showwarning("error","The fields can not be left blank.")
         
      
          
#Function to get the list of users and their password from database and display it in listbox           
def show_users():
   multitextbox.delete(0,END)
   username=username_entry.get();
   password=password_entry.get();
   conn = sqlite3.connect('Users.db')   
   cursor=conn.cursor()
   
   cursor.execute("SELECT id,username,password FROM User ORDER By id DESC")
   result2=cursor.fetchall()
   output=""
   #print(result2)
   for x in result2:
       output=str(x[0])+" "+x[1]+" "+x[2]
   #print(output)   
       #to add each user row to the listbox
       multitextbox.insert(END,output)   
   conn.commit() ;
   cursor.close();
   conn.close()
   
    
#creates a label  for username
label_1 = Label(root, text="Enter your username",width=30)
label_1.place(x=-10,y=40)

#creates a textbox for username
username_entry = Entry(root)
username_entry.place(x=160,y=40,width=200,height=25)

#creates a label for password
label_2 = Label(root, text="Enter your password",width=30)
label_2.place(x=-10,y=80)

#creates a textbox for password
password_entry = Entry(root)
password_entry.place(x=160,y=80,width=200,height=25)


label_3 = Label(root, text="Display all username and assosicated password in the database")
label_3.place(x=160,y=220)

#creates a listbox
multitextbox = Listbox(root)
multitextbox.place(x=160,y=240,width=350,height=150)

# to create the buttons
Button(root, text='Save',width=10,command=save_in_db).place(x=160,y=120)
Button(root, text='Clear',width=10,command=clear).place(x=260,y=120)
Button(root, text='Display',width=10,command=show_users).place(x=70,y=250)


root.mainloop()
