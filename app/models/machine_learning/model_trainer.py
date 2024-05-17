import torch
from tqdm import tqdm
import numpy as np
import joblib

class ModelTrainer:
    def __init__(self, model, optimizer, criterion, device):
        self.model = model
        self.optimizer = optimizer
        self.criterion = criterion
        self.device = device
        self.model.to(self.device)

    def train_epoch(self, data_loader, epoch):
        self.model.train()
        losses = []
        correct_predictions = 0

        epoch_progress = tqdm(data_loader, desc=f"Training Epoch {epoch + 1}", leave=False)
        for batch in epoch_progress:
            input_ids = batch['input_ids'].to(self.device)
            attention_mask = batch['attention_mask'].to(self.device)
            labels = batch['label'].to(self.device)
            dialect_features = batch['dialect_features'].to(self.device)

            outputs = self.model(input_ids=input_ids, attention_mask=attention_mask, labels=labels, dialect_features=dialect_features)
            loss = outputs['loss']
            logits = outputs['logits']

            _, preds = torch.max(logits, dim=1)
            correct_predictions += torch.sum(preds == labels)
            losses.append(loss.item())

            loss.backward()
            self.optimizer.step()
            self.optimizer.zero_grad()

            epoch_progress.set_postfix({'loss': np.mean(losses), 'accuracy': correct_predictions.double() / len(data_loader.dataset)})

        return correct_predictions.double() / len(data_loader.dataset), np.mean(losses)

    def eval_model(self, data_loader):
        self.model.eval()
        losses = []
        correct_predictions = 0

        with torch.no_grad():
            eval_progress = tqdm(data_loader, desc="Evaluating", leave=False)
            for batch in eval_progress:
                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)
                labels = batch['label'].to(self.device)
                dialect_features = batch['dialect_features'].to(self.device)

                outputs = self.model(input_ids=input_ids, attention_mask=attention_mask, labels=labels, dialect_features=dialect_features)
                loss = outputs['loss']
                logits = outputs['logits']

                _, preds = torch.max(logits, dim=1)
                correct_predictions += torch.sum(preds == labels)
                losses.append(loss.item())

                eval_progress.set_postfix({'loss': np.mean(losses), 'accuracy': correct_predictions.double() / len(data_loader.dataset)})

        return correct_predictions.double() / len(data_loader.dataset), np.mean(losses)

    def save_model(self, model_save_path, label_encoder):
        joblib.dump(self.model, model_save_path)
        print(f"Model saved to {model_save_path}")
        label_encoder_path = model_save_path.replace('model', 'label_encoder')
        joblib.dump(label_encoder, label_encoder_path)
        print(f"LabelEncoder saved to {label_encoder_path}")
