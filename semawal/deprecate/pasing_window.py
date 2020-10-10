#!/usr/bin/python
# -*- coding=utf-8 -*-

#WARNING! deprecated at version 0.2, replaced by a web interface.

import tkinter as Tk
from ..node import Node
from ..net import Net
from .csv_parser import parser

########################################################################
class OtherFrame(Tk.Toplevel):
    init_p = True
    #----------------------------------------------------------------------
    def __init__(self, original, net):
        """Constructor"""
        
        self.net = net
        OPTIONS = net.getNodeskeys()

        self.original_frame = original
        Tk.Toplevel.__init__(self)
        self.title("Sementic network")

        hdlbl = Tk.Label(self, text="Network '" + net.value + "': " + str(len(net.nodes)) + " Nodes") 
        hdlbl.config(font=("Segoe UI BOLD", 13))
        hdlbl.grid(row=0, column=0, padx=(1, 00), pady=(5,5)) 

        left = Tk.Frame(self, borderwidth=0, relief="solid")
        right = Tk.Frame(self, borderwidth=0, relief="solid")
        left.grid(row=1, column=0, columnspan=7)
        right.grid(row=1, column=7, columnspan=7)
                 

        lbl = Tk.Label(left, text="The functions area:") 
        lbl.config(font=("Segoe UI", 11))
        lbl.grid(row=0, column=0, padx=(00, 00), pady=(0,0)) 

        #-------------#-------------
        stepOne = Tk.LabelFrame(left, text=" Node functions: ")
        stepOne.grid(row=1, columnspan=27, sticky='W', \
                 padx=15, pady=15, ipadx=15, ipady=15)

        #-------------
        inFileLbl = Tk.Label(stepOne, text="Select a node 1:")
        inFileLbl.grid(row=0, column=0, sticky='E', padx=(0,5), pady=2)

        variable = Tk.StringVar(stepOne)
        variable.set(OPTIONS[0])

        w = Tk.OptionMenu(stepOne, variable, *OPTIONS)
        w.grid(row=0, column=1, columnspan=7, sticky="WE", pady=3)

        showlinks = Tk.Button(stepOne, text="Show links")
        showlinks.grid(row=0, column=8, sticky='W', padx=(0,5), pady=2)
        #-------------
        inFileLb2 = Tk.Label(stepOne, text="Select a node 1:")
        inFileLb2.grid(row=1, column=0, sticky='E', padx=(0,5), pady=2)

        variable1 = Tk.StringVar(stepOne)
        variable1.set(OPTIONS[0])

        w1 = Tk.OptionMenu(stepOne, variable1, *OPTIONS)
        w1.grid(row=1, column=1, columnspan=7, sticky="WE", pady=3)

        showcnx = Tk.Button(stepOne, text="Show connections")
        showcnx.grid(row=1, column=8, sticky='W', padx=(0,5), pady=2)
        #-------------
        inFileLb3 = Tk.Label(stepOne, text="Select a node 1:")
        inFileLb3.grid(row=2, column=0, sticky='E', padx=(0,5), pady=2)

        variable2 = Tk.StringVar(stepOne)
        variable2.set(OPTIONS[0])

        w2 = Tk.OptionMenu(stepOne, variable2, *OPTIONS)
        w2.grid(row=2, column=1, columnspan=7, sticky="WE", pady=3)

        inFileLb4 = Tk.Label(stepOne, text="Select a node 2:")
        inFileLb4.grid(row=2, column=8, sticky='E', padx=(0,5), pady=2)

        variable3 = Tk.StringVar(stepOne)
        variable3.set(OPTIONS[0])

        w3 = Tk.OptionMenu(stepOne, variable3, *OPTIONS)
        w3.grid(row=2, column=9, columnspan=7, sticky="WE", pady=3)

        showrelations = Tk.Button(stepOne, text="Show relations")
        showrelations.grid(row=2, column=16, sticky='W', padx=(0,0), pady=2)
        #-------------
        inFileLb5 = Tk.Label(stepOne, text="Select a node 1:")
        inFileLb5.grid(row=3, column=0, sticky='E', padx=(0,5), pady=2)

        variable4 = Tk.StringVar(stepOne)
        variable4.set(OPTIONS[0])

        w4 = Tk.OptionMenu(stepOne, variable4, *OPTIONS)
        w4.grid(row=3, column=1, columnspan=7, sticky="WE", pady=3)

        inFileLb6 = Tk.Label(stepOne, text="Select a node 2:")
        inFileLb6.grid(row=3, column=8, sticky='E', padx=(0,5), pady=2)

        variable5 = Tk.StringVar(stepOne)
        variable5.set(OPTIONS[0])

        w5 = Tk.OptionMenu(stepOne, variable5, *OPTIONS)
        w5.grid(row=3, column=9, columnspan=7, sticky="WE", pady=3)


        inFileLb7 = Tk.Label(stepOne, text="Insert the relation:")
        inFileLb7.grid(row=3, column=16, sticky='E', padx=(0,5), pady=2)
        e = Tk.Entry(stepOne)
        e.grid(row=3, column=17, columnspan=3, sticky="WE", padx=(0,5))

        showrelations = Tk.Button(stepOne, text="Answer question")
        showrelations.grid(row=3, column=20, sticky='W', padx=(0,0), pady=2)
        
        
        #-------------#-------------
        stepTwo = Tk.LabelFrame(left, text=" Network functions: ")
        stepTwo.grid(row=2, columnspan=27, sticky='W', \
                 padx=15, pady=15, ipadx=15, ipady=15)

        #-------------
        randomsearch = Tk.Button(stepTwo, text="Random search", command=self.randomSearch)
        randomsearch.grid(row=0, column=0, sticky='W', padx=(5,), pady=2)
        #-------------
        inFileLb8 = Tk.Label(stepTwo, text="Select a node 1:")
        inFileLb8.grid(row=1, column=0, sticky='E', padx=(0,5), pady=2)

        variable6 = Tk.StringVar(stepOne)
        variable6.set(OPTIONS[0])

        w6 = Tk.OptionMenu(stepTwo, variable6, *OPTIONS)
        w6.grid(row=1, column=1, columnspan=7, sticky="WE", pady=3)

        searchnode = Tk.Button(stepTwo, text="Search")
        searchnode.grid(row=1, column=8, sticky='W', padx=(0,5), pady=2)
        #-------------
        inFileLb9 = Tk.Label(stepTwo, text="Select a node 1:")
        inFileLb9.grid(row=2, column=0, sticky='E', padx=(0,5), pady=2)

        variable7 = Tk.StringVar(stepOne)
        variable7.set(OPTIONS[0])

        w7 = Tk.OptionMenu(stepTwo, variable7, *OPTIONS)
        w7.grid(row=2, column=1, columnspan=7, sticky="WE", pady=3)

        inFileLb10 = Tk.Label(stepTwo, text="Select a node 2:")
        inFileLb10.grid(row=2, column=8, sticky='E', padx=(0,5), pady=2)

        variable8 = Tk.StringVar(stepOne)
        variable8.set(OPTIONS[0])

        w8 = Tk.OptionMenu(stepTwo, variable8, *OPTIONS)
        w8.grid(row=2, column=9, columnspan=7, sticky="WE", pady=3)

        inFileLb11 = Tk.Label(stepTwo, text="Insert the relation:")
        inFileLb11.grid(row=2, column=16, sticky='E', padx=(0,5), pady=2)
        e = Tk.Entry(stepTwo)
        e.grid(row=2, column=17, columnspan=3, sticky="WE", padx=(0,5))

        searchlink = Tk.Button(stepTwo, text="Search")
        searchlink.grid(row=2, column=20, sticky='W', padx=(0,0), pady=2)
        #-------------
        inFileLb12 = Tk.Label(stepTwo, text="Select a node 1:")
        inFileLb12.grid(row=3, column=0, sticky='E', padx=(0,5), pady=2)

        variable9 = Tk.StringVar(stepOne)
        variable9.set(OPTIONS[0])

        w9 = Tk.OptionMenu(stepTwo, variable9, *OPTIONS)
        w9.grid(row=3, column=1, columnspan=7, sticky="WE", pady=3)

        inFileLb13 = Tk.Label(stepTwo, text="Select a node 2:")
        inFileLb13.grid(row=3, column=8, sticky='E', padx=(0,5), pady=2)

        variable10 = Tk.StringVar(stepOne)
        variable10.set(OPTIONS[0])

        w10 = Tk.OptionMenu(stepTwo, variable10, *OPTIONS)
        w10.grid(row=3, column=9, columnspan=7, sticky="WE", pady=3)

        searchlink = Tk.Button(stepTwo, text="Draw path")
        searchlink.grid(row=3, column=16, sticky='W', padx=(0,0), pady=2)

        #**********************************************
        lbl = Tk.Label(right, text="The results area:") 
        lbl.config(font=("Segoe UI", 11))
        lbl.grid(row=0, column=0, padx=(0, 0), pady=(0,10)) 

        self.T = Tk.Text(right, height=27, width=35)
        S = Tk.Scrollbar(right)
        self.T.grid(row=1, column=0) 
        S.grid(row=1, column=1, sticky='ns') 
        S.config(command=self.T.yview)
        self.T.config(yscrollcommand=S.set)
        quote = """HAMLET: To be, or not to be--that is the question:\nWhether 'tis nobler in the mind to suffer\nThe slings and arrows of outrageous fortune\nOr to take arms against a sea of troubles\nAnd by opposing end them. To die, to sleep--\nNo more--and by a sleep to say we end\nThe heartache, and the thousand natural shocks\nThat flesh is heir to. 'Tis a consummation\nDevoutly to be wished."""
        self.T.insert(Tk.END, quote)

        btn = Tk.Button(self, text="Go to main window", command=self.onClose)
        btn.grid(row=2, column=5, sticky='W', padx=5, pady=10)

    def randomSearch(self):
        pass
        #self.printr(self.net.randomSearch())
    
    def printr(self, text):
        if self.init_p:
            self.T.delete('1.0', Tk.END)
            self.init_p = False
        t = text + "\n"
        self.T.insert(Tk.END, t)
   
    #----------------------------------------------------------------------
    def onClose(self):
        """"""
        self.destroy()
        self.original_frame.show()

