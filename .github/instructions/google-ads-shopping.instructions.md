---
applyTo: "**"
---

If the user asks to analyze Google Ads Shopping / Performance Max:

1) First search existing notes/scripts in `/root/projects/Google Cloud`:
   - `Google Cloud/.milestones.json`
   - `/root/projects/.workspace-tools-index.md`
2) Run READ-ONLY analysis first:
   - `cd "Google Cloud" && ./venv/bin/python3 ads/check_campaign_status.py`
   - `cd "Google Cloud" && ./venv/bin/python3 ads/analyze_product_performance.py --days 30 --min-clicks 1 --min-cost 0.5 --top 10`
3) Default: last 30 full days up to yesterday; if conversion value is 0, ROAS is not meaningful → use CPA / spend-without-conversions and flag tracking/value import.

