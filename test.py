import streamlit as st
import random

# 기본 설정
st.set_page_config(page_title="안정화 수학 퀴즈", page_icon="🎯", layout="centered")

# 난이도 설정
difficulty_levels = {
    "쉬움": {"range": 10, "ops": ["+", "-"]},
    "보통": {"range": 20, "ops": ["+", "-", "*"]},
    "어려움": {"range": 50, "ops": ["+", "-", "*", "/"]}
}

# 세션 상태 초기화
for key in ["difficulty", "current_index", "score", "questions", "answers", "finished"]:
    if key not in st.session_state:
        if key == "questions" or key == "answers":
            st.session_state[key] = []
        elif key == "difficulty":
            st.session_state[key] = "보통"
        elif key == "finished":
            st.session_state[key] = False
        else:
            st.session_state[key] = 0

# 사이드바 난이도 선택
st.sidebar.title("⚙️ 난이도 설정")
st.session_state.difficulty = st.sidebar.radio(
    "난이도를 선택하세요:", ["쉬움", "보통", "어려움"]
)

# 문제 생성 함수
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

# 문제 리스트 10문제 생성 (한 번만)
if not st.session_state.questions:
    for _ in range(10):
        q, a = generate_question(st.session_state.difficulty)
        st.session_state.questions.append({"question": q, "answer": a})

# 앱 제목
st.title("🎯 안정화 수학 퀴즈 (10문제)")

# 시험 진행
if not st.session_state.finished:
    idx = st.session_state.current_index
    # 현재 인덱스 범위 확인
    if idx < len(st.session_state.questions):
        question = st.session_state.questions[idx]

        # 문제 카드 표시
        st.markdown(f"""
        <div style="background-color:#f0f8ff;padding:20px;border-radius:15px;box-shadow:3px 3px 10px rgba(0,0,0,0.2);">
            <h3 style="color:#003366;">문제 {idx+1} / 10</h3>
            <p style="font-size:24px;"><b>{question['question']} = ?</b></p>
        </div>
        """, unsafe_allow_html=True)

        # 사용자 입력
        user_answer = st.text_input("정답을 입력하세요:", key=f"input_{idx}")

        if st.button("제출"):
            if user_answer.strip() == "":
                st.warning("⚠️ 답을 입력해주세요!")
            else:
                try:
                    ua = float(user_answer)
                    correct = abs(ua - question["answer"]) < 1e-2
                    if correct:
                        st.success("✅ 정답입니다!")
                        st.session_state.score += 1
                    else:
                        st.error(f"❌ 오답! 정답: {question['answer']}")

                    st.session_state.answers.append({
                        "question": question["question"],
                        "your_answer": user_answer,
                        "correct_answer": question["answer"],
                        "correct": correct
                    })
                    st.session_state.current_index += 1
                    if st.session_state.current_index >= 10:
                        st.session_state.finished = True
                except ValueError:
                    st.error("⚠️ 숫자만 입력해주세요.")

# 시험 종료
if st.session_state.finished:
    st.subheader("📊 시험 종료!")
    st.write(f"최종 점수: {st.session_state.score} / 10")

    st.subheader("📖 틀린 문제 복습")
    for ans in st.session_state.answers:
        if not ans["correct"]:
            st.write(f"- 문제: {ans['question']} → 당신의 답: {ans['your_answer']} ❌ | 정답: ✅ {ans['correct_answer']}")

    if st.button("다시 시작"):
        st.session_state.current_index = 0
        st.session_state.score = 0
        st.session_state.questions = []
        st.session_state.answers = []
        st.session_state.finished = False