########################################################################
class ErrorFrame(Tk.Toplevel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, original):
        """Constructor"""
        self.original_frame = original
        Tk.Toplevel.__init__(self)
        self.title("Error")

        lbl = Tk.Label(self, text="Error! could not load the network.") 
        lbl.config(font=("Segoe UI BOLD", 13))
        lbl.grid(row=1, column=0, padx=(20, 20), pady=(20,5))  

        lbl = Tk.Label(self, text="Try doing the following.") 
        lbl.config(font=("Segoe UI", 11))
        lbl.grid(row=2, column=0, padx=(20, 20), pady=(0,10)) 

        
        lbl = Tk.Label(self, text="- Check the existance of the file.") 
        lbl.config(font=("Segoe UI", 9))
        lbl.grid(row=3, column=0, padx=(20, 20), pady=(0,5)) 
        lbl = Tk.Label(self, text="- Check the name of the file.") 
        lbl.config(font=("Segoe UI", 9))
        lbl.grid(row=4, column=0, padx=(20, 20), pady=(0,5)) 
        lbl = Tk.Label(self, text="- Make sure that the file is in a csv format.") 
        lbl.config(font=("Segoe UI", 9))
        lbl.grid(row=5, column=0, padx=(20, 20), pady=(0,5)) 
        lbl = Tk.Label(self, text="- make sure the file is well formated.") 
        lbl.config(font=("Segoe UI", 9))
        lbl.grid(row=6, column=0, padx=(20, 20), pady=(0,10)) 


        btn = Tk.Button(self, text="Close", command=self.onClose)
        btn.grid(row=7, column=0, padx=(100, 100), pady=(10,20))
        
    #----------------------------------------------------------------------
    def onClose(self):
        """"""
        self.destroy()
        self.original_frame.show()
    
