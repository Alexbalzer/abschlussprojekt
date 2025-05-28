# # hier sind die UI für APP

# import streamlit as st
# import plotly.express as px
# import pandas as pd
# from fpdf import FPDF
# import io
# from src.main import (
#     get_average_salary_by_industry,
#     get_salary_vs_automation_risk,
#     get_remote_friendly_stats,
#     get_ai_adoption_by_company_size,
#     get_salary_summary_by_industry,
#     get_growth_jobs_vs_salary
# )

# def create_pdf_with_plot_and_table(df, fig):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)

#     # --- Plotly-Figure als Bild exportieren ---
#     img_bytes = fig.to_image(format="png")
#     img_buffer = io.BytesIO(img_bytes)
#     img_filename = "temp_plot.png"
#     with open(img_filename, "wb") as f:
#         f.write(img_buffer.read())

#     # --- Bild ins PDF einfügen ---
#     # (Achtung: FPDF will einen Dateipfad, keine BytesIO! Daher vorher auf Platte speichern.)
#     pdf.image(img_filename, x=10, y=10, w=pdf.w - 20)
#     pdf.ln(70)  # Abstand nach unten; ggf. an Bildhöhe anpassen

#     # --- Tabelle darunter ausgeben ---
#     pdf.ln(10)
#     col_width = pdf.w / (len(df.columns) + 1)
#     row_height = pdf.font_size * 1.5

#     # Header
#     for col in df.columns:
#         pdf.cell(col_width, row_height, str(col), border=1)
#     pdf.ln(row_height)

#     # Data rows
#     for i, row in df.iterrows():
#         for col in df.columns:
#             pdf.cell(col_width, row_height, str(row[col]), border=1)
#         pdf.ln(row_height)

#     # --- PDF in BytesIO speichern ---
#     pdf_output = pdf.output(dest="S").encode("latin1")
#     pdf_buffer = io.BytesIO(pdf_output)

#     # --- Bilddatei nach PDF-Erstellung löschen ---
#     import os
#     if os.path.exists(img_filename):
#         os.remove(img_filename)

#     return pdf_buffer



# def df_to_pdf_buffer(dataframe):
#     from fpdf import FPDF
#     import io

#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#     col_width = pdf.w / (len(dataframe.columns) + 1)
#     row_height = pdf.font_size * 1.5

#     # Header
#     for col in dataframe.columns:
#         pdf.cell(col_width, row_height, str(col), border=1)
#     pdf.ln(row_height)

#     # Data rows
#     for i, row in dataframe.iterrows():
#         for col in dataframe.columns:
#             pdf.cell(col_width, row_height, str(row[col]), border=1)
#         pdf.ln(row_height)

#     # Speichere das PDF in einen BytesIO-Buffer für Streamlit
#     pdf_output = pdf.output(dest="S").encode("latin1")
#     pdf_buffer = io.BytesIO(pdf_output)
#     return pdf_buffer


# # Hauptfunktion für das Streamlit-Dashboard
# def show_dashboard(conn):
#     st.title("📊 AI-Jobmarkt Analyse Dashboard")

#     # Seitenleiste mit Analyse-Auswahl
#     option = st.sidebar.selectbox(
#         "Wähle eine Analyse",
#         [
#             "ℹ️ Info zum Datensatz",
#             "Durchschnittsgehälter nach Branche",
#             "Automatisierungsrisiko vs. Gehalt",
#             "Remote-Freundlichkeit",
#             "AI-Adoption nach Unternehmensgröße",
#             "Wachstum: Top-Jobs mit Gehalt",
#             "Median vs. Durchschnittsgehalt nach Branche"

#         ]
#     )

#     if option == "ℹ️ Info zum Datensatz":
#         st.header("ℹ️ Informationen zum Datensatz")

#         st.markdown("""
# **Herkunft:**  
# Dieser Datensatz ist vollständig synthetisch und dient ausschließlich Bildungs- und Forschungszwecken.  
# Er basiert auf simulierten Stellenprofilen, die reale Arbeitsmarkttrends nachbilden.

# **Spalten im Datensatz:**

# - **Job Title**: Bezeichnung der Stelle (z. B. „Data Scientist“)  
# - **Branche**: Bereich des Unternehmens (z. B. Technologie, Gesundheitswesen)  
# - **Unternehmensgröße**: Klein / Mittel / Groß  
# - **Lage**: Standort (z. B. London, San Francisco)  
# - **AI-Einführungsgrad**: Wie stark das Unternehmen KI einsetzt (Niedrig / Mittel / Hoch)  
# - **Automatisierungsrisiko**: Wahrscheinlichkeit, dass der Beruf durch KI ersetzt wird  
# - **Erforderliche Fähigkeiten**: z. B. „Python“, „Projektmanagement“  
# - **Gehalt (USD)**: Jahresgehalt  
# - **Remote-Fähigkeit**: Ob der Job remote ausgeführt werden kann  
# - **Jobwachstum**: Prognose: Wachstum / Stabil / Niedergang

# **Anwendungsfälle:**

