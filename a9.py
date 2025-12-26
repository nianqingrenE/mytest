import streamlit as st
import pandas as pd
from PIL import Image

# ======================
# 主页面配置（背景改为白色）
# ======================
st.set_page_config(
    page_title="广西职业师范学院应用",
    layout="wide",
    initial_sidebar_state="collapsed"  # 收起侧边栏（可选）
)

# 自定义白色背景样式
st.markdown("""
    <style>
    .stApp {
        background-color: #FFFFFF;
        color: #000000;
    }
    .stHeader, .stToolbar {
        background-color: #FFFFFF !important;
    }
    .stDataFrame {
        color: #000000;
        background-color: #FFFFFF;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    .stMarkdown {
        color: #000000;
    }
    </style>
""", unsafe_allow_html=True)

# ======================
# 顶部导航栏
# ======================
# 定义页面标签
pages = [
    "学校介绍", 
    "个人简历生成器", 
    "动物图鉴", 
    "南宁美食数据", 
    "数字档案"
]

# 创建顶部导航标签页
selected_page = st.radio(
    "广西职业师范学院应用",
    pages,
    horizontal=True,
    label_visibility="collapsed"
)

# 在顶部导航下方添加一条分隔线
st.markdown("<hr>", unsafe_allow_html=True)

# ======================
# 各页面内容
# ======================

