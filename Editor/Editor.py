import sys
import os
from tkinter import filedialog, messagebox
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext, END
import shutil
import traceback
import win32api
import time

mainfolder = os.path.dirname(__file__) + '/assets'

tmpscount = [0]

kosherni = 0
light = 0
af = 0
file = []

try:
    file.append(sys.argv[1])
except:
    file.append("")

if not os.path.exists(mainfolder + "/dbtmp"):
    os.mkdir(mainfolder + "/dbtmp")
    
if not os.path.exists(mainfolder + "/dbtmp/0"):
    os.mkdir(mainfolder + "/dbtmp/0")
    
settingsFile = os.path.dirname(sys.argv[0]) + '/settings'

zoom = 20

try:
    with open(settingsFile, 'r') as sett:
        lols = sett.readlines()
        kosherni = int(lols[0])
        light = int(lols[1])
        zoom = int(float(lols[2]))
except:
    with open(settingsFile, 'w+') as sett:
        sett.write('0\n0\n20')

def findbg(s: str, bg: str):
    global scrs
    scrs[af].tag_remove('foundd', '1.0', END)
    if s:
        idx = '1.0'
        while 1:
            idx = scrs[af].search(s, idx, nocase=0, 
                              stopindex=END) 
            if not idx: break
            lastidx = '%s+%dc' % (idx, len(s)) 
            scrs[af].tag_add('foundd', idx, lastidx)
            idx = lastidx
        scrs[af].tag_config('foundd', background=bg)

def find(s: str, fg: str):
    global scrs
    scrs[af].tag_remove(s, '1.0', END)
    if s:
        idx = '1.0'
        while 1:
            idx = scrs[af].search(s, idx, nocase=0, 
                              stopindex=END) 
            if not idx: break
            lastidx = '%s+%dc' % (idx, len(s)) 
            scrs[af].tag_add(s, idx, lastidx)
            idx = lastidx
        scrs[af].tag_config(s, foreground=fg)
        
def findS(s: str, fg: str):
    global scrs
    scrs[af].tag_remove(s, '1.0', END)
    if s:
        idx = '1.0'
        while 1:
            idx = scrs[af].search(s, idx, nocase=0, 
                              stopindex=END) 
            if not idx: break
            lastidx = '%s+%dc' % (idx, len(scrs[af].get(idx, f'{idx} lineend')))
            scrs[af].tag_add(s, idx, lastidx)
            idx = lastidx
        scrs[af].tag_config(s, foreground=fg)

def adjustSize(event):
    global zoom
    if zoom > 8 and event.delta/50 < 0:
        zoom += event.delta/50
    elif zoom < 200 and event.delta/50 > 0:
        zoom += event.delta/50
    if kosherni:
        for i in range(len(scrs)):
            scrs[i].configure(font=('Baskerville Old Face', int(zoom)))
    else:
        for i in range(len(scrs)):
            scrs[i].configure(font=('Consolas', int(zoom)))

pushs = 0

