import streamlit as st

# 初始化歌曲列表
if 'current_song_index' not in st.session_state:
    st.session_state.current_song_index = 0

# 三首歌曲信息 - 修正音频URL格式
songs = [
    {
        "title": "恭喜发财",
        "artist": "mchaCheers",
        "duration": "1:15", 
        "cover_url": "https://p1.music.126.net/qDDB6HshQrqwyKzE9778QA==/109951172450091661.jpg?param=200y200",
        "audio_url": "https://music.163.com/song/media/outer/url?id=3329668871.mp3"
    },
    {
        "title": "银色荒原", 
        "artist": "裘德",
        "duration": "4:00",  # 根据实际音频时长填写
        "cover_url": "https://p2.music.126.net/r1AKMenByofI7Qqj3E5EqQ==/109951172091080013.jpg?param=200y200",
        "audio_url": "https://music.163.com/song/media/outer/url?id=2750712892.mp3"
    },
    {
        "title": "春天的临终",
        "artist": "裘德",
        "duration": "4:42",  # 根据实际音频时长填写
        "cover_url": "https://p2.music.126.net/r1AKMenByofI7Qqj3E5EqQ==/109951172091080013.jpg?param=200y200",
        "audio_url": "https://music.163.com/song/media/outer/url?id=2733730415.mp3"
    }
]

# 切换歌曲函数
def play_previous():
    st.session_state.current_song_index = (st.session_state.current_song_index - 1) % len(songs)
    st.rerun()

def play_next():
    st.session_state.current_song_index = (st.session_state.current_song_index + 1) % len(songs)
    st.rerun()

# 获取当前歌曲
current_song = songs[st.session_state.current_song_index]

# 应用样式
st.markdown("""
<style>
    /* 黑色背景 */
    .stApp {
        background-color: #000000;
    }
    /* 白色文字 - 改进的选择器 */
    .stApp * {
        color: white !important;
    }
    
    /* 修正按钮文字颜色 */
    .stButton > button {
        color: black !important;
        border-color: white;
    }
    
    .stButton > button:hover {
        background-color: #333;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# 标题区域
st.markdown("## 🎵 简易音乐播放器")
st.markdown("使用Streamlit制作的简单音乐播放器，支持切歌和基本播放控制")
st.divider()

# 主播放器布局
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("**专辑封面**")
    st.image(current_song["cover_url"], width=250)
    
    # 播放控制按钮区域
    st.markdown("<br>", unsafe_allow_html=True)  # 添加一些垂直间距
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("◀◀ 上一首", use_container_width=True, type="secondary"):
            play_previous()
    with col_btn2:
        if st.button("▶▶ 下一首", use_container_width=True, type="secondary"):
            play_next()

with col2:
    st.markdown(f"<h3 style='margin-bottom: 20px;'>{current_song['title']}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p><strong>歌手:</strong> {current_song['artist']}</p>", unsafe_allow_html=True)
    st.markdown(f"<p><strong>时长:</strong> {current_song['duration']}</p>", unsafe_allow_html=True)

# 音频播放器
st.divider()
st.audio(current_song["audio_url"], format="audio/mp3")

# 显示当前播放歌曲的信息
st.markdown(f"<p style='font-size: 12px; color: #888; text-align: center;'>当前播放: {current_song['title']} - {current_song['artist']}</p>", unsafe_allow_html=True)
