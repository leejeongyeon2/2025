import streamlit as st

# MBTI별 추천 직업 데이터
mbti_jobs = {
    "INTJ": ["전략 컨설턴트", "데이터 과학자", "연구원"],
    "INTP": ["소프트웨어 개발자", "이론 물리학자", "UX 디자이너"],
    "ENTJ": ["기업 경영자", "프로젝트 매니저", "변호사"],
    "ENTP": ["창업가", "마케팅 전문가", "언론인"],
    "INFJ": ["심리상담가", "작가", "교육 전문가"],
    "INFP": ["예술가", "작사가", "사회복지사"],
    "ENFJ": ["교사", "인사담당자", "홍보 전문가"],
    "ENFP": ["광고 기획자", "탐험가", "콘텐츠 크리에이터"],
    "ISTJ": ["회계사", "법률 전문가", "군인"],
    "ISFJ": ["간호사", "초등교사", "행정직"],
    "ESTJ": ["공무원", "운영 관리자", "금융 전문가"],
    "ESFJ": ["영업 관리자", "호텔 매니저", "이벤트 기획자"],
    "ISTP": ["엔지니어", "파일럿", "응급 구조원"],
    "ISFP": ["사진작가", "패션 디자이너", "음악가"],
    "ESTP": ["기업가", "스포츠 코치", "소방관"],
    "ESFP": ["배우", "MC", "관광 가이드"]
}

st.title("💡 MBTI 기반 직업 추천기")
st.write("당신의 MBTI를 선택하면 어울리는 직업을 추천해드립니다!")

# MBTI 선택
selected_mbti = st.selectbox("MBTI를 선택하세요", list(mbti_jobs.keys()))

# 추천 직업 출력
if selected_mbti:
    st.subheader(f"📌 {selected_mbti} 유형 추천 직업")
    jobs = mbti_jobs[selected_mbti]
    for job in jobs:
        st.write(f"- {job}")

# 실행 방법 안내
st.markdown("---")
st.caption("터미널에서 `streamlit run app.py`로 실행하세요.")

