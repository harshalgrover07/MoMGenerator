import os
import streamlit as st
from click import prompt
import google.generativeai as genai
import streamlit as st
from pdfextractor import text_extractor
from wordextractor import doc_text_extractor
from image2text import extract_text_image

# Lets configure Genai model
gemini_key = gemini_api_key = os.getenv('Google_API_Key2')
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-2.5-flash-lite',
                              generation_config={'temperature':0.9}
                              )

# 🔽 ADD UI STYLE BLOCK HERE (RIGHT BELOW IMPORTS)
st.markdown("""
<style>
/* ---- Global ---- */
html, body, [class*="css"] {
    font-family: "Segoe UI", sans-serif;
}
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: #ffffff;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1f2933, #111827);
    padding-top: 2rem;
}
[data-testid="stFileUploader"] {
    border: 2px dashed #60a5fa;
    border-radius: 12px;
    padding: 16px;
}
.stButton button {
    background: linear-gradient(90deg, #3b82f6, #22c55e);
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)


# Lets create the sidebar

st.sidebar.title(':rainbow[Upload Your Notes]')
st.sidebar.subheader(':blue[Only Uplaod Images,PDFs and DOCX]')
user_file = st.sidebar.file_uploader('Upload your file here:',
                                     type=['pdf','jpg','jfif','png','docx','jpeg'])

if user_file:
    st.sidebar.success('File uploaded successfully')
    if user_file.type == 'application/pdf':
        user_text = text_extractor(user_file)

    elif user_file.type in ['image/png','image/jpeg','image/jpg','image/jfif']:
        user_text = extract_text_image(user_file)

    elif user_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        user_text=doc_text_extractor(user_file)

    else:
        st.sidebar.error('Enter the correct file type')


    
# Lets create Main Page
st.title(':orange[MoM Generator:-] :blue[AI Assisted Minutes of meeting Generator]')
st.subheader(':green[This Application creates generalized minutes of meetings from the handwritten notes.]')
st.write('''
Follow The Steps:-
1. Upload the notes in PDF,DOCX or Imagr format in sidebar.
2. Click "Generate" to generate the MoM.
''')

if st.button('Generate'):
    with st.spinner(':blue[Please wait....]'):
        prompt=f'''
        <Role> Your an expert in writing and formating minutes of meeting.
        <Goal> Create minutes of meetings from the notes that user has provided.
        <Context> The user has provided some rough notes as text.Here are the notes:{user_text}
        <Format> The Output must follow the below format.
        * Title: Assume Title of the meeting.
        * Agenda : Assume Agenda of the meeting.
        * Attendees: Name of the attendes (if name of the attendes is not there keep it in N/A.)
        * Date and Place : date and the place of the meeting.(If not provided keep it Online.)
        * Body : The body should follow the following sequence of points.
            * Key points discussed.
            * Highlight any decision that has been taken.
            * Mention Actionable Items.
            * Mention any deadline if discussed.
            * Mention Next meeting date if discused.
            * Add a 2-3 Line of summary.
        <Instruction>
            * Use Bullet points and highlight the important keywords by making them bold .
            * Generate the output in docx format'''
        

        response = model.generate_content(prompt)
        st.write(response.text)

        if st.download_button(label='Download',
                           data=response.text,
                           file_name='MoM_generated.txt',
                           mime='text/plain'):
            st.success('Your File has been Downloaded')
        