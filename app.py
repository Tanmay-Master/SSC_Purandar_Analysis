import streamlit as st
import pandas as pd
import plotly.express as px
from school_marathi_mapping import get_marathi_name

# ---------- Page config ----------
st.set_page_config(page_title="SSC School Comparison", layout="wide")
st.title("🏫 School‑wise Pass Percentage Comparison (SSC)")

# ---------- High-quality image download config ----------
# ADJUST IMAGE DIMENSIONS HERE:
# 'height': increase/decrease downloaded image height (pixels)
# 'width': increase/decrease downloaded image width (pixels)
# 'scale': 1=normal, 2=2x resolution (sharper), 3=3x resolution (highest quality)
HIGH_QUALITY_CONFIG = {
    'toImageButtonOptions': {
        'format': 'png',
        'filename': 'school_analysis',
        'height': 1000,  # Increase for taller images
        'width': 2500,   # Increase for wider images
        'scale': 3       # 3x resolution for maximum quality
    }
}

# ---------- Load data (cached for speed) ----------
@st.cache_data
def load_data():
    # Change filename to match your SSC CSV file
    df = pd.read_csv("combined_ssc_data.csv")
    df['Year'] = df['Year'].astype(int)
    # Add Marathi name column
    df['School_Marathi'] = df['Name of the School'].apply(get_marathi_name)
    return df

df = load_data()

# ---------- Sidebar filter ----------
with st.sidebar:
    st.header("🔍 Filters")
    
    # Language toggle
    show_marathi = st.checkbox("मराठीमध्ये (Show in Marathi)", value=True)
    
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
        key="school_filter",
        format_func=lambda x: get_marathi_name(x) if show_marathi else x
    )

# ---------- Filter data ----------
filtered = df[df['Year'] == year].copy()

# Apply school filter if schools are selected
if schools:
    filtered = filtered[filtered['Name of the School'].isin(schools)].copy()

if filtered.empty:
    st.warning(f"No data available for the year {year}.")
    st.stop()

# Add display column based on language preference
filtered['Display_Name'] = filtered['School_Marathi'] if show_marathi else filtered['Name of the School']

filtered['Pass_Label'] = filtered['Pass Percent'].apply(lambda x: f"{x:.1f}%")
filtered = filtered.sort_values('Pass Percent', ascending=False)

# ---------- Plotly chart: school pass % (horizontal bar) ----------
fig = px.bar(
    filtered,
    x='Pass Percent',
    y='Display_Name',
    orientation='h',
    text='Pass_Label',
    title=f'SSC Pass Percentage ({year})',
    color='Pass Percent',
    color_continuous_scale='Blues',
    height=max(400, len(filtered) * 25)
)
fig.update_traces(textposition='outside', textfont_size=16)
fig.update_xaxes(range=[0, 105])
fig.update_layout(
    yaxis={'categoryorder': 'total ascending'},
    margin=dict(l=400, r=100, t=100, b=80),
    yaxis_title='',
    xaxis_title='Pass Percentage (%)',
    font=dict(size=18, family='Arial Black'),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True, config=HIGH_QUALITY_CONFIG)

# ---------- Timeline: School Performance Over Years ----------
st.markdown("---")
st.subheader("📈 School Performance Timeline")

school = st.selectbox(
    "Select School for Timeline View",
    sorted(df['Name of the School'].unique()),
    key="school_selector",
    format_func=lambda x: get_marathi_name(x)  # Display Marathi name
)

school_timeline = df[df['Name of the School'] == school].sort_values('Year')
school_display = get_marathi_name(school) if show_marathi else school

if not school_timeline.empty:
    col1, col2 = st.columns(2)
    
    with col1:
        # Timeline: Candidates Appeared vs Passed
        fig_timeline = px.line(
            school_timeline,
            x='Year',
            y=['Candidates Appeared', 'Total Pass'],
            markers=True,
            title=f'{school_display} – Appeared vs Passed Over Time',
            labels={'value': 'Count', 'variable': 'Category'},
            height=400
        )
        fig_timeline.update_traces(mode='lines+markers', hovertemplate='<b>%{fullData.name}</b><br>Year: %{x}<br>Count: %{y}<extra></extra>', textposition='top center', texttemplate='%{y:.0f}', textfont_size=14)
        fig_timeline.update_layout(
            hovermode='x unified',
            font=dict(size=16, family='Arial Black')
        )
        fig_timeline.update_xaxes(dtick=1)
        st.plotly_chart(fig_timeline, use_container_width=True, config=HIGH_QUALITY_CONFIG)
    
    with col2:
        # Timeline: Pass Percentage Trend
        fig_pass_pct = px.line(
            school_timeline,
            x='Year',
            y='Pass Percent',
            markers=True,
            title=f'{school_display} – Pass Percentage Trend',
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
            textfont_size=14,
            hovertemplate='Year: %{x}<br>Pass %: %{y:.1f}%<extra></extra>'
        )
        fig_pass_pct.update_xaxes(dtick=1)
        fig_pass_pct.update_yaxes(range=[0, 105])
        fig_pass_pct.update_layout(font=dict(size=16, family='Arial Black'))
        st.plotly_chart(fig_pass_pct, use_container_width=True, config=HIGH_QUALITY_CONFIG)
    
    # Performance Table
    st.markdown("**Performance Details:**")
    display_cols = ['Year', 'Candidates Appeared', 'Total Pass', 'Pass Percent', 'Distin-ction', 'Grade I', 'Grade II']
    st.dataframe(school_timeline[display_cols].style.format({
        'Pass Percent': '{:.1f}%',
        'Candidates Appeared': '{:.0f}',
        'Total Pass': '{:.0f}'
    }), use_container_width=True)
