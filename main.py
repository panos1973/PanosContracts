import streamlit as st
from chat import update_chat, show_chat_history, save_and_reset
from gpt_4 import chat_with_GPT4
from gpt_3 import chat_with_GPT3
from gemini_pro import chat_with_Gemini, read_pdf, read_docx
from find_data import find_relevant_files
from claude3_haiku import chat_with_Claude3
from contracts import contract_function
import pandas as pd



st.set_page_config(page_title='Legal Bot', layout='wide')

# Add custom styles
st.markdown("""
    <style>

.st-dn {
    caret-color: rgb(247 248 255);
}
   
h6 {
  font-family: "Source Sans Pro", sans-serif;
  font-weight: 600;
  color: rgb(255,255,255);
  padding: 0px 0px 1rem;
  margin: 0px;
  line-height: 1.2;
}    

.st-bs {
  color: #000000;
}
small {
  color: #ffffff !important;
}

[data-testid="main-menu-list"]{
    background-color: #3c3c3c;
    color: white !important;
}

code {
    color: rgb(0 0 0);
    overflow-wrap: break-word;
}

[data-testid="stChatInput"]{
    background-color: #f0f2f6;
}

[data-testid="stSidebar"]{
    background-color: #3c3c3c;
    color: white !important;
    width: 300px !important;
}
[data-testid="chatAvatarIcon-assistant"]{
    background-color: rgb(138,138,138) !important;,,
}


::-webkit-scrollbar {
    background: #fffefe;
    border-radius: 100px;
    height: 6px;
    width: 6px;
}

p, ol, ul, dl {
    margin: 0px 0px 1rem;
    margin-bottom: 1rem;
    padding: 0px;
    font-size: 1rem;
    font-weight: 400;
    color: white;
    background-color: #3c3c3c !important;
}

.st-ck {
    background-color: #3c3c3c;
}

    h1 {
  font-family: "Source Sans Pro", sans-serif;
  font-weight: 600;
  color: rgb(255,255,255);
  padding: 1.25rem 0px 1rem;
  margin: 0px;
  line-height: 1.2;
}

button, select {
  text-transform: none;
  background-color: rgb(60,60,60) !important;
}

[data-testid="stChatMessage"]{
    color: black !important;
    background-color: #3c3c3c;
}

[data-testid="stFileUploadDropzone"]{
    color: white !important;
}

[data-testid="stImage"]{
    padding-top: 0px;
}
[aria-activedescendant="bui21val-1"]{
    background-color: #3c3c3c !important;
}

    </style>
""", unsafe_allow_html=True)



logo = "300px.png"
st.sidebar.image(logo, use_column_width=True)

# Option to choose from Gemini or GPT
chat_choice = st.sidebar.radio("Επιλέξτε Μοντέλο:", ["GPT-3.5 Turbo", "GPT-4 Turbo", "Claude-3 Haiku", "Gemini-Pro"])
if chat_choice == "GPT-4 Turbo":
    st.header("GPT-4 Turbo")
elif chat_choice == "GPT-3.5 Turbo":
    st.header("GPT-3.5 Turbo")
elif chat_choice == "Gemini-Pro":
    st.header("Gemini-Pro")
elif chat_choice == "Claude-3 Haiku":
    st.header("Claude-3 Haiku")


# If chat is not started yet
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
                        "content": "Παρακαλώ επιλέξτε ένα ΑΙ μοντέλο (αριστερά), και ανεβάστε ένα αρχείο με την περιγραφή της τρέχουσας υπόθεσής σας. \n\n Θα σας συνιστούσα η περιγραφή να είναι όσο πιο αναλυτική γίνεται προκειμένου να μπορέσω να έχω περισσότερα δεδομένα ώστε να εμβαθύνω στην ανάλυσή μου. \n\n\nΣημειώστε ότι το αρχείο μπορεί να είναι σε μορφή docx ή pdf.\n\n\n"
        }
    ]


# New Chat Button
if st.sidebar.button("Νέο Chat"):
    save_and_reset(st.session_state.messages)
    st.session_state.messages = []
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Παρακαλώ επιλέξτε ένα ΑΙ μοντέλο (αριστερά), και ανεβάστε ένα αρχείο με την περιγραφή της τρέχουσας υπόθεσής σας. \n\n Θα σας συνιστούσα η περιγραφή να είναι όσο πιο αναλυτική γίνεται προκειμένου να μπορέσω να έχω περισσότερα δεδομένα ώστε να εμβαθύνω στην ανάλυσή μου. \n\n\nΣημειώστε ότι το αρχείο μπορεί να είναι σε μορφή docx ή pdf.\n\n\n"
        }
    ]

    
# Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message['content'])

# Check if both files are uploaded and set a flag in the session state
if 'contract_ready' not in st.session_state:
    st.session_state.contract_ready = False



if __name__ == "__main__":
    
    # Check if the session state variable 'file_updated' exists, if not, initialize it as False
    if 'uploaded_files' not in st.session_state:
        st.session_state.find_files = False
        st.session_state.uploaded_files=None

    # File uploading feature
    st.sidebar.title("Αρχείο")
    uploaded_file = st.sidebar.file_uploader("Ανεβάστε το αρχείo της τρέχουσας υπόθεσης", accept_multiple_files=False, type=['pdf', 'docx'])
    if not uploaded_file:
        st.session_state.find_files=True
        st.session_state.uploaded_files=None

    if uploaded_file and st.session_state.find_files:
        with st.sidebar:
            with st.spinner("Ψάχνουμε τα σχετικά αρχεία"):    
                st.session_state.uploaded_files = find_relevant_files(uploaded_file)
                st.session_state.find_files=False

    update_chat()
    st.sidebar.title("Click here to use contract functionality")
    #if st.button("Create Contracts"):
    # Upload sample contract
    sample_contract = st.sidebar.file_uploader("Upload your sample contract here", key="sample_contract", type=['pdf', 'docx'])

    # Upload current case
    current_case = st.sidebar.file_uploader("Upload your current case here", key="current_case", type=['pdf', 'docx'])

    # Check if both files are uploaded and update the session state flag
    if sample_contract and current_case:
        st.session_state.contract_ready = True

    # Button to generate new contract, only enabled when both files are uploaded
    if st.sidebar.button("Generate new contract", disabled=not st.session_state.contract_ready):
        with st.spinner("Processing..."):
            # Call the contract function with both files
            contract_function(current_case, sample_contract)
            # Reset the session state flag for the next use
            st.session_state.contract_ready = False

    st.sidebar.title("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    # Microsoft partner logo
    logo2 = "MS_Startups.png"
    st.sidebar.image(logo2, use_column_width=True)
    print("Uploaded files = ")
    # Select chatting model according to user choice
    if st.session_state.uploaded_files:
        if chat_choice == "GPT-4 Turbo":
            chat_with_GPT4(st.session_state.uploaded_files)
        elif chat_choice == "Gemini-Pro":
            chat_with_Gemini(st.session_state.uploaded_files)
        elif chat_choice == "GPT-3.5 Turbo":
            chat_with_GPT3(st.session_state.uploaded_files)
        elif chat_choice == "Claude-3 Haiku":
            chat_with_Claude3(st.session_state.uploaded_files)
