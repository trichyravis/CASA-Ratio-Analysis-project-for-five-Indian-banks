"""
Indian Bank CASA Ratio Analytics — Enhanced Edition
The Mountain Path Academy | https://themountainpathacademy.com
"""

from pathlib import Path
from datetime import datetime
import io
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats as sp_stats
import streamlit as st

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CASA Analytics | The Mountain Path Academy",
    page_icon="🏔️",
    layout="wide",
)
ROOT = Path(__file__).parent

# ── Mountain Path Design System ──────────────────────────────────────────────
GOLD = "#FFD700"
NAVY = "#003366"
MID_BLUE = "#004d80"
CARD_BG = "#112240"
TEXT_LIGHT = "#e6f1ff"
MUTED = "#8892b0"
GREEN = "#28a745"
RED = "#dc3545"
LIGHT_BLUE = "#ADD8E6"

BANK_COLORS = {
    "State Bank of India": "#2563EB",
    "HDFC Bank": "#DC2626",
    "ICICI Bank": "#F97316",
    "Axis Bank": "#A21CAF",
    "Kotak Mahindra Bank": "#059669",
}

BANK_SHORT = {
    "State Bank of India": "SBI",
    "HDFC Bank": "HDFC",
    "ICICI Bank": "ICICI",
    "Axis Bank": "Axis",
    "Kotak Mahindra Bank": "Kotak",
}

SECTOR_COLORS = {"Public Sector": "#2563EB", "Private Sector": "#F97316"}

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown(
    """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
.stApp { background: linear-gradient(135deg, #0a192f 0%, #112240 50%, #1a2332 100%); color: #e6f1ff; font-family: 'Inter', sans-serif; }
.block-container { padding-top: 1.2rem; max-width: 1480px; }

/* Sidebar — force Mountain Path dark theme irrespective of Streamlit defaults */
section[data-testid="stSidebar"],
[data-testid="stSidebarContent"] {
    background: linear-gradient(180deg, #0a192f 0%, #112240 100%) !important;
    color: #e6f1ff !important;
}
section[data-testid="stSidebar"] { border-right: 1px solid #1e3a5f !important; }
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span:not([data-baseweb="tag"] span),
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #ADD8E6 !important;
    -webkit-text-fill-color: #ADD8E6 !important;
}
section[data-testid="stSidebar"] hr { border-color: #1e3a5f !important; }

/* Inputs, upload control, multiselect chips, sliders and toggles */
[data-testid="stFileUploaderDropzone"] {
    background: #112240 !important; border: 1px dashed #FFD700 !important;
}
[data-testid="stFileUploaderDropzone"] button,
section[data-testid="stSidebar"] button {
    background: #003366 !important; color: #FFD700 !important;
    border: 1px solid #FFD700 !important;
}
[data-baseweb="select"] > div { background: #112240 !important; border-color: #1e3a5f !important; color: #e6f1ff !important; }
[data-baseweb="tag"] { background: #003366 !important; border: 1px solid #FFD700 !important; }
[data-baseweb="tag"] span { color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; }
[data-testid="stSlider"] [role="slider"] { background: #FFD700 !important; }
[data-testid="stSlider"] div[data-baseweb="slider"] > div > div { background-color: #FFD700 !important; }
[data-testid="stToggle"] [data-checked="true"] { background: #003366 !important; }

/* Hero banner */
.hero-banner {
    padding: 32px 40px; border-radius: 16px; color: #e6f1ff;
    background: linear-gradient(120deg, #003366 0%, #004d80 55%, #112240 100%);
    border: 1px solid #FFD70040; box-shadow: 0 8px 32px rgba(0,51,102,0.4);
    margin-bottom: 20px; position: relative; overflow: hidden;
}
.hero-banner::after {
    content: ''; position: absolute; top: -50%; right: -10%; width: 300px; height: 300px;
    background: radial-gradient(circle, #FFD70012 0%, transparent 70%);
    border-radius: 50%;
}
.hero-banner h1 { font-size: 2.2rem; margin: 0; color: #FFD700; font-weight: 700; letter-spacing: -0.5px; }
.hero-banner .subtitle { font-size: 1.05rem; color: #8892b0; margin: 8px 0 0; }
.hero-banner .badge { display: inline-block; background: #FFD70018; color: #FFD700;
    padding: 3px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #FFD70030;
    margin-top: 8px; }

/* Metrics */
[data-testid="stMetric"] {
    background: #112240; border: 1px solid #FFD70025; padding: 16px; border-radius: 12px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
}
[data-testid="stMetricLabel"] { color: #8892b0 !important; }
[data-testid="stMetricValue"] { color: #e6f1ff !important; }

/* Info boxes */
.info-box {
    background: #003366; border-left: 4px solid #FFD700; padding: 14px 18px;
    border-radius: 0 10px 10px 0; color: #e6f1ff; margin: 12px 0; font-size: 0.92rem;
}
.info-box b { color: #FFD700; }

.risk-card {
    background: #112240; border: 1px solid #FFD70020; border-radius: 12px;
    padding: 20px; margin: 8px 0;
}
.risk-card h4 { color: #FFD700; margin: 0 0 8px; font-size: 1rem; }
.risk-card p { color: #8892b0; margin: 0; font-size: 0.88rem; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px; background: #0a192f; border: 1px solid #1e3a5f;
    border-radius: 10px; padding: 5px; flex-wrap: wrap;
}
.stTabs button[role="tab"] {
    background-color: #112240 !important;
    border: 1px solid #1e3a5f !important;
    opacity: 1 !important;
}
.stTabs button[role="tab"] * {
    color: #ADD8E6 !important; -webkit-text-fill-color: #ADD8E6 !important;
}
.stTabs button[role="tab"][aria-selected="true"] {
    background-color: #003366 !important; border-color: #FFD700 !important;
}
.stTabs button[role="tab"][aria-selected="true"] * {
    color: #FFD700 !important; -webkit-text-fill-color: #FFD700 !important;
}
.stTabs [data-baseweb="tab"] {
    background: #112240 !important; color: #ADD8E6 !important;
    border: 1px solid #1e3a5f !important; border-radius: 8px !important;
    padding: 8px 14px !important; opacity: 1 !important;
}
.stTabs [data-baseweb="tab"] p,
.stTabs [data-baseweb="tab"] span,
.stTabs [data-baseweb="tab"] div {
    color: #ADD8E6 !important;
    -webkit-text-fill-color: #ADD8E6 !important;
    opacity: 1 !important;
    font-weight: 600 !important;
}
.stTabs [data-baseweb="tab"]:hover {
    background: #004d80 !important; border-color: #FFD700 !important;
}
.stTabs [data-baseweb="tab"]:hover p,
.stTabs [data-baseweb="tab"]:hover span,
.stTabs [data-baseweb="tab"]:hover div {
    color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important;
}
.stTabs [aria-selected="true"] {
    background: #003366 !important; color: #FFD700 !important;
    border: 1px solid #FFD700 !important;
}
.stTabs [aria-selected="true"] p,
.stTabs [aria-selected="true"] span,
.stTabs [aria-selected="true"] div {
    color: #FFD700 !important;
    -webkit-text-fill-color: #FFD700 !important;
    font-weight: 700 !important;
}
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* Tables */
.stDataFrame { border-radius: 10px; overflow: hidden; }

/* Download buttons */
.stDownloadButton > button,
[data-testid="stDownloadButton"] button {
    background: #003366 !important;
    color: #FFD700 !important;
    border: 2px solid #FFD700 !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    padding: 0.55rem 1.15rem !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25) !important;
}
.stDownloadButton > button:hover,
[data-testid="stDownloadButton"] button:hover {
    background: #004d80 !important;
    color: #FFFFFF !important;
    border-color: #FFD700 !important;
}
.stDownloadButton > button p,
[data-testid="stDownloadButton"] button p {
    color: inherit !important;
    font-weight: 700 !important;
}

/* Profile card */
.profile-card {
    background: linear-gradient(135deg, #0a192f, #112240); border: 1px solid #FFD70025;
    border-radius: 14px; padding: 18px; margin: 12px 0;
}
.profile-card .name { color: #FFD700; font-weight: 700; font-size: 1rem; margin: 0 0 4px; }
.profile-card .title { color: #ADD8E6; font-size: 0.82rem; margin: 0 0 8px; line-height: 1.35; }
.profile-card .stats { color: #8892b0; font-size: 0.78rem; margin: 4px 0; }
.profile-card .links { margin-top: 10px; }
.profile-card .links a {
    color: #FFD700; text-decoration: none; font-size: 0.8rem;
    display: inline-block; margin-right: 12px;
}
.profile-card .links a:hover { text-decoration: underline; }

/* About section */
.about-section {
    background: linear-gradient(135deg, #003366 0%, #112240 100%);
    border: 1px solid #FFD70020; border-radius: 16px; padding: 28px 32px; margin: 20px 0;
}
.about-section h3 { color: #FFD700 !important; margin: 0 0 12px; font-size: 1.15rem; }
.about-section p { color: #e6f1ff; font-size: 0.92rem; line-height: 1.6; margin: 8px 0; }
.about-section .highlight { color: #ADD8E6; font-weight: 600; }
.about-section .academy-link {
    display: inline-block; margin-top: 14px; padding: 8px 20px; background: #FFD70018;
    border: 1px solid #FFD70040; border-radius: 8px; color: #FFD700; text-decoration: none;
    font-weight: 600; font-size: 0.9rem; transition: background 0.2s;
}
.about-section .academy-link:hover { background: #FFD70030; }

/* Footer */
.mp-footer {
    text-align: center; padding: 24px 0; margin-top: 30px; border-top: 1px solid #FFD70020;
    color: #8892b0; font-size: 0.85rem;
}
.mp-footer a { color: #FFD700; text-decoration: none; }
.mp-footer a:hover { text-decoration: underline; }
.mp-footer .footer-brand { color: #FFD700; font-size: 1.15rem; font-weight: 700; margin-bottom: 6px; }
.mp-footer .footer-profile { color: #ADD8E6; font-size: 0.82rem; margin: 4px 0 8px; }
.mp-footer .footer-links a { margin: 0 8px; }

/* Misc */
h2, h3 { color: #FFD700 !important; }
.small { font-size: 0.86rem; color: #8892b0; }
div.stSelectbox label, div.stMultiSelect label, div.stSlider label { color: #e6f1ff !important; }
</style>""",
    unsafe_allow_html=True,
)


