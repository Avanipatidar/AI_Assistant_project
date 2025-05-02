# Import necessary modules
import speech_recognition as sr  # For converting speech to text
import webbrowser                # To open URLs in the default web browser
# import pyttsx3                 # (Commented out) Optional: offline TTS engine
import requests                  # To send HTTP requests (e.g., NewsAPI)
import google.generativeai as genai  # For accessing Google Gemini AI
import yt_dlp                    # YouTube downloader library, used for searching
from gtts import gTTS            # Google Text-to-Speech for audio responses
import pygame                    # To play audio (MP3)
import os                        # For file operations (like deleting temp files)

# Google TTS-based speaking function (slow but natural sounding)
def speak(text):
    tts = gTTS(text)                     # Convert text to speech
    tts.save('temp.mp3')                # Save it as an MP3 file
    pygame.mixer.init()                 # Initialize pygame audio mixer
    pygame.mixer.music.load('temp.mp3') # Load the MP3 file
    pygame.mixer.music.play()          # Play the audio
    while pygame.mixer.music.get_busy():  # Wait until playback is done
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()        # Unload the audio file
    os.remove("temp.mp3")              # Delete the temp MP3 file

# Process general questions using Google Gemini
def aiProcess(command):
    try:
        GOOGLE_API_KEY = "AIzaSyD-2QZvJ7DmUVFAMYc4rcw9gYIHZpzFzf8"  # Your Gemini API key
        genai.configure(api_key=GOOGLE_API_KEY)                   # Configure Gemini API
        model = genai.GenerativeModel("gemini-1.5-flash")         # Load Gemini model

        # Generate a short response with low randomness
        response = model.generate_content(
            command,
            generation_config=genai.GenerationConfig(
                max_output_tokens=75,
                temperature=0.1
            )
        )
        return response.text   # Return Gemini's response as plain text
    except Exception as e:
        return f"Sorry, I encountered an error: {e}"  # Handle any errors

# Handle specific voice commands
def processCommand(c):
    # Check if command is to open a specific website
    if "open google" in c.lower():
        webbrowser.open("http://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("http://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("http://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("http://linkedin.com")
    elif "open unstop" in c.lower():
        webbrowser.open("http://unstop.com")
    elif "open" in c.lower():
        try:
            # Extract site name from the command
            site = c.lower().split("open ")[1]
             # List of common domain extensions to try
            domain_extensions = [".com",".org", ".net", ".in", ".edu", ".gov", ".co", ".io", ".info", ".biz", ".ai"]
            # Try each domain extension until one works
            for extension in domain_extensions:
                url = f"http://{site}{extension}"  # Construct the URL
                try:
                    webbrowser.open(url)  # Attempt to open the URL
                    speak(f"Opening {site}")
                    return  # Exit the loop once a valid URL is opened
                except:
                    continue  # Try the next domain extension
            
        except:
            speak("Sorry, I couldn't open that website.")

    # If user says "play", search and play a YouTube video
    elif c.lower().startswith("play"):
        try:
            song = c.lower().split("play ")[1]         # Extract song title
            ydl_opts = {
                'quiet': True,
                'extract_flat': True,
                'force_generic_extractor': True,
            }

            # Search YouTube using yt_dlp
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(f"ytsearch:{song}", download=False)
                if 'entries' in result:
                    video_url = result['entries'][0]['url']  # Get first result
                    speak(f"Playing {song}")                # Speak confirmation
                    webbrowser.open(video_url)              # Open video in browser
                else:
                    speak("Sorry, I couldn't find that song.")  # If not found
        except Exception as e:
            speak(f"Sorry, I couldn't play that song. Error: {e}")  # Handle errors

    # If user asks for news
    elif "news" in c.lower():
        try:
            from datetime import datetime, timedelta

            # Get yesterday's date for fresh news
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

            # Make a GET request to NewsAPI for fetching the latest news
            response = requests.get(
                "https://newsapi.org/v2/everything",
                params={
                    "q": "India",  # General query for Indian news
                    "from": yesterday,  # Fetch news from the last 24 hours
                    "sortBy": "publishedAt",  # Sort by the most recent articles
                    "apiKey": "b76b66ceb98242dcac3d74b528c188f3",
                    "pageSize": 3,  # Limit to 3 articles
                    "language": "en"  # Fetch English news
                }
            )
            articles = response.json().get('articles', [])
            #Converts the API response (in JSON format) into a Python dictionary.
            # Key: 'articles' contains a list of news articles.
            # Default Value: If 'articles' is not found, it defaults to an empty list ([]).
            if articles:
                for article in articles:
                    speak(article.get('title', 'No title available'))  # Speak each headline
            else:
                speak("No fresh news available at the moment.")
        except Exception as e:
            speak(f"Sorry, I couldn't fetch the news. Error: {e}")
    else:
        # If command doesn't match any above, send it to Gemini
        output = aiProcess(c)
        speak(output)

# Main voice assistant loop
if __name__ == "__main__":
    speak("initializing luna...")     # Welcome message
    while True:
        r = sr.Recognizer()           # Create recognizer instance
        print("listening...")
        try:
            with sr.Microphone() as source:
                print("recognizing...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)  # Listen for wake word
                word = r.recognize_google(audio)                          # Convert speech to text

            if word.lower() == "luna":                                    # Check wake word
                speak("ya")                                               # Acknowledge activation
                with sr.Microphone() as source:
                    print("luna Active...")
                    audio = r.listen(source)                              # Listen to full command
                    command = r.recognize_google(audio)                   # Convert to text
                processCommand(command)                                   # Execute command

        except Exception as e:
            print("Error; {0}".format(e))                                 # Catch & print errors