else:
    st.info(f"No timeline data available for {school_display}.")

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

# Add Marathi names
avg_data['School_Marathi'] = avg_data['School'].apply(get_marathi_name)
# Add display column based on language preference
avg_data['Display_Name'] = avg_data['School_Marathi'] if show_marathi else avg_data['School']

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
            y='Display_Name',
            orientation='h',
            title=f'All Schools – Average Pass % ({year_range_str})',
            color='Avg Pass %',
            color_continuous_scale='blues',
            height=max(400, len(avg_data_sorted) * 20)
        )
        fig_all.update_layout(
            yaxis_title='',
            xaxis_title='Average Pass % (%)',
            margin=dict(l=400, r=50, t=80, b=60),
            xaxis=dict(range=[0, 105]),
            font=dict(size=18, family='Arial Black')
        )
        fig_all.update_traces(textposition='outside', texttemplate='%{x:.1f}%', textfont_size=14)
        st.plotly_chart(fig_all, use_container_width=True, config=HIGH_QUALITY_CONFIG)
    
    with col2:
        st.markdown("**Summary:**")
        top_school_display = avg_data_sorted.iloc[-1]['Display_Name']
        st.metric("Top School", top_school_display[:30])
        st.metric("Avg Pass %", f"{avg_data_sorted.iloc[-1]['Avg Pass %']:.1f}%")
        st.metric("Total Schools", len(avg_data_sorted))
        st.metric("Total Students", int(avg_data_sorted['Total Appeared'].sum()))
else:
    st.info("No data available for the last 5 years.")

# ---------- CLUSTER ANALYSIS: High/Medium/Low Performers ----------
st.markdown("---")
st.subheader("📊 Cluster Analysis: School Performance Categories")

# Create clusters based on average pass percentage
cluster_data = df[df['Year'].isin(years_range)].copy()
cluster_stats = cluster_data.groupby('Name of the School').agg({
    'Pass Percent': ['mean', 'std', 'min', 'max'],
    'Candidates Appeared': 'sum',
    'Total Pass': 'sum'
}).reset_index()
cluster_stats.columns = ['School', 'Avg_Pass', 'Std_Pass', 'Min_Pass', 'Max_Pass', 'Total_Appeared', 'Total_Passed']
cluster_stats['School_Marathi'] = cluster_stats['School'].apply(get_marathi_name)
cluster_stats['Display_Name'] = cluster_stats['School_Marathi'] if show_marathi else cluster_stats['School']

# Define cluster thresholds using percentiles (for balanced distribution)
percentile_33 = cluster_stats['Avg_Pass'].quantile(0.33)
percentile_67 = cluster_stats['Avg_Pass'].quantile(0.67)

# Create clusters based on percentiles
def assign_cluster_percentile(pass_pct):
    if pass_pct >= percentile_67:
        return 'High Performers'
    elif pass_pct >= percentile_33:
        return 'Medium Performers'
    else:
        return 'Low Performers'

cluster_stats['Cluster'] = cluster_stats['Avg_Pass'].apply(assign_cluster_percentile)

# Cluster colors
cluster_colors = {
    'High Performers': '#2ecc71',      # Green
    'Medium Performers': '#f39c12',    # Orange
    'Low Performers': '#e74c3c'        # Red
}

col1, col2, col3 = st.columns(3)

with col1:
    cluster_counts = cluster_stats['Cluster'].value_counts()
    high_count = cluster_counts.get('High Performers', 0)
    st.metric("🟢 High Performers", f"{high_count} ({percentile_67:.1f}%+)")

with col2:
    medium_count = cluster_counts.get('Medium Performers', 0)
    st.metric("🟠 Medium Performers", f"{medium_count} ({percentile_33:.1f}%-{percentile_67:.1f}%)")

with col3:
    low_count = cluster_counts.get('Low Performers', 0)
    st.metric("🔴 Low Performers", f"{low_count} (<{percentile_33:.1f}%)")

# Row 1: Pie Chart and Box Plot
col1, col2 = st.columns(2)

with col1:
    # Pie Chart: Distribution of clusters
    fig_pie = px.pie(
        cluster_stats,
        names='Cluster',
        values=cluster_stats['Cluster'].map(cluster_stats['Cluster'].value_counts()),
        title='School Distribution by Performance Category',
        color='Cluster',
        color_discrete_map=cluster_colors,
        hole=0.3
    )
    fig_pie.update_traces(hovertemplate='<b>%{label}</b><br>Count: %{customdata}<extra></extra>', customdata=cluster_stats['Cluster'].map(cluster_stats['Cluster'].value_counts()))
    st.plotly_chart(fig_pie, use_container_width=True, config=HIGH_QUALITY_CONFIG)

