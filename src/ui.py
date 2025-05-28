# hier sind die UI für APP
# --- UI für APP ---

import streamlit as st
import plotly.express as px
import pandas as pd
import kaleido
from fpdf import FPDF
import io
import tempfile
import os
from src.main import (
    get_average_salary_by_industry,
    get_salary_vs_automation_risk,
    get_remote_friendly_stats,
    get_ai_adoption_by_company_size,
    get_salary_summary_by_industry,
    get_growth_jobs_vs_salary
)

# Hilfsfunktion: PDF mit Plotly-Grafik und Tabelle erzeugen
def create_pdf_with_plot_and_table(df, fig):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("helvetica", size=12)

        # --- Plotly-Figur als Bild (PNG) speichern (temporäre Datei) ---
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            fig.write_image(tmpfile.name)
            img_filename = tmpfile.name

        # --- Bild ins PDF einfügen ---
        pdf.image(img_filename, x=10, y=10, w=pdf.w - 20)
        pdf.ln(70)  # Abstand nach unten

        # --- Tabelle darunter einfügen ---
        pdf.ln(10)
        col_width = pdf.w / (len(df.columns) + 1)
        row_height = pdf.font_size * 1.5

        # Header
        for col in df.columns:
            pdf.cell(col_width, row_height, str(col), border=1)
        pdf.ln(row_height)

        # Data rows
        for i, row in df.iterrows():
            for col in df.columns:
                pdf.cell(col_width, row_height, str(row[col]), border=1)
            pdf.ln(row_height)

        # --- PDF in BytesIO speichern ---
        pdf_output = pdf.output(dest="S").encode("latin1")
        pdf_buffer = io.BytesIO(pdf_output)

        # --- Temp-Bild löschen ---
        os.remove(img_filename)

        return pdf_buffer

    except Exception as e:
        st.error(f"PDF-Export fehlgeschlagen: {e}")
        return None

