import streamlit as st
import random

# -------------------
# 앱 기본 설정
# -------------------
st.set_page_config(
    page_title="화려한 수학 퀴즈",  # 브라우저 탭에 표시될 앱 이름
    page_icon="🎯",                 # 탭 아이콘
    layout="centered"               # 화면 중앙 배치
)

# -------------------
# 난이도별 설정
# -------------------
# 난이도에 따라 숫자 범위와 사용할 연산 선택
difficulty_levels = {
    "쉬움": {"range": 10, "ops": ["+", "-"]},
    "보통": {"range": 20, "ops": ["+", "-", "*"]},
    "어려움": {"range": 50, "ops": ["+", "-", "*", "/"]}
}

# -------------------
# 세션 상태 초기화
# -------------------
# Streamlit은 페이지가 새로고침될 때 변수가 초기화됨
# 세션 상태(st.session_state)를 이용해 앱 전체 상태 유지
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "보통"       # 기본 난이도 설정
if "current_index" not in st.session_state:
    st.session_state.current_index = 0         # 현재 문제 번호
if "score" not in st.session_state:
    st.session_state.score = 0                 # 맞힌 문제 수
if "questions" not in st.session_state:
    st.session_state.questions = []            # 문제 리스트 저장
if "answers" not in st.session_state:
    st.session_state.answers = []              # 사용자가 입력한 답 기록
if "finished" not in st.session_state:
    st.session_state.finished = False          # 시험 종료 여부

# -------------------
# 사이드바에서 난이도 선택
# -------------------
st.sidebar.title("⚙️ 난이도 설정")
st.session_state.difficulty = st.sidebar.radio(
    "난이도를 선택하세요:", ["쉬움", "보통", "어려움"]
)

# -------------------
# 수학 문제 생성 함수
# -------------------
def generate_question(difficulty):
    """
    난이도에 따라 수학 문제 생성
    쉬움: +, -
    보통: +, -, *
    어려움: +, -, *, /
    나눗셈은 항상 정수가 나오도록 계산
    """
    level = difficulty_levels[difficulty]
    op = random.choice(level["ops"])
    rng = level["range"]

    if op == "/":
        b = random.randint(1, rng)
        a = b * random.randint(1, rng)  # 나눗셈 결과가 정수
    else:
        a = random.randint(1, rng)
        b = random.randint(1, rng)

    question_text = f"{a} {op} {b}"
    answer = eval(question_text)         # 문제 계산
    if op == "/":
        answer = round(answer, 2)       # 나눗셈은 소수 둘째 자리까지
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
    idx = st.session_state.current_index                 # 현재 문제 번호
    question = st.session_state.questions[idx]          # 현재 문제 정보

    # 카드 형태로 문제 표시 (HTML + CSS)
    st.markdown(f"""
    <div style="background-color:#f0f8ff;padding:20px;border-radius:15px;box-shadow:3px 3px 10px rgba(0,0,0,0.2);">
        <h3 style="color:#003366;">문제 {idx+1} / 10</h3>
        <p style="font-size:24px;"><b>{question['question']} = ?</b></p>
    </div>
    """, unsafe_allow_html=True)

    # 사용자 답 입력
    user_answer = st.text_input("정답을 입력하세요:", key=f"input_{idx}")

    # 제출 버튼 클릭
    if st.button("제출"):
        if user_answer.strip() == "":
            st.warning("⚠️ 답을 입력해주세요!")  # 입력이 없으면 경고
        else:
            try:
                user_answer_float = float(user_answer)
                # 소수점 비교 (오차 0.01 허용)
                is_correct = abs(user_answer_float - question["answer"]) < 1e-2
                if is_correct:
                    st.success("✅ 정답입니다!")
                    st.session_state.score += 1        # 점수 증가
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
                st.error("⚠️ 숫자만 입력해주세요.")  # 숫자가 아닌 입력 처리

# -------------------
# 시험 종료 후 결과
# -------------------
if st.session_state.finished:
    # 점수 표시
    st.markdown(f"""
    <div style="background-color:#e0ffe0;padding:20px;border-radius:15px;box-shadow:3px 3px 10px rgba(0,0,0,0.2);">
        <h2 style="color:#006600;">📊 시험 종료!</h2>
        <h3>최종 점수: {st.session_state.score} / 10</h3>
    </div>
    """, unsafe_allow_html=True)

    # 틀린 문제 복습
    st.subheader("📖 틀린 문제 복습")
    for ans in st.session_state.answers:
        if not ans["correct"]:
            st.markdown(f"""
            <div style="background-color:#ffe0e0;padding:10px;border-radius:10px;margin-bottom:5px;">
            - 문제: **{ans['question']} = ?** → 당신의 답: {ans['your_answer']} ❌ | 정답: ✅ {ans['correct_answer']}
            </div>
            """, unsafe_allow_html=True)

    # 다시 시작 버튼
    if st.button("다시 시작"):
        st.session_state.current_index = 0
        st.session_state.score = 0
        st.session_state.questions = []
        st.session_state.answers = []
        st.session_state.finished = False
