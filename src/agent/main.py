from src.agent.graph import build_bi_graph

if __name__ == "__main__":
    # 编译工作流
    bi_app = build_bi_graph()

    # 生成Mermaid流程图
    mermaid_graph = bi_app.get_graph().draw_mermaid()
    with open("bi_flowchart.md", "w", encoding="utf-8") as f:
        f.write("# 智能BI工作流\n```mermaid\n" + mermaid_graph + "\n```")
    print("✅ 流程图已生成：bi_flowchart.md")
    print("🔗 在线渲染：https://mermaid.live/")

    # 测试查询
    user_query = "查询最大买家名字和订单总金额，按订单总金额降序排列，显示前10条记录。"
    result = bi_app.invoke({
        "user_input": user_query,
        "demand_analysis": None,
        "db_schema": None,
        "generated_sql": None,
        "sql_validation": None,
        "sql_result": None,
        "final_output": None
    })

    # 打印结果
    print("="*50)
    print("用户需求：", user_query)
    print("生成的SQL：", result["generated_sql"])
    print("SQL校验结果：", result["sql_validation"])
    print("BI最终报告：\n", result["final_output"])
