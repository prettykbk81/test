import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="홈앤쇼핑 및 홈쇼핑 일일 매출 현황",
    layout="wide",
    initial_sidebar_state="collapsed"
)

@st.cache_data
def load_and_simulate_data():
    df = pd.read_csv('sales.csv', encoding='utf-8-sig')

    def parse_price(price_str):
        low, high = map(int, price_str.split('-'))
        return (low + high) / 2

    df['mid_price'] = df['예상가격'].apply(parse_price)

    np.random.seed(42)
    today = datetime.now().date()
    dates = [today - timedelta(days=i) for i in range(30)]
    dates.reverse()

    category_multiplier = {
        '건강식품': 1.5,
        '이미용': 1.3,
        '일반식품': 1.2,
        '패션': 1.0,
        '리빙': 0.9
    }

    records = []
    for date in dates:
        for _, row in df.iterrows():
            base_qty = max(10, 200 / row['mid_price'] * 100)
            cat_mult = category_multiplier.get(row['카테고리'], 1.0)

            weekday = date.weekday()
            weekend_mult = 1.2 if weekday in [5, 6] else 1.0

            noise = np.random.normal(1.0, 0.15)
            qty = int(base_qty * cat_mult * weekend_mult * noise)
            qty = max(1, qty)

            revenue = row['mid_price'] * qty

            records.append({
                '날짜': date,
                '홈쇼핑사': row['홈쇼핑사'],
                '상품명': row['상품명'],
                '카테고리': row['카테고리'],
                '가격': row['mid_price'],
                '수량': qty,
                '매출': revenue
            })

    return pd.DataFrame(records)

def fmt_krw(n):
    return f"₩{n:,.0f}"

df = load_and_simulate_data()

st.markdown("""
<h1 style='text-align: center; color: #1E6FBB; font-family: Malgun Gothic, NanumGothic, serif;'>
홈앤쇼핑 및 홈쇼핑 일일 매출 현황
</h1>
""", unsafe_allow_html=True)

today = df['날짜'].max()
yesterday = today - timedelta(days=1)

today_revenue = df[df['날짜'] == today]['매출'].sum()
yesterday_revenue = df[df['날짜'] == yesterday]['매출'].sum()
change_rate = ((today_revenue - yesterday_revenue) / yesterday_revenue * 100) if yesterday_revenue > 0 else 0

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "오늘 매출",
        fmt_krw(today_revenue),
        delta=None,
        label_visibility="visible"
    )

with col2:
    st.metric(
        "어제 매출",
        fmt_krw(yesterday_revenue),
        delta=None,
        label_visibility="visible"
    )

with col3:
    delta_color = "off" if change_rate >= 0 else "inverse"
    st.metric(
        "어제 대비 증감률",
        f"{change_rate:+.1f}%",
        delta=None,
        label_visibility="visible"
    )

st.divider()

daily_revenue = df.groupby('날짜')['매출'].sum().reset_index()
daily_revenue['날짜_str'] = daily_revenue['날짜'].dt.strftime('%m월 %d일')

fig_line = px.line(
    daily_revenue,
    x='날짜',
    y='매출',
    markers=True,
    title='일별 매출 추이',
    labels={'날짜': '날짜', '매출': '매출'},
    line_shape='linear'
)

fig_line.update_traces(
    line=dict(color='#1E6FBB', width=2),
    marker=dict(size=8, color='#1E6FBB'),
    hovertemplate='<b>%{x|%m월 %d일}</b><br>매출: ' +
                  df.groupby('날짜')['매출'].sum().apply(fmt_krw).values[0] +
                  '<extra></extra>'
)

fig_line.update_layout(
    font=dict(family="Malgun Gothic, NanumGothic, sans-serif", size=12),
    hovermode='x unified',
    title_font_size=16,
    yaxis_title='매출 (원)',
    xaxis_title='',
    height=400,
    plot_bgcolor='rgba(240,240,240,0.5)',
    paper_bgcolor='white'
)

fig_line.update_yaxes(tickformat=',.0f')

category_revenue = df.groupby('카테고리')['매출'].sum().reset_index()
category_revenue = category_revenue.sort_values('매출', ascending=False)

colors = ["#1E6FBB", "#3A8FD4", "#5AAEE0", "#7ECAEE", "#A8DCEF"]

fig_pie = go.Figure(data=[go.Pie(
    labels=category_revenue['카테고리'],
    values=category_revenue['매출'],
    marker=dict(colors=colors[:len(category_revenue)]),
    textposition='inside',
    textinfo='label+percent',
    hovertemplate='<b>%{label}</b><br>매출: ₩%{value:,.0f}<extra></extra>'
)])

fig_pie.update_layout(
    title='카테고리별 매출 비중 (30일 누계)',
    font=dict(family="Malgun Gothic, NanumGothic, sans-serif", size=12),
    title_font_size=16,
    height=400,
    paper_bgcolor='white'
)

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.plotly_chart(fig_line, use_container_width=True)

with col_chart2:
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

with st.expander("데이터 보기"):
    st.dataframe(
        df.assign(매출_표시=df['매출'].apply(fmt_krw))
        .drop(columns=['매출'])
        .rename(columns={'매출_표시': '매출', '가격': '단가'})
        [['날짜', '홈쇼핑사', '상품명', '카테고리', '단가', '수량', '매출']],
        use_container_width=True,
        hide_index=True
    )