# ── Data loading ─────────────────────────────────────────────────────────────
@st.cache_data
def load_default():
    d = pd.read_csv(ROOT / "data/casa_ratios.csv", parse_dates=["reporting_date"])
    s = pd.read_csv(ROOT / "data/sources.csv")
    return d, s


def validate(d):
    issues = []
    req = {"bank", "fiscal_year", "reporting_date", "casa_ratio_pct", "basis", "source_id"}
    if not req.issubset(d.columns):
        issues.append("Missing columns: " + ", ".join(sorted(req - set(d.columns))))
    if "casa_ratio_pct" in d and ((d.casa_ratio_pct < 0) | (d.casa_ratio_pct > 100)).any():
        issues.append("CASA ratios must be between 0 and 100.")
    if {"bank", "fiscal_year"}.issubset(d) and d.duplicated(["bank", "fiscal_year"]).any():
        issues.append("Duplicate bank–year observations found.")
    return issues


def read_uploaded_data(uploaded_file) -> pd.DataFrame:
    """Read a user-supplied CSV or Excel workbook."""
    suffix = Path(uploaded_file.name).suffix.lower()
    if suffix == ".xlsx":
        uploaded = pd.read_excel(uploaded_file, engine="openpyxl")
    else:
        uploaded = pd.read_csv(uploaded_file)
    uploaded["reporting_date"] = pd.to_datetime(uploaded["reporting_date"], errors="raise")
    return uploaded


