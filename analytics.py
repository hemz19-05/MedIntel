import streamlit as st
from datetime import datetime

def _init():
    if "logs" not in st.session_state:
        st.session_state["logs"] = []


def log_query(drug_name: str, variant: str = None):
    _init()
    st.session_state["logs"].append({
        "drug": drug_name.strip().lower(),
        "variant": variant,
        "timestamp": datetime.now()
    })


def get_analytics():
    _init()
    logs = st.session_state["logs"]

    drug_list = [x["drug"] for x in logs]
    unique_drugs = sorted(list(set(drug_list)))

    variant_counts = {}
    for x in logs:
        v = x.get("variant")
        if v:
            variant_counts[v] = variant_counts.get(v, 0) + 1


    return {
        "total_queries": len(logs),
        "unique_drugs": len(unique_drugs),
        "drug_list": unique_drugs,
        "variant_counts": variant_counts
    }

