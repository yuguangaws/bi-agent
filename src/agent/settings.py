import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatZhipuAI
from langchain_community.embeddings import ZhipuAIEmbeddings

# 加载环境变量
load_dotenv()

# ===================== LLM 配置 =====================
ZHIPUAI_API_KEY = os.getenv("ZHIPUAI_API_KEY")
ZHIPUAI_MODEL = os.getenv("ZHIPUAI_DEFAULT_MODEL", "glm-3-turbo")

# 生成用LLM
llm_generate = ChatZhipuAI(
    model=ZHIPUAI_MODEL,
    temperature=0,
    api_key=ZHIPUAI_API_KEY
)
# 校验用LLM
llm_validate = ChatZhipuAI(
    model=ZHIPUAI_MODEL,
    temperature=0,
    api_key=ZHIPUAI_API_KEY
)

# =====================  Embedding 配置 =====================
embedding = ZhipuAIEmbeddings(
    api_key=ZHIPUAI_API_KEY,
    model="embedding-2"
)

# ===================== 数据库配置 =====================
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "MyNew#Pass123",
    "database": "bi_test",
    "port": 3306
}
