#https://www.youtube.com/watch?v=s_YUe0z09XU
from tkinter import *  
import tkinter.ttk as ttk   
from tkinter import filedialog
import time
import pygame
import os
from mutagen.mp3 import MP3
from tkinter import simpledialog

root = Tk()
root.title('Murali Mp3 Player')
#root.iconbitmap('')
pygame.mixer.init()
root.geometry('500x400')
#Initialize Pygame Mixer

#add_song function
def add_song():
    try:
        song = filedialog.askopenfilename(initialdir="audio/",title="Choose a Song",filetypes=(("mp3 Files","*.mp3"),))
        dirname = os.path.split(song)[0]
        song = song.split('/')[-1].replace('.mp3','')
        Song_Box.insert(END,song)
        lbl_work_Directory.config(text = dirname)
    except:
        pass
 
#add_manysong function
def add_many_songs():
    try:
        lst_songs = filedialog.askopenfilenames(initialdir="audio/",title="Choose a Song",filetypes=(("mp3 Files","*.mp3"),))
        lbl_work_Directory.config(text = os.path.split(lst_songs[0])[0])
        lst_songs = [x.split('/')[-1].replace('.mp3','') for x in lst_songs] 
        for song in lst_songs:
            Song_Box.insert(END,song)
    except:
        pass

#load existing playlist
def load_playlist():
    try:
        playlistfile  = filedialog.askopenfilename(initialdir="playlists/",title="Select a Playlist",filetypes=(("mp3 Files","*.txt"),))
        if playlistfile is not None:
            l_no = 0
            with open(playlistfile,'r') as fp:
                for song in fp:
                    if l_no == 0:
                        lbl_work_Directory.config(text = song.strip())
                        l_no = 1 
                    else:
                        Song_Box.insert(END,song.strip())
    except:
        pass

def save_playlist():
    try:
        #print('inside Save Playlist...')
        playlistName = simpledialog.askstring(title="Save PlayList ",prompt="Enter Playlist Name:")
        lst_items = Song_Box.get(0,END)
        filename = os.path.join(os.getcwd(),'playlists','{}.txt'.format(playlistName))
        with open(filename,'w') as fp:
            fp.write(lbl_work_Directory["text"] + '\n')
            for i in lst_items:
                fp.write(i + '\n')
    except:
        pass

def delete_song():
    try:
        stop()
        Song_Box.delete(ANCHOR)
        pygame.mixer.music.stop()
    except:
        pass
    

def delete_all_songs():
    try:
        stop()
        Song_Box.delete(0,END)
        pygame.mixer.music.stop()
    except:
        pass
 
#Grab song time info
def play_time():
    try:
        if stopped:
            return 
        #print('inside play_time')
        current_time = pygame.mixer.music.get_pos()/1000
        converted_current_time = time.strftime('%H:%M:%S',time.gmtime(current_time))
        #get current playing song
        song = Song_Box.get(ACTIVE)
        #song = os.path.join(os.getcwd(),'audio','{}.mp3'.format(song)) 
        song = os.path.join(lbl_work_Directory["text"],'{}.mp3'.format(song)) 
        song_mut = MP3(song)
        global song_length
        song_length = song_mut.info.length
        converted_song_length = time.strftime('%H:%M:%S',time.gmtime(song_length))
        current_time += 1
        if int(my_slider.get()) == int(song_length):
            status_bar.config(text=f' Time Elapsed : {converted_song_length} of {converted_song_length}  ')
            if chkvalue.get() == 1: #Default
                pass
            elif chkvalue.get() == 2: #PlayAll
                next_song()
            elif chkvalue.get() == 3: #Repeat
                repeat_again()            
        elif paused:
            pass
        elif int(my_slider.get()) == int(current_time):
            #update slider to position
            slider_position = int(song_length)
            my_slider.config(to=slider_position,value=int(current_time))
        else:
            #slider has moved 
            slider_position = int(song_length)
            my_slider.config(to=slider_position,value=int(my_slider.get()))
            converted_current_time = time.strftime('%H:%M:%S',time.gmtime(int(my_slider.get())))
            status_bar.config(text=f' Time Elapsed : {converted_current_time} of {converted_song_length}  ')
            next_time = int(my_slider.get()) + 1
            my_slider.config(value = next_time)
        status_bar.after(1000,play_time)
    except:
        pass


#play selected song 
def play():
    try:
        global stopped
        stopped = False
        global paused 
        paused  = False
        song = Song_Box.get(ACTIVE)
        #song = os.path.join(os.getcwd(),'audio','{}.mp3'.format(song))  
        song = os.path.join(lbl_work_Directory["text"],'{}.mp3'.format(song)) 
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        play_time()
    except:
        pass

