# # import os
# # from dotenv import load_dotenv
# # from langchain_groq import ChatGroq
# # from langchain_chroma import Chroma
# # from langchain_huggingface import HuggingFaceEmbeddings
# # from langchain_classic.chains import create_retrieval_chain
# # from langchain_classic.chains.combine_documents import create_stuff_documents_chain
# # from langchain_core.prompts import ChatPromptTemplate

# # # Load the secret API key from the .env file securely
# # load_dotenv()

# # # The folder where our vector database lives
# # CHROMA_PATH = "chroma_db"

# # def answer_question(question: str) -> str:
# #     """
# #     Takes a user's question, searches the indexed codebase, 
# #     and generates an accurate answer using Groq (Llama 3).
# #     """
# #     # 1. Check if the database exists (so the server doesn't crash if they ask before uploading)
# #     if not os.path.exists(CHROMA_PATH):
# #         return "Error: No repository has been processed yet. Please upload or link a repository first."

# #     # 2. Re-initialize the exact same embedding model we used to save the data
# #     embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# #     db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    
# #     # 3. Set up the Retriever
# #     # k=4 means Semantic Search will only grab the 4 most relevant chunks of code
# #     retriever = db.as_retriever(search_kwargs={"k": 4})

# #     # 4. Initialize the Groq AI Model
# #     # Llama 3 8B is blazing fast. A low temperature (0.3) keeps the AI strictly logical and prevents creative hallucinations.
# #     llm = ChatGroq(
# #         model="llama-3.1-8b-instant",
# #         temperature=0.3, 
# #     )

# #     # 5. Define the strict instructions for the AI
# #     system_prompt = (
# #         "You are an expert Software Engineer and Codebase Assistant. "
# #         "Use the following pieces of retrieved context to answer the user's question. "
# #         "If the answer is not in the context, say 'I cannot find the answer in the provided codebase.' "
# #         "Do not make up code. Always provide clear explanations and code snippets if applicable.\n\n"
# #         "Context:\n{context}"
# #     )
    
# #     prompt = ChatPromptTemplate.from_messages([
# #         ("system", system_prompt),
# #         ("human", "{input}"),
# #     ])

# #     # 6. Build the RAG Pipeline (Chain)
# #     question_answer_chain = create_stuff_documents_chain(llm, prompt)
# #     rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# #     # 7. Execute the chain and return the final answer
# #     print(f"Asking Groq: {question}")
# #     response = rag_chain.invoke({"input": question})
    
# #     return response["answer"]


# import os
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq
# from langchain_chroma import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_classic.chains import create_retrieval_chain
# from langchain_classic.chains.combine_documents import create_stuff_documents_chain
# from langchain_core.prompts import ChatPromptTemplate

# # Load the secret API key from the .env file securely
# load_dotenv()

# # The folder where our vector database lives
# CHROMA_PATH = "chroma_db"

# def answer_question(question: str) -> str:
#     """
#     Takes a user's question, searches the indexed codebase, 
#     and generates an accurate answer using Groq (Llama 3).
#     """
#     # 1. Check if the database exists (so the server doesn't crash if they ask before uploading)
#     if not os.path.exists(CHROMA_PATH):
#         return "Error: No repository has been processed yet. Please upload or link a repository first."

#     # 2. Re-initialize the exact same embedding model we used to save the data
#     embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#     db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    
#     # 3. Set up the Retriever
#     # k=4 means Semantic Search will only grab the 4 most relevant chunks of code
#     retriever = db.as_retriever(search_kwargs={"k": 4})

#     # 4. Initialize the Groq AI Model
#     # Llama 3 8B is blazing fast. A low temperature (0.3) keeps the AI strictly logical and prevents creative hallucinations.
#     llm = ChatGroq(
#         model="llama-3.1-8b-instant",
#         temperature=0.3, 
#     )

#     # 5. Define the strict instructions for the AI
#     system_prompt = (
#         "You are an expert Software Engineer and Codebase Assistant. "
#         "Use the following pieces of retrieved context to answer the user's question. "
#         "If the answer is not in the context, say 'I cannot find the answer in the provided codebase.' "
#         "Do not make up code. Always provide clear explanations and code snippets if applicable.\n\n"
#         "Context:\n{context}"
#     )
    
#     prompt = ChatPromptTemplate.from_messages([
#         ("system", system_prompt),
#         ("human", "{input}"),
#     ])

#     # 6. Build the RAG Pipeline (Chain)
#     question_answer_chain = create_stuff_documents_chain(llm, prompt)
#     rag_chain = create_retrieval_chain(retriever, question_answer_chain)

#     # 7. Execute the chain and return the final answer
#     print(f"Asking Groq: {question}")
#     response = rag_chain.invoke({"input": question})
    
#     return response["answer"]

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# Load the secret API key from the .env file securely
load_dotenv()

# The folder where our vector database lives
CHROMA_PATH = "chroma_db"

def answer_question(question: str) -> str:
    """
    Takes a user's question, searches the indexed codebase, 
    and generates an accurate answer using Groq (Llama 3).
    """
    # 1. Check if the database exists (so the server doesn't crash if they ask before uploading)
    if not os.path.exists(CHROMA_PATH):
        return "Error: No repository has been processed yet. Please upload or link a repository first."

    # 2. Re-initialize the exact same embedding method we used to save the data
    # Using the HF Inference API instead of loading the model locally — saves RAM
    embeddings = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
    huggingfacehub_api_token=os.environ.get("HF_TOKEN", "").strip(),
    )
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    
    # 3. Set up the Retriever
    retriever = db.as_retriever(search_kwargs={"k": 4})

    # 4. Initialize the Groq AI Model
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.3, 
    )

    # 5. Define the strict instructions for the AI
    system_prompt = (
        "You are an expert Software Engineer and Codebase Assistant. "
        "Use the following pieces of retrieved context to answer the user's question. "
        "If the answer is not in the context, say 'I cannot find the answer in the provided codebase.' "
        "Do not make up code. Always provide clear explanations and code snippets if applicable.\n\n"
        "Context:\n{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    # 6. Build the RAG Pipeline (Chain)
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    # 7. Execute the chain and return the final answer
    print(f"Asking Groq: {question}")
    response = rag_chain.invoke({"input": question})
    
    return response["answer"]