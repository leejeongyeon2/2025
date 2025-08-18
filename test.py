import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from hashlib import sha256

# 페이지 설정
st.set_page_config(page_title="연애 능력치 테스트", page_icon="💘")

st.title("💘 연애 능력치 테스트")
st.caption("각 문항을 1(전혀 아니다) ~ 5(매우 그렇다)로 선택하세요.")

# 카테고리
CATS = ["매력", "센스", "재력", "집착", "인기도"]

# 질문 목록 (카테고리 매핑)
questions = [
    {"q": "첫 만남에서 먼저 대화를 잘 이끈다", "cat": "매력"},
    {"q": "상대방의 농담에 리액션을 잘 해준다", "cat": "센스"},
    {"q": "데이트 비용 부담에 여유가 있다", "cat": "재력"},
    {"q": "연인에게 자주 연락하는 편이다", "cat": "집착"},
    {"q": "친구들 사이에서 인기가 많은 편이다", "cat": "인기도"},
    {"q": "상대방 기념일/이벤트를 잘 챙긴다", "cat": "센스"},
    {"q": "외모/패션에 시간을 투자한다", "cat": "매력"},
    {"q": "금전 문제를 무리 없이 조율한다", "cat": "재력"},
    {"q": "SNS에서 연애 티(표시)를 자주 낸다", "cat": "집착"},
    {"q": "새로운 사람과 쉽게 친해진다", "cat": "인기도"},
]

# 닉네임
name = st.text_input("닉네임을 입력하세요", value="")

# 초기 상태값
if "answers" not in st.session_state:
    st.session_state.answers = [3] * len(questions)  # 기본값 3(보통)

# 문항 입력 UI
for i, item in enumerate(questions):
    st.session_state.answers[i] = st.slider(
        item["q"], 1, 5, st.session_state.answers[i], key=f"q_{i}"
    )

def compute_scores(answers, questions):
    """슬라이더(1~5)를 카테고리별 평균(1~5)로 만들고 → 0~100으로 스케일링."""
    raw = {c: 0 for c in CATS}
    cnt = {c: 0 for c in CATS}
    for val, item in zip(answers, questions):
        raw[item["cat"]] += val
        cnt[item["cat"]] += 1

    scores = {}
    for c in CATS:
        if cnt[c] == 0:
            scores[c] = 0
        else:
            avg = raw[c] / cnt[c]          # 1 ~ 5
            scores[c] = round((avg - 1) / 4 * 100)  # 0 ~ 100
    return scores

def radar_chart(scores, title):
    labels = list(scores.keys())
    values = list(scores.values())
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
    angles_cycle = angles.tolist() + [angles[0]]
    values_cycle = values + [values[0]]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles_cycle, values_cycle, linewidth=2)
