import re
import speech_recognition as sr
import webbrowser
import edge_tts
import asyncio
import pygame
import os
import time
import musicLibrary
import requests
from groq import Groq

r = sr.Recognizer()

pygame.mixer.init()
newsapi = "YOUR_NEWS_API_KEY"

async def speak_async(text):
    print(f"Jarvis: {text}")

    communicate = edge_tts.Communicate(
        text=text,
        voice="en-US-AndrewNeural",
        rate="+15%"
    )

    await communicate.save("voice.mp3")

    pygame.mixer.music.load("voice.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.1)

    pygame.mixer.music.unload()

    os.remove("voice.mp3")


def speak(text):
    asyncio.run(speak_async(text))

def speak_response(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)

    for sentence in sentences:
        sentence = sentence.strip()

        if sentence:
            speak(sentence)

def aiProcess(command):
    client = Groq(
        api_key="YOUR_GROQ_API_KEY"
    )

    stream = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        max_completion_tokens=100,
        stream=True,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Jarvis, a voice assistant. "
                    "Keep every answer short, natural and under 3 sentences unless the user asks for details."
                )
            },
            {
                "role": "user",
                "content": command
            }
        ]
    )

    response = ""

    for chunk in stream:
        if chunk.choices[0].delta.content:
            text = chunk.choices[0].delta.content
            print(text, end="", flush=True)
            response += text

    print()  # Move to a new line after streaming output
    return response

    

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open github" in c.lower():
        webbrowser.open("https://github.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        pygame.mixer.music.stop()
        webbrowser.open(link)
    
    elif "news" in c.lower():
        speak("Fetching the latest headlines.")
        # FIX 1 & 2: Changed 'r' to 'response' to protect the microphone, and added 'f'
        response = requests.get(
    f"https://newsapi.org/v2/everything?q=India&sortBy=publishedAt&language=en&apiKey={newsapi}"
        )
        print(response.status_code)
        print(response.text)
        if response.status_code == 200:
            # Phrase the JSON response
            data = response.json()

            # Extract the articles
            articles = data.get('articles', [])

            # Print the headlines
            for article in articles[:3]:
                title = article["title"]
                print("Speaking:", title)
                speak(title)                
    else:
        output = aiProcess(c)
        print(output)
        speak_response(output)

        start = time.time()
        output = aiProcess(c)
        print("AI:", time.time() - start)

        start = time.time()
        speak_response(output)
        print("TTS:", time.time() - start)

if __name__ == "__main__":
    speak("Initializing Jarvis...")

    
    while True:

        #Listen for the wake world Jarvis
        #obtain audio from the microphone
        
        
        
        # Recognize speech using Sphinx
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=1)
                print("Listening...")
                audio = r.listen(source, timeout = 5, phrase_time_limit = 5)
                
            word = r.recognize_google(audio)
            if "jarvis" in word.lower():
                speak("Yes sir")
                #Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    print(command)
                    
                    processCommand(command)
        except  Exception as e:
            print("Error; {0}".format(e))
            

