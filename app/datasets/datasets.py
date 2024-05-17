import re
from pyarabic import araby
from pathlib import Path
import pandas as pd

CWD = Path(__file__).parents[0]
MADAR_CORPUS_DIR = CWD / Path("static/MADAR.Parallel-Corpora-Public-Version1.1-25MAR2021/MADAR_Corpus")
LEXICON_PATH     = CWD / Path("static/MADAR_Lexicon_v1.0/MADAR_Lexicon_v1.0.tsv")
def preprocess_text(text):
    def remove_arabic_punctuation(text):
        arabic_punctuation = """`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!?"…"–"""
        translator = str.maketrans('', '', arabic_punctuation)
        return text.translate(translator)

    def replace_starting_aleph(text):
        words = text.split()
        modified_words = ['ا' + word[1:] if word.startswith('أ') else word for word in words]
        return ' '.join(modified_words)

    # Remove tashkeel and tatweel
    text = araby.strip_tashkeel(text)
    text = araby.strip_tatweel(text)

    # Remove English punctuation
    text = re.sub(r'[^\w\s]', '', text)

    # Remove Arabic punctuation
    text = remove_arabic_punctuation(text)

    # Remove English digits
    text = re.sub(r'\d+', '', text)

    # Remove Arabic digits
    text = re.sub(r'[٠-٩]', '', text)

    # Replace words starting with 'أ' with 'ا'
    text = replace_starting_aleph(text)

    return " ".join([char.strip() for char in text.split(" ") if char.strip()])


def load_clean_data(madar_directory: Path = MADAR_CORPUS_DIR,madar_lexicon:Path = LEXICON_PATH) -> tuple[pd.DataFrame,pd.DataFrame]:
    # READ ALL .tsv files into pandas df
    corpus_dfs = [pd.read_csv(dataset_path, sep='\t', header=0) for dataset_path in list(madar_directory.rglob('*.tsv'))]
    lexicon_df = pd.read_csv(madar_lexicon,sep='\t',header=0)

    corpus_df = pd.concat(corpus_dfs)
    corpus_df.reset_index(drop=True, inplace=True)

    # Ensure 'lang' and 'sent' columns exist
    if 'lang' not in corpus_df.columns or 'sent' not in corpus_df.columns:
        raise ValueError("Expected columns 'lang' and 'sent' not found in the DataFrame")

    corpus_df.set_index("sentID.BTEC", inplace=True)
    corpus_df = corpus_df[~(corpus_df['sent'].isna() | (corpus_df['sent'] == ''))]
    corpus_df.fillna('', inplace=True)
    corpus_df = corpus_df[['lang', 'sent']]

    corpus_df['lang'] = corpus_df['lang'].apply(str.strip)
    corpus_df['sent'] = corpus_df['sent'].apply(preprocess_text)
    corpus_df['sent'] = corpus_df['sent'].apply(str.strip)
    corpus_df = corpus_df[~corpus_df['lang'].isin(['EN', 'FR'])]

    lexicon_df = lexicon_df[['Tokenization','Dialect']]
    lexicon_df = lexicon_df[~lexicon_df['Dialect'].isin(['EN', 'FR'])]
    lexicon_df['Tokenization'] = lexicon_df['Tokenization'].apply(preprocess_text)
    lexicon_df['Tokenization'] = lexicon_df['Tokenization'].apply(str.strip)
    lexicon_df['Dialect'] = lexicon_df['Dialect'].apply(str.strip)
    lexicon_df

    return corpus_df,lexicon_df

madar_corpus_dataset,madar_lexicon_dataset = load_clean_data()