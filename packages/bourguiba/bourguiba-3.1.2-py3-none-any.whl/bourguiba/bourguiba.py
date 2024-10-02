# bourguiba.py
from .instruction import CommandGenerator
from .model_downloader import ModelDownloader

class Bourguiba:
    def __init__(self):
        self.downloader = ModelDownloader()  # Initialize the model downloader
        
        # Check if the model is downloaded, if not, download it
        if not self.downloader.is_model_downloaded():
            self.downloader.download_model()

        self.generator = CommandGenerator(model_path=self.downloader.get_model_path())  # Pass model path

    def generate_command(self, prompt):
        # Call the CommandGenerator to create the shell command
        return self.generator.generate_command(prompt)

def main():
    # Create an instance of the Bourguiba class
    bourguiba = Bourguiba()

    # Ask the user to input a prompt
    print("Type a description for the shell command you need (e.g., 'create a directory', 'list all files'): ")
    prompt = input("> ").strip()

    # Generate the command based on the input
    command = bourguiba.generate_command(prompt)

    # Print the generated shell command for Linux/macOS and Windows
    print("\nGenerated Commands:\n")
    print(f"Linux/macOS Command: {command}")
    print(f"Windows Command: {command}")

if __name__ == "__main__":
    main()
