import streamlit as st # Streamlit 라이브러리를 가져옵니다. 웹 앱을 만드는 데 사용해요!
import random # 명언을 무작위로 선택할 때 사용할 random 모듈을 가져옵니다.

# =========================================================
# EMOJI_2 1. 기본 앱 설정 및 데이터 초기화
# =========================================================

# 웹 페이지의 레이아웃을 'wide'로 설정하여 넓게 사용합니다.
st.set_page_config(layout="wide") 

# 앱의 메인 제목을 설정합니다.
st.title("EMOJI_3 오늘의 긍정 한 스푼! 명언 추천기 EMOJI_4")
# 앱에 대한 간단한 설명을 추가합니다.
st.write("마음에 따뜻함을 전하는 명언을 만나보세요! EMOJI_5")

# === 중요! 미리 정의된 긍정 명언 목록입니다. ===
# 'quote'는 명언 내용, 'author'는 작가를 나타냅니다.
# 여기에 원하는 명언을 더 추가하거나 수정할 수 있어요!
default_quotes = [
    {'quote': '나는 내가 생각하는 나이다.', 'author': '노먼 빈센트 필'},
    {'quote': '오늘이라는 날은 다시 오지 않는다는 것을 기억하라.', 'author': '단테'},
    {'quote': '행동은 모든 성공의 기본적인 열쇠이다.', 'author': '파블로 피카소'},
    {'quote': '성공은 작은 노력들이 매일 반복되는 결과이다.', 'author': '로버트 칼리에'},
    {'quote': '우리가 간절히 바라는 꿈을 위해 무엇이든 할 수 있다는 것을 깨달을 때, 우리의 잠재력은 무한하다.', 'author': '오프라 윈프리'},
    {'quote': '가능한 일을 하기 위해선 한 가지 방법밖에 없다. 그 일을 사랑하는 것이다.', 'author': '스티브 잡스'},
    {'quote': '우리가 할 수 있는 가장 큰 일은 결코 쓰러지지 않는 것이 아니라, 쓰러질 때마다 일어서는 것이다.', 'author': '공자'},
    {'quote': '성공으로 가는 엘리베이터는 고장 났다. 당신은 계단을 이용해야 한다. 한 번에 한 계단씩.', 'author': '조 지라드'},
    {'quote': '시작이 반이다.', 'author': '아리스토텔레스'},
    {'quote': '태도는 사소한 것이지만 모든 것을 변화시킨다.', 'author': '윈스턴 처칠'},
    {'quote': '길이 없으면 길을 만들면서 가라.', 'author': '이창동'},
    {'quote': '작은 기회가 종종 위대한 기업의 시작이다.', 'author': '데모스테네스'},
    {'quote': '꿈을 포기하지 마라. 한 번도 시작하지 않았다는 것을 후회하지 마라.', 'author': 'J.K. 롤링'},
    {'quote': '가장 큰 영광은 한 번도 넘어지지 않는 것이 아니라 넘어질 때마다 일어나는 것이다.', 'author': '넬슨 만델라'},
    {'quote': '변화를 두려워하지 않는 용기, 그것이 당신을 성장시킬 것이다.', 'author': '에머슨'},
]
# =========================================

# Streamlit의 'session_state'를 사용하여 앱 상태를 유지합니다.
# 'all_quotes'가 session_state에 없으면(앱이 처음 실행될 때), 기본 명언 목록으로 초기화합니다.
# 사용자가 추가하는 명언도 여기에 함께 저장됩니다.
if 'all_quotes' not in st.session_state:
    st.session_state.all_quotes = list(default_quotes) # 리스트의 복사본을 저장합니다.
    random.shuffle(st.session_state.all_quotes) # 앱 시작 시 명언을 무작위로 섞어줍니다.

# 'current_quote_index' 키가 없으면 0으로 초기화합니다.
# 현재 화면에 표시되는 명언의 인덱스를 저장합니다.
if 'current_quote_index' not in st.session_state:
    st.session_state.current_quote_index = 0

# =========================================================
# ✨ 2. 명언 표시 및 '다음 명언 보기' 기능
# =========================================================

# 명언을 표시할 공간을 나눕니다.
col_display, col_button = st.columns([3, 1]) # 3:1 비율로 컬럼을 나눕니다.

