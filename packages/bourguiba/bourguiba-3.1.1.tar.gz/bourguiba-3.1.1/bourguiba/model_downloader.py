import os
import urllib.request

class ModelDownloader:
    def __init__(self):
        self.model_url = "https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct/resolve/main/model.tar.gz"
        self.model_dir = os.path.join(os.getcwd(), 'bourguiba', 'model')
        self.model_tar = os.path.join(self.model_dir, 'model.tar.gz')

    def download_model(self):
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)

        if not os.path.exists(self.model_tar):
            print(f"Downloading model from {self.model_url}...")
            urllib.request.urlretrieve(self.model_url, self.model_tar)
            print("Model downloaded successfully.")
        else:
            print("Model already downloaded.")

if __name__ == "__main__":
    downloader = ModelDownloader()
    downloader.download_model()
