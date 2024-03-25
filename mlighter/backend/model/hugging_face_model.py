from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import pandas as pd

class HuggingFaceModel:
    def __init__(self, model_name):
        print("Creating HuggingFaceModel with name:", model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)

        self.num_labels_consider = 20
        print("Model Created")

    def set_num_labels_consider(self, num_labels_consider):
        self.num_labels_consider = num_labels_consider

    def predict(self, text, original_text=None):
        if original_text is not None:
            if isinstance(text, pd.DataFrame):
                text['original_description'] = original_text
            else:
                text = pd.DataFrame({
                    'description': text,
                    'original_description': original_text
                })

        text.reset_index(drop=True, inplace=True)

        predicted_labels = text.apply(lambda row: self._predict_single(row['description']), axis=1)
        text['labels'] = predicted_labels
        if original_text is not None:
            original_predicted_labels = text.apply(lambda row: self._predict_single(row['original_description']), axis=1)
            text['original_labels'] = original_predicted_labels

        try:
            print(text)
            print("=====================")
            text['idx'] = text.index

            text = text.explode('labels')
            norm_labels = pd.json_normalize(text['labels'])
            print(norm_labels)
            text = pd.concat([text.reset_index(drop=True), norm_labels], axis=1)
            text.drop(columns=['labels'], inplace=True)

            if original_text is not None:
                text = text.explode('original_labels')
                norm_original_labels = pd.json_normalize(text['original_labels'])
                text = pd.concat([text.reset_index(drop=True), norm_original_labels], axis=1)
                text.drop(columns=['original_labels'], inplace=True)

            text.index = text['idx']

            print(text)
            print("=====================")

            return text
        except Exception as e:
            print("Error in predict:", e)
            return text


    def _predict_single(self, text):
        inputs = self.tokenizer(text, return_tensors="pt")
        outputs = self.model(**inputs)

        predictions = torch.sigmoid(outputs.logits)
        predicted_labels = [self.model.config.id2label[_id] for _id in (predictions > 0.3).nonzero()[:, 1].tolist()]

        predicted_labels = pd.DataFrame({
            'label': predicted_labels,
            'prediction': predictions[0][predictions[0] > 0.3].tolist()
        })

        top_results = predicted_labels.sort_values(by='prediction', ascending=False).head(self.num_labels_consider)

        # to array of dictionaries
        top_results = top_results.to_dict(orient='records')

        return top_results
