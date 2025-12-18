"""
Streamlit App for PhonePe Pulse Data Analysis
Digital Payment Growth Analysis in India
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import sys
import os

# Add scripts directory to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from scripts.data_processor import PhonePeDataProcessor
from scripts.visualizations import PhonePeVisualizations

# Page configuration
st.set_page_config(
    page_title="PhonePe Pulse Analysis",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        padding-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">📱 PhonePe Pulse Analysis</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Digital Payment Growth Analysis in India</p>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio("Choose a page", ["Dashboard", "Year-wise Growth", "State Analysis", "Interactive Map"])

# Load data
@st.cache_data
def load_data():
    processor = PhonePeDataProcessor(data_dir='data')
    processor.load_sample_data()
    processed_data = processor.process_data()
    return processed_data, processor.raw_data

processed_data, raw_data = load_data()

# Dashboard Page
if page == "Dashboard":
    st.header("📈 Overview Dashboard")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    yearly_summary = processed_data['yearly_summary']
    state_summary = processed_data['state_summary']
    
    with col1:
        st.metric("Total States", len(state_summary))
    with col2:
        st.metric("Year Range", f"{yearly_summary['Year'].min()}-{yearly_summary['Year'].max()}")
    with col3:
        total_trans = yearly_summary['Transactions'].sum()
        st.metric("Total Transactions", f"{total_trans/1e6:.1f}M")
    with col4:
        total_amount = yearly_summary['Amount'].sum()
        st.metric("Total Amount", f"₹{total_amount/1e12:.2f}T")
    
    st.divider()
    
    # Charts in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Year-wise Transaction Growth")
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=yearly_summary['Year'],
            y=yearly_summary['Transactions'],
            mode='lines+markers',
            name='Transactions',
            line=dict(color='#2E86AB', width=3),
            marker=dict(size=10)
        ))
        fig1.update_layout(
            xaxis_title="Year",
            yaxis_title="Total Transactions",
            height=400,
            hovermode='x unified'
        )
        fig1.update_yaxes(tickformat=".0f")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("Transaction Amount Growth")
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=yearly_summary['Year'],
            y=yearly_summary['Amount'],
            name='Amount',
            marker_color='#F18F01'
        ))
        fig2.update_layout(
            xaxis_title="Year",
            yaxis_title="Total Amount (INR)",
            height=400,
            hovermode='x unified'
        )
        fig2.update_yaxes(tickformat="₹.2s")
        st.plotly_chart(fig2, use_container_width=True)
    
    # Top States
    st.subheader("Top 10 States by Transactions")
    top_states = state_summary.head(10)
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        x=top_states['Transactions'],
        y=top_states['State'],
        orientation='h',
        marker_color='#06A77D',
        text=[f"{x/1e6:.1f}M" for x in top_states['Transactions']],
        textposition='outside'
    ))
    fig3.update_layout(
        xaxis_title="Total Transactions",
        yaxis_title="State",
        height=500,
        yaxis={'categoryorder': 'total ascending'}
    )
    fig3.update_xaxes(tickformat=".0f")
    st.plotly_chart(fig3, use_container_width=True)

# Year-wise Growth Page
elif page == "Year-wise Growth":
    st.header("📅 Year-wise Growth Analysis")
    
    yearly_summary = processed_data['yearly_summary']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Transaction Volume Growth")
        fig = px.line(
            yearly_summary,
            x='Year',
            y='Transactions',
            markers=True,
            title='Year-wise Transaction Growth',
            labels={'Transactions': 'Total Transactions', 'Year': 'Year'}
        )
        fig.update_traces(line_color='#2E86AB', line_width=3, marker_size=10)
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Transaction Amount Growth")
        fig = px.bar(
            yearly_summary,
            x='Year',
            y='Amount',
            title='Year-wise Amount Growth',
            labels={'Amount': 'Total Amount (INR)', 'Year': 'Year'},
            color='Amount',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Growth statistics
    st.subheader("Growth Statistics")
    first_year = yearly_summary.iloc[0]
    last_year = yearly_summary.iloc[-1]
    trans_growth = ((last_year['Transactions'] - first_year['Transactions']) / first_year['Transactions']) * 100
    amount_growth = ((last_year['Amount'] - first_year['Amount']) / first_year['Amount']) * 100
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Transaction Growth", f"{trans_growth:.1f}%", 
                 f"{last_year['Transactions'] - first_year['Transactions']:,.0f}")
    with col2:
        st.metric("Amount Growth", f"{amount_growth:.1f}%",
                 f"₹{(last_year['Amount'] - first_year['Amount'])/1e9:.2f}B")

# State Analysis Page
elif page == "State Analysis":
    st.header("🗺️ State-wise Analysis")
    
    state_summary = processed_data['state_summary']
    
    # Top N selector
    top_n = st.slider("Select number of top states", 5, 29, 10)
    
    top_states = state_summary.head(top_n)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"Top {top_n} States by Transactions")
        fig = px.bar(
            top_states,
            x='Transactions',
            y='State',
            orientation='h',
            title=f'Top {top_n} States',
            labels={'Transactions': 'Total Transactions', 'State': 'State'},
            color='Transactions',
            color_continuous_scale='Greens'
        )
        fig.update_layout(height=600, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader(f"Top {top_n} States by Amount")
        fig = px.bar(
            top_states,
            x='Amount',
            y='State',
            orientation='h',
            title=f'Top {top_n} States by Amount',
            labels={'Amount': 'Total Amount (INR)', 'State': 'State'},
            color='Amount',
            color_continuous_scale='Oranges'
        )
        fig.update_layout(height=600, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    
    # State selector for detailed view
    st.subheader("State Details")
    selected_state = st.selectbox("Select a state", state_summary['State'].tolist())
    state_data = state_summary[state_summary['State'] == selected_state].iloc[0]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Transactions", f"{state_data['Transactions']/1e6:.2f}M")
    with col2:
        st.metric("Total Amount", f"₹{state_data['Amount']/1e9:.2f}B")
    with col3:
        avg_amount = state_data['Amount'] / state_data['Transactions']
        st.metric("Avg Transaction", f"₹{avg_amount:.2f}")

# Interactive Map Page
elif page == "Interactive Map":
    st.header("🗺️ India: State-wise Digital Payment Transactions")
    st.markdown("**Choropleth Map Visualization**")
    
    state_summary = processed_data['state_summary']
    
    # State coordinates for India
    state_coords = {
        'Andhra Pradesh': [15.9129, 79.7400],
        'Arunachal Pradesh': [28.2180, 94.7278],
        'Assam': [26.2006, 92.9376],
        'Bihar': [25.0961, 85.3131],
        'Chhattisgarh': [21.2787, 81.8661],
        'Goa': [15.2993, 74.1240],
        'Gujarat': [23.0225, 72.5714],
        'Haryana': [29.0588, 76.0856],
        'Himachal Pradesh': [31.1048, 77.1734],
        'Jharkhand': [23.6102, 85.2799],
        'Karnataka': [15.3173, 75.7139],
        'Kerala': [10.8505, 76.2711],
        'Madhya Pradesh': [22.9734, 78.6569],
        'Maharashtra': [19.7515, 75.7139],
        'Manipur': [24.6637, 93.9063],
        'Meghalaya': [25.4670, 91.3662],
        'Mizoram': [23.1645, 92.9376],
        'Nagaland': [26.1584, 94.5624],
        'Odisha': [20.9517, 85.0985],
        'Punjab': [30.7333, 76.7794],
        'Rajasthan': [27.0238, 74.2179],
        'Sikkim': [27.5330, 88.5122],
        'Tamil Nadu': [11.1271, 78.6569],
        'Telangana': [18.1124, 79.0193],
        'Tripura': [23.9408, 91.9882],
        'Uttar Pradesh': [26.8467, 80.9462],
        'Uttarakhand': [30.0668, 79.0193],
        'West Bengal': [22.9868, 87.8550],
        'Delhi': [28.6139, 77.2090]
    }
    
    # Prepare data for map
    map_data = state_summary.copy()
    map_data['Lat'] = map_data['State'].map(lambda x: state_coords.get(x, [0, 0])[0])
    map_data['Lon'] = map_data['State'].map(lambda x: state_coords.get(x, [0, 0])[1])
    
    # Create PhonePe Pulse style 3D map with vertical bars
    st.subheader("Interactive 3D Map Visualization")
    
    max_trans = map_data['Transactions'].max()
    min_trans = map_data['Transactions'].min()
    
    # Create 3D scatter map with height representing transaction volume
    fig = go.Figure()
    
    # Normalize transaction values for bar height (0 to 1 scale)
    normalized_trans = (map_data['Transactions'] - min_trans) / (max_trans - min_trans)
    
    # Create color mapping (Blue -> Yellow -> Orange -> Red like PhonePe)
    colors = []
    for val in normalized_trans:
        if val < 0.25:
            colors.append('#4A90E2')  # Light blue
        elif val < 0.5:
            colors.append('#F5D76E')  # Yellow
        elif val < 0.75:
            colors.append('#F39C12')  # Orange
        else:
            colors.append('#E74C3C')  # Red
    
    # Add 3D bars using scattergeo with size representing height
    fig.add_trace(go.Scattergeo(
        lon=map_data['Lon'],
        lat=map_data['Lat'],
        text=map_data['State'] + '<br>Transactions: ' + (map_data['Transactions']/1e6).round(2).astype(str) + 'M' +
             '<br>Amount: ₹' + (map_data['Amount']/1e9).round(2).astype(str) + 'B' +
             '<br>Volume: ' + (normalized_trans * 100).round(1).astype(str) + '%',
        mode='markers',
        marker=dict(
            size=normalized_trans * 80 + 20,  # Size represents bar height
            color=map_data['Transactions'],
            colorscale=[[0, '#4A90E2'], [0.25, '#4A90E2'], [0.25, '#F5D76E'], 
                       [0.5, '#F5D76E'], [0.5, '#F39C12'], [0.75, '#F39C12'],
                       [0.75, '#E74C3C'], [1, '#E74C3C']],  # PhonePe color gradient
            showscale=True,
            colorbar=dict(
                title=dict(
                    text="Transactions<br>(Millions)",
                    font=dict(size=14, color='#333')
                ),
                len=0.7,
                y=0.5,
                thickness=25,
                tickfont=dict(size=11, color='#666'),
                tickformat='.1f'
            ),
            line=dict(width=2, color='rgba(255,255,255,0.8)'),
            opacity=0.85,
            sizemode='diameter'
        ),
        name='States',
        hovertemplate='<b>%{text}</b><extra></extra>'
    ))
    
    # Configure map with dark purple background like PhonePe
    fig.update_geos(
        visible=True,
        resolution=50,
        showcountries=True,
        countrycolor="rgba(255,255,255,0.3)",
        countrywidth=1.5,
        showsubunits=True,
        subunitcolor="rgba(255,255,255,0.2)",
        subunitwidth=1,
        showland=True,
        landcolor="#2C2C54",  # Dark purple
        showocean=True,
        oceancolor="#1a1a3e",  # Darker purple
        showlakes=True,
        lakecolor="#1a1a3e",
        center=dict(lat=20.5937, lon=78.9629),
        projection_type="mercator",
        projection_scale=4.5,
        lonaxis_range=[68, 98],
        lataxis_range=[6, 37],
        bgcolor='#1a1a3e',  # PhonePe dark purple background
        coastlinecolor="rgba(255,255,255,0.2)",
        coastlinewidth=1
    )
    
    fig.update_layout(
        title={
            'text': 'India: State-wise Digital Payment Transactions<br><sub>PhonePe Pulse 3D Style Visualization</sub>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 22, 'color': '#ffffff', 'family': 'Arial, sans-serif'}
        },
        height=800,
        margin=dict(l=0, r=0, t=100, b=0),
        paper_bgcolor='#1a1a3e',  # Dark purple background
        plot_bgcolor='#1a1a3e',
        font=dict(color='#ffffff')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add summary metrics in PhonePe style
    col1, col2, col3, col4 = st.columns(4)
    
    total_trans = state_summary['Transactions'].sum()
    total_amount = state_summary['Amount'].sum()
    avg_trans = total_amount / total_trans
    
    with col1:
        st.metric(
            "Total Transactions",
            f"{total_trans/1e9:.2f}B",
            help="All transactions across India"
        )
    with col2:
        st.metric(
            "Total Payment Value",
            f"₹{total_amount/1e12:.2f}T",
            help="Total amount in transactions"
        )
    with col3:
        st.metric(
            "Avg Transaction Value",
            f"₹{avg_trans:.2f}",
            help="Average transaction amount"
        )
    with col4:
        st.metric(
            "States Covered",
            f"{len(state_summary)}",
            help="Number of states/UTs"
        )
    
    st.success("✅ 3D Map loaded successfully! Bar height and color represent transaction volume.")
    st.info("💡 **PhonePe Pulse Style**: Vertical bar height and color intensity represent transaction volume. Blue (low) → Yellow → Orange → Red (high).")
    
    # Add data table below map
    st.subheader("State-wise Data Table")
    display_data = state_summary[['State', 'Transactions', 'Amount']].copy()
    display_data['Transactions (M)'] = (display_data['Transactions'] / 1e6).round(2)
    display_data['Amount (B)'] = (display_data['Amount'] / 1e9).round(2)
    display_data = display_data[['State', 'Transactions (M)', 'Amount (B)']]
    st.dataframe(display_data, use_container_width=True, height=400)

# Footer
st.markdown("---")
st.markdown("**PhonePe Pulse: Digital Payment Growth Analysis in India** | Built with Streamlit")

