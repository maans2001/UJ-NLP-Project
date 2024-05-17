from collections import Counter
import re


class NgramModel:
    def __init__(self, tokens_list, max_n):
        self.ngram_counts_list = self.generate_ngram_counts_list(tokens_list, max_n)

    @staticmethod
    def generate_ngram_counts(tokens_list, n):
        ngrams = [ngram for tokens in tokens_list for ngram in zip(*[tokens[i:] for i in range(n)])]
        ngram_counts = Counter(ngrams)
        return ngram_counts

    def generate_ngram_counts_list(self, tokens_list, max_n):
        return [self.generate_ngram_counts(tokens_list, n) for n in range(2, max_n + 1)]

    @staticmethod
    def predict_next_word(previous_ngram, ngram_counts):
        candidates = {ngram[-1]: count for ngram, count in ngram_counts.items() if ngram[:-1] == previous_ngram and re.match(r'^[^\u0600-\u06FF]*$', ngram[-1]) is None}
        if not candidates:
            return None
        predicted_word = max(candidates, key=candidates.get)
        return predicted_word