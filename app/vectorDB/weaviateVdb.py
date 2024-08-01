import weaviate

client= weaviate.connect_to_local()
client.is_ready()