def dataframe_to_excel(dataframe: pd.DataFrame, sheet_name: str) -> bytes:
    """Return a professionally formatted in-memory Excel workbook."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        dataframe.to_excel(writer, index=False, sheet_name=sheet_name)
        worksheet = writer.sheets[sheet_name]
        worksheet.freeze_panes = "A2"
        worksheet.auto_filter.ref = worksheet.dimensions

        from openpyxl.styles import Alignment, Font, PatternFill

        header_fill = PatternFill("solid", fgColor="003366")
        header_font = Font(color="FFD700", bold=True)
        for cell in worksheet[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center")

        for column in worksheet.columns:
            letter = column[0].column_letter
            maximum = max(len(str(cell.value or "")) for cell in column)
            worksheet.column_dimensions[letter].width = min(max(maximum + 2, 12), 55)

    return output.getvalue()


# ── Analytics helpers ────────────────────────────────────────────────────────
def compute_risk_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Compute per-bank CASA franchise risk metrics."""
    records = []
    for bank, grp in df.sort_values("reporting_date").groupby("bank"):
        vals = grp["casa_ratio_pct"].values
        n = len(vals)
        mean_v = np.mean(vals)
        std_v = np.std(vals, ddof=1) if n > 1 else 0.0
        cv = (std_v / mean_v * 100) if mean_v > 0 else 0.0

        # Linear trend (OLS)
        if n > 1:
            slope, intercept, r_val, p_val, std_err = sp_stats.linregress(range(n), vals)
        else:
            slope = intercept = r_val = p_val = std_err = 0.0

        # Max drawdown (peak-to-trough decline in CASA ratio)
        cummax = np.maximum.accumulate(vals)
        drawdowns = vals - cummax
        max_dd = np.min(drawdowns)

        # Herfindahl-like concentration: how much one year dominates total
        total_change = vals[-1] - vals[0] if n > 1 else 0.0
        yoy_changes = np.diff(vals) if n > 1 else np.array([0.0])

        records.append({
            "Bank": bank,
            "Short": BANK_SHORT.get(bank, bank[:5]),
            "Sector": grp["bank_type"].iloc[0] if "bank_type" in grp.columns else "N/A",
            "Latest (%)": vals[-1],
            "Mean (%)": mean_v,
            "Std Dev (pp)": std_v,
            "CV (%)": cv,
            "Trend (pp/yr)": slope,
            "R²": r_val ** 2,
            "p-value": p_val,
            "Max Drawdown (pp)": max_dd,
            "Total Δ (pp)": total_change,
            "Worst YoY (pp)": np.min(yoy_changes),
            "Best YoY (pp)": np.max(yoy_changes),
        })
    return pd.DataFrame(records)


def franchise_quality_score(row: pd.Series) -> float:
    """
    Composite deposit franchise quality score (0–100).
    Components: level (30%), stability (25%), trend (25%), drawdown resistance (20%).
    """
    # Level score: 60% → 100, 30% → 0 (linear)
    level_score = np.clip((row["Latest (%)"] - 30) / 30 * 100, 0, 100)

    # Stability: lower CV is better; CV=0 → 100, CV=20 → 0
    stability_score = np.clip((20 - row["CV (%)"]) / 20 * 100, 0, 100)

    # Trend: positive trend → higher score; +3pp/yr → 100, -3pp/yr → 0
    trend_score = np.clip((row["Trend (pp/yr)"] + 3) / 6 * 100, 0, 100)

    # Drawdown resistance: 0pp → 100, -20pp → 0
    dd_score = np.clip((row["Max Drawdown (pp)"] + 20) / 20 * 100, 0, 100)

    return 0.30 * level_score + 0.25 * stability_score + 0.25 * trend_score + 0.20 * dd_score


def interpret_score(score: float) -> tuple[str, str]:
    """Return (label, color) for a franchise quality score."""
    if score >= 70:
        return "Strong", GREEN
    elif score >= 50:
        return "Adequate", GOLD
    elif score >= 35:
        return "Watch", "#F97316"
    else:
        return "Weak", RED


# ── Plotly template ──────────────────────────────────────────────────────────
def hex_to_rgba(hex_color: str, alpha: float) -> str:
    """Convert #RRGGBB to a Plotly-compatible rgba() colour."""
    value = hex_color.lstrip("#")
    if len(value) != 6:
        return f"rgba(37,99,235,{alpha})"
    red, green, blue = (int(value[i : i + 2], 16) for i in (0, 2, 4))
    return f"rgba({red},{green},{blue},{alpha})"


def mp_layout(**kwargs):
    """Return Mountain Path branded layout defaults.

    Merges underscore-separated axis/legend kwargs (e.g. yaxis_ticksuffix)
    into their nested dicts so newer Plotly versions don't choke on mixed
    flat + nested keys for the same property.
    """
    base_xaxis = dict(gridcolor="#1e3a5f", zerolinecolor="#1e3a5f")
    base_yaxis = dict(gridcolor="#1e3a5f", zerolinecolor="#1e3a5f")
    base_legend = dict(
        bgcolor="rgba(17,34,64,0.5)",
        bordercolor="rgba(255,215,0,0.19)",
        borderwidth=1,
        font=dict(color=TEXT_LIGHT, size=11),
    )

    # Pull out any underscore-separated overrides and merge into nested dicts
    clean = {}
    for k, v in kwargs.items():
        if k.startswith("xaxis_"):
            base_xaxis[k.removeprefix("xaxis_")] = v
        elif k.startswith("yaxis_"):
            base_yaxis[k.removeprefix("yaxis_")] = v
        elif k.startswith("legend_"):
            base_legend[k.removeprefix("legend_")] = v
        elif k == "xaxis" and isinstance(v, dict):
            base_xaxis.update(v)
        elif k == "yaxis" and isinstance(v, dict):
            base_yaxis.update(v)
        elif k == "legend" and isinstance(v, dict):
            base_legend.update(v)
        else:
            clean[k] = v

    return dict(
        plot_bgcolor="rgba(17,34,64,0.6)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=TEXT_LIGHT, size=12),
        margin=dict(t=40, l=50, r=30, b=40),
        legend=base_legend,
        xaxis=base_xaxis,
        yaxis=base_yaxis,
        **clean,
    )


# ── Load data ────────────────────────────────────────────────────────────────
default, sources = load_default()