with col2:
    # Box Plot: Pass Percentage Distribution by Cluster
    fig_box = px.box(
        cluster_stats,
        y='Cluster',
        x='Avg_Pass',
        title='Average Pass % Distribution by Cluster',
        color='Cluster',
        color_discrete_map=cluster_colors,
        points='all',
        hover_data={'Display_Name': True, 'Avg_Pass': ':.1f'},
        category_orders={'Cluster': ['Low Performers', 'Medium Performers', 'High Performers']}
    )
    fig_box.update_layout(
        yaxis_title='',
        xaxis_title='Average Pass %',
        height=400,
        showlegend=False,
        font=dict(size=14, family='Arial Black')
    )
    st.plotly_chart(fig_box, use_container_width=True, config=HIGH_QUALITY_CONFIG)

# Row 2: Scatter Plot and Performance Comparison
col1, col2 = st.columns(2)

with col1:
    # Scatter plot: Consistency vs Average Performance
    fig_scatter = px.scatter(
        cluster_stats,
        x='Avg_Pass',
        y='Std_Pass',
        size='Total_Appeared',
        color='Cluster',
        hover_name='Display_Name',
        hover_data={'Avg_Pass': ':.1f', 'Std_Pass': ':.1f', 'Total_Appeared': True},
        title='Performance Consistency: Average vs Standard Deviation',
        labels={'Avg_Pass': 'Avg Pass %', 'Std_Pass': 'Std Dev'},
        color_discrete_map=cluster_colors,
        size_max=60
    )
    fig_scatter.update_layout(
        height=400,
        showlegend=False,
        font=dict(size=14, family='Arial Black')
    )
    st.plotly_chart(fig_scatter, use_container_width=True, config=HIGH_QUALITY_CONFIG)

with col2:
    # Violin plot: Year-wise Pass Percentage by Cluster
    year_cluster = df[df['Year'].isin(years_range)].copy()
    year_cluster['Avg_School_Pass'] = year_cluster.groupby('Name of the School')['Pass Percent'].transform('mean')
    year_cluster['School_Cluster'] = year_cluster['Avg_School_Pass'].apply(assign_cluster_percentile)
    
    fig_violin = px.violin(
        year_cluster,
        x='School_Cluster',
        y='Pass Percent',
        title='Pass % Distribution Over Years',
        color='School_Cluster',
        color_discrete_map=cluster_colors,
        category_orders={'School_Cluster': ['Low Performers', 'Medium Performers', 'High Performers']},
        points=False,
        box=True
    )
    fig_violin.update_layout(
        xaxis_title='',
        yaxis_title='Pass %',
        height=400,
        showlegend=False,
        font=dict(size=14, family='Arial Black')
    )
    st.plotly_chart(fig_violin, use_container_width=True, config=HIGH_QUALITY_CONFIG)

# Cluster Details Table
st.markdown("### 📋 Detailed Cluster Analysis")

cluster_display = cluster_stats[['Display_Name', 'Cluster', 'Avg_Pass', 'Std_Pass', 'Min_Pass', 'Max_Pass', 'Total_Appeared', 'Total_Passed']].copy()
cluster_display.columns = ['School', 'Cluster', 'Avg Pass %', 'Std Dev', 'Min %', 'Max %', 'Total Students', 'Total Passed']
cluster_display = cluster_display.sort_values('Avg Pass %', ascending=False)

# Create styled dataframe
styled_df = cluster_display.style.format({
    'Avg Pass %': '{:.1f}%',
    'Std Dev': '{:.2f}',
    'Min %': '{:.1f}%',
    'Max %': '{:.1f}%',
    'Total Students': '{:.0f}',
    'Total Passed': '{:.0f}'
}).background_gradient(
    subset=['Avg Pass %'],
    cmap='RdYlGn',
    vmin=0,
    vmax=100
)

st.dataframe(styled_df, use_container_width=True)

# Cluster Summary Statistics
st.markdown("### 📈 Cluster Summary Statistics")

summary_stats = []
for cluster in ['High Performers', 'Medium Performers', 'Low Performers']:
    cluster_subset = cluster_stats[cluster_stats['Cluster'] == cluster]
    if len(cluster_subset) > 0:
        summary_stats.append({
            'Cluster': cluster,
            'Count': len(cluster_subset),
            'Avg Pass %': f"{cluster_subset['Avg_Pass'].mean():.1f}%",
            'Min': f"{cluster_subset['Avg_Pass'].min():.1f}%",
            'Max': f"{cluster_subset['Avg_Pass'].max():.1f}%",
            'Total Students': int(cluster_subset['Total_Appeared'].sum()),
            'Total Passed': int(cluster_subset['Total_Passed'].sum())
        })

summary_df = pd.DataFrame(summary_stats)
st.dataframe(summary_df, use_container_width=True, hide_index=True)

# ---------- Optional: raw data table ----------
with st.expander("📋 Show raw data for selected year"):
    st.dataframe(filtered.drop(columns='Pass_Label'))