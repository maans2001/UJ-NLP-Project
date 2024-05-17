import torch
import numpy as np
import joblib
from sklearn.feature_extraction.text import CountVectorizer
import torch.nn.functional as F
class ModelPredictor:
    def __init__(self, model_path, label_encoder_path, lexicon_dict, dialect_index, tokenizer, max_length=128):
        self.model = joblib.load(model_path)
        self.label_encoder = joblib.load(label_encoder_path)
        self.lexicon_dict = lexicon_dict
        self.dialect_index = dialect_index
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)

    def preprocess_single_text(self, text):
        vectorizer = CountVectorizer(tokenizer=lambda x: x.split(), vocabulary=self.lexicon_dict.keys())
        X = vectorizer.fit_transform([text])
        features = np.zeros((1, len(self.dialect_index)), dtype=int)

        for word, idx in vectorizer.vocabulary_.items():
            for dialect in self.lexicon_dict[word]:
                features[0, self.dialect_index[dialect]] += X[:, idx].toarray().flatten()

        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            return_token_type_ids=False,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )

        dialect_features = torch.tensor(features, dtype=torch.float)
        input_ids = encoding['input_ids']
        attention_mask = encoding['attention_mask']

        return {
            'input_ids': input_ids.flatten(),
            'attention_mask': attention_mask.flatten(),
            'dialect_features': dialect_features.flatten()
        }

    def predict_single_text(self, text):
        self.model.eval()
        data = self.preprocess_single_text(text)
        input_ids = data['input_ids'].unsqueeze(0).to(self.device)
        attention_mask = data['attention_mask'].unsqueeze(0).to(self.device)
        dialect_features = data['dialect_features'].unsqueeze(0).to(self.device)

        with torch.no_grad():
            outputs = self.model(input_ids=input_ids, attention_mask=attention_mask, dialect_features=dialect_features)
            logits = outputs['logits']
            # Apply softmax to get probabilities
            probs = F.softmax(logits, dim=1)

            # Get confidence scores for each class
            confidences = probs.squeeze().cpu().numpy()

            # Map the indices to dialect labels
            dialect_confidences = {self.label_encoder.inverse_transform([i])[0]: float(confidence) for i, confidence in enumerate(confidences)}
            return dialect_confidences
