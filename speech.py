import speech_recognition as sr
history_list=[]
def recog(audio,r):
    try:    
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
        spoken_text=r.recognize_google(audio)
        return spoken_text
        # print("You said: " + spoken_text)
        # app.addLabel("You said: " + r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        # app.addLabel("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        # app.addLabel("Could not request results from Google Speech Recognition service; {0}".format(e))

def press_record():
    # app.addLabel("You pressed the button")
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # app.addLabel("Say something!")
        print("Say something!")
        audio = r.listen(source)
    text=recog(audio,r)
    return text
