import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configuración inicial
st.set_page_config(page_title="Dashboard Financiero - Kairos Flow", layout="wide")
st.title("💼 Sistema Financiero Inteligente - Kairos Flow")
st.markdown("Creado con Python + Datos + Visión 🧠")

# Datos simulados
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

# Filtros
st.sidebar.header("🔎 Filtros")
mes_filtro = st.sidebar.multiselect("Seleccioná mes", options=meses, default=meses)
sucursal_filtro = st.sidebar.multiselect("Sucursal", options=sucursales, default=sucursales)

df_filtrado = df[df['Mes'].isin(mes_filtro) & df['Sucursal'].isin(sucursal_filtro)]

# KPIs
st.markdown("## 📊 Indicadores Generales")
col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Ingresos", f"${df_filtrado['Ingresos'].sum():,.0f}")
col2.metric("📤 Total Egresos", f"${df_filtrado['Egresos'].sum():,.0f}")
col3.metric("📈 Ganancia Neta", f"${df_filtrado['Ganancia'].sum():,.0f}", 
            delta=f"{(df_filtrado['Ganancia'].sum() / df_filtrado['Ingresos'].sum()) * 100:.2f}%")

# Evolución mensual
st.markdown("### 📈 Evolución Mensual de Ganancia Neta")
df_evol = df_filtrado.groupby('Mes')[['Ingresos', 'Egresos', 'Ganancia']].sum().reset_index()
graf = px.line(df_evol, x='Mes', y='Ganancia', markers=True, title="Ganancia Neta por Mes")
st.plotly_chart(graf, use_container_width=True)

# Comparativa entre sucursales
st.markdown("### 🏪 Comparativa entre Sucursales")
df_suc = df_filtrado.groupby('Sucursal')[['Ingresos', 'Egresos', 'Ganancia']].sum().reset_index()
graf2 = px.bar(df_suc, x='Sucursal', y='Ganancia', color='Sucursal', title="Ganancia Neta por Sucursal")
st.plotly_chart(graf2, use_container_width=True)

# Distribución de Egresos
st.markdown("### 🧾 Distribución de Egresos por Rubro")
df_rubro = df_filtrado.groupby('Rubro')['Egresos'].sum().reset_index()
graf3 = px.pie(df_rubro, names='Rubro', values='Egresos', title="Egresos por Categoría")
st.plotly_chart(graf3, use_container_width=True)

# Tabla detallada
st.markdown("### 📋 Detalle de Operaciones")
st.dataframe(df_filtrado.sort_values(by='Mes'), use_container_width=True)

# Panel de insights tipo IA
st.markdown("### 🤖 Recomendaciones Inteligentes")
mayor_ganancia = df_suc.loc[df_suc['Ganancia'].idxmax()]
mayor_egreso = df_suc.loc[df_suc['Egresos'].idxmax()]
recomendacion = f"🔍 Tu sucursal más rentable es **{mayor_ganancia['Sucursal']}** con una ganancia neta de ${mayor_ganancia['Ganancia']:,.0f}.\n\n📌 La sucursal que más gasta es **{mayor_egreso['Sucursal']}**, con egresos por ${mayor_egreso['Egresos']:,.0f}.\n\n💡 Sugerencia: Reducir gastos en esa sede podría mejorar tu margen general hasta un **{(mayor_egreso['Egresos']/df_filtrado['Egresos'].sum()*100):.2f}%**."

st.markdown(recomendacion)

# Footer
st.markdown("---")
st.markdown("Creado por Kairos Flow | Este sistema es solo una demo visual, pero 100% funcional y adaptable 💡")
