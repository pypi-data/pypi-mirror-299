import os
import pandas as pd
from transformers import BertForSequenceClassification, Trainer, TrainingArguments, BertTokenizer
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import torch
from torch.utils.data import Dataset
import numpy as np




class TextClassificationModel:
    """
    A text classification model using a pre-trained BERT model. This class provides
    methods for loading data, training, evaluating, and saving the model.
    """
    def __init__(self, model_name='bert-base-uncased', cache_dir=None):
        """
        Initializes the model, tokenizer, and device.
        :param model_name: Name of the pre-trained BERT model (default: bert-base-uncased)
        :param cache_dir: Directory where the model cache is stored (default: None)
        """
        self.model_name = model_name
        self.cache_dir = cache_dir if cache_dir else os.getcwd()  # Use current directory if no cache dir is provided
        self.tokenizer = BertTokenizer.from_pretrained(model_name, cache_dir=self.cache_dir)
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.df = None  # DataFrame to store the data
        self.class_mapping = {}  # Dictionary to map class labels to indices
        self.encoder = OneHotEncoder(sparse_output=False)  # For encoding categorical data


    def load_data(self, file_path):
        """
        Loads the data from a CSV or Excel file.
        :param file_path: Path to the file (CSV or Excel)
        :return: List of column names in the dataset
        """
        # Determine if file is CSV or Excel
        if file_path.endswith('.csv'):
            self.df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            self.df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")

        # Return the column names in the dataset
        print("Columns found in the dataset:")
        print(self.df.columns.tolist())
        return self.df.columns.tolist()

    def set_columns(self, label_column, text_columns, update_class_mapping=False):
        """
        Sets the label and text columns for training, validation, or testing.
        :param label_column: The column containing the target labels
        :param text_columns: The columns containing text data
        :param update_class_mapping: Boolean to indicate if the class mapping should be updated (only for training data)
        :return: Processed text and label data (or just text data if labels are unavailable)
        """
        # Check if the selected columns exist in the dataset
        if label_column not in self.df.columns or any(col not in self.df.columns for col in text_columns):
            raise ValueError("Invalid column selection. Ensure the columns exist in the dataset.")

        # Process the text data: Concatenate multiple text columns into one if necessary
        if len(text_columns) > 1:
            text_data = self.df[text_columns].apply(lambda row: ' '.join(row.values.astype(str)), axis=1).tolist()
        else:
            text_data = self.df[text_columns[0]].astype(str).tolist()

        # Handle the label column (only if label_column is provided)
        if label_column in self.df.columns and update_class_mapping:
            # For training, update the class mapping
            if not np.issubdtype(self.df[label_column].dtype, np.number):
                unique_labels = sorted(self.df[label_column].unique())
                print(f"Text labels found, converting them to numeric: {unique_labels}")
                self.class_mapping = {label: idx for idx, label in enumerate(unique_labels)}
                y_data = self.df[label_column].map(self.class_mapping).tolist()
            else:
                y_data = self.df[label_column].tolist()
                unique_labels = sorted(set(y_data))
                self.class_mapping = {label: idx for idx, label in enumerate(unique_labels)}
            return text_data, y_data

        elif label_column in self.df.columns:
            # For validation and test sets (already have class mapping), use the existing class mapping
            y_data = self.df[label_column].map(self.class_mapping).tolist()
            return text_data, y_data
        else:
            # If no label column is provided (for unlabeled test data)
            return text_data, None  # No labels


    def tokenize_data(self, texts):
        """
        Tokenizes the text data using the BERT tokenizer.
        :param texts: List of texts to be tokenized
        :return: Tokenized data
        """
        return self.tokenizer(texts, truncation=True, padding=True, max_length=512)

    def compute_metrics(self, p):
        """
        Computes metrics (accuracy, precision, recall, f1-score) during evaluation.
        :param p: EvalPrediction object containing predictions and labels
        :return: Dictionary of computed metrics
        """
        labels = p.label_ids
        preds = p.predictions.argmax(-1)
        precision, recall, f1, support = precision_recall_fscore_support(labels, preds, average=None)
        acc = accuracy_score(labels, preds)
        return {
            'accuracy': float(acc),
            'precision_per_class': precision.tolist(),
            'recall_per_class': recall.tolist(),
            'f1_per_class': f1.tolist(),
            'support_per_class': support.tolist()
        }

    def print_class_wise_metrics(self, eval_results):
        """
        Prints class-wise precision, recall, F1-score, and support.
        :param eval_results: The evaluation results containing metrics per class
        """
        precision, recall, f1, support = eval_results['eval_precision_per_class'], eval_results['eval_recall_per_class'], eval_results['eval_f1_per_class'], eval_results['eval_support_per_class']
        print("\nClass-wise Precision, Recall, F1-score, and Support:")
        print(f"{'Class':<15} {'Precision':<10} {'Recall':<10} {'F1-score':<10} {'Support':<10}")
        for idx, _ in enumerate(precision):
            class_name = list(self.class_mapping.keys())[list(self.class_mapping.values()).index(idx)]
            print(f"{class_name:<15} {precision[idx]:<10.4f} {recall[idx]:<10.4f} {f1[idx]:<10.4f} {support[idx]:<10}")

    def create_dataset(self, encodings, labels):
        """
        Creates a PyTorch dataset from encodings and labels.
        :param encodings: Encoded text data
        :param labels: Target labels
        :return: A PyTorch Dataset object
        """
        class CustomDataset(Dataset):
            def __init__(self, encodings, labels):
                self.encodings = encodings
                self.labels = labels

            def __len__(self):
                return len(self.labels)

            def __getitem__(self, idx):
                item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
                item['labels'] = torch.tensor(self.labels[idx], dtype=torch.long)
                return item

        return CustomDataset(encodings, labels)

    def train(self, text_train, y_train, text_test, y_test, save_model_path='./saved_model'):
        """
        Trains the model using the given training and testing data.
        :param text_train: Training text data
        :param y_train: Training labels
        :param text_test: Testing text data
        :param y_test: Testing labels
        :param save_model_path: Path where the model will be saved
        :return: Evaluation results after training
        """
        # Tokenize the text data
        train_encodings = self.tokenize_data(text_train)
        test_encodings = self.tokenize_data(text_test)

        # Create datasets for training and testing
        train_dataset = self.create_dataset(train_encodings, y_train)
        test_dataset = self.create_dataset(test_encodings, y_test)

        # Load pre-trained BERT model
        model = BertForSequenceClassification.from_pretrained(self.model_name, num_labels=len(set(y_train)), cache_dir=self.cache_dir).to(self.device)

        # Set training arguments
        training_args = TrainingArguments(
            output_dir='./results',
            num_train_epochs=3,
            per_device_train_batch_size=4,
            per_device_eval_batch_size=4,
            evaluation_strategy="epoch",
            logging_dir='./logs',
            logging_steps=10,
            save_strategy="epoch",
            load_best_model_at_end=True
        )

        # Initialize Trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=test_dataset,
            compute_metrics=self.compute_metrics
        )

        # Train the model
        trainer.train()

        # Save the model
        model.save_pretrained(save_model_path)
        print(f"Model saved to {save_model_path}")

        # Evaluate the model on the test dataset
        eval_results = trainer.evaluate()

        # Print the class-wise metrics
        self.print_class_wise_metrics(eval_results)

        return eval_results

    def load_and_evaluate(self, save_model_path, text_test, y_test):
        """
        Loads a pre-trained model and evaluates it on the given test data.
        :param save_model_path: Path where the pre-trained model is saved
        :param text_test: Test text data
        :param y_test: Test labels
        :return: Evaluation results
        """
        # Load the saved model
        model = BertForSequenceClassification.from_pretrained(save_model_path, num_labels=len(set(y_test))).to(self.device)

        # Tokenize the test data
        test_encodings = self.tokenize_data(text_test)

        # Create the test dataset
        test_dataset = self.create_dataset(test_encodings, y_test)

        # Create a DataLoader for the test dataset
        test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=4, shuffle=False)

        # Set model to evaluation mode
        model.eval()

        # Collect predictions and true labels
        predictions = []
        true_labels = []
        
        for batch in test_loader:
            with torch.no_grad():
                inputs = {k: v.to(self.device) for k, v in batch.items() if k != 'labels'}
                outputs = model(**inputs)
                logits = outputs.logits
                predictions.append(logits.argmax(-1).cpu().numpy())
                true_labels.append(batch['labels'].cpu().numpy())
        
        predictions = np.concatenate(predictions)
        true_labels = np.concatenate(true_labels)

        # Compute accuracy, precision, recall, f1-score, etc.
        precision, recall, f1, support = precision_recall_fscore_support(true_labels, predictions, average=None)
        acc = accuracy_score(true_labels, predictions)

        # Print class-wise metrics
        eval_results = {
            'accuracy': float(acc),
            'precision_per_class': precision.tolist(),
            'recall_per_class': recall.tolist(),
            'f1_per_class': f1.tolist(),
            'support_per_class': support.tolist()
        }

        self.print_class_wise_metrics(eval_results)

        return eval_results

        
    def predict(self, text_test, save_predictions_path, save_model_path):
        """
        Generates predictions for the test dataset and saves them as a DataFrame.
        :param text_test: Test text data
        :param save_predictions_path: Path where the predictions will be saved
        :param save_model_path: Path where the fine-tuned model is saved
        :return: DataFrame with predictions
        """
        # Load fine-tuned BERT model
        model = BertForSequenceClassification.from_pretrained(save_model_path, num_labels=len(self.class_mapping)).to(self.device)
        
        # Tokenize the test data
        test_encodings = self.tokenize_data(text_test)
        
        # Create the test dataset (no labels needed for prediction)
        test_dataset = self.create_dataset(test_encodings, [0]*len(text_test))  # Placeholder labels

        # Create a DataLoader for the test dataset
        test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=4, shuffle=False)

        # Set model to evaluation mode (disable dropout, batchnorm)
        model.eval()

        # Collect predictions
        predictions = []
        for batch in test_loader:
            with torch.no_grad():  # Ensure no gradient updates
                inputs = {k: v.to(self.device) for k, v in batch.items() if k != 'labels'}
                outputs = model(**inputs)
                logits = outputs.logits
                predictions.append(logits.argmax(-1).cpu().numpy())

        predictions = np.concatenate(predictions)

        # Convert predictions back to class labels
        predicted_labels = [list(self.class_mapping.keys())[list(self.class_mapping.values()).index(pred)] for pred in predictions]

        # Save predictions as a DataFrame
        df_predictions = pd.DataFrame({
            'Text': [' '.join(text) if isinstance(text, list) else text for text in text_test],  # Handle both single and multiple text columns
            'Predicted Label': predicted_labels
        })
        try:
            df_predictions.to_excel(save_predictions_path, index=False)
            print(f"Predictions saved to (Excel){save_predictions_path}")

        except:
            df_predictions.to_excel(save_predictions_path, index=False)

        print(f"Predictions saved to (CSV){save_predictions_path}")

        return df_predictions

    def evaluate_predictions(predictions, true_labels):
        """
        Evaluates predictions using true labels and calculates metrics like precision, recall, and F1-score.
        :param predictions: List of predicted labels
        :param true_labels: List of true labels
        :return: Dictionary of evaluation metrics
        """
        precision, recall, f1, support = precision_recall_fscore_support(true_labels, predictions, average=None)
        acc = accuracy_score(true_labels, predictions)

        eval_results = {
            'accuracy': float(acc),
            'precision_per_class': precision.tolist(),
            'recall_per_class': recall.tolist(),
            'f1_per_class': f1.tolist(),
            'support_per_class': support.tolist()
        }

        return eval_results




