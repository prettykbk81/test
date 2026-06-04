# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json

# matplotlib 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 페이지 설정
st.set_page_config(page_title="홈앤쇼핑 편성표 대시보드", layout="wide")

# ===== Supabase 연결 설정 =====
SUPABASE_URL = "https://ishipuyszpeeayvnhehb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlzaGlwdXlzenBlZWF5dm5oZWhiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODA1NTQ4NzksImV4cCI6MjA5NjEzMDg3OX0.vWyyFrlRVzjKCPBzUVxG7qXz7r-M0B2wEVQ905FR9s8"

# ===== 데이터 로드 =====
@st.cache_data(ttl=3600)
def load_sales_data():
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/sales",
        headers=headers
    )

    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        raise Exception(f"API 오류: {response.status_code} - {response.text}")

try:
    df_sales = load_sales_data()

    # 제목
    st.title("📊 홈앤쇼핑 편성표 대시보드")
    st.markdown("---")

    # 기본 통계
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("총 편성 상품", len(df_sales))
    with col2:
        st.metric("쇼핑 채널", df_sales['shopping_channel'].nunique())
    with col3:
        st.metric("상품 카테고리", df_sales['category'].nunique())
    with col4:
        st.metric("출연진", df_sales['cast_member'].nunique())

    st.markdown("---")

    # 탭 생성
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["전체 현황", "채널별 분석", "카테고리별 분석", "시간대별 분석", "데이터 조회"])

    # ===== TAB 1: 전체 현황 =====
    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("채널별 편성 상품 수")
            channel_counts = df_sales['shopping_channel'].value_counts()

            fig, ax = plt.subplots(figsize=(10, 6))
            colors = ['#0052CC', '#1E90FF', '#4169E1', '#6495ED', '#87CEEB']
            ax.bar(channel_counts.index, channel_counts.values, color=colors[:len(channel_counts)])
            ax.set_ylabel('상품 수', fontsize=11)
            ax.set_title('홈쇼핑사별 편성 상품 수', fontsize=14, fontweight='bold', pad=20)
            plt.xticks(rotation=45)

            for i, v in enumerate(channel_counts.values):
                ax.text(i, v, str(v), ha='center', va='bottom', fontsize=10, fontweight='bold')

            st.pyplot(fig)

        with col2:
            st.subheader("카테고리별 편성 상품 수")
            category_counts = df_sales['category'].value_counts()

            fig, ax = plt.subplots(figsize=(10, 6))
            colors = ['#0052CC', '#1E90FF', '#4169E1', '#6495ED', '#87CEEB']
            ax.bar(category_counts.index, category_counts.values, color=colors[:len(category_counts)])
            ax.set_ylabel('상품 수', fontsize=11)
            ax.set_title('카테고리별 편성 상품 수', fontsize=14, fontweight='bold', pad=20)
            plt.xticks(rotation=45)

            for i, v in enumerate(category_counts.values):
                ax.text(i, v, str(v), ha='center', va='bottom', fontsize=10, fontweight='bold')

            st.pyplot(fig)

        st.markdown("---")
        st.subheader("채널별 카테고리 분포")
        pivot_table = pd.crosstab(df_sales['shopping_channel'], df_sales['category'])

        fig, ax = plt.subplots(figsize=(14, 6))
        pivot_table.plot(kind='bar', ax=ax, color=['#0052CC', '#1E90FF', '#4169E1', '#6495ED', '#87CEEB'])
        ax.set_ylabel('상품 수', fontsize=11)
        ax.set_xlabel('채널', fontsize=11)
        ax.set_title('홈쇼핑사별 카테고리 분포', fontsize=14, fontweight='bold', pad=20)
        ax.legend(title='카테고리', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(rotation=45)

        st.pyplot(fig)

    # ===== TAB 2: 채널별 분석 =====
    with tab2:
        st.subheader("채널별 편성 현황")

        selected_channel = st.selectbox("채널 선택", df_sales['shopping_channel'].unique())
        channel_data = df_sales[df_sales['shopping_channel'] == selected_channel]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("편성 상품 수", len(channel_data))
        with col2:
            st.metric("카테고리 수", channel_data['category'].nunique())
        with col3:
            st.metric("출연진 수", channel_data['cast_member'].nunique())

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("카테고리 분포")
            cat_dist = channel_data['category'].value_counts()

            fig, ax = plt.subplots(figsize=(8, 6))
            colors = ['#0052CC', '#1E90FF', '#4169E1', '#6495ED', '#87CEEB']
            ax.pie(cat_dist.values, labels=cat_dist.index, autopct='%1.1f%%',
                   colors=colors[:len(cat_dist)], startangle=90)
            ax.set_title(f'{selected_channel} - 카테고리별 비중', fontsize=12, fontweight='bold')
            st.pyplot(fig)

        with col2:
            st.subheader("시간대별 편성 수")
            time_dist = channel_data['time_slot'].value_counts().sort_index()

            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(range(len(time_dist)), time_dist.values, color='#0052CC')
            ax.set_yticks(range(len(time_dist)))
            ax.set_yticklabels(time_dist.index)
            ax.set_xlabel('상품 수', fontsize=11)
            ax.set_title(f'{selected_channel} - 시간대별 편성 수', fontsize=12, fontweight='bold')

            for i, v in enumerate(time_dist.values):
                ax.text(v, i, f' {v}', va='center', fontsize=9)

            st.pyplot(fig)

        st.markdown("---")
        st.subheader(f"{selected_channel} 편성 상품 목록")
        st.dataframe(
            channel_data[['time_slot', 'product_name', 'cast_member', 'category', 'price_range']].reset_index(drop=True),
            use_container_width=True
        )

    # ===== TAB 3: 카테고리별 분석 =====
    with tab3:
        st.subheader("카테고리별 편성 현황")

        selected_category = st.selectbox("카테고리 선택", df_sales['category'].unique())
        category_data = df_sales[df_sales['category'] == selected_category]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("편성 상품 수", len(category_data))
        with col2:
            st.metric("참여 채널", category_data['shopping_channel'].nunique())
        with col3:
            st.metric("출연진 수", category_data['cast_member'].nunique())

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("채널별 분포")
            ch_dist = category_data['shopping_channel'].value_counts()

            fig, ax = plt.subplots(figsize=(8, 6))
            colors = ['#0052CC', '#1E90FF', '#4169E1', '#6495ED', '#87CEEB']
            ax.pie(ch_dist.values, labels=ch_dist.index, autopct='%1.1f%%',
                   colors=colors[:len(ch_dist)], startangle=90)
            ax.set_title(f'{selected_category} - 채널별 비중', fontsize=12, fontweight='bold')
            st.pyplot(fig)

        with col2:
            st.subheader("가격대 분포")
            st.write(f"편성된 상품의 가격 범위:")
            st.text(category_data['price_range'].describe())

        st.markdown("---")
        st.subheader(f"{selected_category} 편성 상품 목록")
        st.dataframe(
            category_data[['shopping_channel', 'time_slot', 'product_name', 'cast_member', 'price_range']].reset_index(drop=True),
            use_container_width=True
        )

    # ===== TAB 4: 시간대별 분석 =====
    with tab4:
        st.subheader("시간대별 편성 현황")

        time_counts = df_sales['time_slot'].value_counts().sort_index()

        fig, ax = plt.subplots(figsize=(14, 6))
        colors = ['#0052CC' if i % 2 == 0 else '#1E90FF' for i in range(len(time_counts))]
        ax.bar(range(len(time_counts)), time_counts.values, color=colors)
        ax.set_xticks(range(len(time_counts)))
        ax.set_xticklabels(time_counts.index, rotation=45)
        ax.set_ylabel('상품 수', fontsize=11)
        ax.set_title('시간대별 편성 상품 수', fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3)

        for i, v in enumerate(time_counts.values):
            ax.text(i, v, str(v), ha='center', va='bottom', fontsize=9)

        st.pyplot(fig)

        st.markdown("---")

        selected_time = st.selectbox("시간대 선택", time_counts.index)
        time_data = df_sales[df_sales['time_slot'] == selected_time]

        st.subheader(f"{selected_time} 편성 상품")
        st.dataframe(
            time_data[['shopping_channel', 'product_name', 'cast_member', 'category', 'price_range']].reset_index(drop=True),
            use_container_width=True
        )

    # ===== TAB 5: 데이터 조회 =====
    with tab5:
        st.subheader("전체 데이터 조회")

        # 필터 옵션
        col1, col2, col3 = st.columns(3)

        with col1:
            filter_channel = st.multiselect(
                "채널 필터",
                df_sales['shopping_channel'].unique(),
                default=df_sales['shopping_channel'].unique()
            )

        with col2:
            filter_category = st.multiselect(
                "카테고리 필터",
                df_sales['category'].unique(),
                default=df_sales['category'].unique()
            )

        with col3:
            search_product = st.text_input("상품명 검색", "")

        # 필터 적용
        filtered_df = df_sales[
            (df_sales['shopping_channel'].isin(filter_channel)) &
            (df_sales['category'].isin(filter_category))
        ]

        if search_product:
            filtered_df = filtered_df[filtered_df['product_name'].str.contains(search_product, case=False)]

        st.metric("검색 결과", len(filtered_df))

        # 데이터 표시
        display_columns = ['shopping_channel', 'time_slot', 'product_name', 'cast_member', 'category', 'price_range']
        st.dataframe(
            filtered_df[display_columns].reset_index(drop=True),
            use_container_width=True
        )

        # CSV 다운로드
        csv_data = filtered_df[display_columns].to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="CSV 다운로드",
            data=csv_data,
            file_name="sales_data.csv",
            mime="text/csv"
        )

except Exception as e:
    st.error(f"❌ Supabase 연결 오류: {str(e)}")
    st.info("Supabase 연결을 확인해주세요.")
