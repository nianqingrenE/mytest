import streamlit as st
import requests
from urllib.parse import quote

# 设置页面
st.set_page_config(
    page_title="网易云音乐播放器",
    page_icon="🎵",
    layout="centered"
)

st.title("🎵 网易云音乐播放器")
st.markdown("使用网易云音乐API的简易播放器")

# 歌曲数据库（歌曲名称和对应的ID）
songs = [
    {"id": "5257138", "name": "Counting Stars", "artist": "OneRepublic"},
    {"id": "186756", "name": "理想三旬", "artist": "陈鸿宇"},
    {"id": "1336856778", "name": "世间美好与你环环相扣", "artist": "柏松"},
    {"id": "1363948882", "name": "少年", "artist": "梦然"},
    {"id": "1387581880", "name": "星辰大海", "artist": "黄霄雲"}
]

# 初始化session state
if 'current_song_index' not in st.session_state:
    st.session_state.current_song_index = 0
if 'is_playing' not in st.session_state:
    st.session_state.is_playing = False

# 获取当前歌曲
def get_current_song():
    return songs[st.session_state.current_song_index]

# 构建音乐URL
def get_music_url(song_id):
    return f'https://music.163.com/song/media/outer/url?id={song_id}.mp3'

# 切换歌曲函数
def play_next():
    st.session_state.current_song_index = (st.session_state.current_song_index + 1) % len(songs)
    st.session_state.is_playing = True
    st.rerun()

def play_previous():
    st.session_state.current_song_index = (st.session_state.current_song_index - 1) % len(songs)
    st.session_state.is_playing = True
    st.rerun()

# 主界面
st.divider()

# 当前播放信息
current_song = get_current_song()
st.subheader("🎶 当前播放")
col1, col2 = st.columns([1, 2])
with col1:
    st.markdown(f"**歌曲:** {current_song['name']}")
with col2:
    st.markdown(f"**歌手:** {current_song['artist']}")

# 播放器
audio_url = get_music_url(current_song['id'])
st.audio(audio_url, format="audio/mp3")

# 播放控制按钮
st.divider()
st.subheader("播放控制")

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("⏮️ 上一首", use_container_width=True):
        play_previous()
with col2:
    play_pause_text = "⏸️ 暂停" if st.session_state.is_playing else "▶️ 播放"
    if st.button(play_pause_text, use_container_width=True, type="primary"):
        st.session_state.is_playing = not st.session_state.is_playing
        st.rerun()
with col3:
    if st.button("⏭️ 下一首", use_container_width=True):
        play_next()

# 歌曲列表
st.divider()
st.subheader("📋 歌曲列表")

for i, song in enumerate(songs):
    col1, col2, col3 = st.columns([3, 2, 1])
    with col1:
        # 高亮显示当前播放的歌曲
        if i == st.session_state.current_song_index:
            st.markdown(f"🎵 **{song['name']}**")
        else:
            st.write(song['name'])
    with col2:
        st.write(song['artist'])
    with col3:
        if st.button("播放", key=f"play_{i}", use_container_width=True):
            st.session_state.current_song_index = i
            st.session_state.is_playing = True
            st.rerun()

# 自定义歌曲ID播放
st.divider()
st.subheader("🔍 播放指定歌曲")

with st.expander("通过歌曲ID播放"):
    st.markdown("""
    **如何获取歌曲ID:**
    1. 在网易云音乐网页版找到想听的歌曲
    2. 在浏览器地址栏中可以看到类似 `https://music.163.com/song?id=5257138` 的链接
    3. 其中的数字 `5257138` 就是歌曲ID
    """)
    
    custom_song_id = st.text_input("输入网易云音乐歌曲ID:", placeholder="例如: 5257138")
    if st.button("播放自定义歌曲") and custom_song_id:
        try:
            # 验证ID是否为数字
            song_id = str(int(custom_song_id))
            custom_audio_url = get_music_url(song_id)
            st.audio(custom_audio_url, format="audio/mp3")
            st.success(f"已加载歌曲ID: {song_id}")
        except ValueError:
            st.error("请输入有效的数字ID")
