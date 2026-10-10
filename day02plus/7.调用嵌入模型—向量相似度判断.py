import numpy as np
from langchain_community.embeddings import DashScopeEmbeddings

def euclidean_distance(a, b):
    """计算欧氏距离"""
    return np.linalg.norm(np.array(a) - np.array(b))


if __name__ == '__main__':
    text= ["今天天气不错","猫很爱干净","猫咪一般都很爱干净的"]
    embedding = DashScopeEmbeddings()
    queryVector = embedding.embed_documents(text)

    # 计算 "今天天气不错" (索引0) 和 "猫很爱干净" (索引1) 的距离
    dist_0_1 = euclidean_distance(queryVector[0], queryVector[1])
    print(f"距离('{text[0]}', '{text[1]}'): {dist_0_1:.4f}")

    # 计算 "今天天气不错" (索引0) 和 "猫咪一般都很爱干净的" (索引2) 的距离
    dist_0_2 = euclidean_distance(queryVector[0], queryVector[2])
    print(f"距离('{text[0]}', '{text[2]}'): {dist_0_2:.4f}")

    # 计算 "猫很爱干净" (索引1) 和 "猫咪一般都很爱干净的" (索引2) 的距离
    dist_1_2 = euclidean_distance(queryVector[1], queryVector[2])
    print(f"距离('{text[1]}', '{text[2]}'): {dist_1_2:.4f}")
