import os
import requests
import tempfile
from urllib.parse import urlparse

def download_github_repo(repo_url: str) -> str:
    """
    Takes a GitHub URL, downloads the repository as a .zip file,
    and returns the path to the temporary .zip file.
    """
    # 1. Clean and parse the URL to get the owner and repo name
    # Example: https://github.com/fastapi/fastapi -> owner: fastapi, repo: fastapi
    parsed_url = urlparse(repo_url)
    path_parts = parsed_url.path.strip("/").split("/")
    
    if len(path_parts) < 2:
        raise ValueError("Invalid GitHub URL. Please provide a link like: https://github.com/owner/repo")
        
    owner, repo = path_parts[0], path_parts[1]
    
    # 2. Construct the official GitHub API URL for downloading zip files
    # This automatically fetches the default branch (main or master)
    api_url = f"https://api.github.com/repos/{owner}/{repo}/zipball"
    
    print(f"Downloading repository from: {api_url}")
    
    # 3. Make the network request to download the file
    response = requests.get(api_url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to download from GitHub. Make sure the repository is public. Status: {response.status_code}")
        
    # 4. Create a safe, temporary file path on your computer to store the .zip
    temp_dir = tempfile.gettempdir()
    zip_file_path = os.path.join(temp_dir, f"{repo}_codebase.zip")
    
    # 5. Save the downloaded data into the .zip file
    with open(zip_file_path, "wb") as file:
        file.write(response.content)
        
    print(f"Successfully saved temporary zip to: {zip_file_path}")
    
    # Return the path so our next extraction function knows where to find it!
    return zip_file_path
# 2nd i write this file 