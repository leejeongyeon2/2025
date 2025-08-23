import streamlit as st
import random

# -------------------
# 기본 설정
# -------------------
st.set_page_config(page_title="단어 맞추기 앱", page_icon="📝", layout="centered")

# -------------------
# 기본 단어 데이터 (예시 20개)
# -------------------
default_words = [
    {"word": "apple", "meaning": "사과"},
    {"word": "book", "meaning": "책"},
    {"word": "school", "meaning": "학교"},
    {"word": "computer", "meaning": "컴퓨터"},
    {"word": "dream", "meaning": "꿈"},
    {"word": "family", "meaning": "가족"},
    {"word": "friend", "meaning": "친구"},
    {"word": "future", "meaning": "미래"},
    {"word": "happiness", "meaning": "행복"},
    {"word": "journey", "meaning": "여행"},
    {"word": "knowledge", "meaning": "지식"},
    {"word": "language", "meaning": "언어"},
    {"word": "music", "meaning": "음악"},
    {"word": "nature", "meaning": "자연"},
    {"word": "ocean", "meaning": "바다"},
    {"word": "peace", "meaning": "평화"},
    {"word": "science", "meaning": "과학"},
    {"word": "success", "meaning": "성공"},
    {"word": "universe", "meaning": "우주"},
    {"word": "victory", "meaning": "승리"},
]

# -------------------
# 세션 상태 초기화
# -------------------
if "words" not in st.session_state:      # 단어 리스트
    st.session_state.words = default_words.copy()
if "correct" not in st.session_state:    # 맞춘 개수
    st.session_state.correct = 0
if "wrong" not in st.session_state:      # 틀린 개수
    st.session_state.wrong = 0
if "quiz_word" not in st.session_state:  # 현재 문제 단어
    st.session_state.quiz_word = random.choice(st.session_state.words)
if "options" not in st.session_state:    # 현재 문제 보기
    st.session_state.options = []

# -------------------
# 퀴즈 생성 함수
# -------------------
def make_quiz():
    """랜덤으로 문제(단어와 보기 4개)를 생성"""
    quiz_word = random.choice(st.session_state.words)  # 문제 단어
    options = [quiz_word["meaning"]]                   # 정답 포함
    # 오답 보기 추가
    while len(options) < 4 and len(options) < len(st.session_state.words):
        m = random.choice(st.session_state.words)["meaning"]
        if m not in options:
            options.append(m)
    random.shuffle(options)                            # 보기 섞기
    st.session_state.quiz_word = quiz_word
    st.session_state.options = options

# -------------------
# 앱 제목
# -------------------
st.title("📝 단어 맞추기 퀴즈 앱")

# -------------------
# 단어 추가
# -------------------
st.subheader("✏️ 단어 추가")
with st.form("add_word"):
    w = st.text_input("영어 단어 입력")
    m = st.text_input("뜻 입력")
    submitted = st.form_submit_button("추가")
    if submitted and w and m:
        st.session_state.words.append({"word": w, "meaning": m})
        st.success(f"✅ 추가됨: {w} - {m}")

# -------------------
# 퀴즈 문제 표시
# -------------------
st.subheader("❓ 퀴즈 모드")

# 새로운 문제 생성 버튼
if st.button("새 문제 출제"):
    make_quiz()

# 현재 문제 단어 보여주기
quiz_word = st.session_state.quiz_word
st.write(f"영어 단어: **{quiz_word['word']}**")

# 보기 선택
choice = st.radio("뜻을 고르세요:", st.session_state.options, index=None)

# 정답 확인 버튼
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
st.write(f"👍 맞춘 개수: **{st.session_state.correct}**  |  👎 틀린 개수: **{st.session_state.wrong}**")
