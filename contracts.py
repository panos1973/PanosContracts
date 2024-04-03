import streamlit as st
import anthropic
import nltk
from find_data import read_docx, read_pdf
from create_embeddings import embed

client = anthropic.Anthropic(
    api_key=st.secrets["haiku_api"],
)


introductory_prompt = """
You are provided with a small part of a sample contract i made for another client with similar case and a current case file. 
I want you to read the current case and understand it and then make changes in the part of the contract according to the current case.
You donot have to worry about complete contract, i will provie you complete contarct in diferent parts so you can comlete that. so now just focus on chaning this part of the contract according to provided current case.
Also please utilize all tokens you can, do not hesitate to give long output as long as it is correct and important. Also only return the part of the contract not a single word other than that so that i will combine all updated contract parts and will make a new one.

"""

def chat_haiku(currentcase, sample_contract):
    message = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=4096,
    temperature=0.1,
    system="Respond only in Yoda-speak.",
    messages=[{"role": "user", "content": f"{introductory_prompt}\n\nThis is the current/new case:{currentcase}\n\n here is the part of old contract i want you to update according to above current case \n'{sample_contract}'\n\n Important: 'you must only reply the part of the contract not a single word other than that so that i will combine all updated and not updated parts of the contract and make a new one.'. "}],
        )

    return message.content[0].text



def contract_function(currentcasefile, sample_contractfile):
    if currentcasefile.type == "application/pdf":
            currentcase = read_pdf(currentcasefile)#if file is in pdf format this function will be called
    elif currentcasefile.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        currentcase = read_docx(currentcasefile)

    if sample_contractfile.type == "application/pdf":
            sample_contract = read_pdf(sample_contractfile)#if file is in pdf format this function will be called
    elif sample_contractfile.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        sample_contract = read_docx(sample_contractfile)

    
    # Tokenize the contract using nltk
    contract_tokens = nltk.word_tokenize(sample_contract)
    
    # Chunk the contract into parts with approximately 3000 tokens each
    chunk_size = 3000  # Define the size of each chunk
    contract_chunks = [contract_tokens[i:i + chunk_size] for i in range(0, len(contract_tokens), chunk_size)]
    
    updated_chunks = []
    
    # Iterate over each chunk, update it using Haiku, and collect the updated chunks
    for chunk in contract_chunks:
        # Convert chunk back to string
        chunk_text = ' '.join(chunk)
        
        # Update the chunk using Haiku
        updated_chunk = chat_haiku(currentcase, chunk_text)
        
        # Collect the updated chunk
        updated_chunks.append(updated_chunk)
    
    # Combine the updated chunks to form the updated contract
    updated_contract = ' '.join(updated_chunks)
    
    # Print the updated contract
    print(updated_contract)
    st.write(updated_contract)
