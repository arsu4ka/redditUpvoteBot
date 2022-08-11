import tkinter
import tkinter.filedialog
import customtkinter
import os
from reddit.connection import run

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")


class App(customtkinter.CTk):

    WIDTH = 1050
    HEIGHT = 300

    def __init__(self, *args, fg_color="default_theme", **kwargs):
        super().__init__(*args, fg_color=fg_color, **kwargs)

        # variables to know where to take input from

        self.fromFile = True
        self.filePath = None

        # configuring tkinter window

        self.title("Reddit Upvote Bot")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WB_DELETE_WINDOW", self.on_closing)

        self.grid_columnconfigure(0, weight=1)  
        self.grid_rowconfigure(0, weight=1)

        # creating main frame
        self.frame = customtkinter.CTkFrame(master=self)
        self.frame.grid(row=0, column=0, sticky='nswe', padx=20, pady=20)

        # creating three additional frames in main frame
        self.frame.grid_rowconfigure(2)
        self.frame.grid_columnconfigure(2)

        self.frameMid = customtkinter.CTkFrame(master=self.frame)
        self.frameMid.grid(row=0, column=1, sticky='nswe')

        self.frameLeft = customtkinter.CTkFrame(master=self.frame)
        self.frameLeft.grid(row=0, column=0, pady=10, padx=10)

        self.frameRight = customtkinter.CTkFrame(master=self.frame)
        self.frameRight.grid(row=0, column=2, pady=10, padx=10)

        # configuring elements on main frame (under additional frames)

        self.linkEntry = customtkinter.CTkEntry(master=self.frame, width=400, placeholder_text="Entry link to reddit post here...")
        self.linkEntry.grid(row=1, column=1, pady=20, padx=20)

        self.runBtn = customtkinter.CTkButton(master=self.frame, text="RUN", command=self.on_run)
        self.runBtn.grid(row=2, column=1, pady=30)

        # configuring left additional frame

        self.fileLabel = customtkinter.CTkLabel(master=self.frameLeft, text="Get Account From File")
        self.fileBtn = customtkinter.CTkButton(master=self.frameLeft, text="Browse .txt file", command=self.browse_txt)
        self.addTxtLabel = customtkinter.CTkLabel(master=self.frameLeft, text="username:password:host:port", width=200)

        self.fileLabel.pack()
        self.fileBtn.pack()
        self.addTxtLabel.pack()

        # configuring middle additional frame

        self.directionLbl = customtkinter.CTkLabel(master=self.frameMid, text=" <<< ")
        self.switchChoice = customtkinter.CTkButton(master=self.frameMid, text="Switch Input Mode", command=self.switch_choice)
        self.directionLbl.pack()
        self.switchChoice.pack()

        # configuring right additional frame

        self.fileLabel = customtkinter.CTkLabel(master=self.frameRight, text="Input Account Credentials")
        self.entry = customtkinter.CTkEntry(master=self.frameRight, width=300)
        self.addTxtLabel = customtkinter.CTkLabel(master=self.frameRight, text="username:password:host:port")

        self.fileLabel.pack()
        self.entry.pack()
        self.addTxtLabel.pack()    
        
    def switch_choice(self):
        if self.fromFile:
            self.directionLbl.configure(text=" >>> ")
            self.fromFile = False
            self.filePath = None
            return
        self.directionLbl.configure(text=" <<< ")
        self.fromFile = True

    def on_run(self):
        if self.fromFile:
            data = self.filePath
        else:
            data = self.entry.get()
        print(data)
        run(
            fromFile=self.fromFile,
            data=data,
            reddit_post=self.linkEntry.get()
        )

    def browse_txt(self):
        if self.fromFile:
            self.filePath = tkinter.filedialog.askopenfilename(
                title="Open txt file",
                initialdir=os.getcwd(),
                filetypes = (("Text files","*.txt*"),("all files","*.*"), ("Text files","*.txt")))
        else:
            print("Your current input choice doesn't allow you to browse file!")

    def on_closing(self, event=0):
        self.destoy()