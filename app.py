import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# -----------------------------
# 페이지 기본 설정
# -----------------------------
st.set_page_config(
    page_title="탄소중립 vs 원자력 시나리오 시뮬레이터",
    page_icon="⚛️",
    layout="wide"
)

st.title("⚛️ 탄소중립 vs 원자력 시나리오 시뮬레이터")
st.markdown("""
이 앱은 **한국의 원자력 발전 비중 변화**가  
**탄소 배출량**과 **에너지 자급률**에 어떤 영향을 주는지 시각적으로 보여줍니다.
""")

# -----------------------------
# 사용자 입력
# -----------------------------
st.sidebar.header("🔧 시나리오 설정")

nuclear_share = st.sidebar.slider("원자력 비중 (%)", 0, 100, 30)
renewable_share = st.sidebar.slider("신재생에너지 비중 (%)", 0, 100 - nuclear_share, 20)
fossil_share = 100 - (nuclear_share + renewable_share)

st.sidebar.write(f"화석연료 비중: **{fossil_share}%**")

# -----------------------------
# 단순 모델 계산
# -----------------------------
carbon_emission = fossil_share * 0.7  # 단위: MtCO₂
energy_self = nuclear_share * 0.8 + renewable_share * 1.0

data = {
    "항목": ["원자력", "신재생", "화석연료"],
    "비중(%)": [nuclear_share, renewable_share, fossil_share]
}
df = pd.DataFrame(data)

# -----------------------------
# 그래프 1: 에너지 믹스 파이차트
# -----------------------------
fig_mix = go.Figure(
    data=[go.Pie(
        labels=df["항목"],
        values=df["비중(%)"],
        hole=0.4,
        marker=dict(colors=["#3E7CB1", "#53A548", "#D94F4F"])
    )]
)
fig_mix.update_layout(title="에너지 믹스 구성 비율")

# -----------------------------
# 그래프 2: 탄소 배출량 & 자급률 변화
# -----------------------------
scenarios = ["현재(2024)", "미래 시나리오"]
carbon_values = [50, carbon_emission]
energy_self_values = [60, energy_self]

fig_compare = go.Figure()
fig_compare.add_trace(go.Bar(
    x=scenarios,
    y=carbon_values,
    name="탄소 배출량 (MtCO₂)",
    marker_color="#D94F4F"
))
fig_compare.add_trace(go.Bar(
    x=scenarios,
    y=energy_self_values,
    name="에너지 자급률 (%)",
    marker_color="#53A548"
))
fig_compare.update_layout(
    title="탄소 배출량 & 에너지 자급률 비교",
    barmode="group",
    yaxis_title="값"
)

# -----------------------------
# 결과 출력
# -----------------------------
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_mix, use_container_width=True)
with col2:
    st.plotly_chart(fig_compare, use_container_width=True)

st.markdown("---")
st.subheader("📊 결과 요약")

st.write(f"✅ **탄소 배출량:** {carbon_emission:.1f} MtCO₂")
st.write(f"✅ **에너지 자급률:** {energy_self:.1f} %")
st.info("💡 원자력과 신재생 비중을 높일수록 탄소 배출이 줄고, 자급률이 높아집니다.")
