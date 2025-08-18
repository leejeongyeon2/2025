import streamlit as st
import numpy as np
import plotly.graph_objects as go
from hashlib import sha256

st.set_page_config(page_title="연애 능력치 테스트", page_icon="💘")

st.title("💘 연애 능력치 테스트")
st.caption("각 문항을 1(전혀 아니다) ~ 5(매우 그렇다)로 선택하세요.")

CATS = ["매력", "센스", "재력", "집착", "인기도"]

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

name = st.text_input("닉네임을 입력하세요", value="")

if "answers" not in st.session_state:
    st.session_state.answers = [3] * len(questions)

for i, item in enumerate(questions):
    st.session_state.answers[i] = st.slider(
        item["q"], 1, 5, st.session_state.answers[i], key=f"q_{i}"
    )

def compute_scores(answers, questions):
    raw = {c: 0 for c in CATS}
    cnt = {c: 0 for c in CATS}
    for val, item in zip(answers, questions):
        raw[item["cat"]] += val
        cnt[item["cat"]] += 1
    scores = {}
    for c in CATS:
        avg = (raw[c] / cnt[c]) if cnt[c] else 0  # 1~5
        scores[c] = round((avg - 1) / 4 * 100)    # 0~100
    return scores

col1, col2 = st.columns(2)
show = col1.button("결과 보기 💘")
reset = col2.button("처음부터 다시하기 🔁")

if reset:
    st.session_state.answers = [3] * len(questions)
    st.rerun()

if show:
    scores = compute_scores(st.session_state.answers, questions)
    labels = list(scores.keys())
    values = list(scores.values())

    fig = go.Figure(
        data=go.Scatterpolar(
            r=values + [values[0]],
            theta=labels + [labels[0]],
            fill="toself",
            mode="lines+markers",
        )
    )
    fig.update_layout(
        polar=dict(radialaxis=dict(range=[0, 100])),
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20),
        title=f"{name or '익명'}님의 연애 능력치"
    )
    st.plotly_chart(fig, use_container_width=True)

    top_sorted = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    low_sorted = sorted(scores.items(), key=lambda x: x[1])
    top1, top2 = top_sorted[0], top_sorted[1]
    low1 = low_sorted[0]

    st.subheader("요약")
    st.write(f"강점: **{top1[0]}({top1[1]})**, {top2[0]}({top2[1]})")
    st.write(f"보완 포인트: **{low1[0]}({low1[1]})**")

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
streamlit>=1.35
plotly>=5.20
numpy