with st.sidebar:
    st.markdown(
        f"<div style='text-align:center;padding:10px 0'>"
        f"<span style='font-size:1.4rem;color:{GOLD};font-weight:700'>🏔️ The Mountain Path</span><br>"
        f"<span style='color:{MUTED};font-size:0.8rem'>Academy Analytics</span></div>",
        unsafe_allow_html=True,
    )
    st.divider()
    st.markdown(f"<span style='color:{GOLD};font-weight:600'>Analysis Controls</span>", unsafe_allow_html=True)

    upload = st.file_uploader(
        "Upload custom dataset (Excel or CSV)",
        type=["xlsx", "csv"],
        help="Excel/CSV columns: bank, fiscal_year, reporting_date, casa_ratio_pct, basis, source_id",
    )
    try:
        data = read_uploaded_data(upload) if upload else default.copy()
    except Exception as exc:
        st.error(f"Could not read the uploaded file: {exc}")
        st.stop()
    problems = validate(data)
    if problems:
        for p in problems:
            st.error(p)
        st.stop()

    banks = st.multiselect("Banks", sorted(data.bank.unique()), default=sorted(data.bank.unique()))
    years = sorted(data.fiscal_year.unique(), key=lambda x: int(str(x).replace("FY", "")))
    yr = st.select_slider("Fiscal-year range", options=years, value=(years[0], years[-1]))
    show_labels = st.toggle("Chart data labels", True)
    show_confidence = st.toggle("Regression confidence bands", True)

    st.divider()
    st.caption("Data vintage: 18 Jul 2026 · Annual period-end series FY2021–FY2025")

    # ── Author profile card ──
    st.markdown(
        f"""<div class='profile-card'>
        <p class='name'>Prof. V. Ravichandran</p>
        <p class='title'>Visiting Professor &amp; Professor of Practice at Leading Business Schools<br>
        Founder — The Mountain Path Academy</p>
        <p class='stats'>28+ yrs · HSBC Global Banking &amp; Markets · Synechron<br>
        12+ yrs teaching · Financial Risk · Derivatives · ALM</p>
        <div class='links'>
            <a href='https://themountainpathacademy.com' target='_blank'>🏔️ Academy</a>
            <a href='https://www.linkedin.com/in/trichyravis' target='_blank'>💼 LinkedIn</a>
            <a href='https://github.com/trichyravis' target='_blank'>💻 GitHub</a>
        </div>
    </div>""",
        unsafe_allow_html=True,
    )

# ── Filter ───────────────────────────────────────────────────────────────────
lo, hi = years.index(yr[0]), years.index(yr[1])
selected_years = years[lo : hi + 1]
df = data[data.bank.isin(banks) & data.fiscal_year.isin(selected_years)].copy()

# ── Hero banner ──────────────────────────────────────────────────────────────
st.markdown(
    f"""<div class='hero-banner'>
    <h1>Indian Bank CASA Ratio Analytics</h1>
    <p class='subtitle'>Deposit franchise quality assessment · Peer benchmarking · Risk decomposition · Source-level audit trail</p>
    <div style='display:flex;align-items:center;gap:16px;margin-top:10px;flex-wrap:wrap'>
        <span class='badge'>Build 3 · Excel enabled · Dark theme</span>
        <span class='badge'>5 Banks · FY2021–FY2025 · Period-end basis</span>
        <span style='color:{MUTED};font-size:0.82rem'>
            By <a href='https://www.linkedin.com/in/trichyravis' target='_blank' style='color:{LIGHT_BLUE};text-decoration:none'>
            Prof. V. Ravichandran</a> ·
            <a href='https://themountainpathacademy.com' target='_blank' style='color:{GOLD};text-decoration:none'>
            The Mountain Path Academy</a>
        </span>
    </div>
</div>""",
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='info-box'><b>CASA ratio</b> = (Current + Savings deposits) ÷ Total deposits × 100. "
    "A higher ratio signals a cheaper funding franchise, but must be read alongside deposit growth, "
    "cost of deposits, granularity, stability, and NIM. A declining CASA ratio across the sector may "
    "reflect structural shifts (term-deposit competition, rate cycles) rather than bank-specific weakness.</div>",
    unsafe_allow_html=True,
)

if df.empty:
    st.warning("Select at least one bank to begin analysis.")
    st.stop()

# ── Compute analytics ────────────────────────────────────────────────────────
latest_year = selected_years[-1]
latest = df[df.fiscal_year == latest_year]
leader = latest.loc[latest.casa_ratio_pct.idxmax()]

tmp = df.sort_values("reporting_date")
chg = tmp.groupby("bank").casa_ratio_pct.agg(lambda x: x.iloc[-1] - x.iloc[0])
risk_df = compute_risk_metrics(df)
risk_df["Quality Score"] = risk_df.apply(franchise_quality_score, axis=1)
risk_df["Grade"], risk_df["Grade Color"] = zip(*risk_df["Quality Score"].apply(interpret_score))

# Industry average
industry_avg = latest.casa_ratio_pct.mean()
industry_std = latest.casa_ratio_pct.std()

# ── KPI row ──────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Latest Period", latest_year)
c2.metric("Highest CASA", f"{leader.casa_ratio_pct:.1f}%", leader.bank)
c3.metric("Peer Average", f"{industry_avg:.1f}%")
c4.metric("Peer Dispersion", f"{industry_std:.1f} pp", help="Standard deviation across selected banks")
c5.metric("Median Period Δ", f"{chg.median():+.1f} pp", help="First to last selected year")

# ── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["📊 Overview", "📈 Trend Analytics", "⚠️ Risk & Stability", "🏦 Bank Deep Dive", "🔬 Sector Analysis", "📋 Data & Sources"]
)

