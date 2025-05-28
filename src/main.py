#  Hier sind die Funktionen für die APP

import sqlite3
import pandas as pd
import os

def create_connection(db_path):
    conn = sqlite3.connect(db_path)
    return conn

def initialize_database(db_path="database/job_market.db", csv_path="data/job_market.csv"):
    # Wenn DB existiert, überspringen
    if os.path.exists(db_path):
        print("Datenbank existiert bereits. Kein Import durchgeführt.")
        return

    # CSV laden
    df = pd.read_csv(csv_path)
    df.columns = [col.strip().replace(" ", "_") for col in df.columns]

    # Verbindung & Import
    conn = create_connection(db_path)
    df.to_sql("jobs", conn, if_exists="replace", index=False)
    conn.close()

    print("Datenbank und Tabelle erfolgreich erstellt.")


# Nur bei direktem Start
if __name__ == "__main__":
    initialize_database()

# --- Analysefunktionen ---

def get_average_salary_by_industry(conn):
    query = """
        SELECT Industry, ROUND(AVG(Salary_USD), 2) AS Average_Salary
        FROM jobs
        GROUP BY Industry
        ORDER BY Average_Salary DESC
    """
    return pd.read_sql_query(query, conn)

def get_salary_vs_automation_risk(conn):
    query = """
        SELECT Automation_Risk, ROUND(AVG(Salary_USD), 2) AS Average_Salary, COUNT(*) AS Count
        FROM jobs
        GROUP BY Automation_Risk
        ORDER BY Average_Salary DESC
    """
    return pd.read_sql_query(query, conn)

def get_remote_friendly_stats(conn):
    query = """
        SELECT Remote_Friendly, COUNT(*) AS Job_Count, ROUND(AVG(Salary_USD), 2) AS Average_Salary
        FROM jobs
        GROUP BY Remote_Friendly
    """
    return pd.read_sql_query(query, conn)

def get_ai_adoption_by_company_size(conn):
    query = """
        SELECT Company_Size, AI_Adoption_Level, COUNT(*) AS Count
        FROM jobs
        GROUP BY Company_Size, AI_Adoption_Level
        ORDER BY Company_Size, AI_Adoption_Level
    """
    return pd.read_sql_query(query, conn)

def get_growth_jobs_vs_salary(conn):
    query = """
        SELECT Job_Title, Salary_USD, Job_Growth_Projection
        FROM jobs
        WHERE Job_Growth_Projection = 'Growth'
        ORDER BY Salary_USD DESC
        LIMIT 10
    """
    return pd.read_sql_query(query, conn)

def get_salary_summary_by_industry(conn):
    # Hole die nötigen Daten aus der DB
    df = pd.read_sql_query("SELECT Industry, Salary_USD FROM jobs", conn)
    # Gruppiere nach Branche, berechne Mittelwert und Median
    result = df.groupby("Industry").agg({
        "Salary_USD": ["mean", "median"]
    }).reset_index()
    # Die Spalten werden zu MultiIndex, das machen wir wieder flach
    result.columns = ["Industry", "Durchschnittsgehalt", "Mediangehalt"]
    result["Durchschnittsgehalt"] = result["Durchschnittsgehalt"].round(2)
    result["Mediangehalt"] = result["Mediangehalt"].round(2)
    return result




conn = create_connection("database/job_market.db")
df = get_average_salary_by_industry(conn)
print(df)
