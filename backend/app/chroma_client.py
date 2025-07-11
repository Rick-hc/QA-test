import chromadb

# β版: サーバー不要なローカル in-memory モードで起動
client = chromadb.Client()
# コレクション名は任意。なければ作成されます
collection = client.get_or_create_collection("default_collection")
