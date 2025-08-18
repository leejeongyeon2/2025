import streamlit as st
import numpy as np
from hashlib import sha256
import pandas as pd

# 앱 기본 설정 (타이틀/아이콘)
st.set_page_config(page_title="💘 연애 능력치 테스트 💘", page_icon="💖")

# 🌟 메인 타이틀 출력
st.markdown("<h1 style='text-align:center;'>💖 연애 능력치 테스트 💖</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>✨ 나의 연애 능력치를 확인해보세요! ✨</p>", unsafe_allow_html=True)

# 능력치 카테고리 정의
CATS = ["💎 매력", "🎭 센스", "💰 재력", "📱 집착", "🌟 인기도"]

# 질문 리스트 (각 질문은 어떤 카테고리에 속하는지 함께 저장)
questions = [
    {"q": "👗 첫 만남에서 외모/패션에 신경을 쓴다", "cat": "💎 매력"},
    {"q": "😏 자신만의 매력 포인트(유머, 분위기 등)가 있다", "cat": "💎 매력"},
    {"q": "💬 자신감 있게 말하는 편이다", "cat": "💎 매력"},
    {"q": "👀 호감 있는 사람에게 눈을 잘 맞춘다", "cat": "💎 매력"},

    {"q": "👂 상대방의 기분 변화를 잘 눈치챈다", "cat": "🎭 센스"},
    {"q": "😂 대화 중 적절한 농담을 잘 던진다", "cat": "🎭 센스"},
    {"q": "🎁 선물 고르는 센스가 있다는 말을 자주 듣는다", "cat": "🎭 센스"},
    {"q": "🤲 말보다 행동으로 챙겨주는 편이다", "cat": "🎭 센스"},

    {"q": "🍽️ 데이트 비용을 무리 없이 감당할 수 있다", "cat": "💰 재력"},
    {"q": "💳 상대방에게 여유 있어 보인다는 말을 듣는다", "cat": "💰 재력"},
    {"q": "📊 돈 관리(저축, 소비)를 잘 하는 편이다", "cat": "💰 재력"},
    {"q": "🎉 기념일에 이벤트/선물을 아끼지 않는다", "cat": "💰 재력"},

    {"q": "📞 연인에게 하루에 여러 번 연락해야 안심된다", "cat": "📱 집착"},
    {"q": "🔍 상대방의 SNS 활동을 자주 확인한다", "cat": "📱 집착"},
    {"q": "😠 연인이 친구와 더 많은 시간을 보내면 신경 쓰인다", "cat": "📱 집착"},
    {"q": "⌛ 사소한 연락 지연에도 불안해하는 편이다", "cat": "📱 집착"},

    {"q": "👋 처음 보는 사람과도 금방 친해진다", "cat": "🌟 인기도"},
    {"q": "🥳 친구들 사이에서 주목받는 편이다", "cat": "🌟 인기도"},
    {"q": "😍 여러 사람에게 호감을 받는다고 느낀 적 있다", "cat": "🌟 인기도"},
    {"q": "💌 소개팅 제안을 자주 받는다", "cat": "🌟 인기도"},
]

# 사용자 닉네임 입력
name = st.text_input("✍️ 닉네임을 입력하세요", value="")

# 세션 상태 초기화 (질문 개수가 바뀌면 다시 초기화됨)
if "answers" not in st.session_state or len(st.session_state.answers) != len(questions):
    st.session_state.answers = [3] * len(questions)  # 기본값 3(보통)으로 설정

# 문항 출력 (슬라이더로 답변)
st.subheader("✨ 질문에 답해주세요 ✨")
for i, item in enumerate(questions):
    st.session_state.answers[i] = st.slider(
        item["q"], 1, 5, st.session_state.answers[i], key=f"q_{i}"
    )

