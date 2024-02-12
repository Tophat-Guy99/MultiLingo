import streamlit as st
st.set_page_config(
    page_title = "MultiLingo",
    page_icon = "🗣️",
)

st.sidebar.header("Translate Mode") 
st.sidebar.write("Translate from language to language.")
st.title("Tri Lingo")
st.write("Breaking the bariers for language.") 
trf = st.selectbox('Translate From',
                         ('English 🇬🇧', 'Chinese 🇨🇳', 'French 🇫🇷', 'Spanish 🇪🇸'))

trt = st.selectbox('Translate To',
                         ('English 🇬🇧', 'Chinese 🇨🇳', 'French 🇫🇷', 'Spanish 🇪🇸'))
if trf == trt:
    st.error("Please change selection as selection cannot be the same.")
else:
    sot = st.selectbox('Text Or Speach',
                         ('Text 💬', 'Speach 🗣'))

    if sot == 'Text 💬':
        multitext = st.text_area("Text to Translate",
                         placeholder="Enter some text")
    else :
        if st.button('Click me and start speaking'):
            st.write("Speach") 
            print("This appears in the terminal") 
            st.error("This is an intentional error output")
    

    if st.button("Translate"):
        st.write("Translate") 
        print("This appears in the terminal") 
        st.error("This is an intentional error output")



