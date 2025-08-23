import streamlit as st
import random

# -------------------
# 앱 기본 설정
# -------------------
st.set_page_config(page_title="단어 맞추기 시험", page_icon="📝", layout="centered")

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
# 세션 상태 초기화
# -------------------
if "questions" not in st.session_state:     # 시험 문제 리스트
    st.session_state.questions = random.sample(default_words, 10)  # 10문제 랜덤 추출
if "current_q" not in st.session_state:     # 현재 문제 번호
    st.session_state.current_q = 0
if "score" not in st.session_state:         # 맞은 개수
    st.session_state.score = 0
if "finished" not in st.session_state:      # 시험 종료 여부
    st.session_state.finished = False

# -------------------
# 퀴즈 보기 생성 함수
# -------------------
def make_options(answer, all_words):
    """정답 + 랜덤 오답으로 보기 4개 생성"""
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
    # 현재 문제 가져오기
    q_index = st.session_state.current_q
    question = st.session_state.questions[q_index]

    st.subheader(f"문제 {q_index+1} / 10")
    st.write(f"영어 단어: **{question['word']}**")

    # 보기 생성
    options = make_options(question["meaning"], default_words)

    # 선택
    choice = st.radio("뜻을 고르세요:", options, index=None, key=f"q{q_index}")

    # 정답 확인 버튼
    if st.button("정답 제출"):
        if choice == question["meaning"]:
            st.session_state.score += 1
            st.success("✅ 정답입니다!")
        else:
            st.error(f"❌ 오답입니다! 정답: {question['meaning']}")

        # 다음 문제로 이동
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
    if st.session_state.score == 10:
        st.success("🎉 퍼펙트! 완벽하게 맞췄습니다!")
    elif st.session_state.score >= 7:
        st.info("👍 잘했어요! 조금 더 연습하면 완벽해요.")
    else:
        st.warning("📖 아직 연습이 필요합니다. 다시 도전해 보세요!")

    # 다시 시작 버튼
    if st.button("다시 시작"):
        st.session_state.questions = random.sample(default_words, 10)
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.finished = False
