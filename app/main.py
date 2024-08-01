from app.vectorDB.weaviateVdb import insert_data

context_name = "A delicious Riesling"   
chunk_name = "This wine is a delicious Riesling which pairs well with seafood."
text = "Germany"

uuid = insert_data(context_name, chunk_name, text)