# AquaShift

Rule-based Python/Streamlit concept prototype for water-aware batch scheduling.
No trained AI model, live integration, or measured savings.

## Run locally (Windows, macOS or Linux)

Open a terminal in this extracted folder:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

On Windows, use `py` instead of `python` if needed.
Open the local URL printed in the terminal, usually http://localhost:8501.

## Two-minute demo

1. Keep the default hot-day scenario and two-hour job.
2. Compare afternoon (2,000 L / 1,000 kWh) with late evening (1,000 L / 1,100 kWh).
3. Explain that the job moves to 22:00 and finishes by midnight, with operator approval.
4. Set the electricity budget to 1,000 kWh: no window meets both budgets.
5. Explain why the tool requests review instead of silently overriding constraints.

The water budget is operator supplied; it is not a legal interpretation of local
restrictions. Production use requires translating applicable restrictions into
validated constraints, measuring resource rates, and verifying capacity and
equipment safety. The demo assumes candidate slots have capacity and are safe.
All resource values are hypothetical job-level totals; essential-service demand
and facility-wide consumption are excluded. Moving a job does not guarantee
water savings in a real cooling system.

## Devpost

Built with: Python, Streamlit, pandas, ChatGPT.
Upload AquaShift_Practical_Scenario.png as concept-demo media.
Share source through a public repository if desired; this local app has no
public hosting URL. A screenshot or recording can demonstrate it.
