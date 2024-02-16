# Coursework
So there's like, a lot of stuff to install/import
Note 1: This project is supported only on MacOS, and the installation steps will describe the setup for that operating system as such.
Note 2: This project was designed with Python 3.11.5, hence it is heavily recommended that you use Python 3.11.5 to run this project.
Note 3: As this project also uses TTS, you are encouraged to run this project with volume on.
Note 4: Do not press the "rerun" button (or the R key) when the site is running, especially on the Learner Mode, as it interferes with the flow of the code.

## Libraries to install
### Homebrew
If you do not have Homebrew installed, insert the following line into the terminal:

```/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"```

Install the following packages by entering into the terminal in this format: `brew install <package>`:
- portaudio
- flac

### pip

Install the following packages by entering into the terminal in this format: `pip install <package>`:
- langchain
- langchain-core
- langchain-openai
- SpeechRecognition
- pyttsx3
- py3-tts
- streamlit
- PyAudio

## To run the code:
- Open terminal
- Go to the folder directory for the coursework
- Run the following command: "streamlit run Translation\ Mode.py"
- If the program asks for permission to use your microphone at any point, accept it.