def updatedd():
    global tmpscount
    global pushs
    global af
    try:
        af = notebook.index(notebook.select())
        find("Please ", "pink")
        find("Please\n", "pink")
        find("Thanks ", "pink")
        find("Thanks\n", "pink")
        find("import ", "#007FFF")
        find(" as ", "#007FFF")
        find("println", "#007FFF")
        find("print", "#007FFF")
        find("readln", "#007FFF")
        find("read", "#007FFF")
        find("for ", "#007FFF")
        find("while ", "#007FFF")
        find("int ", "#007FFF")
        find("bool ", "#007FFF")
        find("string ", "#007FFF")
        find("try", "#007FFF")
        find("catch", "#007FFF")
        find("finally", "#007FFF")
        find("if ", "#007FFF")
        find("else", "#007FFF")
        findS("//", "#458B74")
        lil = len(os.listdir(f"{mainfolder}/dbtmp/{af}/"))
        with open(f"{mainfolder}/dbtmp/{af}/tmp{str(lil-1)}.tmp") as lastchange:
            if not scrs[af].get("1.0", "end-1c") == lastchange.read():
                if pushs < 0:
                    if tmpscount[af] < 12:
                        with open(f"{mainfolder}/dbtmp/{af}/tmp{str(tmpscount[af])}.tmp", "w+") as tmp:
                            tmp.write(scrs[af].get("1.0", "end-1c"))
                            tmpscount[af] += 1
                            pushs = 10
                    else:
                        for i in range(lil):
                            try:
                                with open(f"{mainfolder}/dbtmp/{af}/tmp{str(i+1)}.tmp") as new:
                                    with open(f"{mainfolder}/dbtmp/{af}/tmp{str(i)}.tmp", "w+") as tmp:
                                        tmp.write(new.read())
                                        tmpscount[af] = 12
                                        pushs = 10
                            except:
                                with open(f"{mainfolder}/dbtmp/{af}/tmp12.tmp", "w+") as tmp:
                                    tmp.write(scrs[af].get("1.0", "end-1c"))
                                    tmpscount[af] = 12
                                    pushs = 10
                else:
                    pushs -= 1
        engineWindow.update()
        engineWindow.after(0, updatedd)
    except: sys.exit()

def ctrlz(*args):
    for i in range(2):
        global tmpscount
        count = len(os.listdir(f"{mainfolder}/dbtmp/{af}/"))-1
        if count >= 1:
            with open(f"{mainfolder}/dbtmp/{af}/tmp{str(count)}.tmp") as tmp:
                scrs[af].delete("1.0", END)
                scrs[af].insert(END, tmp.read())
            os.remove(f"{mainfolder}/dbtmp/{af}/tmp{str(count)}.tmp")
            tmpscount[af] -= 1
        elif count == 0:
            with open(f"{mainfolder}/dbtmp/{af}/tmp0.tmp") as tmp:
                scrs[af].delete("1.0", END)
                scrs[af].insert(END, tmp.read())
            tmpscount[af] = 1

def Save(*args, mode=0):
    global file
    scrs[af].config(cursor="watch")
    engineWindow.update()
    if not file[af] == "" and mode == 0:
        with open(file[af], "w+") as DB:
            DB.write(scrs[af].get("1.0", "end-1c"))
            notebook.tab(af, text=os.path.basename(file[af]))
    else:
        path = filedialog.asksaveasfilename(title='Saving', defaultextension='ppl', initialfile='main', filetypes=(("Polite person's file", "*.ppl"), ("all files", "*.*")))
        if not path == "":
            file[af] = path
            with open(file[af], "w+") as DB:
                DB.write(scrs[af].get("1.0", "end-1c"))
                notebook.tab(af, text=os.path.basename(file[af]))
    time.sleep(0.1)
    scrs[af].config(cursor="xterm")

def Open():
    path = filedialog.askopenfilename(title='Opening', defaultextension='ppl', filetypes=(("Polite person's file", "*.ppl"), ("all files", "*.*")))
    if not path == "":
        new_file()
        with open(path) as gg:
            scrs[-1].delete("1.0", END)
            scrs[-1].insert(END, gg.read())
            global file
            file[-1] = path
            notebook.tab(len(file)-1, text=os.path.basename(file[-1]))
def Test():
    Save()
    os.remove(f"{os.path.dirname(file[af])}\\bin\\{os.path.basename(file[af]).replace('.ppl', '.exe')}")
    win32api.ShellExecute(0, "open", f"\"{mainfolder}\\Compiler.exe\"", os.path.abspath(file[af]), os.path.dirname(file[af]), 0)
    while not os.path.exists(f"{os.path.dirname(file[af])}\\bin\\{os.path.basename(file[af]).replace('.ppl', '.exe')}"):
        time.sleep(0.1)
    win32api.ShellExecute(0, "open", f"\"{os.path.dirname(file[af])}\\bin\\{os.path.basename(file[af]).replace('.ppl', '.exe')}\"", None, os.path.dirname(file[af]) + '\\bin', 1)
