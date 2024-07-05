import sys
import os
from tkinter import filedialog, messagebox
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext, END
import shutil
import trace
import traceback
import win32api
import time
import keyboard

mainfolder = os.path.dirname(__file__) + '/assets'

tmpscount = [0]

kosherni = 0
light = 0
af = 0
file = []
TipsShown = False
funcs = []
startscr = None
changed = [False]
push = 0

file.append("")

if not os.path.exists(mainfolder + "/dbtmp"):
    os.mkdir(mainfolder + "/dbtmp")
    
if not os.path.exists(mainfolder + "/dbtmp/0"):
    os.mkdir(mainfolder + "/dbtmp/0")
    
settingsFile = os.path.dirname(sys.argv[0]) + '/settings'

zoom = 20

oldpos = "0.0"

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
        
def findBetween(s: str, g: str, fg: str):
    global scrs
    scrs[af].tag_remove(s + g + "between", '1.0', END)
    if s:
        idx = '1.0'
        idy = '1.0'
        while 1:
            idx = scrs[af].search(s, idx, nocase=0, 
                              stopindex=END)
            idy = scrs[af].search(g, idy, nocase=0, 
                              stopindex=END) 
            if not idx or not idy: break
            lastidx = '%s+%dc' % (idx, len(s))
            lastidy = '%s+%dc' % (idy, len(g))
            scrs[af].tag_add(s + g + "between", lastidx, idy)
            idx = lastidx
            idy = lastidy
        scrs[af].tag_config(s + g + "between", foreground=fg)
        
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
        if light:
            clr = "#8B7765"
            clr2 = "#808069"
        else:
            clr = "#EECBAD"
            clr2 = "#CDBE70"
        find("0", clr)
        find("1", clr)
        find("2", clr)
        find("3", clr)
        find("4", clr)
        find("5", clr)
        find("6", clr)
        find("7", clr)
        find("8", clr)
        find("9", clr)
        find("Please ", "#CD6090")
        find("Please\n", "#CD6090")
        find("Thanks ", "#CD6090")
        find("Thanks\n", "#CD6090")
        find("import ", "#007FFF")
        find(" as ", "#007FFF")
        find("println", "#007FFF")
        find("print", "#007FFF")
        find("waitkey", "#007FFF")
        find("readln", "#007FFF")
        find("read", "#007FFF")
        find("for ", "#007FFF")
        find("while ", "#007FFF")
        find("int ", "#007FFF")
        find("bool ", "#007FFF")
        find("string ", "#007FFF")
        find("float ", "#007FFF")
        find("string[]", "#007FFF")
        find("bool[]", "#007FFF")
        find("int[]", "#007FFF")
        find("float[]", "#007FFF")
        find("public ", "#007FFF")
        find("private ", "#007FFF")
        find("void ", "#007FFF")
        find("protected ", "#007FFF")
        find("static ", "#007FFF")
        find("true", "#007FFF")
        find("false", "#007FFF")
        find("new", "#007FFF")
        guess()
        find("(", clr2)
        find(")", clr2)
        find("{", clr2)
        find("}", clr2)
        find("[", clr2)
        find("]", clr2)
        find("try", "#007FFF")
        find("catch", "#007FFF")
        find("finally", "#007FFF")
        find("if ", "#007FFF")
        find("else", "#007FFF")
        findBetween("import ", " as ", clr2)
        findBetween(" as ", ";", clr2)
        findBetween("(\"", "\")", "#E9967A")
        findBetween(" \"", "\";", "#E9967A")
        find("\"", "#E9967A")
        find("\'", "#E9967A")
        findS("//", "#008B00")
        find("/*", "#008B00")
        find("*/", "#008B00")
        findBetween("/*", "*/", "#008B00")
        findbg("$", "#B22222")
        find("$", "#CDAD00")
        if not file[af] == "":
            with open(file[af]) as ff:
                global changed
                if not ff.read() == scrs[af].get("1.0", "end-1c"):
                    changed[af] = True
                else:
                    changed[af] = False
            if changed[af]:
                notebook.tab(af, text='*'+os.path.basename(file[af]))
            else:
                notebook.tab(af, text=os.path.basename(file[af]))
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
    except: print('exc: ' + traceback.format_exc())#sys.exit()

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

