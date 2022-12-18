from .clue_generator_base import ClueGeneratorBase

from tqdm import tqdm
import gensim.downloader

class VectorClueGenerator(ClueGeneratorBase):
    def __init__(self, model_name):
        self._keyed_vectors = gensim.downloader.load(model_name)

    def generate_clue(self, pos_words, neg_words):
        clue_pos_words = dict()
        clue_pos_word_similarities = dict()
        clue_sort_keys = dict()

        for clue in list(self._keyed_vectors.index_to_key):
            if clue.upper() in pos_words:
                continue

            max_neg_similarity = 0

            for neg_word in neg_words:
                max_neg_similarity = max(max_neg_similarity, self._similarity(clue, neg_word))
            
            clueable_pos_words = []
            pos_word_similarities = []
            total_similarity = 0
            for pos_word in pos_words:
                similarity = self._similarity(clue, pos_word)

                if clue == "pet":
                    print(pos_word, similarity, max_neg_similarity)

                if similarity > max_neg_similarity:
                    clueable_pos_words.append(pos_word)
                    pos_word_similarities.append(similarity)
                    total_similarity += similarity
            
            clue_pos_words[clue] = clueable_pos_words
            clue_pos_word_similarities[clue] = pos_word_similarities
            clue_sort_keys[clue] = (len(clueable_pos_words), total_similarity)
        
        sorted_clues = sorted(list(clue_sort_keys.keys()), key=clue_sort_keys.get, reverse=True)
        top_clue = sorted_clues[0]
        clue_words = clue_pos_words[top_clue]
        similarities = clue_pos_word_similarities[top_clue]
        explanations = [ f"{word} similarity: {round(similarity, 2)}" for word, similarity in zip(clue_words, similarities) ]
        return top_clue.upper(), clue_words, explanations


    def _similarity(self, word1, word2):
        word1 = word1.lower()
        word2 = word2.lower()

        if word1 not in self._keyed_vectors.key_to_index or word2 not in self._keyed_vectors.key_to_index:
            return 0
        return self._keyed_vectors.similarity(word1, word2)


class Word2VecGlueGenerator(VectorClueGenerator):
    def __init__(self):
        super().__init__("word2vec-google-news-300")


class GloveNetClueGenerator(VectorClueGenerator):
    def __init__(self):
        super().__init__("glove-wiki-gigaword-300")