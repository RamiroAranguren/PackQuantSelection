
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import yfinance as yf
from datetime import date

px.defaults.template = "plotly_white"


st.set_page_config(
    page_title="Quant Selection – Calculadora",
    page_icon="📈",
    layout="wide",
)


# ============================================================
# Estilo visual tipo Balanz / institucional
# ============================================================

BALANZ_CSS = """
<style>
:root {
    --bg: #f5f7fb;
    --panel: #ffffff;
    --navy: #071a33;
    --navy-2: #0d2747;
    --blue: #0068b5;
    --cyan: #26a7df;
    --gold: #c9a44b;
    --text: #162033;
    --muted: #6b7280;
    --border: #d8e1ee;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(0, 104, 181, 0.12), transparent 28%),
        linear-gradient(180deg, #f7f9fc 0%, #eef3f9 100%);
    color: var(--text);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--navy) 0%, #0a1424 100%);
}

[data-testid="stSidebar"] * {
    color: #eef6ff !important;
}

[data-testid="stSidebar"] input,
[data-testid="stSidebar"] textarea,
[data-testid="stSidebar"] select {
    color: #101828 !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #101828 !important;
}

h1, h2, h3 {
    color: var(--navy);
    letter-spacing: -0.02em;
}

.block-container {
    padding-top: 1.4rem;
    padding-bottom: 3rem;
    max-width: 1280px;
}

.balanz-hero {
    background: linear-gradient(135deg, var(--navy) 0%, var(--navy-2) 58%, #0b5f96 100%);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 22px;
    padding: 24px 28px;
    margin-bottom: 22px;
    box-shadow: 0 16px 40px rgba(7, 26, 51, 0.18);
}

.balanz-eyebrow {
    color: var(--gold);
    text-transform: uppercase;
    font-size: 0.78rem;
    letter-spacing: 0.12em;
    font-weight: 700;
    margin-bottom: 6px;
}

.balanz-title {
    color: white;
    font-size: 2.0rem;
    font-weight: 750;
    line-height: 1.08;
    margin: 0;
}

.balanz-subtitle {
    color: rgba(255,255,255,0.78);
    font-size: 0.98rem;
    margin-top: 8px;
    max-width: 900px;
}

.balanz-badge {
    display: inline-block;
    color: #d8f3ff;
    border: 1px solid rgba(216,243,255,0.28);
    border-radius: 999px;
    padding: 5px 10px;
    font-size: 0.78rem;
    margin-top: 14px;
    margin-right: 6px;
    background: rgba(255,255,255,0.06);
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.88);
    border: 1px solid var(--border);
    border-left: 5px solid var(--blue);
    border-radius: 16px;
    padding: 14px 16px;
    box-shadow: 0 8px 22px rgba(9, 32, 68, 0.08);
}

[data-testid="stMetricLabel"] {
    color: var(--muted);
    font-weight: 650;
}

[data-testid="stMetricValue"] {
    color: var(--navy);
    font-weight: 780;
}

.stDataFrame, [data-testid="stTable"] {
    background: var(--panel);
    border-radius: 16px;
}

div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.75);
    border: 1px solid var(--border);
    border-radius: 14px;
}

.stButton button, .stDownloadButton button {
    background: linear-gradient(135deg, var(--blue), var(--cyan));
    color: white !important;
    border: 0;
    border-radius: 12px;
    font-weight: 700;
    box-shadow: 0 8px 18px rgba(0, 104, 181, 0.22);
}

.stButton button:hover, .stDownloadButton button:hover {
    border: 0;
    filter: brightness(1.03);
    transform: translateY(-1px);
}

hr {
    border-color: rgba(216,225,238,0.8);
}

.small-note {
    color: var(--muted);
    font-size: 0.88rem;
}

/* Inputs legibles en sidebar oscuro */
[data-testid="stSidebar"] .stNumberInput input,
[data-testid="stSidebar"] .stDateInput input,
[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] input {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
    border: 1px solid rgba(216,225,238,0.95) !important;
    border-radius: 10px !important;
    caret-color: #0068B5 !important;
}

[data-testid="stSidebar"] [data-baseweb="input"],
[data-testid="stSidebar"] [data-baseweb="base-input"],
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border-radius: 10px !important;
}

[data-testid="stSidebar"] [data-baseweb="input"] *,
[data-testid="stSidebar"] [data-baseweb="base-input"] *,
[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
}

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown p {
    color: #F8FAFC !important;
}

[data-testid="stSidebar"] .stCheckbox label span {
    color: #F8FAFC !important;
}

/* Plotly claro, aunque el browser / Streamlit intente usar dark mode */
.js-plotly-plot,
.plot-container,
.svg-container {
    background: #FFFFFF !important;
}

[data-testid="stPlotlyChart"] {
    background: #FFFFFF !important;
    border: 1px solid #D8E1EE;
    border-radius: 16px;
    padding: 10px;
    box-shadow: 0 8px 24px rgba(9, 32, 68, 0.07);
}

/* Cards más prolijas y sin truncamiento agresivo */
[data-testid="stMetric"] {
    min-height: 118px;
}

[data-testid="stMetricValue"] {
    font-size: 1.65rem !important;
    line-height: 1.15 !important;
    white-space: nowrap !important;
}

[data-testid="stMetricDelta"] {
    font-size: 0.92rem !important;
}

/* Alertas menos saturadas */
[data-testid="stAlert"] {
    border-radius: 14px;
}

/* Tablas */
[data-testid="stDataFrame"] {
    border: 1px solid #D8E1EE;
    border-radius: 14px;
    overflow: hidden;
}

/* Compactar el bloque superior en pantallas chicas */
@media (max-width: 1100px) {
    .balanz-title { font-size: 1.55rem; }
    [data-testid="stMetricValue"] { font-size: 1.35rem !important; }
}

</style>
"""

