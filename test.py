import streamlit as st # Streamlit 라이브러리를 가져옵니다. 웹 앱을 쉽게 만들 수 있게 해주는 도구예요!
import random # 단어를 무작위로 섞을 때 사용할 random 모듈을 가져옵니다.

# =========================================================
# EMOJI_2 1. 기본 앱 설정 및 데이터 초기화
# =========================================================

# 웹 페이지의 레이아웃을 'wide'로 설정합니다. 더 넓은 화면을 사용할 수 있어요!
st.set_page_config(layout="wide") 

# 앱의 제목을 설정합니다.
st.title("EMOJI_3 나만의 단어 암기 게임 EMOJI_4")
# 앱에 대한 간단한 설명을 추가합니다.
st.write("새 단어를 추가하거나, 암기 게임을 시작해보세요!")

# Streamlit의 핵심 기능 중 하나인 'session_state'를 사용합니다.
# session_state는 사용자가 앱과 상호작용하는 동안(예: 버튼 클릭, 입력) 데이터를 유지시켜주는 저장 공간이에요.
# 앱이 새로고침되거나 다른 페이지로 이동해도 데이터가 날아가지 않도록 해줍니다.

# 'words'라는 키가 session_state에 없으면(앱이 처음 시작될 때), 빈 리스트로 초기화합니다.
# 이 리스트는 단어와 그 뜻을 사전(dictionary) 형태로 저장할 거예요.
# 예시: [{'word': 'apple', 'meaning': '사과'}, {'word': 'banana', 'meaning': '바나나'}]
if 'words' not in st.session_state:
    st.session_state.words = [] 

# 'game_mode_active' 키가 없으면 False로 초기화합니다.
# 현재 게임 모드가 활성화되어 있는지(True) 아닌지(False)를 저장합니다.
if 'game_mode_active' not in st.session_state:
    st.session_state.game_mode_active = False 

# 'current_word_index' 키가 없으면 0으로 초기화합니다.
# 게임 중 현재 보여주고 있는 단어의 인덱스(순서)를 저장합니다.
if 'current_word_index' not in st.session_state:
    st.session_state.current_word_index = 0 

# 사이드바 헤더를 추가합니다. (현재는 사용하지 않지만 메뉴를 추가할 때 유용해요!)
st.sidebar.header("메뉴")


# =========================================================
# EMOJI_5 2. 단어 추가하기 섹션
# =========================================================

# 섹션의 제목을 설정합니다.
st.header("EMOJI_6 새 단어 추가하기")

# 'st.form'을 사용하면 여러 입력 위젯(텍스트 입력, 버튼 등)을 하나로 묶어서 관리할 수 있습니다.
# 폼 내부의 버튼을 누르기 전까지는 입력값이 실시간으로 앱을 새로고침하지 않아요.
with st.form("add_word_form"): # 폼의 고유한 이름을 지정합니다.
    # 단어를 입력받는 텍스트 입력 칸을 만듭니다. key는 이 위젯을 식별하는 고유 이름입니다.
    new_word = st.text_input("단어", key="new_word_input")
    # 뜻을 입력받는 텍스트 입력 칸을 만듭니다.
    new_meaning = st.text_input("뜻", key="new_meaning_input")
    
    # 폼 제출 버튼을 만듭니다. 이 버튼을 눌러야 폼 안의 내용이 처리됩니다.
    submitted = st.form_submit_button("단어 추가!")

    # 만약 '단어 추가!' 버튼이 눌렸다면 (submitted가 True)
    if submitted:
        # 단어와 뜻 입력 칸이 모두 비어있지 않다면
        if new_word and new_meaning:
            # session_state.words 리스트에 새로운 단어와 뜻을 딕셔너리 형태로 추가합니다.
            st.session_state.words.append({'word': new_word, 'meaning': new_meaning})
            # 단어 추가 성공 메시지를 사용자에게 보여줍니다. (초록색 상자)
            st.success(f"'{new_word}' 단어가 추가되었어요! ✨")
        else:
            # 단어 또는 뜻이 비어있으면 경고 메시지를 보여줍니다. (노란색 상자)
            st.warning("단어와 뜻을 모두 입력해주세요! EMOJI_7")


# =========================================================
# EMOJI_8 3. 현재 단어 목록 보기 섹션
# =========================================================

# 섹션의 제목을 설정합니다.
st.header("EMOJI_9 현재 단어 목록")

