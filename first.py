import streamlit as st

# 初始化歌曲列表
if 'current_song_index' not in st.session_state:
    st.session_state.current_song_index = 0

# 三首歌曲信息
songs = [
    {
        "title": "恭喜发财",
        "artist": "mchaCheers",
        "duration": "5:55",
        "cover_url": "https://p1.music.126.net/qDDB6HshQrqwyKzE9778QA==/109951172450091661.jpg?param=130y130",
        "audio_url": "https://music.163.com/#/song?id=3329668871" 
    },
    {
        "title": "银色荒原",
        "artist": "裘德", 
        "duration": "4:00",
        "cover_url": "https://p2.music.126.net/r1AKMenByofI7Qqj3E5EqQ==/109951172091080013.jpg?param=130y130",
        "audio_url": "https://music.163.com/#/song?id=2750712892"  
    },
    {
        "title": "春天的临终",
        "artist": "裘德",
        "duration": "4:42",
        "cover_url": "https://p2.music.126.net/r1AKMenByofI7Qqj3E5EqQ==/109951172091080013.jpg?param=130y130",
        "audio_url": "https://music.163.com/#/song?id=2733730415" 
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

# 界面
st.markdown("""
<style>
    /* 黑色背景 */
    .stApp {
        background-color: #000000;
    }
    /* 白色文字 */
    .css-1d391kg, .stMarkdown, .stTitle, .stSubheader, p, div, h1, h2, h3, h4, h5, h6 {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# 标题
st.markdown("## 🎵 简易音乐播放器")
st.write("使用Streamlit制作的简单音乐播放器，支持切歌和基本播放控制")

# 分隔线
st.divider()

# 主内容区域
col1, col2 = st.columns([1, 2])

with col1:
    st.write("**专辑封面**")
    st.image(current_song["cover_url"], width=250)
    
    # 播放控制按钮
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("◀◀ 上一首", use_container_width=True):
            play_previous()
    with col_btn2:
        if st.button("▶▶ 下一首", use_container_width=True):
            play_next()

with col2:
    st.write(f"**{current_song['title']}**")
    st.write(f"**歌手:** {current_song['artist']}")
    st.write(f"**时长:** {current_song['duration']}")

# 音频播放器
st.divider()
st.audio(current_song["audio_url"], format="audio/mp3")

