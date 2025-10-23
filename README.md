import streamlit as st
from modules import (
    module1_neutronics,
    module2_thermal,
    module3_policy,
    module4_smr,
    module5_radiation
)

st.set_page_config(page_title="NuclearSimHub", page_icon="⚛", layout="wide")

st.title("⚛ NuclearSimHub - 원자력 시뮬레이션 체험 플랫폼")
st.markdown("""
이 앱은 **5가지 원자력 분야 시뮬레이션**을 체험할 수 있는 교육·연구용 도구입니다.  
사전에 정의된 간단한 모델을 통해 한국형 원자력 시스템의 기술적, 정책적, 안전적 측면을 확인할 수 있습니다.
""")

menu = st.sidebar.selectbox(
    "시뮬레이션 주제 선택",
    [
        "1️⃣ 중성자 수송 해석",
        "2️⃣ 열수력 시뮬레이션",
        "3️⃣ 에너지 정책 분석",
        "4️⃣ 소형모듈원자로(SMR) 안정성",
        "5️⃣ 방사선 감쇠 시뮬레이션"
    ]
)

if menu.startswith("1"):
    module1_neutronics.run()
elif menu.startswith("2"):
    module2_thermal.run()
elif menu.startswith("3"):
    module3_policy.run()
elif menu.startswith("4"):
    module4_smr.run()
elif menu.startswith("5"):
    module5_radiation.run()
    import streamlit as st
import numpy as np
import plotly.graph_objects as go

def run():
    st.subheader("🔬 중성자 수송 해석 (Neutronics Simulation)")
    st.write("단순화된 모델을 통해 연료 농축도에 따른 임계도(k-effective)를 계산합니다.")

    enrichment = st.slider("연료 농축도 (U-235 wt%)", 1.0, 5.0, 3.0, 0.1)

    # 단순 가정 모델: k_eff = a * enrichment - b * leakage
    leakage_factor = st.slider("누설 계수", 0.01, 0.05, 0.03)
    k_eff = 0.9 + 0.05 * enrichment - 10 * leakage_factor

    st.metric(label="임계도 (k-effective)", value=f"{k_eff:.3f}")
    st.write("k-effective > 1.0 → 임계상태, k-effective < 1.0 → 비임계상태")

    x = np.linspace(0, 10, 100)
    flux = np.exp(-x * (1.1 - k_eff))  # 단순 감쇠 모델

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=flux, mode='lines', name='중성자속'))
    fig.update_layout(title="중성자속 분포 (가상의 연료 셀)", xaxis_title="거리 (cm)", yaxis_title="상대 중성자속")
    st.plotly_chart(fig, use_container_width=True)
import streamlit as st
import numpy as np
import plotly.express as px

def run():
    st.subheader("🌡 열수력 시뮬레이션 (Thermal-Hydraulics)")
    st.write("냉각재 유량에 따른 연료 온도 분포 변화를 단순 모델로 시뮬레이션합니다.")

    flow_rate = st.slider("냉각재 유량 (kg/s)", 100, 1000, 500, 50)
    power = st.slider("출력 (MW)", 1000, 4000, 2800, 100)

    temp_core = 300 + (power / flow_rate) * 2.5
    st.metric(label="평균 연료 온도 (°C)", value=f"{temp_core:.2f}")

    z = np.linspace(0, 4, 100)  # 노심 높이 (m)
    temp_profile = temp_core + 10 * np.sin(z * np.pi / 4)

    fig = px.line(x=z, y=temp_profile, title="노심 내 온도 분포", labels={'x':'높이 (m)', 'y':'온도 (°C)'})
    st.plotly_chart(fig, use_container_width=True)
import streamlit as st
import pandas as pd
import plotly.express as px

def run():
    st.subheader("🏛 에너지 믹스 시뮬레이션")
    st.write("원자력 발전 비중 변화가 탄소 배출량에 미치는 영향을 단순화된 모델로 시각화합니다.")

    nuclear_share = st.slider("원자력 발전 비중 (%)", 20, 80, 30, 5)

    co2_emission = 300 - (nuclear_share - 20) * 3
    st.metric(label="예상 탄소배출량 (MtCO₂/yr)", value=f"{co2_emission:.1f}")

    mix = pd.DataFrame({
        "원자력비중(%)": [20, 30, 40, 50, 60, 70, 80],
        "CO₂배출량(MtCO₂)": [300 - (x - 20)*3 for x in [20,30,40,50,60,70,80]]
    })

    fig = px.line(mix, x="원자력비중(%)", y="CO₂배출량(MtCO₂)",
                  title="원자력 비중 변화에 따른 탄소 배출량 변화",
                  markers=True)
    st.plotly_chart(fig, use_container_width=True)
import streamlit as st
import numpy as np
import plotly.graph_objects as go

def run():
    st.subheader("⚙️ 소형모듈원자로(SMR) 안정성 시뮬레이션")
    st.write("자연 순환 냉각 시스템의 열적 안정성을 간단히 시뮬레이션합니다.")

    power = st.slider("출력 (MW)", 50, 300, 150, 10)
    area = st.slider("열교환 면적 (m²)", 100, 500, 250, 10)

    # 간단한 시간 응답 모델: T(t) = T₀ + (P/A)*exp(-t/τ)
    t = np.linspace(0, 1000, 200)
    tau = 300
    temp = 300 + (power / area) * (1 - np.exp(-t / tau))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=temp, mode='lines', name='온도 응답'))
    fig.update_layout(title="SMR 자연순환 열응답", xaxis_title="시간 (s)", yaxis_title="온도 (°C)")
    st.plotly_chart(fig, use_container_width=True)
import streamlit as st
import numpy as np
import plotly.express as px

def run():
    st.subheader("☢️ 방사선 감쇠 시뮬레이션")
    st.write("감마선이 차폐재를 통과할 때의 감쇠를 계산합니다.")

    material = st.selectbox("차폐재 종류", ["콘크리트", "납", "철", "물"])
    thickness = st.slider("차폐재 두께 (cm)", 1, 100, 20, 1)

    mu_values = {"콘크리트": 0.08, "납": 0.55, "철": 0.45, "물": 0.07}
    mu = mu_values[material]

    x = np.linspace(0, 100, 100)
    I0 = 1.0
    I = I0 * np.exp(-mu * x)

    transmission = np.exp(-mu * thickness) * 100
    st.metric(label="투과율 (%)", value=f"{transmission:.3f}")

    fig = px.line(x=x, y=I, title=f"{material} 내 감마선 감쇠 곡선",
                  labels={'x':'두께 (cm)', 'y':'상대 강도 (I/I₀)'})
    st.plotly_chart(fig, use_container_width=True)
