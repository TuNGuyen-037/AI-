from gtts import gTTS
import os
import playsound
language = 'vi'
def speak(text):
    print("Bot: {}".format(text))
    #truyen vao text de doc len
    tts = gTTS(text=text, lang=language, slow = False)
    tts.save("sound.mp3")
    playsound.playsound("sound.mp3", False)
    os.remove("sound.mp3")
# Test
speak('Bạn khỏe không ?')
def stop():
    speak("Hẹn gặp lại bạn nhé!")