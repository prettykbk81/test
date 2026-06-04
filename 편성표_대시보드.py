# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# matplotlib 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 페이지 설정
st.set_page_config(page_title="홈쇼핑 6월 4일 편성표", layout="wide")

# 제목
st.title("📺 6월 4일 홈쇼핑 편성표")
st.markdown("---")

# 통합 편성표 데이터 로드
full_df = pd.read_csv('편성표_통합_6월4일.csv')

# 홈쇼핑사 선택
all_homeshows = sorted(full_df['홈쇼핑사'].unique())

col1, col2 = st.columns([3, 1])

with col1:
    selected_homeshows = st.multiselect(
        "보고 싶은 홈쇼핑사를 선택하세요 (여러 개 선택 가능)",
        all_homeshows,
        default=all_homeshows
    )

with col2:
    if st.button("전체 선택", use_container_width=True):
        selected_homeshows = all_homeshows
        st.rerun()
    if st.button("전체 해제", use_container_width=True):
        selected_homeshows = []
        st.rerun()

st.markdown("---")

# 선택된 홈쇼핑사의 데이터
if selected_homeshows:
    filtered_df = full_df[full_df['홈쇼핑사'].isin(selected_homeshows)]

    # 메트릭 표시
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("총 프로그램 수", len(filtered_df))

    with col2:
        st.metric("홈쇼핑사 수", len(selected_homeshows))

    with col3:
        avg_price = int(filtered_df['예상가격'].str.split('-').str[1].astype(int).mean())
        st.metric("평균 가격대", f"₩{avg_price:,}")

    with col4:
        categories = filtered_df['카테고리'].nunique()
        st.metric("카테고리 수", categories)

    with col5:
        max_price = filtered_df['예상가격'].str.split('-').str[1].astype(int).max()
        st.metric("최고 가격", f"₩{max_price:,}")

    st.markdown("---")

    # 편성표 테이블
    st.subheader(f"📅 편성표 ({''.join(selected_homeshows)})")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "홈쇼핑사": st.column_config.TextColumn("홈쇼핑사", width=120),
            "시간": st.column_config.TextColumn("시간", width=100),
            "상품명": st.column_config.TextColumn("상품명", width=180),
            "출연진": st.column_config.TextColumn("출연진", width=100),
            "예상가격": st.column_config.TextColumn("예상가격", width=120),
            "카테고리": st.column_config.TextColumn("카테고리", width=100),
        }
    )

    st.markdown("---")

    # 분석 차트
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("홈쇼핑사별 프로그램 수")

        homeshow_counts = filtered_df['홈쇼핑사'].value_counts().sort_index()

        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#0052CC', '#1E90FF', '#4169E1', '#6495ED', '#87CEEB']
        bars = ax.bar(homeshow_counts.index, homeshow_counts.values, color=colors[:len(homeshow_counts)])
        ax.set_ylabel('프로그램 수', fontsize=11)
        ax.set_title('홈쇼핑사별 프로그램 분포', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        plt.xticks(rotation=45)

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom', fontsize=10)

        st.pyplot(fig)

    with col2:
        st.subheader("카테고리별 프로그램 수")

        category_counts = filtered_df['카테고리'].value_counts().sort_values(ascending=True)

        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#0052CC', '#1E90FF', '#4169E1', '#6495ED', '#87CEEB']
        ax.barh(category_counts.index, category_counts.values, color=colors[:len(category_counts)])
        ax.set_xlabel('프로그램 수', fontsize=11)
        ax.set_title('카테고리별 프로그램 분포', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')

        for i, v in enumerate(category_counts.values):
            ax.text(v + 0.2, i, str(int(v)), va='center', fontsize=10)

        st.pyplot(fig)

    st.markdown("---")

    # 시간대별 카테고리별 프로그램 분포
    st.subheader("시간대별 카테고리별 프로그램 분포")

    # 시간대 추출
    filtered_df_copy = filtered_df.copy()
    filtered_df_copy['시작시간'] = filtered_df_copy['시간'].str.split('-').str[0]

    # Pivot table 생성
    pivot_table = filtered_df_copy.pivot_table(
        index='카테고리',
        columns='시작시간',
        aggfunc='size',
        fill_value=0
    )

    # 정렬 (시간 순서대로)
    pivot_table = pivot_table.reindex(sorted(pivot_table.columns), axis=1)

    # 표 표시
    st.dataframe(
        pivot_table,
        use_container_width=True,
        column_config={col: st.column_config.NumberColumn(col, format="%d") for col in pivot_table.columns}
    )

    st.markdown("---")

    # 시간대별 카테고리 분포 차트
    fig, ax = plt.subplots(figsize=(14, 6))

    x = range(len(pivot_table.columns))
    colors = ['#0052CC', '#1E90FF', '#4169E1', '#6495ED', '#87CEEB', '#ADD8E6']

    for i, category in enumerate(pivot_table.index):
        ax.plot(x, pivot_table.loc[category].values, marker='o', linewidth=2.5, markersize=8,
                label=category, color=colors[i % len(colors)])

    ax.set_xticks(x)
    ax.set_xticklabels(pivot_table.columns, rotation=45)
    ax.set_ylabel('프로그램 수', fontsize=11)
    ax.set_xlabel('방송 시간', fontsize=11)
    ax.set_title('시간대별 카테고리별 프로그램 분포', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)

    st.pyplot(fig)

    st.markdown("---")

    # 홈쇼핑사별 상세 통계
    st.subheader("홈쇼핑사별 상세 통계")

    comparison_data = []
    for name in selected_homeshows:
        data = filtered_df[filtered_df['홈쇼핑사'] == name]
        comparison_data.append({
            '홈쇼핑사': name,
            '프로그램 수': len(data),
            '카테고리 수': data['카테고리'].nunique(),
            '평균 가격': int(data['예상가격'].str.split('-').str[1].astype(int).mean()),
            '최고 가격': data['예상가격'].str.split('-').str[1].astype(int).max(),
            '최저 가격': data['예상가격'].str.split('-').str[0].astype(int).min(),
        })

    comparison_df = pd.DataFrame(comparison_data)

    st.dataframe(
        comparison_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "홈쇼핑사": st.column_config.TextColumn("홈쇼핑사", width=120),
            "프로그램 수": st.column_config.NumberColumn("프로그램 수", width=100),
            "카테고리 수": st.column_config.NumberColumn("카테고리 수", width=100),
            "평균 가격": st.column_config.NumberColumn("평균 가격", width=120, format="₩%d"),
            "최고 가격": st.column_config.NumberColumn("최고 가격", width=120, format="₩%d"),
            "최저 가격": st.column_config.NumberColumn("최저 가격", width=120, format="₩%d"),
        }
    )

else:
    st.warning("선택한 홈쇼핑사가 없습니다. 위에서 홈쇼핑사를 선택해주세요.")

st.markdown("---")
st.caption(f"📅 편성표 기준: 2026년 6월 4일 | 마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
