import streamlit as st
import random
import time
from PIL import Image, ImageDraw

# --- 기본 설정 ---
st.set_page_config(page_title="야바위 게임", page_icon="🎩", layout="centered")
st.title("🎩 야바위 게임 (Shell Game)")
st.write("컵 아래 숨겨진 공을 맞혀보세요!")

# --- 캔버스 설정 ---
CANVAS_W, CANVAS_H = 600, 320
Y_BASE = 220  # 컵의 바닥 y 좌표 기준
SLOT_X = [100, 250, 400]  # 슬롯(고정) x 좌표

# --- 이미지(도형) 생성 ---
def make_cup_img(color="gray"):
    img = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # 컵 몸통
    draw.rectangle([10, 40, 110, 110], fill=color, outline="black", width=3)
    # 컵의 윗부분
    draw.rectangle([30, 20, 90, 40], fill=color, outline="black", width=3)
    return img

def make_ball_img(color="red"):
    img = Image.new("RGBA", (44, 44), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([4, 4, 40, 40], fill=color, outline="black", width=2)
    return img

cup_img = make_cup_img()
ball_img = make_ball_img()

# --- 세션 상태 초기화 ---
if "current_order" not in st.session_state:
    # current_order[slot_index] = cup_id(0..2). 초기엔 slot 0에 cup0, slot1->cup1 ...
    st.session_state.current_order = [0, 1, 2]
if "ball_cup" not in st.session_state:
    # ball_cup는 '어떤 컵(id)' 안에 공이 있는지 (cup_id)
    st.session_state.ball_cup = random.randint(0, 2)
if "animating" not in st.session_state:
    st.session_state.animating = False
if "choice" not in st.session_state:
    st.session_state.choice = None

# --- 장면 그리기 함수 ---
def draw_scene(override_positions=None, show_ball=False):
    """
    override_positions: dict {slot_index: x_pos} 가 주어지면 해당 슬롯 컵은 그 x에 그림.
    show_ball: True면 공을 보이게 함 (공은 그 컵의 중앙 아래에 위치)
    """
    scene = Image.new("RGB", (CANVAS_W, CANVAS_H), "white")
    for slot_idx in range(3):
        # 기본 슬롯 x
        base_x = SLOT_X[slot_idx]
        x = override_positions.get(slot_idx, base_x) if override_positions else base_x
        cup_id = st.session_state.current_order[slot_idx]
        # 컵 이미지는 동일(도형). 위치 조정: 컵 이미지의 왼쪽 위치 = x - cup_img.width//2
        scene.paste(cup_img, (int(x - cup_img.width//2), Y_BASE - cup_img.height), cup_img)
    # 공 표시 (슬롯 기준 찾기)
    if show_ball:
        # 공이 들어있는 컵이 어느 슬롯에 있는지 찾음
        ball_slot = None
        for sidx, cupid in enumerate(st.session_state.current_order):
            if cupid == st.session_state.ball_cup:
                ball_slot = sidx
                break
        if ball_slot is not None:
            bx = override_positions.get(ball_slot, SLOT_X[ball_slot]) if override_positions else SLOT_X[ball_slot]
            # 공 위치: 컵 중앙 아래 (y 기준)
            ball_x = int(bx - ball_img.width//2 + 0)
            ball_y = Y_BASE - cup_img.height + cup_img.height + 6  # 컵 바로 아래
            scene.paste(ball_img, (ball_x, ball_y), ball_img)
    return scene

# --- 부드러운 자리 교환 애니메이션 ---
def animate_swap(slot_a, slot_b, steps=18, delay=0.03):
    """
    slot_a, slot_b: 교환할 슬롯 인덱스 (0..2)
    steps: 프레임 수
    delay: 각 프레임 간 간격 (초)
    """
    st.session_state.animating = True
    placeholder = st.empty()

    start_a = SLOT_X[slot_a]
    start_b = SLOT_X[slot_b]

    # 현재 order에서 해당 슬롯들의 cup_id는 그대로 유지하되, 화면에서 x좌표만 보간
    for step in range(1, steps + 1):
        t = step / steps
        # ease in-out (부드럽게)
        # simple easing: 0.5 - cos(pi * t)/2
        import math
        eased = 0.5 - math.cos(math.pi * t) / 2
        pos_override = {}
        pos_override[slot_a] = int(start_a + (start_b - start_a) * eased)
        pos_override[slot_b] = int(start_b + (start_a - start_b) * eased)
        # the third slot stays put
        scene = draw_scene(override_positions=pos_override, show_ball=False)
        placeholder.image(scene)
        time.sleep(delay)

    # 실제 current_order를 스왑(시각적 애니메이션 끝난 뒤에)
    st.session_state.current_order[slot_a], st.session_state.current_order[slot_b] = (
        st.session_state.current_order[slot_b],
        st.session_state.current_order[slot_a],
    )
    st.session_state.animating = False
    # 마지막 장면(정렬된 위치)
    placeholder.image(draw_scene())

# --- 섞기 애니메이션: 여러번 랜덤 스왑 호출 ---
def shuffle_animation(num_swaps=6):
    if st.session_state.animating:
        return
    # 랜덤 쌍 목록 만들기
    swaps = []
    for _ in range(num_swaps):
        a, b = random.sample(range(3), 2)
        swaps.append((a, b))
    for a, b in swaps:
        animate_swap(a, b, steps=20, delay=0.03)
        # 잠깐 대기(자연스러움)
        time.sleep(0.08)

# --- UI: 플레이 버튼 등 ---
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("섞기 (Shuffle)"):
        shuffle_animation(num_swaps=6)
with col2:
    if st.button("공 보기 (Show Ball)"):
        st.image(draw_scene(show_ball=True))
with col3:
    if st.button("다시 시작 (Reset)"):
        st.session_state.current_order = [0, 1, 2]
        st.session_state.ball_cup = random.randint(0, 2)
        st.session_state.choice = None
        st.experimental_rerun()

st.write("---")
st.write("어느 컵에 공이 있을까요? 아래 버튼을 눌러 선택하세요.")

# 이미지 프리뷰 (처음 장면)
scene_placeholder = st.empty()
scene_placeholder.image(draw_scene())

# 선택 버튼들
btn_cols = st.columns(3)
for i in range(3):
    if btn_cols[i].button(f"컵 {i+1} 선택"):
        if st.session_state.animating:
            st.warning("지금 애니메이션 중입니다. 끝난 뒤에 선택하세요.")
        else:
            st.session_state.choice = i
            # 선택한 슬롯에 들어있는 컵 id가 ball_cup와 같으면 정답
            selected_cup = st.session_state.current_order[i]
            if selected_cup == st.session_state.ball_cup:
                st.success("🎉 정답입니다! 공을 찾았어요!")
            else:
                st.error("😢 틀렸어요! 공의 위치를 보여줄게요.")
            # 결과 보여주기
            st.image(draw_scene(show_ball=True))
