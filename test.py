import streamlit as st
import random

# -------------------
# 기본 설정
# -------------------
st.set_page_config(page_title="단어 맞추기 시험", page_icon="📝", layout="centered")

# -------------------
# 기본 단어 데이터
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
if "questions" not in st.session_state:
    st.session_state.questions = random.sample(default_words, 10)  # 10문제 랜덤
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answers" not in st.session_state:
    st.session_state.answers = []  # 사용자 선택 기록
if "finished" not in st.session_state:
    st.session_state.finished = False

# -------------------
# 보기 생성 함수
# -------------------
def make_options(answer, all_words):
    options = [answer]
    while len(options) < 4:
        m = random.choice(all_words)["meaning"]
        if m not in options:
            options.append(m)
    random.shuffle(options)
    return options

# -------------------
# 앱 제목
# -------------------
st.title("📝 단어 맞추기 시험 모드 (10문제)")

# -------------------
# 시험 진행
# -------------------
if not st.session_state.finished:
    q_index = st.session_state.current_q
    question = st.session_state.questions[q_index]
    st.subheader(f"문제 {q_index+1} / 10")
    st.write(f"영어 단어: **{question['word']}**")

    # 보기 생성
    options = make_options(question["meaning"], default_words)

    # 선택
    choice = st.radio("뜻을 고르세요:", options, key=f"q{q_index}")

    # 제출 버튼
    if st.button("제출", key=f"submit{q_index}"):
        if choice is None:
            st.warning("⚠️ 답을 선택하세요!")
        else:
            # 정답 체크 및 점수 기록
            correct = choice == question["meaning"]
            if correct:
                st.session_state.score += 1
                st.success("✅ 정답입니다!")
            else:
                st.error(f"❌ 오답! 정답: {question['meaning']}")

            # 답안 기록
            st.session_state.answers.append({
                "word": question["word"],
                "your_answer": choice,
                "correct_answer": question["meaning"],
                "correct": correct
            })

            # 다음 문제 이동
            st.session_state.current_q += 1

            # 시험 종료 체크
            if st.session_state.current_q >= 10:
                st.session_state.finished = True

# -------------------
# 시험 종료 후 결과
# -------------------
if st.session_state.finished:
    st.subheader("📊 시험 종료!")
    st.write(f"최종 점수: **{st.session_state.score} / 10**")

    st.subheader("📖 틀린 문제 복습")
    for ans in st.session_state.answers:
        if not ans["correct"]:
            st.write(f"- 단어: **{ans['word']}** → 당신의 답: {ans['your_answer']} ❌ | 정답: ✅ {ans['correct_answer']}")

    # 다시 시작 버튼
    if st.button("다시 시작"):
        st.session_state.questions = random.sample(default_words, 10)
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.answers = []
        st.session_state.finished = False
