import streamlit as st

st.set_page_config(page_title="Calculadora Integrada: Avicultura & FFO", layout="centered")

st.title("🐔 Calculadora Integrada de Produção")
st.markdown("### Avicultura & Graxaria (FFO)")
st.write("Ajuste as premissas e os rendimentos da FFO em porcentagem (%), e preencha **apenas um** dos campos de entrada de volume para calcular automaticamente toda a cadeia produtiva.")

# Barra lateral para premissas fixas e rendimentos da FFO com 1 casa decimal
st.sidebar.header("⚙️ Premissas Fixas Editáveis")
pv_ave = st.sidebar.number_input("Peso Médio Vivo por Ave (kg)", value=3.0, step=0.1, format="%.1f")
cr_ave = st.sidebar.number_input("Consumo de Ração por Ave (kg)", value=5.0, step=0.1, format="%.1f")
dias_mes = st.sidebar.number_input("Dias Operacionais no Mês", value=25, step=1)
fator_mp_pct = st.sidebar.number_input("Fator MP Bruta (% do Peso Vivo)", value=30.0, step=0.5, format="%.1f")
fator_mp = fator_mp_pct / 100.0

st.sidebar.divider()
st.sidebar.header("🏭 Rendimentos FFO (% s/ MP Bruta)")
pct_agua_val = st.sidebar.number_input("Água Evaporada (Quebra) [%]", value=52.3, step=0.1, format="%.1f")
pct_fv_val = st.sidebar.number_input("Farinha de Vísceras (FV) [%]", value=25.0, step=0.1, format="%.1f")
pct_oleo_val = st.sidebar.number_input("Óleo de Frango [%]", value=12.7, step=0.1, format="%.1f")
pct_fps_val = st.sidebar.number_input("Farinha de Penas e Sangue (FPS) [%]", value=10.0, step=0.1, format="%.1f")

# Conversão para proporção interna
pct_agua = pct_agua_val / 100.0
pct_fv = pct_fv_val / 100.0
pct_oleo = pct_oleo_val / 100.0
pct_fps = pct_fps_val / 100.0

st.divider()
st.header("📥 Dados de Entrada (Preencha apenas 1 campo)")
col1, col2, col3 = st.columns(3)

with col1:
    racao_input = st.number_input("Ração Produzida (t/dia)", value=0.0, step=10.0, format="%.1f")
with col2:
    abate_input = st.number_input("Abate Diário (aves/dia)", value=0.0, step=1000.0, format="%.1f")
with col3:
    mp_input = st.number_input("Matéria-Prima Bruta (t/dia)", value=0.0, step=10.0, format="%.1f")

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
    abate_dia = 0.0
    racao_dia = 0.0
    mp_dia = 0.0

pv_dia = (abate_dia * pv_ave) / 1000.0

# Balanço de Massa FFO dinâmico
agua_dia = mp_dia * pct_agua
fv_dia = mp_dia * pct_fv
oleo_dia = mp_dia * pct_oleo
fps_dia = mp_dia * pct_fps
acabado_dia = fv_dia + oleo_dia + fps_dia

st.divider()
st.header("📊 Resultados Calculados")

if abate_dia == 0 and racao_dia == 0 and mp_dia == 0:
    st.info("ℹ️ Insira um valor em um dos campos de 'Dados de Entrada' acima para gerar os cálculos.")
else:
    tab_diario, tab_mensal = st.tabs(["📅 Base Diária", "🗓️ Projeção Mensal"])

    with tab_diario:
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Abate Diário", f"{abate_dia:,.1f} aves")
            st.metric("Ração Diária", f"{racao_dia:,.1f} t")
        with col_b:
            st.metric("Peso Vivo Diário", f"{pv_dia:,.1f} t")
            st.metric("MP Bruta FFO Diária", f"{mp_dia:,.1f} t")
        
        st.subheader("Balanço de Massa FFO (Diário)")
        st.write(f"- **Água Evaporada (Quebra):** {agua_dia:,.1f} t *({pct_agua_val:.1f}%)*")
        st.write(f"- **Farinha de Vísceras (FV):** {fv_dia:,.1f} t *({pct_fv_val:.1f}%)*")
        st.write(f"- **Óleo de Frango:** {oleo_dia:,.1f} t *({pct_oleo_val:.1f}%)*")
        st.write(f"- **Farinha de Penas e Sangue (FPS):** {fps_dia:,.1f} t *({pct_fps_val:.1f}%)*")
        st.success(f"**Total de Produtos Acabados FFO:** {acabado_dia:,.1f} t *({(pct_fv_val+pct_oleo_val+pct_fps_val):.1f}%)*")

    with tab_mensal:
        col_c, col_d = st.columns(2)
        with col_c:
            st.metric("Abate Mensal", f"{abate_dia * dias_mes:,.1f} aves")
            st.metric("Ração Mensal", f"{racao_dia * dias_mes:,.1f} t")
        with col_d:
            st.metric("Peso Vivo Mensal", f"{pv_dia * dias_mes:,.1f} t")
            st.metric("MP Bruta FFO Mensal", f"{mp_dia * dias_mes:,.1f} t")
            
        st.subheader("Balanço de Massa FFO (Mensal)")
        st.write(f"- **Água Evaporada (Quebra):** {agua_dia * dias_mes:,.1f} t")
        st.write(f"- **Farinha de Vísceras (FV):** {fv_dia * dias_mes:,.1f} t")
        st.write(f"- **Óleo de Frango:** {oleo_dia * dias_mes:,.1f} t")
        st.write(f"- **Farinha de Penas e Sangue (FPS):** {fps_dia * dias_mes:,.1f} t")
        st.success(f"**Total de Produtos Acabados FFO:** {acabado_dia * dias_mes:,.1f} t")
