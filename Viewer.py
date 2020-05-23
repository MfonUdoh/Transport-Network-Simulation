import tkinter as tk

window = tk.Tk()
window.title("Transport Network")
window.columnconfigure(0, weight=1, minsize=800)
window.rowconfigure(1, weight=1, minsize=500)

btnPadding = 5

fr_topbtns = tk.Frame(window, bg="black")
fr_topbtns.grid(row=0, column=0, sticky="ew")
btn_open = tk.Button(fr_topbtns, text="Open", fg="white", highlightbackground="black")
btn_save = tk.Button(fr_topbtns, text="Save", fg="white", highlightbackground="black")
btn_run = tk.Button(fr_topbtns, text="Run", fg="white", highlightbackground="black")
btn_open.grid(row=0, column=1, sticky="ew", padx=btnPadding, pady=btnPadding)
btn_save.grid(row=0, column=2, sticky="ew", pady=btnPadding)
btn_run.grid(row=0, column=3, sticky="ew", padx=btnPadding, pady=btnPadding)

fr_main = tk.Frame(window)
fr_main.grid(row=1, column=0, sticky="nsew")
fr_main.columnconfigure(1, weight=1)
fr_main.rowconfigure(0, weight=1)

fr_sidebtns = tk.Frame(fr_main, bg="black")
fr_sidebtns.grid(row=0, column=0, sticky="ns")

def increment(var, j):
    vars = {
        "hub"   :   [lbl_hub_val, 2, 15],
        "dep"   :   [lbl_dep_val, 1, 10],
        "con"   :   [lbl_con_val, 1, 50]
    }
    i = int(vars[var][0]["text"])
    if i+j <= vars[var][2] and i+j >= vars[var][1]:
        vars[var][0]["text"] = i+j

fr_hub = tk.Frame(fr_sidebtns, bg="black")
fr_hub.grid(row=0, column=0, sticky="ew")
fr_hub.columnconfigure(0, weight=1)
fr_hub.rowconfigure(0, weight=1)
fr_hubBtn = tk.Frame(fr_hub, bg="black")
fr_hubBtn.grid(row=1, column=0)

lbl_hub = tk.Label(fr_hub, text="Hubs", fg="white", bg="black")
btn_hub_in = tk.Button(fr_hubBtn, text="+", fg="white", highlightbackground="black", command=lambda: increment("hub", 1))
lbl_hub_val = tk.Label(fr_hubBtn, text="10", fg="white", bg="black")
btn_hub_dec = tk.Button(fr_hubBtn, text="-", fg="white", highlightbackground="black", command=lambda: increment("hub", -1))
lbl_hub.grid(row=0, column=0, padx=btnPadding, pady=btnPadding)
btn_hub_in.grid(row=0, column=2, sticky="ew", padx=btnPadding, pady=btnPadding)
lbl_hub_val.grid(row=0, column=1, padx=btnPadding, pady=btnPadding)
btn_hub_dec.grid(row=0, column=0, sticky="ew", padx=btnPadding, pady=btnPadding)

fr_dep = tk.Frame(fr_sidebtns, bg="black")
fr_dep.grid(row=1, column=0, sticky="ew")
fr_dep.columnconfigure(0, weight=1)
fr_dep.rowconfigure(0, weight=1)
fr_depBtn = tk.Frame(fr_dep, bg="black")
fr_depBtn.grid(row=1, column=0)

lbl_dep = tk.Label(fr_dep, text="Depots", fg="white", bg="black")
btn_dep_in = tk.Button(fr_depBtn, text="+", fg="white", highlightbackground="black", command=lambda: increment("dep", 1))
lbl_dep_val = tk.Label(fr_depBtn, text="5", fg="white", bg="black")
btn_dep_dec = tk.Button(fr_depBtn, text="-", fg="white", highlightbackground="black", command=lambda: increment("dep", -1))
lbl_dep.grid(row=0, column=0, padx=btnPadding, pady=btnPadding)
btn_dep_in.grid(row=0, column=2, sticky="ew", padx=btnPadding, pady=btnPadding)
lbl_dep_val.grid(row=0, column=1, padx=btnPadding, pady=btnPadding)
btn_dep_dec.grid(row=0, column=0, sticky="ew", padx=btnPadding, pady=btnPadding)

fr_con = tk.Frame(fr_sidebtns, bg="black")
fr_con.grid(row=2, column=0, sticky="ew")
fr_con.columnconfigure(0, weight=1)
fr_con.rowconfigure(0, weight=1)
fr_conBtn = tk.Frame(fr_con, bg="black")
fr_conBtn.grid(row=1, column=0)

lbl_con = tk.Label(fr_con, text="Consignments", fg="white", bg="black")
btn_con_in = tk.Button(fr_conBtn, text="+", fg="white", highlightbackground="black", command=lambda: increment("con", 1))
lbl_con_val = tk.Label(fr_conBtn, text="20", fg="white", bg="black")
btn_con_dec = tk.Button(fr_conBtn, text="-", fg="white", highlightbackground="black", command=lambda: increment("con", -1))
lbl_con.grid(row=0, column=0, padx=btnPadding, pady=btnPadding)
btn_con_in.grid(row=0, column=2, sticky="ew", padx=btnPadding, pady=btnPadding)
lbl_con_val.grid(row=0, column=1, padx=btnPadding, pady=btnPadding)
btn_con_dec.grid(row=0, column=0, sticky="ew", padx=btnPadding, pady=btnPadding)

fr_map = tk.Label(fr_main, bg="green")
fr_map.grid(row=0, column=1, sticky="nsew")

window.mainloop()