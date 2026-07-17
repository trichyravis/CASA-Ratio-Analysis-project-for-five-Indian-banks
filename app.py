from pathlib import Path
from datetime import datetime
import io
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Indian Bank CASA Analytics", page_icon="🏦", layout="wide")
ROOT = Path(__file__).parent

COLORS = {"State Bank of India":"#2563EB","HDFC Bank":"#DC2626","ICICI Bank":"#F97316","Axis Bank":"#A21CAF","Kotak Mahindra Bank":"#059669"}

st.markdown("""<style>
.stApp{background:#f5f7fb}.block-container{padding-top:1.4rem;max-width:1450px}
.hero{padding:28px 32px;border-radius:22px;color:white;background:linear-gradient(120deg,#071d49,#123b75 65%,#b78628);box-shadow:0 12px 32px #0b1f4033;margin-bottom:18px}
.hero h1{font-size:2.35rem;margin:0}.hero p{font-size:1.05rem;opacity:.9;margin:8px 0 0}
[data-testid="stMetric"]{background:white;border:1px solid #e2e8f0;padding:16px;border-radius:16px;box-shadow:0 5px 16px #0f172a0c}
.note{background:#fff8e7;border-left:5px solid #c9962e;padding:13px 16px;border-radius:8px;color:#3d3420}
h2,h3{color:#0b2859}.small{font-size:.86rem;color:#64748b}
</style>""", unsafe_allow_html=True)

@st.cache_data
def load_default():
    d = pd.read_csv(ROOT/"data/casa_ratios.csv", parse_dates=["reporting_date"])
    s = pd.read_csv(ROOT/"data/sources.csv")
    return d, s

def validate(d):
    issues=[]
    req={"bank","fiscal_year","reporting_date","casa_ratio_pct","basis","source_id"}
    if not req.issubset(d.columns): issues.append("Missing columns: "+", ".join(sorted(req-set(d.columns))))
    if "casa_ratio_pct" in d and ((d.casa_ratio_pct<0)|(d.casa_ratio_pct>100)).any(): issues.append("CASA ratios must be between 0 and 100.")
    if {"bank","fiscal_year"}.issubset(d) and d.duplicated(["bank","fiscal_year"]).any(): issues.append("Duplicate bank–year observations found.")
    return issues

default, sources = load_default()
with st.sidebar:
    st.markdown("## Analysis controls")
    upload=st.file_uploader("Optional validated CSV override", type="csv", help="Use the same columns as data/casa_ratios.csv")
    data=pd.read_csv(upload, parse_dates=["reporting_date"]) if upload else default.copy()
    problems=validate(data)
    if problems:
        for p in problems: st.error(p)
        st.stop()
    banks=st.multiselect("Banks", sorted(data.bank.unique()), default=sorted(data.bank.unique()))
    years=sorted(data.fiscal_year.unique(), key=lambda x:int(str(x).replace("FY","")))
    yr=st.select_slider("Fiscal-year range", options=years, value=(years[0],years[-1]))
    show_labels=st.toggle("Show chart labels", True)
    st.divider()
    st.caption("Data vintage: 18 July 2026. Annual series shown through FY2025 for consistent five-year audited comparison.")

lo,hi=years.index(yr[0]),years.index(yr[1])
selected_years=years[lo:hi+1]
df=data[data.bank.isin(banks)&data.fiscal_year.isin(selected_years)].copy()

st.markdown("""<div class='hero'><h1>Indian Bank CASA Ratio Analytics</h1><p>Five-year funding-franchise comparison • period-end ratios • source-level audit trail</p></div>""",unsafe_allow_html=True)
st.markdown("<div class='note'><b>CASA ratio</b> = (Current account deposits + Savings account deposits) ÷ Total deposits × 100. A higher ratio generally indicates a larger low-cost deposit franchise, but it must be interpreted with deposit growth, cost of deposits, stability and NIM.</div>",unsafe_allow_html=True)

if df.empty: st.warning("Choose at least one bank."); st.stop()
latest_year=selected_years[-1]
latest=df[df.fiscal_year==latest_year]
leader=latest.loc[latest.casa_ratio_pct.idxmax()]
tmp=df.sort_values("reporting_date")
chg=tmp.groupby("bank").casa_ratio_pct.agg(lambda x:x.iloc[-1]-x.iloc[0])
c1,c2,c3,c4=st.columns(4)
c1.metric("Latest comparison", latest_year)
c2.metric("Highest CASA", f"{leader.casa_ratio_pct:.1f}%", leader.bank)
c3.metric("Selected-bank average", f"{latest.casa_ratio_pct.mean():.1f}%")
c4.metric("Median 5Y change", f"{chg.median():+.1f} pp", help="Percentage points, first to last selected year")

