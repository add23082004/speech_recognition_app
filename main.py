import streamlit as st
from gtts import gTTS
import speech_recognition as sr
from google.cloud import speech_v1p1beta1 as speech
import os

def transcribe_speech(api_choice, language_choice):
    # Initialize speech client for Google Cloud Speech
    if api_choice == "Google Cloud":
        client = speech.SpeechClient()

    # Initialize recognizer class
    r = sr.Recognizer()

    # Reading Microphone as source
    with sr.Microphone() as source:
        st.info("Speak now...")

        # listen for speech and store in audio_text variable
        audio_text = r.listen(source)
        st.info("Transcribing...")

        try:
            if api_choice == "Google Cloud":
                # using Google Cloud Speech Recognition
                text = transcribe_google_cloud(client, audio_text, language_choice)
            else:
                # using gTTS for text-to-speech synthesis
                text = r.recognize_google(audio_text)
                tts = gTTS(text=text, lang=language_choice)
                tts.save("output.mp3")
                os.system("start output.mp3")

            return text

        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError as e:
            return f"Error connecting to the API: {e}"

def transcribe_google_cloud(client, audio_text, language_choice):
    audio_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_choice,
    )

    response = client.recognize(
        config=audio_config,
        audio={"content": audio_text.get_wav_data()},
    )

    return response.results[0].alternatives[0].transcript

def main():
    st.title("Speech Recognition App")
    st.write("Click on the microphone to start speaking:")

    # User selects Speech Recognition API
    api_choice = st.selectbox("Select Speech Recognition API", ["Google", "Google Cloud"])

    # User selects language
    language_choice = st.selectbox("Select Language", ["en-US", "es-ES"])  # Add more languages as needed

    # add a button to trigger speech recognition
    if st.button("Start Recording"):
        text = transcribe_speech(api_choice, language_choice)
        st.write("Transcription: ", text)

    # add a button to stop recording
    if st.button("Stop Recording"):
        st.stop()

if __name__ == "__main__":
    main()
