# -*- coding: utf-8 -*-
import streamlit as st

st.set_page_config(page_title="홈앤쇼핑", layout="wide")

st.title("홈앤쇼핑 Streamlit 테스트")

st.write("✅ Streamlit이 정상적으로 설치되었습니다!")

st.markdown("### 기본 기능 테스트")
name = st.text_input("이름을 입력하세요:")
if name:
    st.write(f"안녕하세요, **{name}**님!")

st.markdown("### 숫자 입력 테스트")
number = st.slider("숫자를 선택하세요:", 0, 100, 50)
st.write(f"선택한 숫자: {number}")

st.success("모든 테스트를 통과했습니다! 🎉")
