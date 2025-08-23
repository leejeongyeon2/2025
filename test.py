import streamlit as st
import random

st.set_page_config(page_title="단어 암기 앱", page_icon="📚")

# 세션 상태 초기화
if "words" not in st.session_state:
    st.session_state.words = [
        {"word": "apple", "meaning": "사과"},
        {"word": "book", "meaning": "책"},
        {"word": "school", "meaning": "학교"},
    ]
if "correct" not in st.session_state:
    st.session_state.correct = 0
if "wrong" not in st.session_state:
    st.session_state.wrong = 0

st.title("📚 단어 암기 앱 (Streamlit)")

# -------------------
# 단어 추가
# -------------------
st.subheader("✏️ 단어 추가")
with st.form("add_word"):
    w = st.text_input("단어 입력")
    m = st.text_input("뜻 입력")
    submitted = st.form_submit_button("추가")
    if submitted and w and m:
        st.session_state.words.append({"word": w, "meaning": m})
        st.success(f"추가됨: {w} - {m}")

# -------------------
# 플래시카드
# -------------------
st.subheader("📖 플래시카드")
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "show_meaning" not in st.session_state:
    st.session_state.show_meaning = False

word = st.session_state.words[st.session_state.current_index]
if st.button("단어 보기 / 뜻 보기"):
    st.session_state.show_meaning = not st.session_state.show_meaning

st.write("👉", word["meaning"] if st.session_state.show_meaning else word["word"])

if st.button("다음 단어"):
    st.session_state.current_index = (st.session_state.current_index + 1) % len(st.session_state.words)
    st.session_state.show_meaning = False

# -------------------
# 퀴즈 모드
# -------------------
st.subheader("❓ 퀴즈 모드")
quiz_word = random.choice(st.session_state.words)
st.write(f"단어: **{quiz_word['word']}**")

options = [quiz_word["meaning"]]
while len(options) < 4 and len(options) < len(st.session_state.words):
    m = random.choice(st.session_state.words)["meaning"]
    if m not in options:
        options.append(m)
random.shuffle(options)

choice = st.radio("뜻을 고르세요:", options)
if st.button("정답 확인"):
    if choice == quiz_word["meaning"]:
        st.session_state.correct += 1
        st.success("✅ 정답입니다!")
    else:
        st.session_state.wrong += 1
        st.error(f"❌ 오답입니다! 정답: {quiz_word['meaning']}")

# -------------------
# 통계
# -------------------
st.subheader("📊 통계")
st.write(f"맞춘 개수: {st.session_state.correct} | 틀린 개수: {st.session_state.wrong}")
