import streamlit as st
import pandas as pd
# 直接导入你现有的BI Agent工作流
from src.agent.graph import build_bi_graph

# 页面配置
st.set_page_config(
    page_title="智能BI分析助手",
    page_icon="📊",
    layout="wide"
)
st.title("📊 智能BI数据分析助手")
st.subheader("输入自然语言，自动查询数据库并生成可视化图表")

# 初始化Agent（缓存，避免重复加载）
@st.cache_resource
def get_agent():
    return build_bi_graph()

bi_app = get_agent()

# 输入框
user_query = st.text_input(
    "请输入你的查询需求：",
    placeholder="例如：查询总销量最高的产品和金额、统计本月销售额排行"
)

# 执行按钮
if st.button("开始分析") and user_query:
    with st.spinner("🤖 AI正在分析需求、生成SQL、查询数据..."):
        # 调用你的BI Agent（和main.py逻辑完全一致）
        result = bi_app.invoke({
            "user_input": user_query,
            "demand_analysis": None,
            "db_schema": None,
            "generated_sql": None,
            "sql_validation": None,
            "sql_result": None,
            "final_output": None
        })

    # ========== 展示结果 ==========
    st.success("✅ 查询完成！")
    
    # 分栏展示
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 需求分析")
        st.write(result["demand_analysis"])
        
        st.markdown("### 🧾 生成的SQL")
        st.code(result["generated_sql"], language="sql")
        
        st.markdown("### ✅ SQL校验结果")
        st.write(result["sql_validation"])
    
    with col2:
        st.markdown("### 📊 查询结果数据")
        df = pd.DataFrame(result["sql_result"])
        st.dataframe(df, use_container_width=True)
        
        # 自动可视化（针对销量/金额字段，适配BI场景）
        st.markdown("### 📈 数据可视化")
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_cols) > 0:
            # 柱状图（最适合BI指标展示）
            st.bar_chart(df, x=df.columns[0], y=numeric_cols[0])
        else:
            st.write("暂无数值型数据可可视化")

    st.markdown("### 🎯 BI最终报告")
    st.write(result["final_output"])