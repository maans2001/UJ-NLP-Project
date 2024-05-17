import streamlit as st
from transformers import BertTokenizer
from models.machine_learning.lexicon_processor import LexiconProcessor
from models.machine_learning.model_predictor import ModelPredictor
from models.machine_learning.bert_with_lexicon import BertWithLexicon
from datasets.datasets import madar_lexicon_dataset
from datasets.datasets import preprocess_text as clean_text
from pathlib import Path
import torch

# Paths
CWD = Path(__file__).parents[0]

model_path_gpu = CWD / Path("../models/machine_learning/static/model_best.joblib")
model_path_cpu = CWD / Path("../models/machine_learning/static/model_best_cpu.joblib")
model_path = model_path_gpu if torch.cuda.is_available() else model_path_cpu

label_encoder_path = CWD / Path("../models/machine_learning/static/label_encoder.joblib")

# Define the directory where the flags are stored
flags_dir = CWD / Path('./flags')

# Define the city mapping with Arabic names, country codes, and country names
city_mapping = {
    'ALE': {'city': 'حَلَب', 'country': 'sy', 'country_name': 'سوريا'},
    'ALG': {'city': 'الجَزَائِر', 'country': 'dz', 'country_name': 'الجزائر'},
    'ALX': {'city': 'الإِسْكَنْدَرِيَّة', 'country': 'eg', 'country_name': 'مصر'},
    'AMM': {'city': 'عَمَّان', 'country': 'jo', 'country_name': 'الأردن'},
    'ASW': {'city': 'أَسْوَان', 'country': 'eg', 'country_name': 'مصر'},
    'BAG': {'city': 'بَغْدَاد', 'country': 'iq', 'country_name': 'العراق'},
    'BAS': {'city': 'البَصْرَة', 'country': 'iq', 'country_name': 'العراق'},
    'BEI': {'city': 'بَيْرُوت', 'country': 'lb', 'country_name': 'لبنان'},
    'BEN': {'city': 'بَنْغَازِي', 'country': 'ly', 'country_name': 'ليبيا'},
    'CAI': {'city': 'القَاهِرَة', 'country': 'eg', 'country_name': 'مصر'},
    'DAM': {'city': 'دِمَشْق', 'country': 'sy', 'country_name': 'سوريا'},
    'DOH': {'city': 'الدَّوْحَة', 'country': 'qa', 'country_name': 'قطر'},
    'FES': {'city': 'فَاس', 'country': 'ma', 'country_name': 'المغرب'},
    'JED': {'city': 'جِدَّة', 'country': 'sa', 'country_name': 'السعودية'},
    'JER': {'city': 'القُدْس', 'country': 'ps', 'country_name': 'فلسطين'},
    'KHA': {'city': 'الخُرْطُوم', 'country': 'sd', 'country_name': 'السودان'},
    'MOS': {'city': 'المَوْصِل', 'country': 'iq', 'country_name': 'العراق'},
    'MSA': {'city': 'فصحى', 'country': 'arl', 'country_name': 'الدول العربية'},  # Arab League flag for Modern Standard Arabic
    'MUS': {'city': 'مَسْقَط', 'country': 'om', 'country_name': 'عمان'},
    'RAB': {'city': 'الرِّبَاط', 'country': 'ma', 'country_name': 'المغرب'},
    'RIY': {'city': 'الرِّيَاض', 'country': 'sa', 'country_name': 'السعودية'},
    'SAL': {'city': 'السَّلْط', 'country': 'jo', 'country_name': 'الأردن'},
    'SAN': {'city': 'صَنْعَاء', 'country': 'ye', 'country_name': 'اليمن'},
    'SFX': {'city': 'صَفَاقُس', 'country': 'tn', 'country_name': 'تونس'},
    'TRI': {'city': 'طَرَابُلُس', 'country': 'ly', 'country_name': 'ليبيا'},
    'TUN': {'city': 'تُونِس', 'country': 'tn', 'country_name': 'تونس'}
}

def machine_learning_app():
    st.title('برنامج تحديد اللهجات (Machine Learning)')

    # User input for the text to be predicted
    user_input = st.text_input("ادخل نص:")

    if st.button("حدد اللهجة"):
        with st.spinner("جاري تحديد اللهجة..."):
            # Load BERT tokenizer
            tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')

            # Preprocess lexicon data
            lexicon_processor = LexiconProcessor(madar_lexicon_dataset)
            lexicon_dict = lexicon_processor.lexicon_dict
            dialect_index = lexicon_processor.dialect_index

            # Create predictor
            predictor = ModelPredictor(model_path, label_encoder_path, lexicon_dict, dialect_index, tokenizer)

            # Make prediction
            predicted_label_confidences = predictor.predict_single_text(clean_text(user_input))
            # Sort the dictionary by values in descending order
            sorted_labels = sorted(predicted_label_confidences.items(), key=lambda item: item[1], reverse=True)

            # Separate top three predictions and the rest
            top_three = sorted_labels[:3]
            others = sorted_labels[3:]

            # Combine the confidence of the remaining labels into one "other" category
            other_confidence = sum(confidence for _, confidence in others)

            # Display the highest predicted value as the header
            highest_label, highest_confidence = top_three[0]
            highest_city_info = city_mapping[highest_label]
            highest_city_name = highest_city_info['city']
            highest_country_code = highest_city_info['country']
            highest_country_name = highest_city_info['country_name']
            highest_flag_path = flags_dir / f"{highest_country_code}.png"

            st.image(str(highest_flag_path), width=64)
            st.markdown(f"## {highest_country_name} - {highest_city_name}")
            st.markdown("---")

            # Display the top three predictions
            st.markdown("## أفضل ٣ تنبؤات")
            for label, confidence in top_three:
                city_info = city_mapping[label]
                city_name = city_info['city']
                country_code = city_info['country']
                country_name = city_info['country_name']
                flag_path = flags_dir / f"{country_code}.png"
                confidence_percentage = confidence * 100

                st.markdown(f"### {country_name} - {city_name} ({confidence_percentage:.2f}%)")
                st.image(str(flag_path), width=64)
                st.markdown("---")

            # Display the "other" category
            other_confidence_percentage = other_confidence * 100
            st.markdown(f"### اخرى ({other_confidence_percentage:.2f}%)")
            st.image(str(flags_dir / "arl.png"), width=64)  # Assuming Arab League flag for "other"
            st.markdown("---")

# Run the Streamlit app
if __name__ == "__main__":
    machine_learning_app()
