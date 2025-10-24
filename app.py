import streamlit as st
import random

# --- 페이지 설정 ---
st.set_page_config(page_title="숫자 맞추기 게임", page_icon="🎯", layout="centered")
st.markdown("<h1 style='text-align:center;'>🎯 숫자 맞추기 게임 🎯</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>두 개의 숫자 중 정답을 골라보세요!</p>", unsafe_allow_html=True)

# --- 세션 상태 초기화 ---
if "score" not in st.session_state:
    st.session_state.score = 0
if "lives" not in st.session_state:
    st.session_state.lives = 3
if "answer" not in st.session_state:
    st.session_state.answer = random.randint(1, 20)
if "choices" not in st.session_state:
    wrong = random.randint(1, 20)
    while wrong == st.session_state.answer:
        wrong = random.randint(1, 20)
    st.session_state.choices = random.sample([st.session_state.answer, wrong], 2)
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

# --- 게임 오버 화면 ---
if st.session_state.game_over:
    st.error("💀 게임 오버 💀")
    st.markdown(f"<h3 style='text-align:center;'>최종 점수: {st.session_state.score}</h3>", unsafe_allow_html=True)
    if st.button("🔁 다시 시작하기"):
        st.session_state.score = 0
        st.session_state.lives = 3
        st.session_state.game_over = False
        st.session_state.answer = random.randint(1, 20)
        wrong = random.randint(1, 20)
        while wrong == st.session_state.answer:
            wrong = random.randint(1, 20)
        st.session_state.choices = random.sample([st.session_state.answer, wrong], 2)
        st.session_state.result = None
        st.rerun()
    st.stop()

# --- 보기 버튼 2개 ---
st.markdown("<h3 style='text-align:center;'>정답을 고르세요 👇</h3>", unsafe_allow_html=True)
cols = st.columns(2)
for i, num in enumerate(st.session_state.choices):
    with cols[i]:
        if st.button(str(num), use_container_width=True):
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
            wrong = random.randint(1, 20)
            while wrong == st.session_state.answer:
                wrong = random.randint(1, 20)
            st.session_state.choices = random.sample([st.session_state.answer, wrong], 2)
            st.session_state.result = None
            st.rerun()
