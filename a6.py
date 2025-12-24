import streamlit as st

# 设置页面标题（显示在浏览器标签页上）
st.set_page_config(page_title="视频中心")

# 定义视频列表，包含视频URL和标题
video_arr = [
    {
        'url': "https://www.w3school.com.cn/example/html5/mov_bbb.mp4",
        'title': "第一集"
    },
    {
        'url': "https://www.w3schools.com/html/movie.mp4",
        'title': "第二集"
    },
    {
        'url': "https://media.w3.org/2010/05/sintel/trailer.mp4",
        'title': "第三集"
    },
]

# 按钮点击事件处理函数
def playVideo(i):
    """切换到指定视频集数
    参数:
        i (int): 视频索引 (0, 1, 2...)
    """
    st.session_state['ind'] = i  # 更新当前播放的视频索引
    st.title(video_arr[i]['title'])  # 更新页面标题为当前视频标题

# 初始化会话状态（如果不存在ind变量）
if 'ind' not in st.session_state:
    st.session_state['ind'] = 0  # 默认播放第一集

# 显示当前播放的视频标题
st.title(video_arr[st.session_state['ind']]['title'])

# 显示当前视频播放器
st.video(video_arr[st.session_state['ind']]['url'])

# 创建水平排列的按钮栏（每个按钮占一列）
cols = st.columns(len(video_arr))

# 为每个视频集数创建按钮
for i, col in enumerate(cols):
    with col:
        st.button(
            f"第{i+1}集", 
            on_click=playVideo, 
            args=[i]
        )
