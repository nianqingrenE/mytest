import streamlit as st

# 初始化歌曲列表
if 'current_song_index' not in st.session_state:
    st.session_state.current_song_index = 0

# 三首歌曲信息
songs = [
    {
        "title": "Bohemian Rhapsody",
        "artist": "Queen",
        "duration": "5:55",
        "cover_url": "https://upload.wikimedia.org/wikipedia/en/4/4d/Bohemian_Rhapsody.png",
        "audio_url": "你的歌曲1路径"  # 请替换为你的歌曲路径
    },
    {
        "title": "Hotel California",
        "artist": "Eagles", 
        "duration": "6:30",
        "cover_url": "https://upload.wikimedia.org/wikipedia/en/4/49/Hotelcalifornia.jpg",
        "audio_url": "你的歌曲2路径"  # 请替换为你的歌曲路径
    },
    {
        "title": "Imagine",
        "artist": "John Lennon",
        "duration": "3:01",
        "cover_url": "https://upload.wikimedia.org/wikipedia/en/4/45/Imagine_cover.jpg",
        "audio_url": "你的歌曲3路径"  # 请替换为你的歌曲路径
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
col1, col2 = st.columns([1, 1])

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
