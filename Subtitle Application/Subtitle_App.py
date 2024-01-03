from tkinter import *
import time
from tkinter import filedialog as fd
from tkinter import messagebox

# Text Cleaning
import string
import re


class StopWatch(Frame):
    def __init__(self, parent=None, **kw):
        Frame.__init__(self, parent, kw)
        self.startTime = 0.0
        self.nextTime= 0.0
        self.onRunning = 0
        self.timestr = StringVar()
        self.make_widget()
        self.frame = Frame


    def make_widget(self):
        global  start_button, pause_button, reset_button, quit_button, load_button, \
                words_button, take_back, forward_button, text, timeText
        timeText = Label(self, textvariable = self.timestr, text='00:00:00.000', font=('Arial', 30))
        self.set_time(self.nextTime)
        timeText.pack(pady = 2, padx = (0,500))

        load_button = Button(self, text='load', height=1, width=7, font=('Arial', 10), command=self.load_srt)
        load_button.place(x=245, y=15)
        take_back = Button(self, text='back', height=1, width=7, font=('Arial', 10), command=self.back)
        take_back.place(x=310, y=15)
        start_button = Button(self, text='start', height=1, width=7, font=('Arial', 10), command=self.start)
        start_button.place(x=375, y=15)
        forward_button = Button(self, text='forward',height=1, width=7, font=('Arial', 10), command=self.forward)
        forward_button.place(x=440, y=15)
        pause_button = Button(self, text='pause', height=1, width=7, font=('Arial', 10), command=self.stop)
        pause_button.place(x=505, y=15)
        reset_button = Button(self, text='reset', height=1, width=7, font=('Arial', 10), command=self.reset)
        reset_button.place(x=570, y=15)
        words_button = Button(self, text='word', height=1, width=7, font=('Arial', 10), command=self.word_tokenize)
        words_button.place(x=635, y=15)
        quit_button = Button(self, text='quit', height=1, width=7, font=('Arial', 10), command=quit)
        quit_button.place(x=700, y=15)

        text = Text(self, height=12, width=100)
        text.pack(fill=X, expand=NO, pady = 2, padx = 2)

    def load_srt(self):
        global texts
        import re
        def srt_to_dict(srtText):
            with open(srtText) as f:
                srtText = f.read()
                #Reduce multiple blank lines to single
                srtText = re.sub(r'\n\s*\n', '\n\n', srtText)

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

        filetypes = (('srt files', '*.srt'),)
        f = fd.askopenfile(filetypes=filetypes)
        file = srt_to_dict(f.name)

        started = []
        ended = []
        texts = []
        for idx, subs in enumerate(file):
                    started.append(subs[0])
                    ended.append(subs[1])
                    texts.append(subs[2])
                    text.insert(END, f"{subs[0]} --> {subs[1]}, {subs[2]}\n")

        content_text = Text(self, height=1, width=100)
        content_text.pack(fill=X, expand=NO, pady = 2, padx = 2)
        content_text.config(state="disabled")
        text.config(state="disabled")

        def callback(var, ind, mode):
            for i in range(len(started)):
                if(format(self.timestr.get()) in started[i]):
                    text.pack_forget()
                    app.geometry("800x90")
                    app.attributes("-transparentcolor", app['bg'])

                    widget_config_list = [start_button, pause_button, reset_button, quit_button,
                                          take_back, forward_button, words_button, load_button]
                    for widget in widget_config_list:
                        widget.config(bg="white")

                    timeText.config(fg="white")
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
        load_button['state'] = 'disabled'

    def word_tokenize(self):
        try:
            def decontracted(phrase):
                # specific
                phrase = re.sub(r"won\'t", "will not", phrase)
                phrase = re.sub(r"can\'t", "can not", phrase)
                phrase = re.sub(r"- ", "", phrase)

                # general
                phrase = re.sub(r"n\'t", " not", phrase)
                phrase = re.sub(r"\'re", " are", phrase)
                phrase = re.sub(r"\'s", " is", phrase)
                phrase = re.sub(r"\'d", " would", phrase)
                phrase = re.sub(r"\'ll", " will", phrase)
                phrase = re.sub(r"\'t", " not", phrase)
                phrase = re.sub(r"\'ve", " have", phrase)
                phrase = re.sub(r"\'m", " am", phrase)
                return phrase

            def clean_text(sent):
                sent = decontracted(sent)
                sent = sent[0].lower() + sent[1:]
                sent = sent.translate(str.maketrans('', '', string.punctuation)).split(" ")
                return sent

            tokens = [clean_text(sent) for sent in texts]
            ordered_tokens = set()
            result = []
            for words in tokens:
                for word in words:
                    if word not in ordered_tokens:
                        ordered_tokens.add(word)
                        result.append(word)

            with open('words.txt', 'w', encoding="utf-8") as f:
                for word in result:
                    f.write(f"{word}\n")
            messagebox.showinfo("Subtitle_App", "Tokenizing Done!!!\nYou can find it in 'words.txt'.")
        except:
            messagebox.showwarning("Subtitle_App", "Can not tokenize")


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
        self.timestr.set("{:0>2}:{:0>2}:{:02.0f}".format(int(hours),int(minutes),seconds))


    def back(self):
            if (self.nextTime - 5.0) <= 0:
                self.Reset()
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
    StopWatch = StopWatch(app)
    StopWatch.pack(side=TOP)
    app.title("Subtitle Application")
    app_height = 300
    app_width = 850
    app.geometry(f'{app_width}x{app_height}+{400}+{80}')
    app.resizable(False, False)
    app.mainloop()
