import requests

OPENFDA_URL = "https://api.fda.gov/drug/label.json"


def get_drug_label(drug_name: str) -> dict:
    drug = drug_name.strip().lower()

    # -------- 1️⃣ Try BRAND NAME --------
    brand_query = f'openfda.brand_name:"{drug}"'
    res = requests.get(
        OPENFDA_URL,
        params={"search": brand_query, "limit": 1},
        timeout=10
    )

    if res.status_code == 200 and res.json().get("results"):
        return res.json()["results"][0]

    # -------- 2️⃣ Try GENERIC / ACTIVE INGREDIENT --------
    ingredient_query = f'openfda.generic_name:"{drug}"'
    res = requests.get(
        OPENFDA_URL,
        params={"search": ingredient_query, "limit": 1},
        timeout=10
    )

    if res.status_code == 200 and res.json().get("results"):
        return res.json()["results"][0]

    # -------- 3️⃣ Try ACTIVE INGREDIENT CONTAINS (fallback) --------
    contains_query = f'openfda.substance_name:"{drug}"'
    res = requests.get(
        OPENFDA_URL,
        params={"search": contains_query, "limit": 1},
        timeout=10
    )

    if res.status_code == 200 and res.json().get("results"):
        return res.json()["results"][0]

    # -------- FAIL CLEANLY --------
    raise ValueError(
        f"No FDA drug label found for '{drug_name}'. "
        "Try a brand name or check spelling."
    )
