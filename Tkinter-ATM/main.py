from User import *
from Teller import *

class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.shared_data = {'Balance':tk.IntVar(),
                            'Account':tk.IntVar(),
                            'Name': tk.StringVar(),
                            }

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        from Teller import TellerMenuPage, TellerAddCustomer

        self.frames = {}
        for F in (StartPage, MenuPage, WithdrawPage, DepositPage, BalancePage,
                  TellerMenuPage, TellerAddCustomer):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = SampleApp()
    app.iconbitmap('images/common/icon.ico')
    app_height = 650
    app_width = 850
    app.title("TEAM BANK ATM")
    app.geometry(f'{app_width}x{app_height}+{400}+{80}')
    app.resizable(False, False)
    app.mainloop()