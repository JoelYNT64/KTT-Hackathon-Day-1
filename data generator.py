"""
Synthetic NISR-style Data Generator
====================================
For: AIMS KTT Hackathon · S2.T1.2 · Stunting Risk Heatmap Dashboard

Generates:
  - households.csv        (2,500 rows)
  - gold_stunting_flag.csv (300 labelled households, 50/50 positive/negative)
  - districts.geojson     (simplified polygons for 5 Rwandan districts)

"""

import numpy as np
import pandas as pd
import json
import random
from pathlib import Path

SEED = 42
np.random.seed(SEED)
random.seed(SEED)

OUTPUT_DIR = Path(".")

# 1. Districts
#5 districts in and around Kigali

DISTRICTS = {
    "Nyarugenge": {
        "stunting_baseline": 0.14,  # urban, lower
        "urban_ratio": 0.84,
        "sectors": ["Gitega", "Kanyinya", "Kigali", "Kimisagara", "Mageragere", "Muhima", "Nyakabanda", "Nyamirambo", "Nyarugenge", "Rwezamenyo"],
    },
    "Gasabo": {
        "stunting_baseline": 0.16,
        "urban_ratio": 0.71,
        "sectors": ["Bumbogo", "Gatsata", "Gikomero", "Gisozi", "Jabana", "Jali", "Kacyiru", "Kimihurura", "Kimironko", "Kinyinya", 
                    "Ndera", "Nduba", "Remera", "Rusororo", "Rutunga"],
    },
    "Kicukiro": {
        "stunting_baseline": 0.18,
        "urban_ratio": 0.99,
    "sectors": ["Kicukiro", "Kagarama", "Niboye", "Gatenga", "Gikondo", "Gahanga", "Kanombe", "Nyarugunga", "Kigarama", "Masaka"],
    },
    "Bugesera": {
        "stunting_baseline": 0.28,  # rural, higher
        "urban_ratio": 0.40,
        "sectors": ["Gashora", "Juru", "Kamabuye", "Ntarama", "Mareba", "Mayange", "Musenyi", "Mwogo", "Ngeruka", "Nyamata", "Nyarugenge", "Rilima", 
                    "Ruhuha", "Rweru", "Shyara"],
    },
    "Gicumbi": {
        "stunting_baseline": 0.32,  
        "urban_ratio": 0.06,
        "sectors": ["Bukure", "Bwisige", "Byumba", "Cyumba", "Giti", "Kaniga", "Manyagiro", "Miyove", "Kageyo", "Mukarange", "Muko", "Mutete", "Nyamiyaga", 
                    "Nyankenke II", "Rubaya", "Rukomo", "Rushaki", "Rutare", "Ruvune", "Rwamiko", "Shangasha"],
    },
}

# ─── 2. CATEGORICAL ENCODINGS ─────────────────────────────────────────────────
WATER_SOURCES = ["piped_indoor", "piped_yard", "protected_spring", "unprotected_spring", "river_lake"]
WATER_RISK    = {"piped_indoor": 0.0, "piped_yard": 0.1, "protected_spring": 0.25,
                 "unprotected_spring": 0.55, "river_lake": 0.9}

SANITATION_TIERS = ["flush_toilet", "improved_latrine", "unimproved_latrine", "open_defecation"]
SANITATION_RISK  = {"flush_toilet": 0.0, "improved_latrine": 0.2,
                    "unimproved_latrine": 0.6, "open_defecation": 1.0}

INCOME_BANDS = ["Q1_lowest", "Q2", "Q3", "Q4", "Q5_highest"]
INCOME_RISK  = {"Q1_lowest": 1.0, "Q2": 0.75, "Q3": 0.5, "Q4": 0.25, "Q5_highest": 0.0}

# ─── 3. GENERATE HOUSEHOLDS ───────────────────────────────────────────────────

def sample_district_proportions(n_total=2500):
    """Weighted sampling according to nisr data"""
    weights = [0.14, 0.32, 0.18, 0.16, 0.20]  # sum to 1
    return [int(w * n_total) for w in weights]

def generate_households(n_total=2500):
    rows = []
    hh_id = 1

    district_list = list(DISTRICTS.keys())
    counts = sample_district_proportions(n_total)

    for district, n in zip(district_list, counts):
        info = DISTRICTS[district]
        clat, clon = info["center"]
        urban_ratio = info["urban_ratio"]

        for _ in range(n):
            is_urban = np.random.rand() < urban_ratio

            # Geography: scatter around district center
            spread = 0.06 if is_urban else 0.25
            lat = clat + np.random.uniform(-spread, spread)
            lon = clon + np.random.uniform(-spread, spread)

            sector = random.choice(info["sectors"])

            # Household attributes — urban skews better
            children_under5 = np.random.choice([1, 2, 3, 4, 5],
                                               p=[0.35, 0.35, 0.18, 0.08, 0.04])

            if is_urban:
                avg_meal_count = round(np.random.normal(2.6, 0.4), 1)
                water = np.random.choice(WATER_SOURCES, p=[0.40, 0.30, 0.15, 0.10, 0.05])
                sanitation = np.random.choice(SANITATION_TIERS, p=[0.35, 0.45, 0.15, 0.05])
                income = np.random.choice(INCOME_BANDS, p=[0.08, 0.15, 0.25, 0.30, 0.22])
            else:
                avg_meal_count = round(np.random.normal(1.9, 0.5), 1)
                water = np.random.choice(WATER_SOURCES, p=[0.05, 0.10, 0.30, 0.35, 0.20])
                sanitation = np.random.choice(SANITATION_TIERS, p=[0.05, 0.30, 0.45, 0.20])
                income = np.random.choice(INCOME_BANDS, p=[0.30, 0.28, 0.22, 0.13, 0.07])

            avg_meal_count = float(np.clip(avg_meal_count, 1.0, 3.0))

            rows.append({
                "household_id": f"HH{hh_id:05d}",
                "lat": round(lat, 6),
                "lon": round(lon, 6),
                "district": district,
                "sector": sector,
                "is_urban": int(is_urban),
                "children_under5": children_under5,
                "avg_meal_count": avg_meal_count,
                "water_source": water,
                "sanitation_tier": sanitation,
                "income_band": income,
            })
            hh_id += 1

    return pd.DataFrame(rows)