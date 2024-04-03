import streamlit as st
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


    
# Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message['content'])

# Check if both files are uploaded and set a flag in the session state
if 'contract_ready' not in st.session_state:
    st.session_state.contract_ready = False



if __name__ == "__main__":
    

    st.sidebar.title("Contract functionality only for testing")
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