tab1,tab2,tab3,tab4=st.tabs(["Overview","Trend analytics","Bank deep dive","Data & sources"])
with tab1:
    a,b=st.columns([1.65,1])
    with a:
        fig=px.line(df,x="fiscal_year",y="casa_ratio_pct",color="bank",markers=True,color_discrete_map=COLORS,labels={"fiscal_year":"Fiscal year","casa_ratio_pct":"CASA ratio (%)","bank":"Bank"})
        if show_labels: fig.update_traces(texttemplate="%{y:.1f}%",textposition="top center")
        fig.update_layout(height=490,hovermode="x unified",legend_title=None,margin=dict(t=35),plot_bgcolor="white",yaxis_ticksuffix="%")
        st.plotly_chart(fig,use_container_width=True)
    with b:
        rank=latest.sort_values("casa_ratio_pct")
        fig=px.bar(rank,x="casa_ratio_pct",y="bank",orientation="h",color="bank",color_discrete_map=COLORS,text="casa_ratio_pct",labels={"casa_ratio_pct":f"CASA ratio — {latest_year}","bank":""})
        fig.update_traces(texttemplate="%{x:.1f}%",textposition="outside")
        fig.update_layout(height=490,showlegend=False,plot_bgcolor="white",xaxis_ticksuffix="%",margin=dict(t=35))
        st.plotly_chart(fig,use_container_width=True)
with tab2:
    pivot=df.pivot(index="bank",columns="fiscal_year",values="casa_ratio_pct").reindex(columns=selected_years)
    heat=go.Figure(go.Heatmap(z=pivot.values,x=pivot.columns,y=pivot.index,colorscale=[[0,"#fee2e2"],[.5,"#fef3c7"],[1,"#d1fae5"]],text=np.round(pivot.values,1),texttemplate="%{text}%",colorbar_title="CASA %"))
    heat.update_layout(height=420,margin=dict(t=30,l=20,r=20,b=20))
    st.plotly_chart(heat,use_container_width=True)
    stats=df.groupby("bank").casa_ratio_pct.agg(["mean","min","max","std"]).reset_index()
    stats["change_pp"]=stats.bank.map(chg); stats["trend_pp_per_year"]=df.sort_values("reporting_date").groupby("bank").casa_ratio_pct.apply(lambda s:np.polyfit(range(len(s)),s,1)[0] if len(s)>1 else np.nan).values
    st.dataframe(stats.rename(columns={"bank":"Bank","mean":"Average %","min":"Minimum %","max":"Maximum %","std":"Volatility (SD)","change_pp":"Total change (pp)","trend_pp_per_year":"Trend (pp/year)"}).style.format(precision=2),use_container_width=True,hide_index=True)
with tab3:
    bank=st.selectbox("Choose a bank",banks)
    bd=df[df.bank==bank].sort_values("reporting_date")
    x,y=st.columns([1.5,1])
    with x:
        fig=px.area(bd,x="fiscal_year",y="casa_ratio_pct",markers=True,color_discrete_sequence=[COLORS.get(bank,"#2563EB")])
        fig.update_traces(line_width=4,fillcolor="rgba(37,99,235,.12)")
        fig.update_layout(height=400,plot_bgcolor="white",yaxis_ticksuffix="%",xaxis_title="",yaxis_title="CASA ratio")
        st.plotly_chart(fig,use_container_width=True)
    with y:
        first,last=bd.iloc[0],bd.iloc[-1]; delta=last.casa_ratio_pct-first.casa_ratio_pct
        st.metric("Latest",f"{last.casa_ratio_pct:.2f}%",f"{delta:+.2f} pp vs {first.fiscal_year}")
        st.metric("Five-year average",f"{bd.casa_ratio_pct.mean():.2f}%")
        st.metric("Range",f"{bd.casa_ratio_pct.min():.1f}% – {bd.casa_ratio_pct.max():.1f}%")
        if delta < -5: st.warning("Material decline in low-cost deposit share. Examine deposit repricing, term-deposit growth, NIM and merger/comparability effects.")
        elif delta > 2: st.success("CASA franchise strengthened over the selected period; verify that deposit growth and retention quality also improved.")
        else: st.info("CASA share was comparatively stable. Review absolute deposit growth and funding cost before concluding.")
with tab4:
    joined=df.merge(sources,on="source_id",how="left",suffixes=("","_source"))
    st.dataframe(joined[["bank","fiscal_year","reporting_date","casa_ratio_pct","basis","notes","document","source_url"]],use_container_width=True,hide_index=True,column_config={"source_url":st.column_config.LinkColumn("Official source")})
    st.download_button("Download filtered data",df.to_csv(index=False).encode(),"filtered_casa_ratios.csv","text/csv")
    st.markdown("### Quality controls")
    st.write("✓ Ratio bounds checked  •  ✓ Duplicate bank-year check  •  ✓ Basis disclosed  •  ✓ Source ID on every row")
    st.caption("Important: CASA is a periodic accounting disclosure, not a tick-by-tick market variable. The latest reliable value is the latest bank-published annual or quarterly disclosure. This project avoids silently scraping PDF tables at runtime because layout changes can corrupt financial data.")

st.divider()
st.caption("Educational analytics project • The Mountain Path Academy • Ratios do not by themselves constitute an investment recommendation")