# 1. 学校介绍（主页）
if selected_page == "学校介绍":
    st.title("广西职业师范学院介绍")
    st.header("关于我们")
    
    st.markdown("""
    <div style='background-color: #F5F5F5; padding: 20px; border-radius: 8px;'>
    <h3>学院概况</h3>
    <p>广西职业师范学院是一所位于广西南宁的全日制普通本科院校，致力于培养高素质应用型人才。学校始建于1955年，前身为广西师范专科学校，2018年升格为本科院校。</p>
    
    <h3>办学特色</h3>
    <ul>
        <li>以职业教育为特色，注重实践能力培养</li>
        <li>拥有省级重点实验室5个</li>
        <li>校企合作单位300+家</li>
        <li>毕业生就业率连续5年超95%</li>
    </ul>
    
    <h3>校园环境</h3>
    <p>校园占地面积1200亩，环境优美，拥有现代化教学楼、图书馆、体育馆等设施。校园内绿树成荫，四季花香，是学习的理想场所。</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("校园风光")
    st.image("https://ts1.tc.mm.bing.net/th/id/R-C.71e70587ae5419531bf534fa66c39c51?rik=uizuOiYAArH1DA&riu=http%3a%2f%2fstatic-data.gaokao.cn%2fupload%2fsvideo%2f1611730557_9407_thumb.jpg&ehk=YlKROXwF1PlkdAC34aFiKYtJ%2fi0vOM%2fbCxpr5%2fxqfjI%3d&risl=&pid=ImgRaw&r=0", 
              caption="广西职业师范学院主校区", 
              use_column_width=True)
    st.caption("图：广西职业师范学院主校区全景")

# 2. 个人简历生成器
elif selected_page == "个人简历生成器":
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
        
        st.session_state.name = st.text_input("姓名", st.session_state.name)
        
        # 职位输入框
        col_pos1, col_pos2 = st.columns([3, 1])
        with col_pos1:
            st.session_state.position = st.text_input("职位", st.session_state.position)
        with col_pos2:
            st.markdown("<small style='color: #666666;'>职位</small>", unsafe_allow_html=True)
        
        # 性别选择
        st.session_state.gender = st.radio("性别", ["", "男", "女", "其他"], index=0)
        
        st.session_state.phone = st.text_input("电话", st.session_state.phone)
        st.session_state.email = st.text_input("邮箱", st.session_state.email)
        
        education = st.selectbox("学历", ["", "专科", "本科", "硕士", "博士"])
        
        st.session_state.skills = st.multiselect(
            "技能（可多选）",
            ["Java", "HTML/CSS", "机器学习", "Python", "JavaScript", "数据库", "云计算", "数据分析", "人工智能", "网络安全"],
            st.session_state.skills
        )
        
        work_experience = st.slider("工作经验（年）", 0, 30, 0)
        
        # 薪资范围滑块
        st.session_state.salary_range = st.slider(
            "期望薪资范围（元/月）",
            0, 100000, (5000, 20000),
            step=1000,
            format="%d元"
        )
        
        st.session_state.personal_intro = st.text_area("个人简介", height=150, value=st.session_state.personal_intro)
        
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

# 3. 动物图鉴
elif selected_page == "动物图鉴":
    st.title("🐾 动物相册网站")
    
    # 你的动物图片列表
    image_ua = [
        {
            'url': 'https://cdn.britannica.com/73/9173-050-9D9EA4BA.jpg',
            'text': '鱼'
        },
        {
            'url': 'https://img95.699pic.com/photo/60059/3325.jpg_wh300.jpg',
            'text': '鸟'
        },
        {
            'url': 'https://www.baltana.com/files/wallpapers-2/Cute-Cat-Images-07756.jpg',
            'text': '猫'
        }
    ]

    # 初始化会话状态
    if 'ind' not in st.session_state:
        st.session_state['ind'] = 0

    # 显示当前图片和描述
    current_img = image_ua[st.session_state['ind']]
    st.image(current_img['url'], caption=current_img['text'], use_column_width=True)

    # 按钮区域
    col1, col2 = st.columns(2)
    with col1:
        if st.button('上一张', use_container_width=True):
            st.session_state['ind'] = (st.session_state['ind'] - 1) % len(image_ua)
    with col2:
        if st.button('下一张', use_container_width=True):
            st.session_state['ind'] = (st.session_state['ind'] + 1) % len(image_ua)

# 4. 南宁美食数据
elif selected_page == "南宁美食数据":
    # 数据准备（保留原代码）
    shops = pd.DataFrame({
        "店铺名称": [
            "复记老友粉(中山路店)", 
            "舒记老友粉(七星路店)", 
            "爱民螺蛳粉(西大店)", 
            "桂小厨(万象城店)", 
            "粉之都(朝阳店)"
        ],
        "地址": [
            "青秀区中山路22号",
            "青秀区七星路123号",
            "西乡塘区大学东路100号",
            "青秀区民族大道136号万象城5楼",
            "兴宁区朝阳路38号"
        ],
        "纬度": [22.8156, 22.8102, 22.8375, 22.8086, 22.8168],
        "经度": [108.3307, 108.3245, 108.2841, 108.3515, 108.3228],
        "评分": [4.7, 4.6, 4.5, 4.8, 4.4],
        "好评率": ["95%", "93%", "90%", "96%", "88%"],
        "人均消费(元)": [15, 14, 12, 60, 10]
    })

    # 12个月价格走势数据
    months = list(range(1, 13))
    price_data = pd.DataFrame({
        "月份": months * 5,
        "店铺名称": [
            "复记老友粉"]*12 + ["舒记老友粉"]*12 + 
            ["爱民螺蛳粉"]*12 + ["桂小厨"]*12 + ["粉之都"]*12,
        "人均价格(元)": [
            # 复记老友粉
            15,15,16,16,17,17,17,18,18,19,19,20,
            # 舒记老友粉
            14,14,15,15,16,16,16,17,17,18,18,19,
            # 爱民螺蛳粉
            12,12,13,13,14,14,14,15,15,16,16,17,
            # 桂小厨
            60,62,63,65,68,70,70,72,75,78,80,82,
            # 粉之都
            10,10,11,11,12,12,12,13,13,14,14,15
        ]
    })
    price_wide = price_data.pivot(index="月份", columns="店铺名称", values="人均价格(元)")

    # 用餐高峰时段数据
    dining_data = pd.DataFrame({
        "时段(小时)": list(range(0, 24)),
        "复记老友粉(中山路店)": [5,8,10,12,15,20,30,45,60,55,40,35,45,50,65,70,60,50,40,30,20,15,10,8],
        "舒记老友粉(七星路店)": [4,7,9,11,14,18,28,40,55,50,38,32,42,48,60,65,58,48,38,28,18,14,9,7],
        "爱民螺蛳粉(西大店)": [3,6,8,10,13,17,25,35,50,45,35,30,40,45,55,60,55,45,35,25,17,13,8,6],
        "桂小厨(万象城店)": [2,3,5,8,12,20,35,50,70,80,90,85,95,100,110,105,95,80,60,40,25,15,10,5],
        "粉之都(朝阳店)": [6,9,12,15,18,22,30,40,50,45,38,32,42,48,55,60,55,45,35,25,18,14,10,7]
    })

    # 界面组件
    st.title("南宁美食数据仪表盘")

    # 1. 店铺分布地图
    st.subheader("📍 南宁美食店铺分布")
    st.map(
        shops, 
        latitude="纬度", 
        longitude="经度", 
        use_container_width=True
    )

    # 2. 餐厅评分柱状图
    st.subheader("⭐ 餐厅评分")
    st.bar_chart(shops.set_index("店铺名称")["评分"], color="#4CAF50", use_container_width=True)

    # 3. 12个月价格走势折线图
    st.subheader("📊 5家餐厅12个月价格走势")
    st.line_chart(
        price_wide,
        color=["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8"],
        use_container_width=True
    )

    # 4. 用餐高峰时段面积图
    st.subheader("⏰ 用餐高峰时段")
    st.area_chart(
        dining_data.set_index("时段(小时)"),
        color=["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8"],
        use_container_width=True
    )

    # 5. 餐厅详情
    st.subheader("📋 餐厅详情")
    st.dataframe(shops[["店铺名称", "地址", "评分", "好评率", "人均消费(元)"]], use_container_width=True)

    # 6. 今日午餐推荐
    st.subheader("🍲 今日午餐推荐")
    st.write("**复记老友粉(中山路店)** - 经典老友粉（酸辣鲜香，地道南宁味）")
    st.image(
        "https://tse1-mm.cn.bing.net/th/id/OIP-C.2m02I_TdBlKVoZTxWmGMTAHaFm?w=252&h=191&c=7&r=0&o=5&cb=ucfimg2&pid=1.7&ucfimg=1",
        caption="复记老友粉",
        use_column_width=True
    )

# 5. 数字档案
elif selected_page == "数字档案":
    st.title("电子病例系统使用人数流量统计")
    st.header("每年季度登入人数统计表📄")
    
    # 创建统计表格
    data = {
        '23年':[500,600,700,800],
        '24年':[600,700,800,900],
        '25年':[600,700,800,900],
    }
    index = pd.Series(['春季', '夏季', '秋季', '冬季'], name='季节')
    df = pd.DataFrame(data, index=index)
    
    st.write('下面是季度统计表', df)
    st.markdown('***')
    
    st.header("🩹基础信息🩹")
    st.text("🥼统计人：全小将")
    st.text("📞联系方式：666666")
    st.text("⏰统计时间：2025-12-18")
    st.text("📌统计项目：微信电子病例小程序系统")
    
    st.subheader('图表代码展示')
    python_code = '''data = {
    '23年':[500,600,700,800],
    '24年':[600,700,800,900],
    '25年':[600,700,800,900],
}
index = pd.Series(['春季', '夏季', '秋季', '冬季'], name='季节')
df = pd.DataFrame(data, index=index)
'''
    st.code(python_code, language='python', line_numbers=True)
    
    st.header("系统情况展示")
    st.subheader('使用情况')
    st.metric(label="今日使用人数", value="250", delta="28%")
    
    st.subheader('功能使用情况')
    c1, c2, c3 = st.columns(3)
    c1.metric(label="查看电子病例", value="100", delta="-11%")
    c2.metric(label="增加人数", value="100", delta="50%")
    c3.metric(label="康复人数", value="50", delta="20%")

# 页脚
st.markdown("---")
st.caption("广西职业师范学院 - 多功能应用平台 | 2025年12月")