def Open(event=None, pth=""):
    if pth == "":
        path = filedialog.askopenfilename(title='Opening', defaultextension='ppl', filetypes=(("Polite person's file", "*.ppl"), ("all files", "*.*")))
    else: path = pth
    if not path == "":
        new_file()
        with open(path) as gg:
            scrs[-1].delete("1.0", END)
            scrs[-1].insert(END, gg.read())
            global file
            file[-1] = path
            notebook.tab(len(file)-1, text=os.path.basename(file[-1]))

def CheckGrammar() -> bool:
    text = scrs[af].get("1.0", "end-1c")
    txtlines = text.split("\n")
    imports = []
    importfs = []
    asses = []
    try:
        for i in range(len(txtlines)):
            if "import" in txtlines[i]:
                spl = txtlines[i].split(' ')
                spl[spl.index('as')+1].replace(';', '')
                inx = spl.index('import')+1
                importfs.append(os.path.dirname(file[af]) + '\\' + spl[inx] + '.ppl')
                imports.append([])
                asses.append(spl[spl.index('as')+1].replace(';', ''))
        for i in range(len(importfs)):
            try:
                with open(importfs[i]) as imp:
                    rd = imp.readlines()
                    for a in range(len(rd)):
                        if "void" in rd[a]:
                            spl = rd[a].split(' ')
                            inx = spl.index('void')+1
                            imports[i].append(spl[inx].split('(')[0])
            except: None
    except: pass
    for i in range(len(txtlines)):
        try:
            if "$" in txtlines[i]:
                messagebox.showerror("Error", f"Forbidden character: '$' at line: {i+1}\nAt:\n  {txtlines[i]}")
                return False
            if not list(txtlines[i].replace(' ', ''))[-1] == ";" and not list(txtlines[i].replace(' ', ''))[-1] == "{" and not list(txtlines[i].replace(' ', ''))[-1] == "}":
                messagebox.showerror("Error", f"Expected: ';' at line: {i+1}\nAt:\n  {txtlines[i]}")
                return False
            if "import" in txtlines[i].split(' '):
                try:
                    if not txtlines[i].split(' ')[txtlines[i].split(' ').index("import") + 2] == 'as':
                        messagebox.showerror("Error", f"Expected: 'as' at line: {i+1}\nAt:\n  {txtlines[i]}")
                        return False
                except:
                    messagebox.showerror("Error", f"Expected: 'as' at line: {i+1}\nAt:\n  {txtlines[i]}")
                    return False
            if "import" in txtlines[i]:
                spl = txtlines[i].split(' ')
                inx = spl.index('import')+1
                importffs = os.path.dirname(file[af]) + '\\' + spl[inx] + '.ppl'
                try:
                    with open(importffs) as fs:
                        fs.close()
                except:
                    messagebox.showerror("Error", f"Unknown module name at line: {i+1}\nAt:\n  {txtlines[i]}")
                    return False
            for a in range(len(asses)):
                if asses[a] in txtlines[i]:
                    funcc = (txtlines[i].split(asses[a] + '.')[1]).split('(')[0]
                    print(funcc, imports[a])
                    if not funcc in imports[a]:
                        messagebox.showerror("Error", f"Unknown function '{asses[a]}.{funcc}' at line: {i+1}\nAt:\n  {txtlines[i]}")
                        return False
        except: None
    return True

