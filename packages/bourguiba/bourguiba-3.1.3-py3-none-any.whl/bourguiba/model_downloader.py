import os
from transformers import AutoModel, AutoTokenizer

class ModelDownloader:
    def __init__(self):
        self.model_name = "meta-llama/Llama-3.1-8B-Instruct"  # LLaMA model from Hugging Face

    def download_model(self):
        model_dir = os.path.join(os.getcwd(), 'bourguiba', 'model')
        os.makedirs(model_dir, exist_ok=True)

        # Download the model and tokenizer
        print(f"Downloading model '{self.model_name}' from Hugging Face...")
        model = AutoModel.from_pretrained(self.model_name)
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)

        # Save the model and tokenizer locally
        model.save_pretrained(model_dir)
        tokenizer.save_pretrained(model_dir)
        print("Model downloaded and saved successfully.")
