import sys
import os
from tkinter import filedialog, messagebox
from tkinter import *
from tkinter import scrolledtext, END
import shutil
import win32api
import time

mainfolder = os.path.dirname(__file__) + '/assets'

tmpscount = 0

kosherni = 0
light = 0

try:
    file = sys.argv[1]
except:
    file = ""

if not os.path.exists(mainfolder + "/dbtmp"):
    os.mkdir(mainfolder + "/dbtmp")
    
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
    global scr
    scr.tag_remove('foundd', '1.0', END) 
    if s:
        idx = '1.0'
        while 1:
            idx = scr.search(s, idx, nocase=0, 
                              stopindex=END) 
            if not idx: break
            lastidx = '%s+%dc' % (idx, len(s)) 
            scr.tag_add('foundd', idx, lastidx)
            idx = lastidx
        scr.tag_config('foundd', background=bg)

def find(s: str, fg: str):
    global scr
    scr.tag_remove(s, '1.0', END)
    if s:
        idx = '1.0'
        while 1:
            idx = scr.search(s, idx, nocase=0, 
                              stopindex=END) 
            if not idx: break
            lastidx = '%s+%dc' % (idx, len(s)) 
            scr.tag_add(s, idx, lastidx)
            idx = lastidx
        scr.tag_config(s, foreground=fg)
        
def findS(s: str, fg: str):
    global scr
    scr.tag_remove(s, '1.0', END)
    if s:
        idx = '1.0'
        while 1:
            idx = scr.search(s, idx, nocase=0, 
                              stopindex=END) 
            if not idx: break
            lastidx = '%s+%dc' % (idx, len(scr.get(idx, f'{idx} lineend')))
            scr.tag_add(s, idx, lastidx)
            idx = lastidx
        scr.tag_config(s, foreground=fg)

def adjustSize(event):
    global zoom
    if zoom > 8 and event.delta/50 < 0:
        zoom += event.delta/50
    elif zoom < 200 and event.delta/50 > 0:
        zoom += event.delta/50
    if kosherni:
        scr.configure(font=('Baskerville Old Face', int(zoom)))
    else:
        scr.configure(font=('Consolas', int(zoom)))

pushs = 0

def updatedd():
    global tmpscount
    global pushs
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
    lil = len(os.listdir(f"{mainfolder}/dbtmp"))
    with open(f"{mainfolder}/dbtmp/tmp{str(lil-1)}.tmp") as lastchange:
        if not scr.get("1.0", "end-1c") == lastchange.read():
            if pushs < 0:
                if tmpscount < 12:
                    with open(f"{mainfolder}/dbtmp/tmp{str(tmpscount)}.tmp", "w+") as tmp:
                        tmp.write(scr.get("1.0", "end-1c"))
                        tmpscount += 1
                        pushs = 10
                else:
                    for i in range(lil):
                        try:
                            with open(f"{mainfolder}/dbtmp/tmp{str(i+1)}.tmp") as new:
                                with open(f"{mainfolder}/dbtmp/tmp{str(i)}.tmp", "w+") as tmp:
                                    tmp.write(new.read())
                                    tmpscount = 12
                                    pushs = 10
                        except:
                            with open(f"{mainfolder}/dbtmp/tmp12.tmp", "w+") as tmp:
                                tmp.write(scr.get("1.0", "end-1c"))
                                tmpscount = 12
                                pushs = 10
            else:
                pushs -= 1
    engineWindow.update()
    engineWindow.after(0, updatedd)

def ctrlz(*args):
    for i in range(2):
        global tmpscount
        count = len(os.listdir(f"{mainfolder}/dbtmp"))-1
        if count >= 1:
            with open(f"{mainfolder}/dbtmp/tmp{str(count)}.tmp") as tmp:
                scr.delete("1.0", END)
                scr.insert(END, tmp.read())
            os.remove(f"{mainfolder}/dbtmp/tmp{str(count)}.tmp")
            tmpscount -= 1
        elif count == 0:
            with open(f"{mainfolder}/dbtmp/tmp0.tmp") as tmp:
                scr.delete("1.0", END)
                scr.insert(END, tmp.read())
            tmpscount = 1

