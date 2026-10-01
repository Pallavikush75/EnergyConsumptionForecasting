import streamlit as st
import xgboost as xgb
import pandas as pd
from datetime import datetime


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Energy Consumption Forecasting",
    page_icon="⚡",
    layout="wide"
)


# ============================================================
# ECO GLOW THEME
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500;600;700&display=swap');


/* ============================================================
   GLOBAL
   ============================================================ */

html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {

    background-color: #050f0c !important;
    color: #ffffff !important;
}

* {
    font-family: "Quicksand", sans-serif !important;
    box-sizing: border-box;
}

.stApp {

    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(90,242,176,0.08),
            transparent 28%
        ),

        radial-gradient(
            circle at 90% 20%,
            rgba(15,74,56,0.16),
            transparent 30%
        ),

        radial-gradient(
            circle at 50% 100%,
            rgba(90,242,176,0.05),
            transparent 30%
        ),

        #050f0c !important;
}


[data-testid="stAppViewContainer"] {

    background:
        radial-gradient(
            circle at 20% 30%,
            rgba(90,242,176,0.06),
            transparent 25%
        ),

        radial-gradient(
            circle at 80% 70%,
            rgba(15,74,56,0.12),
            transparent 28%
        ),

        #050f0c !important;
}


/* ============================================================
   HEADER
   ============================================================ */

header,
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="stBottomBlockContainer"],
[data-testid="stBottom"] {

    background-color: #050f0c !important;
}


/* ============================================================
   TEXT
   ============================================================ */

h1,
h2,
h3,
h4,
h5,
h6 {

    color: #ffffff !important;
    font-weight: 700 !important;
}

h1 {

    text-shadow:
        0 0 8px rgba(90,242,176,0.30),
        0 0 20px rgba(90,242,176,0.18);
}

p,
span,
label {

    color: #d8ede4 !important;
}

strong,
b {

    color: #5af2b0 !important;
    font-weight: 700 !important;
}

hr {

    border: none !important;

    border-top:
        1px solid #0f4a38 !important;

    opacity: 0.8;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #071812 0%,
            #050f0c 100%
        ) !important;

    border-right:
        1px solid #0f4a38 !important;

    box-shadow:
        4px 0 25px rgba(0,0,0,0.30);
}

section[data-testid="stSidebar"] > div {

    background-color: transparent !important;
}

section[data-testid="stSidebar"] h2 {

    color: #ffffff !important;

    text-shadow:
        0 0 8px rgba(90,242,176,0.35);
}

section[data-testid="stSidebar"] p {

    color: #91b7a8 !important;
}


section[data-testid="stSidebar"]
div[role="radiogroup"]
label {

    color: #d8ede4 !important;

    border-radius: 10px;

    padding: 8px;

    transition:
        all 0.3s ease;
}


section[data-testid="stSidebar"]
div[role="radiogroup"]
label:hover {

    background-color:
        #0f4a38 !important;

    color:
        #5af2b0 !important;

    transform:
        translateX(5px);

    box-shadow:
        0 0 15px rgba(90,242,176,0.15);
}


/* ============================================================
   INPUTS
   ============================================================ */

div[data-baseweb="input"] {

    background-color:
        #071812 !important;

    border:
        1px solid #0f4a38 !important;

    border-radius:
        10px !important;
}

div[data-baseweb="input"]:focus-within {

    border-color:
        #5af2b0 !important;

    box-shadow:
        0 0 12px rgba(90,242,176,0.25) !important;
}

input,
textarea {

    background-color:
        #071812 !important;

    color:
        #ffffff !important;
}

input::placeholder,
textarea::placeholder {

    color:
        #71998a !important;
}


/* ============================================================
   NUMBER INPUT
   ============================================================ */

div[data-testid="stNumberInput"] input {

    background-color:
        #071812 !important;

    color:
        #ffffff !important;
}

div[data-testid="stNumberInput"] button {

    background-color:
        #0f4a38 !important;

    color:
        #5af2b0 !important;

    border-color:
        #0f4a38 !important;
}

