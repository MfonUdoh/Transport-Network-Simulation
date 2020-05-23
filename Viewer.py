import tkinter as tk

class GUI(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("Transport Network")

        self.columnconfigure(0, weight=1, minsize=800)
        self.rowconfigure(1, weight=1, minsize=500)

        self.topBar = tk.Frame(
            self, bg="black"
        )
        self.topBar.grid(row=0, column=0, sticky="ew")

        self.mainWindow = tk.Frame(self)
        self.mainWindow.grid(row=1, column=0, sticky="nesw")
        self.mainWindow.columnconfigure(1, weight=1, minsize=700)
        self.mainWindow.rowconfigure(0, weight=1)

        self.sideBar = tk.Frame(
            self.mainWindow, bg="black"
        )
        self.sideBar.grid(row=0, column=0, sticky="ns")

        self.map = tk.Frame(
            self.mainWindow, bg="green"
        )
        self.map.grid(row=0, column=1, sticky="nsew")
        self.map.columnconfigure([x for x in range(10)], weight=1)
        self.map.rowconfigure([x for x in range(10)], weight=1)

        self.option_buttons()
        self.vars()

        self.mainloop()

    def option_buttons(self):
        xPadding = 5
        yPadding = 3

        btn_open = tk.Button(
            self.topBar, text="Open", 
            fg="white", highlightbackground="black"
            ).grid(row=0, column=0, padx=xPadding, pady=yPadding)

        btn_save = tk.Button(
            self.topBar, text="Save",
            fg="white", highlightbackground="black"
            ).grid(row=0, column=1, padx=xPadding, pady=yPadding)

        btn_run = tk.Button(
            self.topBar, text="Run", 
            fg="white", highlightbackground="black", command=self.start_sim
            ).grid(row=0, column=2, padx=xPadding, pady=yPadding)

        btn_stop = tk.Button(
            self.topBar, text="Stop", 
            fg="white", highlightbackground="black"
            ).grid(row=0, column=3, padx=xPadding, pady=yPadding)

        btn_reset = tk.Button(
            self.topBar, text="Reset", 
            fg="white", highlightbackground="black"
            ).grid(row=0, column=4, padx=xPadding, pady=yPadding)

    def vars(self):
        self.vars = {}
        vars = {
            "hub"   :   ["Hub", 10],
            "dep"   :   ["Depot", 5],
            "con"   :   ["Consignment", 20]
        }

        def var_hub(vars, var, row):
            yPadding = 5
            xPadding = 3

            var_frame = tk.Frame(self.sideBar, bg="black")
            var_frame.grid(row=row, column=0, sticky="ew", padx=xPadding, pady=yPadding)
            var_frame.columnconfigure(0, weight=1)
            var_frame.rowconfigure(0, weight=1)

            var_frameTop = tk.Frame(var_frame, bg="black")
            var_frameTop.grid(row=0, column=0)

            tk.Label(
                var_frameTop, 
                text="{}s".format(vars[var][0]),
                fg="white", bg="black"
            ).grid(row=0, column=0, sticky="ew")

            var_frameBottom = tk.Frame(var_frame, bg="black")
            var_frameBottom.grid(row=1, column=0)

            lbl_val = tk.Label(
                var_frameBottom, 
                text="{}".format(vars[var][1]),
                fg="white", bg="black"
            )
            lbl_val.grid(row=0, column=1, sticky="ew")
            self.vars[var] = lbl_val["text"]

            def increment(var, j):
                vars = {
                "hub"   :   [2, 15],
                "dep"   :   [1, 10],
                "con"   :   [1, 50]
                }
                i = int(lbl_val["text"])
                if i+j <= vars[var][1] and i+j >= vars[var][0]:
                    lbl_val["text"] = i+j
                    self.vars[var] = lbl_val["text"]

            tk.Button(var_frameBottom, text="+", command=lambda: increment(var, 1),
            fg="white", highlightbackground="black").grid(row=0, column=2)
            tk.Button(var_frameBottom, text="-", command=lambda: increment(var, -1),
            fg="white", highlightbackground="black").grid(row=0, column=0)
        
        i = 0
        for v in vars:
            var_hub(vars, v, i)
            i += 1

    def start_sim(self):
        hub = tk.Frame(self.map, bg="blue", width=20, height=20)
        hub.grid(row=self.vars['hub'], column=self.vars['dep'])

GUI()