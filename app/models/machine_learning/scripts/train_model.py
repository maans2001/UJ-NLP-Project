from transformers import BertTokenizer
from torch.utils.data import DataLoader
import torch
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
from ....datasets.datasets import madar_lexicon_dataset,madar_corpus_dataset
from ..lexicon_processor import LexiconProcessor
from ..dialect_dataset import DialectDataset
from ..bert_with_lexicon import BertWithLexicon
from ..model_trainer import ModelTrainer
from pathlib import Path

if __name__ == '__main__':
    CWD = Path(__file__).parents[0]

    model_path = CWD / Path("../static/model_best.joblib")
    label_encoder_path = CWD / Path("../static/label_encoder.joblib")

    # Load data

    madar_corpus = madar_corpus_dataset

    # Preprocess lexicon data
    lexicon_processor = LexiconProcessor(madar_lexicon_dataset)

    # Load BERT tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')

    # Preprocess the text and labels
    max_length = 128
    label_encoder = LabelEncoder()
    encoded_labels = label_encoder.fit_transform(madar_corpus['lang'])

    # Save label encoder
    joblib.dump(label_encoder,label_encoder_path)

    # Split the data
    X_train, X_temp, y_train, y_temp = train_test_split(madar_corpus['sent'], encoded_labels, test_size=0.3, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

    # Generate lexicon features
    train_lexicon_features = lexicon_processor.preprocess_lexicon_features(X_train.tolist())
    val_lexicon_features = lexicon_processor.preprocess_lexicon_features(X_val.tolist())
    test_lexicon_features = lexicon_processor.preprocess_lexicon_features(X_test.tolist())

    # Create datasets
    train_dataset = DialectDataset(X_train.tolist(), y_train.tolist(), train_lexicon_features, tokenizer, max_length)
    val_dataset = DialectDataset(X_val.tolist(), y_val.tolist(), val_lexicon_features, tokenizer, max_length)
    test_dataset = DialectDataset(X_test.tolist(), y_test.tolist(), test_lexicon_features, tokenizer, max_length)

    # Create data loaders
    batch_size = 8
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=4, pin_memory=True, prefetch_factor=2)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, num_workers=4, pin_memory=True, prefetch_factor=2)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, num_workers=4, pin_memory=True, prefetch_factor=2)

    # Load BERT model for sequence classification
    num_dialects = len(lexicon_processor.dialect_index)
    model = BertWithLexicon.from_pretrained('bert-base-multilingual-cased', num_dialects=num_dialects, num_labels=len(label_encoder.classes_))
    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
    criterion = torch.nn.CrossEntropyLoss()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # Create trainer
    trainer = ModelTrainer(model, optimizer, criterion, device)

    # Training loop with early stopping
    epochs = 11
    best_accuracy = 0
    patience = 3
    patience_counter = 0
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=2, verbose=True)

    for epoch in range(epochs):
        train_acc, train_loss = trainer.train_epoch(train_loader, epoch)
        val_acc, val_loss = trainer.eval_model(val_loader)
        scheduler.step(val_loss)

        print(f"Epoch {epoch + 1}/{epochs} - Train loss: {train_loss:.4f}, Train accuracy: {train_acc:.4f}, Val loss: {val_loss:.4f}, Val accuracy: {val_acc:.4f}")

        if val_acc > best_accuracy:
            best_accuracy = val_acc
            patience_counter = 0
            trainer.save_model(model_path, label_encoder)
        else:
            patience_counter += 1

        if patience_counter >= patience:
            print("Early stopping")
            break

    # Evaluate on test set
    accuracy, test_loss = trainer.eval_model(test_loader)
    print(f"Test loss: {test_loss:.4f}, Test accuracy: {accuracy:.4f}")
