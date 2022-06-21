from Preprocessing.textPreprocessing import preprocess_text_data
from matchingUtilities import MatchingUtilities
from createTextEmbedding import TransformersEmbeddingGenerator
from sklearn.metrics.pairwise import cosine_similarity
from math import *

def square_rooted(x):
    return round(sqrt(sum([a * a for a in x])), 5)


def cosine_similarity(x, y):
    numerator = sum(a * b for a, b in zip(x, y))
    denominator = square_rooted(x) * square_rooted(y)
    return round(numerator / float(denominator), 3)


def jaccard_similarity(x,y):
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality/float(union_cardinality)




def main():
    datasets = preprocess_text_data()

    mUtilities = MatchingUtilities([datasets[-1]], datasets[:-1])

    '''text_embedding_generator = TransformersEmbeddingGenerator(model='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    embeddings = text_embedding_generator.createTextEmbedding(sentences=['10000000', '34'])
    print(cosine_similarity(embeddings[0], embeddings[1]))
    embeddings = text_embedding_generator.createTextEmbedding(sentences=['99', '39'])
    print(cosine_similarity(embeddings[0], embeddings[1]))
    embeddings = text_embedding_generator.createTextEmbedding(sentences=['99', '1000'])
    print(cosine_similarity(embeddings[0], embeddings[1]))
    embeddings = text_embedding_generator.createTextEmbedding(sentences=['1000', '99'])
    print(cosine_similarity(embeddings[0], embeddings[1]))
    embeddings = text_embedding_generator.createTextEmbedding(sentences=['99', '100'])
    print(cosine_similarity(embeddings[0], embeddings[1]))'''

    print('')



if __name__ == "__main__":
    main()