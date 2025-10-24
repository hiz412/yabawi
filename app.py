import streamlit as st
import random

# --- 기본 설정 ---
st.set_page_config(page_title="숫자 맞추기 게임", page_icon="🎯", layout="centered")
st.markdown("<h1 style='text-align:center;'>🎯 숫자 맞추기 게임 🎯</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>무작위로 정해진 숫자를 맞춰보세요!</p>", unsafe_allow_html=True)

# --- 세션 상태 초기화 ---
if "score" not in st.session_state:
    st.session_state.score = 0
if "lives" not in st.session_state:
    st.session_state.lives = 3
if "answer" not in st.session_state:
    st.session_state.answer = random.randint(1, 20)
if "choices" not in st.session_state:
    st.session_state.choices = random.sample(range(1, 21), 5)
    if st.session_state.answer not in st.session_state.choices:
        st.session_state.choices[random.randint(0, 4)] = st.session_state.answer
if "selected" not in st.session_state:
    st.session_state.selected = None
if "result" not in st.session_state:
    st.session_state.result = None
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# --- 점수 및 목숨 표시 ---
st.markdown(
    f"""
    <div style='text-align:center; font-size:18px;'>
        💯 점수: <b>{st.session_state.score}</b>　
        ❤️ 목숨: <b>{'❤' * st.session_state.lives}</b>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# --- 게임 종료 화면 ---
if st.session_state.game_over:
    st.error("💀 게임 오버! 💀")
    st.markdown(f"<h3 style='text-align:center;'>최종 점수: {st.session_state.score}</h3>", unsafe_allow_html=True)
    if st.button("🔁 다시 시작하기"):
        st.session_state.score = 0
        st.session_state.lives = 3
        st.session_state.game_over = False
        st.session_state.answer = random.randint(1, 20)
        st.session_state.choices = random.sample(range(1, 21), 5)
        if st.session_state.answer not in st.session_state.choices:
            st.session_state.choices[random.randint(0, 4)] = st.session_state.answer
        st.session_state.result = None
        st.session_state.selected = None
        st.rerun()
    st.stop()

# --- 문제 선택 구간 ---
st.markdown("<h3 style='text-align:center;'>보기 중 하나를 선택하세요 👇</h3>", unsafe_allow_html=True)
cols = st.columns(5)
for i, num in enumerate(st.session_state.choices):
    with cols[i]:
        if st.button(str(num), use_container_width=True):
            st.session_state.selected = num
            if num == st.session_state.answer:
                st.session_state.result = "correct"
                st.session_state.score += 10
            else:
                st.session_state.result = "wrong"
                st.session_state.lives -= 1
                if st.session_state.lives <= 0:
                    st.session_state.game_over = True
            st.rerun()

# --- 결과 표시 ---
if st.session_state.result:
    if st.session_state.result == "correct":
        st.success(f"🎉 정답입니다! +10점 (정답: {st.session_state.answer})")
    else:
        st.error(f"❌ 틀렸습니다! 정답은 {st.session_state.answer} 입니다.")

    if not st.session_state.game_over:
        if st.button("➡ 다음 문제"):
            st.session_state.answer = random.randint(1, 20)
            st.session_state.choices = random.sample(range(1, 21), 5)
            if st.session_state.answer not in st.session_state.choices:
                st.session_state.choices[random.randint(0, 4)] = st.session_state.answer
            st.session_state.result = None
            st.session_state.selected = None
            st.rerun()
