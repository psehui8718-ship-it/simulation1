import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# -----------------------------
# 페이지 기본 설정
# -----------------------------
st.set_page_config(
    page_title="원자력 기술 시각화 대시보드",
    page_icon="⚛️",
    layout="wide"
)

st.title("⚛️ 원자력 기술 시각화 통합 대시보드")
st.markdown("""
이 앱은 두 가지 모드를 제공합니다 👇  
1️⃣ **탄소중립 vs 원자력 시나리오 시뮬레이터**  
2️⃣ **소형모듈원자로(SMR) 기술 체험형 대시보드**
""")

# -----------------------------
# 사이드바 기능 선택
# -----------------------------
mode = st.sidebar.selectbox(
    "🔧 기능 선택",
    ["탄소중립 vs 원자력 시나리오 시뮬레이터", "SMR 기술 체험형 대시보드"]
)

# =========================================================
# [1] 탄소중립 vs 원자력 시나리오 시뮬레이터
# =========================================================
if mode == "탄소중립 vs 원자력 시나리오 시뮬레이터":
    st.header("🌍 탄소중립 vs 원자력 시나리오 시뮬레이터")
    st.markdown("""
    원자력과 신재생 비중을 조절하면서  
    탄소 배출량과 에너지 자급률의 변화를 시각적으로 탐색해보세요.
    """)

    # -----------------------------
    # 사용자 입력
    # -----------------------------
    st.sidebar.header("⚙️ 시나리오 설정")

    nuclear_share = st.sidebar.slider("원자력 비중 (%)", 0, 100, 30)
    renewable_share = st.sidebar.slider("신재생에너지 비중 (%)", 0, 100 - nuclear_share, 20)
    fossil_share = 100 - (nuclear_share + renewable_share)

    st.sidebar.write(f"화석연료 비중: **{fossil_share}%**")

    # -----------------------------
    # 계산
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

# =========================================================
# [2] SMR 기술 체험형 대시보드
# =========================================================
elif mode == "SMR 기술 체험형 대시보드":
    st.header("🔋 소형모듈원자로(SMR) 기술 체험형 대시보드")
    st.markdown("""
    **SMR(Small Modular Reactor)** 은 차세대 원자력 기술로,  
    소형화·모듈화되어 설치가 빠르고 안전성이 높은 원자로입니다.  
    아래에서 SMR의 특징과 세계 적용 현황을 살펴보세요.
    """)

    # -----------------------------
    # SMR 개요
    # -----------------------------
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💡 주요 특징")
        st.markdown("""
        - 🔹 **소형화**: 대형 원전의 1/10 규모, 다양한 지역에 설치 가능  
        - 🔹 **모듈형 설계**: 공장에서 제작 후 현장 조립, 시공 기간 단축  
        - 🔹 **고안전성**: 수동안전계통(Passive Safety)으로 냉각 유지  
        - 🔹 **경제성**: 초기 투자비는 낮고, 유지·보수가 간편함  
        - 🔹 **탄소중립 기여**: 온실가스 배출이 거의 없음
        """)
    with col2:
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/2/28/NuScale_Power_Module_Illustration.png",
            caption="NuScale SMR 모듈 예시 (출처: Wikipedia)",
            use_column_width=True
        )

    # -----------------------------
    # SMR vs 대형 원전 비교
    # -----------------------------
    st.header("⚙️ SMR vs 대형 원전 기술 비교")

    comparison_data = pd.DataFrame({
        "항목": ["출력 규모(MWe)", "건설 기간(년)", "안전성(점수)", "단위당 발전비용(억 원/MWe)", "탄소 배출량(지수)"],
        "대형 원전": [1400, 10, 80, 1.0, 100],
        "SMR": [300, 3, 95, 1.2, 10]
    })

    fig_compare = go.Figure()
    for col in ["대형 원전", "SMR"]:
        fig_compare.add_trace(go.Bar(
            x=comparison_data["항목"],
            y=comparison_data[col],
            name=col
        ))

    fig_compare.update_layout(
        title="SMR과 대형 원전의 기술 비교",
        barmode="group",
        yaxis_title="값 (상대 비교)",
        legend_title="구분"
    )

    st.plotly_chart(fig_compare, use_container_width=True)

    # -----------------------------
    # 세계 주요 SMR 프로젝트
    # -----------------------------
    st.header("🌍 세계 주요 SMR 프로젝트 지도")

    smr_projects = pd.DataFrame({
        "국가": ["미국", "영국", "한국", "캐나다", "러시아"],
        "프로젝트명": ["NuScale Power", "Rolls-Royce SMR", "SMART", "ARC-100", "Akademik Lomonosov"],
        "위도": [44.0, 53.5, 36.3, 56.1, 69.7],
        "경도": [-123.0, -1.5, 128.0, -94.7, 33.0],
        "상태": ["시범운전 준비", "개발 중", "상용화 연구", "건설 준비", "운영 중"]
    })

    selected_country = st.selectbox("국가 선택", smr_projects["국가"].unique())
    filtered = smr_projects[smr_projects["국가"] == selected_country]

    st.map(filtered, latitude="위도", longitude="경도", size=80)

    st.markdown(f"**{selected_country}** 의 주요 SMR 프로젝트:")
    st.dataframe(filtered[["프로젝트명", "상태"]])

    st.header("📊 결론 요약")
    st.success("""
    ✅ **SMR은 원자력의 미래형 모델**로,  
    소형·안전·모듈형 설계를 통해 설치 유연성과 경제성을 동시에 확보합니다.  
    향후 탄소중립 에너지 전환의 핵심 기술로 주목받고 있습니다.
    """)
