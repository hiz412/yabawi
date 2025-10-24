import streamlit as st
import random
import time
from PIL import Image, ImageDraw

# --- 기본 설정 ---
st.set_page_config(page_title="야바위 게임", page_icon="🎩", layout="centered")
st.title("🎩 야바위 게임 (Shell Game)")
st.write("컵 아래 숨겨진 공을 맞혀보세요!")

# --- 흰색 배경 만들기 ---
background = Image.new("RGB", (600, 300), "white")

# --- 컵 이미지와 공 이미지 만들기 (단색 도형으로 대체) ---
def make_cup(color="gray"):
    img = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 30, 90, 90], fill=color, outline="black", width=2)
    draw.rectangle([30, 10, 70, 30], fill=color, outline="black", width=2)
    return img

def make_ball(color="red"):
    img = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([5, 5, 35, 35], fill=color, outline="black", width=2)
    return img

cup_img = make_cup()
ball_img = make_ball()

# --- 위치 설정 ---
positions = [(100, 180), (250, 180), (400, 180)]  # 컵 3개 위치

# --- 초기 상태 ---
if "ball_pos" not in st.session_state:
    st.session_state.ball_pos = random.randint(0, 2)
if "shuffled" not in st.session_state:
    st.session_state.shuffled = False
if "choice" not in st.session_state:
    st.session_state.choice = None

# --- 컵과 공을 그리는 함수 ---
def draw_scene(show_ball=False):
    scene = background.copy()
    for i, (x, y) in enumerate(positions):
        if show_ball and i == st.session_state.ball_pos:
            scene.paste(ball_img, (x + 30, y - 40), ball_img)
        scene.paste(cup_img, (x, y - 100), cup_img)
    return scene

# --- 컵 섞기 애니메이션 ---
def shuffle_animation():
    st.session_state.shuffled = True
    img_placeholder = st.empty()

    ball_pos = st.session_state.ball_pos
    for _ in range(5):  # 5번 섞기
        i1, i2 = random.sample(range(3), 2)
        positions[i1], positions[i2] = positions[i2], positions[i1]
        if ball_pos == i1:
            ball_pos = i2
        elif ball_pos == i2:
            ball_pos = i1
        st.session_state.ball_pos = ball_pos
        scene = draw_scene()
        img_placeholder.image(scene)
        time.sleep(0.6)
    img_placeholder.image(draw_scene())

# --- 버튼 영역 ---
col1, col2, col3 = st.columns(3)
if col1.button("섞기 시작"):
    shuffle_animation()
if col2.button("공 위치 보기"):
    st.image(draw_scene(show_ball=True))
if col3.button("다시 시작"):
    st.session_state.ball_pos = random.randint(0, 2)
    st.session_state.shuffled = False
    st.session_state.choice = None
    st.experimental_rerun()

# --- 선택하기 ---
st.write("공이 어디에 있을까요?")
cols = st.columns(3)
for i in range(3):
    if cols[i].button(f"컵 {i+1}"):
        st.session_state.choice = i
        if i == st.session_state.ball_pos:
            st.success("🎉 정답입니다! 공을 찾았어요!")
        else:
            st.error("😢 틀렸어요! 다음엔 더 잘할 수 있을 거예요!")
        st.image(draw_scene(show_ball=True))
