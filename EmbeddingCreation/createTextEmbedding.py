from transformers import AutoTokenizer, AutoModel
import torch
from DatabaseManager.databaseConnection import MySQLManager
import numpy as np


def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


class TransformersEmbeddingGenerator:
    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model_name = AutoModel.from_pretrained(model_name)

    def createTextEmbedding(self, text):
        encoded_input = self.tokenizer(text, padding=True, truncation=True, return_tensors='pt')

        with torch.no_grad():
            model_output = self.model_name(**encoded_input)

        sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
        return sentence_embeddings.cpu().detach().numpy()


class ManageTextEmbeddings:

    def __init__(self, model_name, text_df1, text_df2, data_source1, data_source2):
        self.model_name = model_name
        self.text_df1 = text_df1
        self.text_df2 = text_df2
        self.embedding_generator = TransformersEmbeddingGenerator(model_name=model_name)
        self.data_source1 = data_source1
        self.data_source2 = data_source2
        self.db_manager = MySQLManager()

    def generate_and_save_embeddings(self):

        columns = list(self.text_df1.columns)

        for (text_df, data_source) in [(self.text_df1, self.data_source1), (self.text_df2, self.data_source2)]:
            emb_list = []
            for i in range(len(columns)):
                emb_list.append(self.embedding_generator.createTextEmbedding(text=self.text_df1[columns[i]].tolist()))
            new_columns = ['articleId'] + columns
            self.create_embedding_dicts_from_lists(np.array(text_df.index), new_columns, np.array(emb_list),
                                                   data_source)

    def create_embedding_dicts_from_lists(self, indexes, columns, emb_list, data_source):
        embeddings = []
        for i in range(len(indexes)):
            row = emb_list[:, i]
            values = {columns[0]: indexes[i]}
            for j in range(len(row)):
                values[columns[j + 1]] = row[j].dumps()
            embeddings.append(values)
        self.db_manager.save_many(embeddings, data_source)

    def save_article_ids(self, text_df, data_source):
        id_list = [
            {'articleId': element}
            for element in text_df.index
        ]
        self.db_manager.save_many(id_list, data_source)

    def save_embeddings(self, embedding_list, attribute, data_source):
        embed_list = [
            {attribute: str(list(embedding))[1:][:-1]}
            for embedding in embedding_list
        ]
        self.db_manager.save_many(embed_list, data_source)