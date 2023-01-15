import datetime
from tkinter import *
import time

class stopwatch(Frame):
    def __init__(self, parent=None, **kw):
        Frame.__init__(self, parent, kw)
        self.startTime = 0.0
        self.nextTime= 0.0
        self.onRunning = 0
        self.timestr = StringVar()
        self.MakeWidget()

    def MakeWidget(self):
        global  start_button, pause_button, reset_button
        timeText = Label(self, textvariable = self. timestr, text='00:00:00.000', font=('Arial', 30))
        self.set_time(self.nextTime)
        timeText.pack(pady = 2, padx = (15,0))

        take_back = Button(self, text='BACKWARD',font=('Arial', 10), command=self.back)
        take_back.pack(side=LEFT,ipadx=10, ipady=9)
        start_button = Button(self, text='START', font=('Arial', 10), command=self.start)
        start_button.pack(side=LEFT,ipadx=10, ipady=9)
        pause_button = Button(self, text='PAUSE', font=('Arial', 10), command=self.stop)
        pause_button.pack(side=LEFT,ipadx=10, ipady=9)
        forward_button = Button(self, text='FORWARD', font=('Arial', 10), command=self.forward)
        forward_button.pack(side=LEFT,ipadx=10, ipady=9)
        reset_button = Button(self, text='RESET', font=('Arial', 10), command=self.reset)
        reset_button.pack(side=LEFT,ipadx=10, ipady=9)
        quit_button = Button(self, text='QUIT', font=('Arial', 10), command=quit)
        quit_button.pack(side=LEFT,ipadx=10, ipady=9)


    def updater(self):
        self.nextTime = time.time() - self.startTime
        self.set_time(self.nextTime)
        self.timer = self.after(50, self.updater)

    def start(self):
        if not self.onRunning:
            self.startTime = time.time() - self.nextTime
            self.updater()
            self.onRunning = 1
            start_button['state'] = 'disabled'
            pause_button['state'] = 'normal'
            reset_button['state'] = 'normal'

    def stop(self):
        if self.onRunning:
            self.after_cancel(self.timer)
            self.nextTime = time.time() - self.startTime
            self.set_time(self.nextTime)
            self.onRunning = 0
            start_button['state'] = 'normal'
            pause_button['state'] = 'disabled'
            reset_button['state'] = 'normal'

    def reset(self):
        start_button['state'] = 'normal'
        pause_button['state'] = 'normal'
        reset_button['state'] = 'normal'
        self.startTime = time.time()
        self.nextTime = 0.0
        self.set_time(self.nextTime)


    def set_time(self, nextElap):
        hours, rem = divmod(nextElap, 3600)
        minutes, seconds = divmod(rem, 60)
        self.timestr.set("{:0>2}:{:0>2}:{:05.3f}".format(int(hours),int(minutes),seconds))

    def back(self):
            if (self.nextTime - 5.0) <= 0:
                self.reset()
            else:
                self.after_cancel(self.timer)
                self.nextTime = self.nextTime - 5.0
                self.set_time(self.nextTime)
                self.onRunning = 0
                start_button['state'] = 'normal'
                pause_button['state'] = 'disabled'
                reset_button['state'] = 'normal'

    def forward(self):
        self.after_cancel(self.timer)
        self.nextTime = self.nextTime + 5.0
        self.set_time(self.nextTime)
        self.onRunning = 0
        start_button['state'] = 'normal'
        pause_button['state'] = 'disabled'
        reset_button['state'] = 'normal'


if __name__ == '__main__':
    app = Tk()
    StopWatch = stopwatch(app)
    StopWatch.pack(side=TOP)
    app.title("STOPWATCH")
    app_height = 100
    app_width = 490
    app.geometry(f'{app_width}x{app_height}+{400}+{80}')
    app.resizable(False, False)
    app.mainloop()