def Test():
    global push
    push = 0
    Save()
    if CheckGrammar():
        engineWindow.config(cursor="watch")
        scrs[af].config(cursor="watch")
        menubar.config(cursor="watch")
        try:
            os.remove(f"{os.path.dirname(file[af])}\\bin\\{os.path.basename(file[af]).replace('.ppl', '.exe')}")
        except: None
        win32api.ShellExecute(0, "open", f"\"{mainfolder}\\Compiler.exe\"", os.path.abspath(file[af]), os.path.dirname(file[af]), 1)
        while not os.path.exists(f"{os.path.dirname(file[af])}\\bin\\{os.path.basename(file[af]).replace('.ppl', '.exe')}") and push < 40:
            push += 1
            time.sleep(0.1)
        engineWindow.config(cursor="")
        scrs[af].config(cursor="xterm")
        menubar.config(cursor="")
        win32api.ShellExecute(0, "open", f"\"{os.path.dirname(file[af])}\\bin\\{os.path.basename(file[af]).replace('.ppl', '.exe')}\"", None, os.path.dirname(file[af]) + '\\bin', 1)
    engineWindow.config(cursor="")
    scrs[af].config(cursor="xterm")
    menubar.config(cursor="")
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
    def dell():
        with open(settingsFile, 'w+') as sett:
            sett.write(f'{kosherni}\n{light}\n{zoom}')
        try:
            shutil.rmtree(mainfolder + "/dbtmp")
            os.remove(mainfolder + "/dbtmp")
        except: None
        engineWindow.destroy()
    chh = False
    for i in range(len(changed)):
        if changed[i]: chh = True
    if chh:
        result = messagebox.askyesnocancel(title='Exiting', message='You have unsaved changes!\nSave changes before exiting?')
        if result == True:
            for i in range(len(changed)):
                if changed[i]:
                    notebook.select(i)
                    Save()
            dell()
        elif result == False:
            dell()
        else: None
    else: dell()
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
    notebook.select(len(file)-1)
    changed.append(False)

CurTab = 0
def CloseTab():
    def dell():
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
        changed.pop(CurTab)
    if changed[CurTab]:
        result = messagebox.askyesnocancel(title='Closing tab', message='You have unsaved changes!\nSave changes before closing?')
        if result == True:
            notebook.select(CurTab)
            Save()
            dell()
        elif result == False:
            dell()
        else: None
    else: dell()
def do_popup(event):
    global CurTab
    if event.widget.identify(event.x, event.y) == 'label':
        index = event.widget.index('@%d,%d' % (event.x, event.y))
        CurTab = index
    try: 
        closemen.tk_popup(event.x_root, event.y_root) 
    finally: 
        closemen.grab_release()
        
def insrt(text: str, indx: str, donetxt: str):
    global TipsShown
    try:
        scr.destroy()
        TipsShown = False
        scrs[af].focus_set()
    except: pass
    if indx.split('.')[0] == '1':
        previdx = '%s-%dc' % (indx, len(donetxt))
    else:
        previdx = '%s-%dc' % (indx, len(donetxt)-1)
    scrs[af].delete(previdx, indx)
    scrs[af].insert(indx, text)
    scrs[af].focus_set()
    lastindex = '%s+%dc' % (previdx, len(text))
    scrs[af].mark_set('insert', lastindex)

def foccus():
    try:
        scrs[af].mark_set('insert', str(int(scrs[af].index('insert').split('.')[0])-1) + '.' + scrs[af].index('insert').split('.')[1])
        scr.focus_set()
        scr.selection_set(0, 0)
    except: print('exc: ' + traceback.format_exc())
    scrs[af].unbind("<Down>", END)

