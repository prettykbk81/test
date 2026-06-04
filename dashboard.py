# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# matplotlib 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 페이지 설정
st.set_page_config(page_title="홈앤쇼핑 영업기획 대시보드", layout="wide")

# 제목
st.title("📊 홈앤쇼핑 5월 판매 현황")
st.markdown("---")

# CSV 파일 읽기
tv_sales = pd.read_csv("TV_판매_5월.csv")
mobile_sales = pd.read_csv("모바일쇼핑몰_5월.csv")
prime_sales = pd.read_csv("프라임타임특약_5월.csv")

# 날짜 변환
tv_sales['날짜'] = pd.to_datetime(tv_sales['날짜'])
mobile_sales['날짜'] = pd.to_datetime(mobile_sales['날짜'])
prime_sales['날짜'] = pd.to_datetime(prime_sales['날짜'])

# 탭 생성
tab1, tab2, tab3, tab4 = st.tabs(["전체 현황", "TV 판매", "모바일 쇼핑몰", "프라임타임 특약"])

# ===== TAB 1: 전체 현황 =====
with tab1:
    col1, col2, col3 = st.columns(3)

    # 월간 합계
    tv_total = tv_sales.drop('날짜', axis=1).sum().sum()
    mobile_total = mobile_sales.drop('날짜', axis=1).sum().sum()
    prime_total = prime_sales.drop('날짜', axis=1).sum().sum()
    grand_total = tv_total + mobile_total + prime_total

    with col1:
        st.metric("TV 판매 합계", f"₩{tv_total:,.0f}")
    with col2:
        st.metric("모바일 쇼핑몰", f"₩{mobile_total:,.0f}")
    with col3:
        st.metric("프라임타임 특약", f"₩{prime_total:,.0f}")

    st.markdown("---")

    # 전체 매출 현황
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("채널별 비중")
        channel_data = pd.DataFrame({
            '채널': ['TV 판매', '모바일 쇼핑몰', '프라임타임 특약'],
            '매출': [tv_total, mobile_total, prime_total]
        })

        fig, ax = plt.subplots(figsize=(8, 6))
        colors = ['#0052CC', '#1E90FF', '#4169E1']
        ax.pie(channel_data['매출'], labels=channel_data['채널'], autopct='%1.1f%%',
               colors=colors, startangle=90)
        ax.set_title('채널별 매출 비중', fontsize=14, fontweight='bold', pad=20)
        st.pyplot(fig)

    with col2:
        st.subheader("일일 매출 추이")
        tv_daily = tv_sales.set_index('날짜').sum(axis=1)
        mobile_daily = mobile_sales.set_index('날짜').sum(axis=1)
        prime_daily = prime_sales.set_index('날짜').sum(axis=1)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(tv_daily.index, tv_daily.values, marker='o', label='TV 판매', linewidth=2, color='#0052CC')
        ax.plot(mobile_daily.index, mobile_daily.values, marker='s', label='모바일 쇼핑몰', linewidth=2, color='#1E90FF')
        ax.plot(prime_daily.index, prime_daily.values, marker='^', label='프라임타임 특약', linewidth=2, color='#4169E1')

        ax.set_xlabel('날짜', fontsize=11)
        ax.set_ylabel('매출 (₩)', fontsize=11)
        ax.set_title('채널별 일일 매출 추이', fontsize=14, fontweight='bold', pad=20)
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₩{int(x/1e6)}M'))
        plt.xticks(rotation=45)
        st.pyplot(fig)

