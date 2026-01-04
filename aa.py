import matplotlib
matplotlib.use('Agg')
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import joblib
import matplotlib
from sklearn.metrics import mean_squared_error, r2_score
from PIL import Image
import requests
from io import BytesIO
import platform

# ================ GitHub 仓库配置 ================
# 请修改以下三行为您自己的GitHub信息
GITHUB_USER = "your_github_username"  # 替换为您的GitHub用户名
GITHUB_REPO = "your_repository_name"  # 替换为您的仓库名
GITHUB_BRANCH = "main"  # 替换为您的分支名（通常是main或master）

# 构建GitHub raw URL的函数
def get_github_raw_url(filename):
    return f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}/{filename}"

# ============== 关键修复：设置中文字体支持 ==============
def setup_chinese_font():
    """设置中文字体以解决方框问题"""
    # 获取系统平台
    system_platform = platform.system().lower()
    
    try:
        # Windows 系统字体
        if 'windows' in system_platform:
            plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'KaiTi', 'SimSun']
        # macOS 系统字体
        elif 'darwin' in system_platform:
            plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Heiti TC', 'STSong']
        # Linux 系统字体
        elif 'linux' in system_platform:
            plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei', 'Noto Sans CJK SC', 'Droid Sans Fallback']
        else:
            # 默认字体
            plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'Microsoft YaHei']
        
        # 确保能显示负号
        plt.rcParams['axes.unicode_minus'] = False
        
        # 设置字体大小
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.titlesize'] = 12
        plt.rcParams['axes.labelsize'] = 10
        plt.rcParams['xtick.labelsize'] = 9
        plt.rcParams['ytick.labelsize'] = 9
        plt.rcParams['legend.fontsize'] = 10
        
        # 设置图形质量
        plt.rcParams['figure.dpi'] = 100
        plt.rcParams['savefig.dpi'] = 100
        
        st.success("✅ 中文字体配置成功")
        return True
    except Exception as e:
        st.warning(f"字体配置警告: {str(e)}")
        st.info("使用英文标签作为备选方案")
        return False

# 执行字体设置
use_chinese = setup_chinese_font()

# 如果字体设置失败，使用英文标签
def get_labels(use_chinese=True):
    """根据字体支持情况返回相应的标签"""
    if use_chinese:
        return {
            'gender_ratio_title': '各专业男女比例',
            'gender_ratio_xlabel': '专业',
            'gender_ratio_ylabel': '比例 (%)',
            'score_trends_title': '各专业期中期末成绩对比',
            'score_trends_xlabel': '专业',
            'score_trends_ylabel': '平均分数',
            'attendance_title': '各专业平均上课出勤率',
            'attendance_xlabel': '专业',
            'attendance_ylabel': '平均出勤率',
            'male': '男',
            'female': '女',
            'midterm': '期中考试',
            'final': '期末考试'
        }
    else:
        return {
            'gender_ratio_title': 'Gender Ratio by Major',
            'gender_ratio_xlabel': 'Major',
            'gender_ratio_ylabel': 'Ratio (%)',
            'score_trends_title': 'Midterm vs Final Scores by Major',
            'score_trends_xlabel': 'Major',
            'score_trends_ylabel': 'Average Score',
            'attendance_title': 'Average Class Attendance by Major',
            'attendance_xlabel': 'Major',
            'attendance_ylabel': 'Attendance Rate',
            'male': 'Male',
            'female': 'Female',
            'midterm': 'Midterm',
            'final': 'Final'
        }

# 获取当前使用的标签
labels = get_labels(use_chinese)

# 设置页面配置
st.set_page_config(page_title="学生成绩分析与预测系统", layout="wide")

# 从GitHub加载预训练模型
@st.cache_resource
def load_trained_model():
    try:
        # 从GitHub获取模型
        model_url = get_github_raw_url("student_performance_model.pkl")
        st.info(f"正在从GitHub加载模型: {model_url}")
        
        response = requests.get(model_url, timeout=30)
        
        if response.status_code == 200:
            model = joblib.load(BytesIO(response.content))
            st.success("✅ 成功从GitHub加载预训练模型")
            return model
        else:
            st.error(f"无法从GitHub下载模型，状态码: {response.status_code}")
            st.info("请检查GitHub仓库配置是否正确，或模型文件是否存在")
            return None
        
    except Exception as e:
        st.error(f"加载模型时出错: {str(e)}")
        st.exception(e)
        st.info("请确保student_performance_model.pkl文件已上传到您的GitHub仓库")
        return None

