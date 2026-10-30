# Women and work in India — PLFS dashboard

A read-only Streamlit dashboard for broad, survey-weighted aggregate results from the PLFS July 2023–June 2024 first-visit person file. The analysis ran on a Hadoop/Spark YARN cluster before these summaries were exported. This repository has **no raw PLFS person records, no detailed five-way cube, and no individual model predictions**. The public dashboard shows broad groups; detailed combined filters remain in the local project.

## Run locally

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app/app.py
```

## Deploy on Streamlit Community Cloud

Create a GitHub repository from this folder, push the `main` branch, then select **`app/app.py`** as the entrypoint in Community Cloud. The root `requirements.txt` provides dependencies. No Docker or Hadoop cluster is required to display the saved results.

## Data and interpretation

Source: [MoSPI PLFS 2023–24 catalog](https://microdata.gov.in/NADA/index.php/catalog/213). The public bundle contains broad aggregate rates and sample counts only. The technical definitions, caveats, and saved YARN application IDs are shown in the dashboard. The source data remain subject to the access agreement accepted by the data recipient. These results do not include survey-design margins of error and cannot establish causes. The classifier is educational, not for individual decisions.

Host Grotesk is bundled under the SIL Open Font License in `app/assets/OFL-Host-Grotesk.txt`.
