# #import streamlit as st
# from src.main import create_connection
# from src.ui import show_dashboard

# # Hauptfunktion der App – verbindet UI mit der Datenbank
# def main():
#     # Verbindung zur SQLite-Datenbank aufbauen
#     conn = create_connection("database/job_market.db")
    
#     # Dashboard anzeigen
#     show_dashboard(conn)
    
#     # Verbindung schließen
#     conn.close()

# # Nur ausführen, wenn dieses Skript direkt gestartet wird
# if __name__ == "__main__":
#     main()

import streamlit as st
from src.main import create_connection
from src.ui import show_dashboard

# Setze globale Eigenschaften der Streamlit-Seite
st.set_page_config(
    page_title="AI Job Market Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    conn = create_connection("database/job_market.db")
    show_dashboard(conn)
    conn.close()

if __name__ == "__main__":
    main()