def repeat_again():
    try:
        stop()
        play()
    except:
        pass

#stop selected song
global stopped
stopped = False

def stop():
    try:
        status_bar.config(text='')
        my_slider.config(value=0)
        pygame.mixer.music.stop()
        Song_Box.selection_clear(ACTIVE)
        status_bar.config(text="")
        global stopped
        stopped = True 
    except:
        pass

# play next song 
def next_song():
    try:
        #get curr song
        global stopped
        stopped = False
        status_bar.config(text='')
        my_slider.config(value=0) 
        try:
            next_one = Song_Box.curselection()[0] 
        except:
            next_one = 0
        if (Song_Box.size()-1)  == next_one:
            next_one = 0
        else:
            next_one = next_one + 1
        song = Song_Box.get(next_one)
        #song = os.path.join(os.getcwd(),'audio','{}.mp3'.format(song))  
        song = os.path.join(lbl_work_Directory["text"],'{}.mp3'.format(song)) 
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        #clear active bar in playlist 
        Song_Box.selection_clear(0,END)
        #activate  active bar in playlist 
        Song_Box.activate(next_one)
        Song_Box.selection_set(next_one,last=None)
    except:
        pass

# play prev song 
def prev_song():
    try:
        #print('inside prev song')
        #get curr song 
        global stopped
        stopped = False
        status_bar.config(text='')
        my_slider.config(value=0)
        try:
            prev_one = Song_Box.curselection()[0]
        except:
            prev_one =  Song_Box.size() -1
        #print('curr selection is {}'.format(prev_one))
        if prev_one == 0:
            prev_one = Song_Box.size() -1
            #print('Prev recrd if part is {}'.format(prev_one))
        else:
            prev_one = prev_one - 1
            #print('Prev recrd else part is {}'.format(prev_one))
        song = Song_Box.get(prev_one)
        #song = os.path.join(os.getcwd(),'audio','{}.mp3'.format(song)) 
        song = os.path.join(lbl_work_Directory["text"],'{}.mp3'.format(song)) 
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        #clear active bar in playlist 
        Song_Box.selection_clear(0,END)
        #activate  active bar in playlist 
        Song_Box.activate(prev_one)
        Song_Box.selection_set(prev_one,last=None)
    except:
        pass

def slide(x):
    try:
        #slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)} ')
        song = Song_Box.get(ACTIVE)
        #song = os.path.join(os.getcwd(),'audio','{}.mp3'.format(song)) 
        song = os.path.join(lbl_work_Directory["text"],'{}.mp3'.format(song))  
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0,start=int(my_slider.get()))
    except:
        pass
 
def save_session():
    try:
        pause(False)
        lst_items = Song_Box.get(0,END)
        song = Song_Box.get(ACTIVE)
        position = int(my_slider.get())
        sel_index  = Song_Box.curselection()[0]
        SessionName = simpledialog.askstring(title="Session Name",prompt="Enter Session Name:")
        filename = os.path.join(os.getcwd(),'system','{}.txt'.format(SessionName))
        with open(filename,'w') as fp:
            fp.write(lbl_work_Directory["text"] + '\n') #Dirname
            fp.write(song  + '\n')  #Active song
            fp.write(str(position) + '\n') #Current Position
            fp.write(str(sel_index) + '\n') #Selection Index
            for i in lst_items:
                fp.write(i + '\n')
    except:
        pass
 

def load_session():
    try:
        delete_all_songs()
        sessionlistfile  = filedialog.askopenfilename(initialdir="system/",title="Select a Session",filetypes=(("txt Files","*.txt"),))
        if sessionlistfile is not None:
            l_no = 0
            with open(sessionlistfile,'r') as fp:
                for song in fp:
                    l_no += 1
                    if l_no == 1:
                        lbl_work_Directory.config(text = song.strip())
                    elif l_no == 2:
                        active_song = song.strip() 
                    elif l_no == 3:
                        position = int(song.strip())  
                    elif l_no == 4:
                        selIndex = int(song.strip())                    
                    else:
                        Song_Box.insert(END,song.strip())
            active_song = os.path.join(lbl_work_Directory["text"],'{}.mp3'.format(active_song))  
            Song_Box.activate(selIndex)
            Song_Box.selection_set(selIndex,last=None)
            pygame.mixer.music.load(active_song)
            pygame.mixer.music.play(loops=0,start=position)
    except:
        pass 

#create global pause variable
global paused 
paused  = False
#pause/unpause  selected song 
def pause(is_paused):
    try:
        global paused
        paused = is_paused
        if paused:
            #unpause
            pygame.mixer.music.unpause()
            paused = False
            global stopped
            stopped = False
        else:
            #pause
            pygame.mixer.music.pause()
            paused = True
    except:
        pass
    
