import streamlit as st
from PIL import Image, ImageDraw
import time, random

st.set_page_config(page_title="야바위 게임", page_icon="🎩", layout="centered")
st.markdown("<h1 style='text-align:center;'>🎩 야바위 게임 🎩</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>공이 들어있는 컵을 맞춰보세요!</p>", unsafe_allow_html=True)

# 기본 설정
width, height = 600, 400
cup_width, cup_height = 80, 100
ball_radius = 15
cup_y = 200
positions_x = [150, 300, 450]

# 세션 상태 초기화
if "ball_position" not in st.session_state:
    st.session_state.ball_position = random.randint(0, 2)
if "shuffled" not in st.session_state:
    st.session_state.shuffled = False
if "show_result" not in st.session_state:
    st.session_state.show_result = False


def draw_scene(ball_pos=None, cup_positions=None):
    """PIL로 컵 3개와 공을 그리는 함수"""
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    # 공
    if ball_pos is not None:
        bx = cup_positions[ball_pos]
        draw.ellipse(
            (bx - ball_radius, cup_y + cup_height - 20,
             bx + ball_radius, cup_y + cup_height + 10),
            fill="red", outline="black"
        )

    # 컵
    for x in cup_positions:
        draw.rectangle(
            (x - cup_width//2, cup_y - cup_height, x + cup_width//2, cup_y),
            fill="lightblue", outline="black", width=3
        )

    return img


def shuffle_animation():
    """컵 섞기 애니메이션"""
    placeholder = st.empty()
    cup_positions = positions_x[:]
    sequence = [random.sample([0, 1, 2], 2) for _ in range(8)]

    for (i, j) in sequence:
        start_i, start_j = cup_positions[i], cup_positions[j]
        for step in range(20):
            t = step / 20
            # i컵은 j위치로, j컵은 i위치로 이동
            cup_positions[i] = int(start_i + (start_j - start_i) * t)
            cup_positions[j] = int(start_j + (start_i - start_j) * t)

            img = draw_scene(None, cup_positions)
            placeholder.image(img, use_container_width=True)
            time.sleep(0.03)

        cup_positions[i], cup_positions[j] = start_j, start_i

    # 공 위치 갱신
    st.session_state.ball_position = cup_positions.index(positions_x[st.session_state.ball_position])
    st.session_state.shuffled = True
    placeholder.empty()


# 컵 표시
def show_cups(show_ball=False):
    img = draw_scene(st.session_state.ball_position if show_ball else None, positions_x)
    st.image(img, use_container_width=True)


# 메인 로직
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

# 결과 표시
if st.session_state.show_result:
    show_cups(show_ball=True)
    if st.session_state.choice == st.session_state.ball_position:
        st.success("🎉 정답입니다! 공을 찾았어요!")
    else:
        st.error("❌ 틀렸습니다! 다시 시도해보세요!")

    if st.button("🔁 다시 하기"):
        st.session_state.shuffled = False
        st.session_state.show_result = False
        st.rerun()
