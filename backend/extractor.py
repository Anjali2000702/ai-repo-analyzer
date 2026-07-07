import os
import zipfile
import tempfile

# List of file extensions we actually want the AI to read
ALLOWED_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", 
    ".md", ".txt", ".json", ".html", ".css", 
    ".java", ".cpp", ".c", ".go", ".rs"
}

def extract_and_filter_zip(zip_file_path: str) -> str:
    """
    Extracts a .zip file into a temporary directory and deletes non-text/code files.
    Returns the path to the clean, extracted folder.
    """
    # 1. Create a safe, temporary folder to hold the extracted files
    extract_dir = tempfile.mkdtemp()
    print(f"Extracting .zip to: {extract_dir}")
    
    # 2. Open and extract the .zip file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
        
    # 3. Walk through the extracted files and delete the junk we don't need
    for root, dirs, files in os.walk(extract_dir):
        # Ignore hidden directories like .git by modifying the dirs list in-place
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            file_path = os.path.join(root, file)
            # Get the file extension (e.g., .py, .png)
            _, ext = os.path.splitext(file)
            
            # If it's a hidden file or not in our allowed list, delete it!
            if file.startswith('.') or ext.lower() not in ALLOWED_EXTENSIONS:
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Could not delete {file}: {e}")
                    
    print("Extraction and filtering complete!")
    
    # Return the path to the folder containing only our clean code files
    return extract_dir
# 3rd i write this file