import json
from difflib import get_close_matches
import tkinter as tk
from tkinter import messagebox
import pyttsx3 
from gtts import gTTS
from playsound import playsound
import pygame
import os
import time

pygame.init()
pygame.mixer.init()

data=json.load(open('dictionary_compact.json'))

file_count = 0

speech_playing = False

def translate(word):
    word = word.lower()
    possible = get_close_matches(word, data.keys(), n=3)
    if word in data:
        return data[word]
    elif possible:
        new_word = messagebox.askquestion("Word not found!", f"Word not found! Would you like to try these? {possible}").lower()
        if new_word == 'yes': 
            new_wordz=input({possible}).lower()
            return data[new_wordz]
        else:
            return "Word doesn't exist."
    else:
        return "Word doesn't exist."
    

# search button click event
def on_search():
 word = entry_word.get()
 definition = translate(word)
 label_definition.config(state=tk.NORMAL)
 label_definition.delete('1.0', tk.END)
 label_definition.insert(tk.END, definition)
 label_definition.config(state=tk.DISABLED)

# clear button click event
def on_clear():
    if speech_playing:
        pygame.mixer.music.stop()

    entry_word.delete(0, tk.END)
    label_definition.config(state=tk.NORMAL)
    label_definition.delete('1.0', tk.END)
    label_definition.config(state=tk.DISABLED)

    pygame.time.wait(500)

    for file in os.listdir():
        if file.startswith("output_voice_"):
            os.remove(file)

def on_sound():
    global speech_playing
    global file_count
    if not speech_playing:
        word = entry_word.get()
        definition = translate(word)
        
        # Split definition into chunks of 100 words each
        words = definition.split()
        chunks = [words[i:i+50] for i in range(0, len(words), 50)] #reduce chunks to reduce the delay
        
        for i, chunk in enumerate(chunks):
            chunk_definition = ' '.join(chunk)
            tts = gTTS(text=chunk_definition, lang='en')
            filename = f"output_voice_{file_count}_{i}.mp3"
            tts.save(filename)
            playsound(filename)
            os.remove(filename)  # Delete the temporary file
            
            # Short delay between chunks
            pygame.time.delay(500)
            
        speech_playing = True
        file_count += 1
    else:
        speech_playing = False

def on_exit():
    res=messagebox.askyesno('Confirm','Do you want to exit?')
    if res==True:
        window.destroy()
    else:
        pass
    


#sound button click event
#def on_sound():
 #word = entry_word.get()
 #engine = pyttsx3.init()
 #engine.say(translate(word))
 #engine.runAndWait()


#main window
window = tk.Tk()
window.title("Dictionary")
window.geometry("800x600")  

#word input
label_word = tk.Label(window, text="Enter a word:")
label_word.pack(pady=5)
entry_word = tk.Entry(window)
entry_word.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

#definiton
frame_definition = tk.Frame(window, bd=1, relief=tk.SOLID)
frame_definition.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(frame_definition)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

label_definition = tk.Text(frame_definition, wrap=tk.WORD, yscrollcommand=scrollbar.set)
label_definition.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=label_definition.yview)

#buttons
frame_buttons = tk.Frame(window)
frame_buttons.pack(side="top", pady=5)

button_search = tk.Button(frame_buttons, text="Search", command=on_search)
button_search.pack(side="left", padx=5, fill=tk.BOTH)

button_clear = tk.Button(frame_buttons, text="Clear", command=on_clear)
button_clear.pack(side="left", padx=5, fill=tk.BOTH)

button_sound = tk.Button(frame_buttons, text="Sound", command=on_sound)
button_sound.pack(side="left", padx=5, fill=tk.BOTH)

button_exit = tk.Button(frame_buttons, text="Exit", command=on_exit)
button_exit.pack(side="left", padx=5, fill=tk.BOTH)

frame_buttons.pack_configure(anchor="center")


window.mainloop()