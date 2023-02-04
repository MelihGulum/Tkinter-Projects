import tkinter as tk
from tkinter import *
import time
import tkinter.font as font
from tkinter import messagebox
from itertools import cycle
from PIL import ImageTk, Image
from Model import Model

model = Model()
current_balance = 0

def escape(button_frame, controller):
    def menu():
        controller.show_frame('MenuPage')

    img = ImageTk.PhotoImage(Image.open('images/user/go-back.png').resize((34,34),Image.ANTIALIAS))
    menu_button =Config.NewButton(button_frame,
                            text='MENU',
                                  image= img,
                            command=menu,
                            width=360,
                            height=78)
    menu_button.grid(row=3, column=0, pady=4, padx=(42, 25))
    menu_button.image = img

    def exit():
        controller.show_frame('StartPage')

    img = ImageTk.PhotoImage(Image.open('images/user/close-window.png').resize((34,34),Image.ANTIALIAS))
    exit_button = Config.NewButton(button_frame,
                            text='EXIT',
                            image=img,
                            command=exit,
                            width=360,
                            height=78)
    exit_button.grid(row=3, column=1, pady=4, padx=25)
    exit_button.image = img

def enter_only_digits(entry, action_type) -> bool:
    if action_type == '1' and not entry.isdigit():
        return False
    return True


class Config(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#364859')
        self.controller = controller

        bottom_frame = Frame(self, relief='raised', borderwidth=1)
        bottom_frame.pack(fill='x', side='bottom')

        visa_photo = tk.PhotoImage(file='images/common/visa.png')
        visa_label = tk.Label(bottom_frame, image=visa_photo)
        visa_label.pack(side='left',padx=(10,3))
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file='images/common/mastercard.png')
        mastercard_label = tk.Label(bottom_frame, image=mastercard_photo)
        mastercard_label.pack(side='left', padx=(3,3))
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file='images/common/american-express.png')
        american_express_label = tk.Label(bottom_frame, image=american_express_photo)
        american_express_label.pack(side='left', padx=(3,3))
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
            time_label.config(text=current_time)
            time_label.after(200, tick)
        time_label = tk.Label(bottom_frame, font=('orbitron', 12))
        time_label.pack(side='right', padx=(0,10))
        tick()

    class NewButton(tk.Button):
        def __init__(self, master=None, **kwargs):
            tk.Button.__init__(self,
                               master,
                               relief='raised',
                               borderwidth=3,
                               bg='gray90',
                               fg='black',
                               compound='left',
                               font=("Segoe UI",18),
                               **kwargs)

class StartPage(Config):
    def __init__(self, parent, controller):
        Config.__init__(self, parent, controller)
        space_label = tk.Label(self, height=2, bg='#364859')
        space_label.pack()

        heading_label = Label(self,
                                 text='TEAM BANK ATM',
                                 font=('orbitron', 45, 'bold'),
                                 foreground='#ffffff',
                                 background='#364859')
        heading_label.pack(pady=25)


        account_no_label = tk.Label(self,
                                  text='Account No:',
                                  font=('orbitron', 13),
                                  bg='#364859',
                                  fg='white')
        account_no_label.place(x=130, y=250)

        account_no_entry = tk.Entry(self,
                                    font=('orbitron', 12),
                                    width=22)
        account_no_entry.focus_set()
        account_no_entry.place(x=240, y=245, height=35)

        password_label = tk.Label(self,
                                  text='Password:',
                                  font=('orbitron', 13),
                                  bg='#364859',
                                  fg='white')
        password_label.place(x=130, y=315)

        vcmd = (self.register(enter_only_digits), '%P', '%d')
        my_password = tk.StringVar()
        password_entry_box = tk.Entry(self,
                                      textvariable=my_password,
                                      font=('orbitron', 12),
                                      width=22,
                                      validate='key',
                                      validatecommand=vcmd)
        password_entry_box.place(x=240, y=310, height=35)

        def handle_focus_in(_):
            password_entry_box.configure(fg='black', show='*')

        password_entry_box.bind('<FocusIn>', handle_focus_in)

        def check_password():
            if account_no_entry.get() == "":
                messagebox.showinfo("TEAM BANK ATM", " Account number cannot be empty.")
                password_entry_box.delete(0, END)
            elif password_entry_box.get() == "":
                messagebox.showinfo("TEAM BANK ATM", " Password cannot be empty.")
                account_no_entry.delete(0, END)
            elif (account_no_entry.get() == "Doctor" and my_password.get() == '23815'):
                controller.show_frame('TellerMenuPage')
                account_no_entry.delete(0, END)
                password_entry_box.delete(0, END)
            elif(account_no_entry.get() !="" and password_entry_box.get() !=""):
                log = model.login(account_no_entry.get(), password_entry_box.get())
                if(len(password_entry_box.get()) == 4):
                    if (log) is not None:
                        account_no_entry.delete(0, END)
                        password_entry_box.delete(0, END)

                        global current_balance
                        current_balance = log[5]
                        account_no = log[1]
                        account_name= log[2]
                        controller.shared_data['Balance'].set(current_balance)
                        controller.shared_data['Account'].set(account_no)
                        controller.shared_data['Name'].set(account_name)
                        controller.show_frame("MenuPage")
                    else:
                        messagebox.showerror("TEAM BANK ATM", " You do not have account.")
                        account_no_entry.delete(0, END)
                        password_entry_box.delete(0, END)
                else:
                    messagebox.showerror("TEAM BANK ATM", " Your Password Should Be 4 Character")
            else:
                messagebox.showerror("TEAM BANK ATM", " Something went wrong. Please try again later.")

        enter_button = Config.NewButton(self,
                                 text='ENTER',
                                 command=check_password,
                                 width=15,
                                 height=1)
        enter_button.place(x=240, y=370)

        images = ["images/common/slider1.jpg", "images/common/slider2.jpg", "images/common/slider3.jpg","images/common/slider4.jpg"]
        photos = cycle(ImageTk.PhotoImage(Image.open(image).resize((300, 183))) for image in images)

        def slideShow():
            img = next(photos)
            displayCanvas.config(image=img)
            self.after(2500, slideShow)  # 2.5 seconds

        displayCanvas = tk.Label(self,
                                 text='',
                                 bg='#364859',
                                 anchor='n')
        displayCanvas.place(x=480, y=240)
        slideShow()


