# KTT-Hackathon-Day-1

Stunting Risk Heatmap Dashboard
Project Overview

This project was developed as part of the AIMS KTT Hackathon (S2.T1.2) challenge focused on tackling childhood stunting in Rwanda through data-driven decision making.

The objective was to build a dashboard that helps local authorities identify high-risk households and sectors using synthetic household-level data. By combining risk scoring, geospatial visualization, and printable reports, the solution aims to support faster intervention planning for vulnerable communities.

The platform was designed with low-resource environments in mind, where many decision-makers may rely on printed documents rather than laptops or smartphones.

Key Features
Household Risk Scoring

A scoring model was developed using household indicators such as:

Meal frequency
Water source
Sanitation level
Income band
Number of children under five

Each household receives a stunting risk score to prioritize intervention.

Sector-Level Heatmap Dashboard

Interactive district and sector visualizations display geographic concentrations of risk through choropleth maps.

Printable Reports

Sector-level A4 reports were planned to provide local leaders with:

Top high-risk anonymized households
Key risk drivers
Actionable intervention priorities
Tools & Technologies
Python
Pandas
Plotly / Folium
Streamlit
GeoJSON Mapping
Risk Scoring Models (Rule-based / Logistic Regression)
Project Structure
├── dashboard.py
├── risk_scorer.py
├── households.csv
├── gold_stunting_flag.csv
├── districts.geojson
├── printable/
└── README.md
How to Run

Current Status

Due to limited time during the hackathon, the project could not be fully completed to the intended final production standard. Core functionality and concept validation were achieved, but several planned enhancements remain unfinished.

Planned Improvements
1. Color-Coded Authority Documents

Printable reports should use a clear color-coding system for authorities:

Red → urgent intervention required
Orange → medium priority
Green → low priority

This would improve speed of interpretation during field meetings.

2. Simplified Graph Design

Current dashboards could be improved by reducing visual clutter and limiting graphs to only the most decision-relevant indicators.

3. National Data Centralization

A centralized national database should be implemented so district-level data flows into one secure system, allowing better monitoring, reporting, and resource allocation.

4. Inter-District Connectivity

Neighboring districts should be connected at the central system level to improve coordination where vulnerable households move across administrative boundaries or share common infrastructure.

5. Offline Deployment

Deploy lightweight offline versions for low-connectivity rural zones.

Real-World Impact

If scaled nationally, this system could help:

Detect high-risk communities earlier
Improve nutrition intervention targeting
Support district planning meetings
Reduce response delays
Strengthen national child health monitoring systems
Conclusion

This project demonstrates how geospatial analytics and simple machine learning tools can support public health decision-making in Rwanda. While unfinished due to time constraints, the concept has strong potential for further development into a national decision-support platform.