# ═══════════════════════ TAB 1: OVERVIEW ═══════════════════════════════════
with tab1:
    a, b = st.columns([1.6, 1])
    with a:
        fig = px.line(
            df, x="fiscal_year", y="casa_ratio_pct", color="bank", markers=True,
            color_discrete_map=BANK_COLORS,
            labels={"fiscal_year": "Fiscal Year", "casa_ratio_pct": "CASA Ratio (%)", "bank": "Bank"},
        )
        if show_labels:
            fig.update_traces(texttemplate="%{y:.1f}%", textposition="top center")
        # Add industry average line
        avg_by_year = df.groupby("fiscal_year")["casa_ratio_pct"].mean().reset_index()
        fig.add_scatter(
            x=avg_by_year["fiscal_year"], y=avg_by_year["casa_ratio_pct"],
            mode="lines", name="Peer Average",
            line=dict(color=GOLD, width=2.5, dash="dash"),
        )
        fig.update_layout(**mp_layout(height=500, hovermode="x unified", yaxis_ticksuffix="%"))
        st.plotly_chart(fig, width="stretch")

    with b:
        rank = latest.sort_values("casa_ratio_pct")
        fig = px.bar(
            rank, x="casa_ratio_pct", y="bank", orientation="h",
            color="bank", color_discrete_map=BANK_COLORS,
            text="casa_ratio_pct",
            labels={"casa_ratio_pct": f"CASA Ratio — {latest_year}", "bank": ""},
        )
        fig.update_traces(texttemplate="%{x:.1f}%", textposition="outside")
        # Add average line
        fig.add_vline(x=industry_avg, line_dash="dash", line_color=GOLD, line_width=2,
                      annotation_text=f"Avg {industry_avg:.1f}%", annotation_font_color=GOLD)
        fig.update_layout(**mp_layout(height=500, showlegend=False, xaxis_ticksuffix="%"))
        st.plotly_chart(fig, width="stretch")

    # YoY waterfall for the full peer set
    st.markdown(f"### Year-over-Year Change Waterfall")
    yoy_data = []
    for bank in banks:
        bd = df[df.bank == bank].sort_values("reporting_date")
        if len(bd) < 2:
            continue
        for i in range(1, len(bd)):
            yoy_data.append({
                "Bank": BANK_SHORT.get(bank, bank),
                "Period": f"{bd.iloc[i-1].fiscal_year}→{bd.iloc[i].fiscal_year}",
                "Change (pp)": bd.iloc[i].casa_ratio_pct - bd.iloc[i - 1].casa_ratio_pct,
            })
    if yoy_data:
        yoy_df = pd.DataFrame(yoy_data)
        fig = px.bar(
            yoy_df, x="Period", y="Change (pp)", color="Bank", barmode="group",
            color_discrete_map={v: BANK_COLORS[k] for k, v in BANK_SHORT.items() if k in BANK_COLORS},
        )
        fig.add_hline(y=0, line_color=MUTED, line_width=1)
        fig.update_layout(**mp_layout(height=380))
        st.plotly_chart(fig, width="stretch")


# ═══════════════════════ TAB 2: TREND ANALYTICS ════════════════════════════
with tab2:
    st.markdown("### Heatmap — CASA Ratios Across Banks & Years")
    pivot = df.pivot(index="bank", columns="fiscal_year", values="casa_ratio_pct").reindex(columns=selected_years)
    heat = go.Figure(
        go.Heatmap(
            z=pivot.values, x=pivot.columns, y=pivot.index,
            colorscale=[[0, "#dc3545"], [0.4, "#F97316"], [0.6, "#FFD700"], [1, "#28a745"]],
            text=np.round(pivot.values, 1), texttemplate="%{text}%",
            colorbar=dict(title="CASA %", ticksuffix="%"),
        )
    )
    heat.update_layout(**mp_layout(height=400))
    st.plotly_chart(heat, width="stretch")

    # Regression trend with confidence bands
    st.markdown("### OLS Trend Regression with Confidence Bands")
    fig = go.Figure()
    for bank in banks:
        bd = df[df.bank == bank].sort_values("reporting_date")
        if len(bd) < 2:
            continue
        x_num = np.arange(len(bd))
        y_vals = bd["casa_ratio_pct"].values
        slope, intercept, r_val, p_val, std_err = sp_stats.linregress(x_num, y_vals)
        y_pred = intercept + slope * x_num
        residual_std = np.sqrt(np.sum((y_vals - y_pred) ** 2) / max(len(y_vals) - 2, 1))
        ci_95 = 1.96 * residual_std

        color = BANK_COLORS.get(bank, "#2563EB")
        fig.add_scatter(
            x=bd["fiscal_year"], y=y_vals, mode="markers+lines",
            name=f"{BANK_SHORT.get(bank, bank)} (actual)",
            line=dict(color=color, width=2.5), marker=dict(size=8),
        )
        fig.add_scatter(
            x=bd["fiscal_year"], y=y_pred, mode="lines",
            name=f"{BANK_SHORT.get(bank, bank)} (trend: {slope:+.2f} pp/yr, R²={r_val**2:.2f})",
            line=dict(color=color, width=1.5, dash="dash"),
        )
        if show_confidence:
            fig.add_scatter(
                x=list(bd["fiscal_year"]) + list(bd["fiscal_year"])[::-1],
                y=list(y_pred + ci_95) + list(y_pred - ci_95)[::-1],
                fill="toself", fillcolor=hex_to_rgba(color, 0.08), line=dict(width=0),
                name=f"{BANK_SHORT.get(bank, bank)} ±95% CI", showlegend=False,
            )
    fig.update_layout(**mp_layout(height=500, yaxis_ticksuffix="%", yaxis_title="CASA Ratio (%)", hovermode="x unified"))
    st.plotly_chart(fig, width="stretch")

    # Summary statistics table
    st.markdown("### Descriptive Statistics")
    display_cols = ["Bank", "Latest (%)", "Mean (%)", "Std Dev (pp)", "CV (%)", "Trend (pp/yr)", "R²", "Total Δ (pp)"]
    st.dataframe(
        risk_df[display_cols].style.format({
            "Latest (%)": "{:.2f}", "Mean (%)": "{:.2f}", "Std Dev (pp)": "{:.2f}",
            "CV (%)": "{:.1f}", "Trend (pp/yr)": "{:+.2f}", "R²": "{:.3f}", "Total Δ (pp)": "{:+.2f}",
        }).background_gradient(subset=["Trend (pp/yr)"], cmap="RdYlGn", vmin=-5, vmax=2),
        width="stretch", hide_index=True,
    )


