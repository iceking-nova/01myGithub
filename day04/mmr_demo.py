"""LangChain：普通相似度搜索与 MMR 搜索对比。

安装依赖（PowerShell）：
    python -m pip install "langchain-chroma>=1.0.0" langchain-community dashscope

设置阿里云百炼 API Key 并运行（使用中国内地服务）：
    $env:DASHSCOPE_API_KEY = "你的 API Key"
    python mmr_demo.py

文本向量由 DashScope 在线生成，需要网络和有效 API Key。
"""

import os

from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.documents import Document


if __name__ == "__main__":
    if not os.getenv("DASHSCOPE_API_KEY"):
        raise SystemExit("请先设置环境变量 DASHSCOPE_API_KEY，运行方式见文件顶部。")

    # 1. 准备文档：前三段意思相近，方便观察 MMR 如何减少重复。
    documents = [
        "学习人工智能需要先掌握线性代数、概率论和微积分，这是算法的基础。",
        "人工智能入门应先学线性代数、概率统计和微积分，打好数学基础。",
        "学习 AI 之前，建议先补齐线性代数、概率论与微积分等数学知识。",
        "学习人工智能还需要掌握 Python，熟悉 NumPy、pandas 等数据处理库。",
        "学习人工智能可以通过 Kaggle 项目实战，从泰坦尼克号预测等项目开始练手。",
        "学习人工智能可以看吴恩达的机器学习课程，再逐步学习深度学习。",
    ]
    data = [Document(page_content=text) for text in documents]

    # 2. 创建向量库，使用余弦距离；本示例仅存内存，便于反复运行。
    chroma_db = Chroma(
        collection_name="mmr_demo",
        embedding_function=DashScopeEmbeddings(),
        collection_configuration={"hnsw": {"space": "cosine"}},
    )
    chroma_db.add_documents(
        documents=data,
        ids=[f"id-{i}" for i in range(len(data))],
    )

    # 3. 用户查询。
    query = "学习人工智能需要掌握哪些基础知识，应该如何入门？"
    print(f"查询：{query}")

    # 4. 普通相似度搜索：直接返回与问题最相似的 3 段。
    print("\n【普通相似度搜索】")
    results = chroma_db.similarity_search(query, k=3)
    for i, doc in enumerate(results, start=1):
        print(f"{i}. {doc.page_content}")

    # 5. MMR：先找候选，再兼顾相关性与多样性，选出 3 段。
    print("\n【MMR 搜索】")
    mmr_results = chroma_db.max_marginal_relevance_search(
        query,
        k=3,                     # 最终返回 3 段。
        fetch_k=len(documents),  # 先取 6 段候选，再交给 MMR 筛选。
        lambda_mult=0.5,         # 越接近 1 越重视相关性，越接近 0 越重视多样性。
    )
    for i, doc in enumerate(mmr_results, start=1):
        print(f"{i}. {doc.page_content}")

    print("\n可以尝试把 lambda_mult 改成 1.0 或 0.2，对比选中的内容。")
    print("具体结果由向量模型决定；MMR 不保证每次都选出固定的几段。")
