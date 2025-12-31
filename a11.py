import streamlit as st
import pickle
import pandas as pd
import os
from pathlib import Path

# 设置基准目录（更可靠的路径处理）
BASE_DIR = Path(__file__).parent
IMAGE_DIR = BASE_DIR / "images"
MODEL_DIR = BASE_DIR

# 确保目录存在
os.makedirs(IMAGE_DIR, exist_ok=True)

# 设置页面
st.set_page_config(
    page_title="企鹅分类器",
    page_icon=":penguin:",
    layout='wide'
)

# 读取 CSV（处理编码）
penguins_df = None
csv_path = MODEL_DIR / "penguins-chinese.csv"
try:
    penguins_df = pd.read_csv(csv_path, encoding='utf-8')
except UnicodeDecodeError:
    try:
        penguins_df = pd.read_csv(csv_path, encoding='gbk')
    except Exception as e:
        st.error(f"无法读取数据文件: {str(e)}")
        st.stop()  # 停止执行

# 侧边栏
with st.sidebar:
    logo_path = IMAGE_DIR / "rigth_logo.png"
    if logo_path.exists():
        st.image(str(logo_path), width=100)
    else:
        st.info("提示：将logo图片放在images/rigth_logo.png")

    st.title('请选择页面')
    page = st.selectbox(
        "请选择页面",
        ["简介页面", "预测分类页面"],
        label_visibility='collapsed'
    )

if page == "简介页面":
    st.title("企鹅分类器 🐧")
    st.header('数据集介绍')
    st.markdown("""帕尔默群岛企鹅数据集是用于数据探索和数据可视化的一个出色的数据集，
也可以作为机器学习入门练习。
该数据集是由Gorman等收集，并发布在一个名为palmerpenguins的R语言包，
以对南极企鹅种类进行分类和研究。
该数据集记录了344行观测数据，包含3个不同物种的企鹅：阿德利企鹅、巴布亚企鹅和帽带企鹅的各种信息。""")

    if penguins_df is not None:
        st.subheader("数据集样例")
        st.dataframe(penguins_df.head())

    penguins_path = IMAGE_DIR / "penguins.png"
    if penguins_path.exists():
        st.image(str(penguins_path))
    else:
        st.info("提示：将企鹅图片放在images/penguins.png")

elif page == "预测分类页面":
    st.header("预测企鹅分类")
    st.markdown("这个Web应用是基于帕尔默群岛企鹅数据集构建的模型。只需输入6个信息，就可以预测企鹅的物种，使用下面的表单开始预测吧！")

    col1, col2, col3 = st.columns([3, 1, 2])
    with col1:
        with st.form('user_inputs'):
            island = st.selectbox('企鹅栖息的岛屿', options=['托尔森岛', '比斯科群岛', '德里姆岛'])
            sex = st.selectbox('性别', options=['雄性', '雌性'])
            bill_length = st.number_input('喙的长度（毫米）', min_value=0.0, value=40.0)
            bill_depth = st.number_input('喙的深度（毫米）', min_value=0.0, value=18.0)
            flipper_length = st.number_input('翅膀的长度（毫米）', min_value=0.0, value=200.0)
            body_mass = st.number_input('身体质量（克）', min_value=0.0, value=4000.0)
            submitted = st.form_submit_button('预测分类')

    # 数据预处理
    island_encoded = {'托尔森岛': [0, 0, 1], '比斯科群岛': [0, 1, 0], '德里姆岛': [1, 0, 0]}
    sex_encoded = {'雄性': [1, 0], '雌性': [0, 1]}
    
    island_dream, island_torgerson, island_biscoe = island_encoded[island]
    sex_male, sex_female = sex_encoded[sex]

    format_data = [
        bill_length, bill_depth, flipper_length, body_mass,
        island_dream, island_torgerson, island_biscoe, sex_male, sex_female
    ]

    # 加载模型
    rfc_model = None
    output_uniques_map = None
    model_path = MODEL_DIR / "rfc_model.pkl"
    mapping_path = MODEL_DIR / "output_uniques.pkl"
    
    if not model_path.exists():
        st.error("❌ 模型文件不存在！请先运行训练脚本生成模型")
        st.stop()
    
    try:
        with open(model_path, 'rb') as f:
            rfc_model = pickle.load(f)
        with open(mapping_path, 'rb') as f:
            output_uniques = pickle.load(f)
            output_uniques_map = {i: name for i, name in enumerate(output_uniques)}
    except ModuleNotFoundError as e:
        st.error(f"缺少必要的Python库: {str(e)}")
        st.info("请安装依赖: pip install scikit-learn pandas")
        st.stop()
    except Exception as e:
        st.error(f"加载模型失败: {str(e)}")
        st.stop()

    predict_result_species = None
    if submitted and rfc_model is not None:
        # 创建DataFrame时使用模型期望的特征名
        feature_names = rfc_model.feature_names_in_ if hasattr(rfc_model, 'feature_names_in_') else [
            'bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g',
            'island_Dream', 'island_Torgersen', 'island_Biscoe', 'sex_male', 'sex_female'
        ]
        format_data_df = pd.DataFrame([format_data], columns=feature_names)
        predict_result_code = rfc_model.predict(format_data_df)
        predict_result_species = output_uniques_map[int(predict_result_code[0])]
        st.success(f'## 预测结果: {predict_result_species}企鹅 🐧')
        st.balloons()

    # 右侧图片
    with col3:
        st.markdown("### 企鹅物种参考")
        if predict_result_species:
            species_img_path = IMAGE_DIR / f"{predict_result_species}.png"
            if species_img_path.exists():
                st.image(str(species_img_path), width=300)
            else:
                st.warning(f"缺少物种图片: {species_img_path.name}")
                # 显示默认图片
                default_img = IMAGE_DIR / "default_penguin.png"
                if default_img.exists():
                    st.image(str(default_img), width=300)
        else:
            logo_path = IMAGE_DIR / "rigth_logo.png"
            if logo_path.exists():
                st.image(str(logo_path), width=300)
            else:
                st.info("请上传参考图片到images目录")
