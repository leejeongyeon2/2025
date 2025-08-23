import streamlit as st
import random

# 앱 기본 설정 (페이지 제목, 아이콘, 레이아웃)
st.set_page_config(page_title="🌈 단어 암기 앱", page_icon="📚", layout="centered")

# -------------------
# CSS 스타일 정의 (배경, 카드, 버튼 모양)
# -------------------
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #ffecd2, #fcb69f); /* 배경 그라데이션 */
    }
    .flashcard { /* 플래시카드 스타일 */
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        background: white;
        font-size: 28px;
        font-weight: bold;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        margin: 20px 0;
    }
    .option-btn { /* 버튼 스타일 */
        display: inline-block;
        padding: 12px 20px;
        margin: 5px;
        border-radius: 12px;
        background: #4CAF50;
        color: white;
        font-weight: bold;
        cursor: pointer;
        transition: 0.2s;
    }
    .option-btn:hover {
        background: #45a049;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# -------------------
# 기본 단어 데이터 (20개 예시)
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
# 세션 상태 (앱 실행 중 데이터 유지)
# -------------------
if "words" not in st.session_state:  # 단어 리스트
    st.session_state.words = default_words.copy()
if "correct" not in st.session_state:  # 맞춘 개수
    st.session_state.correct = 0
if "wrong" not in st.session_state:  # 틀린 개수
    st.session_state.wrong = 0
if "current_index" not in st.session_state:  # 현재 플래시카드 인덱스
    st.session_state.current_index = 0
if "show_meaning" not in st.session_state:  # 뜻 보기 여부
    st.session_state.show_meaning = False

# -------------------
# 앱 제목
# -------------------
st.title("🌈 화려한 단어 암기 앱")

# -------------------
# 단어 추가 폼
# -------------------
st.subheader("✏️ 단어 추가")
with st.form("add_word"):
    w = st.text_input("단어 입력")
    m = st.text_input("뜻 입력")
    submitted = st.form_submit_button("추가")
    if submitted and w and m:
        st.session_state.words.append({"word": w, "meaning": m})
        st.success(f"✅ 추가됨: {w} - {m}")

# -------------------
# 플래시카드 기능
# -------------------
st.subheader("📖 플래시카드")
word = st.session_state.words[st.session_state.current_index]  # 현재 단어
content = word["meaning"] if st.session_state.show_meaning else word["word"]

# 카드에 표시
st.markdown(f"<div class='flashcard'>{content}</div>", unsafe_allow_html=True)

# 버튼 (뜻 보기/다음 단어)
col1, col2 = st.columns(2)
with col1:
    if st.button("🔄 단어/뜻 전환"):
        st.session_state.show_meaning = not st.session_state.show_meaning
with col2:
    if st.button("➡️ 다음 단어"):
        st.session_state.current_index = (st.session_state.current_index + 1) % len(st.session_state.words)
        st.session_state.show_meaning = False

# -------------------
# 퀴즈 모드
# -------------------
st.subheader("❓ 퀴즈 모드")
quiz_word = random.choice(st.session_state.words)  # 무작위 문제 단어
st.write(f"단어: **{quiz_word['word']}**")

# 보기 4개 생성 (정답 + 랜덤 오답)
options = [quiz_word["meaning"]]
while len(options) < 4 and len(options) < len(st.session_state.words):
    m = random.choice(st.session_state.words)["meaning"]
    if m not in options:
        options.append(m)
random.shuffle(options)

# 보기 선택
choice = st.radio("뜻을 고르세요:", options, key=random.random())

# 정답 확인
if st.button("정답 확인"):
    if choice == quiz_word["meaning"]:
        st.session_state.correct += 1
        st.success("✅ 정답입니다!")
    else:
        st.session_state.wrong += 1
        st.error(f"❌ 오답입니다! 정답: {quiz_word['meaning']}")

# -------------------
# 통계 표시
# -------------------
st.subheader("📊 통계")
st.write(f"👍 맞춘 개수: **{st.session_state.correct}**  |  👎 틀린 개수: **{st.session_state.wrong}**")
