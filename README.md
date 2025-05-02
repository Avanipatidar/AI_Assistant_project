# AI_Assistant_project
Luna Voice Assistant:-
Luna is a Python-based voice assistant capable of recognizing spoken commands, answering general queries using Google Gemini (Generative AI), reading the latest news, playing YouTube videos, and opening websites—all through voice interaction. It uses Google TTS for natural voice output and several powerful libraries like yt_dlp, speech_recognition, and pygame.

Features:-
Voice Activation: Activate the assistant with the wake word "Luna".
General Q&A: Uses Google Gemini (Generative AI) to respond to general queries.
Latest News: Fetch the latest news headlines via NewsAPI.
Play Music: Search and play songs or videos from YouTube using yt-dlp.
Open Websites: Open websites (e.g., "Open Google") through voice commands.
Voice Feedback: Provides voice responses using Google Text-to-Speech (gTTS) and plays them via pygame.

Requirements:-
Ensure you have Python 3.7+ installed. Then, install the required libraries:

Install Dependencies:-
pip install speechrecognition pygame gTTS requests yt-dlp google-generativeai
Additional Setup for pyaudio:-
The pyaudio library is required by speechrecognition. It might need specific installation steps depending on your OS:
pip install pyaudio

API Keys Required:-
Some features require external APIs, so you'll need to provide your API keys:

1. Google Gemini (Generative AI)
Obtain your API key from Google AI Studio.
Replace the placeholder GOOGLE_API_KEY in the aiProcess() function with your key.
2. NewsAPI
Get your API key from NewsAPI.
Replace the placeholder apiKey in the news-fetching section of the code with your key.

How Luna Works:-
1. Wake Word Detection
Luna listens for the wake word "Luna" to activate.

2. Command Processing
"Open Google" → Opens Google in your default browser.

"Play <song name>" → Searches YouTube and plays the first result.

"News" → Fetches the top 3 latest headlines from India.

Other Queries → Sent to Google Gemini for smart responses.

3. Speech Output
Luna provides verbal responses using Google Text-to-Speech (gTTS).
Audio is played back through pygame for smooth audio playback.

Example Commands:-
Here are a few example commands you can try with Luna:

"Luna" → Activates the voice assistant.

"Open Facebook" → Opens Facebook in the default web browser.

"Play Shape of You" → Searches for "Shape of You" on YouTube and plays the first video.

"What's the capital of France?" → Asks Google Gemini for the answer.

"News" → Fetches the latest headlines.

Notes:-
An internet connection is required for most features (e.g., API calls, TTS, YouTube video search).



