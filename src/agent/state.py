from typing import TypedDict, Optional, List, Dict

class BIState(TypedDict):
    """智能BI工作流状态：存储全流程数据"""
    # 输入
    user_input: str
    # 步骤1：需求分析结果
    demand_analysis: Optional[str]
    # 步骤2：MCP工具返回的库表结构
    db_schema: Optional[Dict]
    # 步骤2：生成的SQL
    generated_sql: Optional[str]
    # 步骤3：SQL校验结果 (pass/retry)
    sql_validation: Optional[str]
    # 步骤4：SQL执行结果
    sql_result: Optional[List[Dict]]
    # 最终输出
    final_output: Optional[str]
