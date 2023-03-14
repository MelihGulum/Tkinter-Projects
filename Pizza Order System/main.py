import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import messagebox
from datetime import datetime
import csv

from pizza import *
from sauce import *

italian_pizza = {"Pizza Napoletana": PizzaNapoletana, "Pizza Capricciosa": PizzaCapricciosa,
                 "Pizza Quattro Formaggi": PizzaQuattroFormaggi,
                 "Sardenara": Sardenara, "Pizza Margherita": PizzaMargherita}

normal_pizza = ['Classic', 'Turk Pizza', 'Regular Pizza']
sauces = {"Ketchup": Ketchup, "Mayonnaise": Mayonnaise, "Mustard": Mustard, "Ranch": Ranch}

def enter_only_digits(entry, action_type) -> bool:
    if action_type == '1' and not entry.isdigit():
        return False
    return True

class MainView(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, SecondPage):
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self,  parent, controller):
        tk.Frame.__init__(self,  parent)
        self.controller = controller

        img = ImageTk.PhotoImage(Image.open('images/Pizzaland.png').resize((250, 250), Image.ANTIALIAS))
        label1 = tk.Label(self, image=img)
        label1.image = img
        label1.place(x="200",y="30")

        def menus():
            newWindow = tk.Toplevel()
            newWindow.title("PizzaLand")
            newWindow.geometry(f'{650}x{340}+{350}+{80}')
            newWindow.resizable(False, False)
            newWindow.iconbitmap('images/Pizzaland.ico')
            upper_container = tk.Frame(newWindow)
            upper_container.pack()

            pizza_columns = ('PIZZA', 'COST')
            pizza_menu = [("Classic", "30"), ("Turk Pizza", "35"), ("Regular Pizza", "30"),
                          ("Napoletana", "60"), ("Pizza Capricciosa", "60"), ("Pizza Quattro Formaggi", "60"),
                          ("Sardenara", "60"), ("Pizza Margherita", "40")]

            left_tree = ttk.Treeview(upper_container, columns=pizza_columns, show='headings', height=10)
            left_tree.heading('PIZZA', text='PIZZA')
            left_tree.heading('COST', text='COST')
            left_tree.column("PIZZA", anchor=tk.W, minwidth=150, width=150, stretch=tk.NO)
            left_tree.column("COST", anchor=tk.CENTER, minwidth=150, width=150, stretch=tk.NO)

            for menu in pizza_menu:
                left_tree.insert('', tk.END, values=menu)
            left_tree.pack(side=tk.LEFT)

            ingredients_column = ('INGREDIENT', 'COST')
            ingredients_menu = [("Black Olives", "2"), ("Mushrooms", "6"), ("Meat", "10"),
                                ("Onion", "2"), ("Corn", "2"), ("Mozzarella", "8"),
                                ("Tomatoes", "3"), ("Parmesan", "7"), ("Basil", "2"),
                                ("San Marzano Tomatoes", "4"), ("Tomato Sauce", "3"),
                                ("Gorgonzola", "4"), ("Parmigiano Reggiano", "4"),
                                ("Goat Cheese", "4"), ("Sardines", "10"), ("Red Onions", "3"),
                                ("Prosciutto Cotto (ham)", "6"), ("Parsley", "3")]

            right_tree = ttk.Treeview(upper_container, columns=ingredients_column, show='headings')
            right_tree.heading('INGREDIENT', text='INGREDIENT')
            right_tree.heading('COST', text='COST')
            right_tree.column("INGREDIENT", anchor=tk.W, minwidth=150, width=150, stretch=tk.NO)
            right_tree.column("COST", anchor=tk.CENTER, minwidth=150, width=150, stretch=tk.NO)

            for menu in ingredients_menu:
                right_tree.insert('', tk.END, values=menu)
            right_tree.pack(side=tk.LEFT)

            sauces_menu = [("Ketchup", "1"), ("Mayonnaise", "2"),
                           ("Mustard", "3"), ("Ranch", "3")]
            sauces_column = ("SAUCE", "COST")
            lower_tree = ttk.Treeview(newWindow, columns=sauces_column, show='headings', height=5)
            lower_tree.heading('SAUCE', text='SAUCE')
            lower_tree.heading('COST', text='COST')
            lower_tree.column("SAUCE", anchor=tk.W, minwidth=150, width=150, stretch=tk.NO)
            lower_tree.column("COST", anchor=tk.CENTER, minwidth=150, width=150, stretch=tk.NO)

            for menu in sauces_menu:
                lower_tree.insert('', tk.END, values=menu)
            lower_tree.pack()

        menu_button =tk.Button(self,
                                text='MENU',
                                command=menus,
                                font=('Arial', 10),
                                width=20,
                                height=3,
                                activebackground="#caeffa")
        menu_button.place(x="250",y="350")

        order_button =tk.Button(self,
                                text='ORDER',
                                command=lambda : controller.show_frame("SecondPage"),
                                font=('Arial', 10),
                                width=20,
                                height=3,
                                activebackground="#caeffa")
        order_button.place(x="250",y="450")

        exit_button =tk.Button(self,
                               text='EXIT',
                               command=lambda : app.destroy(),
                               font=('Arial', 10),
                               width=20,
                               height=3,
                               activebackground="#caeffa")
        exit_button.place(x="250",y="550")

        v1_space_label = tk.Label(self, height=20,width=2, bg='#364859')
        v1_space_label.place(x="100",y="330")
        v2_space_label = tk.Label(self, height=20,width=2, bg='#364859')
        v2_space_label.place(x="548",y="330")

        h1_space_label = tk.Label(self, width=66, bg='#364859')
        h1_space_label.place(x="100",y="310")
        h2_space_label = tk.Label(self, width=66, bg='#364859')
        h2_space_label.place(x="100",y="628")


