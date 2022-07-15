from transformers import AutoTokenizer, AutoModel
import torch
from DatabaseManager.databaseConnection import MySQLManager
import pickle
from tqdm import tqdm


def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


class TransformersEmbeddingGenerator:
    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model_name = AutoModel.from_pretrained(model_name)

    def create_text_embeddings(self, text):
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

    def generate_embeddings(self):
        attributes = list(self.text_df1.columns)
        text_df_list = [(self.text_df1, self.data_source1), (self.text_df2, self.data_source2)]
        for j in range(len(text_df_list)):
            (text_df, data_source) = text_df_list[j]
            emb_list = []
            indices = list(text_df.index)
            with tqdm(total=len(indices), desc='generate embeddings for dataset ' + str(j + 1), position=0, leave=True) as pbar:
                for i in range(len(indices)):
                    pbar.update()
                    embeddings = self.create_embeddings_for_row(indices[i], attributes, text_df.loc[[indices[i]]])
                    emb_list.append(embeddings)
            self.db_manager.save_many(emb_list, data_source)

    def create_embeddings_for_row(self, index, columns, row):
        values = {'articleId': index}
        for col in columns:
            if not col == 'price':
                vector = self.embedding_generator.create_text_embeddings(row[col][0])[0]
                embed_bytes = pickle.dumps(vector)
                values[col] = embed_bytes
            else:
                values[col] = row[col][0]
        return values




