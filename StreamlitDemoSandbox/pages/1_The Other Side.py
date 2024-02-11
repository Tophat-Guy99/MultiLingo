import streamlit as st
import time
st.set_page_config( # configures the default settings of the app (MUST INCLUDE)
    page_title="The Other Side", # Obviously the title of the page, must include. This appears at the top of the browser.
)
st.sidebar.header("The Other Side")

st.title("The Other Side") # This is the title of the page
st.write("Welcome, this is another page!") # This is a general purpose function, but for strings it outputs text to the app

st.info("To allow for multiple pages in Streamlit, make a folder called 'pages', and put it in the same directory as your main page. Then, name your page to the format '#_Name', where # is the number. For our coursework, we only need the number '1'. But for reference, if there are multiple extra pages, then use other numbers to order them. Naming the files is important, their name appears up inside the sidebar.")

st.header("This is a header") #explanatory
st.subheader("This is a subheader") #explanatory
st.caption("snarky text") #explanatory
st.divider() # Horiztonal rule, like the one in Notion
st.markdown("*This text is in italics.* **But this text is in bold.** ***This text is both of them.*** ~~And this text is crossed out.~~") #Outputs markdown text

code = '''def hello():
    print("Hello, Streamlit!")'''
st.code(code, language='python') # This is how to display code nicely in streamlit
