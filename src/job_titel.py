import pandas as pd

# Einlesen der bestehenden CSV
df = pd.read_csv("data/job_market.csv")

# Alle eindeutigen Jobtitel aus der Spalte 'job_titel' extrahieren
jobtitles = df["Job_Title"].dropna().unique()

# Als neue CSV speichern (eine Spalte, keine Überschrift)
pd.Series(jobtitles).to_csv("data/jobtitles.csv", index=False, header=False)

print(f"Es wurden {len(jobtitles)} Jobtitel gespeichert.")