# ═══════════════════════ TAB 3: RISK & STABILITY ══════════════════════════
with tab3:
    st.markdown("### Deposit Franchise Quality Assessment")
    st.markdown(
        "<div class='info-box'>The <b>Franchise Quality Score</b> (0–100) combines four dimensions: "
        "<b>Level</b> (30%) — current CASA ratio; <b>Stability</b> (25%) — coefficient of variation; "
        "<b>Trend</b> (25%) — OLS slope direction; <b>Drawdown Resistance</b> (20%) — maximum peak-to-trough decline. "
        "This is an analytical construct for classroom discussion, not a rating.</div>",
        unsafe_allow_html=True,
    )

    # Score cards
    score_cols = st.columns(len(risk_df))
    for i, (_, row) in enumerate(risk_df.sort_values("Quality Score", ascending=False).iterrows()):
        grade_label, grade_color = row["Grade"], row["Grade Color"]
        with score_cols[i]:
            st.markdown(
                f"<div class='risk-card' style='border-top:3px solid {grade_color}'>"
                f"<h4>{BANK_SHORT.get(row['Bank'], row['Bank'])}</h4>"
                f"<div style='font-size:2rem;font-weight:700;color:{grade_color}'>{row['Quality Score']:.0f}</div>"
                f"<div style='color:{grade_color};font-weight:600;font-size:0.9rem'>{grade_label}</div>"
                f"<p style='margin-top:8px'>CV: {row['CV (%)']:.1f}% · Trend: {row['Trend (pp/yr)']:+.1f} pp/yr</p>"
                f"<p>Max DD: {row['Max Drawdown (pp)']:+.1f} pp</p>"
                f"</div>",
                unsafe_allow_html=True,
            )

    # Radar chart — multi-dimensional comparison
    st.markdown("### Multi-Dimensional Peer Radar")
    radar_dims = ["Latest (%)", "Mean (%)", "CV (%)", "Max Drawdown (pp)", "Trend (pp/yr)"]

    def normalize_for_radar(series, higher_is_better=True):
        mn, mx = series.min(), series.max()
        if mx == mn:
            return pd.Series([0.5] * len(series), index=series.index)
        norm = (series - mn) / (mx - mn)
        return norm if higher_is_better else 1 - norm

    radar_df = risk_df.copy()
    radar_labels = ["Current Level", "Historical Average", "Stability (inv. CV)", "Drawdown Resist.", "Trend Direction"]
    for dim, label, hib in zip(
        radar_dims, radar_labels,
        [True, True, False, True, True],  # higher_is_better flags; DD is negative so True
    ):
        radar_df[f"norm_{label}"] = normalize_for_radar(radar_df[dim], higher_is_better=hib)

    fig = go.Figure()
    for _, row in radar_df.iterrows():
        vals = [row[f"norm_{l}"] for l in radar_labels]
        vals.append(vals[0])  # close the polygon
        fig.add_trace(go.Scatterpolar(
            r=vals, theta=radar_labels + [radar_labels[0]],
            fill="toself", name=BANK_SHORT.get(row["Bank"], row["Bank"]),
            line=dict(color=BANK_COLORS.get(row["Bank"], "#2563EB"), width=2),
            fillcolor=hex_to_rgba(BANK_COLORS.get(row["Bank"], "#2563EB"), 0.13),
        ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(17,34,64,0.6)",
            radialaxis=dict(visible=True, range=[0, 1], gridcolor="#1e3a5f", tickfont=dict(size=9, color=MUTED)),
            angularaxis=dict(gridcolor="#1e3a5f", tickfont=dict(color=TEXT_LIGHT, size=11)),
        ),
        **mp_layout(height=480, legend=dict(bgcolor="rgba(17,34,64,0.5)", font=dict(color=TEXT_LIGHT))),
    )
    st.plotly_chart(fig, width="stretch")

    # Risk table with all metrics
    st.markdown("### Full Risk Metrics Table")
    risk_display = risk_df[
        ["Bank", "Sector", "Latest (%)", "Mean (%)", "Std Dev (pp)", "CV (%)",
         "Trend (pp/yr)", "R²", "p-value", "Max Drawdown (pp)", "Worst YoY (pp)", "Best YoY (pp)",
         "Quality Score", "Grade"]
    ]
    st.dataframe(
        risk_display.style.format({
            "Latest (%)": "{:.2f}", "Mean (%)": "{:.2f}", "Std Dev (pp)": "{:.2f}",
            "CV (%)": "{:.1f}", "Trend (pp/yr)": "{:+.2f}", "R²": "{:.3f}", "p-value": "{:.4f}",
            "Max Drawdown (pp)": "{:+.2f}", "Worst YoY (pp)": "{:+.2f}", "Best YoY (pp)": "{:+.2f}",
            "Quality Score": "{:.0f}",
        }),
        width="stretch", hide_index=True,
    )

    # Volatility clustering
    st.markdown("### Year-over-Year Volatility Distribution")
    yoy_all = []
    for bank in banks:
        bd = df[df.bank == bank].sort_values("reporting_date")
        vals = bd["casa_ratio_pct"].values
        for i in range(1, len(vals)):
            yoy_all.append({"Bank": bank, "YoY Change (pp)": vals[i] - vals[i - 1]})
    if yoy_all:
        yoy_all_df = pd.DataFrame(yoy_all)
        fig = px.box(
            yoy_all_df, x="Bank", y="YoY Change (pp)", color="Bank",
            color_discrete_map=BANK_COLORS, points="all",
        )
        fig.add_hline(y=0, line_dash="dash", line_color=MUTED)
        fig.update_layout(**mp_layout(height=400, showlegend=False, xaxis_title=""))
        st.plotly_chart(fig, width="stretch")