def apply_style():
    st.markdown(BALANZ_CSS, unsafe_allow_html=True)

def render_brand_header(title: str, subtitle: str, badges=None):
    badges = badges or []
    badges_html = "".join([f'<span class="balanz-badge">{b}</span>' for b in badges])
    st.markdown(
        f"""
        <div class="balanz-hero">
            <div class="balanz-eyebrow">Quant Selection</div>
            <div class="balanz-title">{title}</div>
            <div class="balanz-subtitle">{subtitle}</div>
            <div>{badges_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


apply_style()

def fmt_usd(value: float) -> str:
    """Formato compacto para cards de métricas, evitando truncamiento visual."""
    value = float(value)
    if abs(value) >= 1_000_000:
        return f"USD {value/1_000_000:,.2f}M"
    if abs(value) >= 100_000:
        return f"USD {value/1_000:,.1f}K"
    return f"USD {value:,.0f}"

def style_plotly(fig):
    """Estilo claro/institucional para evitar fondos oscuros por default theme."""
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(color="#162033", size=13),
        title=dict(font=dict(color="#071A33", size=20)),
        legend=dict(
            bgcolor="rgba(255,255,255,0.92)",
            bordercolor="#D8E1EE",
            borderwidth=1,
            font=dict(color="#162033"),
        ),
        margin=dict(l=44, r=30, t=55, b=45),
        hovermode="x unified",
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor="#E8EEF7",
        linecolor="#C7D3E3",
        tickfont=dict(color="#334155"),
        title_font=dict(color="#334155"),
        zeroline=False,
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="#E8EEF7",
        linecolor="#C7D3E3",
        tickfont=dict(color="#334155"),
        title_font=dict(color="#334155"),
        zeroline=False,
    )
    fig.update_traces(line=dict(width=2.4))
    return fig

# ============================================================
# Configuración del pack
# ============================================================

REBALANCES = [
    {
        "name": "1Q25",
        "start": "2025-01-08",
        "weights": {
            "ABBV": 0.035, "AVGO": 0.055, "COST": 0.20, "LLY": 0.25,
            "NVDA": 0.20, "ORCL": 0.05, "TMUS": 0.12, "WMT": 0.09,
        },
    },
    {
        "name": "2Q25",
        "start": "2025-04-08",
        "weights": {
            "ABBV": 0.13, "COST": 0.19, "GE": 0.05, "IBM": 0.05,
            "LLY": 0.25, "NVDA": 0.20, "PM": 0.07, "TMUS": 0.06,
        },
    },
    {
        "name": "3Q25",
        "start": "2025-07-08",
        "weights": {
            "GE": 0.11, "IBM": 0.13, "JPM": 0.06,
            "NVDA": 0.25, "PM": 0.20, "WMT": 0.25,
        },
    },
    {
        "name": "4Q25",
        "start": "2025-10-01",
        "weights": {
            "PM": 0.12, "NVDA": 0.30, "IBM": 0.10,
            "GE": 0.16, "JPM": 0.11, "VST": 0.21,
        },
    },
    {
        "name": "1Q26",
        "start": "2026-01-05",
        "weights": {
            "GE": 0.12, "RTX": 0.07, "WFC": 0.06, "CAT": 0.12,
            "NVDA": 0.18, "WMT": 0.15, "GOOGL": 0.20, "IBM": 0.10,
        },
    },
    {
        "name": "2Q26",
        "start": "2026-03-31",
        "weights": {
            "AVGO": 0.166, "CVX": 0.144, "GE": 0.152,
            "GILD": 0.195, "KO": 0.143, "WMT": 0.20,
        },
    },
    {
        "name": "3Q26",
        "start": "2026-07-08",
        "weights": {
            "GE": 0.289, "RTX": 0.186, "MU": 0.167,
            "CSCO": 0.143, "CAT": 0.113, "GS": 0.101,
        },
    },
]


# ============================================================
# Utilidades
# ============================================================

def all_pack_tickers(rebalances):
    return sorted({t for r in rebalances for t in r["weights"].keys()})


def normalize_weights(weights):
    total = sum(weights.values())
    if total == 0:
        raise ValueError("La suma de ponderaciones es cero.")
    return {k: v / total for k, v in weights.items()}


def first_trading_on_or_after(index, dt):
    pos = index.searchsorted(dt)
    if pos >= len(index):
        raise ValueError(f"No hay precios disponibles en o después de {dt.date()}.")
    return index[pos]


def last_trading_on_or_before(index, dt):
    pos = index.searchsorted(dt, side="right") - 1
    if pos < 0:
        raise ValueError(f"No hay precios disponibles en o antes de {dt.date()}.")
    return index[pos]


@st.cache_data(ttl=60 * 60)
def download_prices(tickers, start, end, adjusted):
    end_dt = pd.Timestamp(end) + pd.Timedelta(days=5)

    data = yf.download(
        tickers=tickers,
        start=start,
        end=end_dt.strftime("%Y-%m-%d"),
        auto_adjust=adjusted,
        progress=False,
        group_by="column",
        threads=True,
    )

    if data.empty:
        raise ValueError("No se pudieron descargar precios.")

    # adjusted=True  -> auto_adjust=True: yfinance devuelve "Close" ya ajustado.
    # adjusted=False -> auto_adjust=False: se usa "Close" crudo.
    if isinstance(data.columns, pd.MultiIndex):
        prices = data["Close"].copy()
    else:
        prices = data[["Close"]].copy()
        prices.columns = tickers[:1]

    prices.index = pd.to_datetime(prices.index)
    prices = prices.sort_index().ffill()

    return prices


def build_effective_rebalances(prices, rebalances):
    out = []
    for r in rebalances:
        start = pd.Timestamp(r["start"])
        if start > prices.index.max():
            continue
        eff = first_trading_on_or_after(prices.index, start)
        out.append({
            "name": r["name"],
            "scheduled_start": start,
            "effective_start": eff,
            "weights": normalize_weights(r["weights"]),
        })
    return out


def calculate_client_series(prices, rebalances, benchmark, entry_date, valuation_date, amount):
    entry_eff = first_trading_on_or_after(prices.index, entry_date)
    valuation_eff = last_trading_on_or_before(prices.index, valuation_date)

    if entry_eff > valuation_eff:
        raise ValueError("La fecha de entrada efectiva es posterior a la fecha de valuación.")

    effective_rebalances = build_effective_rebalances(prices, rebalances)
    rb_dates = [r["effective_start"] for r in effective_rebalances]

    current_idx = max([i for i, d in enumerate(rb_dates) if d <= entry_eff], default=None)
    if current_idx is None:
        raise ValueError("La fecha de entrada es anterior al primer rebalanceo efectivo.")

    current_rb = effective_rebalances[current_idx]
    weights = current_rb["weights"]
    tickers = [t for t in weights if t in prices.columns]

    if not tickers:
        raise ValueError("No hay tickers válidos para la composición vigente.")

    missing = [t for t in weights if t not in prices.columns]
    if missing:
        st.warning(f"Tickers sin precio y excluidos: {', '.join(missing)}")

    # Regla clave:
    # En el rebalanceo se define una cantidad modelo de acciones con capital base 1.
    # Si el cliente entra después, compra esa canasta ya drifted, escalada a su monto.
    reb_price_date = current_rb["effective_start"]
    model_weights = pd.Series(weights)[tickers]
    model_weights = model_weights / model_weights.sum()
    model_shares = model_weights / prices.loc[reb_price_date, tickers]

    model_value_entry = float((model_shares * prices.loc[entry_eff, tickers]).sum())
    holdings = model_shares * (amount / model_value_entry)

    future_rebalances = {
        r["effective_start"]: r
        for r in effective_rebalances
        if entry_eff < r["effective_start"] <= valuation_eff
    }

    dates = prices.loc[(prices.index >= entry_eff) & (prices.index <= valuation_eff)].index
    if len(dates) == 0:
        raise ValueError("No hay fechas de precios en el rango indicado.")

    values = []
    pnl_by_ticker = {}

    prev_date = dates[0]
    prev_prices = prices.loc[prev_date]
    value = float((holdings * prev_prices[holdings.index]).sum())
    values.append((prev_date, value))

    for d in dates[1:]:
        cur_prices = prices.loc[d]

        for t in holdings.index:
            pnl = float(holdings[t] * (cur_prices[t] - prev_prices[t]))
            pnl_by_ticker[t] = pnl_by_ticker.get(t, 0.0) + pnl

        value = float((holdings * cur_prices[holdings.index]).sum())
        values.append((d, value))

        # Rebalanceo al cierre: afecta el tramo siguiente.
        if d in future_rebalances:
            rb = future_rebalances[d]
            rb_weights = rb["weights"]
            rb_tickers = [t for t in rb_weights if t in prices.columns]
            w = pd.Series(rb_weights)[rb_tickers]
            w = w / w.sum()
            holdings = (value * w / cur_prices[rb_tickers]).astype(float)

        prev_date = d
        prev_prices = cur_prices

    pack_series = pd.Series(dict(values)).sort_index()
    pack_series.name = "Quant Selection"

    if benchmark not in prices.columns:
        raise ValueError(f"No encontré el benchmark {benchmark}.")
    bench = prices.loc[pack_series.index, benchmark]
    benchmark_series = amount * bench / bench.iloc[0]
    benchmark_series.name = benchmark

    final_prices = prices.loc[valuation_eff, holdings.index]
    final_values = holdings * final_prices
    holdings_df = pd.DataFrame({
        "Ticker": holdings.index,
        "Acciones": holdings.values,
        "Precio": final_prices.values,
        "Valor": final_values.values,
        "Peso actual": final_values.values / final_values.sum(),
    }).sort_values("Valor", ascending=False)

    attribution_df = pd.DataFrame({
        "Ticker": list(pnl_by_ticker.keys()),
        "P&L": list(pnl_by_ticker.values()),
    })
    if not attribution_df.empty:
        attribution_df["Aporte sobre capital inicial"] = attribution_df["P&L"] / amount
        attribution_df = attribution_df.sort_values("Aporte sobre capital inicial", ascending=False)

    return {
        "entry_effective": entry_eff,
        "valuation_effective": valuation_eff,
        "pack_series": pack_series,
        "benchmark_series": benchmark_series,
        "holdings": holdings_df,
        "attribution": attribution_df,
    }


def build_equal_weight_cumulative_rebalances(rebalances):
    """
    Pack equal weight:
    - Arranca con los tickers del primer rebalanceo.
    - En cada rebalanceo real, suma los tickers nuevos que aparecieron.
    - Repondera todo el universo acumulado en partes iguales.
    """
    universe = []
    out = []

    for r in rebalances:
        for t in r["weights"].keys():
            if t not in universe:
                universe.append(t)

        n = len(universe)
        ew = {t: 1 / n for t in universe}

        out.append({
            "name": f"{r['name']} Equal Weight",
            "start": r["start"],
            "weights": ew,
        })

    return out


def calc_metrics(pack_series, bench_series, rf_annual=0.0):
    pack_ret = pack_series.pct_change().dropna()
    bench_ret = bench_series.pct_change().dropna()

    aligned = pd.concat([pack_ret, bench_ret], axis=1).dropna()
    aligned.columns = ["pack", "bench"]

    def annualized_return(rets):
        if len(rets) == 0:
            return np.nan
        return (1 + rets).prod() ** (252 / len(rets)) - 1

    def annualized_vol(rets):
        return rets.std(ddof=1) * np.sqrt(252)

    def sharpe(rets):
        vol = annualized_vol(rets)
        if vol == 0 or np.isnan(vol):
            return np.nan
        rf_daily = (1 + rf_annual) ** (1 / 252) - 1
        return ((rets - rf_daily).mean() * 252) / vol

    def max_drawdown(series):
        return (series / series.cummax() - 1).min()

    cov = np.cov(aligned["pack"], aligned["bench"], ddof=1)[0, 1] if len(aligned) > 1 else np.nan
    var = np.var(aligned["bench"], ddof=1) if len(aligned) > 1 else np.nan
    beta = cov / var if var not in [0, np.nan] and var != 0 else np.nan

    alpha_daily = aligned["pack"].mean() - beta * aligned["bench"].mean() if not np.isnan(beta) else np.nan
    alpha_annual = (1 + alpha_daily) ** 252 - 1 if not np.isnan(alpha_daily) else np.nan

    active = aligned["pack"] - aligned["bench"]
    tracking_error = annualized_vol(active)
    information_ratio = (active.mean() * 252) / tracking_error if tracking_error and not np.isnan(tracking_error) else np.nan

    rows = [
        ("Retorno acumulado", pack_series.iloc[-1] / pack_series.iloc[0] - 1, bench_series.iloc[-1] / bench_series.iloc[0] - 1),
        ("Retorno anualizado", annualized_return(pack_ret), annualized_return(bench_ret)),
        ("Volatilidad anualizada", annualized_vol(pack_ret), annualized_vol(bench_ret)),
        ("Sharpe", sharpe(pack_ret), sharpe(bench_ret)),
        ("Máx. drawdown", max_drawdown(pack_series), max_drawdown(bench_series)),
        ("Mejor día", pack_ret.max(), bench_ret.max()),
        ("Peor día", pack_ret.min(), bench_ret.min()),
        ("Beta vs benchmark", beta, np.nan),
        ("Alpha anualizada", alpha_annual, np.nan),
        ("Tracking error", tracking_error, np.nan),
        ("Information ratio", information_ratio, np.nan),
        ("Correlación", aligned["pack"].corr(aligned["bench"]), np.nan),
        ("% días supera benchmark", (aligned["pack"] > aligned["bench"]).mean(), np.nan),
    ]
    return pd.DataFrame(rows, columns=["Métrica", "Pack", "Benchmark"])


def format_metrics(df):
    out = df.copy()
    pct_metrics = {
        "Retorno acumulado", "Retorno anualizado", "Volatilidad anualizada",
        "Máx. drawdown", "Mejor día", "Peor día", "Alpha anualizada",
        "Tracking error", "% días supera benchmark",
    }
    for col in ["Pack", "Benchmark"]:
        out[col] = out.apply(
            lambda r: "" if pd.isna(r[col])
            else f"{r[col] * 100:.2f}%" if r["Métrica"] in pct_metrics
            else f"{r[col]:.2f}",
            axis=1,
        )
    return out


def build_comparison_table(series_dict, rf_annual=0.0):
    rows = []
    for name, s in series_dict.items():
        rets = s.pct_change().dropna()
        if len(rets) == 0:
            continue

        ann_ret = (1 + rets).prod() ** (252 / len(rets)) - 1
        vol = rets.std(ddof=1) * np.sqrt(252)
        rf_daily = (1 + rf_annual) ** (1 / 252) - 1
        sharpe = ((rets - rf_daily).mean() * 252) / vol if vol != 0 else np.nan
        dd = (s / s.cummax() - 1).min()

        rows.append({
            "Serie": name,
            "Retorno acumulado": s.iloc[-1] / s.iloc[0] - 1,
            "Retorno anualizado": ann_ret,
            "Volatilidad anualizada": vol,
            "Sharpe": sharpe,
            "Máx. drawdown": dd,
            "Valor final": s.iloc[-1],
        })

    return pd.DataFrame(rows)


def format_comparison_table(df):
    out = df.copy()
    pct_cols = ["Retorno acumulado", "Retorno anualizado", "Volatilidad anualizada", "Máx. drawdown"]
    for c in pct_cols:
        out[c] = out[c].map(lambda x: "" if pd.isna(x) else f"{x*100:.2f}%")
    out["Sharpe"] = out["Sharpe"].map(lambda x: "" if pd.isna(x) else f"{x:.2f}")
    out["Valor final"] = out["Valor final"].map(lambda x: "" if pd.isna(x) else f"{x:,.2f}")
    return out


# ============================================================
# Páginas
# ============================================================

page = st.sidebar.radio(
    "Sección",
    ["Calculadora por cliente", "Fun"],
)

if page == "Calculadora por cliente":
    render_brand_header(
        "Calculadora por cliente",
        "Performance, riesgo y atribución según fecha de entrada, respetando rebalanceos discretos y cantidades fijas dentro de cada tramo.",
        ["Base 100", "SPY benchmark", "Atribución", "Riesgo"]
    )

    with st.sidebar:
        st.header("Parámetros")

        amount = st.number_input("Monto invertido (USD)", min_value=100.0, value=10000.0, step=1000.0, format="%.0f")
        entry = st.date_input("Fecha de entrada", value=date(2026, 1, 5), min_value=date(2025, 1, 8))
        valuation = st.date_input("Fecha de valuación", value=date.today(), min_value=date(2025, 1, 8))
        benchmark = st.text_input("Benchmark", value="SPY").upper().strip()

        rf_annual = st.number_input(
            "Tasa libre de riesgo anual para Sharpe",
            min_value=0.0, max_value=0.30, value=0.0, step=0.005, format="%.3f",
        )

        adjusted = st.checkbox(
            "Usar precios ajustados (aprox. total return)",
            value=True,
            help="Sirve como aproximación a retorno total. Para producción conviene validar con fuente profesional.",
        )

        st.divider()
        st.write("**Rebalanceos cargados**")
        st.dataframe(
            pd.DataFrame({
                "Trimestre": [r["name"] for r in REBALANCES],
                "Inicio": [r["start"] for r in REBALANCES],
                "Tickers": [", ".join(r["weights"].keys()) for r in REBALANCES],
            }),
            hide_index=True,
            use_container_width=True,
        )

    try:
        required_tickers = sorted(set(all_pack_tickers(REBALANCES) + [benchmark]))
        download_start = (pd.Timestamp(REBALANCES[0]["start"]) - pd.Timedelta(days=10)).strftime("%Y-%m-%d")
        download_end = pd.Timestamp(valuation).strftime("%Y-%m-%d")

        prices = download_prices(required_tickers, download_start, download_end, adjusted)

        result = calculate_client_series(
            prices=prices,
            rebalances=REBALANCES,
            benchmark=benchmark,
            entry_date=pd.Timestamp(entry),
            valuation_date=pd.Timestamp(valuation),
            amount=float(amount),
        )

        pack_series = result["pack_series"]
        bench_series = result["benchmark_series"]
        metrics = calc_metrics(pack_series, bench_series, rf_annual=float(rf_annual))

        st.success(
            f"Fecha de entrada efectiva: {result['entry_effective'].date()} | "
            f"Fecha de valuación efectiva: {result['valuation_effective'].date()}"
        )

        col1, col2, col3, col4 = st.columns(4)
        pack_return = pack_series.iloc[-1] / pack_series.iloc[0] - 1
        bench_return = bench_series.iloc[-1] / bench_series.iloc[0] - 1

        col1.metric("Valor actual pack", fmt_usd(pack_series.iloc[-1]), f"{pack_return*100:.2f}%")
        col2.metric(f"Valor {benchmark}", fmt_usd(bench_series.iloc[-1]), f"{bench_return*100:.2f}%")
        col3.metric("Diferencia vs benchmark", f"{(pack_return-bench_return)*100:.2f} pp")
        col4.metric("Monto inicial", fmt_usd(amount))

        st.subheader("Evolución base 100")
        plot_df = pd.DataFrame({
            "Quant Selection": pack_series / pack_series.iloc[0] * 100,
            benchmark: bench_series / bench_series.iloc[0] * 100,
        })
        fig = px.line(
            plot_df,
            x=plot_df.index,
            y=plot_df.columns,
            labels={"value": "Índice base 100", "index": "Fecha", "variable": "Serie"},
        )
        fig = style_plotly(fig)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Métricas")
        st.dataframe(format_metrics(metrics), hide_index=True, use_container_width=True)

        st.subheader("Atribución por acción")
        attr = result["attribution"].copy()
        if not attr.empty:
            attr["Aporte sobre capital inicial (%)"] = attr["Aporte sobre capital inicial"] * 100
            attr_chart = attr.sort_values("Aporte sobre capital inicial (%)", ascending=False)

            fig_attr = px.bar(
                attr_chart,
                x="Ticker",
                y="Aporte sobre capital inicial (%)",
                labels={"Aporte sobre capital inicial (%)": "Aporte (pp)"},
            )
            fig_attr = style_plotly(fig_attr)
            fig_attr.update_traces(marker_color="#0068B5")
            st.plotly_chart(fig_attr, use_container_width=True)

            st.dataframe(
                attr_chart[["Ticker", "P&L", "Aporte sobre capital inicial (%)"]],
                hide_index=True,
                use_container_width=True,
            )
        else:
            st.info("No hay atribución disponible para este período.")

        st.subheader("Tenencia actual")
        holdings = result["holdings"].copy()
        holdings["Peso actual"] = holdings["Peso actual"] * 100
        st.dataframe(holdings, hide_index=True, use_container_width=True)

        st.subheader("Descargas")
        export_series = pd.DataFrame({
            "Fecha": pack_series.index,
            "Quant Selection": pack_series.values,
            benchmark: bench_series.values,
        })

        st.download_button(
            "Descargar serie diaria CSV",
            data=export_series.to_csv(index=False).encode("utf-8"),
            file_name="quant_selection_serie_diaria.csv",
            mime="text/csv",
        )

        st.download_button(
            "Descargar métricas CSV",
            data=metrics.to_csv(index=False).encode("utf-8"),
            file_name="quant_selection_metricas.csv",
            mime="text/csv",
        )

    except Exception as e:
        st.error(f"No se pudo calcular la cartera: {e}")


if page == "Fun":
    render_brand_header(
        "Fun · Estrategias alternativas",
        "Pruebas comparativas sobre el universo del Quant Selection para entender sensibilidad, construcción y concentración.",
        ["Equal weight", "Universo acumulado", "Comparativo"]
    )

    with st.sidebar:
        st.header("Parámetros Fun")

        strategy = st.selectbox(
            "Estrategia",
            ["Pack equal weight"],
        )

        amount_fun = st.number_input(
            "Capital base (USD)",
            min_value=100.0,
            value=10000.0,
            step=1000.0,
            format="%.0f",
            key="fun_amount",
        )

        start_fun = st.date_input(
            "Fecha de inicio",
            value=date(2025, 1, 8),
            min_value=date(2025, 1, 8),
            key="fun_start",
        )

        valuation_fun = st.date_input(
            "Fecha de valuación",
            value=date.today(),
            min_value=date(2025, 1, 8),
            key="fun_valuation",
        )

        benchmark_fun = st.text_input("Benchmark Fun", value="SPY").upper().strip()

        rf_fun = st.number_input(
            "Tasa libre de riesgo anual",
            min_value=0.0,
            max_value=0.30,
            value=0.0,
            step=0.005,
            format="%.3f",
            key="fun_rf",
        )

        adjusted_fun = st.checkbox(
            "Usar precios ajustados",
            value=True,
            key="fun_adjusted",
        )

    try:
        ew_rebalances = build_equal_weight_cumulative_rebalances(REBALANCES)

        required_tickers = sorted(set(all_pack_tickers(REBALANCES) + [benchmark_fun]))
        download_start = (pd.Timestamp(REBALANCES[0]["start"]) - pd.Timedelta(days=10)).strftime("%Y-%m-%d")
        download_end = pd.Timestamp(valuation_fun).strftime("%Y-%m-%d")

        prices = download_prices(required_tickers, download_start, download_end, adjusted_fun)

        real_result = calculate_client_series(
            prices=prices,
            rebalances=REBALANCES,
            benchmark=benchmark_fun,
            entry_date=pd.Timestamp(start_fun),
            valuation_date=pd.Timestamp(valuation_fun),
            amount=float(amount_fun),
        )

        ew_result = calculate_client_series(
            prices=prices,
            rebalances=ew_rebalances,
            benchmark=benchmark_fun,
            entry_date=pd.Timestamp(start_fun),
            valuation_date=pd.Timestamp(valuation_fun),
            amount=float(amount_fun),
        )

        real_series = real_result["pack_series"].rename("Quant Selection real")
        ew_series = ew_result["pack_series"].rename("Pack equal weight")
        bench_series = real_result["benchmark_series"].rename(benchmark_fun)

        aligned_index = real_series.index.intersection(ew_series.index).intersection(bench_series.index)
        real_series = real_series.loc[aligned_index]
        ew_series = ew_series.loc[aligned_index]
        bench_series = bench_series.loc[aligned_index]

        st.subheader("Pack equal weight")
        st.markdown(
            """
            **Metodología:** se usan todas las compañías que alguna vez formaron parte del pack hasta cada fecha de rebalanceo.
            En cada rebalanceo real, se suman los tickers nuevos al universo acumulado y se pondera todo en partes iguales.
            Entre rebalanceos, las cantidades quedan fijas.
            """
        )

        col1, col2, col3 = st.columns(3)
        ew_ret = ew_series.iloc[-1] / ew_series.iloc[0] - 1
        real_ret = real_series.iloc[-1] / real_series.iloc[0] - 1
        bench_ret = bench_series.iloc[-1] / bench_series.iloc[0] - 1

        col1.metric("Equal weight", fmt_usd(ew_series.iloc[-1]), f"{ew_ret*100:.2f}%")
        col2.metric("Pack real", fmt_usd(real_series.iloc[-1]), f"{real_ret*100:.2f}%")
        col3.metric(benchmark_fun, fmt_usd(bench_series.iloc[-1]), f"{bench_ret*100:.2f}%")

        st.subheader("Evolución base 100")
        comp_df = pd.DataFrame({
            "Pack equal weight": ew_series / ew_series.iloc[0] * 100,
            "Quant Selection real": real_series / real_series.iloc[0] * 100,
            benchmark_fun: bench_series / bench_series.iloc[0] * 100,
        })
        fig = px.line(
            comp_df,
            x=comp_df.index,
            y=comp_df.columns,
            labels={"value": "Índice base 100", "index": "Fecha", "variable": "Serie"},
        )
        fig = style_plotly(fig)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Métricas comparativas")
        comparison = build_comparison_table(
            {
                "Pack equal weight": ew_series,
                "Quant Selection real": real_series,
                benchmark_fun: bench_series,
            },
            rf_annual=float(rf_fun),
        )
        st.dataframe(format_comparison_table(comparison), hide_index=True, use_container_width=True)

        st.subheader("Universo acumulado por rebalanceo")
        rows = []
        for r in ew_rebalances:
            rows.append({
                "Rebalanceo": r["name"].replace(" Equal Weight", ""),
                "Inicio": r["start"],
                "Cantidad de acciones": len(r["weights"]),
                "Universo": ", ".join(r["weights"].keys()),
            })
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

        st.subheader("Tenencia actual equal weight")
        holdings = ew_result["holdings"].copy()
        holdings["Peso actual"] = holdings["Peso actual"] * 100
        st.dataframe(holdings, hide_index=True, use_container_width=True)

        st.subheader("Descargas")
        export_fun = pd.DataFrame({
            "Fecha": aligned_index,
            "Pack equal weight": ew_series.values,
            "Quant Selection real": real_series.values,
            benchmark_fun: bench_series.values,
        })
        st.download_button(
            "Descargar comparación CSV",
            data=export_fun.to_csv(index=False).encode("utf-8"),
            file_name="quant_selection_fun_equal_weight.csv",
            mime="text/csv",
        )

    except Exception as e:
        st.error(f"No se pudo calcular la sección Fun: {e}")
