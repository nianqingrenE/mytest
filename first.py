import streamlit as st
import time

# 设置页面配置
st.set_page_config(
    page_title="音乐播放器",
    page_icon="🎵",
    layout="centered"
)

# 歌曲数据
songs = [
    {
        "id": 1,
        "title": "Counting Stars",
        "artist": "OneRepublic",
        "url": "https://music.163.com/song/media/outer/url?id=5257138.mp3"
    },
    {
        "id": 2,
        "title": "理想三旬",
        "artist": "陈鸿宇", 
        "url": "https://music.163.com/song/media/outer/url?id=186756.mp3"
    },
    {
        "id": 3,
        "title": "起风了",
        "artist": "买辣椒也用券",
        "url": "https://music.163.com/song/media/outer/url?id=1330348068.mp3"
    }
]

# 初始化session state
if 'current_song_index' not in st.session_state:
    st.session_state.current_song_index = 0
if 'is_playing' not in st.session_state:
    st.session_state.is_playing = False

# 切换歌曲函数
def play_next():
    st.session_state.current_song_index = (st.session_state.current_song_index + 1) % len(songs)
    st.session_state.is_playing = True
    st.rerun()

def play_previous():
    st.session_state.current_song_index = (st.session_state.current_song_index - 1) % len(songs)
    st.session_state.is_playing = True
    st.rerun()

def toggle_play():
    st.session_state.is_playing = not st.session_state.is_playing
    st.rerun()

# 获取当前歌曲
def get_current_song():
    return songs[st.session_state.current_song_index]

# 界面布局
current_song = get_current_song()

# 页面标题
st.title("🎵 音乐播放器")

# 显示当前歌曲信息
st.subheader("当前播放:")
st.write(f"**歌曲:** {current_song['title']}")
st.write(f"**歌手:** {current_song['artist']}")
st.write(f"**编号:** {current_song['id']}")

# 显示分隔线
st.write("---")

# 显示播放状态
status_text = "▶️ 正在播放..." if st.session_state.is_playing else "⏸️ 已暂停"
st.write(f"**状态:** {status_text}")

# 添加音频播放器
st.audio(current_song['url'], format="audio/mp3")

# 播放控制按钮
st.write("---")
st.subheader("播放控制")

# 创建按钮行
col1, col2, col3 = st.columns(3)

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

# 歌曲列表
st.write("---")
st.subheader("歌曲列表")

for i, song in enumerate(songs):
    # 高亮显示当前歌曲
    if i == st.session_state.current_song_index:
        st.markdown(f"**🎵 {song['title']} - {song['artist']}**")
    else:
        st.write(f"{song['title']} - {song['artist']}")
    
    # 为每首歌添加播放按钮
    if st.button(f"播放此歌曲", key=f"play_{i}", use_container_width=True):
        st.session_state.current_song_index = i
        st.session_state.is_playing = True
        st.rerun()

# 自定义歌曲ID播放
st.write("---")
st.subheader("自定义播放")

# 获取歌曲ID
song_id = st.text_input("输入网易云音乐歌曲ID:", placeholder="例如: 5257138")

if song_id and song_id.isdigit():
    # 构建音频URL
    custom_url = f"https://music.163.com/song/media/outer/url?id={song_id}.mp3"
    
    st.write(f"**歌曲ID:** {song_id}")
    st.audio(custom_url, format="audio/mp3")
    
    if st.button("播放此ID的歌曲", use_container_width=True):
        st.info(f"正在播放ID为 {song_id} 的歌曲...")

# 页脚
st.write("---")
st.caption("音乐播放器 | 基于Streamlit开发 | 使用网易云音乐API")
