from torch.utils.data import Dataset
import torch

class DialectDataset(Dataset):
    def __init__(self, texts, labels, lexicon_features, tokenizer, max_length):
        self.texts = texts
        self.labels = labels
        self.lexicon_features = lexicon_features
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        lexicon_feature = self.lexicon_features[idx]

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

        dialect_features = torch.tensor(lexicon_feature, dtype=torch.float)

        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'label': torch.tensor(label, dtype=torch.long),
            'dialect_features': dialect_features
        }
