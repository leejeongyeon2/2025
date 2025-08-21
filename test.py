import streamlit as st
import numpy as np
import pandas as pd
from hashlib import sha256

# ============================================
# 🎯 앱 기본 설정
# ============================================
# 앱의 전반적인 설정: 제목, 아이콘, 페이지 기본값을 설정한다.
# 이 부분은 앱 실행 시 가장 먼저 호출되어 Streamlit 앱의 기본 환경을 결정한다.
st.set_page_config(page_title="💘 연애 능력치 테스트 💘", page_icon="💖")

# ============================================
# 📌 상수 정의
# ============================================
# 앱에서 반복적으로 사용될 상수 데이터들을 미리 정의한다.
# CATS: 능력치 카테고리
# QUESTIONS: 질문 리스트 (카테고리별 질문)
# COMMENTS: 결과 총평 메시지
# LOVE_TYPES: 이름 궁합 풀이 메시지
CATS = ["💎 매력", "🎭 센스", "💰 재력", "📱 집착", "🌟 인기도"]

QUESTIONS = [
    # 매력 관련 질문
    {"q": "👗 첫 만남에서 외모/패션에 신경을 쓴다", "cat": "💎 매력"},
    {"q": "😏 자신만의 매력 포인트(유머, 분위기 등)가 있다", "cat": "💎 매력"},
    {"q": "💬 자신감 있게 말하는 편이다", "cat": "💎 매력"},
    {"q": "👀 호감 있는 사람에게 눈을 잘 맞춘다", "cat": "💎 매력"},

    # 센스 관련 질문
    {"q": "👂 상대방의 기분 변화를 잘 눈치챈다", "cat": "🎭 센스"},
    {"q": "😂 대화 중 적절한 농담을 잘 던진다", "cat": "🎭 센스"},
    {"q": "🎁 선물 고르는 센스가 있다는 말을 자주 듣는다", "cat": "🎭 센스"},
    {"q": "🤲 말보다 행동으로 챙겨주는 편이다", "cat": "🎭 센스"},

    # 재력 관련 질문
    {"q": "🍽️ 데이트 비용을 무리 없이 감당할 수 있다", "cat": "💰 재력"},
    {"q": "💳 상대방에게 여유 있어 보인다는 말을 듣는다", "cat": "💰 재력"},
    {"q": "📊 돈 관리(저축, 소비)를 잘 하는 편이다", "cat": "💰 재력"},
    {"q": "🎉 기념일에 이벤트/선물을 아끼지 않는다", "cat": "💰 재력"},

    # 집착 관련 질문
    {"q": "📞 연인에게 하루에 여러 번 연락해야 안심된다", "cat": "📱 집착"},
    {"q": "🔍 상대방의 SNS 활동을 자주 확인한다", "cat": "📱 집착"},
    {"q": "😠 연인이 친구와 더 많은 시간을 보내면 신경 쓰인다", "cat": "📱 집착"},
    {"q": "⌛ 사소한 연락 지연에도 불안해하는 편이다", "cat": "📱 집착"},

    # 인기도 관련 질문
    {"q": "👋 처음 보는 사람과도 금방 친해진다", "cat": "🌟 인기도"},
    {"q": "🥳 친구들 사이에서 주목받는 편이다", "cat": "🌟 인기도"},
    {"q": "😍 여러 사람에게 호감을 받는다고 느낀 적 있다", "cat": "🌟 인기도"},
    {"q": "💌 소개팅 제안을 자주 받는다", "cat": "🌟 인기도"},
]

COMMENTS = [
    "🔥 불꽃 카리스마! 사랑 앞에서는 누구도 못 막아요!",
    "😎 능글미 장착. 당신은 연애의 마스터!",
    "💸 현실적이고 든든한 타입. 함께라면 든든!",
    "📱 애정 폭발형! 하지만 숨 쉴 공간도 주세요 💕",
    "🌟 어디서든 빛나는 인기인! 고백만 기다리면 끝!",
]

LOVE_TYPES = [
    "🔥 불꽃 같은 사랑 (열정 가득!)",
    "🌊 잔잔한 파도 같은 사랑 (평화롭고 안정적)",
    "🌱 새싹 같은 사랑 (풋풋하고 설레는 관계)",
    "🌙 운명적인 사랑 (만날 수밖에 없는 인연)",
    "🍀 친구 같은 사랑 (편안하고 든든해요)",
]

# ============================================
# 📌 유틸 함수 정의
# ============================================

def compute_scores(answers, questions):
    """
    각 질문의 답변(answers)과 질문 리스트(questions)를 바탕으로
    카테고리별 점수를 계산한다.
    점수는 1~5 범위를 0~100으로 변환하여 출력한다.
    """
    raw = {c: 0 for c in CATS}  # 각 카테고리별 점수 합산용 딕셔너리
    cnt = {c: 0 for c in CATS}  # 각 카테고리별 질문 개수 기록

    # 각 질문의 답변 점수를 카테고리별로 합산
    for val, item in zip(answers, questions):
        raw[item["cat"]] += val
        cnt[item["cat"]] += 1

    # 평균을 구하고 0~100 점수로 변환
    scores = {}
    for c in CATS:
        avg = (raw[c] / cnt[c]) if cnt[c] else 0
        scores[c] = round((avg - 1) / 4 * 100)  # 1~5 점수 → 0~100 변환 공식
    return scores


