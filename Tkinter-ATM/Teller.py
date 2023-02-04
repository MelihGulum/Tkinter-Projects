from User import Config
import tkinter as tk
from tkinter import messagebox
from Model import Model
from tkinter import ttk
from PIL import ImageTk, Image
import random

model = Model()

class TellerMenuPage(Config):
    def __init__(self, parent, controller):
        Config.__init__(self, parent, controller)

        space_label = tk.Label(self, height=2, bg='#364859')
        space_label.pack()
        heading_label = tk.Label(self,
                                 text='TEAM BANK TELLER',
                                 font=('orbitron', 45, 'bold'),
                                 foreground='#ffffff',
                                 background='#364859')
        heading_label.pack(pady=25)

        main_menu_label = tk.Label(self,
                                   text='Main Menu',
                                   font=('orbitron', 13),
                                   fg='white',
                                   bg='#364859')
        main_menu_label.pack()

        selection_label = tk.Label(self,
                                   text='Please make a selection',
                                   font=('orbitron', 13),
                                   fg='white',
                                   bg='#364859',
                                   anchor='w')
        selection_label.pack()

        img = ImageTk.PhotoImage(Image.open("images/teller/teller.png").resize((400, 183)),Image.ANTIALIAS)
        teller_label = tk.Label(self,
                                bg='#364859',
                                image=img)
        teller_label.image = img
        teller_label.pack(pady=(30,0))

        button_frame = tk.Frame(self, bg='#364859')
        button_frame.pack(fill='both', expand=True)

        def add_customer():
            controller.show_frame('TellerAddCustomer')

        add_customer_button = Config.NewButton(button_frame,
                                               text='ADD CUSTOMER',
                                               command=add_customer,
                                               width=19,
                                               height=2)
        add_customer_button.grid(row=1, column=0, pady=(5), padx=(20,0))

        def list_customers():
            newWindow = tk.Toplevel()
            newWindow.geometry("848x286+100+80")
            newWindow.config(background="#386996")
            newWindow.resizable(False, False)
            newWindow.iconbitmap('images/common/icon.ico')

            list_frame = tk.Frame(newWindow)
            list_frame.pack(padx=5,pady=5)

            vsb = ttk.Scrollbar(list_frame)
            vsb.pack(side=tk.RIGHT, fill=tk.Y)
            customer_tree = ttk.Treeview(list_frame, yscrollcommand=vsb.set)
            customer_tree.pack()
            vsb.config(command=customer_tree.yview)
            data = model.getAllData()

            customer_tree['columns'] = ("ID", "ACOOUNT NO", "NAME", "SURNAME", "PASSWORD", "AMOUNT")
            customer_tree.column("#0", width=0, stretch=tk.NO)
            customer_tree.column("ID", anchor=tk.CENTER, minwidth=80, width=80, stretch=tk.NO)
            customer_tree.column("ACOOUNT NO", anchor=tk.W, minwidth=150, width=150, stretch=tk.NO)
            customer_tree.column("NAME", anchor=tk.W, minwidth=150, width=150, stretch=tk.NO)
            customer_tree.column("SURNAME", anchor=tk.W, minwidth=150, width=150, stretch=tk.NO)
            customer_tree.column("PASSWORD", anchor=tk.W, minwidth=150, width=150, stretch=tk.NO)
            customer_tree.column("AMOUNT", anchor=tk.W, minwidth=150, width=150, stretch=tk.NO)

            customer_tree.heading("ID", text="ID", anchor=tk.CENTER)
            customer_tree.heading("ACOOUNT NO", text="ACOOUNT NO", anchor=tk.CENTER)
            customer_tree.heading("NAME", text="NAME", anchor=tk.CENTER)
            customer_tree.heading("SURNAME", text="SURNAME", anchor=tk.CENTER)
            customer_tree.heading("PASSWORD", text="PASSWORD", anchor=tk.CENTER)
            customer_tree.heading("AMOUNT", text="AMOUNT", anchor=tk.CENTER)

            customer_tree.tag_configure('oddrow', background="white")
            customer_tree.tag_configure('evenrow', background="lightblue")
            style = ttk.Style()
            style.theme_use('default')
            style.configure('Treeview',rowheight=25,)
            style.map('Treeview',background=[('selected', '#347083')])

            global count
            count = 0
            for values in data:
                if count % 2 == 0:
                    customer_tree.insert("",tk.END, values=values,tag=('evenrow',))
                else:
                    customer_tree.insert("", tk.END,values=values,tag=('oddrow',))
                count += 1

        list_customer_button = Config.NewButton(button_frame,
                                                text='LIST CUSTOMERS',
                                                command=lambda: [list_customers()],
                                                width=19,
                                                height=2)
        list_customer_button.grid(row=1, column=1, pady=(5),  padx=(20,0))

        def exit():
            controller.show_frame('StartPage')

        exit_button = Config.NewButton(button_frame,
                                       text='EXIT',
                                       command=exit,
                                       width=19,
                                       height=2)
        exit_button.grid(row=1, column=2, pady=(5),  padx=(20,0))