def volume(x):
    try:
        pygame.mixer.music.set_volume(volume_slider.get())
        #current_volume =pygame.mixer.music.get_volume()
    except:
        pass

master_frame = Frame(root)
master_frame.pack(pady=20)

#Create Playlist Box
Song_Box = Listbox(master_frame,bg="black",fg = "green",width=60,selectbackground="gray",selectforeground="black")
Song_Box.grid(row=0,column=0)

#create player control button Images 
back_btn_img = PhotoImage(file=os.path.join(os.getcwd(),'images','back50.png'))
forward_btn_img = PhotoImage(file=os.path.join(os.getcwd(),'images','forward50.png'))
play_btn_img = PhotoImage(file=os.path.join(os.getcwd(),'images','play50.png'))
pause_btn_img = PhotoImage(file=os.path.join(os.getcwd(),'images','pause50.png'))
stop_btn_img = PhotoImage(file=os.path.join(os.getcwd(),'images','stop50.png'))
 
# Create Player Control Frames
controls_frame  = Frame(master_frame)
controls_frame.grid(row=1,column=0,pady=20)

volume_frame  = LabelFrame(master_frame,text = "Volume")
volume_frame.grid(row=0,column=1,padx=20)
#create player control buttons
back_button = Button(controls_frame,image =back_btn_img ,borderwidth=0,command=prev_song)
forward_button = Button(controls_frame,image =forward_btn_img ,borderwidth=0,command=next_song)
play_button = Button(controls_frame,image =play_btn_img ,borderwidth=0,command=play)
pause_button = Button(controls_frame,image =pause_btn_img ,borderwidth=0,command=lambda: pause(paused))
stop_button  = Button(controls_frame,image =stop_btn_img ,borderwidth=0,command=stop)
 

back_button.grid(row=0,column=0,padx=10)
forward_button.grid(row=0,column=1,padx=10)
play_button.grid(row=0,column=2,padx=10)
pause_button.grid(row=0,column=3,padx=10)
stop_button.grid(row=0,column=4,padx=10)
 
#Create Menu
my_menu=Menu(root)
root.config(menu = my_menu)
#Add Addsong menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs",menu = add_song_menu)
add_song_menu.add_command(label="Add One Song to PlayList",command=add_song)
#Add Many Songs Menu
add_song_menu.add_command(label="Add Multiple Songs to PlayList",command=add_many_songs)

#remove song menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs",menu = remove_song_menu)
remove_song_menu.add_command(label="Delete a Song From PlayList",command=delete_song)
remove_song_menu.add_command(label="Delete all Songs From PlayList",command=delete_all_songs)

#Add Playlist menu
playlist_menu = Menu(my_menu)
my_menu.add_cascade(label="PlayLists",menu = playlist_menu)
playlist_menu.add_command(label="Load PlayList",command=load_playlist)
playlist_menu.add_command(label="Save PlayList",command=save_playlist)

#Add Session menu
Session_menu = Menu(my_menu)
my_menu.add_cascade(label="Save Session",menu = Session_menu)
Session_menu.add_command(label="Save Session",command=save_session)
Session_menu.add_command(label="Load Session",command=load_session)

#create status bar
status_bar = Label(root,text='',bd=1,relief=GROOVE,anchor=E)
status_bar.pack(fill=X,side=BOTTOM,ipady=2)
#create slider
my_slider = ttk.Scale(master_frame,from_=0,to=100,orient=HORIZONTAL,value=0,command=slide,length=360)
my_slider.grid(row=2,column=0,pady=10)
frameRadio = LabelFrame(master_frame, text='Play Options')
frameRadio.grid(row=3, column=0, padx=10)
chkvalue = IntVar()
radio_option1 = Radiobutton(frameRadio, text="Default", variable=chkvalue,value  = 1).grid(row=0, column=1)
radio_option2 = Radiobutton(frameRadio, text="PlayAll", variable=chkvalue,value  = 2).grid(row=0, column=2)
radio_option3 = Radiobutton(frameRadio, text="Repeat", variable=chkvalue,value  = 3).grid(row=0, column=3)
chkvalue.set(1)

lbl_work_Directory = Label(master_frame,text=os.path.join(os.getcwd(),'audio'))
lbl_work_Directory.grid(row=3,column=1,pady=10)
lbl_work_Directory.grid_forget()

volume_slider = ttk.Scale(volume_frame,from_=0,to=1,orient=VERTICAL,value=1,command=volume,length=125)
volume_slider.pack(pady=10)
root.mainloop()