class MenuPage(Config):
    def __init__(self, parent, controller):
        Config.__init__(self, parent, controller)
        space_label = tk.Label(self, height=2, bg='#364859')
        space_label.pack()
        heading_label = tk.Label(self,
                                 text='TEAM BANK ATM',
                                 font=('orbitron', 45, 'bold'),
                                 foreground='#ffffff',
                                 background='#364859')
        heading_label.pack(pady=25)

        def greeting():
            import datetime
            currentTime = datetime.datetime.now()
            if currentTime.hour < 12:
                greeting_time_label.config(text="Good Morning,")
            elif 12 <= currentTime.hour < 18:
                greeting_time_label.config(text="Good Afternoon," )
            else:
                greeting_time_label.config(text="Good Evening,")

        space_label = tk.Label(self, height=1, bg='#364859')
        space_label.pack()

        greeting_time_label = tk.Label(self,
                                       text="",
                                       font=('orbitron', 13),
                                    fg='white',
                                    bg='#364859')
        greeting_time_label.place(x=335, y=156)
        greeting()
        greeting_label = tk.Label(self,
                                    textvariable=controller.shared_data['Name'],
                                  font=('orbitron', 13),
                                   fg='white',
                                   bg='#364859')
        greeting_label.place(x=458, y=158)

        main_menu_label = tk.Label(self,
                                   text='Welcome to Main Menu',
                                   font=('orbitron', 13),
                                   fg='white',
                                   bg='#364859')
        main_menu_label.pack()

        selection_label = tk.Label(self,
                                   text=' Please make a selection',
                                   font=('orbitron', 13),
                                   fg='white',
                                   bg='#364859',
                                   anchor='w')
        selection_label.pack()

        button_frame = tk.Frame(self, bg='#364859')
        button_frame.pack(fill='both', expand=True)

        space_label = tk.Label(self, height=1, bg='#364859')
        space_label.pack()

        def withdraw():
            controller.show_frame('WithdrawPage')

        img = ImageTk.PhotoImage(Image.open('images/user/cash-icon.png').resize((64,64),Image.ANTIALIAS))
        withdraw_button = Config.NewButton(button_frame,
                                           text='   WITHDRAW',
                                           image=img,
                                           command=withdraw,
                                           width=360,
                                           height=78)
        withdraw_button.image = img
        withdraw_button.grid(row=1, column=0, pady=(60,5), padx=30)

        def deposit():
            controller.show_frame('DepositPage')

        img = ImageTk.PhotoImage(Image.open('images/user/deposit.png').resize((64,64),Image.ANTIALIAS))
        deposit_button = Config.NewButton(button_frame,
                                   text='   DEPOSIT    ',
                                   image = img,
                                   command=deposit,
                                   width=360,
                                   height=78)
        deposit_button.image = img
        deposit_button.grid(row=2, column=0, pady=(10), padx=30)

        def balance():
            controller.show_frame('BalancePage')

        img = ImageTk.PhotoImage(Image.open('images/user/balance.png').resize((64,64),Image.ANTIALIAS))
        balance_button = Config.NewButton(button_frame,
                                   text='   BALANCE',
                                   image=img,
                                   command=balance,
                                   width=360,
                                   height=78)
        balance_button.image = img
        balance_button.grid(row=1, column=1, pady=(60,5), padx=30)

        def exit():
            controller.show_frame('StartPage')

        img = ImageTk.PhotoImage(Image.open('images/user/close-window.png').resize((70,64),Image.ANTIALIAS))
        exit_button = Config.NewButton(button_frame,
                                text='  EXIT        ',
                                image= img,
                                command=exit,
                                width=360,
                                height=78)
        exit_button.image=img
        exit_button.grid(row=2, column=1, pady=(10), padx=30)


