from tkinter import *
from tkinter import ttk
from stuff import Stuff
import stuffify
from freestuff import scrape_craig

def gather():
    scrape_craig()
    pass
def cancel_crawl():
    exit()
    pass

root = Tk()
root.title("Trinket Shell")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

feet = StringVar()
meters = StringVar()

feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
feet_entry.grid(column=6, row=1, sticky=(W, E))

ttk.Label(mainframe, textvariable=list).grid(column=6, row=2, sticky=(W, E))
ttk.Button(mainframe, text="List Trinkets in Terminal", command=gather).grid(column=6, row=3, sticky=W)
ttk.Button(mainframe, text="Exit", command=cancel_crawl).grid(column=6, row=4, sticky=W)

ttk.Label(mainframe, text="Location").grid(column=7, row=1, sticky=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

feet_entry.focus()
root.bind('<Return>', gather)

root.mainloop()