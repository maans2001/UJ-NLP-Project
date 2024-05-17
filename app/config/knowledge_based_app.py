import streamlit as st
from models.knowledge_based.ngram_model import NgramModel
from models.knowledge_based.sentence_completer import SentenceCompleter
from datasets.datasets import madar_corpus_dataset
from datasets.datasets import preprocess_text as clean_text

import random

# Load and prepare the dataset
sentences = madar_corpus_dataset['sent'].tolist()
tokens_list = [sentence.split() for sentence in sentences]
max_n = 3
ngram_model = NgramModel(tokens_list, max_n)
sentence_completer = SentenceCompleter(ngram_model)

def knowledge_based_app():
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>برنامج خمن الكلمة الجاية (Knowledge Based)</h1>", unsafe_allow_html=True)

    # Placeholder for user input
    user_input = st.text_input("أدخل جملة:")

    col1, col2 = st.columns([3, 1])
    with col1:
        num_words = st.slider("عدد الكلمات المراد تخمينها:", min_value=1, max_value=10, value=1)
    # Placeholder for the output
    output_placeholder = st.empty()

    with col2:
        if st.button("عشوائي"):
            num_words = random.randint(1, 5)
            completed_sentence = sentence_completer.complete_sentence(clean_text(user_input), num_words)
            output_placeholder.markdown(f"<h2 style='color: #FF5733; font-size: 30px; text-align: center;'>{completed_sentence}</h2>", unsafe_allow_html=True)


    if st.button("كلمة عشوائية"):
        user_input = random.choice(sentences)
        num_words = random.randint(1, 5)
        output_placeholder.markdown(f"<h2 style='color: #FF5733; font-size: 30px; text-align: center;'>{user_input}</h2>", unsafe_allow_html=True)

    if st.button("خمن الكلمات الجاية"):
        completed_sentence = sentence_completer.complete_sentence(clean_text(user_input), num_words)
        output_placeholder.markdown(f"<h2 style='color: #FF5733; font-size: 30px; text-align: center;'>{completed_sentence}</h2>", unsafe_allow_html=True)

