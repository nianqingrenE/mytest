import streamlit as st

# 设置网页标题（网站名称）
st.set_page_config(page_title="相册网站", page_icon="🖼️")

# 图片列表（可替换为本地图片路径或自定义图片链接）
image_list = [
    "https://picsum.photos/seed/album1/600/400",  # 示例图1
    "https://picsum.photos/seed/album2/600/400",  # 示例图2
    "https://picsum.photos/seed/album3/600/400",  # 示例图3
    "https://picsum.photos/seed/album4/600/400"   # 示例图4（可按需增减）
]

# 初始化会话状态，记录当前显示的图片索引
if "current_idx" not in st.session_state:
    st.session_state.current_idx = 0

# 显示网页标题（页面内可见）
st.title("相册网站")

# 显示当前图片
st.image(
    image_list[st.session_state.current_idx],
    caption=f"图片 {st.session_state.current_idx + 1}/{len(image_list)}"  # 显示图片序号
)

# 按钮区域：上一张 + 下一张（横向排列）
col1, col2 = st.columns(2)
with col1:
    if st.button("上一张"):
        # 循环切换：第一张的上一张是最后一张
        st.session_state.current_idx = (st.session_state.current_idx - 1) % len(image_list)
with col2:
    if st.button("下一张"):
        # 循环切换：最后一张的下一张是第一张
        st.session_state.current_idx = (st.session_state.current_idx + 1) % len(image_list)