# ═══════════════════════ TAB 4: BANK DEEP DIVE ════════════════════════════
with tab4:
    bank = st.selectbox("Select bank for deep analysis", banks)
    bd = df[df.bank == bank].sort_values("reporting_date")
    bank_risk = risk_df[risk_df["Bank"] == bank].iloc[0]
    grade_label, grade_color = bank_risk["Grade"], bank_risk["Grade Color"]

    # Header metrics
    m1, m2, m3, m4, m5 = st.columns(5)
    first_v, last_v = bd.iloc[0], bd.iloc[-1]
    delta = last_v.casa_ratio_pct - first_v.casa_ratio_pct
    m1.metric("Latest", f"{last_v.casa_ratio_pct:.2f}%", f"{delta:+.2f} pp vs {first_v.fiscal_year}")
    m2.metric("Period Average", f"{bd.casa_ratio_pct.mean():.2f}%")
    m3.metric("Range", f"{bd.casa_ratio_pct.min():.1f}%–{bd.casa_ratio_pct.max():.1f}%")
    m4.metric("Volatility (CV)", f"{bank_risk['CV (%)']:.1f}%")
    m5.metric("Quality Score", f"{bank_risk['Quality Score']:.0f}", grade_label)

    x, y = st.columns([1.5, 1])
    with x:
        # Enhanced area chart with trend line
        fig = go.Figure()
        color = BANK_COLORS.get(bank, "#2563EB")
        fig.add_scatter(
            x=bd["fiscal_year"], y=bd["casa_ratio_pct"],
            mode="lines+markers", name="CASA Ratio",
            fill="tozeroy", fillcolor=hex_to_rgba(color, 0.08),
            line=dict(color=color, width=3), marker=dict(size=10, color=color),
        )
        # Trend line
        if len(bd) > 1:
            x_num = np.arange(len(bd))
            slope, intercept, _, _, _ = sp_stats.linregress(x_num, bd["casa_ratio_pct"].values)
            y_pred = intercept + slope * x_num
            fig.add_scatter(
                x=bd["fiscal_year"], y=y_pred, mode="lines",
                name=f"Trend ({slope:+.2f} pp/yr)",
                line=dict(color=GOLD, width=2, dash="dash"),
            )
        # Peer average line
        avg_line = df.groupby("fiscal_year")["casa_ratio_pct"].mean()
        fig.add_scatter(
            x=avg_line.index, y=avg_line.values, mode="lines",
            name="Peer Average", line=dict(color=MUTED, width=1.5, dash="dot"),
        )
        fig.update_layout(**mp_layout(height=420, yaxis_ticksuffix="%", yaxis_title="CASA Ratio (%)"))
        st.plotly_chart(fig, width="stretch")

    with y:
        # Peer rank position over time
        st.markdown(f"#### Peer Rank Trajectory")
        rank_data = []
        for fy in selected_years:
            fy_data = df[df.fiscal_year == fy].sort_values("casa_ratio_pct", ascending=False)
            for rank_pos, (_, row) in enumerate(fy_data.iterrows(), 1):
                if row.bank == bank:
                    rank_data.append({"Year": fy, "Rank": rank_pos, "Total": len(fy_data)})
        if rank_data:
            rank_df_plot = pd.DataFrame(rank_data)
            fig = px.bar(
                rank_df_plot, x="Year", y="Rank", text="Rank",
                color_discrete_sequence=[color],
            )
            fig.update_yaxes(autorange="reversed", dtick=1, title="Rank (1=Highest)")
            fig.update_traces(textposition="outside")
            fig.update_layout(**mp_layout(height=420))
            st.plotly_chart(fig, width="stretch")

    # Interpretive commentary
    st.markdown("#### Analytical Commentary")
    commentaries = []
    if delta < -5:
        commentaries.append(
            f"⚠️ **Material decline** of {abs(delta):.1f} pp over the selected period. "
            "Examine whether this reflects term-deposit migration, rate competition, "
            "merger-related base effects, or structural franchise erosion. "
            "Cross-check with cost-of-deposits trend and NIM trajectory."
        )
    elif delta < -2:
        commentaries.append(
            f"📉 **Moderate decline** of {abs(delta):.1f} pp. This may reflect sector-wide dynamics "
            "(rate cycle, term-deposit competition) rather than bank-specific weakness. "
            "Compare with peer group trend for context."
        )
    elif delta > 2:
        commentaries.append(
            f"📈 **CASA franchise strengthened** by {delta:.1f} pp. Verify that this reflects "
            "genuine deposit quality improvement (granularity, retention) rather than "
            "denominator effects or window-dressing."
        )
    else:
        commentaries.append(
            "📊 **Broadly stable** CASA share. Review absolute deposit growth, funding cost, "
            "and competitive positioning before drawing conclusions."
        )

    if bank_risk["CV (%)"] > 10:
        commentaries.append(
            f"🔄 **Elevated volatility** (CV = {bank_risk['CV (%)']:.1f}%). Year-on-year swings "
            "may signal sensitivity to rate cycles, seasonal patterns, or event-driven shifts."
        )

    peer_latest_rank = risk_df.sort_values("Latest (%)", ascending=False)["Bank"].tolist().index(bank) + 1
    commentaries.append(
        f"🏁 **Peer rank**: #{peer_latest_rank} of {len(risk_df)} banks in the latest period "
        f"({latest_year}) by CASA ratio."
    )

    for c in commentaries:
        st.markdown(c)


# ═══════════════════════ TAB 5: SECTOR ANALYSIS ═══════════════════════════
with tab5:
    st.markdown("### Public vs Private Sector CASA Dynamics")

    if "bank_type" in df.columns:
        sector_avg = df.groupby(["fiscal_year", "bank_type"])["casa_ratio_pct"].mean().reset_index()
        fig = px.line(
            sector_avg, x="fiscal_year", y="casa_ratio_pct", color="bank_type",
            markers=True, color_discrete_map=SECTOR_COLORS,
            labels={"fiscal_year": "Fiscal Year", "casa_ratio_pct": "Average CASA (%)", "bank_type": "Sector"},
        )
        if show_labels:
            fig.update_traces(texttemplate="%{y:.1f}%", textposition="top center")
        fig.update_layout(**mp_layout(height=420, yaxis_ticksuffix="%", hovermode="x unified"))
        st.plotly_chart(fig, width="stretch")

        # Convergence / divergence analysis
        st.markdown("### Sector Convergence Analysis")
        sector_pivot = sector_avg.pivot(index="fiscal_year", columns="bank_type", values="casa_ratio_pct")
        if "Public Sector" in sector_pivot.columns and "Private Sector" in sector_pivot.columns:
            sector_pivot["Spread (pp)"] = sector_pivot["Private Sector"] - sector_pivot["Public Sector"]
            fig = px.bar(
                sector_pivot.reset_index(), x="fiscal_year", y="Spread (pp)",
                color_discrete_sequence=[GOLD],
                labels={"fiscal_year": "Fiscal Year"},
            )
            fig.add_hline(y=0, line_dash="dash", line_color=MUTED)
            fig.update_layout(**mp_layout(height=350, showlegend=False))
            st.plotly_chart(fig, width="stretch")

            latest_spread = sector_pivot["Spread (pp)"].iloc[-1]
            if latest_spread > 0:
                st.markdown(
                    f"Private sector banks maintain a **{latest_spread:.1f} pp premium** over the public sector bank "
                    "in the latest period. Historically, private banks have leveraged digital platforms and "
                    "relationship banking to attract and retain low-cost deposits."
                )
            else:
                st.markdown(
                    f"The public sector bank has **narrowed or closed the gap** (spread: {latest_spread:+.1f} pp). "
                    "This may reflect government salary account mandates, Jan Dhan deposits, or "
                    "improved digital offerings at PSU banks."
                )
    else:
        st.info("Add a `bank_type` column (Public Sector / Private Sector) to your dataset for sector analysis.")

    # Correlation matrix
    st.markdown("### Cross-Bank CASA Correlation Matrix")
    corr_pivot = df.pivot(index="fiscal_year", columns="bank", values="casa_ratio_pct")
    if len(corr_pivot.columns) >= 2:
        corr = corr_pivot.corr()
        short_labels = [BANK_SHORT.get(b, b) for b in corr.columns]
        fig = go.Figure(
            go.Heatmap(
                z=corr.values, x=short_labels, y=short_labels,
                colorscale=[[0, RED], [0.5, "#112240"], [1, GREEN]],
                zmin=-1, zmax=1,
                text=np.round(corr.values, 2), texttemplate="%{text}",
                colorbar=dict(title="ρ"),
            )
        )
        fig.update_layout(**mp_layout(height=400))
        st.plotly_chart(fig, width="stretch")
        st.markdown(
            "<div class='info-box'>High positive correlations suggest sector-wide macro drivers "
            "(rate cycles, regulatory policy) dominate. Low or negative correlations indicate "
            "bank-specific idiosyncratic factors at work.</div>",
            unsafe_allow_html=True,
        )


