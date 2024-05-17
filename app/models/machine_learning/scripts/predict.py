from transformers import BertTokenizer
from ..lexicon_processor import LexiconProcessor
from ..model_predictor import ModelPredictor
from ....datasets.datasets import madar_lexicon_dataset
from pathlib import Path
# Paths
CWD = Path(__file__).parents[0]

model_path = CWD / Path("../static/model_best.joblib")
label_encoder_path = CWD / Path("../static/label_encoder.joblib")

# Load BERT tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')

# Preprocess lexicon data
lexicon_processor = LexiconProcessor(madar_lexicon_dataset)
lexicon_dict = lexicon_processor.lexicon_dict
dialect_index = lexicon_processor.dialect_index

# Create predictor
predictor = ModelPredictor(model_path, label_encoder_path, lexicon_dict, dialect_index, tokenizer)

# Example new input text
new_text = "ازيك يا باشا"

# Make prediction
prediction = predictor.predict_single_text(new_text)
print(f"Predicted label: {prediction}")
