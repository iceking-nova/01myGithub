from langchain_community.embeddings import DashScopeEmbeddings

# 1. 创建嵌入模型对象
embedding = DashScopeEmbeddings()

# 2. 文本向量化
text = "内容"
queryVector = embedding.embed_query(text)

# 3. 处理输出
print(queryVector)