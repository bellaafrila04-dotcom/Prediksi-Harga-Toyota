import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import plotly.io as pio
import joblib

# =========================================================
# KONFIGURASI HALAMAN
# =========================================================
st.set_page_config(
    page_title="TOYOVALUE",
    page_icon="🚗",
    layout="wide"
)

USD_RATE = 1.30
pio.templates["plotly"].layout.font.family = "Arial, Helvetica, sans-serif"

# =========================================================
# LOAD DATA
# =========================================================
@st.cache_data
def load_data():
    return pd.read_csv("toyota_clean.csv")

@st.cache_resource
def load_model():
    return joblib.load("model_toyota.pkl")


def to_usd(value):
    return float(value) * USD_RATE


def fmt_usd(value):
    return f"${value:,.2f}"


def clear_prediction():
    st.session_state["has_prediction"] = False
    st.session_state["predicted_price"] = None


def hero(title, subtitle, eyebrow="TOYOVALUE"):
    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-eyebrow">{eyebrow}</div>
            <h1>{title}</h1>
            <p class="hero-tagline">Find the right value for your Toyota.</p>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def tickvals_for_years(years):
    if len(years) <= 10:
        return years
    step = 2 if len(years) <= 16 else 3
    vals = years[::step]
    if years[-1] not in vals:
        vals.append(years[-1])
    return vals