with col_display:
    # 현재 인덱스에 해당하는 명언을 가져옵니다.
    # 만약 모든 명언을 다 보았다면 다시 처음으로 돌아갑니다 (순환).
    if st.session_state.all_quotes: # 명언이 하나라도 있다면
        current_quote_obj = st.session_state.all_quotes[st.session_state.current_quote_index]
        
        # 명언 내용을 크게, 중앙에 표시합니다. Markdown을 사용하여 스타일을 적용합니다.
        st.markdown(f"<h2 style='text-align: center; color: #4A90E2;'>“{current_quote_obj['quote']}”</h2>", unsafe_allow_html=True)
        # 작가를 오른쪽 정렬하여 표시합니다.
        st.markdown(f"<h3 style='text-align: right; color: #555555;'>– {current_quote_obj['author']}</h3>", unsafe_allow_html=True)
    else:
        st.info("아직 추가된 명언이 없어요! 아래에서 새로운 명언을 추가해보세요. EMOJI_6")

with col_button:
    st.write("") # 공간을 조금 띄워줍니다.
    st.write("") 
    st.write("") 
    # '다음 명언 보기' 버튼을 만듭니다.
    if st.button("다음 명언 보기 EMOJI_7", type="primary"):
        if st.session_state.all_quotes:
            # 다음 명언 인덱스로 이동합니다. 리스트의 끝에 도달하면 0으로 다시 시작합니다.
            st.session_state.current_quote_index = (st.session_state.current_quote_index + 1) % len(st.session_state.all_quotes)
            st.experimental_rerun() # 화면을 새로고침하여 다음 명언을 보여줍니다.
        else:
            st.warning("표시할 명언이 없어요! 먼저 명언을 추가해주세요. EMOJI_8")


st.markdown("---") # 구분선을 추가합니다.

# =========================================================
# ➕ 3. 나만의 명언 추가하기
# =========================================================

# 'st.expander'를 사용하면 내용을 접었다 폈다 할 수 있어 깔끔하게 앱을 구성할 수 있어요.
with st.expander("✨ 나만의 명언 추가하기"):
    # 폼을 사용하여 명언과 작가를 입력받고, 버튼을 누를 때까지 내용을 일괄 처리합니다.
    with st.form("add_quote_form"):
        new_quote = st.text_area("명언을 입력해주세요. (200자 이내)", height=70, max_chars=200, key="new_quote_input")
        new_author = st.text_input("작가를 입력해주세요. (선택 사항)", key="new_author_input")
        
        # 폼 제출 버튼입니다.
        submitted = st.form_submit_button("나만의 명언 추가하기!")

        if submitted:
            if new_quote: # 명언 내용이 비어있지 않다면
                if not new_author: # 작가가 입력되지 않았다면 '작자 미상'으로 기본 설정
                    new_author = "작자 미상"
                
                # 새로운 명언을 session_state.all_quotes 리스트에 추가합니다.
                st.session_state.all_quotes.append({'quote': new_quote, 'author': new_author})
                st.success("새 명언이 추가되었어요! 감사합니다! EMOJI_9")
                st.experimental_rerun() # 추가된 명언을 포함하여 앱을 새로고침합니다.
            else:
                st.warning("명언 내용을 입력해주세요! EMOJI_10")

st.markdown("---") # 또 다른 구분선을 추가합니다.

# =========================================================
# EMOJI_11 4. 전체 명언 목록 보기
# =========================================================

with st.expander("EMOJI_12 모든 명언 보기"):
    if st.session_state.all_quotes:
        # st.dataframe을 사용하여 현재 저장된 모든 명언을 표 형태로 보여줍니다.
        st.dataframe(st.session_state.all_quotes, use_container_width=True)

        # 모든 명언을 초기화하는 버튼입니다. (기본 명언 + 사용자 추가 명언 모두 삭제 후 기본으로 되돌림)
        if st.button("모든 명언 초기화 (기본 목록으로 되돌리기)", help="모든 명언을 삭제하고, 앱에 내장된 기본 명언 목록으로 되돌립니다.", type="secondary"):
            st.session_state.all_quotes = list(default_quotes) # 기본 명언 목록으로 복원
            st.session_state.current_quote_index = 0 # 인덱스 초기화
            st.info("명언 목록이 초기화되었습니다! ✨")
            st.experimental_rerun() # 변경사항 반영을 위해 새로고침

    else:
        st.info("아직 보여줄 명언이 없어요. 위에서 명언을 추가하거나, 앱을 새로고침하여 기본 명언을 불러올 수 있습니다. EMOJI_13")
