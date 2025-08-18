import streamlit as st
import numpy as np
from hashlib import sha256
import pandas as pd

st.set_page_config(page_title="연애 능력치 테스트", page_icon="💘")

st.title("💘 연애 능력치 테스트")
st.caption("각 문항을 1(전혀 아니다) ~ 5(매우 그렇다)로 선택하세요.")

# 카테고리
CATS = ["매력", "센스", "재력", "집착", "인기도"]

# 확장된 질문 세트 (각 카테고리 4문항씩 총 20문항)
questions = [
    # 매력
    {"q": "첫 만남에서 외모/패션에 신경을 쓴다", "cat": "매력"},
    {"q": "자신만의 매력 포인트(예: 유머, 분위기)가 있다", "cat": "매력"},
    {"q": "자신감 있게 말하는 편이다", "cat": "매력"},
    {"q": "호감 있는 사람에게 눈을 잘 맞춘다", "cat": "매력"},
    
    # 센스
    {"q": "상대방의 기분 변화를 잘 눈치챈다", "cat": "센스"},
    {"q": "대화 중 적절한 농담을 잘 던진다", "cat": "센스"},
    {"q": "선물 고르는 센스가 있다는 말을 자주 듣는다", "cat": "센스"},
    {"q": "말보다 행동으로 챙겨주는 편이다", "cat": "센스"},
    
    # 재력
    {"q": "데이트 비용을 무리 없이 감당할 수 있다", "cat": "재력"},
    {"q": "상대방에게 금전적으로 여유 있어 보인다는 말을 듣는다", "cat": "재력"},
    {"q": "돈 관리(저축, 소비)를 잘 하는 편이다", "cat": "재력"},
    {"q": "기념일에 이벤트/선물을 아끼지 않는다", "cat": "재력"},
    
    # 집착
    {"q": "연인에게 하루에 여러 번 연락해야 안심된다", "cat": "집착"},
    {"q": "상대방의 SNS 활동을 자주 확인한다", "cat": "집착"},
    {"q": "연인이 나보다 친구와 시간을 많이 보내면 신경 쓰인다", "cat": "집착"},
    {"q": "사소한 연락 지연에도 불안해하는 편이다", "cat": "집착"},
    
    # 인기도
    {"q": "처음 보는 사람과도 금방 친해진다", "cat": "인기도"},
    {"q": "친구/지인들 사이에서 주목받는 편이다", "cat": "인기도"},
    {"q": "여러 사람에게 호감을 받는다고 느낀 적이 있다", "cat": "인기도"},
    {"q": "주변에서 소개팅 제안을 자주 받는다", "cat": "인기도"},
]

# 닉네임 입력
name = st.text_input("닉네임을 입력하세요", value="")

# ✅ 세션 상태 초기화 (질문 개수 달라지면 자동 리셋)
if "answers" not in st.session_state or len(st.session_state.answers) != len(questions):
    st.session_state.answers = [3] * len(questions)

# 문항 입력 UI
for i, item in enumerate(questions):
    st.session_state.answers[i] = st.slider(
        item["q"], 1, 5, st.session_state.answers[i], key=f"q_{i}"
    )

# 점수 계산 함수
def compute_scores(answers, questions):
    raw = {c: 0 for c in CATS}
    cnt = {c: 0 for c in CATS}
    for val, item in zip(answers, questions):
        raw[item["cat"]] += val
        cnt[item["cat"]] += 1
    scores = {}
    for c in CATS:
        avg = (raw[c] / cnt[c]) if cnt[c] else 0
        scores[c] = round((avg - 1) / 4 * 100)  # 0~100
    return scores

# 버튼
col1, col2 = st.columns(2)
show = col1.button("결과 보기 💘")
reset = col2.button("처음부터 다시하기 🔁")

if reset:
    st.session_state.answers = [3] * len(questions)
    st.rerun()

if show:
    scores = compute_scores(st.session_state.answers, questions)

    # 📊 시각화 (바 차트)
    df = pd.DataFrame({
        "능력치": list(scores.keys()),
        "점수": list(scores.values())
    }).set_index("능력치")

    st.bar_chart(df)

    # 결과 요약
    top_sorted = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    low_sorted = sorted(scores.items(), key=lambda x: x[1])
    top1, top2 = top_sorted[0], top_sorted[1]
    low1 = low_sorted[0]

    st.subheader("요약")
    st.write(f"강점: **{top1[0]}({top1[1]})**, {top2[0]}({top2[1]})")
    st.write(f"보완 포인트: **{low1[0]}({low1[1]})**")

    # 총평 (항상 같은 입력이면 같은 멘트 나오도록)
    seed_str = f"{name}-{st.session_state.answers}"
    idx = int(sha256(seed_str.encode()).hexdigest(), 16) % 5
    comments = [
        "🔥 불꽃 카리스마! 썸은 이미 연애.",
        "😎 능글미 장착. 사람 끌어당기는 자석.",
        "💸 현실적이고 든든한 타입. 의지됨!",
        "📱 애정표현 과다 주의. 숨도 쉬어가요!",
        "🌟 어디서든 빛나는 인기인!",
    ]
    st.success(f"{name or '익명'}님 총평: {comments[idx]}")
else:
    st.info("모든 문항을 선택한 뒤 **결과 보기**를 눌러보세요.")
