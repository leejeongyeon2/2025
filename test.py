import streamlit as st
import random

# =========================================================
# EMOJI_2 1. 기본 앱 설정 및 데이터 초기화
# =========================================================

st.set_page_config(layout="wide") 

st.title("EMOJI_3 오늘의 긍정 한 스푼! 명언 추천기 EMOJI_4")
st.write("마음에 따뜻함을 전하는 명언을 만나보세요! EMOJI_5")

# === 미리 정의된 긍정 명언 목록 ===
# 이 리스트에 원하는 명언을 더 추가하거나 수정할 수 있어요!
# 기존 명언 목록 그대로 유지합니다.
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

# --- session_state 초기화 로직 개선 ---
# 'all_quotes'가 없으면, default_quotes의 복사본으로 초기화합니다.
# 이렇게 해야 default_quotes 리스트 자체가 앱 내에서 변경되지 않습니다.
if 'all_quotes' not in st.session_state:
    st.session_state.all_quotes = list(default_quotes)
    random.shuffle(st.session_state.all_quotes) # 초기 로드 시 명언 섞기

# 'current_quote_index'가 없으면 0으로 초기화합니다.
if 'current_quote_index' not in st.session_state:
    st.session_state.current_quote_index = 0

# --- 명언 표시 및 '다음 명언 보기' 기능 ---
col_display, col_button = st.columns([3, 1])

with col_display:
    # --- 명언 목록이 비어있을 때의 처리 추가 ---
    if not st.session_state.all_quotes:
        st.info("표시할 명언이 없어요. 아래에서 새로운 명언을 추가하거나, 앱을 새로고침하여 기본 명언을 불러올 수 있습니다. EMOJI_6")
    else:
        # 현재 인덱스에 해당하는 명언을 가져옵니다.
        # 인덱스가 리스트 범위를 벗어나지 않도록 'len(st.session_state.all_quotes)'으로 나머지 연산
        # 또는 'min' 함수를 사용하여 안전하게 인덱스를 가져옵니다.
        # 여기서 인덱스 에러가 발생할 가능성이 있으므로, 현재 인덱스가 유효한지 다시 확인합니다.
        safe_index = st.session_state.current_quote_index % len(st.session_state.all_quotes)
        current_quote_obj = st.session_state.all_quotes[safe_index]
        
        st.markdown(f"<h2 style='text-align: center; color: #4A90E2;'>“{current_quote_obj['quote']}”</h2>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: right; color: #555555;'>– {current_quote_obj['author']}</h3>", unsafe_allow_html=True)

with col_button:
    st.write("") 
    st.write("") 
    st.write("") 
    
    # '다음 명언 보기' 버튼
    # 이 버튼을 클릭하면, 콜백 함수를 호출하여 명언 인덱스를 업데이트하고 화면을 새로고침합니다.
    # 콜백 함수를 사용하는 것이 state 관리와 UI 업데이트에 더 안정적인 방법일 수 있습니다.
    def next_quote():
        if st.session_state.all_quotes:
            st.session_state.current_quote_index = (st.session_state.current_quote_index + 1) % len(st.session_state.all_quotes)
        else:
            # 명언이 없는데 다음 버튼을 누르는 경우
            st.warning("표시할 명언이 없어요! 먼저 명언을 추가해주세요. EMOJI_7")

    st.button("다음 명언 보기 EMOJI_8", type="primary", on_click=next_quote)


st.markdown("---") # 구분선

# =========================================================
# ➕ 3. 나만의 명언 추가하기
# =========================================================

with st.expander("✨ 나만의 명언 추가하기"):
    with st.form("add_quote_form"):
        new_quote = st.text_area("명언을 입력해주세요. (200자 이내)", height=70, max_chars=200, key="new_quote_input")
        new_author = st.text_input("작가를 입력해주세요. (선택 사항)", key="new_author_input")
        
        submitted = st.form_submit_button("나만의 명언 추가하기!")

        if submitted:
            if new_quote:
                if not new_author:
                    new_author = "작자 미상"
                
                # 새로운 명언 추가 시 현재 인덱스를 유지하거나, 맨 처음으로 돌릴 수 있습니다.
                # 여기서는 명언을 추가한 뒤 다시 맨 처음 명언을 보여주도록 current_quote_index를 초기화했습니다.
                # (옵션) st.session_state.all_quotes.append({'quote': new_quote, 'author': new_author})
                # (옵션) 새로운 명언을 추가한 후에는 해당 명언을 바로 볼 수 있도록 인덱스를 업데이트
                st.session_state.all_quotes.insert(0, {'quote': new_quote, 'author': new_author}) # 새로 추가한 것을 맨 앞으로
                st.session_state.current_quote_index = 0 # 인덱스 리셋

                st.success("새 명언이 추가되었어요! 감사합니다! EMOJI_9")
                st.experimental_rerun() # 변경사항 반영 및 명언 추가 후 첫 명언으로 이동
            else:
                st.warning("명언 내용을 입력해주세요! EMOJI_10")

st.markdown("---") # 구분선

# =========================================================
# EMOJI_11 4. 전체 명언 목록 보기 및 초기화
# =========================================================

with st.expander("EMOJI_12 모든 명언 보기"):
    if st.session_state.all_quotes:
        # DataFrame을 직접 수정할 수 있도록 `key`와 `on_change` 콜백을 설정할 수도 있습니다.
        # 여기서는 단순 보기만 가능하게 합니다.
        st.dataframe(st.session_state.all_quotes, use_container_width=True)

        # 초기화 콜백 함수
        def reset_quotes():
            st.session_state.all_quotes = list(default_quotes) # 기본 명언 목록으로 복원
            random.shuffle(st.session_state.all_quotes) # 다시 섞기
            st.session_state.current_quote_index = 0 # 인덱스 초기화
            st.info("명언 목록이 초기화되었습니다! ✨")
        
        # '모든 명언 초기화' 버튼. 콜백 함수를 사용하여 안정적으로 상태를 변경합니다.
        st.button("모든 명언 초기화 (기본 목록으로 되돌리기)", help="사용자 추가 명언을 삭제하고, 앱에 내장된 기본 명언 목록으로 되돌립니다.", type="secondary", on_click=reset_quotes)
        
        # 전체 삭제 (모든 명언을 비움) 버튼
        def clear_all_quotes():
            st.session_state.all_quotes = []
            st.session_state.current_quote_index = 0
            st.info("모든 명언이 완전히 삭제되었습니다. EMOJI_13")

        st.button("모든 명언 완전히 삭제 (빈 목록)", help="모든 명언을 완전히 삭제하여 빈 목록으로 만듭니다.", type="secondary", on_click=clear_all_quotes)

    else:
        st.info("아직 보여줄 명언이 없어요. 위에서 명언을 추가하거나, '모든 명언 초기화' 버튼을 눌러 기본 명언을 불러올 수 있습니다. EMOJI_14")
