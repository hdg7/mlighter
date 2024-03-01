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

    def predict(self, text):
        if isinstance(text, pd.DataFrame):
            print(text)
            predicted_labels = text.apply(lambda x: self._predict_single(x['description']), axis=1)
        elif isinstance(text, list):
            predicted_labels = [self._predict_single(t) for t in text]
        else:
            predicted_labels = self._predict_single(text)

        return predicted_labels

    def _predict_single(self, text):
        inputs = self.tokenizer(text, return_tensors="pt")
        outputs = self.model(**inputs)

        predictions = torch.sigmoid(outputs.logits)
        predicted_labels = [self.model.config.id2label[_id] for _id in (predictions > 0.3).nonzero()[:, 1].tolist()]

        predicted_labels = pd.DataFrame({
            'label': predicted_labels,
            'prediction': predictions[0][predictions[0] > 0.3].tolist()
        })

        print(predicted_labels)

        top_results = predicted_labels.sort_values(by='prediction', ascending=False).head(self.num_labels_consider)

        print(top_results['label'].tolist())

        return top_results