class SecondPage(tk.Frame):
    def __init__(self,   parent, controller):
        tk.Frame.__init__(self,  parent)
        self.controller = controller

        vcmd = (self.register(enter_only_digits), '%P', '%d')

        def pizza_section():
            global pizza_frame
            pizza_frame =tk.LabelFrame(self, text="Choose Pizza",padx=62, pady=10)
            pizza_frame.grid(row=0, column=0, padx=20, pady=10)

            pizza_type = tk.StringVar()
            pizza_label = tk.Label(pizza_frame, text="Pizza")
            pizza_label.grid(row=0, column=0, sticky="W")
            pizza_combobox = ttk.Combobox(pizza_frame,
                                          values=["Classic", "Turk Pizza", "Regular Pizza",
                                                        "Pizza Napoletana", "Pizza Capricciosa",
                                                        "Pizza Quattro Formaggi", "Sardenara",
                                                        "Pizza Margherita"],
                                          textvariable=pizza_type)
            pizza_combobox.grid(row=0, column=1,sticky="NEWS")

            def restrict_ing(*args):
                y = pizza_type.get()

                if y in italian_pizza.keys():
                    for widget in ingredients_frame.winfo_children():
                        widget.configure(state='disabled')
                    for widgets in sauce_frame.winfo_children():
                        widgets.configure(state='disabled')
                else:
                    for widget in ingredients_frame.winfo_children():
                        widget.configure(state='normal')
                    for widgets in sauce_frame.winfo_children():
                        widgets.configure(state='normal')

            pizza_type.trace("w", restrict_ing)

            pizza_quantity = tk.Label(pizza_frame, text="Quantity")
            pizza_quantity.grid(row=1, column=0, sticky="W")
            pizza_quantity_entry = tk.Entry(pizza_frame,width=60,validate='key', validatecommand=vcmd)
            pizza_quantity_entry.grid(row=1, column=1, sticky="NEWS")

            for widget in pizza_frame.winfo_children():
                widget.grid_configure(padx=26, pady=5)

            return pizza_combobox, pizza_quantity_entry

        def ingredient_section():
            global ingredients_frame
            ingredients_frame = tk.LabelFrame(self, text="Ingredients",padx=2,pady=10)
            ingredients_frame.grid(row=1, column=0, padx=20, pady=10)

            ing_array = ('Meat', 'Onion', 'Mushrooms', 'Black Olives', 'Goat Cheese', 'San Marzano Tomatoes',
                         'Mozzarella', 'Tomatoes', 'Parmesan', 'Basil', 'Corn', 'Tomato Sauce',
                         'Gorgonzola', 'Parmigiano Reggiano', 'Sardines', 'Red Onions', 'Parsley', 'Prosciutto Cotto (ham)')

            checkboxes = {}
            c = c2 = c3 = 0

            for Checkbox,i in enumerate(ing_array):
                name = ing_array[Checkbox]
                current_var = tk.IntVar()
                current_box = tk.Checkbutton(ingredients_frame, text=name, variable=current_var)
                current_box.var = current_var

                if Checkbox < 5:
                    current_box.grid(row=0 ,column=Checkbox , sticky="w")
                elif  5 <= Checkbox <=9:
                    current_box.grid(row=1 ,column=c, sticky="w")
                    c += 1
                elif 10 <= Checkbox <= 14:
                    current_box.grid(row=2 ,column=c2, sticky="w")
                    c2 += 1
                else:
                    current_box.grid(row=3, column=c3, sticky="w")
                    c3 += 1

                checkboxes[current_box] = name  # so checkbutton object is the key and value is string

            for widget in ingredients_frame.winfo_children():
                widget.grid_configure(pady=5)
            return checkboxes

        def sauce_section():
            global sauce_frame
            sauce_frame = tk.LabelFrame(self, text="Sauce", padx=70, pady=10)
            sauce_frame.grid(row=2, column=0, padx=20, pady=10)

            sauces = (('Ketchup', 'Ketchup'),
                     ('Mayonnaise', 'Mayonnaise'),
                     ('Ranch', 'Ranch'),
                     ('Mustard', 'Mustard'))

            selected_sauce = tk.StringVar(value="Ketchup")

            for row_index, row in enumerate(sauces):
                r = tk.Radiobutton(sauce_frame, text=row[0], value=row[1], variable=selected_sauce)
                r.grid(row=0, column=row_index)

            sauce_quantity = tk.Label(sauce_frame, text="Quantity")
            sauce_quantity.grid(row=1, column=0, sticky="W")
            sauce_quantity_entry = tk.Entry(sauce_frame, width=60,validate='key', validatecommand=vcmd)
            sauce_quantity_entry.grid(row=1, column=1,columnspan=5)

            for widget in sauce_frame.winfo_children():
                widget.grid_configure(padx=17,pady=5)

            return selected_sauce, sauce_quantity_entry

        def user_info():
            global user_info_frame
            user_info_frame = tk.LabelFrame(self, text="User Information", padx=70, pady=10)
            user_info_frame.grid(row=3, column=0, padx=20, pady=10)

            full_name_label = tk.Label(user_info_frame, text="Full Name: ")
            full_name_label.grid(row=0, column=0, sticky="W")
            full_name_entry = tk.Entry(user_info_frame, width=60)
            full_name_entry.grid(row=0, column=1)

            user_id_label = tk.Label(user_info_frame, text="ID: ")
            user_id_label.grid(row=1, column=0, sticky="W")
            user_id_entry = tk.Entry(user_info_frame, width=60, validate='key', validatecommand=vcmd)
            user_id_entry.grid(row=1, column=1)

            credit_card_label = tk.Label(user_info_frame, text="Credit Card: ")
            credit_card_label.grid(row=2, column=0, sticky="W")
            credit_card_entry = tk.Entry(user_info_frame, width=60, validate='key', validatecommand=vcmd)
            credit_card_entry.grid(row=2, column=1)

            password_label = tk.Label(user_info_frame, text="Password: ")
            password_label.grid(row=3, column=0, sticky="W")
            password_entry = tk.Entry(user_info_frame, width=60, validate='key', validatecommand=vcmd)
            password_entry.grid(row=3, column=1)

            for widget in user_info_frame.winfo_children():
                widget.grid_configure(padx=17, pady=5)
            return full_name_entry, user_id_entry, credit_card_entry, password_entry

        pizza_name, pizza_q = pizza_section()
        checkboxes = ingredient_section()
        sauce_name, sauce_q = sauce_section()
        user_name, user_id, credit_card, password = user_info()

        def get_order():
            #XOR
            validate = (bool(pizza_name.get())  ^ bool(pizza_q.get()) ^ bool(user_name.get())^
                     bool(user_id.get()) ^ bool(credit_card.get()) ^ bool(password.get()) )
            validate_true = (bool(pizza_name.get())  , bool(pizza_q.get()) , bool(user_name.get()),
                     bool(user_id.get()) , bool(credit_card.get()) , bool(password.get()) ).count(True)

            if validate:
                messagebox.showinfo("PizzaLand", "Please Provide The Information ")
            #XNOR
            elif not validate:
            #if specific number of inputs is True and equal to 6
                if validate_true == 6:
                    output = []
                    now = datetime.now()
                    for box in checkboxes:
                        if box.var.get() == 1:
                            output.append(checkboxes[box])
                    if pizza_name.get() in italian_pizza.keys():
                        pizza = italian_pizza[pizza_name.get()](name=pizza_name.get(), ingredients=None, quantity=int(pizza_q.get()))
                        desc = pizza.get_description()
                        cost = pizza.get_cost()
                        ing = None
                        sauce_quant = None
                    elif pizza_name.get() in normal_pizza:
                        ing = output
                        if sauce_q.get():
                            sauce_quant = sauce_q.get()
                            pizza = sauces[sauce_name.get()](Pizza(name=pizza_name.get(), ingredients=ing, quantity=int(pizza_q.get())),
                                                         quantity=int(sauce_quant))
                            desc = pizza.get_description()
                            cost = pizza.get_cost()
                        else:
                            pizza = Pizza(name=pizza_name.get(), ingredients=ing, quantity=int(pizza_q.get()))
                            desc = pizza.get_description()
                            cost = pizza.get_cost()
                            sauce_quant = None
                    else:pass

                    msg = messagebox.askquestion("PizzaLand", f"You ordered {desc}\n"
                                                        f"Total: ${cost}\n"
                                                            "Complete the order?")
                    if msg == 'yes':
                        inputs = [pizza_name, pizza_q, sauce_q, user_name, user_id, credit_card, password]

                        order_date = now.strftime("%d/%m/%Y")
                        order_time = now.strftime("%H:%M:%S")
                        ing = ', '.join([str(i) for i in ing]) if ing != None else 'None'
                        sauce_quant = sauce_quant if sauce_quant != None else 'None'
                        header = ["Full Name", "User ID", "Credit Card", "Password", "Order Date",
                              "Order Time", "Desc", "Cost", "Quantity of Pizza", "Ingredients", "Sauce Quantity"]
                        data = [user_name.get(), user_id.get(), credit_card.get(), password.get(), order_date,
                            order_time, desc, cost, pizza_q.get(), ing, sauce_quant]

                        with open('Orders_Database.csv', 'a',newline='') as file:
                            writer = csv.writer(file)
                            if file.tell() == 0:
                                writer.writerow(header)
                            writer.writerow(data)

                        for i in inputs:
                            i.delete(0, tk.END)
                            sauce_name.set(value='Ketchup')
                    else:
                        pass
                else:
                    messagebox.showinfo("PizzaLand", "Please Provide The Information ")
            else:
                 messagebox.showinfo("PizzaLand", "Please Provide The Information ")

        go_back_button = tk.Button(self,
                                   text='GO BACK',
                                   command= lambda: controller.show_frame("StartPage"),
                                   font=('Arial', 10),
                                   width=10,
                                   height=1,
                                   activebackground="#caeffa")
        go_back_button.place(x="200",y="630")

        order_button =tk.Button(self,
                                text='ORDER',
                                command=get_order,
                                font=('Arial', 10),
                                width=10,
                                height=1,
                                activebackground="#caeffa")
        order_button.place(x="350",y="630")

if __name__ == '__main__':
    app = MainView()
    app.iconbitmap('images/PizzaLand.ico')
    app.title("PizzaLand")
    app_height = 670
    app_width = 675
    app.geometry(f'{app_width}x{app_height}+{400}+{32}')
    app.resizable(False, False)
    app.mainloop()