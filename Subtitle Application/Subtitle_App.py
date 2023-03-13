from tkinter import *
import time
from tkinter import filedialog as fd


class stopwatch(Frame):
    def __init__(self, parent=None, **kw):
        Frame.__init__(self, parent, kw)
        self.startTime = 0.0
        self.nextTime= 0.0
        self.onRunning = 0
        self.timestr = StringVar()
        self.MakeWidget()
        self.frame = Frame


    def MakeWidget(self):
        global  start_button, pause_button, reset_button
        timeText = Label(self, textvariable = self.timestr, text='00:00:00.000', font=('Arial', 30))
        self.SetTime(self.nextTime)
        timeText.pack(pady = 2, padx = (0,250))

        take_back = Button(self, text='back', height=1, width=7, font=('Arial', 10), command=self.back)
        take_back.place(x=375, y=15)
        start_button = Button(self, text='start', height=1, width=7, font=('Arial', 10), command=self.Start)
        start_button.place(x=440, y=15)
        forward_button = Button(self, text='forward',height=1, width=7, font=('Arial', 10), command=self.forward)
        forward_button.place(x=505, y=15)
        pause_button = Button(self, text='pause', height=1, width=7, font=('Arial', 10), command=self.stop)
        pause_button.place(x=570, y=15)
        reset_button = Button(self, text='reset', height=1, width=7, font=('Arial', 10), command=self.Reset)
        reset_button.place(x=635, y=15)
        quit_button = Button(self, text='quit', height=1, width=7, font=('Arial', 10), command=quit)
        quit_button.place(x=700, y=15)

        import re
        def srt_to_dict(srtText):
            with open(srtText) as f:
                srtText = f.read()
            subs = []
            for s in re.sub('\r\n', '\n', srtText).split('\n\n'):
                st = s.split('\n')
                if len(st) >= 3:
                    split = st[1].split(' --> ')
                    subs.append([(split[0].strip().replace(",", ".")),
                                 (split[1].strip().replace(",", ".")),
                                ' '.join(j for j in st[2:len(st)]).replace("â™ª ", "♪ ")
                                 ])
            with open('subtitle.txt', 'w',encoding="utf-8") as f:
                for line in subs:
                    f.write(f"{line}\n")

            return subs

        text = Text(self, height=12, width=100)
        text.pack(fill=X, expand=NO, pady = 2, padx = 2)

        filetypes = (('srt files', '*.srt'),)
        f = fd.askopenfile(filetypes=filetypes)
        file = srt_to_dict(f.name)

        started =[]
        ended= []
        texts = []
        for i in range(len(file)):
                    started.append(file[i][0])
                    ended.append(file[i][1])
                    texts.append(file[i][2])
                    start = file[i][0]
                    end = file[i][1]
                    texted = file[i][2]
                    text.insert(END, f"{start} --> {end}, {texted}\n")
        content_text = Text(self, height=1, width=100)
        content_text.pack(fill=X, expand=NO, pady = 2, padx = 2)
        content_text.config(state="disabled")
        text.config(state="disabled")

        def callback(var, ind, mode):
            for i in range(len(started)):
                if(format(self.timestr.get()) in started[i]):
                    text.pack_forget()
                    app.geometry("800x90")
                    app.attributes("-transparentcolor",app['bg'])
                    timeText.config(fg="white")
                    start_button.config(bg="white")
                    pause_button.config(bg="white")
                    reset_button.config(bg="white")
                    quit_button.config(bg="white")
                    take_back.config(bg="white")
                    forward_button.config(bg="white")
                    content_text.config(state="normal")
                    content_text.config(height=3,font=("Segoe UI",14,"bold"), fg="black")
                    app.attributes("-alpha",0.3)
                    content_text.insert("1.0", f"{texts[i]}\n")
                elif format(self.timestr.get()) in ended[i]:
                    content_text.delete("1.0", END)
                    if ended[i] == ended[-1]:
                        import time
                        time.sleep(3)
                        app.destroy()
                else:
                    pass
        self.timestr.trace_add('write', callback)

    def Updater(self):
        self.nextTime = time.time() - self.startTime
        self.SetTime(self.nextTime)
        self.timer = self.after(50, self.Updater)

    def Start(self):
        if not self.onRunning:
            self.startTime = time.time() - self.nextTime
            self.Updater()
            self.onRunning = 1
            start_button['state'] = 'disabled'
            pause_button['state'] = 'normal'
            reset_button['state'] = 'normal'

    def stop(self):
        if self.onRunning:
            self.after_cancel(self.timer)
            self.nextTime = time.time() - self.startTime
            self.SetTime(self.nextTime)
            self.onRunning = 0
            start_button['state'] = 'normal'
            pause_button['state'] = 'disabled'
            reset_button['state'] = 'normal'

    def Reset(self):
        start_button['state'] = 'normal'
        pause_button['state'] = 'normal'
        reset_button['state'] = 'normal'
        self.startTime = time.time()
        self.nextTime = 0.0
        self.SetTime(self.nextTime)

    def SetTime(self, nextElap):
        hours, rem = divmod(nextElap, 3600)
        minutes, seconds = divmod(rem, 60)
        self.timestr.set("{:0>2}:{:0>2}:{:02.0f}".format(int(hours),int(minutes),seconds))

    def back(self):
            if (self.nextTime - 5.0) <= 0:
                self.Reset()
            else:
                self.after_cancel(self.timer)
                self.nextTime = self.nextTime - 5.0
                self.SetTime(self.nextTime)
                self.onRunning = 0
                start_button['state'] = 'normal'
                pause_button['state'] = 'disabled'
                reset_button['state'] = 'normal'

    def forward(self):
        self.after_cancel(self.timer)
        self.nextTime = self.nextTime + 5.0
        self.SetTime(self.nextTime)
        self.onRunning = 0
        start_button['state'] = 'normal'
        pause_button['state'] = 'disabled'
        reset_button['state'] = 'normal'

if __name__ == '__main__':
    app = Tk()
    StopWatch = stopwatch(app)
    StopWatch.pack(side=TOP)
    app.title("Subtitle Application")
    app_height = 400
    app_width = 850
    app.geometry(f'{app_width}x{app_height}+{400}+{80}')
    app.resizable(False, False)
    app.mainloop()

