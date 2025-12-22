import streamlit as st

# 设置网页标题为“动物相册网站”
st.set_page_config(page_title="动物相册网站", page_icon="🐾")

# 你的动物图片列表（包含图片链接和描述）
image_ua = [
    {
        'url': 'https://cdn.britannica.com/73/9173-050-9D9EA4BA.jpg',
        'text': '鱼'
    },
    {
        'url': 'https://pic.nximg.cn/20131205/3822951_151249097000_2.jpg',
        'text': '鸟'
    },
    {
        'url': 'https://www.baltana.com/files/wallpapers-2/Cute-Cat-Images-07756.jpg',
        'text': '猫'
    }
]

# 初始化会话状态，记录当前图片索引
if 'ind' not in st.session_state:
    st.session_state['ind'] = 0

# 页面标题
st.title("动物相册网站")

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