def setFnt(*args):
    global kosherni
    kosherni = int(plfnt.get())
    with open(settingsFile, 'w+') as sett:
        sett.write(f'{kosherni}\n{light}\n{zoom}')
    if kosherni:
        for i in range(len(scrs)):
            scrs[i].configure(font=('Baskerville Old Face', int(zoom)))
    else:
        for i in range(len(scrs)):
            scrs[i].configure(font=('Consolas', int(zoom)))
def setTheme(*args):
    global light
    light = int(ltth.get())
    with open(settingsFile, 'w+') as sett:
        sett.write(f'{kosherni}\n{light}\n{zoom}')
    if light:
        for i in range(len(scrs)):
            scrs[i].configure(background='#f0f0f0', fg='#0f0f0f', insertbackground='#0f0f0f', insertwidth='3', insertborderwidth='3')
    else:
        for i in range(len(scrs)):
            scrs[i].configure(background='#3e3e3e', fg='#f0f0f0', insertbackground='#f0f0f0', insertwidth='3', insertborderwidth='3')
def exiting():
    with open(settingsFile, 'w+') as sett:
        sett.write(f'{kosherni}\n{light}\n{zoom}')
    try:
        shutil.rmtree(mainfolder + "/dbtmp")
        os.remove(mainfolder + "/dbtmp")
    except: None
    engineWindow.destroy()
def new_file():
    frames.append(ttk.Frame(notebook))
    frames[-1].pack(fill=BOTH, expand=True)
    notebook.add(frames[-1], text="*New")
    scrs.append(scrolledtext.ScrolledText(frames[-1]))
    scrs[-1].pack(expand=1, fill=BOTH)
    if light:
        scrs[-1].configure(background='#f0f0f0', fg='#0f0f0f', insertbackground='#0f0f0f', insertwidth='3', insertborderwidth='3')
    else:
        scrs[-1].configure(background='#3e3e3e', fg='#f0f0f0', insertbackground='#f0f0f0', insertwidth='3', insertborderwidth='3')
    if kosherni:
        scrs[-1].configure(font=('Baskerville Old Face', int(zoom)))
    else:
        scrs[-1].configure(font=('Consolas', int(zoom)))
    file.append("")
    if not os.path.exists(mainfolder + f"/dbtmp/{len(file)-1}"):
        os.mkdir(mainfolder + f"/dbtmp/{len(file)-1}")
    tmpscount.append(0)
    with open(f"{mainfolder}/dbtmp/{len(file)-1}/tmp{str(tmpscount[-1])}.tmp", "w+") as tmp:
        tmp.write(scrs[-1].get("1.0", "end-1c"))
        tmpscount[-1] += 1

CurTab = 0
def CloseTab():
    tmpscount.pop(CurTab)
    dirs = os.listdir(f"{mainfolder}/dbtmp")
    for i in range(len(dirs)):
        if int(dirs[i]) > CurTab:
            try:
                shutil.rmtree(f"{mainfolder}/dbtmp/{int(dirs[i])-1}")
                shutil.copytree(f"{mainfolder}/dbtmp/{dirs[i]}", f"{mainfolder}/dbtmp/{int(dirs[i])-1}")
            except: None
    dirs = os.listdir(f"{mainfolder}/dbtmp")
    for i in range(len(dirs)):
        if int(dirs[i]) > len(tmpscount)-1:
            try:
                shutil.rmtree(f"{mainfolder}/dbtmp/{dirs[i]}")
                os.remove(f"{mainfolder}/dbtmp/{dirs[i]}")
            except: None
    scrs.pop(CurTab)
    notebook.forget(CurTab)
    frames.pop(CurTab)
    file.pop(CurTab)
