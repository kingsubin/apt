import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(page_title="아파트 가격 동향", layout="wide")

# 제목
st.title("📊 아파트 가격 동향 대시보드")

# 사이드바 - 지역 선택
st.sidebar.header("필터 옵션")
selected_region = st.sidebar.selectbox(
    "지역 선택",
    ["서울", "경기", "인천", "부산", "대구", "광주", "대전"]
)

# 날짜 범위 선택
date_range = st.sidebar.date_input(
    "기간 선택",
    value=(datetime.now() - timedelta(days=365), datetime.now()),
    max_value=datetime.now()
)

# 가상의 데이터 생성 (실제 구현시에는 실제 데이터베이스나 API 사용)
@st.cache_data
def load_data():
    dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='M')
    data = {
        '날짜': dates,
        '서울': [100000, 98000, 97000, 96000, 97500, 98500, 99000, 101000, 102000, 101500, 102500, 103000],
        '경기': [80000, 79000, 78500, 77000, 77500, 78500, 79000, 80000, 81000, 80500, 81500, 82000],
        '인천': [70000, 69000, 68500, 68000, 68500, 69500, 70000, 71000, 72000, 71500, 72500, 73000],
        '부산': [75000, 74000, 73500, 73000, 73500, 74500, 75000, 76000, 77000, 76500, 77500, 78000],
        '대구': [72000, 71000, 70500, 70000, 70500, 71500, 72000, 73000, 74000, 73500, 74500, 75000],
        '광주': [68000, 67000, 66500, 66000, 66500, 67500, 68000, 69000, 70000, 69500, 70500, 71000],
        '대전': [69000, 68000, 67500, 67000, 67500, 68500, 69000, 70000, 71000, 70500, 71500, 72000],
    }
    return pd.DataFrame(data)

data = load_data()

# 메인 페이지 레이아웃
col1, col2 = st.columns([2, 1])

with col1:
    # 가격 추세 그래프
    st.subheader("지역별 아파트 가격 추세")
    fig = px.line(data, x='날짜', y=selected_region,
                  title=f'{selected_region} 지역 아파트 평균 가격 추이',
                  labels={'value': '평균 가격(만원/3.3㎡)', '날짜': '날짜'})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # 통계 정보
    st.subheader("가격 통계 정보")
    latest_price = data[selected_region].iloc[-1]
    price_change = data[selected_region].iloc[-1] - data[selected_region].iloc[-2]
    price_change_percent = (price_change / data[selected_region].iloc[-2]) * 100

    st.metric(
        label="현재 평균 가격",
        value=f"{latest_price:,.0f}만원",
        delta=f"{price_change:,.0f}만원 ({price_change_percent:.1f}%)"
    )

    # 가격 분석
    st.write("### 가격 분석")
    st.write(f"최고가: {data[selected_region].max():,.0f}만원")
    st.write(f"최저가: {data[selected_region].min():,.0f}만원")
    st.write(f"평균가: {data[selected_region].mean():,.0f}만원")

# 상세 데이터 테이블
st.write("### 상세 데이터")
st.dataframe(data[['날짜', selected_region]].style.highlight_max(subset=[selected_region]))

# 데이터 다운로드 버튼
csv = data.to_csv(index=False)
st.download_button(
    label="데이터 다운로드 (CSV)",
    data=csv,
    file_name=f'apartment_prices_{selected_region}.csv',
    mime='text/csv'
)