import streamlit as st
import time
st.set_page_config( # configures the default settings of the app (MUST INCLUDE)
    page_title="Hello", # Obviously the title of the page, must include. This appears at the top of the browser.
    page_icon="👋", # This is an optional parameter for if you want an emoji icon or anything supported by st.image
)
st.sidebar.header("Main Page") # For multiple pages and requiring a sidebar, this is useful if you want to label the inside of your sidebar
st.sidebar.write("Welcome, have a look around, and don't forget to check the source code for useful explanations.")
st.title("App Name") # This is the title of the page
st.write("Transcending language barriers") # This is a general purpose function, but for strings it outputs the markdown text to the app
selectbox = st.selectbox('Selection Option', # This is a selection box, it is a dropdown that allow the user to pick an option. This first parameter is a string to indicate what it is about.
                         ('A', 'B', 'C') # These are the options, again, also strings. The options are put inside a tuple, which is basically a list but with () brackets
                         ) # You can put this in one line, I just separated it to make it easier to see.

# To evaluate the what the option for selection box is (and other choices too, assume the variable is a string. The exception is the st.multiselect input, which uses a list)

options = st.multiselect( # This is a multiple selection box, functions similarly to the above box, but allows multiple options. Instead of a tuple, the
    'What are your favorite colors',
    ['Green', 'Yellow', 'Red', 'Blue'],
    ['Yellow', 'Red'])
st.write('You selected:', options)

if st.button("Click me"): # This creates a button called "Translate", the if statement fires whenever the button is pressed
    st.write("Hello!") # Displays hello. Spamming this button will not make a lot of hello words, because all previous text written is cleared and removed when the button is pressed
    print("This appears in the terminal") # Regular output and other python functions still work
    st.error("This is an intentional error output") # This is used to make a red error message, useful for input validation (example: input and output languages are the same)

def multiplechoicecontainer(): # You can put streamlit stuff into a function, this is very useful if you want certain elements to only show when they press a button and make it neat (e.g: learner mode quiz)
    multiplechoice = st.radio( # This is basically the "multiple choice selection" contruct
        "This is a question?", # This is the question parameter, takes in a string
        [":rainbow[Answer 1]", "***Answer 2***", "Answer 3"], #Use a list of strings for each option. (SIDENOTE: MARKUP TEXT WORKS FOR THE STRINGS, YOU CAN USE BOLD AND ITALICS AND ETC)
        captions = ["Caption", "Another caption", "Quippy MCU joke"] # Captions are an optional feature for st.radio, it gives small text captions below every option, use a list of strings in order
    )

    if multiplechoice == "Answer 3": # This will change depending on the current state of the option selection. For learner mode I suppose you can remove this and just have a submit button at the bottom.
        st.write("Selected 3")
        st.write("another text")
    else:
        st.write("Selected other")
multiplechoicecontainer() # Don't forget to fire the function


if 'unique' in st.session_state and st.session_state.unique == True: # these are session state things, treat them as variables that update in real time with button click
    st.session_state.running = True # They will be used for the following slowbutton to prevent input while the function is running
else:
    st.session_state.running = False

slowbutton = st.button('make slow function', disabled=st.session_state.running, key="unique")  #another button, with a disabled parameter to disable it while the spinner loads
# By the way, if there are multiple widgets of the same name (first parameter), it is best to assign them a unique key to avoid giving an error, as shown above
if slowbutton: #another way of execution a function
    st.session_state.disabledslowbutton = True
    #placeholder.button('make slow function', disabled=True, key="disabled")
    with st.spinner('Wait for it...'): # This makes a loading spinner that lasts until the function ends. # It also disables any input written below it unless that stuff is wrapped in a function
        debouncetoggle = True
        time.sleep(5) # just an example of a delay
    st.session_state.output = 'slowbuttonfinished' # Another session state variable, used to save the outcome of this function because of the next line
    st.rerun() # This resets the button, removing any output. This means that to output, you must save any output and put it in another function
if 'output' in st.session_state:
    st.success('Done!') # This is just to show green text to indicate that something was successful
    # This will be erased when the slowbutton is pressed again


if st.button("warning and info"):
    st.warning("this is a warning") # This is a yellow box to indicate a warning
    st.info("this is information") # This is a blue box to indicate information

def toggleandslider():

    toggle = st.toggle("Disable slider input", #Label of the toggle
                   False) # Default value of the toggle
    number = st.slider('How old are you?', # This is a number slider. The first parameter is the title/question string
                   0, # Minimum value
                   130, # Maximum value
                   25, # This is the value that first appears when the slider is first rendered. The default value is the minimum value
                   step=5, #optional step interval, remember that ALL NUMBER VALUES MUST BE OF THE SAME TYPE, EITHER INT OR FLOAT
                   disabled=toggle) # This is the disabled parameter, it disables input if it is set to True. This can be used for any input object, such as text input or selectionboxes. Do note that you must either reference another widget (like toggle), or use a session state variable that updates in real time (it's like Swift)
    st.write("The number is: " + str(number))

    color = st.select_slider( # This is similar to the number slider, but with fixed selection options instead
        'Select a color of the rainbow',
        options=['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet'],
        disabled=toggle)
    st.write('This color is:', color)
toggleandslider()

singletext = st.text_input('Text Label', # This is a single-line text input
                           "i was here", # This is an optional second parameter, text that appears when first rendered
                           placeholder="Enter some text") # Optional parameter, displays text that appears when nothing is inside
st.write('The current text is', singletext)

multitext = st.text_area("Text to input", # This functions the same way, but allows for paragraph indentations
                         placeholder="Enter some text")

number = st.number_input('Add or subtract', #numerical input, basically a counter
                         0.0, #optional minimum value
                         10.0, #optional maximum value
                         5.0, #optional value that first appears when widget is first rendered, default is minimum value or 0.
                         step=0.25 #optional interval, float
                         )

option = st.checkbox('I pledge my allegiance to God Emperor LKY') # Basic optional checkbox

if option:
    st.write('You clicked on the checkbox!')

st.link_button("For more information and additional helpful features, check the source code, The Other Side, or click this button to go to the API reference.", "https://docs.streamlit.io/library/api-reference")
