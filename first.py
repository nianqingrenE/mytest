import streamlit as st

# 图片列表（这里用示例图链接，也可以替换为本地图片路径）
image_list = [
    "https://picsum.photos/seed/cat1/400/300",  # 示例图1
    "https://picsum.photos/seed/dog1/400/300",  # 示例图2
    "https://picsum.photos/seed/bird1/400/300"  # 示例图3
]

# 初始化会话状态，记录当前显示的图片索引
if "current_idx" not in st.session_state:
    st.session_state.current_idx = 0

# 显示当前图片
st.image(image_list[st.session_state.current_idx])

# 按钮区域：上一张 + 下一张
col1, col2 = st.columns(2)
with col1:
    if st.button("上一张"):
        st.session_state.current_idx = (st.session_state.current_idx - 1) % len(image_list)
with col2:
    if st.button("下一张"):
        st.session_state.current_idx = (st.session_state.current_idx + 1) % len(image_list)
