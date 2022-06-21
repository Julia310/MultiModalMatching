from transformers import AutoTokenizer
from transformers import pipeline
from numpy import array

class TextEmbeddingGenerator:

    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.feature_extractor = pipeline('feature-extraction',model=model_name, tokenizer=self.tokenizer)

    def createEmbeddingList(self, text_list):
        embedding_list = []
        for text in text_list:
            features = self.createTextEmbedding(text)
            a = array(features)
            print(a.shape)
            embedding_list.append(features)
        return embedding_list

    def createTextEmbedding(self, text):
        tokens = self.tokenizer(text)
        if (len(tokens['input_ids'])) > 512:
            tokens = [t for t in tokens if len(t) > 0 ]
            text = ''.join(tokens[:512])
        return self.feature_extractor(text)[0][0]

