from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root=Tk()

root.title("ARGO-MP3 Player")
root.geometry("700x460")
#root.configure(background='gray')

#Initialize Pygame
pygame.mixer.init()


#Create Function to deal with time
def play_time():


	#Check to see if time is stopped

	if stopped:
		return 

	#Grab current song time
	current_time=pygame.mixer.music.get_pos()/1000
	#convert song time to time format
	converted_current_time=time.strftime('%H:%M:%S', time.gmtime(current_time))


	#reCONSTRUCTURE SONG WITH DIRECTORY STUFF
	song=playlist_box.get(ACTIVE)
	song=f'E:/RahulData/Projects/python/mp3/audio/{song}.mp3'

	#find current song length
	song_mut=MP3(song)
	global song_length
	song_length=song_mut.info.length

	#Convert to time format
	converted_song_length=time.strftime('%H:%M:%S', time.gmtime(song_length))

	#Check to see if song is over
	if int(song_slider.get()) == int(song_length):
		stop()


	elif paused:
		#Check to see if paused, if so..end
		pass
	else:
		#move slider along one sec at a time
		next_time=int(song_slider.get()) + 1
		#output new time value to slider, and to length of song
		song_slider.config(to=song_length,value=next_time)

		#Convert slider position to time format
		converted_current_time=time.strftime('%H:%M:%S', time.gmtime(int(song_slider.get())))
 
 		#Output slider
		status_bar.config(text=f'Time Elapsed : {converted_current_time} / {converted_song_length  }')

	#Add current time to status
	if current_time>=1:
		status_bar.config(text=f'Time Elapsed : {converted_current_time} / {converted_song_length  }')
	
	#Create loop to check the time every second
	status_bar.after(1000, play_time)

#Create Volume Function
def volume(x):
	pygame.mixer.music.set_volume(volume_slider.get())

#Create Song sldier function
def slide(x):
	
	#reCONSTRUCTURE SONG WITH DIRECTORY STUFF
	song=playlist_box.get(ACTIVE)
	song=f'E:/RahulData/Projects/python/mp3/audio/{song}.mp3'
	
	#LOAD SONG WITH PYGAME MIXER
	pygame.mixer.music.load(song)
	#PLAY ONG WITH PYGAME MIXER
	pygame.mixer.music.play(loops=0, start=song_slider.get())


#Create Function to add One song to playlist
def add_song():
	song=filedialog.askopenfilename(initialdir='audio/',title="Choose A Song!", filetypes=(("mp3 Files", "*.mp3"),))
	#strip out directory structure and .mp3 song title
	song=song.replace("E:/RahulData/Projects/python/mp3/audio/","")
	song=song.replace(".mp3","")
	#Add to end of playlist
	playlist_box.insert(END, song)

#create function to add many songs to playlist
def add_many_songs():
	songs=filedialog.askopenfilenames(initialdir='audio/',title="Choose A Song!", filetypes=(("mp3 Files", "*.mp3"),))
	
	#Loop through song names and replace directory structure and song name
	for song in songs:
		#strip out directory structure and .mp3 song title
		song=song.replace("E:/RahulData/Projects/python/mp3/audio/","")
		song=song.replace(".mp3","")
		#Add to end of playlist
		playlist_box.insert(END, song)

#Create Function to delete one song from playlist
def del_song():
	#Delete highlighted song from playlist...ANCHOR is the highlighted part
	playlist_box.delete(ANCHOR)

#Create Function to delete all songs from playlist
def del_all_songs():
	#delete All Songs 
	playlist_box.delete(0, END)

#Create Play Function
def play():
	#Set Stopped to false since a song is playing
	global stopped
	stopped=False
	#reCONSTRUCTURE SONG WITH DIRECTORY STUFF
	song=playlist_box.get(ACTIVE)
	song=f'E:/RahulData/Projects/python/mp3/audio/{song}.mp3'
	
	#LOAD SONG WITH PYGAME MIXER
	pygame.mixer.music.load(song)
	#PLAY ONG WITH PYGAME MIXER
	pygame.mixer.music.play(loops=0)

	# Get Song time
	play_time()


#Create Stopped function
global stopped
stopped=False
#Create Stop Function
def stop():
	#stop the song
	pygame.mixer.music.stop()
	#Clear active song selection bar
	playlist_box.selection_clear(ACTIVE)

	status_bar.config(text='')

	#Set our slider to zero
	song_slider.config(value=0)

	#Set stop variable to true
	global stopped
	stopped = True

#Create paused variable
global paused
paused = False

