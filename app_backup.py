import streamlit as st
import xgboost as xgb

# Page settings
st.set_page_config(
    page_title="Energy Consumption Forecasting",
    page_icon="⚡",
    layout="wide"
)

# Load trained XGBoost model
model = xgb.XGBRegressor()
model.load_model("xgb_model.json")


# Title
st.title("⚡ Energy Consumption Forecasting")

st.write(
    "Machine Learning based 1-hour-ahead energy consumption forecasting system."
)

st.divider()


# Model Performance
st.subheader("📊 Model Performance")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="🎯 Accuracy",
        value="99.13%"
    )

with col2:
    st.metric(
        label="📉 MAPE",
        value="0.87%"
    )

st.divider()

st.info(
    "Best Model: XGBoost — 1-hour-ahead forecasting"
)

st.divider()


# Forecast Information
st.subheader("📋 Enter Forecast Information")


# Time information
col1, col2, col3 = st.columns(3)

with col1:
    hour = st.number_input(
        "Hour",
        min_value=0,
        max_value=23,
        value=12
    )

with col2:
    dayofweek = st.number_input(
        "Day of Week",
        min_value=0,
        max_value=6,
        value=2
    )

with col3:
    month = st.number_input(
        "Month",
        min_value=1,
        max_value=12,
        value=9
    )


# Previous energy consumption
st.subheader("⚡ Previous Energy Consumption")

col1, col2 = st.columns(2)

with col1:
    lag_1 = st.number_input(
        "Previous Hour Consumption",
        min_value=0.0,
        value=35000.0
    )

with col2:
    lag_2 = st.number_input(
        "2 Hours Ago Consumption",
        min_value=0.0,
        value=34000.0
    )

col1, col2 = st.columns(2)

with col1:
    lag_3 = st.number_input(
        "3 Hours Ago Consumption",
        min_value=0.0,
        value=33000.0
    )

with col2:
    lag_24 = st.number_input(
        "24 Hours Ago Consumption",
        min_value=0.0,
        value=35000.0
    )

lag_168 = st.number_input(
    "7 Days Ago Consumption",
    min_value=0.0,
    value=36000.0
)


st.divider()


# Prediction button
if st.button("🔮 Predict Energy Consumption"):

    # Input validation
    if (
        lag_1 <= 0
        or lag_2 <= 0
        or lag_3 <= 0
        or lag_24 <= 0
        or lag_168 <= 0
    ):
        st.warning(
            "⚠️ Please enter valid energy consumption values greater than 0."
        )

    else:

        # Prepare input data
        input_data = [[
            hour,
            dayofweek,
            month,
            lag_24,
            lag_168,
            lag_1,
            lag_2,
            lag_3
        ]]

        # Make prediction
        prediction = model.predict(input_data)

        # Forecast Result
        st.subheader("🔮 Forecast Result")

        result_col1, result_col2 = st.columns(2)

        with result_col1:
            st.metric(
                label="Predicted Energy Consumption",
                value=f"{prediction[0]:,.2f}"
            )

        with result_col2:
            st.metric(
                label="Forecast Horizon",
                value="1 Hour Ahead"
            )

        st.success(
            "✅ Prediction generated successfully using XGBoost."
        )


        # Consumption Trend
        st.subheader("📈 Energy Consumption Trend")

        chart_data = {
            "Time": [
                "7 Days Ago",
                "24 Hours Ago",
                "3 Hours Ago",
                "2 Hours Ago",
                "Previous Hour",
                "Next Hour (Predicted)"
            ],
            "Consumption": [
                lag_168,
                lag_24,
                lag_3,
                lag_2,
                lag_1,
                prediction[0]
            ]
        }

        st.line_chart(
            chart_data,
            x="Time",
            y="Consumption"
        )