from .ngram_model import NgramModel
class SentenceCompleter:
    def __init__(self, ngram_model:NgramModel):
        self.ngram_model = ngram_model

    def complete_sentence(self, initial_sentence, num_words):
        words = initial_sentence.split()
        for _ in range(num_words):
            n = min(len(words), len(self.ngram_model.ngram_counts_list)) + 1
            previous_ngram = tuple(words[-(n-1):])
            next_word = self.ngram_model.predict_next_word(previous_ngram, self.ngram_model.ngram_counts_list[n-2])
            if next_word is None:
                break
            words.append(next_word)
        return ' '.join(words)