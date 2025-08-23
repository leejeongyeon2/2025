import streamlit as st
import random  # 랜덤 문제 생성을 위해 필요

# -------------------
# 1. 앱 기본 설정
# -------------------
# 브라우저 탭 제목, 아이콘, 화면 레이아웃 중앙 배치
st.set_page_config(
    page_title="🎉 재미있는 수학 퀴즈",  # 브라우저 탭에 표시되는 제목
    page_icon="🧮",                      # 브라우저 탭 아이콘
    layout="centered"                    # 앱 화면을 중앙 정렬
)

# -------------------
# 2. 난이도 설정
# -------------------
# 난이도별 숫자 범위와 사용할 연산 정의
difficulty_levels = {
    "쉬움": {"range": 10, "ops": ["+", "-"]},      # 1~10 범위, 덧셈/뺄셈
    "보통": {"range": 20, "ops": ["+", "-", "*"]}, # 1~20 범위, 덧셈/뺄셈/곱셈
    "어려움": {"range": 50, "ops": ["+", "-", "*", "/"]} # 1~50 범위, 모든 연산
}

# -------------------
# 3. 세션 상태 초기화
# -------------------
# Streamlit은 페이지 새로고침 시 변수 초기화됨
# st.session_state를 사용하면 값 유지 가능
# KeyError 방지를 위해 모든 필요한 key를 미리 초기화
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "보통"  # 기본 난이도
if "current_index" not in st.session_state:
    st.session_state.current_index = 0    # 현재 문제 번호
if "score" not in st.session_state:
    st.session_state.score = 0            # 점수
if "questions" not in st.session_state:
    st.session_state.questions = []       # 문제 리스트 저장
if "answers" not in st.session_state:
    st.session_state.answers = []         # 사용자가 입력한 답 기록
if "submitted" not in st.session_state:
    st.session_state.submitted = False    # 제출 상태 (제출 후 다음 버튼 활성화 여부)
if "finished" not in st.session_state:
    st.session_state.finished = False     # 시험 종료 여부

# -------------------
# 4. 사이드바 난이도 선택
# -------------------
# 사용자가 난이도를 선택할 수 있는 사이드바
st.sidebar.title("⚙️ 난이도 설정")
st.session_state.difficulty = st.sidebar.radio(
    "난이도를 선택하세요:", ["쉬움", "보통", "어려움"]
)

# -------------------
# 5. 수학 문제 생성 함수
# -------------------
def generate_question(difficulty):
    """
    난이도별 랜덤 수학 문제 생성
    '/' 연산은 항상 정수 결과가 나오도록 처리
    반환: 문제 문자열, 정답
    """
    level = difficulty_levels[difficulty]  # 선택된 난이도 설정
    op = random.choice(level["ops"])       # 연산 선택
    rng = level["range"]                   # 숫자 범위

    # 나눗셈은 항상 정수가 나오도록 계산
    if op == "/":
        b = random.randint(1, rng)
        a = b * random.randint(1, rng)
    else:  # 나머지 연산
        a = random.randint(1, rng)
        b = random.randint(1, rng)

    question_text = f"{a} {op} {b}"       # 문제 문자열 생성
    answer = eval(question_text)           # 문제 계산
    if op == "/":
        answer = round(answer, 2)         # 소수 둘째 자리까지 반올림
    return question_text, answer

# -------------------
# 6. 문제 리스트 생성 (10문제)
# -------------------
# 앱 시작 시 문제 리스트가 없으면 10문제 생성
if not st.session_state.questions:
    for _ in range(10):
        q, a = generate_question(st.session_state.difficulty)
        st.session_state.questions.append({"question": q, "answer": a})

# -------------------
# 7. 앱 제목 표시
# -------------------
# HTML + CSS + 이모티콘 사용
st.markdown("""
<div style="text-align:center;">
    <h1>🧮🎉 재미있는 수학 퀴즈 🏆</h1>
    <p>총 10문제! 정답을 맞히고 점수를 올려보세요!</p>
</div>
""", unsafe_allow_html=True)