div[data-testid="stNumberInput"] button:hover {

    background-color:
        #5af2b0 !important;

    color:
        #050f0c !important;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {

    background:
        linear-gradient(
            135deg,
            #0f4a38,
            #146b4f
        ) !important;

    color:
        #5af2b0 !important;

    border:
        1px solid #5af2b0 !important;

    border-radius:
        10px !important;

    font-weight:
        700 !important;

    padding:
        9px 20px !important;

    transition:
        all 0.3s ease;
}

.stButton > button:hover {

    background:
        linear-gradient(
            135deg,
            #5af2b0,
            #3bd995
        ) !important;

    color:
        #050f0c !important;

    transform:
        translateY(-2px);

    box-shadow:
        0 0 18px rgba(90,242,176,0.45);
}


/* ============================================================
   DOWNLOAD BUTTON
   ============================================================ */

.stDownloadButton > button {

    background:
        linear-gradient(
            135deg,
            #0f4a38,
            #146b4f
        ) !important;

    color:
        #5af2b0 !important;

    border:
        1px solid #5af2b0 !important;

    border-radius:
        10px !important;

    font-weight:
        700 !important;
}

.stDownloadButton > button:hover {

    background:
        #5af2b0 !important;

    color:
        #050f0c !important;

    box-shadow:
        0 0 18px rgba(90,242,176,0.45);
}


/* ============================================================
   METRIC CARDS
   ============================================================ */

[data-testid="stMetric"] {

    background:
        linear-gradient(
            145deg,
            rgba(7,24,18,0.95),
            rgba(15,74,56,0.35)
        ) !important;

    border:
        1px solid #0f4a38 !important;

    border-radius:
        14px !important;

    padding:
        18px !important;

    box-shadow:
        0 0 15px rgba(90,242,176,0.05);

    transition:
        all 0.3s ease;
}

[data-testid="stMetric"]:hover {

    transform:
        translateY(-5px);

    border-color:
        #5af2b0 !important;

    box-shadow:
        0 8px 25px rgba(90,242,176,0.15),
        0 0 20px rgba(90,242,176,0.10);
}

[data-testid="stMetricValue"] {

    color:
        #5af2b0 !important;

    font-weight:
        700 !important;

    text-shadow:
        0 0 10px rgba(90,242,176,0.25);
}

[data-testid="stMetricLabel"] {

    color:
        #d8ede4 !important;
}


/* ============================================================
   ALERTS
   ============================================================ */

div[data-testid="stAlert"] {

    border-radius:
        12px !important;

    border:
        1px solid #0f4a38 !important;

    background-color:
        rgba(7,24,18,0.85) !important;
}


/* ============================================================
   DATAFRAME
   ============================================================ */

[data-testid="stDataFrame"] {

    background-color:
        #071812 !important;

    border:
        1px solid #0f4a38 !important;

    border-radius:
        12px !important;
}


/* ============================================================
   EXPANDER
   ============================================================ */

[data-testid="stExpander"] {

    background-color:
        #071812 !important;

    border:
        1px solid #0f4a38 !important;

    border-radius:
        12px !important;
}


/* ============================================================
   TABS
   ============================================================ */

button[data-baseweb="tab"] {

    background-color:
        #050f0c !important;

    color:
        #91b7a8 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {

    color:
        #5af2b0 !important;

    border-bottom:
        2px solid #5af2b0 !important;
}


/* ============================================================
   LINKS
   ============================================================ */

a {

    color:
        #5af2b0 !important;
}


/* ============================================================
   CODE
   ============================================================ */

code {

    color:
        #5af2b0 !important;

    background-color:
        #071812 !important;
}


/* ============================================================
   SCROLLBAR
   ============================================================ */

