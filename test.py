import streamlit as st # Streamlit 라이브러리를 가져옵니다.
import random # 단어를 무작위로 섞을 때 사용할 random 모듈을 가져옵니다.

# =========================================================
# EMOJI_1 1. 기본 앱 설정 및 데이터 초기화 (미리 정의된 단어 포함)
# =========================================================

# 웹 페이지의 레이아웃을 'wide'로 설정합니다.
st.set_page_config(layout="wide") 

# 앱의 제목을 설정합니다.
st.title("EMOJI_2 나만의 단어 암기 게임 (기본 단어 버전) EMOJI_3")
# 앱에 대한 간단한 설명을 추가합니다.
st.write("미리 준비된 단어들로 바로 암기 게임을 시작해보세요! EMOJI_4")

# === 중요! 미리 정의된 단어 목록입니다. ===
# 이 리스트에 원하는 단어와 뜻을 추가하거나 수정할 수 있어요!
default_words = [
    {'word': 'apple', 'meaning': '사과'},
    {'word': 'banana', 'meaning': '바나나'},
    {'word': 'car', 'meaning': '자동차'},
    {'word': 'dog', 'meaning': '개'},
    {'word': 'flower', 'meaning': '꽃'},
    {'word': 'house', 'meaning': '집'},
    {'word': 'river', 'meaning': '강'},
    {'word': 'mountain', 'meaning': '산'},
    {'word': 'ocean', 'meaning': '바다'},
    {'word': 'dream', 'meaning': '꿈'},
    {'word': 'hope', 'meaning': '희망'},
    {'word': 'friend', 'meaning': '친구'},
    {'word': 'love', 'meaning': '사랑'},
    {'word': 'future', 'meaning': '미래'},
]
# =========================================

# 'words'라는 키가 session_state에 없으면, 미리 정의된 'default_words'로 초기화합니다.
# 이렇게 하면 앱을 실행하자마자 이 단어들이 목록에 나타나요!
if 'words' not in st.session_state:
    st.session_state.words = list(default_words) # default_words의 복사본을 사용하여 변경되지 않도록 합니다.

# 'game_mode_active' 키가 없으면 False로 초기화합니다.
if 'game_mode_active' not in st.session_state:
    st.session_state.game_mode_active = False 

# 'current_word_index' 키가 없으면 0으로 초기화합니다.
if 'current_word_index' not in st.session_state:
    st.session_state.current_word_index = 0 

st.sidebar.header("메뉴")


# =========================================================
# EMOJI_5 (이전 버전의 단어 추가하기 섹션은 이번 버전에서 제거되었습니다.)
# =========================================================


# =========================================================
# EMOJI_6 2. 현재 단어 목록 보기 섹션
# =========================================================

# 섹션의 제목을 설정합니다.
st.header("EMOJI_7 현재 단어 목록")

# 미리 정의된 단어가 항상 있으므로, 이 부분은 항상 실행됩니다.
# 탭 기능을 사용해서 '단어 목록'과 '게임 시작'을 분리합니다.
tab1, tab2 = st.tabs(["단어 목록", "게임 시작"])

# '단어 목록' 탭 안의 내용
with tab1:
    # st.dataframe을 사용하여 단어 목록을 예쁜 표 형태로 보여줍니다.
    st.dataframe(st.session_state.words, use_container_width=True) 
    
    # '현재 목록 초기화' 버튼을 만듭니다.
    # 이 버튼을 누르면 'default_words'로 목록이 다시 채워집니다.
    if st.button("현재 목록 초기화", help="초기 단어 목록으로 되돌립니다.", type="secondary"):
        st.session_state.words = list(default_words) # 초기 단어 목록으로 복원
        st.info("단어 목록이 초기화되었어요! ✨") 
        st.session_state.game_mode_active = False # 혹시 게임 중이었다면 종료
        st.session_state.current_word_index = 0 # 인덱스도 초기화
        st.experimental_rerun() # 앱을 새로고침하여 변경사항을 즉시 반영합니다.
    
    # 추가적으로 '모든 단어 삭제' 기능을 남겨둘 수도 있지만,
    # '초기화' 기능이 있으니 여기서는 생략했습니다.
    # 만약 완전히 빈 상태로 만들고 싶다면 아래 코드를 추가할 수 있습니다.
    # if st.button("모든 단어 완전히 삭제", type="secondary"):
    #     st.session_state.words = []
    #     st.info("모든 단어가 삭제되었어요! 새롭게 시작해보세요! EMOJI_8")
    #     st.experimental_rerun()


