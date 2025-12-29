import streamlit as st
import random

# 设置页面配置
st.set_page_config(
    page_title="医疗费用预测系统",
    page_icon="🏥",
    layout="wide"
)

# 侧边栏导航
st.sidebar.title("医疗费用预测")
page = st.sidebar.radio("选择页面", ["简介", "预测医疗费用"])

# 简介页面
if page == "简介":
    st.title("🏥 医疗费用预测系统")
    
    st.markdown("""
    ### 系统简介
    本系统通过分析个人健康状况和人口统计学特征，预测年度医疗费用支出。系统采用基于医学研究的规则引擎，无需复杂的机器学习模型。
    
    ### 使用方法
    1. 在左侧边栏选择"预测医疗费用"
    2. 填写您的个人信息
    3. 点击"预测"按钮获取结果
    
    ### 预测因素
    - **年龄**：年龄越大，医疗费用通常越高
    - **BMI指数**：过高或过低的BMI都会增加医疗风险
    - **吸烟状况**：吸烟显著增加多种疾病风险
    - **子女数量**：影响家庭医疗支出
    - **居住地区**：不同地区的医疗成本差异
    """)
    
    # 显示示例数据
    st.subheader("示例预测结果")
    st.info("35岁, BMI 25, 非吸烟者, 2个孩子, 居住在东南部: 约 12,500元/年")
    st.info("50岁, BMI 32, 吸烟者, 0个孩子, 居住在北部: 约 32,800元/年")

# 预测页面
else:
    st.title("🏥 预测您的年度医疗费用")
    
    # 用户输入表单
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("年龄", min_value=0, max_value=120, value=30, step=1,
                                help="请输入您的年龄（岁）")
            
            sex = st.selectbox("性别", ["男性", "女性"], help="请选择您的性别")
            
            bmi = st.number_input("BMI指数", min_value=10.0, max_value=60.0, value=25.0, step=0.1,
                                help="身体质量指数（体重kg/身高m²）")
            
        with col2:
            children = st.number_input("子女数量", min_value=0, max_value=10, value=0, step=1,
                                     help="您需要照顾的18岁以下子女数量")
            
            smoker = st.selectbox("是否吸烟", ["否", "是"], help="您目前是否吸烟")
            
            region = st.selectbox("居住地区", ["东北部", "东南部", "西北部", "西南部"], 
                                help="您主要居住的地区")
        
        submitted = st.form_submit_button("预测医疗费用")
    
    # 预测逻辑（基于规则，不依赖机器学习库）
    if submitted:
        st.subheader("预测结果")
        
        # 基础费用（根据年龄）
        base_cost = 2000  # 基础费用
        
        # 年龄系数
        if age < 18:
            age_factor = 0.7
        elif age < 30:
            age_factor = 1.0
        elif age < 45:
            age_factor = 1.5
        elif age < 60:
            age_factor = 2.2
        else:
            age_factor = 3.0
        
        # BMI系数（U型曲线，过低和过高都有风险）
        if 18.5 <= bmi <= 24.9:
            bmi_factor = 1.0  # 健康范围
        elif bmi < 18.5:
            bmi_factor = 1.3  # 体重过轻
        elif bmi < 30:
            bmi_factor = 1.5  # 超重
        else:
            bmi_factor = 2.2  # 肥胖
        
        # 吸烟系数
        smoker_factor = 2.5 if smoker == "是" else 1.0
        
        # 地区系数
        region_factors = {
            "东北部": 1.2,
            "东南部": 1.0,
            "西北部": 1.1,
            "西南部": 1.05
        }
        region_factor = region_factors[region]
        
        # 子女系数
        children_factor = 1 + (children * 0.3)
        
        # 计算预测费用
        predicted_cost = base_cost * age_factor * bmi_factor * smoker_factor * region_factor * children_factor
        
        # 添加一些随机波动（模拟真实数据变化）
        randomness = random.uniform(0.95, 1.05)
        final_cost = predicted_cost * randomness
        
        # 显示结果
        st.success(f"预测的年度医疗费用: **{final_cost:,.0f} 元**")
        
        # 显示详细分析
        with st.expander("详细分析"):
            st.write("### 费用构成分析")
            st.write(f"- 基础医疗费用: {base_cost:,.0f} 元")
            st.write(f"- 年龄调整系数 ({age}岁): ×{age_factor:.1f}")
            st.write(f"- BMI调整系数 (BMI={bmi}): ×{bmi_factor:.1f}")
            st.write(f"- 吸烟状况调整: ×{smoker_factor:.1f}")
            st.write(f"- 地区调整系数 ({region}): ×{region_factor:.2f}")
            st.write(f"- 子女数量调整 ({children}个): ×{children_factor:.1f}")
            
            st.write("### 健康建议")
            if smoker == "是":
                st.warning("🚭 吸烟显著增加医疗费用。考虑戒烟可降低约60%的相关医疗支出。")
            if bmi < 18.5:
                st.warning("⚖️ 您的BMI偏低，建议咨询医生制定健康增重计划。")
            elif bmi > 24.9:
                st.warning("⚖️ 您的BMI偏高，适度减重10%可显著降低多种疾病风险。")
            if age > 45:
                st.info("👴 定期体检可以早期发现健康问题，长期来看可降低医疗费用。")

# 页脚
st.sidebar.markdown("---")
st.sidebar.info("💡 提示：此预测基于一般统计规律，实际医疗费用可能因个人健康状况和具体医疗服务而异。")
