import tkinter as tk
from Controller import Controller
import time
import csv

class GUI(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("Transport Network")
        self.width = 800
        self.height = 500

        self.columnconfigure(0, weight=1, minsize=self.width)
        self.rowconfigure(1, weight=1, minsize=self.height)

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
        self.clean_map()

        self.option_buttons()
        self.vars()
        self.OS = 0

        self.mainloop()
    
    def clean_map(self):
        self.map = tk.Canvas(
            self.mainWindow, bg="green"
        )
        self.map.grid(row=0, column=1, sticky="nsew")

    def option_buttons(self):
        xPadding = 5
        yPadding = 3

        btn_open = tk.Button(
            self.topBar, text="Open", 
            fg="white", bg="black", highlightbackground="black"
            ).grid(row=0, column=0, padx=xPadding, pady=yPadding)

        btn_save = tk.Button(
            self.topBar, text="Save",
            fg="white", bg="black", highlightbackground="black", command=self.save_data
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

        self.time = tk.Label(self.topBar, text=0, fg="white", bg="black")
        self.time.grid(row=0, column=5, padx=xPadding, pady=yPadding)

    def vars(self):
        self.vars = {}
        vars = {
            "time"  :   ["Time", 5000],
            "speed" :   ["Speed", 1],
            "hub"   :   ["Hubs", 10],
            "dep"   :   ["Depots", 5],
            "con"   :   ["Consignments", 40]
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
                "speed" :   [1, 5, 1],
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
        if self.OS == 0:
            self.OS = Controller(int(self.vars['hub']), int(self.vars['dep']), int(self.vars['con']), int(self.vars['speed']))
            self.place_objects()
            self.run = True
            while self.OS.time < int(self.vars["time"]) and self.run:
                self.clean_map()
                self.place_objects()
                self.OS.sim()
                self.time['text'] = self.OS.time
                self.update_idletasks()
                self.update()

    def stop_sim(self):
        self.run = False

    def reset_sim(self):
        self.stop_sim()
        self.clean_map()
        self.OS = 0
        self.time['text'] = 0
        self.update_idletasks()

    def save_data(self):
        if self.OS != 0:
            with open('simData.csv', mode='w') as simData:
                wrt = csv.writer(simData, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                wrt.writerow(['Hub', 'Item', 'Origin', 'Destination', 'Extra'])
                for hub in self.OS.world['hubs']:
                    for trailer in self.OS.world['hubs'][hub].park:
                        wrt.writerow([hub, trailer, self.OS.world['hubs'][hub].park[trailer].origin, self.OS.world['hubs'][hub].park[trailer].destination, len(self.OS.world['hubs'][hub].park[trailer].cargo), 'Parked'])
                    for trailer in self.OS.world['hubs'][hub].loadingBay:
                        wrt.writerow([hub, trailer, self.OS.world['hubs'][hub].loadingBay[trailer].origin, self.OS.world['hubs'][hub].loadingBay[trailer].destination, len(self.OS.world['hubs'][hub].loadingBay[trailer].cargo), 'Loading'])
                    for trailer in self.OS.world['hubs'][hub].unloadingBay:
                        wrt.writerow([hub, trailer, self.OS.world['hubs'][hub].unloadingBay[trailer].origin, self.OS.world['hubs'][hub].unloadingBay[trailer].destination, len(self.OS.world['hubs'][hub].unloadingBay[trailer].cargo), 'Unloading'])
                    for package in self.OS.world['hubs'][hub].cargo:
                        wrt.writerow([hub, package, package.origin, package.destination, package.path])


    def place_objects(self):
        for hub in self.OS.world['hubs']:
            for road in self.OS.world['hubs'][hub].roads:
                x1 = self.OS.world['hubs'][hub].roads[road].x1*(self.width-100)
                y1 = self.OS.world['hubs'][hub].roads[road].y1*self.height
                x2 = self.OS.world['hubs'][hub].roads[road].x2*(self.width-100)
                y2 = self.OS.world['hubs'][hub].roads[road].y2*self.height
                self.map.create_line(x1, y1, x2, y2, fill="blue", width=len(self.OS.world['hubs'][hub].roads[road].trailers)*2)
        for hub in self.OS.world['hubs']:
            for road in self.OS.world['hubs'][hub].roads:
                for trailer in self.OS.world['hubs'][hub].roads[road].trailers:
                    x = trailer.x*(self.width-100)
                    y = trailer.y*self.height
                    self.map.create_oval(x-1, y-1, x+1, y+1, outline="black", fill="black", width=5)
        for hub in self.OS.world['hubs']:
            size = (len(self.OS.world['hubs'][hub].cargo) + 3)/2
            x = self.OS.world['hubs'][hub].x*(self.width-100)
            y = self.OS.world['hubs'][hub].y*self.height
            self.map.create_rectangle(x-size, y+size, x+size, y-size, outline="blue", fill="red",width=len(self.OS.world['hubs'][hub].deliveredBin))
            self.map.create_text(x, y, fill="white", text=str(self.OS.world['hubs'][hub])) 

GUI()