import hashlib
from pathlib import Path
import re
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# =========================================================
# PAGE CONFIG (MUST BE FIRST STREAMLIT COMMAND)
# =========================================================
st.set_page_config(
    page_title="ChurnIQ | Customer Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# PREMIUM SAAS UI / UX STYLING
# =========================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(59,130,246,.10), transparent 28%),
        radial-gradient(circle at 95% 8%, rgba(139,92,246,.09), transparent 25%),
        #f6f8fc;
}

[data-testid="stHeader"] {
    background: rgba(246,248,252,.78);
    backdrop-filter: blur(12px);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #08111f 0%, #0f172a 55%, #111827 100%);
    border-right: 1px solid rgba(255,255,255,.07);
}

[data-testid="stSidebar"] * {
    color: #e5edf8 !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #94a3b8 !important;
}

[data-testid="stSidebar"] .stButton button {
    background: rgba(255,255,255,.05);
    border: 1px solid rgba(255,255,255,.08);
    color: #e5edf8 !important;
    border-radius: 10px;
}

[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(59,130,246,.18);
    border-color: rgba(96,165,250,.35);
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.brand {
    padding: 8px 4px 24px 4px;
}

.brand-icon {
    display: inline-flex;
    width: 42px;
    height: 42px;
    border-radius: 12px;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #4f46e5, #06b6d4);
    font-size: 22px;
    margin-right: 10px;
    vertical-align: middle;
}

.brand-name {
    font-size: 22px;
    font-weight: 800;
    color: #ffffff !important;
    vertical-align: middle;
}

.brand-sub {
    color: #8290a8 !important;
    font-size: 12px;
    margin-top: 8px;
    line-height: 1.5;
}

.hero {
    position: relative;
    overflow: hidden;
    padding: 34px 38px;
    border-radius: 24px;
    margin-bottom: 24px;
    background:
        radial-gradient(circle at 85% 20%, rgba(96,165,250,.24), transparent 25%),
        linear-gradient(135deg, #08111f, #172554 58%, #312e81);
    box-shadow: 0 20px 60px rgba(15,23,42,.18);
    border: 1px solid rgba(255,255,255,.08);
    color: white;
}

.hero:after {
    content: "";
    position: absolute;
    width: 240px;
    height: 240px;
    right: -90px;
    bottom: -120px;
    border-radius: 50%;
    background: rgba(255,255,255,.08);
}

.hero h1 {
    color: white !important;
    font-size: clamp(30px, 4vw, 48px);
    font-weight: 800;
    letter-spacing: -1.5px;
    margin: 6px 0 8px;
}

.hero p {
    color: #cbd5e1 !important;
    font-size: 15px;
    line-height: 1.7;
    max-width: 820px;
}

.hero-badge {
    display: inline-block;
    margin-top: 16px;
    padding: 7px 11px;
    border-radius: 999px;
    background: rgba(16,185,129,.12);
    border: 1px solid rgba(52,211,153,.24);
    color: #a7f3d0;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: .4px;
}

.section-title {
    color: #0f172a;
    font-size: 20px;
    font-weight: 800;
    letter-spacing: -.4px;
    margin: 18px 0 10px;
}

.section-caption {
    color: #64748b;
    font-size: 13px;
    margin-bottom: 12px;
}

.metric-card {
    min-height: 128px;
    padding: 20px;
    border-radius: 18px;
    background: rgba(255,255,255,.88);
    border: 1px solid #e6eaf1;
    box-shadow: 0 10px 30px rgba(15,23,42,.06);
    transition: transform .2s ease, box-shadow .2s ease;
}

.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 16px 34px rgba(15,23,42,.10);
}

.metric-label {
    color: #64748b;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: .8px;
}

.metric-value {
    color: #0f172a;
    font-size: 28px;
    font-weight: 800;
    margin-top: 8px;
}

.metric-note {
    color: #94a3b8;
    font-size: 12px;
    margin-top: 5px;
}

.card {
    background: #ffffff;
    border: 1px solid #e7ebf2;
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 7px 22px rgba(15, 23, 42, .04);
}

.insight {
    min-height: 120px;
    padding: 18px 20px;
    border-radius: 17px;
    background: white;
    border: 1px solid #e7ebf2;
    border-left: 4px solid #4f46e5;
    box-shadow: 0 8px 25px rgba(15,23,42,.05);
    color: #475569;
    font-size: 13px;
    line-height: 1.6;
}

.insight b {
    color: #0f172a;
}

.status {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    color: #10b981;
    font-size: 12px;
    font-weight: 600;
}

.status-dot {
    width: 8px;
    height: 8px;
    background: #10b981;
    border-radius: 50%;
    display: inline-block;
}

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e6eaf1;
    padding: 17px 18px;
    border-radius: 16px;
    box-shadow: 0 8px 25px rgba(15,23,42,.05);
}

div[data-testid="stMetricLabel"] {
    color: #64748b;
}

div[data-testid="stMetricValue"] {
    color: #0f172a;
    font-weight: 800;
}

.stButton > button, .stDownloadButton > button {
    border-radius: 10px;
    font-weight: 700;
    min-height: 42px;
}

.stButton > button:hover, .stDownloadButton > button:hover {
    transform: translateY(-1px);
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
.stTextInput input,
.stNumberInput input {
    border-radius: 10px !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid #e6eaf1;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 8px 25px rgba(15,23,42,.04);
}

[data-testid="stChatMessage"] {
    border-radius: 15px;
    border: 1px solid #e7ebf2;
}

footer {
    visibility: hidden;
}

@media (max-width: 900px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .hero {
        padding: 26px 22px;
        border-radius: 18px;
    }
}
</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# PROJECT PATHS
# =========================================================
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# =========================================================
# LOCAL AUTHENTICATION
# =========================================================
DB_PATH = DATA_DIR / "churniq_users.db"


def init_auth_db():
    DATA_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def valid_email(email):
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))


def create_user(name, email, password):
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            "INSERT INTO users(name,email,password_hash) VALUES(?,?,?)",
            (name.strip(), email.lower().strip(), hash_password(password)),
        )
        conn.commit()
        return True, "Account created successfully."
    except sqlite3.IntegrityError:
        return False, "An account with this email already exists."
    finally:
        conn.close()


def authenticate(email, password):
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT id, name, email FROM users WHERE email=? AND password_hash=?",
        (email.lower().strip(), hash_password(password)),
    ).fetchone()
    conn.close()
    return row


init_auth_db()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "auth_user" not in st.session_state:
    st.session_state.auth_user = None