# =========================================================
# EMOJI_9 3. 단어 암기 게임 시작 섹션 (플래시카드 모드)
# =========================================================

# 미리 정의된 단어가 항상 있으므로, 게임 시작 조건은 항상 충족됩니다.
with tab2: # '게임 시작' 탭 안의 내용
    # 섹션의 제목을 설정합니다.
    st.header("EMOJI_10 단어 암기 게임 시작!")

    # 'game_mode_active'가 False, 즉 게임 모드가 활성화되지 않은 상태라면
    if not st.session_state.game_mode_active:
        # '게임 시작!' 버튼을 만듭니다.
        if st.button("게임 시작!", type="primary"):
            # 게임 시작 전에 단어 목록을 무작위로 섞습니다.
            random.shuffle(st.session_state.words) 
            st.session_state.current_word_index = 0 # 현재 단어 인덱스를 0으로 초기화합니다.
            st.session_state.game_mode_active = True # 게임 모드를 활성화합니다.
            st.experimental_rerun() # 앱을 새로고침하여 게임 화면으로 전환합니다.
    # 'game_mode_active'가 True, 즉 게임 모드가 활성화된 상태라면
    else:
        # 전체 단어의 개수를 가져옵니다.
        total_words = len(st.session_state.words)
        # 현재 단어 인덱스가 전체 단어 개수보다 작다면 (아직 모든 단어를 다 보지 않았다면)
        if st.session_state.current_word_index < total_words:
            # 현재 인덱스에 해당하는 단어 정보를 가져옵니다.
            current_item = st.session_state.words[st.session_state.current_word_index]

            # 현재 보고 있는 단어를 크게 표시합니다.
            st.subheader(f"✨ 단어: {current_item['word']}")

            # '뜻 보기' 버튼을 만듭니다.
            if st.button("뜻 보기 EMOJI_11", key="show_meaning_btn"):
                # 버튼이 눌리면 해당 단어의 뜻을 보여줍니다.
                st.write(f"**EMOJI_12 뜻: {current_item['meaning']}**")
            
            # 버튼 두 개를 나란히 배치하기 위해 컬럼을 나눕니다.
            col1, col2 = st.columns(2)
            with col1: # 첫 번째 컬럼에 '이전 단어' 버튼을 배치합니다.
                # '이전 단어' 버튼을 만듭니다.
                if st.button("이전 단어 ⏪", key="prev_word_btn"):
                    # 현재 단어 인덱스가 0보다 크면 (첫 단어가 아니라면)
                    if st.session_state.current_word_index > 0:
                        st.session_state.current_word_index -= 1 # 인덱스를 1 감소시켜 이전 단어로 이동합니다.
                        st.experimental_rerun() # 앱을 새로고침하여 변경된 단어를 보여줍니다.
                    else:
                        st.info("여기가 첫 단어예요! EMOJI_13") # 첫 단어일 경우 안내 메시지
            with col2: # 두 번째 컬럼에 '다음 단어' 버튼을 배치합니다.
                # '다음 단어' 버튼을 만듭니다.
                if st.button("다음 단어 ⏩", key="next_word_btn"):
                    st.session_state.current_word_index += 1 # 인덱스를 1 증가시켜 다음 단어로 이동합니다.
                    st.experimental_rerun() # 앱을 새로고침하여 변경된 단어를 보여줍니다.
        # 모든 단어를 다 살펴봤다면
        else:
            # 게임 완료 메시지를 보여줍니다.
            st.success("EMOJI_14 모든 단어를 다 살펴보셨어요! 대단해요!")
            # '게임 다시 시작!' 버튼을 만듭니다.
            if st.button("게임 다시 시작!", type="primary"):
                st.session_state.game_mode_active = False # 게임 모드를 비활성화합니다.
                st.session_state.current_word_index = 0 # 인덱스를 초기화합니다.
                st.experimental_rerun() # 앱을 새로고침하여 게임 시작 화면으로 돌아갑니다.

        # EMOJI_15 게임 종료 버튼 (항상 게임 진행 중에 보임)
        if st.button("게임 종료 EMOJI_16", key="end_game_btn_always"): 
            st.session_state.game_mode_active = False # 게임 모드를 비활성화합니다.
            st.session_state.current_word_index = 0 # 인덱스를 초기화합니다.
            st.info("게임을 종료합니다! 다음에 또 만나요! EMOJI_17") # 종료 메시지
            st.experimental_rerun() # 앱을 새로고침하여 초기 화면으로 돌아갑니다.
