import streamlit as st
import pandas as pd
from deadlock_logic import check_deadlock, bankers_algorithm

st.set_page_config(page_title="Deadlock Visualizer", layout="centered")
st.title("🔍 Deadlock Detection and Avoidance")

# Session state for reset
if "available" not in st.session_state:
    st.session_state["available"] = "0,0,0"
    st.session_state["allocation"] = "0 0 0\n0 0 0\n0 0 0"
    st.session_state["max_need"] = "0 0 0\n0 0 0\n0 0 0"

# Input: processes/resources
num_processes = st.number_input("Number of Processes", min_value=1, value=3)
num_resources = st.number_input("Number of Resources", min_value=1, value=3)

# Mode selector
mode = st.radio("Choose Algorithm", ["Deadlock Detection", "Banker's Algorithm (Avoidance)"])

# Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("🧪 Fill Example Data"):
        st.session_state["available"] = "0,0,0"
        st.session_state["allocation"] = "0 1 0\n2 0 0\n3 0 3"
        st.session_state["max_need"] = "0 1 0\n3 0 2\n3 0 3"
with col2:
    if st.button("♻️ Reset"):
        st.session_state["available"] = "0,0,0"
        st.session_state["allocation"] = "0 0 0\n0 0 0\n0 0 0"
        st.session_state["max_need"] = "0 0 0\n0 0 0\n0 0 0"

# Inputs
available_input = st.text_input("Available Resources (comma-separated)", key="available")
allocation_input = st.text_area("Allocation Matrix (rows newline-separated, values space-separated)", key="allocation")
max_input = st.text_area("Max Need Matrix (same format)", key="max_need")

if st.button("🚦 Run"):
    try:
        available = list(map(int, available_input.strip().split(',')))
        allocation = [list(map(int, row.split())) for row in allocation_input.strip().split('\n')]
        max_need = [list(map(int, row.split())) for row in max_input.strip().split('\n')]

        request = [[max_need[i][j] - allocation[i][j] for j in range(num_resources)] for i in range(num_processes)]

        # Algorithm
        if mode == "Deadlock Detection":
            result = check_deadlock(allocation, request, available)
        else:
            result = bankers_algorithm(allocation, max_need, available)

        # Result Message
        if result["safe"]:
            st.success("✅ System is Safe (No Deadlock)")
            st.info(f"🟢 Safe Sequence: {' ➝ '.join(result['sequence'])}")
        else:
            st.error("🔴 System is in Deadlock!")
            st.warning(f"⚠️ Partial Sequence: {' ➝ '.join(result['sequence']) if result['sequence'] else 'None'}")

        # Tables
        st.subheader("📋 Allocation Matrix")
        st.dataframe(pd.DataFrame(allocation, columns=[f"R{i}" for i in range(num_resources)]))

        st.subheader("📋 Max Need Matrix")
        st.dataframe(pd.DataFrame(max_need, columns=[f"R{i}" for i in range(num_resources)]))

        st.subheader("📋 Request Matrix (Max - Allocation)")
        st.dataframe(pd.DataFrame(request, columns=[f"R{i}" for i in range(num_resources)]))

        st.subheader("📋 Available Resources")
        st.dataframe(pd.DataFrame([available], columns=[f"R{i}" for i in range(num_resources)]))

    except Exception as e:
        st.error(f"⚠️ Error: {e}")

st.markdown("---")  # Adds a horizontal line
st.markdown(
    "<div style='text-align: center; font-size: 16px; color: #888;'>"
    "💡 Developed by © <b>Syeda Farzana Sultana</b>"
    "</div>",
    unsafe_allow_html=True
)
