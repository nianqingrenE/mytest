import streamlit as st

# 初始化歌曲列表
if 'current_song_index' not in st.session_state:
    st.session_state.current_song_index = 0

# 三首歌曲信息
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
        "duration": "4:00",
        "cover_url": "https://p2.music.126.net/r1AKMenByofI7Qqj3E5EqQ==/109951172091080013.jpg?param=200y200",
        "audio_url": "https://music.163.com/song/media/outer/url?id=2750712892.mp3"
    },
    {
        "title": "春天的临终",
        "artist": "裘德",
        "duration": "4:42",
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
    
    /* 白色文字 */
    .stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp span, .stApp div {
        color: white !important;
    }
    
    /* 按钮样式 - 灰色矩形 */
    .stButton > button {
        color: black !important;
        background-color: #cccccc !important;
        border: 1px solid #999999 !important;
        border-radius: 4px !important;
        font-weight: bold !important;
        padding: 8px 16px !important;
    }
    
    .stButton > button:hover {
        background-color: #dddddd !important;
        border-color: #aaaaaa !important;
    }
    
    /* 标题样式 */
    h1, h2, h3 {
        color: white !important;
        text-align: left !important;
    }
    
    /* 列间距 */
    .stColumn {
        padding: 10px;
    }
    
    /* 歌曲信息样式 */
    .song-info {
        margin-top: 20px;
        line-height: 1.8;
    }
    
    .song-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .song-details {
        font-size: 16px;
        color: #cccccc;
    }
</style>
""", unsafe_allow_html=True)

# 标题区域
st.markdown("# 🎵 简易音乐播放器")
st.markdown("使用Streamlit制作的简单音乐播放器，支持切歌和基本播放控制")
st.divider()

# 主播放器布局 - 左侧专辑封面，右侧信息和按钮
col_left, col_right = st.columns([1, 2])

# 左侧列 - 专辑封面
with col_left:
    st.markdown("**专辑封面**")
    st.image(current_song["cover_url"], width=280)

# 右侧列 - 歌曲信息和按钮
with col_right:
    # 歌曲标题
    st.markdown(f'<div class="song-title">{current_song["title"]}</div>', unsafe_allow_html=True)
    
    # 歌手和时长信息
    st.markdown(f'<div class="song-details">歌手: {current_song["artist"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="song-details">时长: {current_song["duration"]}</div>', unsafe_allow_html=True)
    
    # 在时长信息下面添加垂直间距
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # 按钮布局 - 放在时长信息下面的空位
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("◀◀ 上一首", use_container_width=True, key="prev_btn"):
            play_previous()
    with btn_col2:
        if st.button("▶▶ 下一首", use_container_width=True, key="next_btn"):
            play_next()

# 音频播放器和进度信息
st.divider()
st.audio(current_song["audio_url"], format="audio/mp3")

# 底部信息 - 当前播放状态
st.markdown(f"<p style='text-align: center; color: #888; font-size: 14px; margin-top: 15px;'>当前播放: {current_song['title']} - {current_song['artist']}</p>", unsafe_allow_html=True)