#Create Pause Function
def pause(is_paused):
	global paused
	paused=is_paused

	if paused:
		#unpause
		pygame.mixer.music.unpause()
		paused=False
	else:
		#pause
		pygame.mixer.music.pause()
		paused=True

#Create Forward function to play the next song
def next_song():
	#Reset slider position and status bar
	status_bar.config(text='')
	song_slider.config(value=0)

	#Get current song number
	next_one=playlist_box.curselection()
	#Add one to the current song number tuple/list
	next_one=next_one[0] + 1

	#Grab the song title from the playlist
	song=playlist_box.get(next_one)
	#Add directory structure stuff to the song title
	song=f'E:/RahulData/Projects/python/mp3/audio/{song}.mp3'

	#LOAD SONG WITH PYGAME MIXER
	pygame.mixer.music.load(song)
	#PLAY ONG WITH PYGAME MIXER
	pygame.mixer.music.play(loops=0)

	#Clear Active bar in playlist
	playlist_box.selection_clear(0, END)

	#Move active bar to the next song
	playlist_box.activate(next_one)

	#Set activate bar to next song
	playlist_box.selection_set(next_one, last=None)


def previous_song():
	#Reset slider position and status bar
	status_bar.config(text='')
	song_slider.config(value=0)


		#Get current song number
	next_one=playlist_box.curselection()
	#Add one to the current song number tuple/list
	next_one=next_one[0] - 1

	#Grab the song title from the playlist
	song=playlist_box.get(next_one)
	#Add directory structure stuff to the song title
	song=f'E:/RahulData/Projects/python/mp3/audio/{song}.mp3'

	#LOAD SONG WITH PYGAME MIXER
	pygame.mixer.music.load(song)
	#PLAY ONG WITH PYGAME MIXER
	pygame.mixer.music.play(loops=0)

	#Clear Active bar in playlist
	playlist_box.selection_clear(0, END)

	#Move active bar to the next song
	playlist_box.activate(next_one)

	#Set activate bar to next song
	playlist_box.selection_set(next_one, last=None)







#Create Main Frame
main_frame=Frame(root)
main_frame.pack(pady=20)

#Create Playlist box
playlist_box=Listbox(main_frame, bg="black", fg="green", width=80, height=15, selectbackground="green",selectforeground="white")
playlist_box.grid(row=0,column=0,padx=25)

#Create Volume slider frame
volume_frame=LabelFrame(main_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=18)


#Create Volume slider
volume_slider=ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=0.5, length=205, command=volume)
volume_slider.pack(pady=10)


#Create Song slider
song_slider=ttk.Scale(main_frame, from_=0, to=100, orient=HORIZONTAL, value=0, length=360, command=slide)
song_slider.grid(row=1,column=0,pady=20)

#Define Button images for Contro
back_btn_images=PhotoImage(file='images/back50.png')
forward_btn_images=PhotoImage(file='images/forward50.png')
play_btn_images=PhotoImage(file='images/play50.png')
pause_btn_images=PhotoImage(file='images/pause50.png')
stop_btn_images=PhotoImage(file='images/stop50.png')

#Create Button frame
control_frame=Frame(main_frame)
control_frame.grid(row=2,column=0,pady=5)

#Create Play/stop etc buttons
back_button=Button(control_frame, image=back_btn_images ,borderwidth=0, command=previous_song)
forward_button=Button(control_frame, image=forward_btn_images,borderwidth=0, command=next_song)
play_button=Button(control_frame, image=play_btn_images,borderwidth=0, command=play)
pause_button=Button(control_frame, image=pause_btn_images,borderwidth=0, command=lambda: pause(paused))
stop_button=Button(control_frame, image=stop_btn_images,borderwidth=0, command=stop)


back_button.grid(row=0,column=0 ,padx=10)
forward_button.grid(row=0,column=1,padx=10)
play_button.grid(row=0,column=2,padx=10)
pause_button.grid(row=0,column=3,padx=10)
stop_button.grid(row=0,column=4,padx=10)

#Create Main Menu
my_menu=Menu(root)
root.config(menu=my_menu)

#Create Menu Dropdowns
add_song_menu=Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
#Add one song to playlist
add_song_menu.add_command(label="Add One Song", command=add_song)
#Add Many Songs to playlist
add_song_menu.add_command(label="Add Multiple Songs", command=add_many_songs)

#Create delete song menu
remove_song_menu=Menu(my_menu,tearoff=0)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A Song from Playlist", command=del_song)
remove_song_menu.add_command(label="Delete All Songs from Playlist", command=del_all_songs)

#Create Status bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=CENTER, fg="white",bg="gray")
status_bar.pack(fill=X, side=BOTTOM, ipady=8)


root.mainloop()