# -------------------
# 8. 시험 진행
# -------------------
if not st.session_state.finished:  # 시험이 끝나지 않은 경우
    idx = st.session_state.current_index  # 현재 문제 번호
    # KeyError 방지를 위해 현재 인덱스가 문제 리스트 범위 내인지 확인
    if 0 <= idx < len(st.session_state.questions):
        question = st.session_state.questions[idx]

        # -------------------
        # 8-1. 문제 카드 표시
        # -------------------
        st.markdown(f"""
        <div style="
            background-color:#e0f7fa;
            padding:20px;
            border-radius:15px;
            box-shadow:4px 4px 12px rgba(0,0,0,0.2);
            margin-bottom:10px;">
            <h3 style="color:#00796b;">문제 {idx+1} / 10 🧩</h3>
            <p style="font-size:24px;"><b>{question['question']} = ?</b></p>
        </div>
        """, unsafe_allow_html=True)

        # -------------------
        # 8-2. 사용자 답 입력
        # -------------------
        # 문제마다 고유 key 지정
        user_answer = st.text_input("✏️ 정답을 입력하세요:", key=f"input_{idx}")

        # -------------------
        # 8-3. 제출 버튼
        # -------------------
        # 이미 제출한 경우 중복 방지
        if not st.session_state.submitted:
            if st.button("✅ 제출"):
                if user_answer.strip() == "":
                    st.warning("⚠️ 답을 입력해주세요!")  # 입력 없으면 경고
                else:
                    try:
                        ua = float(user_answer)  # 입력값 숫자 변환
                        correct = abs(ua - question["answer"]) < 1e-2  # 소수 비교
                        if correct:
                            st.success("🎉 정답입니다!")  # 정답 표시
                            st.session_state.score += 1  # 점수 증가
                        else:
                            st.error(f"❌ 오답! 정답: {question['answer']}")  # 오답 표시

                        # 답안 기록
                        st.session_state.answers.append({
                            "question": question["question"],  # 문제
                            "your_answer": user_answer,       # 사용자 답
                            "correct_answer": question["answer"], # 정답
                            "correct": correct                # 정답 여부
                        })
                        st.session_state.submitted = True  # 제출 완료 표시
                    except ValueError:
                        st.error("⚠️ 숫자만 입력해주세요.")  # 숫자 외 입력 처리

        # -------------------
        # 8-4. 다음 문제 버튼
        # -------------------
        # 제출 완료 후에만 표시
        if st.session_state.submitted:
            if st.button("➡️ 다음 문제"):
                st.session_state.current_index += 1   # 다음 문제로 이동
                st.session_state.submitted = False    # 제출 상태 초기화
                if st.session_state.current_index >= 10:
                    st.session_state.finished = True    # 10문제 완료 시 시험 종료

# -------------------
# 9. 시험 종료 후 결과
# -------------------
if st.session_state.finished:
    # 최종 점수 카드
    st.markdown(f"""
    <div style="
        background-color:#dcedc8;
        padding:20px;
        border-radius:15px;
        box-shadow:4px 4px 12px rgba(0,0,0,0.2);">
        <h2 style="color:#33691e;">🏆 시험 종료!</h2>
        <h3>총 점수: {st.session_state.score} / 10 🎯</h3>
    </div>
    """, unsafe_allow_html=True)

    # 틀린 문제 복습
    st.subheader("📖 틀린 문제 복습")
    for ans in st.session_state.answers:
        if not ans["correct"]:
            st.markdown(f"""
            <div style="
                background-color:#ffcdd2;
                padding:10px;
                border-radius:10px;
                margin-bottom:5px;">
                - 문제: **{ans['question']} = ?** → 당신의 답: {ans['your_answer']} ❌ | 정답: ✅ {ans['correct_answer']}
            </div>
            """, unsafe_allow_html=True)

    # -------------------
    # 9-1. 다시 시작 버튼
    # -------------------
    if st.button("🔄 다시 시작"):
        # 세션 상태 초기화
        st.session_state.current_index = 0
        st.session_state.score = 0
        st.session_state.questions = []
        st.session_state.answers = []
        st.session_state.submitted = False
        st.session_state.finished = False
