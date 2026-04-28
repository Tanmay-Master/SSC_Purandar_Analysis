import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- Page config ----------
st.set_page_config(page_title="SSC School Comparison", layout="wide")
st.title("🏫 School‑wise Pass Percentage Comparison (SSC)")

# ---------- Load data (cached for speed) ----------
@st.cache_data
def load_data():
    # Change filename to match your SSC CSV file
    df = pd.read_csv("combined_ssc_data.csv")
    df['Year'] = df['Year'].astype(int)
    return df

df = load_data()

# ---------- Sidebar filter ----------
with st.sidebar:
    st.header("🔍 Filters")
    year = st.selectbox(
        "Select Year",
        sorted(df['Year'].unique()),
        index=len(df['Year'].unique()) - 1   # default = latest year
    )
    
    # Get schools available for selected year
    schools_in_year = sorted(df[df['Year'] == year]['Name of the School'].unique())
    
    schools = st.multiselect(
        "Select Schools (leave empty for all)",
        schools_in_year,
        default=None,
        key="school_filter"
    )

# ---------- Filter data ----------
filtered = df[df['Year'] == year].copy()

# Apply school filter if schools are selected
if schools:
    filtered = filtered[filtered['Name of the School'].isin(schools)].copy()

if filtered.empty:
    st.warning(f"No data available for the year {year}.")
    st.stop()

filtered['Pass_Label'] = filtered['Pass Percent'].apply(lambda x: f"{x:.1f}%")
filtered = filtered.sort_values('Pass Percent', ascending=False)

# ---------- Plotly chart: school pass % (horizontal bar) ----------
fig = px.bar(
    filtered,
    x='Pass Percent',
    y='Name of the School',
    orientation='h',
    text='Pass_Label',
    title=f'SSC Pass Percentage ({year})',
    color='Pass Percent',
    color_continuous_scale='Blues',
    height=max(400, len(filtered) * 25)
)
fig.update_traces(textposition='outside', textfont_size=12)
fig.update_xaxes(range=[0, 105])
fig.update_layout(
    yaxis={'categoryorder': 'total ascending'},
    margin=dict(l=300, r=100, t=100, b=80),
    yaxis_title='',
    xaxis_title='Pass Percentage (%)',
    font=dict(size=11),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# ---------- Timeline: School Performance Over Years ----------
st.markdown("---")
st.subheader("📈 School Performance Timeline")

school = st.selectbox(
    "Select School for Timeline View",
    sorted(df['Name of the School'].unique()),
    key="school_selector"
)

school_timeline = df[df['Name of the School'] == school].sort_values('Year')

if not school_timeline.empty:
    col1, col2 = st.columns(2)
    
    with col1:
        # Timeline: Candidates Appeared vs Passed
        fig_timeline = px.line(
            school_timeline,
            x='Year',
            y=['Candidates Appeared', 'Total Pass'],
            markers=True,
            title=f'{school} – Appeared vs Passed Over Time',
            labels={'value': 'Count', 'variable': 'Category'},
            height=400
        )
        fig_timeline.update_traces(mode='lines+markers', hovertemplate='<b>%{fullData.name}</b><br>Year: %{x}<br>Count: %{y}<extra></extra>', textposition='top center', texttemplate='%{y:.0f}', textfont_size=10)
        fig_timeline.update_layout(
            hovermode='x unified'
        )
        fig_timeline.update_xaxes(dtick=1)
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    with col2:
        # Timeline: Pass Percentage Trend
        fig_pass_pct = px.line(
            school_timeline,
            x='Year',
            y='Pass Percent',
            markers=True,
            title=f'{school} – Pass Percentage Trend',
            labels={'Pass Percent': 'Pass %'},
            height=400,
            line_shape='spline',
            text='Pass Percent'
        )
        fig_pass_pct.update_traces(
            mode='lines+markers+text',
            line_color='#1f77b4',
            marker_size=8,
            texttemplate='%{text:.1f}%',
            textposition='top center',
            hovertemplate='Year: %{x}<br>Pass %: %{y:.1f}%<extra></extra>'
        )
        fig_pass_pct.update_xaxes(dtick=1)
        fig_pass_pct.update_yaxes(range=[0, 105])
        st.plotly_chart(fig_pass_pct, use_container_width=True)
    
    # Performance Table
    st.markdown("**Performance Details:**")
    display_cols = ['Year', 'Candidates Appeared', 'Total Pass', 'Pass Percent', 'Distin-ction', 'Grade I', 'Grade II']
    st.dataframe(school_timeline[display_cols].style.format({
        'Pass Percent': '{:.1f}%',
        'Candidates Appeared': '{:.0f}',
        'Total Pass': '{:.0f}'
    }), use_container_width=True)
else:
    st.info(f"No timeline data available for {school}.")

# ---------- Top Schools by Average Pass % (Last 5 Years) ----------
st.markdown("---")

# Calculate dynamic year range (last 5 years)
max_year = df['Year'].max()
min_year = max_year - 4
years_range = list(range(min_year, max_year + 1))
year_range_str = f"{min_year}-{max_year}"

st.subheader(f"🏆 Top Schools by Average Pass % ({year_range_str})")

# Filter data for last 5 years and aggregate
avg_data = df[df['Year'].isin(years_range)].groupby('Name of the School').agg({
    'Pass Percent': 'mean',
    'Candidates Appeared': 'sum',
    'Total Pass': 'sum'
}).reset_index()
avg_data.columns = ['School', 'Avg Pass %', 'Total Appeared', 'Total Passed']

# Apply school filter if schools are selected
if schools:
    avg_data = avg_data[avg_data['School'].isin(schools)].copy()

# Sort all schools in descending order by average pass percentage
avg_data_sorted = avg_data.sort_values('Avg Pass %', ascending=True)

if not avg_data_sorted.empty:
    # Visualization
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_all = px.bar(
            avg_data_sorted,
            x='Avg Pass %',
            y='School',
            orientation='h',
            title=f'All Schools – Average Pass % ({year_range_str})',
            color='Avg Pass %',
            color_continuous_scale='blues',
            height=max(400, len(avg_data_sorted) * 20)
        )
        fig_all.update_layout(
            yaxis_title='',
            xaxis_title='Average Pass % (%)',
            margin=dict(l=250, r=50, t=80, b=60),
            xaxis=dict(range=[0, 105])
        )
        fig_all.update_traces(textposition='outside', texttemplate='%{x:.1f}%')
        st.plotly_chart(fig_all, use_container_width=True)
    
    with col2:
        st.markdown("**Summary:**")
        st.metric("Top School", avg_data_sorted.iloc[0]['School'][:40])
        st.metric("Avg Pass %", f"{avg_data_sorted.iloc[0]['Avg Pass %']:.1f}%")
        st.metric("Total Schools", len(avg_data_sorted))
        st.metric("Total Students", int(avg_data_sorted['Total Appeared'].sum()))
else:
    st.info("No data available for the last 5 years.")

# ---------- Optional: raw data table ----------
with st.expander("📋 Show raw data for selected year"):
    st.dataframe(filtered.drop(columns='Pass_Label'))