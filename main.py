import streamlit as st

# 페이지 설정
st.set_page_config(page_title="MBTI 궁합 테스트", page_icon="💖", layout="centered")

# MBTI 궁합 데이터 (예시)
compatibility_data = {
    ("INTJ", "ENFP"): {"score": 95, "desc": "서로의 부족한 부분을 채워주는 완벽한 조합!"},
    ("ENFP", "INTJ"): {"score": 95, "desc": "서로의 장단점이 조화를 이루는 최고의 궁합!"},
    ("INFJ", "ENTP"): {"score": 90, "desc": "서로의 생각을 자극하며 성장하는 관계."},
    ("ENTP", "INFJ"): {"score": 90, "desc": "차분함과 활발함이 만나 좋은 시너지!"},
    ("ISTJ", "ESFP"): {"score": 88, "desc": "서로 다른 성격이 균형을 맞추는 관계."},
    ("ESFP", "ISTJ"): {"score": 88, "desc": "정반대의 성향이지만 서로에게 배울 점이 많아요."}
    # 필요하면 더 추가 가능
}

mbti_list = [
    "INTJ","INTP","ENTJ","ENTP",
    "INFJ","INFP","ENFJ","ENFP",
    "ISTJ","ISFJ","ESTJ","ESFJ",
    "ISTP","ISFP","ESTP","ESFP"
]

# 타이틀
st.markdown(
    """
    <h1 style="text-align:center; color:#E91E63;">💖 MBTI 궁합 테스트</h1>
    <p style="text-align:center; font-size:18px; color:#555;">
    두 사람의 MBTI를 선택하면 궁합 점수를 알려드립니다!
    </p>
    """,
    unsafe_allow_html=True
)

# MBTI 선택
col1, col2 = st.columns(2)
with col1:
    my_mbti = st.selectbox("당신의 MBTI", mbti_list)
with col2:
    partner_mbti = st.selectbox("상대방 MBTI", mbti_list)

# 궁합 결과
if st.button("궁합 보기 💌"):
    result = compatibility_data.get((my_mbti, partner_mbti))
    if result:
        score = result["score"]
        desc = result["desc"]
        st.markdown(
            f"""
            <div style='background-color:#fff0f5; padding:20px; border-radius:15px; text-align:center;'>
                <h2 style='color:#E91E63;'>궁합 점수: {score}점</h2>
                <p style='font-size:18px; color:#555;'>{desc}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style='background-color:#f0f8ff; padding:20px; border-radius:15px; text-align:center;'>
                <h2 style='color:#2E86C1;'>데이터 없음</h2>
                <p style='font-size:18px; color:#555;'>아직 등록되지 않은 궁합이에요. 😢</p>
            </div>
            """,
            unsafe_allow_html=True
        )

