import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="연애 능력치 테스트", page_icon="💘")

st.title("💘 연애 능력치 테스트 💘")
name = st.text_input("당신의 이름(닉네임)을 입력하세요:")

questions = [
    ("첫 만남에서 먼저 대화를 잘 이끈다", "매력"),
    ("상대방 농담에 리액션을 잘 해준다", "센스"),
    ("데이트 비용은 내가 주로 낸다", "재력"),
    ("연인에게 하루에 5번 이상 연락한다", "집착"),
    ("친구들 사이에서 인기가 많다", "인기도"),
]

scores = {"매력": 0, "센스": 0, "재력": 0, "집착": 0, "인기도": 0}

if name:
    st.subheader("질문에 답해주세요!")

    for q, category in questions:
        answer = st.radio(q, ["예", "아니오"], key=q)
        if answer == "예":
            scores[category] += random.randint(15, 25)
        else:
            scores[category] += random.randint(5, 15)

    if st.button("결과 보기 💘"):
        labels = list(scores.keys())
        values = list(scores.values())

        # 레이더 차트
        angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
        values += values[:1]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
        ax.plot(angles, values, "o-", linewidth=2)
        ax.fill(angles, values, alpha=0.25)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)
        ax.set_yticklabels([])
        st.pyplot(fig)

        # 결과 멘트
        comments = [
            "🔥 당신은 사랑의 불꽃 그 자체!",
            "😂 귀엽고 엉뚱한 매력이 있군요.",
            "💸 돈으로 밀고 나가는 스타일!",
            "📱 집착의 화신! 연애는 적당히~",
            "🌟 인기 폭발! 고백만 기다리면 됨!",
        ]
        st.success(f"{name}님의 연애 능력치 결과!\n\n👉 {random.choice(comments)}")