if not st.session_state.authenticated:
    st.markdown(
        """
    <div style="
        min-height:78vh;
        display:flex;
        align-items:center;
        justify-content:center;
        padding:25px 10px;
    ">
      <div style="
        width:min(980px,96%);
        background:linear-gradient(135deg,#0b1220 0%,#172554 55%,#0f766e 100%);
        border-radius:28px;
        padding:48px;
        color:white;
        box-shadow:0 25px 70px rgba(15,23,42,.20);
    ">
      <div style="font-size:12px;color:#93c5fd;font-weight:700;
                  letter-spacing:1.4px;text-transform:uppercase;">
          CUSTOMER INTELLIGENCE PLATFORM
      </div>
      <div style="font-size:46px;font-weight:800;letter-spacing:-2px;margin-top:10px;">
          ChurnIQ
      </div>
      <div style="font-size:19px;font-weight:600;margin-top:5px;">
          Predict churn. Protect revenue. Retain customers.
      </div>
      <div style="max-width:650px;color:#cbd5e1;font-size:14px;
                  line-height:1.7;margin-top:14px;">
          AI-powered customer analytics for churn prediction, customer
          segmentation, retention analysis and revenue intelligence.
      </div>
    </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    _, auth_col, _ = st.columns([1.2, 1, 1.2])
    with auth_col:
        login_tab, register_tab = st.tabs(["🔐 Sign In", "✨ Create Account"])

        with login_tab:
            st.markdown("### Welcome back")
            login_email = st.text_input("Email", key="login_email")
            login_password = st.text_input(
                "Password", type="password", key="login_password"
            )

            if st.button(
                "Sign In to ChurnIQ", use_container_width=True, type="primary"
            ):
                if not valid_email(login_email):
                    st.error("Enter a valid email address.")
                elif not login_password:
                    st.error("Enter your password.")
                else:
                    user = authenticate(login_email, login_password)
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.auth_user = {
                            "id": user[0],
                            "name": user[1],
                            "email": user[2],
                        }
                        st.session_state.workspace_started = True
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")

        with register_tab:
            st.markdown("### Create your account")
            reg_name = st.text_input("Full name", key="reg_name")
            reg_email = st.text_input("Email address", key="reg_email")
            reg_password = st.text_input(
                "Password", type="password", key="reg_password"
            )
            reg_confirm = st.text_input(
                "Confirm password", type="password", key="reg_confirm"
            )

            if st.button("Create ChurnIQ Account", use_container_width=True):
                if not reg_name.strip():
                    st.error("Enter your name.")
                elif not valid_email(reg_email):
                    st.error("Enter a valid email address.")
                elif len(reg_password) < 6:
                    st.error("Password must be at least 6 characters.")
                elif reg_password != reg_confirm:
                    st.error("Passwords do not match.")
                else:
                    ok, message = create_user(
                        reg_name, reg_email, reg_password
                    )
                    if ok:
                        st.success(message + " You can now sign in.")
                    else:
                        st.error(message)

    st.markdown(
        """
    <div style="text-align:center;color:#94a3b8;font-size:11px;margin-top:5px;">
        Local demo authentication • Passwords are stored as hashes
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.stop()

# =========================================================
# ENTRY SCREEN
# =========================================================
if "workspace_started" not in st.session_state:
    st.session_state.workspace_started = True

if not st.session_state.workspace_started:
    st.markdown(
        """
    <div style="
        min-height:78vh;
        display:flex;
        align-items:center;
        justify-content:center;
        padding:30px 10px;
    ">
      <div style="
        width:min(920px, 96%);
        background:linear-gradient(135deg,#0b1220 0%,#172554 55%,#0f766e 100%);
        border-radius:28px;
        padding:58px 62px;
        color:white;
        box-shadow:0 25px 70px rgba(15,23,42,.20);
    ">
        <div style="font-size:13px;color:#93c5fd;font-weight:700;
                    letter-spacing:1.4px;text-transform:uppercase;">
            CUSTOMER INTELLIGENCE PLATFORM
        </div>

        <div style="font-size:52px;font-weight:800;letter-spacing:-2px;
                    margin-top:12px;">
            ChurnIQ
        </div>

        <div style="font-size:22px;font-weight:600;margin-top:8px;">
            Predict churn. Protect revenue. Retain customers.
        </div>

        <div style="max-width:690px;color:#cbd5e1;font-size:15px;
                    line-height:1.75;margin-top:18px;">
            An AI-powered customer analytics workspace for churn prediction,
            RFM segmentation, cohort retention, revenue-at-risk analysis and
            intelligent business insights.
        </div>

        <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:28px;">
            <span style="padding:9px 13px;border-radius:999px;
                         background:rgba(255,255,255,.10);
                         border:1px solid rgba(255,255,255,.14);
                         font-size:12px;">🤖 AI Churn Prediction</span>
            <span style="padding:9px 13px;border-radius:999px;
                         background:rgba(255,255,255,.10);
                         border:1px solid rgba(255,255,255,.14);
                         font-size:12px;">📊 Advanced Analytics</span>
            <span style="padding:9px 13px;border-radius:999px;
                         background:rgba(255,255,255,.10);
                         border:1px solid rgba(255,255,255,.14);
                         font-size:12px;">💰 Revenue Intelligence</span>
        </div>

        <div style="margin-top:34px;color:#94a3b8;font-size:12px;">
            Secure analytics workspace • Built with Python, Streamlit, Pandas,
            Plotly & AI
        </div>
    </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    _, center, _ = st.columns([2, 1, 2])
    with center:
        if st.button(
            "🚀 Enter Analytics Workspace",
            use_container_width=True,
            type="primary",
        ):
            st.session_state.workspace_started = True
            st.rerun()

    st.markdown(
        """
    <div style="text-align:center;color:#94a3b8;font-size:11px;margin-top:8px;">
        ChurnIQ v1.0 • Customer Intelligence
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.stop()

# =========================================================
# DATA LOADING
# =========================================================
@st.cache_data
def load_data():
    return pd.read_csv(DATA_DIR / "churn_predictions.csv")


df = load_data()

# Make numeric columns safe for calculations
numeric_columns = [
    "total_charges",
    "monthly_charges",
    "tenure_months",
    "churn_probability",
    "last_purchase_days",
    "support_tickets",
    "age",
]
for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)


# =========================================================
# HELPERS
# =========================================================
def money(value):
    return f"₹{value:,.0f}"


def metric_card(label, value, note=""):
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-note">{note}</div>
    </div>
    """


def chart_layout(fig, height=390):
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=55, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#334155"),
        title_font=dict(size=16, color="#111827"),
        legend=dict(orientation="h", y=-0.18),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#eef2f7")
    return fig


def page_header(title, description, icon):
    st.markdown(
        f"""
        <div style="margin-bottom:22px;">
            <div style="font-size:30px;font-weight:800;color:#111827;">
                {icon} {title}
            </div>
            <div style="color:#64748b;font-size:13px;margin-top:6px;">
                {description}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def executive_metric(label, value, subtitle):
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-note">{subtitle}</div>
    </div>
    """


def build_churn_trend(data):
    candidates = ["month", "date", "signup_date", "cohort_month"]
    date_col = next((c for c in candidates if c in data.columns), None)

    if date_col:
        temp = data.copy()
        temp["_date"] = pd.to_datetime(temp[date_col], errors="coerce")
        temp = temp.dropna(subset=["_date"])
        if not temp.empty:
            trend = (
                temp.assign(period=temp["_date"].dt.to_period("M").astype(str))
                .groupby("period")
                .agg(
                    customers=("customer_id", "count"),
                    churned=("churn", lambda x: (x == "Yes").sum()),
                )
                .reset_index()
            )
            trend["churn_rate"] = trend["churned"] / trend["customers"] * 100
            return trend

    temp = data.copy()
    temp["tenure_band"] = pd.cut(
        temp["tenure_months"],
        bins=[-1, 6, 12, 24, 36, 60, float("inf")],
        labels=["0–6 mo", "7–12 mo", "13–24 mo", "25–36 mo", "37–60 mo", "60+ mo"],
    )
    trend = (
        temp.groupby("tenure_band", observed=False)
        .agg(
            customers=("customer_id", "count"),
            churned=("churn", lambda x: (x == "Yes").sum()),
        )
        .reset_index()
    )
    trend["churn_rate"] = trend["churned"] / trend["customers"] * 100
    return trend


def retention_recommendation(row):
    risk = str(row.get("risk_level", ""))
    contract = str(row.get("contract_type", ""))
    monthly = float(row.get("monthly_charges", 0) or 0)
    tenure = float(row.get("tenure_months", 0) or 0)
    probability = float(row.get("churn_probability", 0) or 0)

    actions = []

    if risk == "High Risk" or probability >= 70:
        actions.append("Immediate retention outreach")
    elif risk == "Medium Risk" or probability >= 40:
        actions.append("Proactive engagement campaign")
    else:
        actions.append("Maintain engagement")

    if contract.lower() in {"month-to-month", "monthly"}:
        actions.append("Offer longer-term contract incentive")

    if monthly >= 80:
        actions.append("Prioritize premium/high-value support")

    if tenure <= 12:
        actions.append("Run onboarding & early-lifecycle campaign")

    if not actions:
        actions.append("Standard customer engagement")

    return " • ".join(dict.fromkeys(actions))


def safe_numeric(series):
    return pd.to_numeric(series, errors="coerce").fillna(0)


def make_rfm_view(data):
    temp = data.copy()

    temp["rfm_recency"] = 1 / (1 + safe_numeric(temp["tenure_months"]))
    temp["rfm_frequency"] = safe_numeric(
        temp.get("total_transactions", pd.Series(1, index=temp.index))
    )
    temp["rfm_monetary"] = safe_numeric(temp["total_charges"])

    def quintile_score(series, reverse=False):
        if series.nunique() <= 1:
            return pd.Series(3, index=series.index)

        ranked = series.rank(method="first")
        score = (
            pd.qcut(ranked, 5, labels=False, duplicates="drop") + 1
        )

        if reverse:
            score = 6 - score

        return score.astype(int)

    temp["R"] = quintile_score(temp["rfm_recency"], reverse=False)
    temp["F"] = quintile_score(temp["rfm_frequency"], reverse=False)
    temp["M"] = quintile_score(temp["rfm_monetary"], reverse=False)

    temp["RFM Score"] = temp[["R", "F", "M"]].sum(axis=1)

    def segment(score):
        if score >= 13:
            return "Champions"
        if score >= 10:
            return "Loyal Customers"
        if score >= 7:
            return "Potential Loyalists"
        if score >= 5:
            return "At Risk"
        return "Needs Attention"

    temp["RFM Segment"] = temp["RFM Score"].apply(segment)
    return temp


def assistant_local_answer(question, data):
    q = question.lower().strip()

    total = len(data)
    churned = int((data["churn"] == "Yes").sum())
    churn_rate = churned / total * 100 if total else 0
    high = data[data["risk_level"] == "High Risk"]
    medium = data[data["risk_level"] == "Medium Risk"]

    if any(x in q for x in ["high risk", "high-risk"]):
        return (
            f"### 🔴 High-Risk Customers\n"
            f"There are **{len(high):,} high-risk customers** in the current portfolio. "
            f"Their combined revenue exposure is **{money(high['total_charges'].sum())}**."
        )

    if "medium risk" in q:
        return (
            f"### 🟠 Medium-Risk Customers\n"
            f"There are **{len(medium):,} medium-risk customers**. "
            f"Consider proactive engagement before they move into the high-risk segment."
        )

    if "churn rate" in q or "churn percentage" in q:
        return (
            f"### 📉 Churn Rate\n"
            f"The current portfolio churn rate is **{churn_rate:.2f}%** "
            f"({churned:,} churned customers out of {total:,})."
        )

    if "revenue" in q and ("risk" in q or "at risk" in q):
        return (
            f"### 💰 Revenue at Risk\n"
            f"High-risk customers represent approximately **{money(high['total_charges'].sum())}** "
            f"in total-charge exposure."
        )

    if "customer" in q and ("total" in q or "how many" in q or "count" in q):
        return f"### 👥 Customer Base\nThere are **{total:,} customers** in the current dataset."

    if "recommend" in q or "retention" in q or "retain" in q:
        return (
            "### 🎯 Retention Strategy\n"
            "1. Prioritize high-risk, high-value customers.\n"
            "2. Contact month-to-month customers with suitable long-term-plan incentives.\n"
            "3. Give premium support to high-value customers.\n"
            "4. Use onboarding campaigns for customers with short tenure.\n"
            "5. Monitor medium-risk customers before they become high risk."
        )

    if "city" in q or "location" in q:
        if "city" in data.columns and len(high):
            city = high.groupby("city")["total_charges"].sum().sort_values(ascending=False)
            if len(city):
                return (
                    f"### 📍 Risk Concentration\n"
                    f"**{city.index[0]}** has the highest high-risk revenue exposure "
                    f"at approximately **{money(city.iloc[0])}**."
                )

    return (
        "### 🤖 ChurnIQ Assistant\n"
        "I can analyze the current customer dataset. Try asking:\n\n"
        "- **How many high-risk customers do we have?**\n"
        "- **What is our churn rate?**\n"
        "- **How much revenue is at risk?**\n"
        "- **Which city has the highest risk?**\n"
        "- **What retention strategy do you recommend?**"
    )


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown(
        """
    <div class="brand">
        <div>
            <span class="brand-icon">📊</span>
            <span class="brand-name">ChurnIQ</span>
        </div>
        <div class="brand-sub">
            Customer Intelligence Platform<br>
            Predict • Segment • Retain
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="status"><span class="status-dot"></span> Analytics engine online</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    page = st.radio(
        "WORKSPACE",
        [
            "📊 Overview",
            "👥 RFM Segmentation",
            "📅 Cohort Analysis",
            "🤖 Churn Prediction",
            "💰 Revenue at Risk",
            "🔎 Customer Explorer",
            "🤖 AI Business Assistant",
        ],
        label_visibility="visible",
    )

    st.markdown("---")
    if st.session_state.get("auth_user"):
        user = st.session_state.auth_user
        st.markdown(
            f"""
            <div style="padding:10px 0;color:#cbd5e1;font-size:12px;">
                <b style="color:#fff;">{user["name"]}</b><br>
                {user["email"]}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.caption("ChurnIQ v1.0 • Internal Analytics")

    if st.button("↩️ Sign Out", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.auth_user = None
        st.session_state.workspace_started = False
        st.rerun()


# =========================================================
# PAGE 1: EXECUTIVE DASHBOARD OVERVIEW
# =========================================================
if page == "📊 Overview":
    user_name = st.session_state.get("auth_user", {}).get("name", "there")

    st.markdown(
        f"""
        <div class="hero">
            <div style="font-size:12px;color:#93c5fd;font-weight:700;
                        letter-spacing:1px;text-transform:uppercase;">
                EXECUTIVE CUSTOMER INTELLIGENCE
            </div>
            <h1 style="margin-top:8px;">Welcome back, {user_name} 👋</h1>
            <p>Monitor customer health, churn exposure and revenue risk from one intelligent workspace.</p>
            <span class="hero-badge">● Analytics engine online</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Filters
    filter_cols = st.columns(3)

    with filter_cols[0]:
        city_options = (
            ["All"] + sorted(df["city"].dropna().astype(str).unique().tolist())
            if "city" in df.columns
            else ["All"]
        )
        selected_city = st.selectbox("City", city_options, key="exec_city")

    with filter_cols[1]:
        contract_options = (
            ["All"]
            + sorted(df["contract_type"].dropna().astype(str).unique().tolist())
            if "contract_type" in df.columns
            else ["All"]
        )
        selected_contract = st.selectbox(
            "Contract", contract_options, key="exec_contract"
        )

    with filter_cols[2]:
        selected_period = st.selectbox(
            "Analytics View",
            ["Current Portfolio", "High Risk Focus", "Churned Customers"],
            key="exec_period",
        )

    filtered = df.copy()

    if selected_city != "All" and "city" in filtered.columns:
        filtered = filtered[filtered["city"].astype(str) == selected_city]

    if selected_contract != "All" and "contract_type" in filtered.columns:
        filtered = filtered[
            filtered["contract_type"].astype(str) == selected_contract
        ]

    if selected_period == "High Risk Focus":
        filtered = filtered[filtered["risk_level"] == "High Risk"]
    elif selected_period == "Churned Customers":
        filtered = filtered[filtered["churn"] == "Yes"]

    total_customers = len(filtered)
    churned = int((filtered["churn"] == "Yes").sum())
    churn_rate = (churned / total_customers * 100) if total_customers else 0
    high_risk_df = filtered[filtered["risk_level"] == "High Risk"]
    revenue_risk = high_risk_df["total_charges"].sum()
    avg_probability = (
        filtered["churn_probability"].mean() if total_customers else 0
    )

    st.markdown(
        "<div class='section-title'>Executive Snapshot</div>",
        unsafe_allow_html=True,
    )

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(
            executive_metric(
                "TOTAL CUSTOMERS",
                f"{total_customers:,}",
                "Active analytical population",
            ),
            unsafe_allow_html=True,
        )

    with m2:
        st.markdown(
            executive_metric(
                "CHURN RATE",
                f"{churn_rate:.2f}%",
                f"{churned:,} customers churned",
            ),
            unsafe_allow_html=True,
        )

    with m3:
        st.markdown(
            executive_metric(
                "HIGH-RISK CUSTOMERS",
                f"{len(high_risk_df):,}",
                f"Avg. probability {avg_probability:.1f}%",
            ),
            unsafe_allow_html=True,
        )

    with m4:
        st.markdown(
            executive_metric(
                "REVENUE AT RISK",
                money(revenue_risk),
                "Estimated high-risk revenue",
            ),
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Trend + risk distribution
    left, right = st.columns([1.45, 1])

    with left:
        st.markdown(
            "<div class='section-title'>Churn Trend & Customer Health</div>",
            unsafe_allow_html=True,
        )

        trend = build_churn_trend(filtered)

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=trend.iloc[:, 0],
                y=trend["churn_rate"],
                mode="lines+markers",
                name="Churn Rate",
                line=dict(width=3),
            )
        )
        fig.update_yaxes(title="Churn Rate (%)")
        fig.update_xaxes(title="Customer Period")
        fig.update_layout(
            title="Customer churn pattern",
            hovermode="x unified",
        )
        st.plotly_chart(
            chart_layout(fig, 410),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with right:
        st.markdown(
            "<div class='section-title'>Risk Distribution</div>",
            unsafe_allow_html=True,
        )

        risk_data = (
            filtered["risk_level"]
            .value_counts()
            .reindex(["High Risk", "Medium Risk", "Low Risk"])
            .fillna(0)
            .reset_index()
        )
        risk_data.columns = ["risk_level", "customers"]

        fig = px.pie(
            risk_data,
            names="risk_level",
            values="customers",
            hole=0.62,
            color="risk_level",
            color_discrete_map={
                "High Risk": "#ef4444",
                "Medium Risk": "#f59e0b",
                "Low Risk": "#10b981",
            },
        )
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(
            chart_layout(fig, 410),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    # Top risk customers
    st.markdown(
        "<div class='section-title'>🔥 Priority Customers</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='section-caption'>High-risk customers with the highest predicted churn probability.</div>",
        unsafe_allow_html=True,
    )

    priority_columns = [
        "customer_id",
        "city",
        "contract_type",
        "monthly_charges",
        "total_charges",
        "churn_probability",
        "risk_level",
    ]
    priority_columns = [
        c for c in priority_columns if c in high_risk_df.columns
    ]

    priority = (
        high_risk_df[priority_columns]
        .sort_values("churn_probability", ascending=False)
        .head(8)
        .copy()
    )

    if "churn_probability" in priority.columns:
        priority["churn_probability"] = priority["churn_probability"].round(2)

    st.dataframe(
        priority,
        use_container_width=True,
        hide_index=True,
    )

    # Management insights
    st.markdown(
        "<div class='section-title'>💡 Management Insights</div>",
        unsafe_allow_html=True,
    )

    insight_cols = st.columns(3)

    top_city = "N/A"
    if len(high_risk_df) and "city" in high_risk_df.columns:
        top_city = high_risk_df.groupby("city")["total_charges"].sum().idxmax()

    top_segment = "N/A"
    if len(filtered) and "segment" in filtered.columns:
        top_segment = filtered["segment"].value_counts().idxmax()

    with insight_cols[0]:
        st.markdown(
            f"""
            <div class="insight">
                <b>🎯 Retention Priority</b><br>
                {len(high_risk_df):,} customers are currently classified as high risk.
                Prioritize high-value customers first.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with insight_cols[1]:
        st.markdown(
            f"""
            <div class="insight">
                <b>📍 Risk Concentration</b><br>
                <b>{top_city}</b> currently has the highest high-risk revenue exposure.
                Consider targeted retention campaigns.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with insight_cols[2]:
        st.markdown(
            f"""
            <div class="insight">
                <b>👥 Customer Mix</b><br>
                <b>{top_segment}</b> is the largest customer segment in the selected view.
                Use segment-specific engagement strategies.
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# PAGE 2: RFM SEGMENTATION
# =========================================================
elif page == "👥 RFM Segmentation":
    st.markdown(
        """
        <div class="hero">
            <div style="font-size:12px;color:#93c5fd;font-weight:700;
                        letter-spacing:1px;text-transform:uppercase;">
                CUSTOMER SEGMENTATION
            </div>
            <h1 style="margin-top:8px;">RFM Intelligence</h1>
            <p>Segment customers by behavioral value and identify where retention effort should be focused.</p>
            <span class="hero-badge">● Recency • Frequency • Monetary analysis</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    rfm = make_rfm_view(df)
    rfm["total_charges"] = pd.to_numeric(
        rfm["total_charges"], errors="coerce"
    ).fillna(0)

    segment_summary = (
        rfm.groupby("RFM Segment")
        .agg(
            customers=("customer_id", "count"),
            revenue=("total_charges", "sum"),
            avg_churn_probability=("churn_probability", "mean"),
        )
        .reset_index()
        .sort_values("revenue", ascending=False)
    )

    a, b, c, d = st.columns(4)
    with a:
        st.metric("Customers", f"{len(rfm):,}")
    with b:
        st.metric("Segments", f"{rfm['RFM Segment'].nunique():,}")
    with c:
        st.metric(
            "At-Risk Segment", f"{(rfm['RFM Segment'] == 'At Risk').sum():,}"
        )
    with d:
        champions_revenue = segment_summary.loc[
            segment_summary["RFM Segment"] == "Champions", "revenue"
        ].sum()
        st.metric("Champion Revenue", money(champions_revenue))

    left, right = st.columns([1.1, 1])

    with left:
        st.markdown(
            "<div class='section-title'>📊 Customer Value Segments</div>",
            unsafe_allow_html=True,
        )
        fig = px.bar(
            segment_summary,
            x="RFM Segment",
            y="customers",
            text="customers",
        )
        fig.update_layout(
            title="Customers by RFM segment",
            xaxis_title="Segment",
            yaxis_title="Customers",
        )
        st.plotly_chart(
            chart_layout(fig, 410),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with right:
        st.markdown(
            "<div class='section-title'>💰 Revenue by Segment</div>",
            unsafe_allow_html=True,
        )

        pie_labels = segment_summary["RFM Segment"].astype(str).tolist()

        pie_values = (
            pd.to_numeric(
                segment_summary["revenue"],
                errors="coerce",
            )
            .fillna(0)
            .tolist()
        )

        fig = px.pie(
        segment_summary,
        names="RFM Segment",
        values="revenue",
        hole=0.58,
        )
        names=pie_labels,
        values=pie_values,
        hole=0.58,
        

        fig.update_traces(
            texttemplate="%{percent:.1%}",
            textinfo="text",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Revenue: ₹%{value:,.0f}<br>"
                "Share: %{percent}<extra></extra>"
            ),
        )

        fig.update_layout(
            showlegend=True,
            legend=dict(
                orientation="h",
                y=-0.18,
            ),
        )

        st.plotly_chart(
            chart_layout(fig, 410),
            use_container_width=True,
            config={"displayModeBar": False},
        )
    st.markdown(
        "<div class='section-title'>🧭 Segment Performance</div>",
        unsafe_allow_html=True,
    )
    segment_table = segment_summary.copy()
    segment_table["revenue"] = segment_table["revenue"].round(2)
    segment_table["avg_churn_probability"] = segment_table[
        "avg_churn_probability"
    ].round(2)
    st.dataframe(segment_table, use_container_width=True, hide_index=True)

    st.markdown(
        "<div class='section-title'>🔎 Customer-Level RFM</div>",
        unsafe_allow_html=True,
    )

    segment_filter = st.selectbox(
        "Select RFM Segment",
        ["All"] + sorted(rfm["RFM Segment"].unique().tolist()),
        key="rfm_segment_filter",
    )

    rfm_filtered = (
        rfm
        if segment_filter == "All"
        else rfm[rfm["RFM Segment"] == segment_filter]
    )

    rfm_columns = [
        "customer_id",
        "R",
        "F",
        "M",
        "RFM Score",
        "RFM Segment",
        "churn_probability",
        "risk_level",
        "total_charges",
    ]
    rfm_columns = [c for c in rfm_columns if c in rfm_filtered.columns]

    rfm_display = rfm_filtered[rfm_columns].sort_values(
        "RFM Score", ascending=False
    ).head(20)

    st.dataframe(
        rfm_display,
        use_container_width=True,
        hide_index=True,
    )

    rfm_csv = rfm_filtered[rfm_columns].to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Export RFM Analysis",
        data=rfm_csv,
        file_name="churniq_rfm_analysis.csv",
        mime="text/csv",
    )


# =========================================================
# PAGE 3: COHORT ANALYSIS
# =========================================================
elif page == "📅 Cohort Analysis":
    st.markdown(
        """
        <div class="hero">
            <div style="font-size:12px;color:#93c5fd;font-weight:700;
                        letter-spacing:1px;text-transform:uppercase;">
                RETENTION ANALYTICS
            </div>
            <h1 style="margin-top:8px;">Cohort Retention Intelligence</h1>
            <p>Compare customer groups over their lifecycle and identify retention patterns.</p>
            <span class="hero-badge">● Cohort-based retention monitoring</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cohort = df.copy()

    date_candidates = ["signup_date", "join_date", "date", "cohort_month"]
    date_col = next((c for c in date_candidates if c in cohort.columns), None)

    if date_col:
        cohort["_cohort_date"] = pd.to_datetime(
            cohort[date_col], errors="coerce"
        )
        cohort = cohort.dropna(subset=["_cohort_date"])
        cohort["Cohort"] = cohort["_cohort_date"].dt.to_period("M").astype(str)
    else:
        cohort["Cohort"] = pd.cut(
            safe_numeric(cohort["tenure_months"]),
            bins=[-1, 3, 6, 12, 24, 36, 60, float("inf")],
            labels=[
                "0–3 mo",
                "4–6 mo",
                "7–12 mo",
                "13–24 mo",
                "25–36 mo",
                "37–60 mo",
                "60+ mo",
            ],
        ).astype(str)

    cohort_summary = (
        cohort.groupby("Cohort", observed=False)
        .agg(
            customers=("customer_id", "count"),
            churned=("churn", lambda x: (x == "Yes").sum()),
            revenue=("total_charges", "sum"),
            avg_churn_probability=("churn_probability", "mean"),
        )
        .reset_index()
    )
    cohort_summary["retention_rate"] = (
        1 - cohort_summary["churned"] / cohort_summary["customers"]
    ) * 100

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Cohorts", f"{len(cohort_summary):,}")
    with c2:
        st.metric(
            "Avg. Retention", f"{cohort_summary['retention_rate'].mean():.1f}%"
        )
    with c3:
        best_idx = cohort_summary["retention_rate"].idxmax()
        st.metric("Best Cohort", str(cohort_summary.loc[best_idx, "Cohort"]))
    with c4:
        st.metric("Cohort Revenue", money(cohort_summary["revenue"].sum()))

    left, right = st.columns([1.15, 1])

    with left:
        st.markdown(
            "<div class='section-title'>📈 Retention by Cohort</div>",
            unsafe_allow_html=True,
        )

        fig = px.line(
            cohort_summary,
            x="Cohort",
            y="retention_rate",
            markers=True,
        )
        fig.update_layout(
            title="Cohort retention rate",
            xaxis_title="Cohort",
            yaxis_title="Retention (%)",
        )
        st.plotly_chart(
            chart_layout(fig, 410),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with right:
        st.markdown(
            "<div class='section-title'>👥 Cohort Size</div>",
            unsafe_allow_html=True,
        )

        fig = px.bar(
            cohort_summary,
            x="Cohort",
            y="customers",
            text="customers",
        )
        fig.update_layout(
            title="Customers by cohort",
            xaxis_title="Cohort",
            yaxis_title="Customers",
        )
        st.plotly_chart(
            chart_layout(fig, 410),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    st.markdown(
        "<div class='section-title'>🧩 Cohort Performance Matrix</div>",
        unsafe_allow_html=True,
    )

    matrix = cohort_summary[
        [
            "Cohort",
            "customers",
            "churned",
            "retention_rate",
            "revenue",
            "avg_churn_probability",
        ]
    ].copy()

    matrix["retention_rate"] = matrix["retention_rate"].round(2)
    matrix["avg_churn_probability"] = matrix["avg_churn_probability"].round(2)

    st.dataframe(
        matrix,
        use_container_width=True,
        hide_index=True,
    )

    cohort_csv = matrix.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Export Cohort Report",
        data=cohort_csv,
        file_name="churniq_cohort_analysis.csv",
        mime="text/csv",
    )


# =========================================================
# PAGE 4: CHURN PREDICTION & RETENTION ENGINE
# =========================================================
elif page == "🤖 Churn Prediction":
    st.markdown(
        """
        <div class="hero">
            <div style="font-size:12px;color:#93c5fd;font-weight:700;
                        letter-spacing:1px;text-transform:uppercase;">
                RETENTION INTELLIGENCE
            </div>
            <h1 style="margin-top:8px;">Retention Recommendation Engine</h1>
            <p>Turn churn predictions into practical customer-retention actions.</p>
            <span class="hero-badge">● Recommendations generated from customer risk signals</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    high = df[df["risk_level"] == "High Risk"]
    medium = df[df["risk_level"] == "Medium Risk"]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("High Risk", f"{len(high):,}")
    with c2:
        st.metric("Medium Risk", f"{len(medium):,}")
    with c3:
        st.metric("High-Risk Revenue", money(high["total_charges"].sum()))
    with c4:
        st.metric(
            "Avg. High-Risk Probability",
            f"{high['churn_probability'].mean():.1f}%"
            if len(high)
            else "0.0%",
        )

    st.markdown(
        "<div class='section-title'>🎯 Customer Retention Queue</div>",
        unsafe_allow_html=True,
    )

    risk_filter = st.selectbox(
        "Risk level",
        ["High Risk", "Medium Risk", "All At-Risk"],
        key="retention_risk_filter",
    )

    if risk_filter == "High Risk":
        retention_df = df[df["risk_level"] == "High Risk"].copy()
    elif risk_filter == "Medium Risk":
        retention_df = df[df["risk_level"] == "Medium Risk"].copy()
    else:
        retention_df = df[
            df["risk_level"].isin(["High Risk", "Medium Risk"])
        ].copy()

    retention_df["recommendation"] = retention_df.apply(
        retention_recommendation, axis=1
    )
    retention_df["priority_score"] = (
        retention_df["churn_probability"] * 0.65
        + (
            retention_df["total_charges"]
            / max(float(df["total_charges"].max()), 1)
            * 100
        )
        * 0.35
    )

    retention_df = retention_df.sort_values("priority_score", ascending=False)

    show_cols = [
        "customer_id",
        "city",
        "contract_type",
        "tenure_months",
        "monthly_charges",
        "total_charges",
        "churn_probability",
        "risk_level",
        "recommendation",
    ]
    show_cols = [c for c in show_cols if c in retention_df.columns]

    display_df = retention_df[show_cols].head(15).copy()
    if "churn_probability" in display_df.columns:
        display_df["churn_probability"] = display_df[
            "churn_probability"
        ].round(2)

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown(
        "<div class='section-title'>⚡ Recommended Action Plan</div>",
        unsafe_allow_html=True,
    )

    action_cols = st.columns(3)

    with action_cols[0]:
        st.markdown(
            """
            <div class="insight">
                <b>🔴 High Risk</b><br><br>
                Contact immediately, review customer pain points and provide
                a personalized retention incentive where appropriate.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with action_cols[1]:
        st.markdown(
            """
            <div class="insight">
                <b>🟠 Medium Risk</b><br><br>
                Start proactive engagement, monitor usage and encourage
                customers toward stronger long-term plans.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with action_cols[2]:
        st.markdown(
            """
            <div class="insight">
                <b>🟢 Low Risk</b><br><br>
                Maintain customer satisfaction with regular engagement,
                service quality and loyalty initiatives.
            </div>
            """,
            unsafe_allow_html=True,
        )

    csv_data = retention_df[show_cols].to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Export Retention Queue",
        data=csv_data,
        file_name="churniq_retention_queue.csv",
        mime="text/csv",
        use_container_width=False,
    )


# =========================================================
# PAGE 5: REVENUE AT RISK
# =========================================================
elif page == "💰 Revenue at Risk":
    st.markdown(
        """
        <div class="hero">
            <div style="font-size:12px;color:#93c5fd;font-weight:700;
                        letter-spacing:1px;text-transform:uppercase;">
                REVENUE INTELLIGENCE
            </div>
            <h1 style="margin-top:8px;">Revenue at Risk</h1>
            <p>Understand how much customer value is exposed to churn and where the financial risk is concentrated.</p>
            <span class="hero-badge">● Financial exposure monitoring</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    f1, f2, f3 = st.columns(3)

    with f1:
        revenue_city = st.selectbox(
            "City",
            ["All"] + sorted(df["city"].dropna().astype(str).unique().tolist()),
            key="revenue_city",
        )

    with f2:
        revenue_contract = st.selectbox(
            "Contract",
            ["All"]
            + sorted(df["contract_type"].dropna().astype(str).unique().tolist()),
            key="revenue_contract",
        )

    with f3:
        revenue_risk = st.selectbox(
            "Risk Segment",
            ["All", "High Risk", "Medium Risk", "Low Risk"],
            key="revenue_risk",
        )

    revenue_df = df.copy()

    if revenue_city != "All":
        revenue_df = revenue_df[revenue_df["city"].astype(str) == revenue_city]

    if revenue_contract != "All":
        revenue_df = revenue_df[
            revenue_df["contract_type"].astype(str) == revenue_contract
        ]

    if revenue_risk != "All":
        revenue_df = revenue_df[revenue_df["risk_level"] == revenue_risk]

    high_risk = revenue_df[revenue_df["risk_level"] == "High Risk"].copy()
    medium_risk = revenue_df[revenue_df["risk_level"] == "Medium Risk"].copy()
    at_risk = revenue_df[
        revenue_df["risk_level"].isin(["High Risk", "Medium Risk"])
    ].copy()

    total_revenue = revenue_df["total_charges"].sum()
    high_risk_revenue = high_risk["total_charges"].sum()
    medium_risk_revenue = medium_risk["total_charges"].sum()
    total_at_risk = at_risk["total_charges"].sum()

    exposure_pct = (
        total_at_risk / total_revenue * 100 if total_revenue else 0
    )

    st.markdown(
        "<div class='section-title'>Financial Exposure Snapshot</div>",
        unsafe_allow_html=True,
    )

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.metric("Portfolio Revenue", money(total_revenue))

    with k2:
        st.metric("Revenue at Risk", money(total_at_risk))

    with k3:
        st.metric("High-Risk Exposure", money(high_risk_revenue))

    with k4:
        st.metric("Risk Exposure", f"{exposure_pct:.1f}%")

    left, right = st.columns([1.2, 1])

    with left:
        st.markdown(
            "<div class='section-title'>💰 Revenue Exposure by Risk</div>",
            unsafe_allow_html=True,
        )

        exposure_data = pd.DataFrame(
            {
                "Risk": ["Low Risk", "Medium Risk", "High Risk"],
                "Revenue": [
                    revenue_df[revenue_df["risk_level"] == "Low Risk"][
                        "total_charges"
                    ].sum(),
                    medium_risk_revenue,
                    high_risk_revenue,
                ],
            }
        )

        fig = px.bar(
            exposure_data,
            x="Risk",
            y="Revenue",
            text_auto=".2s",
        )
        fig.update_layout(
            title="Customer revenue exposure",
            yaxis_title="Revenue",
            xaxis_title="Risk Level",
        )
        st.plotly_chart(
            chart_layout(fig, 410),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with right:
        st.markdown(
            "<div class='section-title'>🎯 Exposure Composition</div>",
            unsafe_allow_html=True,
        )

        composition = pd.DataFrame(
            {
                "Category": ["High Risk", "Medium Risk", "Low Risk"],
                "Revenue": [
                    high_risk_revenue,
                    medium_risk_revenue,
                    revenue_df[revenue_df["risk_level"] == "Low Risk"][
                        "total_charges"
                    ].sum(),
                ],
            }
        )

        fig = px.pie(
            composition,
            names="Category",
            values="Revenue",
            hole=0.60,
        )
        fig.update_traces(textinfo="percent")
        st.plotly_chart(
            chart_layout(fig, 410),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    st.markdown(
        "<div class='section-title'>📍 Revenue Risk by City</div>",
        unsafe_allow_html=True,
    )

    if "city" in revenue_df.columns:
        city_risk = (
            revenue_df[
                revenue_df["risk_level"].isin(["High Risk", "Medium Risk"])
            ]
            .groupby("city")
            .agg(
                revenue_at_risk=("total_charges", "sum"),
                customers=("customer_id", "count"),
                avg_probability=("churn_probability", "mean"),
            )
            .reset_index()
            .sort_values("revenue_at_risk", ascending=False)
        )

        city_risk["avg_probability"] = city_risk["avg_probability"].round(2)

        st.dataframe(
            city_risk.head(10),
            use_container_width=True,
            hide_index=True,
        )

    st.markdown(
        "<div class='section-title'>🔥 Highest Revenue Exposure Customers</div>",
        unsafe_allow_html=True,
    )

    risk_customers = at_risk.sort_values(
        ["total_charges", "churn_probability"],
        ascending=[False, False],
    ).copy()

    exposure_columns = [
        "customer_id",
        "city",
        "contract_type",
        "monthly_charges",
        "total_charges",
        "churn_probability",
        "risk_level",
    ]
    exposure_columns = [
        c for c in exposure_columns if c in risk_customers.columns
    ]

    top_exposure = risk_customers[exposure_columns].head(15).copy()

    if "churn_probability" in top_exposure.columns:
        top_exposure["churn_probability"] = top_exposure[
            "churn_probability"
        ].round(2)

    st.dataframe(
        top_exposure,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown(
        "<div class='section-title'>💡 Financial Risk Actions</div>",
        unsafe_allow_html=True,
    )

    a1, a2, a3 = st.columns(3)

    with a1:
        st.markdown(
            f"""
            <div class="insight">
                <b>🔴 Protect High-Value Revenue</b><br><br>
                {len(high_risk):,} high-risk customers account for
                <b>{money(high_risk_revenue)}</b> in exposure.
                Prioritize these customers first.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with a2:
        st.markdown(
            f"""
            <div class="insight">
                <b>🟠 Prevent Risk Escalation</b><br><br>
                {len(medium_risk):,} medium-risk customers represent
                <b>{money(medium_risk_revenue)}</b>.
                Early engagement can reduce future exposure.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with a3:
        st.markdown(
            f"""
            <div class="insight">
                <b>📊 Exposure Monitoring</b><br><br>
                Current at-risk exposure is
                <b>{exposure_pct:.1f}%</b> of the selected portfolio revenue.
                Monitor this KPI regularly.
            </div>
            """,
            unsafe_allow_html=True,
        )

    export_columns = [
        c
        for c in [
            "customer_id",
            "city",
            "contract_type",
            "monthly_charges",
            "total_charges",
            "churn_probability",
            "risk_level",
        ]
        if c in at_risk.columns
    ]

    export_data = (
        at_risk[export_columns]
        .sort_values(
            "total_charges",
            ascending=False,
        )
        .to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        "📥 Export Revenue Risk Report",
        data=export_data,
        file_name="churniq_revenue_risk_report.csv",
        mime="text/csv",
    )


# =========================================================
# PAGE 6: CUSTOMER EXPLORER
# =========================================================
elif page == "🔎 Customer Explorer":
    st.markdown(
        """
        <div class="hero">
            <div style="font-size:12px;color:#93c5fd;font-weight:700;
                        letter-spacing:1px;text-transform:uppercase;">
                CUSTOMER 360
            </div>
            <h1 style="margin-top:8px;">Customer Explorer</h1>
            <p>Inspect individual customer health, churn probability, value and recommended retention actions.</p>
            <span class="hero-badge">● Customer intelligence profile</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    search_col, risk_col = st.columns([2, 1])

    with search_col:
        customer_ids = df["customer_id"].dropna().astype(str).tolist()
        selected_customer = st.selectbox(
            "Search Customer",
            customer_ids,
            key="customer_profile_id",
        )

    customer = df[df["customer_id"].astype(str) == selected_customer].iloc[0]

    with risk_col:
        risk_value = str(customer.get("risk_level", "Unknown"))
        st.markdown(
            f"""
            <div style="
                margin-top:28px;padding:12px 16px;border-radius:14px;
                background:#f8fafc;border:1px solid #e2e8f0;
                text-align:center;font-weight:700;">
                Risk Status: {risk_value}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div style="
            margin:16px 0 22px;padding:24px;border-radius:20px;
            background:linear-gradient(135deg,#0f172a,#1e293b);
            color:white;">
            <div style="font-size:12px;color:#93c5fd;font-weight:700;
                        letter-spacing:1px;text-transform:uppercase;">
                CUSTOMER PROFILE
            </div>
            <div style="font-size:30px;font-weight:800;margin-top:6px;">
                {selected_customer}
            </div>
            <div style="color:#cbd5e1;margin-top:5px;">
                {customer.get("city", "Unknown")} •
                {customer.get("contract_type", "Unknown")} •
                {customer.get("tenure_months", 0)} months tenure
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    probability = float(customer.get("churn_probability", 0) or 0)
    monthly = float(customer.get("monthly_charges", 0) or 0)
    total = float(customer.get("total_charges", 0) or 0)
    tenure = float(customer.get("tenure_months", 0) or 0)

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.metric("Churn Probability", f"{probability:.2f}%")
    with k2:
        st.metric("Monthly Charges", money(monthly))
    with k3:
        st.metric("Customer Value", money(total))
    with k4:
        st.metric("Tenure", f"{tenure:.0f} months")

    left, right = st.columns([1, 1.15])

    with left:
        st.markdown(
            "<div class='section-title'>🎯 Churn Risk Score</div>",
            unsafe_allow_html=True,
        )

        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=probability,
                number={"suffix": "%"},
                title={"text": "Predicted Churn Probability"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#ef4444"},
                    "steps": [
                        {"range": [0, 40], "color": "#dcfce7"},
                        {"range": [40, 70], "color": "#fef3c7"},
                        {"range": [70, 100], "color": "#fee2e2"},
                    ],
                },
            )
        )
        st.plotly_chart(
            chart_layout(gauge, 330),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with right:
        st.markdown(
            "<div class='section-title'>👤 Customer Details</div>",
            unsafe_allow_html=True,
        )

        details = {
            "Customer ID": selected_customer,
            "City": customer.get("city", "—"),
            "Contract": customer.get("contract_type", "—"),
            "Tenure": f"{tenure:.0f} months",
            "Monthly Charges": money(monthly),
            "Total Charges": money(total),
            "Current Churn": customer.get("churn", "—"),
            "Risk Level": risk_value,
        }

        detail_df = pd.DataFrame(
            list(details.items()),
            columns=["Attribute", "Value"],
        )

        st.dataframe(
            detail_df,
            use_container_width=True,
            hide_index=True,
        )

    recommendation = retention_recommendation(customer)

    st.markdown(
        "<div class='section-title'>💡 Personalized Retention Action</div>",
        unsafe_allow_html=True,
    )

    icon = "🔴" if risk_value == "High Risk" else ("🟠" if risk_value == "Medium Risk" else "🟢")

    st.markdown(
        f"""
        <div class="insight" style="font-size:15px;line-height:1.7;">
            <b>{icon} Recommended Action</b><br>
            {recommendation}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='section-title'>📌 Customer Signals</div>",
        unsafe_allow_html=True,
    )

    signal_cols = st.columns(3)

    with signal_cols[0]:
        status = (
            "High exposure"
            if total >= df["total_charges"].median()
            else "Standard exposure"
        )
        st.markdown(
            f"<div class='insight'><b>💰 Value Signal</b><br>{status}</div>",
            unsafe_allow_html=True,
        )

    with signal_cols[1]:
        contract_signal = (
            "Contract upgrade opportunity"
            if str(customer.get("contract_type", "")).lower()
            in {"month-to-month", "monthly"}
            else "Stable contract profile"
        )
        st.markdown(
            f"<div class='insight'><b>📄 Contract Signal</b><br>{contract_signal}</div>",
            unsafe_allow_html=True,
        )

    with signal_cols[2]:
        tenure_signal = (
            "Early lifecycle customer"
            if tenure <= 12
            else "Established customer"
        )
        st.markdown(
            f"<div class='insight'><b>⏱️ Tenure Signal</b><br>{tenure_signal}</div>",
            unsafe_allow_html=True,
        )


# =========================================================
# PAGE 7: AI BUSINESS ASSISTANT
# =========================================================
elif page == "🤖 AI Business Assistant":
    st.markdown(
        """
        <div class="hero">
            <div style="font-size:12px;color:#93c5fd;font-weight:700;
                        letter-spacing:1px;text-transform:uppercase;">
                INTELLIGENT BUSINESS ANALYTICS
            </div>
            <h1 style="margin-top:8px;">AI Business Assistant</h1>
            <p>Ask questions about customers, churn, risk and revenue using natural language.</p>
            <span class="hero-badge">● Connected to ChurnIQ customer intelligence</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "ai_messages" not in st.session_state:
        st.session_state.ai_messages = []

    st.markdown(
        "<div class='section-title'>⚡ Quick Questions</div>",
        unsafe_allow_html=True,
    )

    q1, q2, q3, q4 = st.columns(4)
    quick_question = None

    with q1:
        if st.button("🔴 High-risk count", use_container_width=True):
            quick_question = "How many high-risk customers do we have?"

    with q2:
        if st.button("📉 Churn rate", use_container_width=True):
            quick_question = "What is our churn rate?"

    with q3:
        if st.button("💰 Revenue at risk", use_container_width=True):
            quick_question = "How much revenue is at risk?"

    with q4:
        if st.button("🎯 Retention strategy", use_container_width=True):
            quick_question = "What retention strategy do you recommend?"

    for message in st.session_state.ai_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    typed_question = st.chat_input(
        "Ask ChurnIQ about customers, churn, risk or revenue..."
    )

    question = quick_question or typed_question

    if question:
        st.session_state.ai_messages.append({"role": "user", "content": question})

        with st.chat_message("user"):
            st.markdown(question)

        answer = None

        try:
            from src.rag._engine import answer_question
            answer = answer_question(question)
        except Exception:
            answer = None

        if not answer:
            answer = assistant_local_answer(question, df)

        st.session_state.ai_messages.append(
            {"role": "assistant", "content": answer}
        )

        with st.chat_message("assistant"):
            st.markdown(answer)

    if st.session_state.ai_messages:
        if st.button("🗑️ Clear Conversation"):
            st.session_state.ai_messages = []
            st.rerun()


# =========================================================
# FOOTER
# =========================================================
st.markdown(
    """
    <div style="
        margin-top:42px;
        padding:18px 4px 12px;
        border-top:1px solid #e2e8f0;
        color:#94a3b8;
        font-size:11px;
        text-align:center;">
        <b style="color:#475569;">ChurnIQ v1.0</b> • Customer Intelligence Platform
        &nbsp;•&nbsp; Predict churn. Protect revenue. Retain customers.
    </div>
    """,
    unsafe_allow_html=True,
)
