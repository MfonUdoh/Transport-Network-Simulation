import tkinter as tk
from Controller import Controller
import time

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
        # self.map.columnconfigure([x for x in range(10)], weight=1)
        # self.map.rowconfigure([x for x in range(10)], weight=1)

        self.option_buttons()
        self.vars()
        self.hubs = {}

        try:
            self.OS.sim()
        except:
            pass

        self.mainloop()

    def option_buttons(self):
        xPadding = 5
        yPadding = 3

        btn_open = tk.Button(
            self.topBar, text="Open", 
            fg="white", bg="black", highlightbackground="black"
            ).grid(row=0, column=0, padx=xPadding, pady=yPadding)

        btn_save = tk.Button(
            self.topBar, text="Save",
            fg="white", bg="black", highlightbackground="black"
            ).grid(row=0, column=1, padx=xPadding, pady=yPadding)

        btn_run = tk.Button(
            self.topBar, text="Run", 
            fg="white", bg="black", highlightbackground="black", command=self.start_sim
            ).grid(row=0, column=2, padx=xPadding, pady=yPadding)

        btn_stop = tk.Button(
            self.topBar, text="Stop", 
            fg="white", bg="black", highlightbackground="black", command=self.stop_sim
            ).grid(row=0, column=3, padx=xPadding, pady=yPadding)

        btn_reset = tk.Button(
            self.topBar, text="Reset", 
            fg="white", bg="black", highlightbackground="black", command=self.reset_sim
            ).grid(row=0, column=4, padx=xPadding, pady=yPadding)

    def vars(self):
        self.vars = {}
        vars = {
            "time"  :   ["Time", 5000],
            "hub"   :   ["Hubs", 10],
            "dep"   :   ["Depots", 5],
            "con"   :   ["Consignments", 25]
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
                text="{}".format(vars[var][0]),
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

            def increment(var, inc):
                vars = {
                "time"  :   [1000, 10000, 1000],
                "hub"   :   [2, 15, 1],
                "dep"   :   [1, 10, 1],
                "con"   :   [1, 75, 5]
                }
                if inc == "+":
                    j = vars[var][2]
                else:
                    j = -vars[var][2]
                i = int(lbl_val["text"])
                if i+j <= vars[var][1] and i+j >= vars[var][0]:
                    lbl_val["text"] = i+j
                    self.vars[var] = lbl_val["text"]

            tk.Button(var_frameBottom, text="+", command=lambda: increment(var, "+"),
            fg="white", bg="black", highlightbackground="black").grid(row=0, column=2)
            tk.Button(var_frameBottom, text="-", command=lambda: increment(var, "-"),
            fg="white", bg="black", highlightbackground="black").grid(row=0, column=0)

        i = 0
        for v in vars:
            var_hub(vars, v, i)
            i += 1

    def start_sim(self):
        if self.hubs == {}:
            self.OS = Controller(int(self.vars['hub']), int(self.vars['dep']), int(self.vars['con']))
            for i in self.OS.world['hubs']:
                size = len(self.OS.world['hubs'][i].cargo) + 5
                self.hubs[i] = tk.Frame(self.map, bg="blue",width=size, height=size)
                # self.hubs[i].grid(row=self.OS.world['hubs'][i].y, column=self.OS.world['hubs'][i].x)
                self.hubs[i].place(relx=self.OS.world['hubs'][i].y, rely=self.OS.world['hubs'][i].x)
            self.run = True
            while self.OS.time < int(self.vars["time"]) and self.run:
                self.OS.sim()
                self.update_idletasks()
                self.update()

    def stop_sim(self):
        self.run = False

    def reset_sim(self):
        for i in self.hubs:
            self.hubs[i].place_forget()
        self.hubs = {}
        self.update_idletasks()

GUI()