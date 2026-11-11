import streamlit as st
from datetime import datetime

# ============================================================
# SISTEM PAKAR SEDERHANA - FORWARD CHAINING
# UTS Praktik Artificial Intelligence
# Catatan: hasil adalah indikasi berdasarkan aturan tugas,
# bukan diagnosis medis.
# ============================================================

st.set_page_config(
    page_title="Sistem Pakar Kesehatan",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------- DATA GEJALA -----------------------
GEJALA = {
    "G01": "Demam",
    "G02": "Demam tinggi",
    "G03": "Demam naik turun",
    "G04": "Menggigil",
    "G05": "Berkeringat berlebihan",
    "G06": "Sakit kepala",
    "G07": "Nyeri di belakang mata",
    "G08": "Nyeri otot",
    "G09": "Nyeri sendi",
    "G10": "Tubuh terasa lemas",
    "G11": "Nafsu makan menurun",
    "G12": "Mual",
    "G13": "Muntah berulang",
    "G14": "Nyeri perut hebat",
    "G15": "Diare",
    "G16": "Sembelit",
    "G17": "Batuk",
    "G18": "Pilek",
    "G19": "Sakit tenggorokan",
    "G20": "Sesak napas berat",
    "G21": "Nyeri dada",
    "G22": "Ruam merah pada kulit",
    "G23": "Mata merah",
    "G24": "Bintik putih dalam mulut",
    "G25": "Nyeri saat buang air kecil",
    "G26": "Sering buang air kecil",
    "G27": "Nyeri pinggang",
    "G28": "Hilang penciuman/pengecapan",
    "G29": "Pendarahan dari hidung/gusi",
    "G30": "Penurunan kesadaran",
}

# -------------------------- BASIS ATURAN ----------------------
# Setiap aturan: kode, kesimpulan, daftar kode gejala, keterangan.
ATURAN = [
    {"kode": "R01", "kesimpulan": "Indikasi influenza", "gejala": ["G01", "G06", "G08", "G17"]},
    {"kode": "R02", "kesimpulan": "Indikasi influenza", "gejala": ["G01", "G17", "G18"]},
    {"kode": "R03", "kesimpulan": "Indikasi COVID-19", "gejala": ["G01", "G07", "G19", "G28"]},
    {"kode": "R04", "kesimpulan": "Indikasi COVID-19", "gejala": ["G01", "G08", "G10", "G28"]},
    {"kode": "R05", "kesimpulan": "Indikasi DBD", "gejala": ["G02", "G06", "G07", "G08"]},
    {"kode": "R06", "kesimpulan": "Indikasi DBD", "gejala": ["G02", "G09", "G12"]},
    {"kode": "R07", "kesimpulan": "Indikasi DBD", "gejala": ["G01", "G07", "G09", "G22"]},
    {"kode": "R08", "kesimpulan": "Indikasi demam tifoid", "gejala": ["G01", "G06", "G10", "G11", "G14"]},
    {"kode": "R09", "kesimpulan": "Indikasi demam tifoid", "gejala": ["G01", "G12", "G14", "G15"]},
    {"kode": "R10", "kesimpulan": "Indikasi demam tifoid", "gejala": ["G01", "G11", "G14", "G16"]},
    {"kode": "R11", "kesimpulan": "Indikasi malaria", "gejala": ["G01", "G04", "G05", "G08"]},
    {"kode": "R12", "kesimpulan": "Indikasi malaria", "gejala": ["G03", "G04", "G05", "G08"]},
    {"kode": "R13", "kesimpulan": "Indikasi ISK", "gejala": ["G01", "G25", "G26"]},
    {"kode": "R14", "kesimpulan": "Indikasi ISK", "gejala": ["G01", "G25", "G27"]},
    {"kode": "R15", "kesimpulan": "Indikasi pneumonia", "gejala": ["G01", "G17", "G20", "G21"]},
    {"kode": "R16", "kesimpulan": "Indikasi pneumonia", "gejala": ["G02", "G17", "G20", "G10"]},
    {"kode": "R17", "kesimpulan": "Indikasi campak", "gejala": ["G01", "G17", "G22", "G23"]},
    {"kode": "R18", "kesimpulan": "Indikasi campak", "gejala": ["G01", "G22", "G23", "G24"]},
    {"kode": "R19", "kesimpulan": "Peringatan pendarahan", "gejala": ["G01", "G29"]},
    {"kode": "R20", "kesimpulan": "Peringatan tanda bahaya", "gejala": ["G01", "G13", "G14"]},
    {"kode": "R21", "kesimpulan": "Peringatan darurat", "gejala": ["G01", "G30"]},
    {"kode": "R22", "kesimpulan": "Peringatan darurat", "gejala": ["G01", "G20"]},
]

# -------------------------- SKENARIO UJI ----------------------
SKENARIO = {
    "Input manual": [],
    "Skenario 1 — Influenza (R01)": ["G01", "G06", "G08", "G17"],
    "Skenario 2 — COVID-19 (R03)": ["G01", "G07", "G19", "G28"],
    "Skenario 3 — Peringatan darurat (R21)": ["G01", "G30"],
    "Skenario 4 — DBD (R05)": ["G02", "G06", "G07", "G08"],
}

# -------------------------- FUNGSI INFERENSI ------------------
def forward_chaining(fakta_awal):
    """
    Forward chaining:
    1. Fakta awal = gejala yang dipilih pengguna.
    2. Periksa aturan IF-THEN satu per satu.
    3. Jika seluruh gejala pada suatu aturan ada dalam fakta,
       aturan dinyatakan terpenuhi dan kesimpulan ditambahkan.
    4. Catat proses agar dapat ditampilkan sebagai jejak inferensi.
    """
    fakta = set(fakta_awal)
    aturan_terpenuhi = []
    kesimpulan = []
    jejak = []

    jejak.append({
        "langkah": 1,
        "jenis": "Fakta awal",
        "detail": ", ".join(f"{kode} ({GEJALA[kode]})" for kode in sorted(fakta))
        if fakta else "Belum ada gejala yang dipilih.",
    })

    nomor_langkah = 2
    for aturan in ATURAN:
        cocok = all(kode in fakta for kode in aturan["gejala"])
        if cocok:
            aturan_terpenuhi.append(aturan)
            if aturan["kesimpulan"] not in kesimpulan:
                kesimpulan.append(aturan["kesimpulan"])
            jejak.append({
                "langkah": nomor_langkah,
                "jenis": f"Aturan {aturan['kode']} terpenuhi",
                "detail": (
                    "Semua kondisi terpenuhi: "
                    + " AND ".join(f"{kode} ({GEJALA[kode]})" for kode in aturan["gejala"])
                    + f" → {aturan['kesimpulan']}."
                ),
            })
            nomor_langkah += 1

    if not aturan_terpenuhi:
        jejak.append({
            "langkah": nomor_langkah,
            "jenis": "Belum ada aturan terpenuhi",
            "detail": "Kombinasi gejala yang dipilih belum cocok dengan seluruh kondisi pada aturan mana pun.",
        })

    return aturan_terpenuhi, kesimpulan, jejak


# -------------------------- TAMPILAN --------------------------
st.markdown(
    """
    <style>
    .main-title {font-size: 2.1rem; font-weight: 800; margin-bottom: 0.2rem;}
    .subtitle {font-size: 1rem; color: #64748b; margin-bottom: 1.1rem;}
    .info-card {
        padding: 1rem 1.1rem; border-radius: 14px;
        border: 1px solid rgba(128,128,128,.25);
        background: rgba(128,128,128,.06);
    }
    .small-muted {color: #64748b; font-size: .9rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.title("🩺 Sistem Pakar")
    st.caption("UTS Praktik Artificial Intelligence")
    st.divider()
    st.markdown("**Metode:** Forward Chaining")
    st.markdown("**Antarmuka:** Streamlit")
    st.markdown("**Basis pengetahuan:** 30 gejala · 22 aturan")
    st.divider()
    st.info(
        "Aplikasi pembelajaran. Hasil mengikuti aturan IF–THEN pada soal dan "
        "tidak menggantikan pemeriksaan tenaga kesehatan."
    )
    st.caption("Dibuat menggunakan Python")

st.markdown('<div class="main-title">Sistem Pakar Identifikasi Gejala</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Pilih gejala, jalankan inferensi, lalu lihat aturan yang terpenuhi dan jejak Forward Chaining.</div>',
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Kode gejala", len(GEJALA))
with col2:
    st.metric("Aturan IF–THEN", len(ATURAN))
with col3:
    st.metric("Metode inferensi", "Forward Chaining")

st.divider()

st.subheader("1. Pilih gejala")
st.write("Untuk mencoba aplikasi, pilih salah satu skenario uji. Pilih **Input manual** untuk memilih gejala sendiri.")

label_to_code = {f"{kode} — {nama}": kode for kode, nama in GEJALA.items()}

def muat_skenario():
    nama_skenario = st.session_state.get("skenario_pilihan", "Input manual")
    st.session_state["pilihan_gejala"] = [
        f"{kode} — {GEJALA[kode]}" for kode in SKENARIO[nama_skenario]
    ]

if "pilihan_gejala" not in st.session_state:
    st.session_state["pilihan_gejala"] = []

skenario_pilihan = st.selectbox(
    "Skenario pengujian",
    list(SKENARIO.keys()),
    key="skenario_pilihan",
    on_change=muat_skenario,
)
pilihan_label = st.multiselect(
    "Gejala yang ditemukan",
    options=list(label_to_code.keys()),
    key="pilihan_gejala",
    placeholder="Klik di sini untuk memilih satu atau beberapa gejala...",
)
fakta_pengguna = [label_to_code[label] for label in pilihan_label]

with st.expander("Lihat daftar lengkap kode gejala"):
    gejala_rows = [{"Kode": kode, "Gejala": nama} for kode, nama in GEJALA.items()]
    st.dataframe(gejala_rows, use_container_width=True, hide_index=True)

jalankan = st.button("🔎 Proses Forward Chaining", type="primary", use_container_width=True)

if jalankan:
    aturan_terpenuhi, kesimpulan, jejak = forward_chaining(fakta_pengguna)
    st.session_state["hasil_inferensi"] = {
        "fakta": fakta_pengguna,
        "aturan": aturan_terpenuhi,
        "kesimpulan": kesimpulan,
        "jejak": jejak,
        "waktu": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
    }

if "hasil_inferensi" in st.session_state:
    hasil = st.session_state["hasil_inferensi"]
    st.divider()
    st.subheader("2. Hasil inferensi")

    left, right = st.columns([1, 1])
    with left:
        st.markdown("**Gejala yang dipilih**")
        if hasil["fakta"]:
            for kode in hasil["fakta"]:
                st.write(f"• **{kode}** — {GEJALA[kode]}")
        else:
            st.warning("Belum ada gejala yang dipilih.")
    with right:
        st.markdown("**Kesimpulan sistem**")
        if hasil["kesimpulan"]:
            for item in hasil["kesimpulan"]:
                if "Peringatan darurat" in item:
                    st.error(f"🚨 {item}")
                elif "Peringatan" in item:
                    st.warning(f"⚠️ {item}")
                else:
                    st.success(f"• {item}")
        else:
            st.info("Tidak ada kesimpulan yang dapat ditarik berdasarkan aturan yang tersedia.")

    st.markdown("**Aturan yang berhasil dipenuhi**")
    if hasil["aturan"]:
        for aturan in hasil["aturan"]:
            kondisi = " AND ".join(aturan["gejala"])
            with st.container(border=True):
                st.markdown(f"**{aturan['kode']} — {aturan['kesimpulan']}**")
                st.code(f"IF {kondisi} THEN {aturan['kesimpulan']}", language="text")
                st.caption("Semua kode gejala dalam kondisi aturan ini ditemukan pada fakta awal.")
    else:
        st.write("Tidak ada aturan yang terpenuhi.")

    st.subheader("3. Tahapan proses inferensi")
    st.caption(f"Waktu pengujian: {hasil['waktu']}")
    for langkah in hasil["jejak"]:
        with st.container(border=True):
            st.markdown(f"**Langkah {langkah['langkah']}: {langkah['jenis']}**")
            st.write(langkah["detail"])

    st.subheader("4. Ringkasan pengujian")
    st.write(
        f"Fakta awal berjumlah **{len(hasil['fakta'])} gejala**. "
        f"Aturan yang terpenuhi berjumlah **{len(hasil['aturan'])}**. "
        f"Kesimpulan unik yang dihasilkan berjumlah **{len(hasil['kesimpulan'])}**."
    )

    st.warning(
        "Penting: ini adalah simulasi sistem pakar untuk tugas kuliah, bukan alat diagnosis. "
        "Jika seseorang mengalami sesak napas berat, penurunan kesadaran, atau perdarahan, "
        "segera cari pertolongan medis darurat."
    )

with st.expander("Lihat basis aturan R01–R22"):
    aturan_rows = []
    for aturan in ATURAN:
        aturan_rows.append({
            "Kode aturan": aturan["kode"],
            "Kondisi IF": " AND ".join(aturan["gejala"]),
            "Kesimpulan THEN": aturan["kesimpulan"],
        })
    st.dataframe(aturan_rows, use_container_width=True, hide_index=True)

st.divider()
st.caption("Proyek UTS Praktik Artificial Intelligence · Sistem Pakar berbasis aturan")
