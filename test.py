import streamlit as st
import random

# -------------------
# 기본 설정
# -------------------
st.set_page_config(page_title="단어 맞추기 시험", page_icon="📝", layout="centered")

# -------------------
# 단어 데이터
# -------------------
words_list = [
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
    st.session_state.questions = random.sample(words_list, 10)
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answers" not in st.session_state:
    st.session_state.answers = []
if "finished" not in st.session_state:
    st.session_state.finished = False

# -------------------
# 보기 생성 함수
# -------------------
def make_options(correct_meaning):
    options = [correct_meaning]
    while len(options) < 4:
        m = random.choice(words_list)["meaning"]
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
    idx = st.session_state.current_index
    question = st.session_state.questions[idx]

    st.subheader(f"문제 {idx+1} / 10")
    st.write(f"영어 단어: **{question['word']}**")

    # 보기 생성
    options = make_options(question["meaning"])

    # 문제별 radio key 고정 → 선택 유지
    choice_key = f"choice_{idx}"
    if choice_key not in st.session_state:
        st.session_state[choice_key] = options[0]  # 기본값 설정

    st.session_state[choice_key] = st.radio(
        "뜻을 선택하세요:", options, index=options.index(st.session_state[choice_key]), key=choice_key
    )

    # 제출 버튼
    if st.button("제출", key=f"submit_{idx}"):
        selected = st.session_state[choice_key]
        correct = selected == question["meaning"]
        if correct:
            st.session_state.score += 1
            st.success("✅ 정답입니다!")
        else:
            st.error(f"❌ 오답! 정답: {question['meaning']}")

        # 답안 기록
        st.session_state.answers.append({
            "word": question["word"],
            "your_answer": selected,
            "correct_answer": question["meaning"]
        })

        # 다음 문제 이동
        st.session_state.current_index += 1
        if st.session_state.current_index >= 10:
            st.session_state.finished = True

        # radio 값 초기화 방지 → 새로운 문제 key 자동 적용
        st.experimental_rerun()  # 안정적으로 다음 문제 표시

# -------------------
# 시험 종료 후 결과
# -------------------
if st.session_state.finished:
    st.subheader("📊 시험 종료!")
    st.write(f"최종 점수: **{st.session_state.score} / 10**")

    st.subheader("📖 틀린 문제 복습")
    for ans in st.session_state.answers:
        if ans["your_answer"] != ans["correct_answer"]:
            st.write(f"- 단어: **{ans['word']}** → 당신의 답: {ans['your_answer']} ❌ | 정답: ✅ {ans['correct_answer']}")

    if st.button("다시 시작"):
        st.session_state.questions = random.sample(words_list, 10)
        st.session_state.current_index = 0
        st.session_state.score = 0
        st.session_state.answers = []
        st.session_state.finished = False
        st.experimental_rerun()
