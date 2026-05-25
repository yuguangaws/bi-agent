import os
import json
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.embeddings import ZhipuAIEmbeddings

# 加载环境变量
load_dotenv()

# 1. 读取 JSON 表元数据
def load_metadata_from_json():
    with open("table_metadata.json", "r", encoding="utf-8") as f:
        return json.load(f)

# 2. 初始化智谱 Embedding
embedding = ZhipuAIEmbeddings(
    api_key=os.getenv("ZHIPUAI_API_KEY"),
    model="embedding-2"
)

# 3. 构建向量库（自动持久化，无需 persist()）
def build_vector_db():
    try:
        metadata_list = load_metadata_from_json()
        docs = []
        
        for item in metadata_list:
            table_name = item["table_name"]
            columns = ", ".join(item["columns"])
            comment = item["comment"]
            
            page_content = f"表名：{table_name} | 字段：{columns} | 业务说明：{comment}"
            docs.append(Document(page_content=page_content, metadata=item))
        
        # ✅ 修复点：删除 db.persist()，新版自动保存
        db = Chroma.from_documents(
            documents=docs,
            embedding=embedding,
            persist_directory="./table_vector_db"  # 自动保存到这个文件夹
        )
        
        print("✅ 向量库构建成功！自动保存至 ./table_vector_db")
        
    except Exception as e:
        print(f"❌ 错误：{str(e)}")

if __name__ == "__main__":
    build_vector_db()
