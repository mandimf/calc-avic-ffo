import streamlit as st

st.set_page_config(page_title="Calculadora Integrada: Avicultura & FFO", layout="centered")

st.title("🐔 Calculadora Integrada de Produção")
st.markdown("### Avicultura & Graxaria (FFO)")
st.write("Ajuste as premissas e rendimentos da FFO, e preencha **apenas um** dos campos de entrada de volume para calcular automaticamente toda a cadeia produtiva em cascata.")

# Barra lateral para premissas fixas e rendimentos da FFO editáveis
st.sidebar.header("⚙️ Premissas Fixas Editáveis")
pv_ave = st.sidebar.number_input("Peso Médio Vivo por Ave (kg)", value=3.00, step=0.1)
cr_ave = st.sidebar.number_input("Consumo de Ração por Ave (kg)", value=5.00, step=0.1)
dias_mes = st.sidebar.number_input("Dias Operacionais no Mês", value=25, step=1)
fator_mp = st.sidebar.number_input("Fator MP Bruta (% do Peso Vivo)", value=0.30, step=0.01, format="%.2f")

st.sidebar.divider()
st.sidebar.header("🏭 Rendimentos FFO (% s/ MP Bruta)")
pct_agua = st.sidebar.slider("Água Evaporada (Quebra)", min_value=0.0, max_value=0.8, value=0.523, step=0.005, format="%.3f")
pct_fv = st.sidebar.slider("Farinha de Vísceras (FV)", min_value=0.0, max_value=0.5, value=0.250, step=0.005, format="%.3f")
pct_oleo = st.sidebar.slider("Óleo de Frango", min_value=0.0, max_value=0.3, value=0.127, step=0.005, format="%.3f")
pct_fps = st.sidebar.slider("Farinha de Penas e Sangue (FPS)", min_value=0.0, max_value=0.3, value=0.100, step=0.005, format="%.3f")

st.divider()
st.header("📥 Dados de Entrada (Preencha apenas 1 campo)")
col1, col2, col3 = st.columns(3)

with col1:
    racao_input = st.number_input("Ração Produzida (t/dia)", value=0.0, step=50.0)
with col2:
    abate_input = st.number_input("Abate Diário (aves/dia)", value=0.0, step=10000.0)
with col3:
    mp_input = st.number_input("Matéria-Prima Bruta (t/dia)", value=0.0, step=10.0)

# Lógica de cálculo em cascata
if abate_input > 0:
    abate_dia = abate_input
    racao_dia = (abate_dia * cr_ave) / 1000.0
    mp_dia = (abate_dia * pv_ave / 1000.0) * fator_mp
elif racao_input > 0:
    racao_dia = racao_input
    abate_dia = (racao_dia * 1000.0) / cr_ave
    mp_dia = (abate_dia * pv_ave / 1000.0) * fator_mp
elif mp_input > 0:
    mp_dia = mp_input
    pv_dia_calc = mp_dia / fator_mp
    abate_dia = (pv_dia_calc * 1000.0) / pv_ave
    racao_dia = (abate_dia * cr_ave) / 1000.0
else:
    # Valor padrão inicial caso nenhum seja preenchido
    racao_dia = 1000.0
    abate_dia = (racao_dia * 1000.0) / cr_ave
    mp_dia = (abate_dia * pv_ave / 1000.0) * fator_mp

pv_dia = (abate_dia * pv_ave) / 1000.0

# Balanço de Massa FFO dinâmico com base nos sliders da barra lateral
agua_dia = mp_dia * pct_agua
fv_dia = mp_dia * pct_fv
oleo_dia = mp_dia * pct_oleo
fps_dia = mp_dia * pct_fps
acabado_dia = fv_dia + oleo_dia + fps_dia

st.divider()
st.header("📊 Resultados Calculados")

tab_diario, tab_mensal = st.tabs(["📅 Base Diária", "🗓️ Projeção Mensal"])

with tab_diario:
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Abate Diário", f"{abate_dia:,.0f} aves")
        st.metric("Ração Diária", f"{racao_dia:,.2f} t")
    with col_b:
        st.metric("Peso Vivo Diário", f"{pv_dia:,.2f} t")
        st.metric("MP Bruta FFO Diária", f"{mp_dia:,.2f} t")
    
    st.subheader("Balanço de Massa FFO (Diário)")
    st.write(f"- **Água Evaporada (Quebra):** {agua_dia:,.2f} t *({pct_agua*100:.1f}%)*")
    st.write(f"- **Farinha de Vísceras (FV):** {fv_dia:,.2f} t *({pct_fv*100:.1f}%)*")
    st.write(f"- **Óleo de Frango:** {oleo_dia:,.2f} t *({pct_oleo*100:.1f}%)*")
    st.write(f"- **Farinha de Penas e Sangue (FPS):** {fps_dia:,.2f} t *({pct_fps*100:.1f}%)*")
    st.success(f"**Total de Produtos Acabados FFO:** {acabado_dia:,.2f} t *({(pct_fv+pct_oleo+pct_fps)*100:.1f}%)*")

with tab_mensal:
    col_c, col_d = st.columns(2)
    with col_c:
        st.metric("Abate Mensal", f"{abate_dia * dias_mes:,.0f} aves")
        st.metric("Ração Mensal", f"{racao_dia * dias_mes:,.2f} t")
    with col_d:
        st.metric("Peso Vivo Mensal", f"{pv_dia * dias_mes:,.2f} t")
        st.metric("MP Bruta FFO Mensal", f"{mp_dia * dias_mes:,.2f} t")
        
    st.subheader("Balanço de Massa FFO (Mensal)")
    st.write(f"- **Água Evaporada (Quebra):** {agua_dia * dias_mes:,.2f} t")
    st.write(f"- **Farinha de Vísceras (FV):** {fv_dia * dias_mes:,.2f} t")
    st.write(f"- **Óleo de Frango:** {oleo_dia * dias_mes:,.2f} t")
    st.write(f"- **Farinha de Penas e Sangue (FPS):** {fps_dia * dias_mes:,.2f} t")
    st.success(f"**Total de Produtos Acabados FFO:** {acabado_dia * dias_mes:,.2f} t")
