from tkinter import *
from tkinter import ttk


class TextTab(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # variables
        self.tabs: dict[str: Text] = {}
        self.activetab = "default"
        
        # change variables
        for k, v in kwargs.setdefault("attrs", {}).items():
            self.__setattr__(k, v)
        
        # create widgets
        self.header = Frame(self, height=30, width=self.winfo_width() - 1)
        self.tabframe = Frame(self)
        self.createtab(self.activetab)
        self.createtab("n2")
        
        # pack widgets
        self.header.pack(fill=X, side=TOP)
        self.tabframe.pack(fill=BOTH, expand=True, side=BOTTOM)
        
        self.update()

    def createtab(self, name):
        self.tabs[name] = Text(self.tabframe)

    def update(self):
        for i in self.tabs.values():
            i.pack_forget()
        
        try:
            self.tabs[self.activetab].pack(fill=BOTH, expand=True)
        except KeyError:
            self.tabs[list(self.tabs.keys())[0]].pack(fill=BOTH, expand=True)
        
        for i in self.header.children.copy().values():
            i.destroy()
        
        for i in self.tabs.keys():
            b = ttk.Button(self.header, text=i, command=lambda *a: (self.__setattr__(self.activetab, i), self.update()))
            b.pack(side=RIGHT)
            
        super().update()
        

if __name__ == "__main__":
    root = Tk()
    f = TextTab(root)
    f.pack()
    print(dir(f))
    root.mainloop()
    