# - Analyse der Auswirkungen von KI auf Berufe  
# - Skill-Gap-Erkennung  
# - Gehaltsvergleiche nach Branche und Risiko  
# - Unterstützung bei strategischer Personalentwicklung
# """)


#     # -----------------------
#     # 1. Durchschnittsgehälter nach Branche
#     # -----------------------
#     if option == "Durchschnittsgehälter nach Branche":
#         df = get_average_salary_by_industry(conn)

#         # Spalten für schönere Anzeige umbenennen
#         df = df.rename(columns={
#             "Industry": "Branche",
#             "Average_Salary": "Durchschnittsgehalt (USD)"
#         })

#         st.subheader("Durchschnittsgehälter nach Branche")
#         fig = px.bar(df, x="Durchschnittsgehalt (USD)", y="Branche", orientation="h")
#         st.plotly_chart(fig)
#         st.markdown("""
#         **Interpretation:**  
#         Diese Grafik zeigt das durchschnittliche Jahresgehalt in verschiedenen Branchen.  
#         Du kannst erkennen, welche Branchen besonders gut oder schlecht bezahlen und damit Rückschlüsse auf Fachkräftemangel oder Spezialisierung ziehen.
#         """)


#     # -----------------------
#     # 2. Automatisierungsrisiko vs. Gehalt
#     # -----------------------
#     # -----------------------
#     # 2. Automatisierungsrisiko vs. Gehalt oder Jobanzahl
#     # -----------------------
#     elif option == "Automatisierungsrisiko vs. Gehalt":
#         # Basisdaten laden (vereinfachte Gruppierung)
#         df = get_salary_vs_automation_risk(conn)

#         # Spaltennamen umbenennen für schönere Anzeige
#         df = df.rename(columns={
#             "Automation_Risk": "Automatisierungsrisiko",
#             "Average_Salary": "Durchschnittsgehalt (USD)",
#             "Count": "Anzahl Jobs"
#         })

#         st.subheader("Automatisierungsrisiko nach Gehalt oder Jobanzahl")

#         # Auswahl: Welche Kennzahl soll dargestellt werden?
#         metric = st.radio(
#             "Was soll verglichen werden?",
#             ["Durchschnittsgehalt (USD)", "Anzahl Jobs"]
#         )

#         # Auswahl: Gruppierung nach Branche oder Unternehmensgröße
#         compare_dim = st.selectbox(
#             "Vergleiche nach:",
#             ["(keine Gruppierung)", "Branche", "Unternehmensgröße"]
#         )

#         # 📊 Fall 1: keine zusätzliche Gruppierung
#         if compare_dim == "(keine Gruppierung)":
#             fig = px.bar(
#                 df,
#                 x="Automatisierungsrisiko",
#                 y=metric,
#                 color="Automatisierungsrisiko",
#                 hover_data=["Durchschnittsgehalt (USD)", "Anzahl Jobs"]
#             )

#         # 📊 Fall 2: Gruppierung nach Branche oder Unternehmensgröße
#         else:
#             # Wähle das SQL-Feld basierend auf der Auswahl
#             group_col = "Industry" if compare_dim == "Branche" else "Company_Size"

#             # SQL-Abfrage mit Gruppierung nach Automatisierungsrisiko + gewählter Dimension
#             raw_df = pd.read_sql_query(
#                 f"""
#                 SELECT Automation_Risk, {group_col} AS Gruppe,
#                        ROUND(AVG(Salary_USD), 2) AS [Durchschnittsgehalt (USD)],
#                        COUNT(*) AS [Anzahl Jobs]
#                 FROM jobs
#                 GROUP BY Automation_Risk, {group_col}
#                 """,
#                 conn
#             )

#             # Auch hier Spalte für Anzeige anpassen
#             raw_df = raw_df.rename(columns={
#                 "Automation_Risk": "Automatisierungsrisiko"
#             })

#             # Balkendiagramm mit Gruppierungsfarben
#             fig = px.bar(
#                 raw_df,
#                 x="Automatisierungsrisiko",
#                 y=metric,
#                 color="Gruppe",
#                 barmode="group",
#                 hover_data=["Durchschnittsgehalt (USD)", "Anzahl Jobs"]
#             )

#         # Diagramm anzeigen
#         st.plotly_chart(fig)

#     # -----------------------
#     # 3. Remote-Freundlichkeit
#     # -----------------------
#     elif option == "Remote-Freundlichkeit":
#         df = get_remote_friendly_stats(conn)

#         df = df.rename(columns={
#             "Remote_Friendly": "Remote-Arbeit möglich",
#             "Job_Count": "Anzahl Jobs",
#             "Average_Salary": "Durchschnittsgehalt (USD)"
#         })

#         st.subheader("Remote-freundliche vs. nicht-remote Jobs")
#         st.dataframe(df)

#         # Kreisdiagramm zur Verteilung
#         fig = px.pie(df, names="Remote-Arbeit möglich", values="Anzahl Jobs", title="Remote vs. Nicht-Remote")
#         st.plotly_chart(fig)

#     # -----------------------
#     # 4. AI-Adoption nach Unternehmensgröße
#     # -----------------------
#     elif option == "AI-Adoption nach Unternehmensgröße":
#         df = get_ai_adoption_by_company_size(conn)

