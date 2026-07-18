from pathlib import Path
import pandas as pd

root=Path(__file__).parent
d=pd.read_csv(root/"data/casa_ratios.csv")
s=pd.read_csv(root/"data/sources.csv")
required={"bank","fiscal_year","reporting_date","casa_ratio_pct","basis","source_id"}
assert required.issubset(d.columns), required-set(d.columns)
assert d.casa_ratio_pct.between(0,100).all(), "Ratio outside 0–100"
assert not d.duplicated(["bank","fiscal_year"]).any(), "Duplicate bank-year"
assert set(d.source_id).issubset(set(s.source_id)), "Missing source metadata"
assert d.groupby("bank").size().eq(5).all(), "Each bank must have five annual observations"
print(f"Validated {len(d)} observations, {d.bank.nunique()} banks and {d.fiscal_year.nunique()} years.")
