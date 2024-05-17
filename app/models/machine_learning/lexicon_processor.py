import pandas as pd
from collections import defaultdict
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

class LexiconProcessor:
    def __init__(self, lexicon_data:pd.DataFrame):
        self.lexicon_data = lexicon_data
        self.lexicon_dict, self.dialect_index = self._load_lexicon()

    def _load_lexicon(self):
        lexicon_data = self.lexicon_data
        lexicon_data['Tokenization'] = lexicon_data['Tokenization'].apply(lambda x: x.replace(' ', ''))
        lexicon_dict = defaultdict(list)
        for _, row in lexicon_data.iterrows():
            lexicon_dict[row['Tokenization']].append(row['Dialect'])

        all_dialects = sorted(set(sum(lexicon_dict.values(), [])))
        dialect_index = {dialect: idx for idx, dialect in enumerate(all_dialects)}

        return lexicon_dict, dialect_index

    def process_texts_batch(self, texts_batch):
        vectorizer = CountVectorizer(tokenizer=lambda x: x.split(), vocabulary=self.lexicon_dict.keys())
        X = vectorizer.fit_transform(texts_batch)
        features = np.zeros((len(texts_batch), len(self.dialect_index)), dtype=int)

        for word, idx in vectorizer.vocabulary_.items():
            for dialect in self.lexicon_dict[word]:
                features[:, self.dialect_index[dialect]] += X[:, idx].toarray().flatten()

        return features

    def preprocess_lexicon_features(self, texts, batch_size=1000):
        features = []
        for i in range(0, len(texts), batch_size):
            texts_batch = texts[i:i + batch_size]
            batch_features = self.process_texts_batch(texts_batch)
            features.append(batch_features)

        return np.vstack(features)