########################################################################
class MyApp(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        self.root = parent
        self.root.title("Network file selection")
        self.frame = Tk.Frame(parent)
        self.frame.pack()

        lbl = Tk.Label(self.frame, text="Please select your root network name") 
        lbl.config(font=("Segoe UI", 15))
        lbl.grid(row=1, column=0, padx=(20, 20), pady=(70,10))  

        self.fle = Tk.Entry(self.frame, width=40)
        self.fle.grid(row=2, column=0, padx=(100, 100), pady=(20,20))
        
        btn = Tk.Button(self.frame, text="Parse file", command=self.openFrame)
        btn.grid(row=3, column=0, padx=(100, 100), pady=(10,70))

    #----------------------------------------------------------------------
    def hide(self):
        """"""
        self.root.withdraw()
        
    #----------------------------------------------------------------------
    def openFrame(self):
        """"""
        self.hide()
        text = self.fle.get()
        net  = parser.read(text)
        if net:
            subFrame = OtherFrame(self,net)
        else:
            subFrame = ErrorFrame(self)
        
        
    #----------------------------------------------------------------------
    def show(self):
        """"""
        self.root.update()
        self.root.deiconify()
    
#----------------------------------------------------------------------
if __name__ == "__main__":
    root = Tk.Tk()
    #root.geometry("300x200")
    app = MyApp(root)
    root.mainloop()