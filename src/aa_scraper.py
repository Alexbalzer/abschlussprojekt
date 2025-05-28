#       python src/aa_scraper.py


# # import requests
# # import json

# # BASE_URL = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service"
# # job_search_endpoint = "/pc/v4/jobs"
# # headers = {"X-API-Key": "jobboerse-jobsuche"}
# # params = {
# #     "page": 1,
# #     "size": 5,
# #     "ort": "Berlin",
# #     "umkreis": 25
# # }

# # response = requests.get(BASE_URL + job_search_endpoint, headers=headers, params=params)

# # print("Status Code:", response.status_code)
# # if response.ok:
# #     data = response.json()
# #     print(json.dumps(data, indent=2, ensure_ascii=False))
# # else:
# #     print("Fehler:", response.text)
 
# import requests
# import pandas as pd
# import time
# import os

# API_KEY = "jobboerse-jobsuche"
# SAVE_PATH = "data/raw/arbeitsagentur_jobs.csv"
# SEARCH_TERM = "Data Scientist"
# PAGE_SIZE = 50

# os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)

# url = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs"
# headers = {
#     "Accept": "application/json",
#     "X-API-Key": API_KEY
# }
# params = {
#     "was": SEARCH_TERM,
#     "zeitarbeit": "false",
#     "angebotsart": "1",
#     "size": PAGE_SIZE,
#     "page": 1
# }

# all_jobs = []
# while True:
#     print(f"Hole Seite {params['page']} ...")
#     response = requests.get(url, headers=headers, params=params)
#     if response.status_code != 200:
#         print("Fehler beim Abruf:", response.status_code)
#         print(response.text)
#         break

#     data = response.json()
#     print("Gefundene Gesamtjobs laut API:", data.get("maxErgebnisse"))

#     jobs = data.get('stellenangebote', [])
#     if not jobs:
#         print("Keine weiteren Jobs gefunden.")
#         break

#     for job in jobs:
#         arbeitsort = job.get("arbeitsort", {})
#         job_url = job.get("externeUrl")
#         # Wenn kein externer Link, baue eine interne Such-URL (optional)
#         if not job_url and job.get("refnr"):
#             job_url = f"https://jobboerse.arbeitsagentur.de/vamJB/stellenangebotFinden.html?refnr={job['refnr']}"
#         all_jobs.append({
#             "Titel": job.get("titel"),
#             "Beruf": job.get("beruf"),
#             "Arbeitgeber": job.get("arbeitgeber"),
#             "Ort": arbeitsort.get("ort", ""),
#             "Region": arbeitsort.get("region", ""),
#             "Land": arbeitsort.get("land", ""),
#             "PLZ": arbeitsort.get("plz", ""),
#             "Veröffentlicht am": job.get("aktuelleVeroeffentlichungsdatum"),
#             "Eintrittsdatum": job.get("eintrittsdatum"),
#             "URL": job_url
#         })

#     # Abbruchbedingung: Keine weiteren Seiten (paging.hasNext gibt's offenbar nicht immer!)
#     if len(jobs) < PAGE_SIZE:
#         break
#     params['page'] += 1
#     time.sleep(0.5)  # Fair bleiben!

# df = pd.DataFrame(all_jobs)
# df.to_csv(SAVE_PATH, index=False, encoding="utf-8")
# print(f"\nFertig! Es wurden {len(df)} Jobs gespeichert in {SAVE_PATH}.")

import requests
import pandas as pd
import time
import os
import sqlite3

API_KEY = "jobboerse-jobsuche"
DB_PATH = "database/job_market.db"
TITLES_PATH = "data/jobtitles.csv"
TABLE_NAME = "arbeitsagentur_jobpool"
PAGE_SIZE = 50

# Lade Jobtitel aus CSV (erste Spalte)
titles = pd.read_csv(TITLES_PATH, header=None)[0].dropna().unique()

url = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs"
headers = {
    "Accept": "application/json",
    "X-API-Key": API_KEY
}

all_jobs = []
for title in titles:
    print(f"\nStarte Suche für Jobtitel: {title}")
    params = {
        "was": title,
        "zeitarbeit": "false",
        "angebotsart": "1",
        "externestellenboersen": "true",
        "size": PAGE_SIZE,
        "page": 1
    }
    while True:
        print(f"Hole Seite {params['page']} für {title} ...")
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print("Fehler beim Abruf:", response.status_code)
            print(response.text)
            break

        data = response.json()
        jobs = data.get('stellenangebote', [])
        if not jobs:
            print("Keine weiteren Jobs gefunden für", title)
            break

        for job in jobs:
            arbeitsort = job.get("arbeitsort", {})
            job_url = job.get("externeUrl")
            if not job_url and job.get("refnr"):
                job_url = f"https://jobboerse.arbeitsagentur.de/vamJB/stellenangebotFinden.html?refnr={job['refnr']}"
            all_jobs.append({
                "Suchbegriff": title,
                "Titel": job.get("titel"),
                "Beruf": job.get("beruf"),
                "Arbeitgeber": job.get("arbeitgeber"),
                "Ort": arbeitsort.get("ort", ""),
                "Region": arbeitsort.get("region", ""),
                "Land": arbeitsort.get("land", ""),
                "PLZ": arbeitsort.get("plz", ""),
                "Veröffentlicht_am": job.get("aktuelleVeroeffentlichungsdatum"),
                "Eintrittsdatum": job.get("eintrittsdatum"),
                "URL": job_url
            })

        if len(jobs) < PAGE_SIZE:
            break
        params['page'] += 1
        time.sleep(0.5)  # Fair bleiben!

# Alles als DataFrame
df = pd.DataFrame(all_jobs)

# Direkt in SQLite speichern (Tabelle ggf. überschreiben)
with sqlite3.connect(DB_PATH) as conn:
    df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)
print(f"\nFertig! Es wurden {len(df)} Jobs in die Tabelle '{TABLE_NAME}' von '{DB_PATH}' gespeichert.")