def do_popup(event):
    global CurTab
    if event.widget.identify(event.x, event.y) == 'label':
        index = event.widget.index('@%d,%d' % (event.x, event.y))
        CurTab = index
    try: 
        closemen.tk_popup(event.x_root, event.y_root) 
    finally: 
        closemen.grab_release()

engineWindow = Tk()
engineWindow.geometry("1280x720")
engineWindow.iconbitmap(f"{mainfolder}/icon.ico")
engineWindow.title(f'PPL redactor')
engineWindow.iconify()
engineWindow.deiconify()
closemen = Menu(engineWindow, tearoff=0)
closemen.add_command(label="Close", command=CloseTab)
menubar = Menu()
file_menu = Menu(menubar, tearoff=False)
settsmenu = Menu(menubar, tearoff=False)
menubar.add_cascade(menu=file_menu, label="File", font=('Arial', 15))
menubar.add_cascade(menu=settsmenu, label="Settings", font=('Arial', 15))
menubar.add_command(label='Test', font=('Arial', 15), command=Test)
plfnt = BooleanVar(engineWindow)
plfnt.set(bool(kosherni))
settsmenu.add_checkbutton(label="Polite font",variable=plfnt)
plfnt.trace_variable("w", setFnt)
ltth = BooleanVar(engineWindow)
ltth.set(bool(light))
settsmenu.add_checkbutton(label="Light theme",variable=ltth)
ltth.trace_variable("w", setTheme)
file_menu.add_command(label="New",command=new_file)
file_menu.add_command(label="Undo",command=ctrlz,accelerator="Ctrl+Z")
file_menu.add_command(label="Save",command=Save,accelerator="Ctrl+S")
file_menu.add_command(label="Save as",command=lambda x: Save(mode=1))
file_menu.add_command(label="Open",command=Open,accelerator="Ctrl+O")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=engineWindow.destroy)
engineWindow.config(menu=menubar)
notebook = ttk.Notebook()
notebook.pack(expand=True, fill=BOTH)
frames = []
scrs = []
frames.append(ttk.Frame(notebook))
frames[0].pack(fill=BOTH, expand=True)
if not file[0] == "":
    notebook.add(frames[0], text=os.path.basename(file[0]))
else:
    notebook.add(frames[0], text="*New")
notebook.bind("<3>", do_popup)
scrs.append(scrolledtext.ScrolledText(frames[0]))
scrs[0].pack(expand=1, fill=BOTH)
if light:
    scrs[0].configure(background='#f0f0f0', fg='#0f0f0f', insertbackground='#0f0f0f', insertwidth='3', insertborderwidth='3')
else:
    scrs[0].configure(background='#3e3e3e', fg='#f0f0f0', insertbackground='#f0f0f0', insertwidth='3', insertborderwidth='3')
if kosherni:
    scrs[0].configure(font=('Baskerville Old Face', zoom))
else:
    scrs[0].configure(font=('Consolas', zoom))
if not file[0] == "":
    with open(file[0], 'r') as DB:
        scrs[0].insert(END, DB.read())
with open(f"{mainfolder}/dbtmp/{af}/tmp{str(tmpscount[0])}.tmp", "w+") as tmp:
    tmp.write(scrs[0].get("1.0", "end-1c"))
    tmpscount[0] += 1
engineWindow.bind('<Control-MouseWheel>', adjustSize)
engineWindow.bind('<Control-s>', Save)
engineWindow.bind('<Control-S>', Save)
engineWindow.bind('<Control-o>', Open)
engineWindow.bind('<Control-O>', Open)
engineWindow.bind('<Control-z>', ctrlz)
engineWindow.bind('<Control-Z>', ctrlz)
engineWindow.protocol("WM_DELETE_WINDOW", exiting)
engineWindow.configure(background='#3e3e3e')
updatedd()
engineWindow.update()