# 从GitHub加载数据
@st.cache_data
def load_data():
    try:
        # 从GitHub获取数据
        data_url = get_github_raw_url("student_data.csv")
        st.info(f"正在从GitHub加载数据: {data_url}")
        
        response = requests.get(data_url, timeout=30)
        
        if response.status_code == 200:
            # 读取CSV文件，没有列名，需要指定
            df = pd.read_csv(BytesIO(response.content), header=None)
            
            # 检查列数
            if df.shape[1] < 8:
                st.warning(f"数据文件列数不足，当前有 {df.shape[1]} 列，需要 8 列。将使用模拟数据。")
                return generate_sample_data()
                
            # 设置列名 - 与训练模型时使用的列名一致
            df.columns = ['学号', '性别', '专业', '特征1', '特征2', '特征3', '特征4', '成绩']
            
            # 转换数值列
            numeric_columns = ['特征1', '特征2', '特征3', '特征4', '成绩']
            for col in numeric_columns:
                # 尝试将列转换为数值，无法转换的设为NaN
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # 数据清洗
            # 1. 删除包含NaN的行
            df = df.dropna(subset=numeric_columns)
            
            # 2. 过滤异常值
            df = df[
                (df['成绩'].between(40, 100)) &
                (df['特征3'].between(40, 100)) &  # 特征3对应期中成绩
                (df['特征1'].between(0, 60)) &    # 特征1对应学习时长
                (df['特征2'].between(0, 1)) &     # 特征2对应出勤率
                (df['特征4'].between(0, 1))       # 特征4对应作业完成率
            ]
            
            # 3. 确保分类列是字符串
            df['性别'] = df['性别'].astype(str).str.strip()
            df['专业'] = df['专业'].astype(str).str.strip()
            df['学号'] = df['学号'].astype(str).str.strip()
            
            # 4. 重置索引
            df = df.reset_index(drop=True)
            
            st.success(f"✅ 成功加载 {len(df)} 条有效学生记录")
            return df
        else:
            st.warning(f"⚠️ 无法从GitHub下载数据文件 (状态码: {response.status_code})，使用模拟数据")
            return generate_sample_data()
    except Exception as e:
        st.error(f"加载数据时出错: {e}")
        st.exception(e)  # 显示完整异常信息
        return generate_sample_data()

def generate_sample_data():
    """生成模拟数据用于演示"""
    np.random.seed(42)
    majors = ['人工智能', '信息工程', '大数据管理', '工商管理', '网络空间安全', '软件工程']
    genders = ['男', '女']
    
    n_samples = 200
    data = {
        '学号': [f"2023{i:05d}" for i in range(n_samples)],
        '性别': np.random.choice(genders, n_samples, p=[0.6, 0.4]),
        '专业': np.random.choice(majors, n_samples),
        '特征1': np.clip(np.random.normal(25, 8, n_samples), 5, 50),  # 学习时长
        '特征2': np.clip(np.random.normal(0.8, 0.15, n_samples), 0.5, 1.0),  # 出勤率
        '特征3': np.clip(np.random.normal(75, 10, n_samples), 40, 100),  # 期中成绩
        '特征4': np.clip(np.random.normal(0.85, 0.1, n_samples), 0.6, 1.0),  # 作业完成率
        '成绩': np.clip(np.random.normal(80, 12, n_samples), 40, 100)  # 期末成绩
    }
    
    df = pd.DataFrame(data)
    st.info("ℹ️ 使用模拟数据运行系统")
    return df

# 评估模型性能 (使用测试集)
def evaluate_model(model, df):
    try:
        if len(df) < 20:
            return None, None
        
        # 准备特征和目标变量
        X = df[['性别', '专业', '特征1', '特征2', '特征3', '特征4']]
        y = df['成绩']
        
        # 只使用20%的数据进行评估
        from sklearn.model_selection import train_test_split
        _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # 预测
        y_pred = model.predict(X_test)
        
        # 评估
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        return r2, rmse
    except Exception as e:
        st.error(f"评估模型时出错: {str(e)}")
        st.exception(e)
        return None, None

