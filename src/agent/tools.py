from typing import List, Dict
from langchain_chroma import Chroma
from src.agent.settings import DB_CONFIG, embedding

class MCPBITools:
    """MCP工具封装：数据库表结构查询、SQL执行"""
    def __init__(self, db_config):
        self.db_config = db_config

    def load_vector_db(self):
        """加载表结构向量库"""
        return Chroma(
            persist_directory="./table_vector_db",
            embedding_function=embedding
        )

    def get_relevant_tables(self, user_query: str, top_k=5) -> dict:
        """语义检索相关表结构"""
        db = self.load_vector_db()
        docs = db.similarity_search(user_query, k=top_k)
        
        table_schema = {}
        for doc in docs:
            table_name = doc.metadata["table_name"]
            columns = doc.metadata["columns"]
            table_schema[table_name] = columns
        return table_schema

    def execute_sql(self, sql: str) -> List[Dict]:
        """执行SQL语句"""
        import pymysql
        try:
            conn = pymysql.connect(**self.db_config)
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            return [{"error": f"SQL执行失败：{str(e)}"}]

# 初始化全局工具实例
mcp_tools = MCPBITools(DB_CONFIG)