class WithdrawPage(Config):
    def __init__(self, parent, controller):
        Config.__init__(self, parent, controller)

        heading_label = tk.Label(self,
                                 text='TEAM BANK ATM',
                                 font=('orbitron', 45, 'bold'),
                                 foreground='#ffffff',
                                 background='#364859')
        heading_label.pack(pady=25)

        global current_balance
        controller.shared_data['Balance'].set(current_balance)
        balance_text_label = tk.Label(self,
                                 text="Current Balance: $",
                                 font=('orbitron', 13),
                                 fg='white',
                                 bg='#364859')
        balance_text_label.place(x=273, y=125)
        balance_label = tk.Label(self,
                                 textvariable=controller.shared_data['Balance'],
                                 font=('orbitron', 13),
                                 fg='white',
                                 bg='#364859')
        balance_label.pack(padx=(38,0))

        choose_amount_label = tk.Label(self,
                                       text='Choose the amount you want to withdraw',
                                       font=('orbitron', 13),
                                       fg='white',
                                       bg='#3d3d5c')
        choose_amount_label.pack()
        button_frame = tk.Frame(self, bg='#364859')
        button_frame.pack(fill='both', expand=True)

        def withdraw(amount):
            global current_balance
            if (current_balance <=0) or ((current_balance -amount) <=0):
                messagebox.showinfo("TEAM BANK ATM",
                                    "You Do not Have No Money")
            else:
                current_balance -= amount
                controller.shared_data['Balance'].set(current_balance)
                messagebox.showinfo("TEAM BANK ATM", f" ${amount} was withdrawn."
                                                     f"\n You are being redirected to the home page.")
                model.update_balance(current_balance,controller.shared_data['Account'].get())
                controller.show_frame('MenuPage')

        def other_amount(_):
            global current_balance
            if current_balance <=0:
                messagebox.showinfo("TEAM BANK ATM", "You Do not Have No Money")
            if int(cash.get()) > current_balance:
                messagebox.showinfo("TEAM BANK ATM", "There is not enough balance.")
            else:
                current_balance -= int(cash.get())
                controller.shared_data['Balance'].set(current_balance)
                messagebox.showinfo("TEAM BANK ATM", f" ${int(cash.get())} was withdrawn."
                                                     f"\n You are being redirected to the home page.")
                model.update_balance(current_balance, controller.shared_data['Account'].get())
                cash.set('')
                controller.show_frame('MenuPage')


        cash_image = ImageTk.PhotoImage(Image.open("images/user/banknote.png").resize((34, 34)))

        fifty_button = Config.NewButton(button_frame,
                                        text=' $50  ',
                                        image=cash_image,
                                        command=lambda: withdraw(50),
                                        width=360,
                                        height=78)
        fifty_button.grid(row=0, column=0, pady=(20,10), padx=(40,20))
        fifty_button.image = cash_image

        hundred_button = Config.NewButton(button_frame,
                                          text=' $100',
                                          image=cash_image,
                                          command=lambda: withdraw(100),
                                          width=360,
                                          height=78)
        hundred_button.grid(row=1, column=0, pady=5, padx=(40,20))
        hundred_button.image = cash_image

        hundred_fifty_button = Config.NewButton(button_frame,
                                                text=' $150',
                                                image=cash_image,
                                                command=lambda: withdraw(150),
                                                width=360,
                                                height=78)
        hundred_fifty_button.grid(row=2, column=0, pady=5, padx=(40,20))
        hundred_fifty_button.image = cash_image

        two_hundred_fifty_button = Config.NewButton(button_frame,
                                                    text=' $250',
                                                    image=cash_image,
                                                    command=lambda: withdraw(250),
                                                    width=360,
                                                    height=78)
        two_hundred_fifty_button.grid(row=0, column=1,pady=(20,10))
        two_hundred_fifty_button.image = cash_image

        five_hundred_button = Config.NewButton(button_frame,
                                               text=' $500',
                                               image=cash_image,
                                               command=lambda: withdraw(500),
                                               width=360,
                                               height=78)
        five_hundred_button.grid(row=1, column=1, pady=5)
        five_hundred_button.image = cash_image

        cash = tk.StringVar()
        italic_style = font.Font(family='Helvetica',weight="normal",slant = "italic")
        other_amount_entry = tk.Entry(button_frame,
                                      textvariable=cash,
                                      width=33,
                                      bd=1,
                                      bg='gray90',
                                      fg='grey49',
                                      justify='center',
                                      font= italic_style)

        other_amount_entry.insert(0, "OTHER")
        other_amount_entry.bind("<FocusIn>", lambda args: other_amount_entry.delete(0, END))
        other_amount_entry.grid(row=2, column=1, pady=10, ipady=30, ipadx=3)
        other_amount_entry.bind('<Return>', other_amount)

        escape(button_frame, controller)


