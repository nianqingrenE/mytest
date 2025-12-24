import streamlit as st
import time
import base64
from io import BytesIO

# 设置页面配置
st.set_page_config(
    page_title="简易音乐播放器",
    page_icon="🎵",
    layout="centered"
)

# 应用标题
st.title("简易音乐播放器")
st.markdown("使用Streamlit制作的简单音乐播放器，支持切歌和基本播放控制")

# 歌曲数据
songs = [
    {
        "id": 1,
        "title": "Bohemian Rhapsody",
        "artist": "Queen",
        "duration": "5:55",
        "album_cover": "https://upload.wikimedia.org/wikipedia/en/4/4d/Bohemian_Rhapsody.png"
    },
    {
        "id": 2,
        "title": "Hotel California",
        "artist": "Eagles",
        "duration": "6:30",
        "album_cover": "https://upload.wikimedia.org/wikipedia/en/4/49/Hotelcalifornia.jpg"
    },
    {
        "id": 3,
        "title": "Imagine",
        "artist": "John Lennon",
        "duration": "3:01",
        "album_cover": "https://upload.wikimedia.org/wikipedia/en/4/45/Imagine_cover.jpg"
    }
]

# 初始化session state
if 'current_song_index' not in st.session_state:
    st.session_state.current_song_index = 0
if 'is_playing' not in st.session_state:
    st.session_state.is_playing = False
if 'progress' not in st.session_state:
    st.session_state.progress = 0
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()

# 获取当前歌曲
def get_current_song():
    return songs[st.session_state.current_song_index]

# 切换歌曲
def play_next():
    st.session_state.current_song_index = (st.session_state.current_song_index + 1) % len(songs)
    st.session_state.progress = 0
    st.session_state.is_playing = True
    st.session_state.last_update = time.time()
    st.rerun()

def play_previous():
    st.session_state.current_song_index = (st.session_state.current_song_index - 1) % len(songs)
    st.session_state.progress = 0
    st.session_state.is_playing = True
    st.session_state.last_update = time.time()
    st.rerun()

def toggle_play():
    st.session_state.is_playing = not st.session_state.is_playing
    st.session_state.last_update = time.time()
    st.rerun()

# 模拟播放进度
if st.session_state.is_playing:
    current_time = time.time()
    time_diff = current_time - st.session_state.last_update
    
    # 每0.5秒更新一次进度
    if time_diff > 0.5:
        song_duration = 355  # 假设歌曲时长为355秒（5:55）
        st.session_state.progress += (time_diff / song_duration) * 100
        
        if st.session_state.progress >= 100:
            st.session_state.progress = 0
            # 自动播放下一首
            play_next()
        
        st.session_state.last_update = current_time
        st.rerun()

# 主播放器界面
st.divider()

current_song = get_current_song()

# 创建两列布局
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 专辑封面")
    st.image(current_song["album_cover"], width=200)

with col2:
    st.markdown(f"### {current_song['title']}")
    st.markdown(f"**歌手：** {current_song['artist']}")
    st.markdown(f"**时长：** {current_song['duration']}")

# 播放控制按钮
st.divider()

# 创建按钮列
col1, col2, col3 = st.columns([1, 1, 1], gap="large")

with col1:
    if st.button("⏮️ 上一首", use_container_width=True):
        play_previous()

with col2:
    play_pause_text = "⏸️ 暂停" if st.session_state.is_playing else "▶️ 播放"
    if st.button(play_pause_text, use_container_width=True, type="primary"):
        toggle_play()

with col3:
    if st.button("⏭️ 下一首", use_container_width=True):
        play_next()

# 播放进度条
st.divider()
progress_bar = st.progress(int(st.session_state.progress))
st.caption(f"播放进度: {int(st.session_state.progress)}%")

# 歌曲列表
st.divider()
st.markdown("### 歌曲列表")
for i, song in enumerate(songs):
    col1, col2, col3 = st.columns([4, 3, 2])
    with col1:
        if st.button(f"{song['title']}", key=f"select_{i}", use_container_width=True):
            st.session_state.current_song_index = i
            st.session_state.progress = 0
            st.session_state.is_playing = True
            st.session_state.last_update = time.time()
            st.rerun()
    with col2:
        st.write(f"歌手: {song['artist']}")
    with col3:
        st.write(f"时长: {song['duration']}")

# 功能说明区域
st.divider()
st.markdown("### 音乐播放器功能说明：")
st.markdown("""
1. **播放/暂停**：点击中间的播放/暂停按钮控制音乐播放
2. **切歌功能**：使用左右箭头按钮切换上一首/下一首
3. **歌曲列表**：从列表中选择任意歌曲播放
""")

st.divider()
st.markdown("### 课堂练习任务：")
st.markdown("""
1. 实现基本的播放控制功能 ✓
2. 添加专辑封面显示 ✓
3. 实现切歌功能（上一首/下一首） ✓
4. 显示歌曲基本信息（标题、歌手、时长） ✓
""")

st.markdown("### 扩展练习（可选）：")
st.markdown("""
1. 添加随机播放功能
2. 实现音量控制
3. 添加播放进度显示 ✓
""")

st.divider()
st.caption("Streamlit音乐播放器 | 课堂练习示例 | 使用Python和Streamlit构建")