# 创建专业统计数据
def create_major_stats(df):
    # 确保数值列是正确的类型
    for col in ['特征1', '特征2', '特征3', '成绩']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    major_stats = df.groupby('专业').agg(
        avg_study_hours=('特征1', 'mean'),  # 特征1 = 学习时长
        avg_midterm=('特征3', 'mean'),     # 特征3 = 期中成绩
        avg_final=('成绩', 'mean'),        # 成绩 = 期末成绩
        avg_attendance=('特征2', 'mean'),  # 特征2 = 出勤率
        male_ratio=('性别', lambda x: (x == '男').mean() * 100),
        female_ratio=('性别', lambda x: (x == '女').mean() * 100),
        count=('学号', 'count')
    ).reset_index()
    
    # 确保所有列都是数值类型
    for col in ['avg_study_hours', 'avg_midterm', 'avg_final', 'avg_attendance', 'male_ratio', 'female_ratio']:
        major_stats[col] = pd.to_numeric(major_stats[col], errors='coerce')
    
    # 删除包含NaN的行
    major_stats = major_stats.dropna()
    
    return major_stats

# 创建专业分析图表 - 使用正确的中文字体
def plot_gender_ratio(major_stats):
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(major_stats['专业']))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, major_stats['male_ratio'], width, label=labels['male'], color='#4A90E2')
    bars2 = ax.bar(x + width/2, major_stats['female_ratio'], width, label=labels['female'], color='#FF6B6B')
    
    ax.set_xlabel(labels['gender_ratio_xlabel'], fontsize=12)
    ax.set_ylabel(labels['gender_ratio_ylabel'], fontsize=12)
    ax.set_title(labels['gender_ratio_title'], fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(major_stats['专业'], rotation=45, ha='right', fontsize=10)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    # 添加数据标签
    for bar in bars1 + bars2:
        height = bar.get_height()
        if not np.isnan(height):
            ax.annotate(f'{height:.1f}%',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom',
                       fontsize=9)
    
    plt.tight_layout()
    return fig

def plot_score_trends(major_stats):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = range(len(major_stats['专业']))
    ax.plot(x, major_stats['avg_midterm'], marker='o', label=labels['midterm'], linewidth=2, markersize=8, color='#4A90E2')
    ax.plot(x, major_stats['avg_final'], marker='s', label=labels['final'], linewidth=2, markersize=8, color='#FF6B6B')
    
    ax.set_xlabel(labels['score_trends_xlabel'], fontsize=12)
    ax.set_ylabel(labels['score_trends_ylabel'], fontsize=12)
    ax.set_title(labels['score_trends_title'], fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(major_stats['专业'], rotation=45, ha='right', fontsize=10)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 设置y轴范围
    min_score = max(40, min(major_stats['avg_midterm'].min(), major_stats['avg_final'].min()) - 10)
    max_score = min(100, max(major_stats['avg_midterm'].max(), major_stats['avg_final'].max()) + 10)
    ax.set_ylim(min_score, max_score)
    
    plt.tight_layout()
    return fig

def plot_attendance_rates(major_stats):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars = ax.bar(major_stats['专业'], major_stats['avg_attendance'], color='#2ECC71')
    
    ax.set_xlabel(labels['attendance_xlabel'], fontsize=12)
    ax.set_ylabel(labels['attendance_ylabel'], fontsize=12)
    ax.set_title(labels['attendance_title'], fontsize=14, fontweight='bold')
    ax.set_ylim(0.5, 1.0)
    ax.grid(axis='y', alpha=0.3)
    
    # 添加数据标签
    for bar in bars:
        height = bar.get_height()
        if not np.isnan(height):
            ax.annotate(f'{height:.1%}',
                       xy=(bar.get_x() + bar.get_width()/2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom',
                       fontsize=9)
    
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.tight_layout()
    return fig

# 从GitHub加载图片
def load_image_from_github(filename, caption):
    try:
        img_url = get_github_raw_url(filename)
        response = requests.get(img_url, timeout=10)
        
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            st.image(img, caption=caption, use_container_width=True)
            return img
        else:
            st.warning(f"无法加载图片 {filename}，状态码: {response.status_code}")
            return None
    except Exception as e:
        st.warning(f"无法加载图片 {filename}: {str(e)}")
        return None

# 获取默认图片（当GitHub图片不存在时）
def get_default_image():
    # 使用一个简单的占位图
    fig, ax = plt.subplots(figsize=(8, 4))
    if use_chinese:
        ax.text(0.5, 0.5, '学生成绩分析系统', 
                ha='center', va='center', 
                fontsize=20, color='#4A90E2',
                fontproperties=matplotlib.font_manager.FontProperties(
                    family=['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']))
    else:
        ax.text(0.5, 0.5, 'Student Performance Analysis System', 
                ha='center', va='center', 
                fontsize=16, color='#4A90E2')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    buf.seek(0)
    plt.close(fig)
    return buf

# 创建成功/鼓励图片
def create_result_image(passed=True):
    fig, ax = plt.subplots(figsize=(6, 3))
    if passed:
        if use_chinese:
            text = "成绩预测：通过！"
            color = '#2ECC71'
        else:
            text = "Prediction: Pass!"
            color = '#2ECC71'
    else:
        if use_chinese:
            text = "成绩预测：需要努力"
            color = '#FF6B6B'
        else:
            text = "Prediction: Needs Work"
            color = '#FF6B6B'
    
    ax.text(0.5, 0.5, text, 
            ha='center', va='center', 
            fontsize=18, color='white', 
            bbox=dict(facecolor=color, alpha=0.8, boxstyle='round,pad=1'))
    ax.axis('off')
    
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    buf.seek(0)
    plt.close(fig)
    return buf

# 主函数
def main():
    # 侧边栏导航
    st.sidebar.title("🎓 学生成绩分析系统")
    page = st.sidebar.radio("选择页面", ["项目介绍", "专业分析", "成绩预测"])
    
    # 加载数据
    df = load_data()
    
    # 加载预训练模型
    model = None
    r2, rmse = None, None
    if page == "成绩预测" or page == "专业分析":
        model = load_trained_model()
        if model is not None:
            r2, rmse = evaluate_model(model, df)
    
    # 创建专业统计数据
    major_stats = None
    if page == "专业分析" and len(df) > 0:
        major_stats = create_major_stats(df)
    
    # 页面1: 项目介绍
    if page == "项目介绍":
        if use_chinese:
            st.title("🎓 学生成绩分析与预测系统")
        else:
            st.title("🎓 Student Performance Analysis & Prediction System")
        
        if use_chinese:
            st.header("🖼️ 系统界面展示")
        else:
            st.header("🖼️ System Interface")
        
        # 从GitHub加载首页图片
        homepage_img = load_image_from_github("首页.png", "系统主界面" if use_chinese else "System Main Interface")
        if homepage_img is None:
            st.info("使用默认界面" if use_chinese else "Using default interface")
            default_img = get_default_image()
            st.image(default_img, caption="系统主界面 (默认图片)" if use_chinese else "System Interface (Default)", use_container_width=True)
        
        if use_chinese:
            st.header("📋 项目概述")
            st.write("""
            本系统是一个基于机器学习的学生成绩分析平台，通过对学生历史成绩数据的分析，
            识别影响学业表现的关键因素，并预测未来成绩表现。
            系统整合了数据可视化和预测模型，为教育工作者提供数据驱动的决策支持。
            """)
        else:
            st.header("📋 Project Overview")
            st.write("""
            This system is a machine learning-based student performance analysis platform. By analyzing 
            historical student grade data, it identifies key factors affecting academic performance and 
            predicts future grade performance. The system integrates data visualization and predictive models 
            to provide data-driven decision support for educators.
            """)
        
        if use_chinese:
            st.header("🎯 项目目标")
        else:
            st.header("🎯 Project Goals")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if use_chinese:
                st.subheader("分析关键因素")
                st.write("""
                - 识别影响成绩的主要因素
                - 分析不同专业间的成绩差异
                - 研究学习行为与成绩的关系
                """)
            else:
                st.subheader("Analyze Key Factors")
                st.write("""
                - Identify main factors affecting grades
                - Analyze performance differences across majors
                - Study relationship between study habits and grades
                """)
        
        with col2:
            if use_chinese:
                st.subheader("可视化展示")
                st.write("""
                - 专业成绩分布对比
                - 性别与成绩的关联分析
                - 期中期末成绩相关性
                """)
            else:
                st.subheader("Visualization")
                st.write("""
                - Compare grade distributions by major
                - Analyze gender vs performance correlation
                - Midterm vs final exam correlations
                """)
        
        with col3:
            if use_chinese:
                st.subheader("智能预测")
                st.write("""
                - 基于历史数据预测期末成绩
                - 提供个性化学习建议
                - 早期预警潜在问题学生
                """)
            else:
                st.subheader("Smart Prediction")
                st.write("""
                - Predict final grades based on historical data
                - Provide personalized study recommendations
                - Early warning for at-risk students
                """)
        
        # 显示系统架构图
        if use_chinese:
            st.header("⚙️ 系统架构")
        else:
            st.header("⚙️ System Architecture")
        
        system_architecture = """
        数据输入 → 数据预处理 → 特征工程 → 模型训练 → 预测分析 → 可视化展示
        """ if use_chinese else """
        Data Input → Data Preprocessing → Feature Engineering → Model Training → Prediction Analysis → Visualization
        """
        st.code(system_architecture, language='text')
        
        if use_chinese:
            st.subheader("技术栈")
            st.markdown("""
            - **数据处理**: Pandas, NumPy
            - **可视化**: Matplotlib, Seaborn
            - **机器学习**: Scikit-learn, Random Forest
            - **应用框架**: Streamlit
            """)
        else:
            st.subheader("Tech Stack")
            st.markdown("""
            - **Data Processing**: Pandas, NumPy
            - **Visualization**: Matplotlib, Seaborn
            - **Machine Learning**: Scikit-learn, Random Forest
            - **Application Framework**: Streamlit
            """)
        
        # 数据概览
        if use_chinese:
            st.header("📊 数据概览")
        else:
            st.header("📊 Data Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("总学生数" if use_chinese else "Total Students", len(df))
        
        with col2:
            if '专业' in df.columns:
                st.metric("专业数" if use_chinese else "Majors", df['专业'].nunique())
        
        with col3:
            if '性别' in df.columns:
                male_ratio = (df['性别'] == '男').mean() * 100
                st.metric("男生比例" if use_chinese else "Male Ratio", f"{male_ratio:.1f}%")
        
        with col4:
            if '成绩' in df.columns:
                avg_final = df['成绩'].mean()
                st.metric("平均期末成绩" if use_chinese else "Avg Final Score", f"{avg_final:.1f}")
        
        # 显示数据样本 - 调整列名显示
        if use_chinese:
            st.subheader("数据样本")
        else:
            st.subheader("Data Sample")
        
        display_df = df.head(10).copy()
        # 重命名列以便更好地理解
        if use_chinese:
            display_df = display_df.rename(columns={
                '学号': 'Student ID',
                '性别': 'Gender',
                '专业': 'Major',
                '特征1': 'Study Hours',
                '特征2': 'Attendance Rate',
                '特征3': 'Midterm Score',
                '特征4': 'Homework Completion',
                '成绩': 'Final Score'
            })
        else:
            display_df = display_df.rename(columns={
                '学号': 'Student ID',
                '性别': 'Gender',
                '专业': 'Major',
                '特征1': 'Study Hours',
                '特征2': 'Attendance Rate',
                '特征3': 'Midterm',
                '特征4': 'Homework Completion',
                '成绩': 'Final Score'
            })
        st.dataframe(display_df)
    
    # 页面2: 专业分析
    elif page == "专业分析":
        st.title("📊 专业数据分析" if use_chinese else "📊 Major Data Analysis")
        
        if major_stats is None or len(major_stats) == 0:
            st.error("无法生成专业统计数据，请检查数据格式" if use_chinese else "Cannot generate major statistics, please check data format")
            return
        
        # 1. 各专业学习指标对比表格
        if use_chinese:
            st.subheader("1. 各专业学习指标对比")
        else:
            st.subheader("1. Learning Metrics Comparison by Major")
        
        display_df = major_stats.copy()
        display_df['avg_study_hours'] = display_df['avg_study_hours'].round(1)
        display_df['avg_midterm'] = display_df['avg_midterm'].round(1)
        display_df['avg_final'] = display_df['avg_final'].round(1)
        display_df['avg_attendance'] = (display_df['avg_attendance'] * 100).round(1).astype(str) + '%'
        
        st.dataframe(
            display_df[['专业', 'avg_study_hours', 'avg_midterm', 'avg_final', 'avg_attendance']],
            use_container_width=True,
            column_config={
                '专业': '专业' if use_chinese else 'Major',
                'avg_study_hours': '周均学习时长(小时)' if use_chinese else 'Weekly Study Hours',
                'avg_midterm': '期中平均分' if use_chinese else 'Avg Midterm',
                'avg_final': '期末平均分' if use_chinese else 'Avg Final',
                'avg_attendance': '平均出勤率' if use_chinese else 'Avg Attendance'
            }
        )
        
        # 2. 各专业男女性别比例 - 双层柱状图
        if use_chinese:
            st.subheader("2. 各专业男女性别比例")
        else:
            st.subheader("2. Gender Ratio by Major")
        
        fig_gender = plot_gender_ratio(major_stats)
        st.pyplot(fig_gender)
        
        # 3. 各专业学习指标对比 - 折线图
        if use_chinese:
            st.subheader("3. 各专业期中期末成绩对比")
        else:
            st.subheader("3. Midterm vs Final Scores by Major")
        
        fig_scores = plot_score_trends(major_stats)
        st.pyplot(fig_scores)
        
        # 4. 各专业出勤率分析 - 单层柱状图
        if use_chinese:
            st.subheader("4. 各专业出勤率分析")
        else:
            st.subheader("4. Attendance Rate Analysis by Major")
        
        fig_attendance = plot_attendance_rates(major_stats)
        st.pyplot(fig_attendance)
        
        # 5. 大数据管理专业专项分析
        if use_chinese:
            st.subheader("5. 大数据管理专业专项分析")
        else:
            st.subheader("5. Big Data Management Major Analysis")
        
        # 获取大数据管理专业数据
        bigdata_stats = major_stats[major_stats['专业'] == '大数据管理']
        
        if not bigdata_stats.empty:
            bigdata_stats = bigdata_stats.iloc[0]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("平均出勤率" if use_chinese else "Avg Attendance", f"{bigdata_stats['avg_attendance']:.1%}")
            with col2:
                st.metric("平均期末成绩" if use_chinese else "Avg Final Score", f"{bigdata_stats['avg_final']:.1f}分" if use_chinese else f"{bigdata_stats['avg_final']:.1f}")
            with col3:
                st.metric("周均学习时间" if use_chinese else "Weekly Study Time", f"{bigdata_stats['avg_study_hours']:.1f}小时" if use_chinese else f"{bigdata_stats['avg_study_hours']:.1f} hrs")
            
            # 从原始数据中提取大数据管理专业的学生
            bigdata_students = df[df['专业'] == '大数据管理']
            
            # 确保数值列是数字类型
            for col in ['特征2', '成绩']:  # 特征2 = 出勤率, 成绩 = 期末成绩
                bigdata_students[col] = pd.to_numeric(bigdata_students[col], errors='coerce')
            
            if len(bigdata_students) > 10:
                # 创建子图
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
                
                # 出勤率与期末成绩散点图
                ax1.scatter(bigdata_students['特征2'], bigdata_students['成绩'], 
                           alpha=0.7, color='#2ECC71', edgecolors='black')
                if use_chinese:
                    ax1.set_title('出勤率与期末成绩关系', fontsize=12, fontweight='bold')
                    ax1.set_xlabel('上课出勤率', fontsize=10)
                    ax1.set_ylabel('期末成绩', fontsize=10)
                else:
                    ax1.set_title('Attendance vs Final Score', fontsize=12, fontweight='bold')
                    ax1.set_xlabel('Attendance Rate', fontsize=10)
                    ax1.set_ylabel('Final Score', fontsize=10)
                ax1.grid(True, alpha=0.3)
                
                # 设置x轴和y轴范围
                ax1.set_xlim(0.4, 1.0)
                ax1.set_ylim(40, 100)
                
                # 期末成绩分布直方图
                ax2.hist(bigdata_students['成绩'], bins=10, edgecolor='black', 
                        alpha=0.7, color='#3498DB')
                if use_chinese:
                    ax2.set_title('期末成绩分布', fontsize=12, fontweight='bold')
                    ax2.set_xlabel('期末成绩', fontsize=10)
                    ax2.set_ylabel('学生数量', fontsize=10)
                else:
                    ax2.set_title('Final Score Distribution', fontsize=12, fontweight='bold')
                    ax2.set_xlabel('Final Score', fontsize=10)
                    ax2.set_ylabel('Number of Students', fontsize=10)
                ax2.grid(True, alpha=0.3)
                
                # 设置x轴范围
                ax2.set_xlim(40, 100)
                
                plt.tight_layout()
                st.pyplot(fig)
            else:
                st.warning("大数据管理专业学生数量不足，无法生成详细分析图表" if use_chinese else "Not enough students in Big Data Management major to generate detailed analysis charts")
        else:
            st.warning("未找到大数据管理专业的数据" if use_chinese else "No data found for Big Data Management major")
    
    # 页面3: 成绩预测
    elif page == "成绩预测":
        if use_chinese:
            st.title("🎯 期末成绩预测")
        else:
            st.title("🎯 Final Grade Prediction")
        
        if model is None:
            st.error("模型加载失败，无法进行预测" if use_chinese else "Model loading failed, cannot make predictions")
            return
        
        # 显示模型性能
        if use_chinese:
            st.subheader("模型性能")
        else:
            st.subheader("Model Performance")
        
        col1, col2 = st.columns(2)
        with col1:
            if r2 is not None:
                st.metric("R²分数" if use_chinese else "R² Score", f"{r2:.3f}")
            else:
                st.metric("R²分数" if use_chinese else "R² Score", "N/A")
        with col2:
            if rmse is not None:
                st.metric("RMSE" if use_chinese else "RMSE", f"{rmse:.2f}")
            else:
                st.metric("RMSE" if use_chinese else "RMSE", "N/A")
        
        # 用户输入表单 - 添加错误处理
        if use_chinese:
            st.subheader("请输入学生信息")
        else:
            st.subheader("Enter Student Information")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            student_id = st.text_input("学号" if use_chinese else "Student ID", "2023123456")
            gender = st.selectbox("性别" if use_chinese else "Gender", ["男", "女"] if use_chinese else ["Male", "Female"])
            
            # 获取专业列表
            majors = df['专业'].unique().tolist() if '专业' in df.columns else ['人工智能', '信息工程', '大数据管理', '工商管理', '网络空间安全', '软件工程']
            major_label = "专业" if use_chinese else "Major"
            major = st.selectbox(major_label, majors)
        
        with col2:
            study_label = "每周学习时长 (小时)" if use_chinese else "Weekly Study Hours"
            study_hours = st.slider(study_label, 0.0, 50.0, 20.0, 1.0)  # 对应 特征1
            
            attendance_label = "上课出勤率" if use_chinese else "Class Attendance Rate"
            attendance_rate = st.slider(attendance_label, 0.0, 1.0, 0.8, 0.05)      # 对应 特征2
            
            midterm_label = "期中考试分数" if use_chinese else "Midterm Score"
            midterm_score = st.slider(midterm_label, 0.0, 100.0, 70.0, 1.0)    # 对应 特征3
            
            homework_label = "作业完成率" if use_chinese else "Homework Completion Rate"
            homework_completion_rate = st.slider(homework_label, 0.0, 1.0, 0.9, 0.05)  # 对应 特征4
        
        # 预测按钮
        predict_button = "预测期末成绩" if use_chinese else "Predict Final Grade"
        if st.button(predict_button, type="primary"):
            try:
                # 构建输入数据 - 使用与训练模型相同的特征名称
                input_data = pd.DataFrame({
                    '性别': [gender],
                    '专业': [major],
                    '特征1': [float(study_hours)],  # 学习时长
                    '特征2': [float(attendance_rate)],  # 出勤率
                    '特征3': [float(midterm_score)],  # 期中成绩
                    '特征4': [float(homework_completion_rate)]  # 作业完成率
                })
                
                # 预测
                prediction = model.predict(input_data)[0]
                predicted_score = round(prediction, 1)
                
                # 防止预测值超出合理范围
                predicted_score = max(40, min(100, predicted_score))
                
                # 显示结果
                if use_chinese:
                    st.subheader("📊 预测结果")
                else:
                    st.subheader("📊 Prediction Results")
                
                # 根据预测分数结果选择不同显示
                if predicted_score >= 60:
                    result_color = "#2ECC71"
                    if use_chinese:
                        result_text = f"🎉 预测期末成绩: {predicted_score} 分"
                        message = "恭喜你！预测结果显示你会及格！"
                    else:
                        result_text = f"🎉 Predicted Final Score: {predicted_score}"
                        message = "Congratulations! The prediction shows you will pass!"
                    # 从GitHub加载通过图片
                    result_image = load_image_from_github("通过.png", message)
                else:
                    result_color = "#FF6B6B"
                    if use_chinese:
                        result_text = f"💡 预测期末成绩: {predicted_score} 分"
                        message = "加油！还有提升空间，继续努力！"
                    else:
                        result_text = f"💡 Predicted Final Score: {predicted_score}"
                        message = "Keep working! There's room for improvement, keep trying!"
                    # 从GitHub加载加油图片
                    result_image = load_image_from_github("加油.png", message)
                
                # 显示条幅
                st.markdown(f"""
                <div style="background-color: {result_color}; color: white; padding: 15px; border-radius: 8px; margin: 10px 0;">
                    <h3 style="margin: 0;">{result_text}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # 如果加载GitHub图片失败，使用默认图片
                if result_image is None:
                    result_img = create_result_image(predicted_score >= 60)
                    st.image(result_img, caption=message, use_container_width=True)
                
                # 学习建议
                if use_chinese:
                    st.subheader("📝 学习建议")
                else:
                    st.subheader("📝 Study Recommendations")
                
                if predicted_score < 60:
                    if use_chinese:
                        st.warning("⚠️ 建议增加学习时间，提高出勤率和作业完成度")
                        st.markdown("""
                        - 每周增加5-8小时学习时间
                        - 确保出勤率达到85%以上
                        - 完成所有作业并额外练习
                        """)
                    else:
                        st.warning("⚠️ Consider increasing study time and improving attendance and homework completion")
                        st.markdown("""
                        - Increase study time by 5-8 hours per week
                        - Ensure attendance rate is above 85%
                        - Complete all homework and do additional practice
                        """)
                elif predicted_score < 80:
                    if use_chinese:
                        st.info("✏️ 保持良好学习习惯，加强薄弱环节训练")
                        st.markdown("""
                        - 针对期中考试薄弱科目重点复习
                        - 参与学习小组互相讨论
                        - 定期向老师请教疑难问题
                        """)
                    else:
                        st.info("✏️ Maintain good study habits and focus on weak areas")
                        st.markdown("""
                        - Focus on subjects where midterm scores were low
                        - Join study groups for discussion
                        - Regularly consult teachers for difficult problems
                        """)
                else:
                    if use_chinese:
                        st.success("🌟 优秀！继续保持并尝试挑战更高难度的学习内容")
                        st.markdown("""
                        - 参与学科竞赛或项目实践
                        - 帮助其他同学巩固知识
                        - 预习高阶课程内容
                        """)
                    else:
                        st.success("🌟 Excellent! Keep it up and try challenging advanced content")
                        st.markdown("""
                        - Participate in subject competitions or projects
                        - Help classmates consolidate knowledge
                        - Preview advanced course content
                        """)
                
                # 影响因素分析
                if use_chinese:
                    st.subheader("🔍 成绩影响因素参考")
                else:
                    st.subheader("🔍 Key Factors Affecting Performance")
                
                factors = {
                    "学习时长": f"{study_hours} 小时/周",
                    "出勤率": f"{attendance_rate:.1%}",
                    "期中成绩": f"{midterm_score} 分",
                    "作业完成率": f"{homework_completion_rate:.1%}"
                } if use_chinese else {
                    "Study Hours": f"{study_hours} hrs/week",
                    "Attendance Rate": f"{attendance_rate:.1%}",
                    "Midterm Score": f"{midterm_score} points",
                    "Homework Completion": f"{homework_completion_rate:.1%}"
                }
                
                for factor, value in factors.items():
                    st.markdown(f"- **{factor}**: {value}")
                
                # 额外提示
                if use_chinese:
                    st.info("💡 提示：此预测基于历史数据训练的模型，实际成绩可能受多种因素影响。")
                else:
                    st.info("💡 Note: This prediction is based on a model trained on historical data. Actual scores may be affected by various factors.")

            except Exception as e:
                st.error(f"预测时出错: {str(e)}" if use_chinese else f"Error during prediction: {str(e)}")
                st.exception(e)  # 显示完整异常信息

if __name__ == "__main__":
    main()

