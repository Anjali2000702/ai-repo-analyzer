# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# #initialize the backend application
# app = FastAPI(title="AI Repo Analyzer API")

# #configure CORS middleware

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],# allow any forntend to connect (we will restrict this later)
#     allow_credentials=True,
#     allow_methods=["*"], # allow all request types(GET, POST, etc.)
#     allow_headers=["*"],

# )

# #create our first endpoint
# @app.get("/")
# async def root():
#     return {"message": "Backend engine is running successfully!"}
# # 1st i write this 


# 2nd time update
# connect all the backend files together
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel

# # Import our custom worker scripts
# import github_handler
# import extractor
# import indexer

# # Initialize the backend application
# app = FastAPI(title="AI Repo Analyzer API")

# # Configure CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  
#     allow_credentials=True,
#     allow_methods=["*"],  
#     allow_headers=["*"],
# )

# # Define the expected JSON format for the incoming request
# class RepoRequest(BaseModel):
#     github_url: str

# # Our original health-check endpoint
# @app.get("/")
# async def root():
#     return {"message": "Backend engine is running successfully!"}

# # Our new Orchestration Endpoint
# @app.post("/process-github-repo")
# async def process_github_repo(request: RepoRequest):
#     try:
#         print(f"\n--- Starting Processing for {request.github_url} ---")
        
#         # Step 1: Download
#         print("Step 1: Downloading repository...")
#         zip_path = github_handler.download_github_repo(request.github_url)
        
#         # Step 2: Extract & Filter
#         print("Step 2: Extracting and filtering files...")
#         extracted_folder = extractor.extract_and_filter_zip(zip_path)
        
#         # Step 3: Index into Vector DB
    #     print("Step 3: Indexing files into Vector Database...")
    #     indexer.create_vector_db(extracted_folder)
        
    #     return {"message": "Repository successfully processed and indexed into ChromaDB!"}
        
    # except Exception as e:
    #     # SDE Best Practice: Catch errors and return a 500 Internal Server Error safely
    #     print(f"Error occurred: {e}")
    #     raise HTTPException(status_code=500, detail=str(e))


# update 
# update your fast api server to include a new endpoint (ask) this endpoint will receive a quesiton formt he user send it to rag_core.py and 
# return the AI's answer

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import our custom worker scripts
import github_handler
import extractor
import indexer
import rag_core  # <-- NEW: Importing our AI brain!

# Initialize the backend application
app = FastAPI(title="AI Repo Analyzer API")

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)


# Expected JSON format for processing a repo
class RepoRequest(BaseModel):
    github_url: str

# Expected JSON format for asking a question
class ChatRequest(BaseModel):
    question: str

@app.get("/")
async def root():
    return {"message": "Backend engine is running successfully!"}

@app.post("/process-github-repo")
async def process_github_repo(request: RepoRequest):
    try:
        print(f"\n--- Starting Processing for {request.github_url} ---")
        zip_path = github_handler.download_github_repo(request.github_url)
        extracted_folder = extractor.extract_and_filter_zip(zip_path)
        indexer.create_vector_db(extracted_folder)
        return {"message": "Repository successfully processed and indexed into ChromaDB!"}
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# NEW: The Orchestration Endpoint for the Chatbot
@app.post("/ask")
async def ask_question(request: ChatRequest):
    try:
        print(f"\n--- New Question Received: {request.question} ---")
        # Send the question to our RAG core and wait for the AI's answer
        answer = rag_core.answer_question(request.question)
        return {"answer": answer}
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
