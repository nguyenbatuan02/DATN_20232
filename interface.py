import streamlit as st
import torch
import torch.nn as nn
import numpy as np
from transformers import AutoConfig, AutoTokenizer, MBartForConditionalGeneration
from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments, DataCollatorForSeq2Seq
#from utils.preprocess import *
from rouge import Rouge     
import wandb
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

tokenizer = AutoTokenizer.from_pretrained('vinai/bartpho-word-base', add_eos_token=True, padding_side='right')
model = MBartForConditionalGeneration.from_pretrained('/kaggle/input/finetune-bartpho2/Checkpoint Bartpho/checkpoint-9000',
                                                     torch_dtype=torch.bfloat16,
                                                    #quantization_config=bnb_config, # If you need 
                                                    device_map="auto",
                                                    use_cache=True,)
tokenizer.pad_token = tokenizer.eos_token

def split_passage(passage, max_tokens=900):
    # Split the passage into chunks with approximately max_tokens per chunk
    chunks = []
    current_chunk = ""
    current_tokens = 0
    
    for word in passage.split():
        word_tokens = len(tokenizer.tokenize(word))
        if current_tokens + word_tokens <= max_tokens:
            current_chunk += " " + word
            current_tokens += word_tokens
        else:
            chunks.append(current_chunk.strip())
            current_chunk = word
            current_tokens = word_tokens
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def split_pass(text):
    return re.split(r'(?=(Theo|Căn cứ|Tại khoản, Tại điều))', text)

def find_introduction_phrase(text):
    match = re.search(r'((Theo|Căn cứ).*?(quy định|như sau))', text)
    if match:
        return match.group(0)
    return ""
def replace_unk_with_newline(text):
    # Replace <unk> with newline characters
    cleaned_text = text.replace("<unk>", "\n")
    return cleaned_text

def fin_answer(passage, answer):
    #answer = answer.replace("</s> <s> ", "").strip("</s>")
    sub_passages = split_pass(passage)
    vectorizer = TfidfVectorizer().fit_transform(sub_passages + [answer])
    vectors = vectorizer.toarray()

    # Tính toán độ tương tự cosine giữa câu trả lời và các đoạn văn bản
    cosine_similarities = cosine_similarity(vectors[-1].reshape(1, -1), vectors[:-1])
    similarity_scores = cosine_similarities[0]
     #for i, score in enumerate(similarity_scores):
        #print(f"Đoạn {i+1}: {score}")
    # Tìm đoạn văn bản có độ tương tự cao nhất
    most_similar_index = similarity_scores.argmax()
    max_score = similarity_scores[most_similar_index]
    if max_score > 0.3:
        #relevant_passage = sub_passages[most_similar_index]
        relevant_passage = sub_passages[most_similar_index]
        # Tìm cụm từ giới thiệu trong đoạn văn bản liên quan
        intro_phrase = find_introduction_phrase(relevant_passage)

        # Kết hợp cụm từ giới thiệu với câu trả lời
        final_answer = intro_phrase + ": " + answer if intro_phrase else answer
        
    else: 
         final_answer = 'Không tìm thấy thông tin câu trả lời'
    return final_answer


st.title("Law Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
with st.form(key='my_form'):
    question = st.text_input("Nhập câu hỏi")
    context = st.text_area("Nhập ngữ cảnh")
    submit_button = st.form_submit_button(label='Gửi')

PROMPT = """
Trả lời câu hỏi: {input} dựa trên đoạn văn sau: {in}. \n
Nếu không tìm thấy thông tin câu trả lời, hãy trả lời là bạn không biết
"""
question = question
passage = context
text = PROMPT.format_map({
    'in': split_passage(passage)[0],
    'input': question,
})
input_ids = tokenizer(text, return_tensors='pt', add_special_tokens=False).to('cuda')
generated_ids = model.generate(
    input_ids=input_ids['input_ids'],
    max_new_tokens=1024,
    do_sample=True,
    top_p=0.95,
    top_k=40,
    temperature=0.3,
    repetition_penalty=1.1,
    no_repeat_ngram_size=7,
    num_beams=5,
)
generated_answer = tokenizer.batch_decode(generated_ids)[0]
generated_answer = generated_answer.replace("</s> <s> ", "").strip("</s>")
generated_answer = replace_unk_with_newline(generated_answer)
#print(generated_answer)
answer = fin_answer(passage, generated_answer)

if submit_button and question and context:
    # Display user question and context in chat message container
    with st.chat_message("user"):
        st.markdown(f"**Câu hỏi:** {question}\n\n**Ngữ cảnh:** {context}")
    # Add user question and context to chat history
    st.session_state.messages.append({"role": "user", "content": f"**Câu hỏi:** {question}\n\n**Ngữ cảnh:** {context}"})


    # Here you would call your model or processing function to get the answer
    # For demonstration, we will just echo the context and question
    response = f"**AI luật:** \n\n {answer}"

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})