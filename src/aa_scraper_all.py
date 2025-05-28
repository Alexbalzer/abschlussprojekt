# import requests
# import pandas as pd
# import time
# import os

# API_KEY = "jobboerse-jobsuche"
# SAVE_PATH = "data/raw/arbeitsagentur_jobpool.csv"
# TITLES_PATH = "data/jobtitles.csv"
# PAGE_SIZE = 50

# os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)

# # Lade Jobtitel aus CSV (erste Spalte)
# titles = pd.read_csv(TITLES_PATH, header=None)[0].dropna().unique()

# url = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs"
# headers = {
#     "Accept": "application/json",
#     "X-API-Key": API_KEY
# }

# all_jobs = []
# for title in titles:
#     print(f"\nStarte Suche für Jobtitel: {title}")
#     params = {
#         "was": title,
#         "zeitarbeit": "false",
#         "angebotsart": "1",
#         "externestellenboersen": "true",
#         "size": PAGE_SIZE,
#         "page": 1
#     }
#     while True:
#         print(f"Hole Seite {params['page']} für {title} ...")
#         response = requests.get(url, headers=headers, params=params)
#         if response.status_code != 200:
#             print("Fehler beim Abruf:", response.status_code)
#             print(response.text)
#             break

#         data = response.json()
#         jobs = data.get('stellenangebote', [])
#         if not jobs:
#             print("Keine weiteren Jobs gefunden für", title)
#             break

#         for job in jobs:
#             arbeitsort = job.get("arbeitsort", {})
#             job_url = job.get("externeUrl")
#             if not job_url and job.get("refnr"):
#                 job_url = f"https://jobboerse.arbeitsagentur.de/vamJB/stellenangebotFinden.html?refnr={job['refnr']}"
#             all_jobs.append({
#                 "Suchbegriff": title,
#                 "Titel": job.get("titel"),
#                 "Beruf": job.get("beruf"),
#                 "Arbeitgeber": job.get("arbeitgeber"),
#                 "Ort": arbeitsort.get("ort", ""),
#                 "Region": arbeitsort.get("region", ""),
#                 "Land": arbeitsort.get("land", ""),
#                 "PLZ": arbeitsort.get("plz", ""),
#                 "Veröffentlicht am": job.get("aktuelleVeroeffentlichungsdatum"),
#                 "Eintrittsdatum": job.get("eintrittsdatum"),
#                 "URL": job_url
#             })

#         if len(jobs) < PAGE_SIZE:
#             break
#         params['page'] += 1
#         time.sleep(0.5)  # Fair bleiben!

# # Alles speichern
# df = pd.DataFrame(all_jobs)
# df.to_csv(SAVE_PATH, index=False, encoding="utf-8")
# print(f"\nFertig! Es wurden {len(df)} Jobs für {len(titles)} Jobtitel gespeichert in {SAVE_PATH}.")