# 점수 계산 함수
def compute_scores(answers, questions):
    raw = {c: 0 for c in CATS}  # 카테고리별 점수 합
    cnt = {c: 0 for c in CATS}  # 카테고리별 질문 개수
    for val, item in zip(answers, questions):
        raw[item["cat"]] += val
        cnt[item["cat"]] += 1
    scores = {}
    for c in CATS:
        avg = (raw[c] / cnt[c]) if cnt[c] else 0
        scores[c] = round((avg - 1) / 4 * 100)  # 1~5 점수를 0~100으로 환산
    return scores

# 버튼 2개 (결과 보기, 리셋)
col1, col2 = st.columns(2)
show = col1.button("💘 결과 보기 💘")
reset = col2.button("🔄 처음부터 다시하기")

# 리셋 버튼 눌렀을 때
if reset:
    st.session_state.answers = [3] * len(questions)
    st.rerun()  # 페이지 새로고침

# 결과 보기 버튼 눌렀을 때
if show:
    scores = compute_scores(st.session_state.answers, questions)  # 점수 계산

    # 📊 시각화 (바 차트)
    df = pd.DataFrame({
        "능력치": list(scores.keys()),
        "점수": list(scores.values())
    }).set_index("능력치")

    st.markdown("### 📊 나의 연애 능력치 그래프")
    st.bar_chart(df)  # bar chart 출력

    # 결과 요약 (가장 높은 점수 2개 + 가장 낮은 점수 1개)
    top_sorted = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    low_sorted = sorted(scores.items(), key=lambda x: x[1])
    top1, top2 = top_sorted[0], top_sorted[1]
    low1 = low_sorted[0]

    st.subheader("🌈 결과 요약")
    st.write(f"💖 강점: **{top1[0]}({top1[1]}점)**, **{top2[0]}({top2[1]}점)**")
    st.write(f"💔 보완 포인트: **{low1[0]}({low1[1]}점)**")

    # 총평 (항상 같은 답변이면 같은 멘트 나오도록 sha256 사용)
    seed_str = f"{name}-{st.session_state.answers}"
    idx = int(sha256(seed_str.encode()).hexdigest(), 16) % 5
    comments = [
        "🔥 불꽃 카리스마! 사랑 앞에서는 누구도 못 막아요!",
        "😎 능글미 장착. 당신은 연애의 마스터!",
        "💸 현실적이고 든든한 타입. 함께라면 든든!",
        "📱 애정 폭발형! 하지만 숨 쉴 공간도 주세요 💕",
        "🌟 어디서든 빛나는 인기인! 고백만 기다리면 끝!",
    ]
    st.success(f"✨ {name or '익명'}님의 총평 ✨\n\n{comments[idx]}")

    # 💞 이름 궁합 기능 추가
    st.markdown("---")
    st.subheader("💞 이름 궁합 테스트")

    partner = st.text_input("💕 궁합을 보고 싶은 사람의 이름을 입력하세요", value="")

    if partner:
        # 닉네임 + 상대 이름을 해시로 변환 → 0~100 점수 생성
        seed_str = f"{name}-{partner}"
        comp_score = int(sha256(seed_str.encode()).hexdigest(), 16) % 101  
        st.write(f"✨ {name} 💖 {partner} ✨ 의 궁합 점수는...")
        st.markdown(f"<h2 style='text-align:center;'>💘 {comp_score}% 💘</h2>", unsafe_allow_html=True)

        # 점수별 멘트
        if comp_score >= 80:
            msg = "천생연분 ✨ 두 분은 운명 그 자체예요!"
        elif comp_score >= 60:
            msg = "좋은 케미 💕 노력하면 연애 성공!"
        elif comp_score >= 40:
            msg = "그럭저럭 😅 서로 이해가 필요해요"
        else:
            msg = "😢 애매한 인연... 하지만 친구로는 딱 좋아요!"
        
        st.success(msg)

else:
    st.info("👉 모든 문항을 선택한 뒤 **결과 보기 💘**를 눌러주세요!")
