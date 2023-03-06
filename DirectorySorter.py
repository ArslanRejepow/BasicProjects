import os, shutil, psutil, threading, time
from customtkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import Frame

root = CTk()
root.title('Disk Tertipleýji')
root.geometry('750x600')
root.minsize(750, 600)
root.maxsize(750, 600)

frame_folder = CTkFrame(master=root, width=100, height=10)
frame_folder.place(x=50, y=40)

label = CTkLabel(master=root, text="Disk Tertipleýji", font=('Serif', 27)).place(x=270, y=2)

frame_disk = CTkFrame(master=root, width=10, height=10)
frame_disk.place(x=400, y=40)

path = ""

disks = [item.device for item in psutil.disk_partitions()]


# Get all files in directory
extentions = {'Aýdymlar': '.mp3, .wav, .m4a', 
                'Dokumentler': '.docx, .doc, .xlsx, .pdf', 
                'Suratlar': '.png, .jpg, .jpeg',
                'Wideolar': '.mp4, .ts, .webm',
                'Arhiwler': '.zip, .rar, .exe',
                }

def check_disks():
    global disks
    while True:
        temp_disks = [item.device for item in psutil.disk_partitions()]
        if temp_disks != disks:
            disks = temp_disks
            print(disks)
            disks_combobox.configure(values= disks)
        time.sleep(1)


def sort_folder():
    global path
    files = os.listdir(path)
    for file_name in files:
        # Get file extension
        _, file_extension = os.path.splitext(file_name)
        if file_extension:
            for dest, exts in extentions.items():
                if file_extension in exts:
                    if not os.path.exists(path+'/'+dest):
                        os.makedirs(path+'/'+dest)
                    shutil.move(os.path.join(path, file_name), os.path.join(path+'/'+dest, file_name))
    if empty_folder.get() or empty_folder_disk.get():
        try:
            delete_empty_folders(path)
        except Exception as e:
            print(e)
    mb.showinfo('Info', path+' Tertiplendi')

def sort_all_folder():
    global path
    for  root, folders, files in os.walk(path):
        for file_name in files:
            print(file_name)
            _, file_extension = os.path.splitext(file_name)
            if file_extension:
                for dest, exts in extentions.items():
                    if file_extension in exts:
                        if not os.path.exists(path+'/'+dest):
                            os.makedirs(path+'/'+dest)
                        shutil.move(os.path.join(path, root+'/'+file_name), os.path.join(path+'/'+dest, file_name))
    if empty_folder.get() or empty_folder_disk.get():
        try:
            delete_empty_folders(path)
        except Exception as e:
            print(e)
    mb.showinfo('Info', path+' Tertiplendi')

def delete_empty_folders(path):
    s=1
    while s==1:
        lean = False
        for root, dirs, files in os.walk(path):
            for dir in dirs:
                #Check if the directory is empty
                if len(os.listdir(os.path.join(root, dir))) == 0:
                    #Delete the directory
                    lean=True
                    os.rmdir(os.path.join(root, dir))
        if lean==False:
            s=0

def sort_callback():
    global extentions
    if eventt%2==0:
        extentions = {}
        if docs.get():
            extentions["Dokumentler"] =  ".docx, .doc, .xlsx, .pdf"
        if images.get():
            extentions["Suratlar"] = ".png, .jpg, .jpeg"
        if musics.get():
            extentions['Aýdymlar'] =  '.mp3, .wav, .m4a'
        if videos.get():
            extentions['Wideolar'] = '.mp4, .ts, .webm'
        if folder_name.get() and extensions_.get():
            extentions[folder_name.get()] = extensions_.get()
    print(extentions)
    if os_walk.get():
        sort_all_folder()
    else:
        sort_folder()

def sort_disk():
    global path, extentions
    path = disks_combobox.get()
    if eventt2%2==0:
        extentions = {}
        if docs2.get():
            extentions["Dokumentler"] =  ".docx, .doc, .xlsx, .pdf"
        if images2.get():
            extentions["Suratlar"] = ".png, .jpg, .jpeg"
        if musics2.get():
            extentions['Aýdymlar'] =  '.mp3, .wav, .m4a'
        if videos2.get():
            extentions['Wideolar'] = '.mp4, .ts, .webm'
        if folder_name2.get() and extensions_2.get():
            extentions[folder_name2.get()] = extensions_2.get()
    print(extentions)
    if os_walk_disk.get():
        sort_all_folder()
    else:
        sort_folder()

def select_folder():
    global path
    path = fd.askdirectory()
    button2.configure(state=NORMAL)
    label.configure(text=path.split('/')[-1:])