# ===== TAB 2: TV 판매 =====
with tab2:
    st.subheader("📺 TV 판매 현황")

    col1, col2, col3, col4 = st.columns(4)
    categories = ['건강식품', '일반식품', '리빙', '이미용']
    colors_list = ['#0052CC', '#1E90FF', '#4169E1', '#6495ED']

    tv_monthly = tv_sales.drop('날짜', axis=1).sum()

    with col1:
        st.metric("건강식품", f"₩{tv_monthly['건강식품']:,.0f}")
    with col2:
        st.metric("일반식품", f"₩{tv_monthly['일반식품']:,.0f}")
    with col3:
        st.metric("리빙", f"₩{tv_monthly['리빙']:,.0f}")
    with col4:
        st.metric("이미용", f"₩{tv_monthly['이미용']:,.0f}")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("카테고리별 매출")
        tv_cat = ['건강식품', '일반식품', '리빙', '이미용', '패션', '렌탈여행']
        tv_values = [tv_monthly[cat] for cat in tv_cat]

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(tv_cat, tv_values, color=['#0052CC', '#1E90FF', '#4169E1', '#6495ED', '#87CEEB', '#ADD8E6'])
        ax.set_ylabel('매출 (₩)', fontsize=11)
        ax.set_title('TV 판매 카테고리별 매출', fontsize=14, fontweight='bold', pad=20)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₩{int(x/1e6)}M'))
        plt.xticks(rotation=45)

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'₩{int(height/1e6)}M', ha='center', va='bottom', fontsize=9)

        st.pyplot(fig)

    with col2:
        st.subheader("일일 매출 추이")
        fig, ax = plt.subplots(figsize=(10, 6))

        for cat, color in zip(tv_cat, colors_list + ['#87CEEB', '#ADD8E6']):
            daily = tv_sales.set_index('날짜')[cat]
            ax.plot(daily.index, daily.values, marker='o', label=cat, linewidth=2, color=color, alpha=0.7)

        ax.set_xlabel('날짜', fontsize=11)
        ax.set_ylabel('매출 (₩)', fontsize=11)
        ax.set_title('TV 판매 카테고리별 일일 추이', fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='best', fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₩{int(x/1e6)}M'))
        plt.xticks(rotation=45)
        st.pyplot(fig)

# ===== TAB 3: 모바일 쇼핑몰 =====
with tab3:
    st.subheader("📱 모바일 쇼핑몰 현황")

    col1, col2, col3, col4, col5 = st.columns(5)

    mobile_monthly = mobile_sales.drop('날짜', axis=1).sum()

    with col1:
        st.metric("건강식품", f"₩{mobile_monthly['건강식품']:,.0f}")
    with col2:
        st.metric("일반식품", f"₩{mobile_monthly['일반식품']:,.0f}")
    with col3:
        st.metric("리빙", f"₩{mobile_monthly['리빙']:,.0f}")
    with col4:
        st.metric("이미용", f"₩{mobile_monthly['이미용']:,.0f}")
    with col5:
        st.metric("패션", f"₩{mobile_monthly['패션']:,.0f}")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("카테고리별 매출")
        mobile_cat = ['건강식품', '일반식품', '리빙', '이미용', '패션']
        mobile_values = [mobile_monthly[cat] for cat in mobile_cat]

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(mobile_cat, mobile_values, color=['#0052CC', '#1E90FF', '#4169E1', '#6495ED', '#87CEEB'])
        ax.set_ylabel('매출 (₩)', fontsize=11)
        ax.set_title('모바일 쇼핑몰 카테고리별 매출', fontsize=14, fontweight='bold', pad=20)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₩{int(x/1e6)}M'))
        plt.xticks(rotation=45)

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'₩{int(height/1e6)}M', ha='center', va='bottom', fontsize=9)

        st.pyplot(fig)

    with col2:
        st.subheader("일일 매출 추이")
        fig, ax = plt.subplots(figsize=(10, 6))

        for cat, color in zip(mobile_cat, ['#0052CC', '#1E90FF', '#4169E1', '#6495ED', '#87CEEB']):
            daily = mobile_sales.set_index('날짜')[cat]
            ax.plot(daily.index, daily.values, marker='o', label=cat, linewidth=2, color=color, alpha=0.7)

        ax.set_xlabel('날짜', fontsize=11)
        ax.set_ylabel('매출 (₩)', fontsize=11)
        ax.set_title('모바일 쇼핑몰 카테고리별 일일 추이', fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='best', fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₩{int(x/1e6)}M'))
        plt.xticks(rotation=45)
        st.pyplot(fig)

# ===== TAB 4: 프라임타임 특약 =====
with tab4:
    st.subheader("⭐ 프라임타임 특약 현황")

    col1, col2, col3 = st.columns(3)

    prime_monthly = prime_sales.drop('날짜', axis=1).sum()

    with col1:
        st.metric("건강식품", f"₩{prime_monthly['건강식품']:,.0f}")
    with col2:
        st.metric("패션", f"₩{prime_monthly['패션']:,.0f}")
    with col3:
        st.metric("이미용", f"₩{prime_monthly['이미용']:,.0f}")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("카테고리별 매출")
        prime_cat = ['건강식품', '패션', '이미용']
        prime_values = [prime_monthly[cat] for cat in prime_cat]

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(prime_cat, prime_values, color=['#0052CC', '#1E90FF', '#4169E1'])
        ax.set_ylabel('매출 (₩)', fontsize=11)
        ax.set_title('프라임타임 특약 카테고리별 매출', fontsize=14, fontweight='bold', pad=20)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₩{int(x/1e6)}M'))
        plt.xticks(rotation=45)

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'₩{int(height/1e6)}M', ha='center', va='bottom', fontsize=9)

        st.pyplot(fig)

    with col2:
        st.subheader("일일 매출 추이")
        fig, ax = plt.subplots(figsize=(10, 6))

        for cat, color in zip(prime_cat, ['#0052CC', '#1E90FF', '#4169E1']):
            daily = prime_sales.set_index('날짜')[cat]
            ax.plot(daily.index, daily.values, marker='o', label=cat, linewidth=2, color=color, alpha=0.7)

        ax.set_xlabel('날짜', fontsize=11)
        ax.set_ylabel('매출 (₩)', fontsize=11)
        ax.set_title('프라임타임 특약 카테고리별 일일 추이', fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='best', fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₩{int(x/1e6)}M'))
        plt.xticks(rotation=45)
        st.pyplot(fig)

# 하단 정보
st.markdown("---")
st.caption(f"📅 데이터 기준: 2026년 5월 | 마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
