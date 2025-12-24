import streamlit as st
from PIL import Image

# 设置页面配置
st.set_page_config(page_title="个人简历生成器", layout="wide")

# 标题
st.title("📄 个人简历生成器")

# 初始化session_state
if 'name' not in st.session_state:
    st.session_state.name = ""
if 'position' not in st.session_state:
    st.session_state.position = ""
if 'phone' not in st.session_state:
    st.session_state.phone = ""
if 'email' not in st.session_state:
    st.session_state.email = ""
if 'personal_intro' not in st.session_state:
    st.session_state.personal_intro = ""
if 'skills' not in st.session_state:
    st.session_state.skills = []
if 'salary_range' not in st.session_state:
    st.session_state.salary_range = (0, 0)
if 'gender' not in st.session_state:
    st.session_state.gender = ""

# 创建两列布局
col1, col2 = st.columns([1, 2])

# 左侧表单区域
with col1:
    st.subheader("📝 个人信息表单")
    
    st.session_state.name = st.text_input("姓名")
    
    # 职位输入框，右侧添加说明
    col_pos1, col_pos2 = st.columns([3, 1])
    with col_pos1:
        st.session_state.position = st.text_input("职位")
    with col_pos2:
        st.markdown("<small style='color: gray;'>职位</small>", unsafe_allow_html=True)
    
    # 添加性别选择
    st.session_state.gender = st.radio("性别", ["", "男", "女", "其他"], index=0)
    
    st.session_state.phone = st.text_input("电话")
    st.session_state.email = st.text_input("邮箱")
    
    education = st.selectbox("学历", ["", "专科", "本科", "硕士", "博士"])
    
    st.session_state.skills = st.multiselect(
        "技能（可多选）",
        ["Java", "HTML/CSS", "机器学习", "Python", "JavaScript", "数据库", "云计算", "数据分析", "人工智能", "网络安全"]
    )
    
    work_experience = st.slider("工作经验（年）", 0, 30, 0)
    
    # 薪资范围滑块
    st.session_state.salary_range = st.slider(
        "期望薪资范围（元/月）",
        0, 100000, (5000, 20000),
        step=1000,
        format="%d元"
    )
    
    st.session_state.personal_intro = st.text_area("个人简介", height=150)
    
    uploaded_file = st.file_uploader("上传个人照片", type=["jpg", "jpeg", "png"])

# 右侧预览区域
with col2:
    st.subheader("👀 简历预览")
    
    if st.session_state.name:
        st.header(st.session_state.name)
    else:
        st.header("姓名")
    
    # 显示职位和性别
    if st.session_state.position and st.session_state.gender:
        st.subheader(f"{st.session_state.position} | {st.session_state.gender}")
    elif st.session_state.position:
        st.subheader(st.session_state.position)
    elif st.session_state.gender:
        st.subheader(st.session_state.gender)
    else:
        st.subheader("职位")
    
    # 显示上传的照片
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, width=150)
    
    # 联系信息
    st.markdown("### 联系方式")
    contact_info = []
    if st.session_state.phone:
        contact_info.append(f"📱 电话: {st.session_state.phone}")
    if st.session_state.email:
        contact_info.append(f"📧 邮箱: {st.session_state.email}")
    if education:
        contact_info.append(f"🎓 学历: {education}")
    if work_experience > 0:
        contact_info.append(f"💼 工作经验: {work_experience} 年")
    if st.session_state.salary_range[0] > 0 or st.session_state.salary_range[1] > 0:
        contact_info.append(f"💰 期望薪资: {st.session_state.salary_range[0]} - {st.session_state.salary_range[1]} 元/月")
    
    for info in contact_info:
        st.write(info)
    
    # 专业技能
    if st.session_state.skills:
        st.markdown("### 专业技能")
        for skill in st.session_state.skills:
            st.write(f"- {skill}")
    
    # 个人简介
    if st.session_state.personal_intro:
        st.markdown("### 个人简介")
        st.write(st.session_state.personal_intro)

# 页脚提示
st.markdown("---")
st.caption("提示：在左侧表单中填写您的信息，右侧将实时显示简历预览")
