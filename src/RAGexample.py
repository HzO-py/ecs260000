import openai
import os
import random
from llama_index.core import SimpleDirectoryReader,GPTVectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding

def generate_response(query):
    openai.api_key = "" #replace by your key
    client = openai
    embed_model = OpenAIEmbedding(client=client)

    # documents = ["user_manual_1.txt", "user_manual_2.txt"] # This is your custom data
    dataset_folder = "dataset"
    rag_folder = os.path.join(dataset_folder, "RAG_processed")
    random_value = random.randint(1, 157)

    filename = f"{random_value}.txt"
    file_path = os.path.join(rag_folder, filename)
    reader = SimpleDirectoryReader(input_files=[file_path])
    # reader = SimpleDirectoryReader("./dataset/example")
    index = GPTVectorStoreIndex.from_documents(reader.load_data())

    # Initialize the query engine
    query_engine = index.as_query_engine(similarity_top_k=3)
    retrieved_info = query_engine.query(query)

    prompt = f"Using the following information: {retrieved_info}, please answer the question: {query}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",  
        messages=[  
            {"role": "user", "content": prompt}  
        ],
        max_tokens=150 
    )
    return response.choices[0].message.content

# Example usage
query = "How do I reset my device?"
print(generate_response(query))


