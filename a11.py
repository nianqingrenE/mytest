import streamlit as st
import pickle
import pandas as pd
import os

# 设置页面
st.set_page_config(
    page_title="企鹅分类器",
    page_icon=":penguin:",
    layout='wide'
)

# 图片文件夹路径
IMAGE_DIR = r"D:\streamlit_env\images"

# 模型文件夹路径
MODEL_DIR = r"D:\streamlit_env"

# 读取 CSV（处理编码）
penguins_df = None
try:
    penguins_df = pd.read_csv(os.path.join(MODEL_DIR, "penguins-chinese.csv"), encoding='gbk')
except:
    try:
        penguins_df = pd.read_csv(os.path.join(MODEL_DIR, "penguins-chinese.csv"), encoding='gb2312')
    except:
        st.error("无法读取 penguins-chinese.csv 文件")

# 侧边栏
with st.sidebar:
    logo_path = os.path.join(IMAGE_DIR, "rigth_logo.png")
    if os.path.exists(logo_path):
        st.image(logo_path, width=100)
    else:
        st.warning(f"找不到图片: {logo_path}")

    st.title('请选择页面')
    page = st.selectbox(
        "请选择页面",
        ["简介页面", "预测分类页面"],
        label_visibility='collapsed'
    )

if page == "简介页面":
    st.title("企鹅分类器:penguin:")
    st.header('数据集介绍')
    st.markdown("""帕尔默群岛企鹅数据集是用于数据探索和数据可视化的一个出色的数据集，
也可以作为机器学习入门练习。
该数据集是由Gorman等收集，并发布在一个名为palmerpenguins的R语言包，
以对南极企鹅种类进行分类和研究。
该数据集记录了344行观测数据，包含3个不同物种的企鹅：阿德利企鹅、巴布亚企鹅和帽带企鹅的各种信息。""")

    if penguins_df is not None:
        st.subheader("数据集样例")
        st.dataframe(penguins_df.head())

    penguins_path = os.path.join(IMAGE_DIR, "penguins.png")
    if os.path.exists(penguins_path):
        st.image(penguins_path)
    else:
        st.warning(f"找不到图片: {penguins_path}")

elif page == "预测分类页面":
    st.header("预测企鹅分类")
    st.markdown("这个Web应用是基于帕尔默群岛企鹅数据集构建的模型。只需输入6个信息，就可以预测企鹅的物种，使用下面的表单开始预测吧！")

    col1, col2, col3 = st.columns([3, 1, 2])
    with col1:
        with st.form('user_inputs'):
            island = st.selectbox('企鹅栖息的岛屿', options=['托尔森岛', '比斯科群岛', '德里姆岛'])
            sex = st.selectbox('性别', options=['雄性', '雌性'])
            bill_length = st.number_input('喙的长度（毫米）', min_value=0.0)
            bill_depth = st.number_input('喙的深度（毫米）', min_value=0.0)
            flipper_length = st.number_input('翅膀的长度（毫米）', min_value=0.0)
            body_mass = st.number_input('身体质量（克）', min_value=0.0)
            submitted = st.form_submit_button('预测分类')

    # 数据预处理
    island_biscoe, island_dream, island_torgerson = 0, 0, 0
    if island == '比斯科群岛':
        island_biscoe = 1
    elif island == '德里姆岛':
        island_dream = 1
    elif island == '托尔森岛':
        island_torgerson = 1

    sex_female, sex_male = 0, 0
    if sex == '雌性':
        sex_female = 1
    elif sex == '雄性':
        sex_male = 1

    format_data = [
        bill_length, bill_depth, flipper_length, body_mass,
        island_dream, island_torgerson, island_biscoe, sex_male, sex_female
    ]

    # 加载模型
    rfc_model = None
    output_uniques_map = None
    try:
        with open(os.path.join(MODEL_DIR, "rfc_model.pkl"), 'rb') as f:
            rfc_model = pickle.load(f)
        with open(os.path.join(MODEL_DIR, "output_uniques.pkl"), 'rb') as f:
            output_uniques = pickle.load(f)
            output_uniques_map = {i: name for i, name in enumerate(output_uniques)}
    except FileNotFoundError:
        st.error("模型文件不存在，请先运行 save_model.py 生成 rfc_model.pkl 和 output_uniques.pkl")
    except Exception as e:
        st.error(f"加载模型失败: {str(e)}")

    predict_result_species = None
    if submitted and rfc_model is not None:
        format_data_df = pd.DataFrame([format_data], columns=rfc_model.feature_names_in_)
        predict_result_code = rfc_model.predict(format_data_df)
        predict_result_species = output_uniques_map[predict_result_code[0]]
        st.write(f'根据您输入的数据，预测该企鹅的物种名称是：**{predict_result_species}**')

    # 右侧图片
    with col3:
        if submitted and predict_result_species:
            species_img_path = os.path.join(IMAGE_DIR, f"{predict_result_species}.png")
            if os.path.exists(species_img_path):
                st.image(species_img_path, width=300)
            else:
                st.warning(f"找不到物种图片: {species_img_path}")
        else:
            logo_path = os.path.join(IMAGE_DIR, "rigth_logo.png")
            if os.path.exists(logo_path):
                st.image(logo_path, width=300)
            else:
                st.warning(f"找不到图片: {logo_path}")
