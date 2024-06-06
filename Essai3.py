import streamlit as st
import pandas as pd
import numpy as np
import time

# Function to simulate real-time data
def generate_real_time_data():
    mttr_hours = np.random.randint(3, 8)
    mttr_percentage_change = np.random.uniform(-10, 10)
    mtbf_hours = np.random.randint(8, 15)
    mtbf_percentage_change = np.random.uniform(-10, 10)
    quality = np.random.uniform(85, 95)
    performance = np.random.uniform(85, 95)
    availability = np.random.uniform(75, 85)
    oee = (quality * performance * availability) / 10000

    return {
        "mttr": {"Hours": mttr_hours, "Percentage Change": mttr_percentage_change},
        "mtbf": {"Hours": mtbf_hours, "Percentage Change": mtbf_percentage_change},
        "oee": {"OEE": oee, "Quality": quality, "Performance": performance, "Availability": availability},
    }

# Initialize the table for maintenance actions
if 'maintenance_actions' not in st.session_state:
    st.session_state.maintenance_actions = pd.DataFrame(columns=['Action', 'Frequency', 'Maintained'])

# Header
st.title("Maintenance KPIs Dashboard")

# Main loop to simulate real-time data
data = generate_real_time_data()

# MTTR and MTBF Visualization
st.header("Maintenance KPIs")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Mean Time to Repair (MTTR)")
    st.metric("MTTR Hours", data["mttr"]["Hours"])
    st.metric("MTTR Change", f"{data['mttr']['Percentage Change']:.2f}%")
    st.bar_chart(pd.DataFrame({'Hours': [data["mttr"]["Hours"]], 'Percentage Change': [data["mttr"]["Percentage Change"]]}))

with col2:
    st.subheader("Mean Time Between Failures (MTBF)")
    st.metric("MTBF Hours", data["mtbf"]["Hours"])
    st.metric("MTBF Change", f"{data['mtbf']['Percentage Change']:.2f}%")
    st.bar_chart(pd.DataFrame({'Hours': [data["mtbf"]["Hours"]], 'Percentage Change': [data["mtbf"]["Percentage Change"]]}))

# OEE Visualization
st.header("Overall Equipment Effectiveness (OEE)")

col3, col4 = st.columns(2)
with col3:
    oee_value = data["oee"]["OEE"]
    quality_value = data["oee"]["Quality"]
    performance_value = data["oee"]["Performance"]
    availability_value = data["oee"]["Availability"]

    st.metric("OEE", f"{oee_value:.2f}%")
    st.bar_chart(pd.DataFrame({'Quality': [quality_value], 'Performance': [performance_value], 'Availability': [availability_value]}))

with col4:
    st.subheader("OEE Breakdown")
    st.write(f"Quality: {quality_value:.2f}%")
    st.write(f"Performance: {performance_value:.2f}%")
    st.write(f"Availability: {availability_value:.2f}%")

# Table for Maintenance Actions
st.header("Maintenance Actions")

action = st.text_input("Action")
frequency = st.number_input("Frequency", min_value=1)
maintained = st.checkbox("Maintained")

if st.button("Add Action"):
    new_action = {'Action': action, 'Frequency': frequency, 'Maintained': maintained}
    st.session_state.maintenance_actions = st.session_state.maintenance_actions.append(new_action, ignore_index=True)

st.dataframe(st.session_state.maintenance_actions)

# Planned and Realized Actions Curve
st.header("Planned vs Realized Actions")
planned_actions = st.session_state.maintenance_actions['Frequency'].sum()
realized_actions = st.session_state.maintenance_actions[st.session_state.maintenance_actions['Maintained'] == True]['Frequency'].sum()
planned_vs_realized = pd.DataFrame({'Planned Actions': [planned_actions], 'Realized Actions': [realized_actions]})

st.line_chart(planned_vs_realized)

# PMP Calculation
st.header("Planned Maintenance Percentage (PMP)")
if planned_actions > 0:
    pmp_value = (realized_actions / planned_actions) * 100
else:
    pmp_value = 0

st.metric("PMP", f"{pmp_value:.2f}%")

# Wait for a while before updating the data
time.sleep(5)
