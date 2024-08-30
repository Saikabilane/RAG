import chromadb
import pandas as pd

pictures = pd.read_csv("./image_filenames.csv")
pics_loc = pictures['Image Name']
pics_loc = list(pics_loc)
texts = pictures['Description']
texts = list(texts)

ids = []
count = 1
for page in range(len(texts)):
    ids.append("id"+str(count))
    count += 1

chroma_client = chromadb.PersistentClient(path="./collection")

img_collection = chroma_client.create_collection(name="images")

img_collection.add(
    documents = texts,
    ids=ids
)

def ask_query(prompt):
    results = img_collection.query(
        query_texts=[prompt], 
        n_results=2
    )
    return results['documents']
