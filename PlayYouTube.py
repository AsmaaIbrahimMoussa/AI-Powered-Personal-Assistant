import pywhatkit        
def play_song(text):             
    song = text.replace('play', "") 
    print('playing'+ song)        
    pywhatkit.playonyt(song) 
