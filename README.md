## Getting Started
0. 学习langgraph以来写的第一个agent
流程图如下：
<img width="685" height="1266" alt="image" src="https://github.com/user-attachments/assets/6a93539f-4751-4bed-ad1c-75004134fec2" />

个人总结：智能查数最关键的点是让LLM充分理解表结构，根据用户的输入生成最正确的SQL语句，所以代码里
- rag-builder.py是用来将表结构信息向量化，表结构信息见table_metadata.json
- tools.py里的get_relevant_tables是将用户的输入和向量库里的表结构信息匹配，以选择最合适的表和字段，并生成最准确的SQL语句
- graph.py里的validate_sql用于将生成的SQL和用户的需求做二次校验，通过后才执行SQL，不通过则重试上述步骤
- streamlit_app.py做一个简单的UI页面

#
1. Install dependencies

```bash
cd path/to/your/app
uv pip install -r requirement.txt
```
#
2. Customize the code and project as needed. Create a `.env` file if you need to use secrets.

```bash
cp .env.example .env
# .env，这里用的智谱的API
ZHIPUAI_API_KEY=xxxxxx
ZHIPUAI_DEFAULT_MODEL=glm-3-turbo
```
#
3. Start the bi-agent.

```shell
streamlit run streamlit_app.py
```
#
实际运行效果图如下：
<img width="3612" height="4176" alt="image" src="https://github.com/user-attachments/assets/5fdd413b-302d-4f9e-91e9-ef21d9c48906" />
