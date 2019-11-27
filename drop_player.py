import simpleaudio as sa
import os
from tkinter import *
from tkinter import ttk


root = Tk()
root.title("Grubstakers Drops")

drop_files = []
drop_list = []
drop_variable = []

for file in os.listdir('./drops'):
    if file[-4:] == ".wav":
        drop_files.append("./drops/" + file)
        drop_list.append(file)

drop_files = sorted(drop_files, key=str.casefold)
drop_list = sorted(drop_list, key=str.casefold)

for item in drop_list:
    drop_variable.append(item[:-4])

drop_variable = StringVar(value=drop_variable)
statusmsg = StringVar()

def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

def play_drop ( *args ):
    idxs = lbox.curselection()
    for i in idxs:
        idx = int(i)
        drop_path = drop_files[idx]
        wave_obj = sa.WaveObject.from_wave_file( drop_path )
        play_obj = wave_obj.play()

def show_drop( *args ):
    idxs = lbox.curselection()
    for i in idxs:
        idx = int(i)
        drop_display = drop_list[idx]
        statusmsg.set( drop_display[:-4] )

def stop_drop ( *args ):
    sa.stop_all()

def quit ( *args ):
    sys.exit()

mainframe = ttk.Frame(root, padding=(20, 20, 20, 20))
mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
playframe = ttk.Frame(mainframe, padding=(1, 1, 1, 1))
playframe.grid(column=1, row=48, sticky=(N,W,E,S))
root.grid_columnconfigure(0, weight=4)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=0)

s = ttk.Style()
s.theme_use('clam')

play_img = PhotoImage(file='play.png')
stop_img = PhotoImage(file='stop.png')
quit_img = PhotoImage(file='quit.png')

lbox = Listbox(mainframe, listvariable=drop_variable, selectmode='browse', height=40, width=50)
play = Button(playframe, image=play_img, command=play_drop )
stop = Button(playframe, image=stop_img, command=stop_drop )
quit = Button(mainframe, image=quit_img, command=quit )
sc = ttk.Scrollbar( mainframe, orient=VERTICAL, command=lbox.yview)
drop_select = ttk.Label(root, textvariable=statusmsg, anchor=(W))

lbox.configure(yscrollcommand=sc.set)

lbox.grid(column=0,row=0,rowspan=50)
play.grid(column=0,row=0, padx=5 )
stop.grid(column=1,row=0, padx=5 )
quit.grid(column=1,row=49, padx=5 )
sc.grid(column=0,row=0,rowspan=50,sticky=(N,S,E))
drop_select.grid(column=0, row=1, sticky=(W,E))

root.bind('<Return>', play_drop)
root.bind('<space>', play_drop)
root.bind('<Key>', stop_drop)
lbox.bind('<<ListboxSelect>>', show_drop)

# Colorize alternating lines of the listbox
for i in range(0,len(drop_files),2):
    lbox.itemconfigure(i, background='#f2f2f0')

imgicon = PhotoImage(file='grub.png')
root.tk.call('wm', 'iconphoto', root._w, imgicon)

statusmsg.set('')

root.mainloop()