::-webkit-scrollbar {

    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {

    background:
        #050f0c;
}

::-webkit-scrollbar-thumb {

    background:
        #0f4a38;

    border-radius:
        10px;
}

::-webkit-scrollbar-thumb:hover {

    background:
        #5af2b0;
}


/* ============================================================
   HERO IMAGE - COMPACT ECO STYLE
   ============================================================ */

div[data-testid="stImage"] {

    display: flex !important;

    justify-content: center !important;

    align-items: center !important;

    width: 100% !important;

    margin-top: 40px !important;

    margin-bottom: 8px !important;
}


div[data-testid="stImage"] img {

    width: 100% !important;

    max-width: 500px !important;

    height: 200px !important;

    object-fit: cover !important;

    object-position: center !important;

    border-radius: 16px !important;

    border:
        1px solid rgba(90,242,176,0.28) !important;

    box-shadow:
        0 0 18px rgba(90,242,176,0.10),
        0 0 35px rgba(15,74,56,0.16) !important;

    filter:
        brightness(0.88)
        saturate(0.90)
        contrast(1.03) !important;

    transition:
        all 0.3s ease !important;
}


div[data-testid="stImage"] img:hover {

    border-color:
        rgba(90,242,176,0.55) !important;

    box-shadow:
        0 0 22px rgba(90,242,176,0.16),
        0 0 45px rgba(15,74,56,0.22) !important;

    transform:
        scale(1.01);
}


/* ============================================================
   HERO TEXT
   ============================================================ */

.hero-text {

    font-size: 20px;

    line-height: 1.6;

    color:
        #d8ede4;

    margin-top:
        30px;
}


/* ============================================================
   REDUCE EXTRA BOTTOM SPACE
   ============================================================ */

[data-testid="stMainBlockContainer"] {

    padding-bottom: 0rem !important;

    margin-bottom: 0rem !important;
}

[data-testid="stMain"] {

    padding-bottom: 0px !important;

    margin-bottom: 0px !important;
}

[data-testid="stAppViewContainer"] main {

    padding-bottom: 0px !important;

    margin-bottom: 0px !important;
}

section.main > div {

    padding-bottom: 0px !important;

    margin-bottom: 0px !important;
}


/* ============================================================
   FOOTER
   ============================================================ */

.eco-footer {

    margin-top: 0px !important;

    /* ADDED: space below footer */
    margin-bottom: 18px !important;

    /* ADDED: more vertical breathing space */
    padding: 5px 4px 12px 4px !important;

    text-align: center;

    border-top:
        1px solid #0f4a38;

    color:
        #71998a;

    font-size:
        10px !important;

    /* CHANGED: slightly more height */
    line-height:
        1.2 !important;

    /* CHANGED: gives space below text */
    height:
        32px !important;

    min-height:
        32px !important;

    overflow:
        hidden !important;

    /* ADDED: moves the footer text slightly upward */
    transform:
        translateY(-4px);
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 768px) {

    .hero-text {

        font-size:
            16px;
    }

    div[data-testid="stImage"] img {

        max-width:
            100% !important;

        height:
            160px !important;

        border-radius:
            14px !important;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD MODEL
# ============================================================

model = xgb.XGBRegressor()

model.load_model(
    "xgb_model.json"
)


# ============================================================
# PREDICTION HISTORY
# ============================================================

if "prediction_history" not in st.session_state:

    st.session_state.prediction_history = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## ⚡ ENERGY AI"
    )

    st.caption(
        "Energy Forecasting System"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "📊 Forecast",
            "📈 Analytics",
            "ℹ️ About"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown(
        """
        <p style="font-size:13px;">

        <b>Model</b><br>
        XGBoost<br><br>

        <b>Forecast Horizon</b><br>
        1 Hour Ahead<br><br>

        <b>Accuracy</b><br>
        99.13%

        </p>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    hero_left, hero_right = st.columns(
        [1.05, 1],
        gap="large"
    )

    with hero_left:

        st.markdown(
            "<div style='height:25px'></div>",
            unsafe_allow_html=True
        )

        st.markdown(
            """
            ### Smart energy consumption forecasting
            powered by Machine Learning and XGBoost.
            """
        )

        st.markdown(
            "<div style='height:12px'></div>",
            unsafe_allow_html=True
        )

        st.markdown(
            """
            🌱 **Clean Energy Intelligence**
            """
        )

        st.markdown(
            """
            <p class="hero-text">

            Monitor historical energy usage, identify
            consumption patterns and generate a
            <b>1-hour-ahead energy forecast</b>
            using XGBoost.

            </p>
            """,
            unsafe_allow_html=True
        )

    with hero_right:

        st.image(
            "https://images.openai.com/static-rsc-4/mIpSMdlR-QuqNa6ujaBdw4U565ufns307sAhF9LJTM9qucwJ5Bq8QJeEoA6cQ7bEZQAqe_v72IUUbKmXoR5AMSgH_xjnqUhR_OHzQ3IL_iV7AlYppxhEwl5tGfmhXcsMR8QQRgRf_xovS7gOOP_Icpdt7f5i9ZhqUHtAIWKwjNE?purpose=inline",
            caption="Smart Energy • Power Consumption • Energy Monitoring",
            use_container_width=True
        )

    st.divider()

    st.title(
        "⚡ Energy Consumption Forecasting"
    )

    st.write(
        "Machine Learning based 1-hour-ahead "
        "energy consumption forecasting system."
    )

    st.divider()

    st.subheader(
        "🌿 Welcome to Energy AI"
    )

    st.write(
        "This dashboard provides an interactive platform "
        "for forecasting energy consumption using a trained "
        "XGBoost machine learning model."
    )

    st.divider()

    st.subheader(
        "📊 Model Performance"
    )

    col1, col2, col3, col4 = st.columns(4)

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

    with col3:

        st.metric(
            label="🤖 Model",
            value="XGBoost"
        )

    with col4:

        st.metric(
            label="⏱️ Forecast",
            value="1 Hour"
        )

    st.divider()

    st.subheader(
        "🤖 Model Status"
    )

    status_col1, status_col2 = st.columns(2)

    with status_col1:

        st.success(
            "✅ Model Loaded Successfully"
        )

    with status_col2:

        st.info(
            "⚡ Ready for Energy Forecasting"
        )

    st.divider()

    st.subheader(
        "📋 Project Overview"
    )

    st.write(
        """
        The Energy Consumption Forecasting system predicts
        electricity consumption for the next one hour using
        historical energy consumption and time-based features.
        """
    )

    st.write(
        """
        The trained XGBoost model is integrated with a
        Streamlit-based frontend, allowing users to enter
        forecasting information and receive an immediate
        prediction.
        """
    )

    st.divider()

    st.subheader(
        "📌 Prediction Inputs"
    )

    feature_col1, feature_col2 = st.columns(2)

    with feature_col1:

        st.markdown(
            """
            **Time Features**

            • Hour

            • Day of Week

            • Month
            """
        )

    with feature_col2:

        st.markdown(
            """
            **Historical Consumption**

            • Previous Hour

            • 2 Hours Ago

            • 3 Hours Ago

            • 24 Hours Ago

            • 7 Days Ago
            """
        )

    st.divider()

    st.subheader(
        "🚀 How to Use"
    )

    st.write(
        "1. Open the **📊 Forecast** section from the sidebar."
    )

    st.write(
        "2. Enter the required time and historical consumption values."
    )

    st.write(
        "3. Click **🔮 Predict Energy Consumption**."
    )

    st.write(
        "4. View the predicted energy consumption and trend graph."
    )

    st.write(
        "5. Check the prediction history in the Analytics section."
    )


# ============================================================
# FORECAST PAGE
# ============================================================

elif page == "📊 Forecast":

    st.title(
        "📊 Energy Consumption Forecast"
    )

    st.write(
        "Enter the required information to generate "
        "a 1-hour-ahead forecast."
    )

    st.divider()

    st.subheader(
        "📋 Enter Forecast Information"
    )

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

    st.subheader(
        "⚡ Previous Energy Consumption"
    )

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

    if st.button(
        "🔮 Predict Energy Consumption"
    ):

        if (
            lag_1 <= 0
            or lag_2 <= 0
            or lag_3 <= 0
            or lag_24 <= 0
            or lag_168 <= 0
        ):

            st.warning(
                "⚠️ Please enter valid energy consumption "
                "values greater than 0."
            )

        else:

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

            prediction = model.predict(
                input_data
            )

            predicted_value = float(
                prediction[0]
            )

            prediction_record = {

                "Time":
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),

                "Hour":
                    hour,

                "Day of Week":
                    dayofweek,

                "Month":
                    month,

                "Predicted Consumption":
                    round(
                        predicted_value,
                        2
                    )
            }

            st.session_state.prediction_history.append(
                prediction_record
            )

            st.subheader(
                "🔮 Forecast Result"
            )

            result_col1, result_col2 = st.columns(2)

            with result_col1:

                st.metric(
                    label="Predicted Energy Consumption",
                    value=f"{predicted_value:,.2f}"
                )

            with result_col2:

                st.metric(
                    label="Forecast Horizon",
                    value="1 Hour Ahead"
                )

            st.success(
                "✅ Prediction generated successfully using XGBoost."
            )

            HIGH_CONSUMPTION_THRESHOLD = 40000

            if predicted_value >= HIGH_CONSUMPTION_THRESHOLD:

                st.warning(
                    f"""
                    ⚠️ High Energy Consumption Detected!

                    Predicted consumption is
                    {predicted_value:,.2f},
                    which is above the
                    high-consumption threshold.
                    """
                )

                st.info(
                    """
                    💡 Recommendation:
                    Monitor energy usage and consider
                    reducing non-essential consumption.
                    """
                )

            else:

                st.success(
                    f"""
                    🟢 Normal Energy Consumption

                    Predicted consumption is
                    {predicted_value:,.2f}.
                    """
                )

                st.info(
                    """
                    💡 Recommendation:
                    Energy consumption is within the
                    defined normal range.
                    """
                )

            st.subheader(
                "📈 Energy Consumption Trend"
            )

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
                    predicted_value
                ]
            }

            st.line_chart(
                chart_data,
                x="Time",
                y="Consumption"
            )


# ============================================================
# ANALYTICS PAGE
# ============================================================

elif page == "📈 Analytics":

    st.title(
        "📈 Model Analytics"
    )

    st.write(
        "Performance and technical information of the "
        "energy consumption forecasting model."
    )

    st.divider()

    st.subheader(
        "📊 Model Performance"
    )

    col1, col2, col3 = st.columns(3)

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

    with col3:

        st.metric(
            label="🤖 Model",
            value="XGBoost"
        )

    st.divider()

    st.subheader(
        "📊 Performance Overview"
    )

    performance_data = {

        "Metric": [
            "Accuracy",
            "MAPE"
        ],

        "Value": [
            99.13,
            0.87
        ]
    }

    st.bar_chart(
        performance_data,
        x="Metric",
        y="Value"
    )

    st.caption(
        "Model performance metrics obtained during model evaluation."
    )

    st.divider()

    st.subheader(
        "📜 Prediction History"
    )

    if len(
        st.session_state.prediction_history
    ) > 0:

        history_df = pd.DataFrame(
            st.session_state.prediction_history
        )

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader(
            "📥 Download Prediction History"
        )

        csv_data = history_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📥 Download CSV Report",
            data=csv_data,
            file_name="energy_prediction_history.csv",
            mime="text/csv"
        )

        if st.button(
            "🗑️ Clear Prediction History"
        ):

            st.session_state.prediction_history = []

            st.success(
                "Prediction history cleared successfully."
            )

            st.rerun()

    else:

        st.info(
            """
            📭 No prediction history available yet.

            Go to the Forecast section and generate
            a prediction.
            """
        )

    st.divider()

    st.subheader(
        "🤖 Model Information"
    )

    info_col1, info_col2 = st.columns(2)

    with info_col1:

        st.markdown(
            """
            **Algorithm**

            XGBoost

            **Forecast Type**

            1-hour-ahead forecasting

            **Application**

            Energy Consumption Forecasting
            """
        )

    with info_col2:

        st.markdown(
            """
            **Frontend**

            Streamlit

            **Development Environment**

            Python + Google Colab + VS Code

            **Deployment Interface**

            Interactive Web Dashboard
            """
        )

    st.divider()

    st.subheader(
        "📌 Model Input Features"
    )

    feature_data = {

        "Feature": [
            "Hour",
            "Day of Week",
            "Month",
            "Previous Hour Consumption",
            "2 Hours Ago Consumption",
            "3 Hours Ago Consumption",
            "24 Hours Ago Consumption",
            "7 Days Ago Consumption"
        ]
    }

    st.dataframe(
        feature_data,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader(
        "⏱️ Forecast Information"
    )

    forecast_col1, forecast_col2 = st.columns(2)

    with forecast_col1:

        st.info(
            """
            Forecast Horizon

            1 Hour Ahead
            """
        )

    with forecast_col2:

        st.success(
            """
            Model Status

            Ready for Prediction
            """
        )


# ============================================================
# ABOUT PAGE
# ============================================================

elif page == "ℹ️ About":

    st.title(
        "ℹ️ About the Project"
    )

    st.subheader(
        "⚡ Energy Consumption Forecasting"
    )

    st.write(
        """
        A Machine Learning based system designed to forecast
        energy consumption one hour ahead using historical
        energy consumption and time-based information.
        """
    )

    st.divider()

    st.subheader(
        "🎯 Project Objective"
    )

    st.write(
        """
        The main objective of this project is to predict future
        energy consumption using historical consumption patterns
        and time-related features.
        """
    )

    st.write(
        """
        The system provides an interactive interface where users
        can enter the required forecasting information and obtain
        a one-hour-ahead energy consumption prediction.
        """
    )

    st.divider()

    st.subheader(
        "🤖 Machine Learning Model"
    )

    model_col1, model_col2 = st.columns(2)

    with model_col1:

        st.markdown(
            """
            **Algorithm**

            XGBoost

            **Forecast Type**

            1-hour-ahead forecasting

            **Model Output**

            Predicted energy consumption
            """
        )

    with model_col2:

        st.markdown(
            """
            **Accuracy**

            99.13%

            **MAPE**

            0.87%

            **Model Status**

            Ready for Prediction
            """
        )

    st.divider()

    st.subheader(
        "🛠️ Technologies Used"
    )

    tech_col1, tech_col2 = st.columns(2)

    with tech_col1:

        st.markdown(
            """
            **Development & Data**

            • Python

            • Google Colab

            • Pandas

            • NumPy
            """
        )

    with tech_col2:

        st.markdown(
            """
            **Machine Learning & Frontend**

            • XGBoost

            • Scikit-learn

            • Streamlit

            • VS Code
            """
        )

    st.divider()

    st.subheader(
        "🔄 Project Workflow"
    )

    st.write(
        """
        **1. Data Collection**

        Historical energy consumption data is used as the
        foundation of the forecasting system.
        """
    )

    st.write(
        """
        **2. Data Preprocessing**

        The dataset is cleaned and prepared for Machine Learning.
        """
    )

    st.write(
        """
        **3. Feature Engineering**

        Time-based and historical consumption features are created.
        """
    )

    st.write(
        """
        **4. Model Training**

        Different Machine Learning approaches are evaluated
        and XGBoost is used for the forecasting system.
        """
    )

    st.write(
        """
        **5. Model Evaluation**

        The trained model is evaluated using Accuracy and MAPE.
        """
    )

    st.write(
        """
        **6. Deployment**

        The trained XGBoost model is integrated into a
        Streamlit web interface for interactive prediction.
        """
    )

    st.divider()

    st.subheader(
        "⏱️ Forecast Horizon"
    )

    st.success(
        "⚡ The system generates a 1-hour-ahead energy consumption forecast."
    )

    st.divider()

    st.subheader(
        "✅ System Status"
    )

    status_col1, status_col2, status_col3 = st.columns(3)

    with status_col1:

        st.info(
            """
            🤖 XGBoost Model

            Loaded
            """
        )

    with status_col2:

        st.success(
            """
            📊 Accuracy

            99.13%
            """
        )

    with status_col3:

        st.success(
            """
            🚀 Frontend

            Operational
            """
        )


# ============================================================
# EMPTY SPACE BEFORE FOOTER
# ============================================================

st.markdown(
    """
    <div style="height:15px;"></div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="eco-footer">
        ⚡ Energy AI &nbsp;•&nbsp;
        Smart Energy Consumption Forecasting &nbsp;•&nbsp;
        🌱 Eco Glow Intelligence
    </div>
    """,
    unsafe_allow_html=True
)