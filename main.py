
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from src.data_loader import (
    load_f1_session,
    load_driver_laps,
    load_driver_info,
    load_car_telemetry
)

from src.telemetry import (
    compare_drivers,
    compare_two_drivers
)

from src.speed_analysis import (
    prepare_speed_data,
    plot_speed_telemetry
)


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="ApexTelemetry | F1 Analytics",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# CUSTOM DESIGN
# ==========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;500;600;700;800;900&family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: #080D11;
    color: #F4F7F8;
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-weight: 800 !important;
    letter-spacing: 1px;
    color: #F4F7F8;
}

header[data-testid="stHeader"] {
    background: rgba(8,13,17,0.95);
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #132128, #080D11);
    border-right: 1px solid #29434A;
}

section[data-testid="stSidebar"] * {
    color: #EAF2F3;
}

section[data-testid="stSidebar"] h1 {
    color: #00D2BE;
}

.hero {
    min-height: 440px;
    padding: 45px;
    border-radius: 18px;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    overflow: hidden;

    background-image:
        linear-gradient(
            90deg,
            rgba(3,8,12,0.95) 0%,
            rgba(3,8,12,0.70) 45%,
            rgba(3,8,12,0.15) 100%
        ),
        linear-gradient(
            0deg,
            rgba(3,8,12,0.75),
            transparent
        ),
        url("https://images.ctfassets.net/1fvlg6xqnm65/66MhVUrs7P6LSgBBe56ESM/64dbbfe04059718e29c4e747db950e62/Front_Low_LH_v001.jpg?fm=webp&q=85&w=1920");

    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;

    border: 1px solid #24545A;
    box-shadow: 0 18px 50px rgba(0,0,0,0.35);
    margin-bottom: 35px;
}

.hero-label {
    color: #00D2BE;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 4px;
    margin-bottom: 15px;
}

.hero-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: clamp(52px, 7vw, 88px);
    line-height: 0.95;
    font-weight: 900;
    color: white;
    text-shadow: 0 4px 20px rgba(0,0,0,0.6);
}

.hero-description {
    max-width: 560px;
    color: #D9E4E7;
    font-size: 15px;
    line-height: 1.8;
    margin-top: 20px;
}

.section-heading {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 32px;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin-top: 38px;
    margin-bottom: 20px;
    border-left: 5px solid #00D2BE;
    padding: 4px 0 4px 15px;
}

div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #17262D, #10171C);
    border: 1px solid #29434A;
    border-radius: 15px;
    padding: 20px;
}

div[data-testid="stMetricLabel"] {
    color: #A9C0C4;
    font-weight: 700;
    letter-spacing: 1px;
}

div[data-testid="stMetricValue"] {
    color: #00D2BE;
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 36px;
    font-weight: 800;
}

