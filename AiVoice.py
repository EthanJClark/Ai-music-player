# %%
import openai
import os

import dspy

from dotenv import load_dotenv
load_dotenv()

# %%
import sounddevice as sd
import soundfile as sf
import io
import speech_recognition as sr

# %%
wake_word = "hey computer"



# %%
def start_assistant(text, voice= "alloy",save_to_file=False):
    with openai.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=text,
        # style="angry"
    ) as response: 
        if save_to_file:
            response.stream_to_file("output.wav")
        else:
            audio_bytes = b"".join(chunk for chunk in response.iter_bytes())
                
            
            data, samplerate = sf.read(io.BytesIO(audio_bytes), dtype='float32')
            sd.play(data, samplerate)
            sd.wait()  # Wait until file is done playing

# %%
def wake_word_listener():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    while True:
        with mic as source:
            print("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source)

            try:
                text = recognizer.recognize_google(audio).lower()
                if wake_word in text:
                    start_assistant("hello! how can i assist you?")
                    break
            except sr.UnknownValueError:
                pass


# %%
if __name__ == "__main__":
    start_assistant("[speak like a narrator]. Hello! welcome to AI Lalapalooza", voice= "alloy", save_to_file=True)  # Test the assistant
    print("done")


# %%