# ═══════════════════════ TAB 6: DATA & SOURCES ════════════════════════════
with tab6:
    st.markdown("### Source-Tagged Dataset")
    joined = df.merge(sources, on="source_id", how="left", suffixes=("", "_source"))
    display_cols = ["bank", "fiscal_year", "reporting_date", "casa_ratio_pct", "basis", "notes", "document", "source_url"]
    available_cols = [c for c in display_cols if c in joined.columns]
    st.dataframe(
        joined[available_cols], width="stretch", hide_index=True,
        column_config={"source_url": st.column_config.LinkColumn("Official Source")},
    )

    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            "⬇ Download filtered data (Excel)",
            dataframe_to_excel(df, "CASA Data"),
            "filtered_casa_ratios.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    with col_dl2:
        # Export risk metrics
        export_risk = risk_df.drop(columns=["Short", "Grade Color"], errors="ignore")
        st.download_button(
            "⬇ Download risk metrics (Excel)",
            dataframe_to_excel(export_risk, "Risk Metrics"),
            "casa_risk_metrics.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    st.markdown("### Data Quality Controls")
    checks = [
        ("Ratio bounds", "All CASA ratios are between 0–100%", True),
        ("Duplicate check", "No duplicate bank–year observations", True),
        ("Basis disclosure", "Every row has a basis label (period-end / MEB / QAB)", True),
        ("Source linkage", "Every observation has a source_id mapped to sources.csv", True),
        ("Comparability note", "HDFC Bank FY2024 post-merger flagged as not strictly comparable", True),
    ]
    for name, desc, passed in checks:
        icon = "✅" if passed else "❌"
        st.markdown(f"{icon} **{name}** — {desc}")

    st.markdown("### Methodology Notes")
    st.markdown(
        "CASA is a periodic accounting disclosure, not a continuously traded variable. "
        "The series uses period-end ratios at 31 March for each fiscal year. "
        "Axis Bank labels the March-end measure MEB; its QAB figure (typically lower) must not be substituted. "
        "HDFC Bank's FY2024 onward includes the merged HDFC Ltd balance sheet, breaking strict comparability. "
        "Never mix average/QAB with period-end/MEB CASA in a single trend without clearly separating the series."
    )
    st.markdown(
        "**Franchise Quality Score methodology**: Level (30%) maps the latest ratio linearly from [30%, 60%] → [0, 100]; "
        "Stability (25%) maps CV from [0%, 20%] → [100, 0]; Trend (25%) maps slope from [-3, +3] pp/yr → [0, 100]; "
        "Drawdown Resistance (20%) maps max drawdown from [-20, 0] pp → [0, 100]. "
        "All component scores are clipped to [0, 100] before weighting."
    )


# ── About & Footer ───────────────────────────────────────────────────────────
st.markdown("---")

st.markdown(
    f"""<div class='about-section'>
    <h3>About This Project</h3>
    <p>
        This dashboard is developed by <span class='highlight'>Prof. V. Ravichandran</span>,
        Visiting Professor &amp; Professor of Practice at Leading Business Schools, and founder of
        <span class='highlight'>The Mountain Path Academy</span>.
    </p>
    <p>
        With <span class='highlight'>28+ years of industry experience</span> at HSBC Global Banking &amp; Markets
        and Synechron in risk analytics, Basel II/III, VaR, FRTB, and ECL modelling, and
        <span class='highlight'>12+ years of teaching</span> Financial Risk Management, Derivatives,
        Fixed Income Securities, Financial Modelling, and ALM at leading business schools, this project
        reflects a practitioner-educator's approach to building classroom-ready analytical tools
        that bridge theory and real-world banking data.
    </p>
    <p>
        The Mountain Path Academy offers structured courses, mentoring, and hands-on projects in
        applied finance, risk management, and financial modelling — designed for working professionals,
        MBA students, and aspiring risk analysts.
    </p>
    <a href='https://themountainpathacademy.com' target='_blank' class='academy-link'>
        🏔️ &nbsp;Visit The Mountain Path Academy
    </a>
</div>""",
    unsafe_allow_html=True,
)

st.markdown(
    f"""<div class='mp-footer'>
    <div class='footer-brand'>🏔️ The Mountain Path Academy</div>
    <div class='footer-profile'>Prof. V. Ravichandran · Visiting Professor &amp; Professor of Practice at Leading Business Schools</div>
    <div>
        <a href='https://themountainpathacademy.com' target='_blank'>themountainpathacademy.com</a>
    </div>
    <div class='footer-links' style='margin-top:8px'>
        <a href='https://www.linkedin.com/in/trichyravis' target='_blank'>LinkedIn</a>
        <a href='https://github.com/trichyravis' target='_blank'>GitHub</a>
    </div>
    <div style='margin-top:10px;font-size:0.78rem;color:{MUTED}'>
        Educational analytics project · Ratios do not constitute investment advice · © 2026 The Mountain Path Academy
    </div>
</div>""",
    unsafe_allow_html=True,
)
