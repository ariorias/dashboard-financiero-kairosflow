import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Título principal
st.set_page_config(page_title="Sistema Financiero - Kairos Flow", layout="wide")
st.title("💼 Dashboard Financiero - Kairos Flow")

# Simulación de datos
np.random.seed(42)
meses = pd.date_range("2024-01-01", periods=6, freq='M').strftime('%b-%Y')
sucursales = ['Estación Norte', 'Hotel Central', 'Bar del Sur']
rubros = ['Combustible', 'Hospedaje', 'Gastronomía', 'Mantenimiento', 'Sueldos']

data = []
for mes in meses:
    for suc in sucursales:
        for rubro in rubros:
            ingresos = np.random.randint(300000, 1200000)
            egresos = ingresos * np.random.uniform(0.6, 0.95)
            data.append([mes, suc, rubro, ingresos, egresos])

df = pd.DataFrame(data, columns=['Mes', 'Sucursal', 'Rubro', 'Ingresos', 'Egresos'])
df['Ganancia'] = df['Ingresos'] - df['Egresos']

# KPIs generales
total_ingresos = df['Ingresos'].sum()
total_egresos = df['Egresos'].sum()
ganancia_neta = total_ingresos - total_egresos

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Ingresos", f"${total_ingresos:,.0f}")
col2.metric("📤 Total Egresos", f"${total_egresos:,.0f}")
col3.metric("📈 Ganancia Neta", f"${ganancia_neta:,.0f}", delta=f"{(ganancia_neta/total_ingresos)*100:.2f}%")

# Filtros
st.sidebar.header("🔎 Filtros")
mes_filtro = st.sidebar.multiselect("Seleccioná mes", options=meses, default=meses)
sucursal_filtro = st.sidebar.multiselect("Sucursal", options=sucursales, default=sucursales)

df_filtrado = df[df['Mes'].isin(mes_filtro) & df['Sucursal'].isin(sucursal_filtro)]

# Gráfico de evolución por filtro
st.markdown("### 📊 Evolución de Ingresos y Egresos")

if len(sucursal_filtro) > 1:
    titulo = " (Total consolidado de sucursales seleccionadas)"
elif len(sucursal_filtro) == 1:
    titulo = f" ({sucursal_filtro[0]})"
else:
    titulo = " (Todas las sucursales)"

df_evolucion = df_filtrado.groupby(['Mes'])[['Ingresos', 'Egresos']].sum().reset_index()
grafico = px.line(df_evolucion, x='Mes', y=['Ingresos', 'Egresos'], markers=True,
                  labels={'value': 'Monto', 'variable': 'Concepto'},
                  title=f"Evolución financiera{titulo}")
st.plotly_chart(grafico, use_container_width=True)

# Gráfico por rubro
st.markdown("### 🔍 Detalle por Rubro")
fig_rubro = px.bar(df_filtrado.groupby('Rubro')[['Ingresos', 'Egresos']].sum().reset_index(), 
                   x='Rubro', y=['Ingresos', 'Egresos'], barmode='group')
st.plotly_chart(fig_rubro, use_container_width=True)

# Tabla detallada
st.markdown("### 📋 Tabla Detallada")
st.dataframe(df_filtrado.sort_values(by='Mes'), use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Creado por Kairos Flow | Demo de sistema financiero inteligente con Python 🐍")
