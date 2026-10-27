import streamlit as st
import pandas as pd

st.set_page_config(page_title="농약 현장 가이드", page_icon="🌱", layout="centered")

st.title("🌱 농약·작물보호제 현장 검색기")

# 데이터 불러오기
@st.cache_data
def load_data():
    return pd.read_csv("pesticide_data.csv")

df = load_data()

# 모바일 검색 필터
col1, col2 = st.columns(2)
with col1:
    selected_crop = st.selectbox("작물 선택", df["작물"].unique())

filtered_diseases = df[df["작물"] == selected_crop]["병해충"].unique()
with col2:
    selected_disease = st.selectbox("병해충 선택", filtered_diseases)

# 검색 결과
results = df[(df["작물"] == selected_crop) & (df["병해충"] == selected_disease)]
st.markdown(f"### 📋 검색 결과 ({len(results)}건)")

for _, row in results.iterrows():
    with st.expander(f"💊 [{row['카테고리']}] {row['상표명']} ({row['품목명']})", expanded=True):
        st.write(f"**· 사용 시기:** {row['사용시기']}")
        st.write(f"**· 희석 배수:** {row['희석배수']}배")
        st.write(f"**· 사용 방법:** {row['사용방법']}")

# 현장 희석 계산기
st.markdown("---")
st.subheader("🧮 현장 희석 계산기")
tank_capacity = st.number_input("약통 용량 (L)", value=20.0, step=5.0)
ratio = st.number_input("희석 배수", value=2000, step=100)

required_amount = (tank_capacity * 1000) / ratio
st.info(f"💡 **필요 약제량:** 약 **{required_amount:.1f} mL (g)**")