# Hauptfunktion für das Streamlit-Dashboard
def show_dashboard(conn):
    st.title("📊 AI-Jobmarkt Analyse Dashboard")

    # Seitenleiste mit Analyse-Auswahl
    option = st.sidebar.selectbox(
        "Wähle eine Analyse",
        [
            "ℹ️ Info zum Datensatz",
            "Durchschnittsgehälter nach Branche",
            "Automatisierungsrisiko vs. Gehalt",
            "Remote-Freundlichkeit",
            "AI-Adoption nach Unternehmensgröße",
            "Wachstum: Top-Jobs mit Gehalt",
            "Median vs. Durchschnittsgehalt nach Branche"
        ]
    )

    if option == "ℹ️ Info zum Datensatz":
        st.header("ℹ️ Informationen zum Datensatz")
        st.markdown("""
**Herkunft:**  
Dieser Datensatz ist vollständig synthetisch und dient ausschließlich Bildungs- und Forschungszwecken.  
Er basiert auf simulierten Stellenprofilen, die reale Arbeitsmarkttrends nachbilden.

**Spalten im Datensatz:**
- **Job Title**: Bezeichnung der Stelle (z. B. „Data Scientist“)  
- **Branche**: Bereich des Unternehmens (z. B. Technologie, Gesundheitswesen)  
- **Unternehmensgröße**: Klein / Mittel / Groß  
- **Lage**: Standort (z. B. London, San Francisco)  
- **AI-Einführungsgrad**: Wie stark das Unternehmen KI einsetzt (Niedrig / Mittel / Hoch)  
- **Automatisierungsrisiko**: Wahrscheinlichkeit, dass der Beruf durch KI ersetzt wird  
- **Erforderliche Fähigkeiten**: z. B. „Python“, „Projektmanagement“  
- **Gehalt (USD)**: Jahresgehalt  
- **Remote-Fähigkeit**: Ob der Job remote ausgeführt werden kann  
- **Jobwachstum**: Prognose: Wachstum / Stabil / Niedergang

**Anwendungsfälle:**
- Analyse der Auswirkungen von KI auf Berufe  
- Skill-Gap-Erkennung  
- Gehaltsvergleiche nach Branche und Risiko  
- Unterstützung bei strategischer Personalentwicklung
""")

    # -----------------------
    # 1. Durchschnittsgehälter nach Branche
    # -----------------------
    if option == "Durchschnittsgehälter nach Branche":
        df = get_average_salary_by_industry(conn)
        df = df.rename(columns={
            "Industry": "Branche",
            "Average_Salary": "Durchschnittsgehalt (USD)"
        })
        st.subheader("Durchschnittsgehälter nach Branche")
        fig = px.bar(df, x="Durchschnittsgehalt (USD)", y="Branche", orientation="h")
        st.plotly_chart(fig)
        st.markdown("""
**Interpretation:**  
Diese Grafik zeigt das durchschnittliche Jahresgehalt in verschiedenen Branchen.  
Du kannst erkennen, welche Branchen besonders gut oder schlecht bezahlen und damit Rückschlüsse auf Fachkräftemangel oder Spezialisierung ziehen.
""")

    # -----------------------
    # 2. Automatisierungsrisiko vs. Gehalt oder Jobanzahl
    # -----------------------
    elif option == "Automatisierungsrisiko vs. Gehalt":
        df = get_salary_vs_automation_risk(conn)
        df = df.rename(columns={
            "Automation_Risk": "Automatisierungsrisiko",
            "Average_Salary": "Durchschnittsgehalt (USD)",
            "Count": "Anzahl Jobs"
        })
        st.subheader("Automatisierungsrisiko nach Gehalt oder Jobanzahl")
        metric = st.radio(
            "Was soll verglichen werden?",
            ["Durchschnittsgehalt (USD)", "Anzahl Jobs"]
        )
        compare_dim = st.selectbox(
            "Vergleiche nach:",
            ["(keine Gruppierung)", "Branche", "Unternehmensgröße"]
        )
        if compare_dim == "(keine Gruppierung)":
            fig = px.bar(
                df,
                x="Automatisierungsrisiko",
                y=metric,
                color="Automatisierungsrisiko",
                hover_data=["Durchschnittsgehalt (USD)", "Anzahl Jobs"]
            )
        else:
            group_col = "Industry" if compare_dim == "Branche" else "Company_Size"
            raw_df = pd.read_sql_query(
                f"""
                SELECT Automation_Risk, {group_col} AS Gruppe,
                       ROUND(AVG(Salary_USD), 2) AS [Durchschnittsgehalt (USD)],
                       COUNT(*) AS [Anzahl Jobs]
                FROM jobs
                GROUP BY Automation_Risk, {group_col}
                """,
                conn
            )
            raw_df = raw_df.rename(columns={
                "Automation_Risk": "Automatisierungsrisiko"
            })
            fig = px.bar(
                raw_df,
                x="Automatisierungsrisiko",
                y=metric,
                color="Gruppe",
                barmode="group",
                hover_data=["Durchschnittsgehalt (USD)", "Anzahl Jobs"]
            )
        st.plotly_chart(fig)

    # -----------------------
    # 3. Remote-Freundlichkeit
    # -----------------------
    elif option == "Remote-Freundlichkeit":
        df = get_remote_friendly_stats(conn)
        df = df.rename(columns={
            "Remote_Friendly": "Remote-Arbeit möglich",
            "Job_Count": "Anzahl Jobs",
            "Average_Salary": "Durchschnittsgehalt (USD)"
        })
        st.subheader("Remote-freundliche vs. nicht-remote Jobs")
        st.dataframe(df)
        fig = px.pie(df, names="Remote-Arbeit möglich", values="Anzahl Jobs", title="Remote vs. Nicht-Remote")
        st.plotly_chart(fig)

    # -----------------------
    # 4. AI-Adoption nach Unternehmensgröße
    # -----------------------
    elif option == "AI-Adoption nach Unternehmensgröße":
        df = get_ai_adoption_by_company_size(conn)
        df = df.rename(columns={
            "Company_Size": "Unternehmensgröße",
            "AI_Adoption_Level": "KI-Einsatz",
            "Count": "Anzahl Jobs"
        })
        st.subheader("KI-Adoption nach Unternehmensgröße")
        fig = px.bar(df,
                     x="Unternehmensgröße",
                     y="Anzahl Jobs",
                     color="KI-Einsatz",
                     barmode="group")
        st.plotly_chart(fig)

    # -----------------------
    # 5. Wachsende Top-Berufe mit Gehalt + Drillthrough
    # -----------------------
    elif option == "Wachstum: Top-Jobs mit Gehalt":
        df = get_growth_jobs_vs_salary(conn)
        df = df.rename(columns={
            "Job_Title": "Job Title",
            "Salary_USD": "Salary (USD)",
            "Job_Growth_Projection": "Job Growth"
        })
        st.subheader("Wachsende Berufe mit hohem Gehalt")
        fig = px.bar(df, x="Salary (USD)", y="Job Title", orientation="h")
        st.plotly_chart(fig)
        selected_job = st.selectbox("🔍 Mehr Details zu einem Beruf anzeigen:", df["Job Title"].unique())
        job_details = pd.read_sql_query(
            """
            SELECT *
            FROM jobs
            WHERE Job_Title = ?
            """,
            conn,
            params=(selected_job,)
        )
        st.markdown(f"### Details für: **{selected_job}**")
        st.dataframe(job_details)

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
# **Interpretation:**  
# Der **Median** ist der „mittlere Wert“ – er zeigt, was jemand verdient, der genau in der Mitte liegt.  
# Der **Durchschnitt (arithmetisches Mittel)** wird stark durch sehr hohe oder sehr niedrige Gehälter beeinflusst.
# 👉 Wenn der Median **deutlich kleiner** als der Durchschnitt ist, gibt es einige **sehr gut bezahlte Ausreißer**.  
# 👉 Wenn beide Werte nah beieinander liegen, ist die Gehaltsverteilung eher „symmetrisch“.
# """)

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

