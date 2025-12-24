import streamlit as st

# 设置网页标题为“音乐”
st.set_page_config(page_title="音乐", page_icon="🐾")

# 你的动物图片列表（包含图片链接和描述）
image_ua = [
    {
        'audio_file = 'https://music.163.com/song/media/outer/url?id=188204.mp3'',
        'text': '沉默是金'
    },
    {
        'audio_file = 'https://music.163.com/song/media/outer/url?id=65766.mp3'',
        'text': '富士山下'
    },
    {
        'audio_file = 'https://music.163.com/song/media/outer/url?id=115502.mp3'',
        'text': '红日'
    }
]

# 初始化会话状态，记录当前图片索引
if 'ind' not in st.session_state:
    st.session_state['ind'] = 0

# 页面标题
st.title("音乐")

# 显示当前图片和描述
current_img = image_ua[st.session_state['ind']]
st.image(current_img['url'], caption=current_img['text'], use_column_width=True)

# 定义“上一张”功能
def prevImg():
    st.session_state['ind'] = (st.session_state['ind'] - 1) % len(image_ua)

# 定义“下一张”功能
def nextImg():
    st.session_state['ind'] = (st.session_state['ind'] + 1) % len(image_ua)

# 按钮区域
col1, col2 = st.columns(2)
with col1:
    st.button('上一张', use_container_width=True, on_click=prevImg)
with col2:
    st.button('下一张', use_container_width=True, on_click=nextImg)


