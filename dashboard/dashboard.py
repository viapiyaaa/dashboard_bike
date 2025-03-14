import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

day_df = pd.read_csv("day_data.csv")
hour_df = pd.read_csv("hour_data.csv")

def create_classify_day(row):
    if row["holiday"] == 1:
        return "Holiday"
    elif row["weekday"] in [0, 6]:
        return "Weekend"
    else:
        return "Workday"

day_df["day_type"] = day_df.apply(create_classify_day, axis=1)

bins = [0, 6, 12, 16, 19, 24]
labels = ["Dini Hari", "Pagi", "Siang", "Sore", "Malam"]
hour_df["time_category"] = pd.cut(hour_df["hr"], bins=bins, labels=labels, right=False)

category_count = day_df.groupby("day_type")["cnt"].sum().reset_index()
category_avg = day_df.groupby("day_type")["cnt"].mean().reset_index()

time_distribution = hour_df.groupby("time_category")["cnt"].sum().reset_index()
time_counts = hour_df["time_category"].value_counts().reset_index()
time_counts.columns = ["time_category", "count"]
time_analysis = time_distribution.merge(time_counts, on="time_category")
time_analysis["avg_peminjaman"] = time_analysis["cnt"] / time_analysis["count"]

st.header('📊 Bicycle Distribution Dashboard')

with st.sidebar:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo.jpg")

    st.subheader("🔍 Pilih Tampilan:")
    if st.button("Dashboard Utama"):
        st.session_state.page = "dashboard"
    if st.button("Distribusi Berdasarkan Klasifikasi Hari"):
        st.session_state.page = "day_classification"
    if st.button("Distribusi Berdasarkan Kategori Waktu"):
        st.session_state.page = "time_category"

if "page" not in st.session_state:
    st.session_state.page = "dashboard"

if st.session_state.page == "dashboard":
    st.subheader("📌 Average Bike Rentals by Day Classification")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Holiday", f"{category_avg[category_avg['day_type'] == 'Holiday']['cnt'].values[0]:,.0f}")
    with col2:
        st.metric("Weekend", f"{category_avg[category_avg['day_type'] == 'Weekend']['cnt'].values[0]:,.0f}")
    with col3:
        st.metric("Workday", f"{category_avg[category_avg['day_type'] == 'Workday']['cnt'].values[0]:,.0f}")

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x="day_type", y="cnt", data=category_avg, palette=["#90CAF9", "#90CAF9", "#90CAF9"], ax=ax)
    ax.set_xlabel("Day Type")
    ax.set_ylabel("Average Bike Rentals")
    ax.set_title("Average Bike Rentals by Day Classification")
    st.pyplot(fig)
    
    st.subheader("📌 Average Bike Rentals by Time Category")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Dini Hari", f"{time_analysis[time_analysis['time_category'] == 'Dini Hari']['avg_peminjaman'].values[0]:,.0f}")
    with col2:
        st.metric("Pagi", f"{time_analysis[time_analysis['time_category'] == 'Pagi']['avg_peminjaman'].values[0]:,.0f}")
    with col3:
        st.metric("Siang", f"{time_analysis[time_analysis['time_category'] == 'Siang']['avg_peminjaman'].values[0]:,.0f}")
    with col4:
        st.metric("Sore", f"{time_analysis[time_analysis['time_category'] == 'Sore']['avg_peminjaman'].values[0]:,.0f}")
    with col5:
        st.metric("Malam", f"{time_analysis[time_analysis['time_category'] == 'Malam']['avg_peminjaman'].values[0]:,.0f}")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x="time_category", y="avg_peminjaman", data=time_analysis, order=labels, color="#90CAF9", ax=ax)
    st.pyplot(fig)

elif st.session_state.page == "day_classification":
    st.title('Distribution of Bicycle Loans by Day Classification')
    tab1, tab2 = st.tabs(["Amounts", "Average"])

    with tab1:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x="day_type", y="cnt", data=category_count, palette=["#D3D3D3", "#D3D3D3", "#90CAF9"], ax=ax)
        st.pyplot(fig)

    with tab2:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x="day_type", y="cnt", data=category_avg, palette=["#D3D3D3", "#D3D3D3", "#90CAF9"], ax=ax)
        st.pyplot(fig)

elif st.session_state.page == "time_category":
    st.title('Borrowing by Time Category')
    tab1, tab2 = st.tabs(["Total", "Average"])

    with tab1:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x="time_category", y="cnt", data=time_analysis, palette=["#D3D3D3", "#D3D3D3", "#90CAF9"], ax=ax)
        st.pyplot(fig)

    with tab2:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x="time_category", y="avg_peminjaman", data=time_analysis, palette=["#D3D3D3", "#D3D3D3", "#90CAF9"], ax=ax)
        st.pyplot(fig)