#         # ----- PDF-Export: Mit Grafik + Tabelle -----
#         st.info("Starte PDF-Export-Test...")

#         pdf_buffer = create_pdf_with_plot_and_table(df, fig)
#         st.write(f"pdf_buffer Typ: {type(pdf_buffer)}")

#         if pdf_buffer:
#             st.download_button(
#                 label="⬇️ Tabelle & Grafik als PDF herunterladen",
#                 data=pdf_buffer,
#                 file_name="median_vs_mittelwert_mit_grafik.pdf",
#                 mime="application/pdf"
#             )
#         else:
#             st.info("Kein PDF-Download verfügbar (möglicherweise ist beim PDF-Export ein Fehler aufgetreten).")

    # -----------------------
    # 6. Median vs. Durchschnittsgehalt nach Branche
    # -----------------------
    elif option == "Median vs. Durchschnittsgehalt nach Branche":
        df = get_salary_summary_by_industry(conn)
        df = df.rename(columns={
            "Industry": "Branche",
            "Durchschnittsgehalt": "Ø Gehalt (USD)",
            "Mediangehalt": "Median (USD)"
        })
        st.subheader("Vergleich: Durchschnittsgehalt vs. Median je Branche")
        fig = px.bar(
            df,
            x="Branche",
            y=["Ø Gehalt (USD)", "Median (USD)"],
            barmode="group"
        )
        st.plotly_chart(fig)
        st.markdown("""
**Interpretation:**  
Der **Median** ist der „mittlere Wert“ – er zeigt, was jemand verdient, der genau in der Mitte liegt.  
Der **Durchschnitt (arithmetisches Mittel)** wird stark durch sehr hohe oder sehr niedrige Gehälter beeinflusst.
👉 Wenn der Median **deutlich kleiner** als der Durchschnitt ist, gibt es einige **sehr gut bezahlte Ausreißer**.  
👉 Wenn beide Werte nah beieinander liegen, ist die Gehaltsverteilung eher „symmetrisch“.
""")

        # ----- Excel-Export -----
        excel_buffer = io.BytesIO()
        df.to_excel(excel_buffer, index=False)
        excel_buffer.seek(0)
        st.download_button(
            label="⬇️ Tabelle als Excel herunterladen",
            data=excel_buffer,
            file_name="median_vs_mittelwert_nach_branche.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # ----- PNG-Speicher-Test -----
        try:
            fig.write_image("test_plot.png")
            st.success("✅ Plotly PNG wurde gespeichert!")
        except Exception as e:
            st.error(f"❌ Plotly PNG konnte NICHT gespeichert werden: {e}")

        # ----- PDF-Export: Mit Grafik + Tabelle -----
        st.info("Starte PDF-Export-Test...")

        pdf_buffer = create_pdf_with_plot_and_table(df, fig)
        st.write(f"pdf_buffer Typ: {type(pdf_buffer)}")

        if pdf_buffer:
            st.download_button(
                label="⬇️ Tabelle & Grafik als PDF herunterladen",
                data=pdf_buffer,
                file_name="median_vs_mittelwert_mit_grafik.pdf",
                mime="application/pdf"
            )
        else:
            st.info("Kein PDF-Download verfügbar (möglicherweise ist beim PDF-Export ein Fehler aufgetreten).")