class DepositPage(Config):
    def __init__(self, parent, controller):
        Config.__init__(self, parent, controller)
        space_label = tk.Label(self, height=2, bg='#364859')
        space_label.pack()
        heading_label = tk.Label(self,
                                 text='TEAM BANK ATM',
                                 font=('orbitron', 45, 'bold'),
                                 foreground='#ffffff',
                                 background='#364859')
        heading_label.pack(pady=25)

        space_label = tk.Label(self, height=2, bg='#364859')
        space_label.pack()

        enter_amount_label = tk.Label(self,
                                      text='Enter amount',
                                      font=('orbitron', 13),
                                      bg='#3d3d5c',
                                      fg='white')
        enter_amount_label.pack(pady=10)

        vcmd = (self.register(enter_only_digits), '%P', '%d')
        cash = tk.StringVar()
        deposit_entry = tk.Entry(self,
                                 textvariable=cash,
                                 font=('orbitron', 12),
                                 justify='center',
                                 width=22,
                                 validate='key',
                                 validatecommand=vcmd)
        deposit_entry.pack(ipady=7)

        def deposit_cash():
            global current_balance
            if int(cash.get()) <= 0:
                messagebox.showerror("TEAM BANK ATM","Invalid amount.")
                deposit_entry.delete(0, END)
            elif int(cash.get()) >= 10000:
                messagebox.showinfo("TEAM BANK ATM"," You can not deposit this amount. "
                                                    "\n You can do this from the nearest branch.")
                deposit_entry.delete(0, END)
            else:
                current_balance += int(cash.get())
                controller.shared_data['Balance'].set(current_balance)
                messagebox.showinfo("TEAM BANK ATM", f" ${int(cash.get())} deposited."
                                                     f"\n You are being redirected to the home page.")
                model.update_balance(current_balance, controller.shared_data['Account'].get())
                controller.show_frame('MenuPage')
                cash.set('')

        enter_button = tk.Button(self,
                                 text='Enter',
                                 command=deposit_cash,
                                 relief='raised',
                                 borderwidth=3,
                                 width=40,
                                 height=3)
        enter_button.pack(pady=10)

        space_label = tk.Label(self, height=2, bg='#364859')
        space_label.pack()

        button_frame = tk.Frame(self, bg='#364859')
        button_frame.pack(fill='both', expand=True)

        escape(button_frame, controller)

class BalancePage(Config):
    def __init__(self, parent, controller):
        Config.__init__(self, parent, controller)
        space_label = tk.Label(self, height=2, bg='#364859')
        space_label.pack()
        heading_label = tk.Label(self,
                                 text='TEAM BANK ATM',
                                 font=('orbitron', 45, 'bold'),
                                 foreground='#ffffff',
                                 background='#364859')
        heading_label.pack(pady=25)

        space_label = tk.Label(self, height=2, bg='#364859')
        space_label.pack()

        global current_balance
        controller.shared_data['Balance'].set(current_balance)
        balance_text_label = tk.Label(self,
                                 text="Current Balance: $ ",
                                 font=('orbitron', 13),
                                 fg='white',
                                 bg='#364859')
        balance_text_label.place(x=273, y=197)
        balance_label = tk.Label(self,
                                 textvariable=controller.shared_data['Balance'],
                                 font=('orbitron', 13),
                                 fg='white',
                                 bg='#364859')
        balance_label.pack(padx=(38,0))

        space_label = tk.Label(self, height=11, bg='#364859')
        space_label.pack()

        img = ImageTk.PhotoImage(Image.open("images/user/money.png").resize((200, 200)))
        teller_label = tk.Label(self,
                                bg='#364859',
                                image=img)
        teller_label.image = img
        teller_label.place(x=330, y=216)

        button_frame = tk.Frame(self, bg='#364859')
        button_frame.pack(fill='both', expand=True)
        escape(button_frame, controller)
