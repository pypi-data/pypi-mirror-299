# model_downloader.py
import os
import urllib.request

class ModelDownloader:
    def __init__(self, model_url='https://example.com/model.tar.gz', model_dir='model'):
        self.model_url = model_url  # URL to the model
        self.model_dir = model_dir  # Directory where the model will be stored
        self.model_tar = os.path.join(self.model_dir, 'model.tar.gz')  # Model tar file path

    def download_model(self):
        # Create the model directory if it doesn't exist
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)

        # Download the model
        print(f"Downloading model from {self.model_url}...")
        urllib.request.urlretrieve(self.model_url, self.model_tar)
        print("Model downloaded successfully!")

        # Extract the model (assuming it's in tar.gz format)
        self.extract_model()

    def extract_model(self):
        import tarfile
        print(f"Extracting model...")
        with tarfile.open(self.model_tar, 'r:gz') as tar:
            tar.extractall(path=self.model_dir)
        print(f"Model extracted successfully!")

    def is_model_downloaded(self):
        # Check if the model is already downloaded (simple check for the directory)
        return os.path.exists(self.model_dir) and os.path.isdir(self.model_dir)

    def get_model_path(self):
        return self.model_dir  # Return the directory where the model is stored
