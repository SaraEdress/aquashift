"""AquaShift: transparent scheduling prototype, not a trained AI model."""
import streamlit as st
import pandas as pd

def recommend(slots, duration, deadline, water_cap, energy_cap):
    eligible = [s for s in slots if s["start"] + duration <= deadline
                and s["water"] <= water_cap and s["energy"] <= energy_cap
                and s["safe"]]
    return min(eligible, key=lambda s: (s["water"], s["energy"])) if eligible else None

def main():
    st.set_page_config(page_title="AquaShift", page_icon="💧", layout="wide")
    st.title("💧 AquaShift")
    st.subheader("Water-aware computing. Better neighbours.")
    st.warning("RULE-BASED PROTOTYPE • Illustrative data • No live controls or trained AI model")
    st.write("Compare operating windows for one flexible batch job. Essential services stay running.")
    scenario = st.sidebar.selectbox("Scenario", ["Hot day / water restrictions", "Normal day"])
    duration = st.sidebar.slider("Job duration (hours)", 1, 6, 2)
    deadline = st.sidebar.slider("Completion deadline (hour today)", 16, 24, 24)
    water_cap = st.sidebar.number_input("Operator-set job water budget (litres)", 0, 10000, 1500, 100)
    energy_cap = st.sidebar.number_input("Maximum job electricity (kWh)", 0, 10000, 1100, 50)
    hot = scenario.startswith("Hot")
    # Assumed rates for this job, not empirical cooling predictions.
    slots = [
        dict(name="Afternoon", start=14, temperature=34 if hot else 24,
             water=(1000 if hot else 500)*duration, energy=500*duration, safe=True),
        dict(name="Evening", start=20, temperature=24 if hot else 20,
             water=(600 if hot else 400)*duration, energy=525*duration, safe=True),
        dict(name="Late evening", start=22, temperature=21 if hot else 18,
             water=(500 if hot else 350)*duration, energy=550*duration, safe=True),
    ]
    st.caption("Window temperatures and resource rates are invented scenario inputs. Actual rates require facility measurements; temperature alone does not determine water use.")
    table = pd.DataFrame([{"Window":s["name"],"Start":f'{s["start"]}:00',
        "Temperature (°C)":s["temperature"],"Job water (L)":s["water"],
        "Job electricity (kWh)":s["energy"],
        "Finishes by deadline":s["start"]+duration<=deadline} for s in slots])
    st.dataframe(table, hide_index=True, use_container_width=True)
    chosen = recommend(slots, duration, deadline, water_cap, energy_cap)
    if chosen is None:
        st.error("No feasible window. Request operator review; do not override limits.")
    else:
        baseline = slots[0]
        water_delta = baseline["water"] - chosen["water"]
        energy_delta = chosen["energy"] - baseline["energy"]
        st.success(f'Recommendation: {chosen["name"]} at {chosen["start"]}:00 — pending operator approval')
        a,b,c=st.columns(3)
        a.metric("Illustrative water reduction", f"{water_delta:,} L")
        b.metric("Electricity change vs afternoon", f"{energy_delta:+,} kWh")
        c.metric("Completion time", f'{chosen["start"]+duration}:00')
        st.write("Why: meets the deadline and resource budgets, passes the assumed safety check, and uses the least water among eligible windows.")
        st.info("Default hot-day example: shift from 14:00 to 22:00. Job water falls from 2,000 L to 1,000 L, while electricity rises from 1,000 to 1,100 kWh. These are hypothetical job-level estimates, not facility savings.")
        if st.button("Approve illustrative schedule"):
            st.success("Demo approval recorded on screen only. No real computing or cooling equipment is controlled.")
    st.markdown("**Community benefit:** reduce avoidable local water pressure while keeping essential services available.")
    st.markdown("**Future AI:** predict resource demand from validated facility data; retain explicit budgets, safety constraints and operator approval.")
    st.download_button("Download scenario comparison", table.to_csv(index=False), "aquashift_scenario.csv", "text/csv")

if __name__ == "__main__":
    main()
