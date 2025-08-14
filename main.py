import streamlit as st

# 페이지 설정
st.set_page_config(page_title="MBTI 직업 추천기", page_icon="💡", layout="wide")

# MBTI별 추천 직업 + 이미지
mbti_jobs = {
    "INTJ": {
        "jobs": ["전략 컨설턴트", "데이터 과학자", "연구원"],
        "img": "https://images.unsplash.com/photo-1581091012184-5c05f1f7f885"
    },
    "ENFP": {
        "jobs": ["광고 기획자", "탐험가", "콘텐츠 크리에이터"],
        "img": "https://images.unsplash.com/photo-1522202222190-dc93d7b5f3ae"
    },
    "INFJ": {
        "jobs": ["심리상담가", "작가", "교육 전문가"],
        "img": "https://images.unsplash.com/photo-1507842217343-583bb7270b66"
    },
    "ISTP": {
        "jobs": ["엔지니어", "파일럿", "응급 구조원"],
        "img": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d"
    },
    # 필요 시 나머지 MBTI도 추가 가능
}

st.markdown(
    """
    <h1 style="text-align:center; color:#4CAF50;">💡 MBTI 기반 직업 추천기</h1>
    <p style="text-align:center; font-size:18px;">당신의 MBTI를 선택하면 어울리는 직업과 이미지를 추천해드립니다!</p>
    """,
    unsafe_allow_html=True
)

# MBTI 선택
selected_mbti = st.selectbox("MBTI를 선택하세요", list(mbti_jobs.keys()))

if selected_mbti:
    data = mbti_jobs[selected_mbti]
    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(data["img"], caption=f"{selected_mbti} 추천 분위기 이미지", use_container_width=True)

    with col2:
        st.markdown(f"## 📌 {selected_mbti} 유형 추천 직업")
        for job in data["jobs"]:
            st.markdown(
                f"""
                <div style='background-color:#f0f8ff; padding:15px; border-radius:10px; margin-bottom:10px;'>
                    <b style='color:#2E86C1;'>✅ {job}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

