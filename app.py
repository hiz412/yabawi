import streamlit as st
import random
from PIL import Image

# --- 설정 ---
st.set_page_config(page_title="야바위 게임 🎩", page_icon="🎩", layout="centered")

st.title("🎩 야바위 게임 (Shell Game)")
st.markdown("컵 아래 숨겨진 공을 맞혀보세요!")

# --- 이미지 로드 ---
cup_img = Image.open("images/cup.png")
ball_img = Image.open("images/ball.png")
background_img = Image.open("images/background.jpg")

st.image(background_img, use_container_width=True)

# --- 상태 초기화 ---
if "ball_position" not in st.session_state:
    st.session_state.ball_position = random.randint(0, 2)
if "revealed" not in st.session_state:
    st.session_state.revealed = False

# --- 컵 표시 ---
cols = st.columns(3)

# 3개의 컵 버튼 생성
for i in range(3):
    with cols[i]:
        if st.button(f"컵 {i+1}"):
            st.session_state.revealed = True
            st.session_state.choice = i

# --- 결과 표시 ---
if st.session_state.revealed:
    st.write("---")
    correct = st.session_state.ball_position
    choice = st.session_state.choice

    # 컵 아래 공 보여주기
    cup_display = []
    for i in range(3):
        if i == correct:
            cup_display.append(ball_img)
        else:
            cup_display.append(cup_img)
    
    st.image(cup_display, width=150)

    if choice == correct:
        st.success("🎉 정답입니다! 공을 찾았어요!")
    else:
        st.error(f"😅 아쉽네요! 공은 컵 {correct+1}번에 있었어요.")

    if st.button("다시 하기 🔄"):
        st.session_state.ball_position = random.randint(0, 2)
        st.session_state.revealed = False
        st.rerun()
else:
    st.info("컵을 클릭해서 공이 어디 있는지 맞혀보세요!")

