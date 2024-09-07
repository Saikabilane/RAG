import chromadb
chroma_client = chromadb.PersistentClient(path="./collection")
from pypdf import PdfReader

filePath = "./anatomy_vol_3_book_back.pdf"

reader = PdfReader(filePath)
pages = len(reader.pages)

texts = []
ids = []
count = 1
for page in range(pages):
    text = reader.pages[page].extract_text()
    texts.append(text)
    ids.append("id"+str(count))
    count += 1

collection = chroma_client.create_collection(name="book_back")

collection.add(
    documents = texts,
    ids=ids
)