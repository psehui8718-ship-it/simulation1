import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))
NuclearSimHub/
├── app.py
└── modules/
    ├── module1_neutronics.py
    ├── module2_thermal.py
    ├── module3_policy.py
    ├── module4_smr.py
    └── module5_radiation.py
streamlit
plotly
numpy
pandas
scipy
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
