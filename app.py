import streamlit as st
from src.parser import parse_whatsapp_chat
import src.analyzer as analyzer
import matplotlib.pyplot as plt

# --------- Cargar el chat solo una vez ---------
@st.cache_data
def load_chat():
    return parse_whatsapp_chat('data/_chat.txt')

chat_df = load_chat()

st.title("Chat Analyzer 📊")
st.markdown("Analiza tu chat de WhatsApp de manera **interactiva**.")

# --------- Controles de filtrado ---------
years = st.multiselect("Año", sorted(chat_df["timestamp"].dt.year.unique()), default=sorted(chat_df["timestamp"].dt.year.unique()))
months = st.multiselect("Mes", sorted(chat_df["timestamp"].dt.month.unique()))
start_hour = st.slider("Hora de inicio", 0, 23, 18)
end_hour = st.slider("Hora de fin", 1, 24, 24)
users = st.multiselect("Usuarios", sorted(chat_df["sender"].unique()))

single_line = st.checkbox("Solo mensajes de una línea (sin saltos de línea)", value=False)

# --------- Filtro combinado usando analyzer ---------
filtered = analyzer.filter_chat(
    chat_df,
    years=years if years else None,
    months=months if months else None,
    start_hour=start_hour,
    end_hour=end_hour,
    users=users if users else None,
    single_line_only=single_line
)

st.info(f"**Total mensajes filtrados:** {len(filtered)}")

# --------- Gráfico: Mensajes por mes ---------
msgs_per_month = analyzer.messages_per_month(filtered)
if not msgs_per_month.empty:
    st.subheader("Mensajes por mes")
    fig, ax = plt.subplots()
    msgs_per_month.plot(kind="bar", ax=ax)
    ax.set_xlabel("Mes")
    ax.set_ylabel("Cantidad de mensajes")
    st.pyplot(fig)
else:
    st.warning("No hay mensajes para graficar por mes.")

# --------- Gráfico: Mensajes por hora ---------
msgs_per_hour = analyzer.messages_per_hour(filtered)
if not msgs_per_hour.empty:
    st.subheader("Mensajes por hora del día")
    fig2, ax2 = plt.subplots()
    msgs_per_hour.plot(kind="bar", ax=ax2)
    ax2.set_xlabel("Hora del día")
    ax2.set_ylabel("Cantidad de mensajes")
    st.pyplot(fig2)

# --------- Gráfico: Proporción por usuario ---------
user_counts = analyzer.messages_per_user(filtered)
if not user_counts.empty:
    st.subheader("Mensajes por usuario")
    fig3, ax3 = plt.subplots()
    user_counts.plot(kind="pie", autopct='%1.0f%%', ax=ax3)
    ax3.set_ylabel("")
    st.pyplot(fig3)
    # Tabla con % exacto
    st.write("Tabla de mensajes por usuario:")
    user_percentages = 100 * user_counts / user_counts.sum()
    user_table = user_counts.to_frame("Cantidad")
    user_table["%"] = user_percentages.round(1)
    st.dataframe(user_table)
else:
    st.warning("No hay mensajes para mostrar usuarios.")

# --------- Mostrar algunos mensajes filtrados ---------
if not filtered.empty:
    st.subheader("Ejemplo de mensajes filtrados")
    st.write(filtered[["timestamp", "sender", "message"]].head(10))