eventt = 1
frame_select_types = ""
docs=images=musics=videos=folder_name=extensions_=''
def sel_type():
    global eventt, frame_select_types, docs, images, musics, videos, folder_name, extensions_
    if eventt%2==1:
        frame_select_types = CTkFrame(master=frame_folder)
        docs = CTkCheckBox(master=frame_select_types, text="Dokumentler")
        docs.grid(row=0, column=0, pady=6, padx=10)
        images = CTkCheckBox(master=frame_select_types, text="Suratlar")
        images.grid(row=1, column=0, pady=6, padx=10)
        musics = CTkCheckBox(master=frame_select_types, text="Aýdymlar")
        musics.grid(row=2, column=0, pady=6, padx=10)
        videos = CTkCheckBox(master=frame_select_types, text="Wideolar")
        videos.grid(row=3, column=0, pady=6, padx=10)
        label = CTkLabel(master=frame_select_types, text="Aýratyn tertiple").grid(row=4, column=0)
        label = CTkLabel(master=frame_select_types, text="Papka ady:").grid(row=5, column=0)
        folder_name = CTkEntry(master=frame_select_types)
        folder_name.grid(row=5, column=1, pady=6, padx=10) 

        label = CTkLabel(master=frame_select_types, text="Giňeltmesi:").grid(row=6, column=0)
        extensions_ = CTkEntry(master=frame_select_types)
        extensions_.grid(row=6, column=1, pady=6, padx=10)  

        frame_select_types.grid(row=6, column=0, pady=6, padx=10)
        eventt+=1
    else:
        frame_select_types.destroy()
        eventt+=1

eventt2=1
frame_select_types2 = ""
docs2=images2=musics2=videos2=folder_name2=extensions_2=''
def sel_type_disk():
    global eventt2, frame_select_types2, docs2, images2, musics2, videos2, folder_name2, extensions_2
    if eventt2%2==1:
        frame_select_types2 = CTkFrame(master=frame_disk)
        docs2 = CTkCheckBox(master=frame_select_types2, text="Dokumentler")
        docs2.grid(row=0, column=0, pady=6, padx=10)
        images2 = CTkCheckBox(master=frame_select_types2, text="Suratlar")
        images2.grid(row=1, column=0, pady=6, padx=10)
        musics2 = CTkCheckBox(master=frame_select_types2, text="Aýdymlar")
        musics2.grid(row=2, column=0, pady=6, padx=10)
        videos2 = CTkCheckBox(master=frame_select_types2, text="Wideolar")
        videos2.grid(row=3, column=0, pady=6, padx=10)
        label2 = CTkLabel(master=frame_select_types2, text="Aýratyn tertiple").grid(row=4, column=0)
        label2 = CTkLabel(master=frame_select_types2, text="Papka ady:").grid(row=5, column=0)
        folder_name2 = CTkEntry(master=frame_select_types2)
        folder_name2.grid(row=5, column=1, pady=6, padx=10) 

        label = CTkLabel(master=frame_select_types2, text="Giňeltmesi:").grid(row=6, column=0)
        extensions_2 = CTkEntry(master=frame_select_types2)
        extensions_2.grid(row=6, column=1, pady=6, padx=10)  

        frame_select_types2.grid(row=5, column=0, pady=6, padx=10)
        eventt2+=1
    else:
        frame_select_types2.destroy()
        eventt2+=1

label = CTkLabel(master=frame_folder, text='Papka saýlanmadyk')
label.grid(row=1, column=0, pady=6, padx=10)
button = CTkButton(master=frame_folder, text='Papka saýlaň', command=select_folder).grid(row=2, column=0, pady=25, padx=10)

empty_folder = CTkCheckBox(master=frame_folder, text="Boş papkalar pozulsynmy")
empty_folder.grid(row=3, column=0, pady=6, padx=10)

os_walk = CTkCheckBox(master=frame_folder, text="Papkalaň içini hem tertiplesinmi")
os_walk.grid(row=4, column=0, pady=6, padx=10)

select_types = CTkButton(master=frame_folder, text="Tiplerini saýla", command=sel_type)
select_types.grid(row=5, column=0, pady=6, padx=10)

button2 = CTkButton(master=frame_folder, text='Tipine göra tertiple', command=sort_callback)
button2.grid(row=7, column=0, pady=6, padx=10)
button2.configure(state=DISABLED)


disks_combobox = CTkComboBox(master=frame_disk, values = disks)
disks_combobox.grid(row=1, column=0)

empty_folder_disk = CTkCheckBox(master=frame_disk, text="Boş papkalar pozulsynmy")
empty_folder_disk.grid(row=2, column=0, pady=6, padx=10)

os_walk_disk = CTkCheckBox(master=frame_disk, text="Papkalaň içini hem tertiplesinmi")
os_walk_disk.grid(row=3, column=0, pady=6, padx=10)

select_types_disk = CTkButton(master=frame_disk, text="Tiplerini saýla", command=sel_type_disk)
select_types_disk.grid(row=4, column=0, pady=6, padx=10)

button3 = CTkButton(master=frame_disk, text='Disk tertiple', command=sort_disk)
button3.grid(row=6, column=0, pady=25, padx=10)

thread = threading.Thread(target=check_disks)
thread.start()

root.mainloop()