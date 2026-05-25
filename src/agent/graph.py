from langgraph.graph import StateGraph, END
from src.agent.state import BIState
from src.agent.settings import llm_generate, llm_validate
from src.agent.tools import mcp_tools

# ===================== Graph 节点 =====================
def analyze_demand(state: BIState) -> BIState:
    """节点1：需求分析"""
    user_input = state["user_input"]
    prompt = f"""
    你是智能BI需求分析师，将用户自然语言转换为结构化查询需求：
    用户输入：{user_input}
    输出要求：明确查询指标、筛选条件、时间范围、关联表
    """
    response = llm_generate.invoke(prompt)
    return {"demand_analysis": response.content}

def generate_sql_via_mcp(state: BIState) -> BIState:
    """节点2：生成SQL"""
    demand = state["demand_analysis"]
    user_input = state["user_input"]
    
    schema = mcp_tools.get_relevant_tables(user_query=user_input)
    prompt = f"""
    你是SQL专家，根据需求和表结构生成合规SQL：
    1. 严格禁止使用 select *，必须指定字段
    2. 语法标准：MySQL
    3. 表结构：{schema}
    4. 用户需求：{demand}
    只输出纯SQL语句，不要任何解释, 禁止添加任何Markdown格式、反引号```、注释、多余符号、换行，仅返回干净的SQL文本
    """
    sql = llm_generate.invoke(prompt).content.strip()
    return {"db_schema": schema, "generated_sql": sql}

def validate_sql(state: BIState) -> BIState:
    """节点3：SQL校验"""
    user_input = state["user_input"]
    sql = state["generated_sql"]
    prompt = f"""
    你是SQL校验专家，执行2项校验，仅输出【pass】或【retry】：
    校验1：是否包含 select * → 包含则直接retry
    校验2：SQL逻辑是否匹配用户原始需求 → 不匹配则retry
    用户需求：{user_input}
    待校验SQL：{sql}
    输出：仅pass/retry
    """
    validation_result = llm_validate.invoke(prompt).content.strip().lower()
    return {"sql_validation": validation_result}

def execute_sql(state: BIState) -> BIState:
    """节点4：执行SQL"""
    sql = state["generated_sql"]
    result = mcp_tools.execute_sql(sql)
    return {"sql_result": result}

def generate_final_output(state: BIState) -> BIState:
    """节点5：生成最终报告"""
    result = state["sql_result"]
    demand = state["demand_analysis"]
    prompt = f"""
    你是BI报表分析师，将SQL结果转换为自然语言指标报告：
    用户需求：{demand}
    查询结果：{result}
    输出：简洁、易懂的业务指标
    """
    output = llm_generate.invoke(prompt).content
    return {"final_output": output}

# ===================== 条件路由 =====================
def sql_validation_router(state: BIState) -> str:
    return "execute_sql" if state["sql_validation"] == "pass" else "generate_sql_via_mcp"

# ===================== 构建工作流 =====================
def build_bi_graph():
    workflow = StateGraph(BIState)

    # 添加节点
    workflow.add_node("analyze_demand", analyze_demand)
    workflow.add_node("generate_sql_via_mcp", generate_sql_via_mcp)
    workflow.add_node("validate_sql", validate_sql)
    workflow.add_node("execute_sql", execute_sql)
    workflow.add_node("generate_final_output", generate_final_output)

    # 定义流转
    workflow.set_entry_point("analyze_demand")
    workflow.add_edge("analyze_demand", "generate_sql_via_mcp")
    workflow.add_edge("generate_sql_via_mcp", "validate_sql")

    # 条件边
    workflow.add_conditional_edges(
        "validate_sql",
        sql_validation_router,
        {
            "execute_sql": "execute_sql",
            "generate_sql_via_mcp": "generate_sql_via_mcp"
        }
    )

    workflow.add_edge("execute_sql", "generate_final_output")
    workflow.add_edge("generate_final_output", END)

    return workflow.compile()
