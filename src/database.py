import chromadb
import streamlit as st
from chromadb.utils import embedding_functions

# 2026 Stable Embedding Model
MODEL_NAME = "models/gemini-embedding-001"

def get_collection(api_key):
    gemini_ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
        api_key=api_key,
        model_name=MODEL_NAME
    )
    client = chromadb.PersistentClient(path="./data/chroma_db")
    return client.get_or_create_collection("re_tutor_v3", embedding_function=gemini_ef)

# def process_and_store_json(json_data, api_key):
#     collection = get_collection(api_key)
#     docs, metas, ids = [], [], []
#     for i, item in enumerate(json_data):
#         # Concatenate data into a single searchable string
#         text = f"Prop at {item.get('address')}. {item.get('description')} Zoning: {item.get('zoning')}"
#         docs.append(text)
#         metas.append({str(k): str(v) for k, v in item.items()})
#         ids.append(str(item.get('id', i)))
#     collection.upsert(documents=docs, metadatas=metas, ids=ids)
#     return len(docs)

### ----- NEW PROCESS AND STORE ----- ###

def process_and_store_json(json_data, api_key):
    client = chromadb.PersistentClient(path="./data/chroma_db")

    # DELETE old collection completely
    try:
        client.delete_collection("re_tutor_v3")
    except:
        pass

    gemini_ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
        api_key=api_key,
        model_name=MODEL_NAME
    )

    collection = client.get_or_create_collection(
        "re_tutor_v3",
        embedding_function=gemini_ef
    )

    docs, metas, ids = [], [], []
    for i, item in enumerate(json_data):
        text = f"Prop at {item.get('address')}. {item.get('description')} Zoning: {item.get('zoning')}"
        docs.append(text)
        metas.append({str(k): str(v) for k, v in item.items()})
        ids.append(str(item.get('id', i)))

    collection.upsert(documents=docs, metadatas=metas, ids=ids)

    return len(docs)

def query_listings(query_text, api_key, num_results=3): # Changed from 1 to 3
    try:
        collection = get_collection(api_key)
        results = collection.query(query_texts=[query_text], n_results=num_results)
        # Join multiple listings into one block of text
        if results and results["documents"]:
            return "\n---\n".join(results["documents"][0]) 
    except:
        return None