class TellerAddCustomer(Config):
    def __init__(self, parent, controller):
        Config.__init__(self, parent, controller)

        space_label = tk.Label(self, height=2, bg='#364859')
        space_label.pack()
        heading_label = tk.Label(self,
                                 text='TEAM BANK TELLER',
                                 font=('orbitron', 45, 'bold'),
                                 foreground='#ffffff',
                                 background='#364859')
        heading_label.pack(pady=25)

        def enter_only_digits(entry, action_type) -> bool:
            if action_type == '1' and not entry.isdigit():
                return False
            return True

        def enter_only_string(entry, action_typed) -> bool:
            if action_typed == '1' and not entry.isalpha():
                return False
            return True

        def check_psw_len(new_value):
            try:
                if new_value.strip() == "": return True
                value = int(new_value)
                if value < 0 or value > 9999:
                    return False
            except ValueError:
                return False
            return True

        def caps(event):
            name.set(name.get().upper())
            surname.set(surname.get().upper())

        vcmd = (self.register(enter_only_digits), '%P', '%d')
        vcmd2 = (self.register(enter_only_string), '%P', '%d')
        vcmd3 = (self.register(check_psw_len), '%P')

        space_label = tk.Label(self, height=6, bg='#364859')
        space_label.pack()

        account_no_label = tk.Label(self,text='ACCOUNT NO :', width=15, height=3, anchor='c')
        account_no_label.place(x=70, y=180)
        account_no_entry = tk.Entry(self, width=100, justify='center')
        account_no_entry.place(x=181, y=180, height=51)
        account_no_entry.insert(0, model.check_account_no(random.sample(range(1, 10000), 1)))
        account_no_entry.config(state= "disabled")

        name = tk.StringVar()
        name_label = tk.Label(self,text='NAME :', width=15, height=3, anchor='c')
        name_label.place(x=70, y=242)
        name_entry_box = tk.Entry(self, textvariable=name, width=100, justify='center', validate='key', validatecommand=vcmd2)
        name_entry_box.place(x=181, y=242, height=51)
        name_entry_box.bind("<KeyRelease>", caps)

        surname = tk.StringVar()
        surname_label = tk.Label(self,text='SURNAME :',width=15, height=3, anchor='c')
        surname_label.place(x=70, y=304)
        surname_entry_box = tk.Entry(self, textvariable=surname, width=100, justify='center', validate='key', validatecommand=vcmd2)
        surname_entry_box.place(x=181, y=304, height=51)
        surname_entry_box.bind("<KeyRelease>", caps)

        password_label = tk.Label(self, text='PASSWORD :', width=15, height=3, anchor='c')
        password_label.place(x=70, y=366)
        password_entry_box = tk.Entry(self, width=100, justify='center', validate='key', validatecommand=vcmd3)
        password_entry_box.place(x=181, y=366, height=51)

        amount_label = tk.Label(self,text='AMOUNT :',width=15, height=3, anchor='c')
        amount_label.place(x=70, y=428)
        amount_entry_box = tk.Entry(self,width=100, justify='center', validate='key', validatecommand=vcmd)
        amount_entry_box.place(x=181, y=428, height=51)

        def submit():
            if not (account_no_entry.get() =="" and name_entry_box.get() ==""and
                    surname_entry_box.get() =="" and password_entry_box.get()==""
                    and amount_entry_box.get() == ""):
                if not (account_no_entry.get() == "" or name_entry_box.get() == "" or
                        surname_entry_box.get() == "" or password_entry_box.get() == ""
                        or amount_entry_box.get() == ""):
                    if(len(password_entry_box.get()) == 4):
                        if not (int(amount_entry_box.get()) <= 100):
                            try:
                                model.addToTable(account_no_entry.get(), name_entry_box.get(), surname_entry_box.get(),
                                                 password_entry_box.get(), amount_entry_box.get())
                                messagebox.showinfo("TEAM BANK ATM", " New Customer Added Successfully. "
                                                                     "\n You are being redirected to the home page.")
                                controller.show_frame("TellerMenuPage")

                                account_no_entry.config(state="normal")
                                account_no_entry.delete(0, tk.END)
                                name_entry_box.delete(0, tk.END)
                                surname_entry_box.delete(0, tk.END)
                                password_entry_box.delete(0, tk.END)
                                amount_entry_box.delete(0, tk.END)
                                account_no_entry.insert(0, random.sample(range(1, 10000), 1))
                                account_no_entry.config(state="disabled")
                                name_entry_box.focus_set()
                            except:
                                messagebox.showerror("TEAM BANK ATM", " Try Again Later")
                        else:
                            messagebox.showerror("TEAM BANK ATM", " Initial Amount Must Be Bigger Than $100")
                    else:
                        messagebox.showerror("TEAM BANK ATM", " The Password Should Be 4 Character")
                else:
                    messagebox.showerror("TEAM BANK ATM", " No information can be left blank.")
            else:
                messagebox.showerror("TEAM BANK ATM", " Fill in all the information.")

        submit_button = Config.NewButton(self,
                                         text='SUBMIT',
                                         command=submit,
                                         width=19,
                                         height=2)
        submit_button.place(x=450, y=510)

        def teller_menu():
            controller.show_frame('TellerMenuPage')

        teller_menu_button = Config.NewButton(self,
                                              text='MAIN MENU',
                                              command=teller_menu,
                                              width=19,
                                              height=2)
        teller_menu_button.place(x=100, y=510)