def do_popup2(x, y, text:list):
    global scr
    global startscr
    if light:
        scr = Listbox(scrs[af], background='#B0B0B0', fg='#0f0f0f', font=("Arial", 15), height=5, width=28)
    else:
        scr = Listbox(scrs[af], background='#5C5C5C', fg='#f0f0f0', font=("Arial", 15), height=5, width=28)
    scr.place(x=x, y=y)
    for i in range(len(text)):
        scr.insert(END, text[i])
    scr.bind('<Double-Button>', lambda event: insrt(text[int(scr.curselection()[0])], startindex, donetext))
    scr.bind("<Tab>", lambda event: insrt(text[int(scr.curselection()[0])], startindex, donetext))
    scrs[af].bind("<Down>", lambda event: foccus())
    startscr = text

def guess():
    global push
    global TipsShown
    global donetext
    global startindex
    global startscr
    itext = scrs[af].get("1.0", "end-1c")
    itext = itext.splitlines()
    imports = []
    importfs = []
    asses = []
    try:
        for i in range(len(itext)):
            if "void" in itext[i]:
                try:
                    spl = itext[i].split(' ')
                    inx = spl.index('void')+1
                    find(' ' + spl[inx].split('(')[0], "#A2CD5A")
                except: None
            if "new" in itext[i]:
                try:
                    spl = itext[i].split(' ')
                    inx = spl.index('new')+1
                    find(' ' + spl[inx].split('(')[0], "#A2CD5A")
                except: None
            if "import" in itext[i]:
                spl = itext[i].split(' ')
                spl[spl.index('as')+1].replace(';', '')
                inx = spl.index('import')+1
                importfs.append(os.path.dirname(file[af]) + '\\' + spl[inx] + '.ppl')
                imports.append([])
                asses.append(spl[spl.index('as')+1].replace(';', ''))
        for i in range(len(importfs)):
            try:
                with open(importfs[i]) as imp:
                    rd = imp.readlines()
                    for a in range(len(rd)):
                        if "void" in rd[a]:
                            spl = rd[a].split(' ')
                            inx = spl.index('void')+1
                            imports[i].append(spl[inx].replace('\n', ''))
            except:
                findbg(os.path.basename(importfs[i]).split('.')[0], "#B22222")
                find(os.path.basename(importfs[i]).split('.')[0], "#CDAD00")
    except: pass
    try:
        pos = scrs[af].bbox('insert')[:2]
    except: None
    index = scrs[af].index('insert')
    srch1 = scrs[af].search('\n', index, backwards=True, stopindex="1.0")
    srch3 = scrs[af].search(' ', index, backwards=True, stopindex="1.0")
    srch4 = scrs[af].search(';', index, backwards=True, stopindex="1.0")
    srch5 = scrs[af].search('(', index, backwards=True, stopindex="1.0")
    srch6 = scrs[af].search('{', index, backwards=True, stopindex="1.0")
    #srch8 = scrs[af].search('}', index, backwards=True, stopindex="1.0")
    searchers = []
    text = ""
    if srch1:
        searchers.append(len(scrs[af].get(srch1, index)))
    if srch3:
        searchers.append(len(scrs[af].get(srch3, index)))
    if srch4:
        searchers.append(len(scrs[af].get(srch4, index)))
    if srch5:
        searchers.append(len(scrs[af].get(srch5, index)))
    if srch6:
        searchers.append(len(scrs[af].get(srch6, index)))
    try:
        srch = min(searchers)
        try:
            if srch == len(scrs[af].get(srch1, index)):
                srch = srch1
        except: None
        try:
            if srch == len(scrs[af].get(srch3, index)):
                srch = srch3
        except: None
        try:
            if srch == len(scrs[af].get(srch4, index)):
                srch = srch4
        except: None
        try:
            if srch == len(scrs[af].get(srch5, index)):
                srch = srch5
        except: None
        try:
            if srch == len(scrs[af].get(srch6, index)):
                srch = srch6
        except: None
    except: srch = srch1
    try:
        scr.configure(font=("Arial", int(zoom*0.8)))
        scr.place_configure(x=pos[0]-zoom, y=pos[1]+8+zoom)
    except: None
    if srch:
        text = scrs[af].get(srch, index)
    else:
        text = scrs[af].get("1.0", index)
    donetext = text
    startindex = index
    allist = []
    rofls = ['import', 'print', 'println', 'read', 'readln', 'Please', 'Thanks', 'for', 'while', 'if', 'else', 'try', 'catch', 'Path', 'waitkey', 'void', 'private', 'protected', 'public', 'static', 'string', 'float', 'bool', 'int']
    text = text.replace('\n', '').replace(' ', '')
    if srch == srch6:
        text = text.replace('{', '')
    elif srch == srch5:
        text = text.replace('(', '')
    if text == "":
        text = '$'
    if text in rofls[0]:
        allist.append('import')
    if text in rofls[1] or text in rofls[2]:
        allist.append('print();')
        allist.append('println();')
    if text in rofls[3] or text in rofls[4]:
        allist.append('read();')
        allist.append('readln();')
    if text in rofls[5]:
        allist.append('Please')
    if text in rofls[6]:
        allist.append('Thanks')
    if text in rofls[7]:
        allist.append('for (int i; i < 10; i++) {}')
    if text in rofls[8]:
        allist.append('while (true) {}')
    if text in rofls[9]:
        allist.append('if () {}')
    if text in rofls[10]:
        allist.append('else {}')
    if text in rofls[11]:
        allist.append('try {} catch {}')
    if text in rofls[12]:
        allist.append('catch {}')
    if text in rofls[13]:
        allist.append('Path')
    if text in rofls[14]:
        allist.append('waitkey();')
    if text in rofls[15]:
        allist.append('void ')
    if text in rofls[16]:
        allist.append('private ')
    if text in rofls[17]:
        allist.append('protected ')
    if text in rofls[18]:
        allist.append('public ')
    if text in rofls[19]:
        allist.append('static ')
    if text in rofls[20]:
        allist.append('string ')
    if text in rofls[21]:
        allist.append('float ')
    if text in rofls[22]:
        allist.append('bool ')
    if text in rofls[23]:
        allist.append('int ')
    for i in range(len(imports)):
        for a in range(len(imports[i])):
            if text in asses[i] + '.' + imports[i][a]:
                allist.append(asses[i] + '.' + imports[i][a])
            find(imports[i][a], "#A2CD5A")
    if not allist == []:
        if not TipsShown:
            do_popup2(pos[0]-0.8*zoom, pos[1]+1.2*zoom, allist)
            TipsShown = True
    else:
        try:
            scr.destroy()
            TipsShown = False
            scrs[af].focus_set()
        except: pass
    if not allist == startscr and TipsShown:
        try:
            scr.destroy()
            do_popup2(pos[0]-0.8*zoom, pos[1]+1.2*zoom, allist)
            startscr = allist
        except: pass

def delTips(event):
    try:
        scr.destroy()
        scrs[af].focus_set()
        if TipsShown:
            scrs[af].mark_set('insert', oldpos)
        TipsShown = False
    except: pass

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
file_menu.add_command(label="Save as",command=lambda: Save(mode=1))
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
with open(f"{mainfolder}/dbtmp/{af}/tmp{str(tmpscount[0])}.tmp", "w+") as tmp:
    tmp.write(scrs[0].get("1.0", "end-1c"))
    tmpscount[0] += 1
try:
    Open(pth=sys.argv[1])
except: None
engineWindow.bind('<Control-MouseWheel>', adjustSize)
engineWindow.bind('<Control-s>', Save)
engineWindow.bind('<Control-S>', Save)
engineWindow.bind('<Control-o>', Open)
engineWindow.bind('<Control-O>', Open)
engineWindow.bind('<Control-z>', ctrlz)
engineWindow.bind('<Control-Z>', ctrlz)
engineWindow.bind('<Escape>', delTips)
engineWindow.protocol("WM_DELETE_WINDOW", exiting)
engineWindow.configure(background='#3e3e3e')
updatedd()
engineWindow.update()