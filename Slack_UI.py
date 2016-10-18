import Tkinter

class Slack_App(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()
        label = Tkinter.Label(self,text="Enter the URL",
                              anchor="w",fg="black")
        label.grid(column=0,row=0,sticky='EW')
        self.entry = Tkinter.Entry(self, width = 100)
        self.entry.grid(column=1,row=0,sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        v = Tkinter.StringVar()
        v.set("1")
        rButton = Tkinter.Radiobutton(self,text = "MS SharePoint", variable=v,
                                      value=1)
        rButton.grid(column=1,row=1)
        rButton = Tkinter.Radiobutton(self,text = "MS Excel", variable=v,
                                      value=2)
        rButton.grid(column=1,row=2)
        rButton = Tkinter.Radiobutton(self,text = "Database", variable=v,
                                      value=3)
        rButton.grid(column=1,row=3)
        
        button = Tkinter.Button(self,text=u"Click me !",
                                command=self.OnButtonClick)
        button.grid(column=1,row=4)

        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelVariable,
                              anchor="w",fg="white",bg="blue")
        label.grid(column=0,row=5,columnspan=2,sticky='EW')

        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)

    def OnButtonClick(self):
        self.labelVariable.set("You clicked the button !")

    def OnPressEnter(self,event):
        self.labelVariable.set("You pressed enter !")


if __name__ == "__main__":
    app = Slack_App(None)
    app.iconbitmap(r'C:\Python27\Slack_Proj\theft-bot.ico')
    app.title('Bot Engine!!')
    app.mainloop()