def render_questions(questions):
    """
    Streamlit UI에 모든 질문을 출력한다.
    각 질문은 슬라이더로 표시되며, 1~5 사이에서 사용자가 선택.
    사용자가 선택한 모든 답변은 리스트로 반환된다.
    """
    st.subheader("✨ 질문에 답해주세요 ✨")
    answers = []
    for i, item in enumerate(questions):
        ans = st.slider(item["q"], 1, 5, 3, key=f"q_{i}")  # 기본값은 3(중간값)
        answers.append(ans)
    return answers


def show_results(name, answers):
    """
    사용자의 답변을 토대로 능력치를 계산하고 시각화.
    - 능력치 그래프 출력
    - 강점/약점 요약
    - 랜덤 총평 메시지 출력
    """
    scores = compute_scores(answers, QUESTIONS)

    # 📊 카테고리별 점수를 그래프로 시각화
    df = pd.DataFrame({"능력치": list(scores.keys()), "점수": list(scores.values())}).set_index("능력치")
    st.markdown("### 📊 나의 연애 능력치 그래프")
    st.bar_chart(df)

    # 🌈 결과 요약: 상위 2개, 최하위 1개 능력치 표시
    top_sorted = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    low_sorted = sorted(scores.items(), key=lambda x: x[1])
    top1, top2 = top_sorted[0], top_sorted[1]
    low1 = low_sorted[0]

    st.subheader("🌈 결과 요약")
    st.write(f"💖 강점: **{top1[0]}({top1[1]}점)**, **{top2[0]}({top2[1]}점)**")
    st.write(f"💔 보완 포인트: **{low1[0]}({low1[1]}점)**")

    # 총평 메시지: 이름과 답변 기반 해시값을 이용해 랜덤하게 선택
    seed_str = f"{name}-{answers}"
    idx = int(sha256(seed_str.encode()).hexdigest(), 16) % len(COMMENTS)
    st.success(f"✨ {name or '익명'}님의 총평 ✨\n\n{COMMENTS[idx]}")


def show_compatibility(name, partner):
    """
    이름을 입력받아 두 사람의 궁합을 계산하고 결과를 출력.
    - 궁합 점수 (0~100)
    - 점수별 해석 메시지
    - 이름 풀이 기반 사랑 타입
    """
    seed_str = f"{name}-{partner}"
    comp_score = int(sha256(seed_str.encode()).hexdigest(), 16) % 101

    st.markdown("---")
    st.subheader("💞 이름 궁합 테스트")

    st.write(f"✨ {name} 💖 {partner} ✨ 의 궁합 점수는...")
    st.markdown(f"<h2 style='text-align:center;'>💘 {comp_score}% 💘</h2>", unsafe_allow_html=True)

    # 점수 범위별 메시지 출력
    if comp_score >= 80:
        msg = "천생연분 ✨ 두 분은 운명 그 자체예요!"
    elif comp_score >= 60:
        msg = "좋은 케미 💕 노력하면 연애 성공!"
    elif comp_score >= 40:
        msg = "그럭저럭 😅 서로 이해가 필요해요"
    else:
        msg = "😢 애매한 인연... 하지만 친구로는 딱 좋아요!"
    st.success(msg)

    # 이름의 글자 코드 합을 기반으로 사랑 타입 결정
    type_seed = sum(ord(ch) for ch in (name + partner))
    love_type = LOVE_TYPES[type_seed % len(LOVE_TYPES)]
    st.markdown("### 🔮 이름 궁합 풀이")
    st.info(love_type)

# ============================================
# 📌 메인 실행 함수
# ============================================

def main():
    """
    앱의 전체 실행 흐름을 제어하는 메인 함수.
    1. 닉네임 입력
    2. 질문 출력 및 답변 수집
    3. 결과 출력 및 이름 궁합 확인
    """
    # 앱 제목 및 설명 출력
    st.markdown("<h1 style='text-align:center;'>💖 연애 능력치 테스트 💖</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>✨ 나의 연애 능력치 & 이름 궁합을 확인해보세요 ✨</p>", unsafe_allow_html=True)

    # 사용자 닉네임 입력
    name = st.text_input("✍️ 닉네임을 입력하세요", value="")

    # 질문 출력 및 답변 수집
    answers = render_questions(QUESTIONS)

    # 결과 보기 & 초기화 버튼
    col1, col2 = st.columns(2)
    show = col1.button("💘 결과 보기 💘")
    reset = col2.button("🔄 처음부터 다시하기")

    if reset:
        st.rerun()  # 페이지 리셋

    # 결과 출력
    if show:
        show_results(name, answers)

        # 이름 궁합 확인
        partner = st.text_input("💕 궁합을 보고 싶은 사람의 이름을 입력하세요", value="")
        if partner:
            show_compatibility(name, partner)
    else:
        st.info("👉 모든 문항을 선택한 뒤 **결과 보기 💘**를 눌러주세요!")

# ============================================
# 📌 실행 진입점
# ============================================
if __name__ == "__main__":
    main()
