# Copilot Instructions

## Default Workflow (always)

1) Prefer existing docs/scripts before creating new code.
2) Start with READ-ONLY analysis; ask before making changes.
3) Use explicit date ranges and KPIs when analyzing data.

## Workspace Notes (Google Ads / Shopping)

If the user asks something like “analysiere meine Google Ads Shopping Anzeige/Kampagne”:

- Google Ads scripts live in `/root/projects/Google Cloud/ads`
- Start with:
  - `cd "Google Cloud" && ./venv/bin/python3 ads/check_campaign_status.py`
  - `cd "Google Cloud" && ./venv/bin/python3 ads/analyze_product_performance.py --days 30 --min-clicks 1 --min-cost 0.5 --top 10`
- Default date range: last 30 full days up to yesterday.
- If conversion value is 0, ROAS is not meaningful → evaluate via CPA / spend-without-conversions and flag tracking/value import.

