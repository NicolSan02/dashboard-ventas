import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv('data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df['Branch'] = df['Branch'].astype(str).str.upper().str.strip()
    return df

df = load_data()

st.title("📊 Dashboard de Ventas - Cadena de Tiendas de Conveniencia")
st.markdown("Este dashboard interactivo permite explorar ventas, comportamiento de clientes y métricas clave del negocio.")

#     filtros
st.sidebar.header("Filtros")
branch = st.sidebar.selectbox("Selecciona una sucursal:", options=sorted(df['Branch'].unique()))
customer_type = st.sidebar.radio("Tipo de cliente:", options=["All", "Member", "Normal"])

if customer_type != "All":
    filtered_df = df[(df['Branch'] == branch) & (df['Customer type'] == customer_type)]
else:
    filtered_df = df[df['Branch'] == branch]


# Sección 0: Evolución de ventas
st.subheader("1️⃣ Evolución de las Ventas Totales")
ventas_diarias = filtered_df.groupby('Date')['Total'].sum()
st.line_chart(ventas_diarias)

# Sección 1: Ingresos por línea de producto
st.subheader("2️⃣ Ingresos Totales por Línea de Producto")
ingresos = filtered_df.groupby('Product line')['Total'].sum().sort_values()
fig1, ax1 = plt.subplots()
sns.barplot(x=ingresos.values, y=ingresos.index, ax=ax1)
st.pyplot(fig1)

# Sección 2: Gasto por tipo de cliente
st.subheader("3️⃣ Gasto Total por Tipo de Cliente")
fig2, ax2 = plt.subplots()
sns.boxplot(data=df, x='Customer type', y='Total', ax=ax2)
st.pyplot(fig2)

# Sección 3: Métodos de pago
st.subheader("4️⃣ Métodos de Pago Preferidos")
payment_counts = filtered_df['Payment'].value_counts()
fig3, ax3 = plt.subplots()
sns.barplot(x=payment_counts.index, y=payment_counts.values, ax=ax3)
ax3.set_ylabel("Cantidad de transacciones")
st.pyplot(fig3)

# Sección 4: Relación entre Costo y Ganancia
st.subheader("5️⃣ Costo vs. Ganancia")
fig4 = px.scatter(filtered_df, x='cogs', y='gross income', color='Product line',
                  title='Relación entre Costo y Ganancia')
st.plotly_chart(fig4)
