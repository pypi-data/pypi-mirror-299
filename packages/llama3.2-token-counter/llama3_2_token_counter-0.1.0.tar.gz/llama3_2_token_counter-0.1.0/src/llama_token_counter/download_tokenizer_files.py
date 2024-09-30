import os
from huggingface_hub import hf_hub_download, list_repo_files

def download_tokenizer_files(repo_id, local_dir):
    """
    Download tokenizer files for a specific model from Hugging Face.

    @param repo_id: The repository ID of the model (e.g., 'openai/whisper-large-v3')
    @param local_dir: The local directory to save the downloaded files
    @return: A list of paths to the downloaded files
    """
    # Get the Hugging Face token from environment variable
    hf_token = os.environ.get("HF_TOKEN")
    if not hf_token:
        raise ValueError("HF_TOKEN environment variable not set")

    try:
        # List all files in the repository
        all_files = list_repo_files(repo_id, token=hf_token)
        
        # Filter for tokenizer files
        tokenizer_files = [f for f in all_files if 'tokenizer' in f.lower() or f.endswith('.model')]
        
        downloaded_files = []
        for file in tokenizer_files:
            file_path = hf_hub_download(
                repo_id=repo_id,
                filename=file,
                token=hf_token,
                local_dir=local_dir
            )
            downloaded_files.append(file_path)
            print(f"Successfully downloaded {file} to {file_path}")
        
        return downloaded_files
    except Exception as e:
        print(f"Error downloading tokenizer files: {e}")
        return []

# Example usage
if __name__ == "__main__":
    repo_id = "meta-llama/Llama-3.2-90B-Vision"
    local_dir = "./tokenizer"
    
    downloaded_files = download_tokenizer_files(repo_id, local_dir)
    if downloaded_files:
        print(f"Tokenizer files downloaded to: {local_dir}")
        for file in downloaded_files:
            print(f"- {file}")
    else:
        print("No tokenizer files were downloaded.")