def Save(*args, mode=0):
    global file
    scr.config(cursor="watch")
    engineWindow.update()
    if not file == "" and mode == 0:
        with open(file, "w+") as DB:
            DB.write(scr.get("1.0", "end-1c"))
            engineWindow.title(f'PPL redactor - {os.path.splitext(os.path.basename(file))[0]}')
    else:
        path = filedialog.asksaveasfilename(title='Saving', defaultextension='ppl', initialfile='main', filetypes=(("Polite person's file", "*.ppl"), ("all files", "*.*")))
        if not path == "":
            file = path
            with open(file, "w+") as DB:
                DB.write(scr.get("1.0", "end-1c"))
                engineWindow.title(f'PPL redactor - {os.path.splitext(os.path.basename(file))[0]}')
    time.sleep(0.1)
    scr.config(cursor="xterm")

def Open():
    path = filedialog.askopenfilename(title='Opening', defaultextension='ppl', filetypes=(("Polite person's file", "*.ppl"), ("all files", "*.*")))
    if not path == "":
        with open(path) as gg:
            scr.delete("1.0", END)
            scr.insert(END, gg.read())
            global file
            file = path
            engineWindow.title(f'PPL redactor - {os.path.splitext(os.path.basename(file))[0]}')
def Test():
    Save()
    os.remove(f"{os.path.dirname(file)}\\bin\\{os.path.basename(file).replace('.ppl', '.exe')}")
    win32api.ShellExecute(0, "open", f"\"{mainfolder}\\Compiler.exe\"", os.path.abspath(file), os.path.dirname(file), 0)
    while not os.path.exists(f"{os.path.dirname(file)}\\bin\\{os.path.basename(file).replace('.ppl', '.exe')}"):
        time.sleep(0.1)
    win32api.ShellExecute(0, "open", f"\"{os.path.dirname(file)}\\bin\\{os.path.basename(file).replace('.ppl', '.exe')}\"", None, os.path.dirname(file) + '\\bin', 1)
def setFnt(*args):
    global kosherni
    kosherni = int(plfnt.get())
    with open(settingsFile, 'w+') as sett:
        sett.write(f'{kosherni}\n{light}\n{zoom}')
    if kosherni:
        scr.configure(font=('Baskerville Old Face', int(zoom)))
    else:
        scr.configure(font=('Consolas', int(zoom)))
def setTheme(*args):
    global light
    light = int(ltth.get())
    with open(settingsFile, 'w+') as sett:
        sett.write(f'{kosherni}\n{light}\n{zoom}')
    if light:
        scr.configure(background='#f0f0f0', fg='#0f0f0f', insertbackground='#0f0f0f', insertwidth='3', insertborderwidth='3')
    else:
        scr.configure(background='#3e3e3e', fg='#f0f0f0', insertbackground='#f0f0f0', insertwidth='3', insertborderwidth='3')
def exiting():
    with open(settingsFile, 'w+') as sett:
        sett.write(f'{kosherni}\n{light}\n{zoom}')
    shutil.rmtree(mainfolder + "/dbtmp")
    engineWindow.destroy()
def new_file():
    global tmpscount
    shutil.rmtree(mainfolder + "/dbtmp")
    os.mkdir(mainfolder + "/dbtmp")
    tmpscount = 0
    scr.delete("1.0", END)
    global file
    file = ""
    engineWindow.title(f'PPL redactor - *New')
    with open(f"{mainfolder}/dbtmp/tmp{str(tmpscount)}.tmp", "w+") as tmp:
        tmp.write(scr.get("1.0", "end-1c"))
        tmpscount += 1

engineWindow = Tk()
if not file == "":
    engineWindow.title(f'PPL redactor - {os.path.splitext(os.path.basename(file))[0]}')
else:
    engineWindow.title(f'PPL redactor - *New')
engineWindow.geometry("1280x720")
engineWindow.iconbitmap(f"{mainfolder}/icon.ico")
engineWindow.iconify()
engineWindow.deiconify()
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
scr = scrolledtext.ScrolledText(engineWindow)
scr.pack(expand=1, fill=BOTH)
if light:
    scr.configure(background='#f0f0f0', fg='#0f0f0f', insertbackground='#0f0f0f', insertwidth='3', insertborderwidth='3')
else:
    scr.configure(background='#3e3e3e', fg='#f0f0f0', insertbackground='#f0f0f0', insertwidth='3', insertborderwidth='3')
if kosherni:
    scr.configure(font=('Baskerville Old Face', zoom))
else:
    scr.configure(font=('Consolas', zoom))
if not file == "":
    with open(file, 'r') as DB:
        scr.insert(END, DB.read())
with open(f"{mainfolder}/dbtmp/tmp{str(tmpscount)}.tmp", "w+") as tmp:
    tmp.write(scr.get("1.0", "end-1c"))
    tmpscount += 1
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