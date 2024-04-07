from tkinter import *
import math
import winsound

repetition = 0

class Pomodoro(Frame):
    def __init__(self, parent=None, **kw):
        Frame.__init__(self, parent, kw)
        self.current_time = 0
        self.work_time = 25
        self.break_time = 5
        self.cycle = 5
        self.make_widget()
        self.frame = Frame


    def make_widget(self):
        global work_entry, min_entry, timeText, checkmark_label1, checkmark_label2, type_text\
            ,set_work_button, set_break_button, min_entry, work_entry, cycle_entry, cycle_button, \
            start_button, reset_button

        header = Label(self, text="POMODORO", font=('Arial', 30))
        header.pack(pady=20, side=TOP)

        # Widgets to set working minute
        cycle_label = Label(self, text='Cycle Count:', font=('Arial', 12))
        cycle_label.place(x=75, y=300)
        vcmd = (self.register(self.num_only))
        cycle_entry = Entry(self, width=5, justify='center', validate='all', validatecommand=(vcmd, '%P'))
        cycle_entry.place(x=180, y=302)
        cycle_entry.insert(0, "5")
        cycle_entry.bind("<FocusIn>", lambda args: cycle_entry.delete(0, END))

        cycle_button = Button(text="SET", font=('Arial', 10), command=self.set_cycle, width=10, relief=GROOVE)
        cycle_button.place(x=230, y=296)
        self.button_hover(cycle_button)

        # Widgets to set working minute
        work_min = Label(self, text='Work Minute:', font=('Arial', 12))
        work_min.place(x=75, y=350)
        vcmd = (self.register(self.num_only))
        work_entry = Entry(self, width=5, justify='center', validate='all', validatecommand=(vcmd, '%P'))
        work_entry.place(x=180, y=352)
        work_entry.insert(0, "25")
        work_entry.bind("<FocusIn>", lambda args: work_entry.delete(0, END))

        set_work_button = Button(text="SET", font=('Arial', 10), command=self.set_work_timer, width=10, relief=GROOVE)
        set_work_button.place(x=230, y=346)
        self.button_hover(set_work_button)

        # Widgets to set break minute
        break_min = Label(self, text='Break Minute:', font=('Arial', 12))
        break_min.place(x=75, y=400)
        min_entry = Entry(self, width=5, justify='center', validate='all', validatecommand=(vcmd, '%P'))
        min_entry.place(x=180, y=402)
        min_entry.insert(0, "5")
        min_entry.bind("<FocusIn>", lambda args: min_entry.delete(0, END))

        set_break_button = Button(text="SET", font=('Arial', 10), command=self.set_break_time, width=10, relief=GROOVE)
        set_break_button.place(x=230, y=396)
        self.button_hover(set_break_button)

        timeText = Label(self, text='00:00', font=('Arial', 15))
        timeText.place(x=175, y=200)

        start_button = Button(text="START", font=('Arial', 10), command=self.start_timer, width=19, height=2, relief=GROOVE)
        start_button.place(x=30, y=450)
        self.button_hover(start_button)

        reset_button = Button(text="RESET", font=('Arial', 10), command=self.reset, width=19, height=2, relief=GROOVE)
        reset_button.place(x=210, y=450)
        reset_button['state'] = 'disabled'
        self.button_hover(reset_button)

        type_text = Label(self, text='', font=('Arial', 15))
        type_text.place(x=170, y=150)

        checkmark_label1 = Label(self, text="")
        checkmark_label1.place(x=135, y=250)
        checkmark_label2 = Label(self, text="")
        checkmark_label2.place(x=175, y=250)

    def button_hover(self, button):
        button.bind("<Enter>", lambda e: button.config(fg='white', bg='#357EC7'))
        button.bind("<Leave>", lambda e: button.config(fg='black', bg='SystemButtonFace'))


    def state_changing(self, button_list, entry_list, state):
        for btn in button_list:
            btn['state'] = state
        for entry in entry_list:
            entry.config(state=state)

    def num_only(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

    def set_cycle(self):
        if cycle_entry.get() == "":
            self.cycle = 5
        else:
            self.cycle = cycle_entry.get()

    def set_work_timer(self):
        if work_entry.get() == "":
            self.work_time = 25
        else:
            self.work_time = work_entry.get()

    def set_break_time(self):
        if min_entry.get() == "":
            self.break_time = 5
        else:
            self.break_time = min_entry.get()

    def start_countdown(self, count):
        global countdown
        count = int(count)
        if count > 0:
            if count <= 3600:
                count -= 1
                minutes, seconds = divmod(count, 60)
                countdown = self.after(1000, self.start_countdown, count)
                timeText.config(text=f"{minutes:02d}:{seconds:02d}")
            else:
                count -= 1
                hours, rem = divmod(count, 3600)
                minutes, seconds = divmod(rem, 60)
                self.after(1000, self.start_countdown, count)
                timeText.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        else:
            if repetition % 2 == 0:
                work_sess = math.floor(repetition / 2)
                checkmark_label1.config(text="CYCLE: ")
                checkmark_label2.config(text='✅' * work_sess, fg='SpringGreen3')
                if work_sess == int(self.cycle):
                    print(work_sess, self.cycle)
                    return self.reset()
            self.start_timer()

    def start_timer(self):
        global repetition
        work_time = self.work_time
        break_time = self.break_time
        if repetition%2==0:
            self.start_countdown(int(work_time)*60)
            type_text.config(text="WORK")
            winsound.Beep(852 , 1000)
        else:
            self.start_countdown(int(break_time)*60)
            type_text.config(text="BREAK")
            winsound.Beep(852, 1000)
        repetition += 1
        reset_button['state'] = 'normal'
        self.state_changing(button_list=[set_work_button, set_break_button, cycle_button, start_button],
                            entry_list=[min_entry, work_entry, cycle_entry],
                            state='disabled')

    def reset(self):
        global repetition
        repetition = 0
        self.current_time = 0
        self.after_cancel(countdown)
        checkmark_label1.config(text='')
        checkmark_label2.config(text='')
        timeText.config(text="00:00")
        type_text.config(text="")
        self.state_changing(button_list=[set_work_button, set_break_button, cycle_button, start_button],
                            entry_list=[min_entry, work_entry, cycle_entry],
                            state='normal')


if __name__ == '__main__':
    app = Tk()
    StopWatch = Pomodoro(app)
    StopWatch.pack(side="top", fill="both", expand=True)
    app.title("Pomodoro")
    app_height = 550
    app_width = 400
    app.geometry(f'{app_width}x{app_height}+{500}+{80}')
    app.resizable(False, False)
    app.mainloop()