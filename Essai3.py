import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
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

# Initialize the table for maintenance actions and KPI data storage with pre-existing values
if 'maintenance_actions' not in st.session_state:
    st.session_state.maintenance_actions = pd.DataFrame([
        {'Action': 'Lubrication', 'Frequency': 5, 'Maintained': True},
        {'Action': 'Inspection', 'Frequency': 3, 'Maintained': False},
        {'Action': 'Replacement', 'Frequency': 2, 'Maintained': True},
    ])

if 'kpi_data' not in st.session_state:
    st.session_state.kpi_data = {
        'mttr': [5, 6, 4, 7],
        'mtbf': [10, 12, 11, 9],
        'time': ["10:00", "10:05", "10:10", "10:15"]
    }

# Header
st.title("Preventive Maintenance Plan Dashboard")

# Simulate real-time data
data = generate_real_time_data()

# Update KPI data storage
current_time = time.strftime("%H:%M:%S")
st.session_state.kpi_data['mttr'].append(data["mttr"]["Hours"])
st.session_state.kpi_data['mtbf'].append(data["mtbf"]["Hours"])
st.session_state.kpi_data['time'].append(current_time)

# MTTR and MTBF Visualization
st.header("Maintenance KPIs")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Mean Time to Repair (MTTR)")
    delta_color = "inverse" if data["mttr"]["Percentage Change"] < 0 else "normal"
    st.metric("MTTR Hours", data["mttr"]["Hours"], f"{data['mttr']['Percentage Change']:.2f}%", delta_color='inverse')
    st.line_chart(pd.DataFrame({'Time': st.session_state.kpi_data['time'], 'MTTR': st.session_state.kpi_data['mttr']}).set_index('Time'))

with col2:
    st.subheader("Mean Time Between Failures (MTBF)")
    delta_color = "inverse" if data["mtbf"]["Percentage Change"] < 0 else "normal"
    st.metric("MTBF Hours", data["mtbf"]["Hours"], f"{data['mtbf']['Percentage Change']:.2f}%", delta_color='inverse')
    st.line_chart(pd.DataFrame({'Time': st.session_state.kpi_data['time'], 'MTBF': st.session_state.kpi_data['mtbf']}).set_index('Time'))

# OEE Visualization
st.header("Overall Equipment Effectiveness (OEE)")

oee_value = data["oee"]["OEE"]
quality_value = data["oee"]["Quality"]
performance_value = data["oee"]["Performance"]
availability_value = data["oee"]["Availability"]

st.metric("OEE", f"{oee_value:.2f}%")

# Horizontal bar chart for OEE components using Altair
oee_components = pd.DataFrame({
    'Component': ['Quality', 'Performance', 'Availability'],
    'Value': [quality_value, performance_value, availability_value]
})

chart = alt.Chart(oee_components).mark_bar().encode(
    x=alt.X('Value:Q'),
    y=alt.Y('Component:N', sort='-x'),
    color=alt.Color('Component:N', scale=alt.Scale(range=['#5a61bd', '#7178df', '#9ca2ef'])),
    tooltip=['Component', 'Value']
).properties(
    width=600,
    height=300,
    title='OEE Components'
).configure_axis(
    labelColor='white',
    titleColor='white'
).configure_view(
    strokeWidth=0
).configure_title(
    color='white'
).configure(
    background='#14192F'
)

st.altair_chart(chart, use_container_width=True)

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
