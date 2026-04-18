import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Jaeger Simulator", layout="centered")
st.title("🚀 Jaeger Simulator - Matching Order Gojek Style")
st.markdown("**Simulasi sederhana sistem matching Jaeger (Gojek)**")

if 'drivers' not in st.session_state:
    st.session_state.drivers = []

st.sidebar.header("Tambah Driver")
name = st.sidebar.text_input("Nama Driver", value=f"Driver_{len(st.session_state.drivers)+1}")
eta = st.sidebar.slider("ETA (menit)", 1, 20, 5)
waiting = st.sidebar.slider("Waiting Time (menit)", 0, 30, 5)
performance = st.sidebar.slider("Performance (0-10)", 0.0, 10.0, 8.0, 0.1)

if st.sidebar.button("➕ Tambah Driver"):
    if name.strip():
        st.session_state.drivers.append({
            "Nama": name.strip(),
            "ETA": eta,
            "Waiting": waiting,
            "Performance": round(performance, 1)
        })
        st.sidebar.success(f"{name} ditambahkan!")

st.subheader("Daftar Driver")
if st.session_state.drivers:
    df = pd.DataFrame(st.session_state.drivers)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Hapus Semua"):
            st.session_state.drivers.clear()
            st.rerun()
    with col2:
        if st.button("🔄 Contoh Data"):
            st.session_state.drivers = [
                {"Nama": "Asep", "ETA": 3, "Waiting": 12, "Performance": 9.2},
                {"Nama": "Budi", "ETA": 5, "Waiting": 4, "Performance": 8.5},
                {"Nama": "Caca", "ETA": 2, "Waiting": 1, "Performance": 7.8},
            ]
            st.rerun()
else:
    st.info("Tambahkan driver dari sidebar.")

pickup = st.text_input("Lokasi Pickup", "Serang Station")

st.subheader("Jalankan Matching")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📍 Closest (ETA Only)", type="primary"):
        st.session_state.mode = "closest"
        st.session_state.pickup = pickup
        st.rerun()
with col2:
    if st.button("⚖️ Jaeger Style", type="primary"):
        st.session_state.mode = "jaeger"
        st.session_state.pickup = pickup
        st.rerun()
with col3:
    if st.button("🎲 Random"):
        st.session_state.mode = "random"
        st.session_state.pickup = pickup
        st.rerun()

if 'mode' in st.session_state and st.session_state.drivers:
    drivers = st.session_state.drivers.copy()
    etas = [d["ETA"] for d in drivers]
    waits = [d["Waiting"] for d in drivers]
    perfs = [d["Performance"] for d in drivers]
    
    def normalize(vals, reverse=False):
        if not vals: return []
        mn, mx = min(vals), max(vals)
        if mn == mx: return [1.0] * len(vals)
        if reverse: return [(mx - v) / (mx - mn) for v in vals]
        return [(v - mn) / (mx - mn) for v in vals]
    
    eta_scores = normalize(etas, reverse=True)
    wait_scores = normalize(waits)
    perf_scores = normalize(perfs)
    
    results = []
    for i, d in enumerate(drivers):
        if st.session_state.mode == "closest":
            score = eta_scores[i]
            mode_text = "Closest (ETA Only)"
        elif st.session_state.mode == "jaeger":
            score = 0.4 * eta_scores[i] + 0.4 * wait_scores[i] + 0.2 * perf_scores[i]
            mode_text = "Jaeger Multi-Objective"
        else:
            score = random.random()
            mode_text = "Random"
        
        results.append({"Nama": d["Nama"], "Skor": round(score, 3), "ETA": d["ETA"], "Waiting": d["Waiting"], "Performance": d["Performance"]})
    
    results.sort(key=lambda x: x["Skor"], reverse=True)
    
    st.success(f"**PEMENANG: {results[0]['Nama']}** (Skor: {results[0]['Skor']})")
    st.write(f"**Pickup:** {st.session_state.pickup}")
    st.write(f"**Mode:** {mode_text}")
    st.dataframe(pd.DataFrame(results), use_container_width=True, hide_index=True)

st.caption("Simulasi Jaeger Gojek | Bisa langsung dipakai di HP")
