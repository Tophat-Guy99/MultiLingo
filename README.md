# Coursework
So there's like, a lot of stuff to install/import

## Libraries to install (at least what I had to do)
So the following libraries to install (using "pip install <name>" in terminal)
- python-dotenv
- langchain
- SpeechRecognition
- pyttsx3
- py3-tts (came across an error, had to do this to get tts working)

## If it still doesn't work even though you installed it
Now for some reason even though I've install this stuff on my mac it doesn't work in vscode so what I had to do was:
- Go into vscode
- Create a virtual environment (cmd + shift + p)
- Select .venv
- Select days_1_2_requirements.txt
- Any warnings should go away
Keep in mind that this only works in vscode, this does NOT work in IDLE. Maybe my macbook libraries are just screwed up, so someone else test the first option to see if it works.

## env files
So at the moment once you've opened up the folder, create a new text file called "env", and inside it, you'll put an API key inside that.
Copy paste the following: OPENAI_API_KEY=""
Inside those quotation marks is where you'll put the API key. Since OpenAI is watching us, when we get the API key we'll strictly keep it confidential (write it down on paper and hold onto that paper for you life?)
