import streamlit as st
import time
import random

# ----- 기본 설정 -----
st.set_page_config(page_title="야바위 게임", page_icon="🎩", layout="centered")
st.markdown("<h1 style='text-align:center;'>🎩 야바위 게임 🎩</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>공이 들어있는 컵을 맞춰보세요!</p>", unsafe_allow_html=True)

# ----- 이미지 URL (수정 가능) -----
CUP_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Red_cup.svg/512px-Red_cup.svg.png"
BALL_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Billiard_ball_3.png/240px-Billiard_ball_3.png"

# ----- 상태 초기화 -----
if "ball_position" not in st.session_state:
    st.session_state.ball_position = random.randint(0, 2)
if "shuffled" not in st.session_state:
    st.session_state.shuffled = False
if "show_result" not in st.session_state:
    st.session_state.show_result = False

# ----- 컵 섞기 애니메이션 -----
def shuffle_animation():
    placeholder = st.empty()
    positions = [0, 1, 2]
    sequence = []

    # 섞는 순서 랜덤 생성
    for _ in range(8):
        i, j = random.sample([0, 1, 2], 2)
        sequence.append((i, j))

    # 컵 이동 시각적 애니메이션
    for (i, j) in sequence:
        for shift in range(0, 20, 2):  # 왼쪽→오른쪽 이동
            with placeholder.container():
                st.markdown(
                    f"""
                    <div style='text-align:center; background:white;'>
                        <img src='{CUP_URL}' width='{120 - shift}' style='margin:20px;'>
                        <img src='{CUP_URL}' width='{120 + shift}' style='margin:20px;'>
                        <img src='{CUP_URL}' width='120' style='margin:20px;'>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            time.sleep(0.03)
        positions[i], positions[j] = positions[j], positions[i]

    st.session_state.ball_position = positions.index(st.session_state.ball_position)
    st.session_state.shuffled = True
    placeholder.empty()

# ----- 컵 보여주기 -----
def show_cups(show_ball=False):
    st.markdown("<div style='text-align:center; background:white;'>", unsafe_allow_html=True)
    for i in range(3):
        if show_ball and i == st.session_state.ball_position:
            st.markdown(f"<img src='{BALL_URL}' width='80' style='margin:10px;'>", unsafe_allow_html=True)
        st.markdown(f"<img src='{CUP_URL}' width='120' style='margin:20px;'>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ----- 메인 로직 -----
if not st.session_state.shuffled:
    if st.button("🔀 컵 섞기 시작하기"):
        shuffle_animation()
        st.rerun()
else:
    show_cups()
    st.markdown("<br>", unsafe_allow_html=True)
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            if st.button(f"🎩 컵 {i+1} 선택"):
                st.session_state.choice = i
                st.session_state.show_result = True
                st.rerun()

# ----- 결과 -----
if st.session_state.show_result:
    st.markdown("<br><hr>", unsafe_allow_html=True)
    show_cups(show_ball=True)

    if st.session_state.choice == st.session_state.ball_position:
        st.success("🎉 정답입니다! 공을 찾았어요!")
    else:
        st.error("❌ 틀렸습니다! 다시 시도해보세요!")

    if st.button("🔁 다시 하기"):
        st.session_state.shuffled = False
        st.session_state.show_result = False
        st.rerun()