.stButton > button {
    background: linear-gradient(90deg, #00AFA4, #00D2BE);
    color: #061014;
    border: none;
    border-radius: 9px;
    min-height: 46px;
    font-weight: 800;
    letter-spacing: 1px;
}

.stButton > button:hover {
    background: #65F2E3;
    color: #061014;
}

.stSelectbox label {
    color: #B8C9CC !important;
    font-weight: 700;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #29434A;
    border-radius: 12px;
    overflow: hidden;
}

hr {
    border-color: #29434A;
}

.footer {
    text-align: center;
    color: #82969B;
    font-size: 12px;
    padding-top: 40px;
    letter-spacing: 2px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# CACHED DATA FUNCTIONS
# ==========================================================

@st.cache_data(ttl=600, show_spinner=False)
def get_sessions(year, country, session_name):
    return load_f1_session(year, country, session_name)


@st.cache_data(ttl=600, show_spinner=False)
def get_laps(session_key):
    return load_driver_laps(session_key)


@st.cache_data(ttl=600, show_spinner=False)
def get_drivers(session_key):
    return load_driver_info(session_key)


@st.cache_data(ttl=300, show_spinner=False)
def get_telemetry(session_key, driver_number):
    return load_car_telemetry(session_key, driver_number)


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.markdown("""
<h1 style="font-size:44px; margin-bottom:0;">APEX</h1>
<h2 style="font-size:24px; margin-top:0;">TELEMETRY</h2>
<p style="font-size:11px; color:#9DB1B6; letter-spacing:2px;">
FORMULA 1 PERFORMANCE ANALYTICS
</p>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

st.sidebar.markdown("### RACE CONFIGURATION")

year = st.sidebar.selectbox(
    "Season",
    [2024, 2023],
    index=0
)

country = st.sidebar.selectbox(
    "Grand Prix",
    [
        "Bahrain",
        "Saudi Arabia",
        "Australia",
        "Japan",
        "China",
        "Miami",
        "Monaco",
        "Canada",
        "Spain",
        "Austria",
        "Great Britain",
        "Hungary",
        "Belgium",
        "Netherlands",
        "Italy",
        "Singapore",
        "United States",
        "Mexico",
        "Brazil",
        "Las Vegas",
        "Abu Dhabi"
    ]
)

session_name = st.sidebar.selectbox(
    "Session",
    [
        "Race",
        "Qualifying",
        "Practice 1",
        "Practice 2",
        "Practice 3"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### DATA SOURCE")
st.sidebar.write("OpenF1 API")
st.sidebar.caption("Python • Pandas • Matplotlib • Streamlit")


# ==========================================================
# HERO SECTION - FIXED HTML
# ==========================================================

st.markdown("""
<div class="hero">
<div class="hero-label">MERCEDES-AMG PETRONAS INSPIRED</div>
<div class="hero-title">EVERY MILLISECOND<br>MATTERS.</div>
<div class="hero-description">
Explore Formula 1 performance through real session data.
Compare drivers, analyse lap times and understand
the speed behind every racing moment.
</div>
</div>
""", unsafe_allow_html=True)


# ==========================================================
# RACE DATA CENTER
# ==========================================================

st.markdown(
    '<div class="section-heading">RACE DATA CENTER</div>',
    unsafe_allow_html=True
)

if st.button("LOAD RACE DATA", use_container_width=True):

    try:
        with st.spinner("Connecting to OpenF1..."):

            sessions = get_sessions(
                year,
                country,
                session_name
            )

            if sessions.empty:
                st.warning(
                    "No session found. Try another Grand Prix or session."
                )

            else:
                session_key = int(
                    sessions.iloc[0]["session_key"]
                )

                laps = get_laps(session_key)
                drivers = get_drivers(session_key)

                st.session_state["session_key"] = session_key
                st.session_state["laps"] = laps
                st.session_state["drivers"] = drivers

                st.session_state.pop("speed_data", None)
                st.session_state.pop("speed_driver", None)

                st.success(
                    f"Race data loaded! Session key: {session_key}"
                )

    except Exception as error:
        st.error(f"Unable to load race data: {error}")


# ==========================================================
# ANALYTICS DASHBOARD
# ==========================================================

if "laps" in st.session_state and "drivers" in st.session_state:

    laps = st.session_state["laps"].copy()
    drivers = st.session_state["drivers"].copy()
    session_key = st.session_state["session_key"]

    # DRIVER NAME MAPPING

    driver_names = {}

    if not drivers.empty:

        for _, row in drivers.iterrows():

            number = str(row.get("driver_number", ""))

            first_name = str(row.get("first_name", ""))
            last_name = str(row.get("last_name", ""))

            full_name = f"{first_name} {last_name}".strip()

            if not full_name:
                full_name = f"Driver {number}"

            acronym = row.get("name_acronym", "")

            if pd.notna(acronym) and str(acronym).strip():
                display_name = f"{acronym} - {full_name}"
            else:
                display_name = full_name

            driver_names[number] = display_name

    # SESSION OVERVIEW

    st.markdown(
        '<div class="section-heading">SESSION OVERVIEW</div>',
        unsafe_allow_html=True
    )

    driver_count = (
        drivers["driver_number"].nunique()
        if not drivers.empty and "driver_number" in drivers.columns
        else 0
    )

    lap_count = len(laps)

    if not laps.empty and "lap_duration" in laps.columns:
        valid_laps = pd.to_numeric(
            laps["lap_duration"],
            errors="coerce"
        ).notna().sum()
    else:
        valid_laps = 0

    metric1, metric2, metric3 = st.columns(3)

    metric1.metric("DRIVERS", driver_count)
    metric2.metric("TOTAL LAP RECORDS", lap_count)
    metric3.metric("VALID LAP TIMES", valid_laps)

    # LAP TIME PERFORMANCE

    st.markdown(
        '<div class="section-heading">LAP TIME PERFORMANCE</div>',
        unsafe_allow_html=True
    )

    averages = compare_drivers(laps)

    if not averages.empty:

        averages["Driver Name"] = averages["Driver"].map(
            lambda number: driver_names.get(
                number,
                f"Driver {number}"
            )
        )

        chart_data = averages.sort_values(
            "Average Lap (s)",
            ascending=True
        )

        fig, ax = plt.subplots(figsize=(13, 7))

        fig.patch.set_facecolor("#0B1115")
        ax.set_facecolor("#121D23")

        bars = ax.barh(
            chart_data["Driver Name"],
            chart_data["Average Lap (s)"],
            color="#00D2BE",
            height=0.62,
            edgecolor="#0B171B",
            linewidth=0.8
        )

        minimum = chart_data["Average Lap (s)"].min()
        maximum = chart_data["Average Lap (s)"].max()

        ax.set_xlim(
            max(0, minimum - 1),
            maximum + 1.5
        )

        ax.bar_label(
            bars,
            fmt="%.2f",
            padding=5,
            color="white",
            fontsize=8
        )

        ax.set_title(
            "DRIVER LAP PERFORMANCE",
            color="white",
            fontsize=18,
            fontweight="bold",
            pad=20
        )

        ax.set_xlabel(
            "AVERAGE LAP TIME (SECONDS)",
            color="#B8C9CC"
        )

        ax.tick_params(colors="white", labelsize=9)

        ax.grid(
            axis="x",
            color="#6C858A",
            alpha=0.18,
            linestyle="--"
        )

        ax.set_axisbelow(True)

        for spine in ax.spines.values():
            spine.set_color("#30454B")

        plt.tight_layout()

        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.caption(
            "Lower average lap time is faster. These averages use "
            "available lap records and are not adjusted for pit stops, "
            "traffic, tyre strategy or track conditions."
        )

        st.markdown("### DRIVER PERFORMANCE TABLE")

        display_table = averages[
            [
                "Driver Name",
                "Average Lap (s)",
                "Best Lap (s)",
                "Valid Laps"
            ]
        ].copy()

        display_table["Average Lap (s)"] = (
            display_table["Average Lap (s)"].round(3)
        )

        display_table["Best Lap (s)"] = (
            display_table["Best Lap (s)"].round(3)
        )

        st.dataframe(
            display_table,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.warning("No valid lap-time data found.")

    # HEAD-TO-HEAD COMPARISON

    st.markdown(
        '<div class="section-heading">HEAD-TO-HEAD</div>',
        unsafe_allow_html=True
    )

    if not averages.empty:

        driver_options = averages["Driver"].astype(str).tolist()

        if len(driver_options) >= 2:

            col1, col2 = st.columns(2)

            with col1:
                first_driver = st.selectbox(
                    "SELECT DRIVER 1",
                    driver_options,
                    format_func=lambda number: driver_names.get(
                        number,
                        f"Driver {number}"
                    ),
                    key="driver_one"
                )

            second_options = [
                number for number in driver_options
                if number != first_driver
            ]

            with col2:
                second_driver = st.selectbox(
                    "SELECT DRIVER 2",
                    second_options,
                    format_func=lambda number: driver_names.get(
                        number,
                        f"Driver {number}"
                    ),
                    key="driver_two"
                )

            comparison = compare_two_drivers(
                laps,
                first_driver,
                second_driver
            )

            if not comparison.empty:

                name1 = driver_names.get(
                    first_driver,
                    f"Driver {first_driver}"
                )

                name2 = driver_names.get(
                    second_driver,
                    f"Driver {second_driver}"
                )

                fig, ax = plt.subplots(figsize=(13, 5))

                fig.patch.set_facecolor("#0B1115")
                ax.set_facecolor("#121D23")

                ax.plot(
                    comparison["lap_number"],
                    comparison["Driver 1"],
                    label=name1,
                    color="#00D2BE",
                    linewidth=2.5
                )

                ax.plot(
                    comparison["lap_number"],
                    comparison["Driver 2"],
                    label=name2,
                    color="#E8F1F2",
                    linewidth=2
                )

                ax.set_title(
                    "LAP-BY-LAP DRIVER COMPARISON",
                    color="white",
                    fontsize=17,
                    fontweight="bold",
                    pad=18
                )

                ax.set_xlabel("LAP NUMBER", color="#B8C9CC")
                ax.set_ylabel("LAP TIME (SECONDS)", color="#B8C9CC")

                ax.tick_params(colors="white")

                ax.grid(
                    color="#6C858A",
                    alpha=0.18,
                    linestyle="--"
                )

                ax.legend(
                    facecolor="#17262D",
                    edgecolor="#30454B",
                    labelcolor="white"
                )

                for spine in ax.spines.values():
                    spine.set_color("#30454B")

                plt.tight_layout()

                st.pyplot(fig, use_container_width=True)
                plt.close(fig)

                st.dataframe(
                    comparison.round(3),
                    use_container_width=True,
                    hide_index=True
                )

            else:
                st.info(
                    "No matching lap numbers found for these drivers."
                )

        else:
            st.info(
                "At least two drivers are needed for comparison."
            )

    # SPEED TELEMETRY

    st.markdown(
        '<div class="section-heading">SPEED TELEMETRY</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Explore the selected driver's speed measurements throughout "
        "the session."
    )

    if not drivers.empty:

        telemetry_driver_options = sorted(
            drivers["driver_number"].astype(str).unique().tolist()
        )

        selected_driver = st.selectbox(
            "SELECT DRIVER FOR SPEED ANALYSIS",
            telemetry_driver_options,
            format_func=lambda number: driver_names.get(
                number,
                f"Driver {number}"
            ),
            key="telemetry_driver"
        )

        if st.button(
            "LOAD SPEED TELEMETRY",
            use_container_width=True
        ):

            try:
                with st.spinner("Loading speed measurements..."):

                    telemetry = get_telemetry(
                        session_key,
                        selected_driver
                    )

                    st.session_state["speed_data"] = telemetry
                    st.session_state["speed_driver"] = selected_driver

            except Exception as error:
                st.error(
                    f"Could not load speed telemetry: {error}"
                )

        if (
            "speed_data" in st.session_state
            and st.session_state.get("speed_driver") == selected_driver
        ):

            try:
                speed_data = prepare_speed_data(
                    st.session_state["speed_data"]
                )

                driver_name = driver_names.get(
                    selected_driver,
                    f"Driver {selected_driver}"
                )

                fig = plot_speed_telemetry(
                    speed_data,
                    driver_name
                )

                st.pyplot(fig, use_container_width=True)
                plt.close(fig)

                speed1, speed2, speed3 = st.columns(3)

                speed1.metric(
                    "MAXIMUM SPEED",
                    f"{speed_data['speed'].max():.0f} km/h"
                )

                speed2.metric(
                    "AVERAGE SPEED",
                    f"{speed_data['speed'].mean():.0f} km/h"
                )

                speed3.metric(
                    "TELEMETRY POINTS",
                    len(speed_data)
                )

            except Exception as error:
                st.warning(
                    f"Speed analysis unavailable: {error}"
                )

    # RAW DATA

    with st.expander("VIEW RAW LAP DATA"):
        st.dataframe(
            laps,
            use_container_width=True
        )

    with st.expander("VIEW DRIVER INFORMATION"):
        st.dataframe(
            drivers,
            use_container_width=True
        )

else:

    st.info(
        "Choose a season, Grand Prix and session from the sidebar, "
        "then click LOAD RACE DATA."
    )


# ==========================================================
# F1 TEAM LINKS
# ==========================================================

st.markdown(
    '<div class="section-heading">INSIDE THE WORLD OF F1</div>',
    unsafe_allow_html=True
)

video_col1, video_col2 = st.columns(2)

with video_col1:

    st.markdown("### MERCEDES-AMG PETRONAS")

    st.write(
        "Discover Mercedes race weekends, car development, "
        "engineering and behind-the-scenes videos."
    )

    st.markdown(
        "[Mercedes on YouTube](https://www.youtube.com/@MercedesAMGF1)"
    )

    st.markdown(
        "[Official Mercedes F1 website](https://www.mercedesamgf1.com/)"
    )

with video_col2:

    st.markdown("### SCUDERIA FERRARI")

    st.write(
        "Explore Ferrari race content, team stories and "
        "Formula 1 engineering."
    )

    st.markdown(
        "[Ferrari on YouTube](https://www.youtube.com/@Ferrari)"
    )

    st.markdown(
        "[Official Ferrari website](https://www.ferrari.com/)"
    )


# ==========================================================
# FOOTER
# ==========================================================

st.markdown("""
<div class="footer">
APEXTELEMETRY<br><br>
FORMULA 1 PERFORMANCE ANALYTICS<br>
PYTHON • PANDAS • MATPLOTLIB • STREAMLIT • OPENF1
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding:12px; color:#888; font-size:12px;">
    Developed by <b>Kalyani Kadam</b><br>
    <a href="mailto:kadamkalyanii01@gmail.com"
       style="color:#00D2BE; text-decoration:none;">
       kadamkalyanii01@gmail.com
    </a>
</div>
""", unsafe_allow_html=True)