#         df = df.rename(columns={
#             "Company_Size": "Unternehmensgröße",
#             "AI_Adoption_Level": "KI-Einsatz",
#             "Count": "Anzahl Jobs"
#         })

#         st.subheader("KI-Adoption nach Unternehmensgröße")
#         fig = px.bar(df,
#                      x="Unternehmensgröße",
#                      y="Anzahl Jobs",
#                      color="KI-Einsatz",
#                      barmode="group")
#         st.plotly_chart(fig)

#     # -----------------------
#     # 5. Wachsende Top-Berufe mit Gehalt + Drillthrough
#     # -----------------------
#     elif option == "Wachstum: Top-Jobs mit Gehalt":
#         df = get_growth_jobs_vs_salary(conn)

#         df = df.rename(columns={
#             "Job_Title": "Job Title",
#             "Salary_USD": "Salary (USD)",
#             "Job_Growth_Projection": "Job Growth"
#         })

#         st.subheader("Wachsende Berufe mit hohem Gehalt")

#         # Balkendiagramm
#         fig = px.bar(df, x="Salary (USD)", y="Job Title", orientation="h")
#         st.plotly_chart(fig)

#         # Auswahl für Drillthrough
#         selected_job = st.selectbox("🔍 Mehr Details zu einem Beruf anzeigen:", df["Job Title"].unique())

#         # Detaildaten abfragen und anzeigen
#         job_details = pd.read_sql_query(
#             """
#             SELECT *
#             FROM jobs
#             WHERE Job_Title = ?
#             """,
#             conn,
#             params=(selected_job,)
#         )

#         st.markdown(f"### Details für: **{selected_job}**")
#         st.dataframe(job_details)

#     # -----------------------
#     # 6. Median vs. Durchschnittsgehalt nach Branche
#     # -----------------------


#     elif option == "Median vs. Durchschnittsgehalt nach Branche":
#         df = get_salary_summary_by_industry(conn)
#         df = df.rename(columns={
#             "Industry": "Branche",
#             "Durchschnittsgehalt": "Ø Gehalt (USD)",
#             "Mediangehalt": "Median (USD)"
#         })

#         st.subheader("Vergleich: Durchschnittsgehalt vs. Median je Branche")
#         fig = px.bar(
#             df,
#             x="Branche",
#             y=["Ø Gehalt (USD)", "Median (USD)"],
#             barmode="group"
#         )
#         st.plotly_chart(fig)

#         st.markdown("""
#         **Interpretation:**  
#         Der **Median** ist der „mittlere Wert“ – er zeigt, was jemand verdient, der genau in der Mitte liegt.  
#         Der **Durchschnitt (arithmetisches Mittel)** wird stark durch sehr hohe oder sehr niedrige Gehälter beeinflusst.
#         👉 Wenn der Median **deutlich kleiner** als der Durchschnitt ist, gibt es einige **sehr gut bezahlte Ausreißer**.  
#         👉 Wenn beide Werte nah beieinander liegen, ist die Gehaltsverteilung eher „symmetrisch“.
#         """)

#         # ----- Excel-Export -----
#         excel_buffer = io.BytesIO()
#         df.to_excel(excel_buffer, index=False)
#         excel_buffer.seek(0)

#         st.download_button(
#             label="⬇️ Tabelle als Excel herunterladen",
#             data=excel_buffer,
#             file_name="median_vs_mittelwert_nach_branche.xlsx",
#             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#         )

#         # ----- PDF-Export -----
#         # def df_to_pdf_buffer(dataframe):
#         #     pdf = FPDF()
#         #     pdf.add_page()
#         #     pdf.set_font("Arial", size=12)
#         #     col_width = pdf.w / (len(dataframe.columns) + 1)
#         #     row_height = pdf.font_size * 1.5

#         #     # Header
#         #     for col in dataframe.columns:
#         #         pdf.cell(col_width, row_height, str(col), border=1)
#         #     pdf.ln(row_height)

#         #     # Data rows
#         #     for i, row in dataframe.iterrows():
#         #         for col in dataframe.columns:
#         #             pdf.cell(col_width, row_height, str(row[col]), border=1)
#         #         pdf.ln(row_height)

#         #     pdf_buffer = io.BytesIO()
#         #     pdf.output(pdf_buffer)
#         #     pdf_buffer.seek(0)
#         #     return pdf_buffer

#         # pdf_buffer = df_to_pdf_buffer(df)

#         # st.download_button(
#         #     label="⬇️ Tabelle als PDF herunterladen",
#         #     data=pdf_buffer,
#         #     file_name="median_vs_mittelwert_nach_branche.pdf",
#         #     mime="application/pdf"
#         # )
#         # ... (dein Code zur Grafik und Tabelle)

# # PDF Download mit Bild & Tabelle
#         pdf_buffer = create_pdf_with_plot_and_table(df, fig)
#         st.download_button(
#             label="⬇️ Tabelle & Grafik als PDF herunterladen",
#             data=pdf_buffer,
#             file_name="median_vs_mittelwert_mit_grafik.pdf",
#             mime="application/pdf"
#         )