# session_state.words 리스트에 단어가 하나라도 있다면
if st.session_state.words:
    # 탭 기능을 사용해서 '단어 목록'과 '게임 시작'을 분리합니다.
    # 사용자가 탭을 클릭하여 원하는 화면으로 전환할 수 있습니다.
    tab1, tab2 = st.tabs(["단어 목록", "게임 시작"])

    # '단어 목록' 탭 안의 내용
    with tab1:
        # st.dataframe을 사용하여 단어 목록을 예쁜 표 형태로 보여줍니다.
        # use_container_width=True로 설정하면 표가 화면 너비에 맞게 조절됩니다.
        st.dataframe(st.session_state.words, use_container_width=True) 
        
        # '모든 단어 삭제' 버튼을 만듭니다.
        # type="secondary"로 설정하여 기본 버튼과 다른 스타일을 부여합니다.
        # help는 마우스를 올렸을 때 나타나는 풍선 도움말입니다.
        if st.button("모든 단어 삭제", help="모든 단어를 영구히 삭제합니다.", type="secondary"):
            # 단어 목록이 비어있지 않다면
            if st.session_state.words:
                st.session_state.words = [] # 단어 리스트를 완전히 비웁니다.
                st.info("모든 단어가 삭제되었어요! 새롭게 시작해보세요! EMOJI_10") # 정보 메시지를 보여줍니다.
                st.experimental_rerun() # 앱을 새로고침하여 변경사항(단어가 없어진 것)을 즉시 반영합니다.
            else:
                # 삭제할 단어가 없으면 경고 메시지를 보여줍니다.
                st.warning("삭제할 단어가 없어요! EMOJI_11")
# session_state.words 리스트가 비어있다면
else:
    # 사용자에게 단어를 추가하라는 정보 메시지를 보여줍니다.
    st.info("아직 추가된 단어가 없어요. 새로운 단어를 추가해보세요! EMOJI_12")


# =========================================================
# EMOJI_13 4. 단어 암기 게임 시작 섹션 (플래시카드 모드)
# =========================================================

# session_state.words 리스트에 단어가 하나라도 있어야 게임 섹션을 활성화합니다.
if st.session_state.words:
    # '게임 시작' 탭 안의 내용
    with tab2: # 위에서 정의한 tab2 (게임 시작 탭) 안에 코드를 작성합니다.
        # 섹션의 제목을 설정합니다.
        st.header("EMOJI_14 단어 암기 게임 시작!")

        # 'game_mode_active'가 False, 즉 게임 모드가 활성화되지 않은 상태라면
        if not st.session_state.game_mode_active:
            # '게임 시작!' 버튼을 만듭니다.
            if st.button("게임 시작!", type="primary"):
                # 단어 목록이 비어있지 않다면
                if st.session_state.words:
                    random.shuffle(st.session_state.words) # 게임 시작 전에 단어 목록을 무작위로 섞습니다.
                    st.session_state.current_word_index = 0 # 현재 단어 인덱스를 0으로 초기화합니다.
                    st.session_state.game_mode_active = True # 게임 모드를 활성화합니다.
                    st.experimental_rerun() # 앱을 새로고침하여 게임 화면으로 전환합니다.
                else:
                    st.warning("게임을 시작하려면 단어를 먼저 추가해주세요! EMOJI_15")
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
                if st.button("뜻 보기 EMOJI_16", key="show_meaning_btn"):
                    # 버튼이 눌리면 해당 단어의 뜻을 보여줍니다.
                    st.write(f"**EMOJI_17 뜻: {current_item['meaning']}**")
                
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
                            st.info("여기가 첫 단어예요! EMOJI_18") # 첫 단어일 경우 안내 메시지
                with col2: # 두 번째 컬럼에 '다음 단어' 버튼을 배치합니다.
                    # '다음 단어' 버튼을 만듭니다.
                    if st.button("다음 단어 ⏩", key="next_word_btn"):
                        st.session_state.current_word_index += 1 # 인덱스를 1 증가시켜 다음 단어로 이동합니다.
                        st.experimental_rerun() # 앱을 새로고침하여 변경된 단어를 보여줍니다.
            # 모든 단어를 다 살펴봤다면
            else:
                # 게임 완료 메시지를 보여줍니다.
                st.success("EMOJI_19 모든 단어를 다 살펴보셨어요! 대단해요!")
                # '게임 다시 시작!' 버튼을 만듭니다.
                if st.button("게임 다시 시작!", type="primary"):
                    st.session_state.game_mode_active = False # 게임 모드를 비활성화합니다.
                    st.session_state.current_word_index = 0 # 인덱스를 초기화합니다.
                    st.experimental_rerun() # 앱을 새로고침하여 게임 시작 화면으로 돌아갑니다.

            # EMOJI_20 게임 종료 버튼 (항상 게임 진행 중에 보임)
            # key 충돌을 방지하기 위해 이전에 사용된 키와 다르게 지정합니다.
            if st.button("게임 종료 EMOJI_21", key="end_game_btn_always"): 
                st.session_state.game_mode_active = False # 게임 모드를 비활성화합니다.
                st.session_state.current_word_index = 0 # 인덱스를 초기화합니다.
                st.info("게임을 종료합니다! 다음에 또 만나요! EMOJI_22") # 종료 메시지
                st.experimental_rerun() # 앱을 새로고침하여 초기 화면으로 돌아갑니다.

# 단어가 없어서 게임을 시작할 수 없는 경우의 메시지는
# 이미 위 '현재 단어 목록' 섹션의 else 구문에서 처리하고 있으므로, 여기서는 추가적인 처리가 필요 없습니다.
else:
    pass 