# =========================================================
# CSS
# =========================================================
st.markdown(
    """
<style>
.stApp {
    background-color: #f6f7fb;
}
[data-testid="stSidebar"] {
    background-color: #08142d;
}
[data-testid="stSidebar"] * {
    color: white !important;
}
.stApp, [data-testid="stSidebar"] {
    font-family: Arial, Helvetica, sans-serif;
}
h1, h2, h3, h4, .section-title { font-family: Arial, Helvetica, sans-serif; font-weight: 700; letter-spacing: -0.015em; }
[data-testid="stMarkdownContainer"] p, [data-testid="stWidgetLabel"] p, [data-baseweb="select"] { font-family: Arial, Helvetica, sans-serif; }
[data-testid="stWidgetLabel"] p { font-weight: 600; }
.hero-card .hero-tagline { font-family: Georgia, "Times New Roman", serif !important; }
.hero-card .hero-tagline { font-family: Georgia, "Times New Roman", serif; font-style: italic; font-weight: 400; font-size: 1.14rem; color: #fff0f1; margin: 0 0 10px; letter-spacing: .01em; }
[data-testid="stSidebar"] [role="radiogroup"] { gap: 4px; }
[data-testid="stSidebar"] [role="radiogroup"] label { padding: 2px 0; margin: 0; }
[data-testid="stSidebar"] [role="radiogroup"] label p { font-size: 1.12rem !important; font-weight: 600; }
.sidebar-note { border: 1px solid rgba(255,255,255,.14); border-radius: 12px; padding: 14px; font-size: .82rem; line-height: 1.6; }
.sidebar-note div { margin-top: 6px; opacity: .75; }
.stHeadingAnchor {
    display: none !important;
}
.hero-card {
    background:
        linear-gradient(90deg, rgba(8,20,45,0.82), rgba(165,16,39,0.80)),
        url("https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=1600&q=80");
    background-size: cover;
    background-position: center;
    border-radius: 26px;
    padding: 34px 34px;
    color: white;
    margin-bottom: 28px;
    box-shadow: 0 12px 28px rgba(0,0,0,0.14);
}
.hero-card h1 {
    margin: 0 0 14px 0;
    font-size: 2.45rem;
    font-weight: 800;
    color: white;
}
.hero-card p {
    margin: 0 0 8px 0;
    font-size: 1.02rem;
    color: #f8fafc;
    max-width: 760px;
}
.hero-eyebrow {
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 0.9rem;
    font-weight: 700;
    color: #fecaca;
    margin-bottom: 8px;
}
.section-title {
    font-size: 1.25rem;
    font-weight: 800;
    color: #1e293b;
    margin-bottom: 8px;
}
.card-box {
    background-color: white;
    padding: 18px;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 6px 20px rgba(0,0,0,0.05);
}
.result-box {
    background: linear-gradient(135deg, #111827, #dc2626);
    color: white;
    padding: 22px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 12px 25px rgba(0,0,0,0.16);
    min-height: 170px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
}
.result-box h2 {
    color: white;
    margin-bottom: 8px;
    font-size: 1.2rem;
}
.result-box h1 {
    font-size: 2.1rem;
    color: white;
    margin: 10px 0;
}
.result-box p {
    color: #f8fafc;
    font-size: 0.95rem;
}
.info-box {
    background-color: white;
    border-radius: 22px;
    padding: 24px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 6px 20px rgba(0,0,0,0.05);
}
.about-box {
    background-color: white;
    border-radius: 22px;
    padding: 22px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 6px 20px rgba(0,0,0,0.05);
    line-height: 1.8;
}
[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 12px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.04);
}
[data-testid="stMetricLabel"] {
    font-size: 0.88rem !important;
}
[data-testid="stMetricValue"] {
    font-size: 1.15rem !important;
}
.stButton > button,
.stFormSubmitButton > button {
    background-color: #dc2626;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 18px;
    font-weight: bold;
    width: 100%;
}
.footer {
    text-align: center;
    color: #64748b;
    font-size: 13px;
    margin-top: 28px;
    padding: 18px;
}
</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# LOAD OBJECTS
# =========================================================
df = load_data()
model_ml = load_model()
scores = pd.read_csv("model_scores.csv")

# dukung beberapa nama kolom
cv_col = "CV_R2" if "CV_R2" in scores.columns else "CV R2" if "CV R2" in scores.columns else None
r2_col = "R2"

if cv_col:
    best_model_row = scores.loc[scores[cv_col].idxmax()]
else:
    best_model_row = scores.loc[scores[r2_col].idxmax()]

if "has_prediction" not in st.session_state:
    st.session_state["has_prediction"] = False
if "predicted_price" not in st.session_state:
    st.session_state["predicted_price"] = None

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.markdown("""
<div style="display:flex;align-items:center;gap:10px;">
<svg viewBox="0 0 90 60" width="42" height="28" xmlns="http://www.w3.org/2000/svg">
  <g stroke="#ffffff" stroke-width="4" fill="none">
    <ellipse cx="45" cy="30" rx="41" ry="25" />
    <ellipse cx="45" cy="30" rx="13" ry="25" />
    <ellipse cx="45" cy="17" rx="33" ry="12" />
  </g>
</svg>
<h2 style="margin:0;color:white;font-size:1.1rem;">TOYOVALUE</h2>
</div>
""", unsafe_allow_html=True)
st.sidebar.caption("Prediksi Harga Mobil Toyota")
st.sidebar.divider()

menu = st.sidebar.radio(
    "Menu",
    ["Prediksi Harga", "Analisis Pasar", "Evaluasi Model", "Tentang Aplikasi"],
)
st.sidebar.divider()
st.sidebar.markdown('<div class="sidebar-note"><strong>TOYOVALUE · 2026</strong><div>Analisis kendaraan &amp; estimasi harga berbasis data.</div></div>', unsafe_allow_html=True)

# =========================================================
# PAGE 1: PREDIKSI
# =========================================================
if menu == "Prediksi Harga":
    hero("Prediksi Harga Toyota", "Ketahui estimasi harga Toyota Anda dengan pembelajaran mesin.")

    st.markdown('<div class="section-title">Prediksi Harga Toyota Anda</div>', unsafe_allow_html=True)
    st.write("Masukkan spesifikasi kendaraan untuk memperoleh estimasi harga mobil Toyota.")

    col1, col2 = st.columns([1.1, 0.9], gap="large")

    with col1:
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown("## Spesifikasi Kendaraan")

        model_options = sorted(df["model"].dropna().unique().tolist())
        if "selected_model" not in st.session_state:
            st.session_state["selected_model"] = model_options[0]

        selected_model = st.selectbox(
            "Tipe Mobil Toyota",
            model_options,
            key="selected_model",
            on_change=clear_prediction,
        )

        model_df = df[df["model"] == selected_model].copy()
        year_options = sorted(model_df["year"].dropna().astype(int).unique().tolist())

        if st.session_state.get("last_model") != selected_model:
            st.session_state["selected_year"] = year_options[len(year_options)//2]
            st.session_state["selected_transmission"] = None
            st.session_state["selected_fuel"] = None
            st.session_state["last_model"] = selected_model
        elif st.session_state.get("selected_year") not in year_options:
            st.session_state["selected_year"] = year_options[len(year_options)//2]
            st.session_state["selected_transmission"] = None
            st.session_state["selected_fuel"] = None

        year = st.selectbox(
            "Tahun Produksi",
            year_options,
            key="selected_year",
            on_change=clear_prediction,
        )

        year_df = model_df[model_df["year"].astype(int) == int(year)].copy()
        transmission_options = sorted(year_df["transmission"].dropna().unique().tolist())

        if st.session_state.get("selected_transmission") not in transmission_options:
            st.session_state["selected_transmission"] = transmission_options[0]

        transmission = st.selectbox(
            "Transmisi",
            transmission_options,
            key="selected_transmission",
            on_change=clear_prediction,
        )

        trans_df = year_df[year_df["transmission"] == transmission].copy()
        fuel_options = sorted(trans_df["fuel_type"].dropna().unique().tolist())

        if st.session_state.get("selected_fuel") not in fuel_options:
            st.session_state["selected_fuel"] = fuel_options[0]

        fuel_type = st.selectbox(
            "Tipe Bahan Bakar",
            fuel_options,
            key="selected_fuel",
            on_change=clear_prediction,
        )

        subset_df = trans_df[trans_df["fuel_type"] == fuel_type].copy()
        if subset_df.empty:
            subset_df = trans_df.copy()

        engine_default = round(float(subset_df["engine_size"].median()), 1)
        mileage_default = int(subset_df["mileage"].median())
        tax_default = int(subset_df["tax"].median())
        mpg_default = round(float(subset_df["mpg"].median()), 1)

        engine_size = st.slider(
            "Kapasitas Mesin (L)",
            min_value=float(round(df["engine_size"].min(), 1)),
            max_value=float(round(df["engine_size"].max(), 1)),
            value=float(engine_default),
            step=0.1,
            on_change=clear_prediction,
        )

        mileage = st.slider(
            "Jarak Tempuh",
            min_value=int(df["mileage"].min()),
            max_value=int(df["mileage"].max()),
            value=int(mileage_default),
            step=500,
            on_change=clear_prediction,
        )

        tax = st.slider(
            "Pajak Tahunan",
            min_value=int(df["tax"].min()),
            max_value=int(df["tax"].max()),
            value=int(tax_default),
            step=5,
            on_change=clear_prediction,
        )

        mpg = st.slider(
            "Efisiensi Bahan Bakar (MPG)",
            min_value=float(round(df["mpg"].min(), 1)),
            max_value=float(round(df["mpg"].max(), 1)),
            value=float(mpg_default),
            step=0.1,
            on_change=clear_prediction,
        )

        predict_btn = st.button("Prediksi Harga")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        if predict_btn:
            input_data = pd.DataFrame({
                "model": [selected_model],
                "year": [int(year)],
                "transmission": [transmission],
                "mileage": [mileage],
                "fuel_type": [fuel_type],
                "tax": [tax],
                "mpg": [mpg],
                "engine_size": [engine_size],
            })

            prediction = float(model_ml.predict(input_data)[0])
            prediction_usd = to_usd(prediction)
            st.session_state["has_prediction"] = True
            st.session_state["predicted_price"] = prediction_usd
            st.session_state["summary"] = {
                "model": selected_model,
                "year": year,
                "transmission": transmission,
                "fuel_type": fuel_type,
                "engine_size": engine_size,
                "mileage": mileage,
                "tax": tax,
                "mpg": mpg,
            }

        if st.session_state.get("has_prediction"):
            prediction_usd = st.session_state["predicted_price"]
            s = st.session_state["summary"]
            st.markdown(
                f"""
                <div class="result-box">
                    <h2>Estimasi Harga Kendaraan</h2>
                    <h1>{fmt_usd(prediction_usd)}</h1>
                    <p>{s['model']} • {s['year']} • {s['transmission']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.markdown("### Ringkasan Kendaraan")
            c1, c2 = st.columns(2)
            c1.metric("Tipe Mobil", s["model"])
            c2.metric("Tahun", int(s["year"]))
            c3, c4 = st.columns(2)
            c3.metric("Transmisi", s["transmission"])
            c4.metric("Bahan Bakar", s["fuel_type"])
            c5, c6 = st.columns(2)
            c5.metric("Kapasitas Mesin", f"{s['engine_size']:.1f} L")
            c6.metric("Jarak Tempuh", f"{s['mileage']:,}")
            c7, c8 = st.columns(2)
            c7.metric("Pajak Tahunan", f"{s['tax']}")
            c8.metric("MPG", f"{s['mpg']:.1f}")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                """
                <div class="result-box">
                    <h2>Estimasi Harga Kendaraan</h2>
                    <h1>$ —</h1>
                    <p>Pilih spesifikasi mobil Anda lalu klik Prediksi Harga.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.markdown("### Ringkasan Kendaraan")
            st.caption("Ringkasan akan muncul setelah Anda menekan tombol Prediksi Harga.")
            st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.get("has_prediction"):
        st.markdown("## Insight Prediksi")
        s = st.session_state["summary"]
        prediction_usd = st.session_state["predicted_price"]

        similar = df[df["model"] == s["model"]].copy()
        similar["price_usd"] = similar["price"].apply(to_usd)

        chart1, chart2 = st.columns(2, gap="large")
        with chart1:
            fig_dist = px.histogram(
                similar,
                x="price_usd",
                nbins=25,
                title="Distribusi Harga Kendaraan Sejenis",
                color_discrete_sequence=["#cbd5e1"],
            )
            fig_dist.add_vline(
                x=prediction_usd,
                line_width=3,
                line_dash="dash",
                line_color="#dc2626",
            )
            fig_dist.update_layout(
                xaxis_title="Harga ($)",
                yaxis_title="Jumlah",
                xaxis=dict(tickmode="linear", tick0=0, dtick=5000, tickformat="~s"),
            )
            st.plotly_chart(fig_dist, use_container_width=True)
            st.caption(f"Garis merah putus-putus: hasil prediksi. Pembanding: {len(similar):,} mobil Toyota {s['model']} dalam dataset.")

        with chart2:
            q1 = similar["price_usd"].quantile(0.25)
            med = similar["price_usd"].median()
            q3 = similar["price_usd"].quantile(0.75)
            compare_df = pd.DataFrame(
                {
                    "Kategori": ["Q1", "Median", "Prediksi", "Q3"],
                    "Harga": [q1, med, prediction_usd, q3],
                }
            )
            fig_compare = px.bar(
                compare_df,
                x="Kategori",
                y="Harga",
                title="Perbandingan Harga Mobil Sejenis",
                color="Kategori",
                color_discrete_sequence=["#9ca3af", "#6b7280", "#dc2626", "#0f172a"],
            )
            fig_compare.update_layout(yaxis_title="Harga ($)", showlegend=False)
            fig_compare.update_yaxes(tickmode="linear", tick0=0, dtick=5000 if max(q3, prediction_usd) >= 15000 else 1000, tickformat="~s")
            st.plotly_chart(fig_compare, use_container_width=True)

        st.markdown("### Simulasi perubahan harga (what-if)")
        chart3, chart4 = st.columns(2, gap="large")
        with chart3:
            min_mileage = int(df["mileage"].min())
            max_mileage = int(df["mileage"].max())
            step = max(2500, int((max_mileage - min_mileage) / 12))
            mileage_points = list(range(min_mileage, max_mileage + 1, step))
            if mileage_points[-1] != max_mileage:
                mileage_points.append(max_mileage)

            sim_mileage = pd.DataFrame(
                {
                    "model": [s["model"]] * len(mileage_points),
                    "year": [int(s["year"])] * len(mileage_points),
                    "transmission": [s["transmission"]] * len(mileage_points),
                    "mileage": mileage_points,
                    "fuel_type": [s["fuel_type"]] * len(mileage_points),
                    "tax": [s["tax"]] * len(mileage_points),
                    "mpg": [s["mpg"]] * len(mileage_points),
                    "engine_size": [s["engine_size"]] * len(mileage_points),
                }
            )
            sim_mileage["predicted_price_usd"] = model_ml.predict(sim_mileage) * USD_RATE
            fig_mileage = px.line(
                sim_mileage,
                x="mileage",
                y="predicted_price_usd",
                markers=True,
                title="Jarak Tempuh vs Prediksi Harga",
                color_discrete_sequence=["#dc2626"],
            )
            fig_mileage.add_scatter(
                x=[s["mileage"]],
                y=[prediction_usd],
                mode="markers",
                marker=dict(size=10, color="#0f172a"),
                name="Pilihan Anda",
            )
            fig_mileage.update_layout(
                xaxis_title="Jarak tempuh (mil)",
                yaxis_title="Estimasi harga ($)",
                xaxis=dict(tickmode="linear", dtick=10000, tickformat=",d"),
                yaxis=dict(tickformat=",.0f"),
            )
            st.plotly_chart(fig_mileage, use_container_width=True)

        with chart4:
            model_years = sorted(df[df["model"] == s["model"]]["year"].dropna().astype(int).unique().tolist())
            sim_year = pd.DataFrame(
                {
                    "model": [s["model"]] * len(model_years),
                    "year": model_years,
                    "transmission": [s["transmission"]] * len(model_years),
                    "mileage": [s["mileage"]] * len(model_years),
                    "fuel_type": [s["fuel_type"]] * len(model_years),
                    "tax": [s["tax"]] * len(model_years),
                    "mpg": [s["mpg"]] * len(model_years),
                    "engine_size": [s["engine_size"]] * len(model_years),
                }
            )
            sim_year["predicted_price_usd"] = model_ml.predict(sim_year) * USD_RATE
            fig_year = px.line(
                sim_year,
                x="year",
                y="predicted_price_usd",
                markers=True,
                title="Tahun Produksi vs Prediksi Harga",
                color_discrete_sequence=["#0f172a"],
            )
            fig_year.add_scatter(
                x=[int(s["year"])],
                y=[prediction_usd],
                mode="markers",
                marker=dict(size=10, color="#dc2626"),
                name="Pilihan Anda",
            )
            fig_year.update_layout(
                xaxis_title="Tahun produksi",
                yaxis_title="Estimasi harga ($)",
                xaxis=dict(tickmode="array", tickvals=tickvals_for_years(model_years)),
                yaxis=dict(tickformat=",.0f"),
            )
            st.plotly_chart(fig_year, use_container_width=True)

# =========================================================
# PAGE 2: ANALISIS PASAR
# =========================================================
elif menu == "Analisis Pasar":
    hero("Analisis Pasar Toyota", "Jelajahi karakteristik kendaraan dan harga dalam dataset.")

    st.write("Cari atau pilih tipe mobil Toyota untuk melihat pola harga dan karakteristik datanya.")

    all_models = sorted(df["model"].dropna().unique().tolist())
    selected_models = st.multiselect(
        "Cari atau pilih tipe mobil Toyota",
        all_models,
        default=[],
        placeholder="Ketik atau pilih tipe mobil...",
        key="market_models",
    )
    st.caption("Jika belum ada tipe mobil yang dipilih, analisis menampilkan seluruh dataset.")

    if not selected_models:
        market_df = df.copy()
    else:
        market_df = df[df["model"].isin(selected_models)].copy()

    market_df["price_usd"] = market_df["price"].apply(to_usd)

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Mobil", f"{len(market_df):,}")
    m2.metric("Tipe Mobil", market_df["model"].nunique())
    m3.metric("Rata-rata Harga", fmt_usd(market_df["price_usd"].mean()))

    c1, c2 = st.columns(2, gap="large")
    with c1:
        fig1 = px.histogram(
            market_df,
            x="price_usd",
            nbins=30,
            title="Distribusi Harga Mobil Toyota",
            color_discrete_sequence=["#dc2626"],
        )
        fig1.update_layout(xaxis_title="Harga ($)", yaxis_title="Jumlah", xaxis=dict(tickmode="linear", tick0=0, dtick=5000, tickformat="~s"))
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        avg_by_model = market_df.groupby("model", as_index=False)["price_usd"].mean().sort_values("price_usd", ascending=False)
        fig2 = px.bar(
            avg_by_model,
            x="model",
            y="price_usd",
            title="Rata-rata Harga per Model Toyota",
            color_discrete_sequence=["#0f172a"],
        )
        fig2.update_layout(xaxis_title="Model", yaxis_title="Harga rata-rata ($)", height=460)
        fig2.update_xaxes(categoryorder="array", categoryarray=avg_by_model["model"].tolist(), tickangle=-45, automargin=True)
        fig2.update_yaxes(tickmode="linear", tick0=0, dtick=5000, tickformat="~s", rangemode="tozero")
        st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2, gap="large")
    with c3:
        fig3 = px.box(
            market_df,
            x="model",
            y="price_usd",
            title="Sebaran Harga per Model",
            color_discrete_sequence=["#dc2626"],
        )
        fig3.update_layout(xaxis_title="Model", yaxis_title="Harga ($)", height=460)
        fig3.update_xaxes(tickangle=-45, automargin=True)
        fig3.update_yaxes(tickmode="linear", tick0=0, dtick=5000, tickformat="~s", rangemode="tozero")
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        fuel_summary = market_df["fuel_type"].value_counts().reset_index()
        fuel_summary.columns = ["fuel_type", "jumlah"]
        # Tetapkan warna langsung agar tidak berubah menjadi hitam di iframe.
        fuel_colors = {
            "Petrol": "#2874C9",
            "Hybrid": "#159D83",
            "Diesel": "#DC3856",
            "Other": "#9666D5",
        }
        neon_colors = {
            "Petrol": "#00B8FF",
            "Hybrid": "#00F2AD",
            "Diesel": "#FF386D",
            "Other": "#C67BFF",
        }
        labels = fuel_summary["fuel_type"].tolist()
        base_colors = [fuel_colors.get(x, "#64748B") for x in labels]
        vivid_colors = [neon_colors.get(x, "#38E8FF") for x in labels]
        fig4 = px.pie(
            fuel_summary,
            names="fuel_type",
            values="jumlah",
            title="Komposisi Tipe Bahan Bakar",
            hole=0.45,
            template="plotly_white",
        )
        fig4.update_traces(
            sort=False,
            textinfo="none",
            marker=dict(colors=base_colors, line=dict(color="#f6f7fb", width=2)),
            customdata=vivid_colors,
            pull=[0] * len(fuel_summary),
            hovertemplate="%{label}<br>Jumlah: %{value:,}<br>Persentase: %{percent}<extra></extra>",
        )
        fig4.update_layout(
            height=460, paper_bgcolor="#f6f7fb", plot_bgcolor="#f6f7fb",
            legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.10),
            margin=dict(t=65, b=75, l=10, r=10),
            font=dict(family="Arial, Helvetica, sans-serif", color="#151922", size=13),
            annotations=[dict(x=0.50, y=0.50, xref="paper", yref="paper", text="", showarrow=False, font=dict(size=12, color="#64748b"))],
        )
        pie_script = r"""
        const gd = document.getElementById('{plot_id}');
        const trace = gd.data[0];
        const base = Array.from(trace.marker.colors);
        const neon = Array.from(trace.customdata);
        let selected = -1;
        // CSS neon hover tanpa merender ulang grafik sehingga hover tidak berkedip.
        function decorate() {
            const slices = gd.querySelectorAll('.pielayer .slice');
            slices.forEach((slice, i) => {
                const path = slice.querySelector('.surface');
                if (!path) return;
                const idx = i;
                path.style.setProperty('--neon', neon[idx]);
                path.classList.toggle('toy-selected', idx === selected);
            });
        }
        gd.on('plotly_afterplot', decorate);
        decorate();
        gd.on('plotly_click', function(event) {
            if (!event.points || !event.points.length) return;
            const p = event.points[0];
            const index = trace.labels.indexOf(p.label);
            if (index < 0) return;
            selected = selected === index ? -1 : index;
            const pulls = trace.labels.map((_, i) => i === selected ? 0.10 : 0);
            const colors = base.map((color, i) => i === selected ? neon[i] : color);
            const total = trace.values.reduce((a, b) => a + Number(b), 0);
            const value = Number(trace.values[index]);
            const text = selected < 0 ? '' : '<b>' + p.label + '</b><br>' + value.toLocaleString('id-ID') + ' mobil<br>' + (100 * value / total).toFixed(2) + '%';
            Plotly.restyle(gd, {pull: [pulls], 'marker.colors': [colors]}, [0])
                .then(() => Plotly.relayout(gd, {'annotations[0].text': text}))
                .then(decorate);
        });
        """
        pie_html = pio.to_html(fig4, full_html=True, include_plotlyjs=True,
                               config={"responsive": True, "displaylogo": False},
                               post_script=pie_script)
        pie_css = """<style>
        .pielayer .slice .surface { cursor: pointer; transition: filter .15s ease; }
        .pielayer .slice:hover .surface, .pielayer .slice .surface.toy-selected {
            fill: var(--neon) !important;
            filter: drop-shadow(0 0 5px var(--neon)) brightness(1.12);
        }
        </style>"""
        components.html(pie_html.replace("</head>", pie_css + "</head>"),
                        height=480, scrolling=False)

# =========================================================
# PAGE 3: EVALUASI MODEL
# =========================================================
elif menu == "Evaluasi Model":
    hero("Evaluasi Model", "Bandingkan performa beberapa algoritma machine learning yang digunakan.")

    note = f"Model terpilih: {best_model_row['Model']}"
    if cv_col:
        note += " (R² validasi silang tertinggi)."
    st.write(note)

    a, b, c, d = st.columns(4)
    a.metric("R² pengujian", f"{best_model_row['R2']:.4f}")
    b.metric("MAE", f"{best_model_row['MAE']:,.2f}")
    c.metric("RMSE", f"{best_model_row['RMSE']:,.2f}")
    d.metric("R² validasi silang", f"{best_model_row[cv_col]:.4f}" if cv_col else "-")

    st.dataframe(scores, use_container_width=True)

    p1, p2 = st.columns(2, gap="large")
    with p1:
        y_cols = ["R2"] + ([cv_col] if cv_col else [])
        fig_perf1 = px.bar(
            scores,
            x="Model",
            y=y_cols,
            barmode="group",
            title="Perbandingan Nilai R²",
            color_discrete_sequence=["#dc2626", "#0f172a"],
        )
        st.plotly_chart(fig_perf1, use_container_width=True)

    with p2:
        fig_perf2 = px.bar(
            scores,
            x="Model",
            y=["MAE", "RMSE"],
            barmode="group",
            title="Perbandingan Galat Model",
            color_discrete_sequence=["#dc2626", "#94a3b8"],
        )
        st.plotly_chart(fig_perf2, use_container_width=True)

# =========================================================
# PAGE 4: TENTANG
# =========================================================
elif menu == "Tentang Aplikasi":
    hero("Tentang Aplikasi", "Pelajari tujuan, fitur, dan manfaat dari TOYOVALUE.")

    st.markdown('<div class="about-box">', unsafe_allow_html=True)
    st.markdown("## Apa itu TOYOVALUE?")
    st.write(
        "TOYOVALUE merupakan aplikasi prediksi harga mobil bekas Toyota berbasis pembelajaran mesin. "
        "Aplikasi ini membantu pengguna memperkirakan nilai kendaraan dari beberapa spesifikasi utama, "
        "serta mendukung eksplorasi data pasar Toyota secara ringkas dan interaktif."
    )

    k1, k2, k3 = st.columns(3)
    k1.metric("Data kendaraan", f"{len(df):,}")
    k2.metric("Tipe mobil", df['model'].nunique())
    k3.metric("Algoritma", len(scores))

    st.markdown("### Tujuan Aplikasi")
    st.markdown(
        """
- Membantu memperkirakan harga mobil Toyota berdasarkan spesifikasi kendaraan.
- Menyajikan gambaran umum pasar mobil Toyota melalui visualisasi data.
- Membandingkan performa beberapa model machine learning untuk prediksi harga.
- Menjadi media pembelajaran sederhana untuk penerapan data science pada kasus nyata.
"""
    )

    st.markdown("### Fitur Utama")
    st.markdown(
        """
- **Prediksi Harga**: menghitung estimasi harga kendaraan berdasarkan input pengguna.
- **Analisis Pasar**: menampilkan distribusi harga, rata-rata harga, dan komposisi data Toyota.
- **Evaluasi Model**: memperlihatkan hasil perbandingan performa algoritma machine learning.
- **Tampilan Interaktif**: memudahkan pengguna memahami data dan hasil prediksi dengan visual yang rapi.
"""
    )

    st.markdown("### Manfaat Penggunaan")
    st.markdown(
        """
- Membantu pengguna memperoleh gambaran nilai kendaraan secara cepat.
- Menjadi referensi awal sebelum menjual atau membeli mobil Toyota bekas.
- Memberikan contoh implementasi machine learning dalam bidang otomotif.
"""
    )

    st.markdown("### Catatan")
    st.write(
        "Harga ditampilkan dalam dolar AS dengan asumsi mata uang asli GBP dan kurs ilustratif tetap 1 GBP = 1,30 USD. "
        "Hasil yang diberikan merupakan estimasi model, sehingga dapat berbeda dengan harga pasar aktual."
    )
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown(
    """
    <div class="footer">
    TOYOVALUE © 2026 | Prediksi Harga Mobil Toyota
    </div>
    """,
    unsafe_allow_html=True,
)