from tkinter import *
from tkinter import ttk
import sqlite3
import tkinter.font
import sys
import os
import subprocess


#if you want to use it as a real .exe file please remove exe()'s #
def exe():
    subprocess.check_call([sys.executable, '-m','pip','install','pyinstaller'])
    reqs= subprocess.check_output([sys.executable, '-m','pip','freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split() ]
    print(installed_packages)
    os.system("pyinstaller --onefile -w dictionary.py")

#exe()

#Making root configurations
root = Tk()
root.title("LEARN VACOBULARY")
root.iconbitmap('dict.ico')
app_height =550
app_width =500
root.geometry(f'{app_width}x{app_height}+{400}+{100}')
root.resizable(False, False)
root.config(background ="light gray")

#Connection to the our sqlite database
conn = sqlite3.connect('user_dict.db')
c = conn.cursor()

#We are creating here our table in db ,if is exist alreadty this block will be skipped
c.execute(""" CREATE TABLE if not exists words(
    word text,
    meaning text

)
            
""")

#This is our submit function. We get entryies and inserting the values in db and table
def submit():
    conn = sqlite3.connect('user_dict.db')
    c = conn.cursor()

    c.execute('INSERT INTO words VALUES (:wordEntry , :meaningEntry)',
              {
                  'wordEntry': wordEntry.get(),
                  'meaningEntry': meaningEntry.get()
              }
              )

    conn.commit()
    conn.close()

    wordEntry.delete(0 ,END)
    meaningEntry.delete(0 , END)



#This function lead us to secand page
#When clicked "Show words" button showAll function execute and it will list he words
def showAll():
    hideAllFrames()
    showAllFrame.pack(fill="both" , expand="true")
    conn = sqlite3.connect('user_dict.db')
    c = conn.cursor()

    c.execute("SELECT * , oid FROM words")
    records = c.fetchall()
    #print(records)
    print_records =''

    conn.commit()
    conn.close()

    style = ttk.Style()
    style.theme_use('default')
    style.configure('Treeview',

                    rowheight=25,
                    )
    style.map('Treeview',
              background=[('selected','#347083')])

#selectRecords func. is help us to select the word we wanted
    def selectRecord(e):
        wordEntry.delete(0 ,END)
        meaningEntry.delete(0 , END)
        wordIdEntry.delete(0, END)
        selected = myTree.focus()
        values = myTree.item(selected ,'values')
        wordIdEntry.insert(0 ,values[0])
        wordEntry.insert(0, values[1])
        meaningEntry.insert(0, values[2])


#When clik "Update Word" button this func. will summon
#And it allows us to change the selected word
    def update():
        selected = myTree.focus()
        myTree.item(selected , text="", values=(wordIdEntry.get(),wordEntry.get(), meaningEntry.get(),))
        conn = sqlite3.connect('user_dict.db')
        c = conn.cursor()

        c.execute(""" UPDATE words SET
            word =:word,
            meaning=:meaning
        
            WHERE oid = :oid""",
                  {
                      'word' : wordEntry.get(),
                      'meaning': meaningEntry.get(),
                      'oid' :wordIdEntry.get(),

                  }
        )


        conn.commit()
        conn.close()

#If you clicked the "Delete Word" button it will delete the selected word
    def delete():
        selected = myTree.focus()
        myTree.item(selected , text="", values=(wordIdEntry.get(),wordEntry.get(), meaningEntry.get(),))
        conn = sqlite3.connect('user_dict.db')
        c = conn.cursor()
        c.execute("DELETE from words  WHERE oid= " + wordIdEntry.get())

        conn.commit()
        conn.close()

#We are creating here table for our wordlist
    myTree = ttk.Treeview(root)
    myTree.place(x=57, y=10)

    myTree['columns'] = ("ID", "WORD", "MEANING")
    myTree.column("#0", width=0, stretch=NO)
    myTree.column("ID", anchor=CENTER, width=80)
    myTree.column("WORD", anchor=W, width=150)
    myTree.column("MEANING", anchor=W, width=150)

    myTree.heading("ID", text="ID", anchor=CENTER)
    myTree.heading("WORD", text="WORD", anchor=CENTER)
    myTree.heading("MEANING", text="MEANING", anchor=CENTER)


    myTree.tag_configure('oddrow', background="white")
    myTree.tag_configure('evenrow', background="lightblue")

    global  count
    count= 0
    for record in records:
        if count % 2 ==0:
            myTree.insert(parent='', index="end" ,iid=count , text="", values=(record[2],record[0],record[1],),tag=('evenrow', ))
        else:
            myTree.insert(parent='', index="end" ,iid=count , text="", values=(record[2],record[0],record[1],),tag=('oddrow', ))
        count +=1



    wordIdLabel = Label(root, text="The words Id: ", bg="light gray")
    wordIdLabel.place(x=109, y=340)
    wordIdEntry = Entry(root, width=30, borderwidth=1, fg="blue")
    wordIdEntry.place(x=185, y=340)
    wordIdEntry.insert(0, "")

    wordLabel = Label(root, text="The word you want to update: ", bg="light gray")
    wordLabel.place(x=22, y=370)
    wordEntry = Entry(root, width=30, borderwidth=1, fg="blue")
    wordEntry.place(x=185, y=370)
    wordEntry.insert(0, "")

    meaningLabel = Label(root, text="Words meaning:", bg="light gray")
    meaningLabel.place(x=92, y=400)
    meaningEntry = Entry(root, width=30, borderwidth=1, fg="blue")
    meaningEntry.place(x=185, y=400)
    meaningEntry.insert(0, "")
    updateButton = Button(root, text="Update Word",padx=30,pady=10,borderwidth=2,activebackground="gray",bg="#546879",
                          relief=GROOVE, command=update)
    updateButton.place(x=250, y = 500)
    updateFrame = Frame(root, width=550, height=500, bg="light gray")
    deleteButton = Button(root, text="Delete Word",padx=30,pady=10,borderwidth=2,activebackground="gray",bg="#546879",
                          relief=GROOVE, command=delete)
    deleteButton.place(x=80, y = 500)
    myTree.bind("<ButtonRelease-1>", selectRecord ,)


#hideAllFrames provides us to travel safe between frames.
#when we click "Show words" frames which are in main page will disappear

def hideAllFrames():
    insertFrame.pack_forget()
    greetingFrame.pack_forget()

greetingFrame = LabelFrame(root,bg="light gray",borderwidth=0,highlightthickness=0)
greetingFrame.pack()
font = tkinter.font.Font(family="Helvetica", size=25, weight="bold")
headerLabel = Label(greetingFrame, text="WELCOME TO" + "\n" + " LEARN VACOBULARY", font=font, bg="light gray")
headerLabel.pack(side="top", fill="x", pady=20)

insertFrame = LabelFrame(root, bg="light gray")
insertFrame.pack(fill="x", padx=20, pady=100)

wordLabel = Label(insertFrame, text="The word you want to insert:", bg="light gray")
wordLabel.grid(row=0,column=0 ,padx=10 ,pady=10)
wordEntry = Entry(insertFrame, width=30, borderwidth=1, fg="blue")
wordEntry.grid(row=0,column=1,padx=10 ,pady=10)
wordEntry.insert(0, "")

meaningLabel = Label(insertFrame, text="Words meaning:", bg="light gray")
meaningLabel.grid(row=1,column=0,padx=10 ,pady=10)
meaningEntry = Entry(insertFrame, width=30, borderwidth=1, fg="blue")
meaningEntry.grid(row=1,column=1,padx=10 ,pady=10)
submitButton = Button(root, text="Submit", padx=30, pady=10, borderwidth=2, activebackground="gray", bg="#546879",
                          relief=GROOVE, command=submit)
submitButton.place(x=100, y=450)


showAllButton = Button(root, text="Show Words" ,padx=30,pady=10,borderwidth=2,activebackground="gray",bg="#546879",relief=GROOVE, command=showAll)
showAllButton.place(x=250 , y=450)
showAllFrame = Frame(root , width = 550 , height=500 , bg="light gray")


root.mainloop()
