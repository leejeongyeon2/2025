import streamlit as st
import random

# -------------------
# 앱 기본 설정
# -------------------
st.set_page_config(page_title="화려한 수학 퀴즈", page_icon="🎯", layout="centered")

# -------------------
# 난이도별 설정
# -------------------
difficulty_levels = {
    "쉬움": {"range": 10, "ops": ["+", "-"]},
    "보통": {"range": 20, "ops": ["+", "-", "*"]},
    "어려움": {"range": 50, "ops": ["+", "-", "*", "/"]}
}

# -------------------
# 세션 상태 초기화
# -------------------
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "보통"
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "questions" not in st.session_state:
    st.session_state.questions = []
if "answers" not in st.session_state:
    st.session_state.answers = []
if "finished" not in st.session_state:
    st.session_state.finished = False

# -------------------
# 난이도 선택
# -------------------
st.sidebar.title("⚙️ 난이도 설정")
st.session_state.difficulty = st.sidebar.radio("난이도를 선택하세요:", ["쉬움", "보통", "어려움"])

# -------------------
# 수학 문제 생성 함수
# -------------------
def generate_question(difficulty):
    level = difficulty_levels[difficulty]
    op = random.choice(level["ops"])
    rng = level["range"]

    if op == "/":
        b = random.randint(1, rng)
        a = b * random.randint(1, rng)
    else:
        a = random.randint(1, rng)
        b = random.randint(1, rng)

    question_text = f"{a} {op} {b}"
    answer = eval(question_text)
    if op == "/":
        answer = round(answer, 2)
    return question_text, answer

# -------------------
# 문제 리스트 생성 (10문제)
# -------------------
if not st.session_state.questions:
    for _ in range(10):
        q, a = generate_question(st.session_state.difficulty)
        st.session_state.questions.append({"question": q, "answer": a})

# -------------------
# 앱 제목
# -------------------
st.title("🎯 화려한 수학 문제 풀이 퀴즈 (10문제)")

# -------------------
# 시험 진행
# -------------------
if not st.session_state.finished:
    idx = st.session_state.current_index
    question = st.session_state.questions[idx]

    st.markdown(f"""
    <div style="background-color:#f0f8ff;padding:20px;border-radius:15px;box-shadow:3px 3px 10px rgba(0,0,0,0.2);">
        <h3 style="color:#003366;">문제 {idx+1} / 10</h3>
        <p style="font-size:24px;"><b>{question['question']} = ?</b></p>
    </div>
    """, unsafe_allow_html=True)

    # 사용자 답 입력
    user_answer = st.text_input("정답을 입력하세요:", key=f"input_{idx}")

    # 제출 버튼
    if st.button("제출"):
        if user_answer.strip() == "":
            st.warning("⚠️ 답을 입력해주세요!")
        else:
            try:
                user_answer_float = float(user_answer)
                is_correct = abs(user_answer_float - question["answer"]) < 1e-2
                if is_correct:
                    st.success("✅ 정답입니다!")
                    st.session_state.score += 1
                else:
                    st.error(f"❌ 오답! 정답: {question['answer']}")
                # 답안 기록
                st.session_state.answers.append({
                    "question": question["question"],
                    "your_answer": user_answer,
                    "correct_answer": question["answer"],
                    "correct": is_correct
                })
                # 다음 문제로 이동
                st.session_state.current_index += 1
                if st.session_state.current_index >= 10:
                    st.session_state.finished = True
            except ValueError:
                st.error("⚠️ 숫자만 입력해주세요.")

# -------------------
# 시험 종료 후 결과
# -------------------
if st.session_state.finished:
    st.markdown(f"""
    <div style="background-color:#e0ffe0;padding:20px;border-radius:15px;box-shadow:3px 3px 10px rgba(0,0,0,0.2);">
        <h2 style="color:#006600;">📊 시험 종료!</h2>
        <h3>최종 점수: {st.session_state.score} / 10</h3>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📖 틀린 문제 복습")
    for ans in st.session_state.answers:
        if not ans["correct"]:
            st.markdown(f"""
            <div style="background-color:#ffe0e0;padding:10px;border-radius:10px;margin-bottom:5px;">
            - 문제: **{ans['question']} = ?** → 당신의 답: {ans['your_answer']} ❌ | 정답: ✅ {ans['correct_answer']}
            </div>
            """, unsafe_allow_html=True)

    if st.button("다시 시작"):
        st.session_state.current_index = 0
        st.session_state.score = 0
        st.session_state.questions = []
        st.session_state.answers = []
        st.session_state.finished = False
