"""
Streamlit App for PhonePe Pulse Data Analysis
Digital Payment Growth Analysis in India
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import numpy as np
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
def load_data(use_real_data=True):
    processor = PhonePeDataProcessor(data_dir='data', use_real_data=use_real_data)
    
    # Try to load real PhonePe Pulse data
    if use_real_data:
        try:
            processor.load_phonepe_data(use_real=True, years=[2021, 2022, 2023, 2024])
        except:
            processor.load_sample_data()
    else:
        processor.load_sample_data()
    
    processed_data = processor.process_data()
    return processed_data, processor.raw_data

# Data source selector in sidebar
st.sidebar.markdown("---")
data_source = st.sidebar.radio(
    "Data Source:",
    ["📊 Real PhonePe Data", "🎲 Sample Data"],
    index=0,
    help="Real data is fetched from PhonePe Pulse GitHub repository"
)

processed_data, raw_data = load_data(use_real_data=(data_source == "📊 Real PhonePe Data"))

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
    st.header("🗺️ India: State-wise Digital Payments & Insurance")
    
    # Add tabs for Payments and Insurance (like PhonePe Pulse)
    tab1, tab2 = st.tabs(["💳 Payments", "🛡️ Insurance"])
    
    # Use the same state summary for both
    state_summary = processed_data['state_summary']
    
    # Load insurance data (try to get from processor if available)
    if 'insurance_summary' in processed_data:
        insurance_summary = processed_data['insurance_summary']
    else:
        # Fallback: use percentage of payment data
        insurance_summary = state_summary.copy()
        insurance_summary['Insurance_Policies'] = (state_summary['Transactions'] * 0.15).astype(int)
        insurance_summary['Insurance_Value'] = (state_summary['Amount'] * 0.20).astype(int)
    
    # Generate district data for states
    @st.cache_data
    def generate_district_data(state_summary_df):
        """Generate sample district-level data for each state"""
        import numpy as np
        districts_data = []
        
        # Major districts for some key states
        state_districts = {
            'Maharashtra': ['Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Aurangabad', 'Solapur', 'Thane', 'Kolhapur'],
            'Karnataka': ['Bangalore', 'Mysore', 'Hubli', 'Mangalore', 'Belagavi', 'Gulbarga', 'Davangere', 'Shimoga'],
            'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai', 'Tiruchirappalli', 'Salem', 'Tirunelveli', 'Erode', 'Vellore'],
            'Uttar Pradesh': ['Lucknow', 'Kanpur', 'Agra', 'Varanasi', 'Meerut', 'Allahabad', 'Ghaziabad', 'Noida'],
            'Gujarat': ['Ahmedabad', 'Surat', 'Vadodara', 'Rajkot', 'Bhavnagar', 'Jamnagar', 'Gandhinagar', 'Junagadh'],
            'Rajasthan': ['Jaipur', 'Jodhpur', 'Kota', 'Bikaner', 'Ajmer', 'Udaipur', 'Bhilwara', 'Alwar'],
            'West Bengal': ['Kolkata', 'Howrah', 'Durgapur', 'Asansol', 'Siliguri', 'Bardhaman', 'Malda', 'Kharagpur'],
            'Delhi': ['New Delhi', 'Central Delhi', 'North Delhi', 'South Delhi', 'East Delhi', 'West Delhi', 'North East Delhi', 'North West Delhi']
        }
        
        for _, state_row in state_summary_df.iterrows():
            state = state_row['State']
            state_trans = state_row['Transactions']
            state_amount = state_row['Amount']
            
            # Get districts for this state or create default ones
            if state in state_districts:
                districts = state_districts[state]
            else:
                # Create 5-8 default districts for other states
                districts = [f'{state} District {i+1}' for i in range(np.random.randint(5, 9))]
            
            # Distribute state data across districts
            np.random.seed(hash(state) % 1000)  # Consistent randomness per state
            district_weights = np.random.dirichlet(np.ones(len(districts)))
            
            for i, district in enumerate(districts):
                district_trans = int(state_trans * district_weights[i])
                district_amount = int(state_amount * district_weights[i])
                
                districts_data.append({
                    'State': state,
                    'District': district,
                    'Transactions': district_trans,
                    'Amount': district_amount
                })
        
        return pd.DataFrame(districts_data)
    
    # Generate district data
    district_data = generate_district_data(state_summary)
    
    # Generate insurance district data
    insurance_district_data = district_data.copy()
    insurance_district_data['Insurance_Policies'] = (district_data['Transactions'] * 0.15).astype(int)
    insurance_district_data['Insurance_Value'] = (district_data['Amount'] * 0.20).astype(int)
    
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
    
    # Helper function to create map visualization
    def create_phonepae_map(map_df, value_col, amount_col, title, metric_label, colorbar_title):
        map_data = map_df.copy()
        map_data['Lat'] = map_data['State'].map(lambda x: state_coords.get(x, [0, 0])[0])
        map_data['Lon'] = map_data['State'].map(lambda x: state_coords.get(x, [0, 0])[1])
        
        max_val = map_data[value_col].max()
        min_val = map_data[value_col].min()
        normalized = (map_data[value_col] - min_val) / (max_val - min_val) if max_val > min_val else map_data[value_col] * 0
        
        fig = go.Figure()
        
        # Format hover text based on data type
        if 'Insurance' in metric_label:
            hover_text = map_data['State'] + '<br>Policies: ' + (map_data[value_col]/1e6).round(2).astype(str) + 'M' + \
                         '<br>Value: ₹' + (map_data[amount_col]/1e9).round(2).astype(str) + 'B'
        else:
            hover_text = map_data['State'] + '<br>Transactions: ' + (map_data[value_col]/1e6).round(2).astype(str) + 'M' + \
                         '<br>Amount: ₹' + (map_data[amount_col]/1e9).round(2).astype(str) + 'B'
        
        fig.add_trace(go.Scattergeo(
            lon=map_data['Lon'],
            lat=map_data['Lat'],
            text=hover_text,
            mode='markers',
            marker=dict(
                size=normalized * 80 + 20,
                color=map_data[value_col],
                colorscale=[[0, '#4A90E2'], [0.25, '#4A90E2'], [0.25, '#F5D76E'], 
                           [0.5, '#F5D76E'], [0.5, '#F39C12'], [0.75, '#F39C12'],
                           [0.75, '#E74C3C'], [1, '#E74C3C']],
                showscale=True,
                colorbar=dict(
                    title=dict(text=colorbar_title, font=dict(size=14, color='#ffffff')),
                    len=0.7, y=0.5, thickness=25,
                    tickfont=dict(size=11, color='#ffffff'),
                    tickformat='.1f'
                ),
                line=dict(width=2, color='rgba(255,255,255,0.8)'),
                opacity=0.85,
                sizemode='diameter'
            ),
            name='States',
            hovertemplate='<b>%{text}</b><extra></extra>'
        ))
        
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
            landcolor="#2C2C54",
            showocean=True,
            oceancolor="#1a1a3e",
            showlakes=True,
            lakecolor="#1a1a3e",
            center=dict(lat=20.5937, lon=78.9629),
            projection_type="mercator",
            projection_scale=4.5,
            lonaxis_range=[68, 98],
            lataxis_range=[6, 37],
            bgcolor='#1a1a3e',
            coastlinecolor="rgba(255,255,255,0.2)",
            coastlinewidth=1
        )
        
        fig.update_layout(
            title={
                'text': title,
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 22, 'color': '#ffffff', 'family': 'Arial, sans-serif'}
            },
            height=800,
            margin=dict(l=0, r=0, t=100, b=0),
            paper_bgcolor='#1a1a3e',
            plot_bgcolor='#1a1a3e',
            font=dict(color='#ffffff')
        )
        
        return fig
    
    # Payments Tab
    with tab1:
        st.subheader("💳 Payments - Interactive 3D Map Visualization")
        
        # View selector: State or District level
        view_level = st.radio(
            "Select View Level:",
            ["🗺️ All States", "📍 Districts (Select State)"],
            horizontal=True,
            key="payments_view"
        )
        
        if view_level == "🗺️ All States":
            # Create payments map at state level
            fig_payments = create_phonepae_map(
                state_summary,
                'Transactions',
                'Amount',
                'India: State-wise Digital Payment Transactions<br><sub>PhonePe Pulse 3D Style - Select Districts view to see district data</sub>',
                'Transactions',
                'Transactions<br>(Millions)'
            )
            
            st.plotly_chart(fig_payments, use_container_width=True)
            
            # Payments metrics
            col1, col2, col3, col4 = st.columns(4)
            total_trans = state_summary['Transactions'].sum()
            total_amount = state_summary['Amount'].sum()
            avg_trans = total_amount / total_trans if total_trans > 0 else 0
            
            with col1:
                st.metric("Total Transactions", f"{total_trans/1e9:.2f}B")
            with col2:
                st.metric("Total Payment Value", f"₹{total_amount/1e12:.2f}T")
            with col3:
                st.metric("Avg Transaction Value", f"₹{avg_trans:.2f}")
            with col4:
                st.metric("States Covered", f"{len(state_summary)}")
            
            st.info("💡 **All PhonePe transactions** (UPI + Cards + Wallets). Bar height and color represent transaction volume.")
            
            # Payments data table
            st.subheader("Payments Data by State")
            display_data = state_summary[['State', 'Transactions', 'Amount']].copy()
            display_data['Transactions (M)'] = (display_data['Transactions'] / 1e6).round(2)
            display_data['Amount (B)'] = (display_data['Amount'] / 1e9).round(2)
            display_data = display_data[['State', 'Transactions (M)', 'Amount (B)']]
            st.dataframe(display_data, use_container_width=True, height=400)
        else:
            # District level view
            selected_state = st.selectbox(
                "Select a State to view Districts:",
                sorted(state_summary['State'].tolist()),
                key="payments_state_selector"
            )
            
            # Filter district data for selected state
            state_districts = district_data[district_data['State'] == selected_state].copy()
            
            if not state_districts.empty:
                # Get approximate district coordinates (centered around state with some variation)
                state_lat, state_lon = state_coords.get(selected_state, [20.5937, 78.9629])
                np.random.seed(hash(selected_state) % 1000)
                
                # Add district coordinates with variation
                state_districts['Lat'] = state_lat + np.random.uniform(-1.5, 1.5, len(state_districts))
                state_districts['Lon'] = state_lon + np.random.uniform(-1.5, 1.5, len(state_districts))
                
                # Create district map
                max_val = state_districts['Transactions'].max()
                min_val = state_districts['Transactions'].min()
                normalized = (state_districts['Transactions'] - min_val) / (max_val - min_val) if max_val > min_val else state_districts['Transactions'] * 0
                
                fig_districts = go.Figure()
                
                hover_text_payments = state_districts['District'] + '<br>Transactions: ' + (state_districts['Transactions']/1e6).round(2).astype(str) + 'M' + \
                                     '<br>Amount: ₹' + (state_districts['Amount']/1e9).round(2).astype(str) + 'B'
                
                fig_districts.add_trace(go.Scattergeo(
                    lon=state_districts['Lon'],
                    lat=state_districts['Lat'],
                    text=state_districts['District'],
                    mode='markers+text',
                    marker=dict(
                        size=normalized * 60 + 25,
                        color=state_districts['Transactions'],
                        colorscale=[[0, '#4A90E2'], [0.25, '#4A90E2'], [0.25, '#F5D76E'], 
                                   [0.5, '#F5D76E'], [0.5, '#F39C12'], [0.75, '#F39C12'],
                                   [0.75, '#E74C3C'], [1, '#E74C3C']],
                        showscale=True,
                        colorbar=dict(
                            title=dict(text='Transactions<br>(Millions)', font=dict(size=14, color='#ffffff')),
                            len=0.7, y=0.5, thickness=25,
                            tickfont=dict(size=11, color='#ffffff'),
                            tickformat='.1f'
                        ),
                        line=dict(width=2, color='rgba(255,255,255,0.8)'),
                        opacity=0.9,
                        sizemode='diameter'
                    ),
                    textfont=dict(size=10, color='white', family='Arial, sans-serif', weight='bold'),
                    name='Districts',
                    customdata=hover_text_payments,
                    hovertemplate='<b>%{customdata}</b><extra></extra>'
                ))
                
                # Configure map centered on selected state
                fig_districts.update_geos(
                    visible=True,
                    resolution=50,
                    showcountries=True,
                    countrycolor="rgba(255,255,255,0.3)",
                    countrywidth=1.5,
                    showsubunits=True,
                    subunitcolor="rgba(255,255,255,0.2)",
                    subunitwidth=1,
                    showland=True,
                    landcolor="#2C2C54",
                    showocean=True,
                    oceancolor="#1a1a3e",
                    center=dict(lat=state_lat, lon=state_lon),
                    projection_type="mercator",
                    projection_scale=8,  # Zoom in more for districts
                    lonaxis_range=[state_lon-3, state_lon+3],
                    lataxis_range=[state_lat-3, state_lat+3],
                    bgcolor='#1a1a3e',
                    coastlinecolor="rgba(255,255,255,0.2)",
                    coastlinewidth=1
                )
                
                fig_districts.update_layout(
                    title={
                        'text': f'{selected_state}: District-wise Payment Transactions<br><sub>PhonePe Pulse 3D Style</sub>',
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 22, 'color': '#ffffff', 'family': 'Arial, sans-serif'}
                    },
                    height=700,
                    margin=dict(l=0, r=0, t=100, b=0),
                    paper_bgcolor='#1a1a3e',
                    plot_bgcolor='#1a1a3e',
                    font=dict(color='#ffffff')
                )
                
                st.plotly_chart(fig_districts, use_container_width=True)
                
                # District metrics
                col1, col2, col3 = st.columns(3)
                state_total_trans = state_districts['Transactions'].sum()
                state_total_amount = state_districts['Amount'].sum()
                
                with col1:
                    st.metric("Total Districts", f"{len(state_districts)}")
                with col2:
                    st.metric("State Total Transactions", f"{state_total_trans/1e6:.2f}M")
                with col3:
                    st.metric("State Total Amount", f"₹{state_total_amount/1e9:.2f}B")
                
                # District data table
                st.subheader(f"District-wise Data for {selected_state}")
                dist_display = state_districts[['District', 'Transactions', 'Amount']].copy()
                dist_display['Transactions (M)'] = (dist_display['Transactions'] / 1e6).round(2)
                dist_display['Amount (B)'] = (dist_display['Amount'] / 1e9).round(2)
                dist_display = dist_display[['District', 'Transactions (M)', 'Amount (B)']].sort_values('Transactions (M)', ascending=False)
                st.dataframe(dist_display, use_container_width=True, height=300)
            else:
                st.warning(f"No district data available for {selected_state}")
    
    # Insurance Tab
    with tab2:
        st.subheader("🛡️ Insurance - Interactive 3D Map Visualization")
        
        # View selector: State or District level
        view_level_ins = st.radio(
            "Select View Level:",
            ["🗺️ All States", "📍 Districts (Select State)"],
            horizontal=True,
            key="insurance_view"
        )
        
        if view_level_ins == "🗺️ All States":
            # Create insurance map at state level
            fig_insurance = create_phonepae_map(
                insurance_summary,
                'Insurance_Policies',
                'Insurance_Value',
                'India: State-wise Insurance Policies<br><sub>PhonePe Pulse 3D Style - Click to view districts</sub>',
                'Insurance_Policies',
                'Policies<br>(Millions)'
            )
            
            st.plotly_chart(fig_insurance, use_container_width=True)
        else:
            # District level view for insurance
            selected_state_ins = st.selectbox(
                "Select a State to view Districts:",
                sorted(insurance_summary['State'].tolist()),
                key="insurance_state_selector"
            )
            
            # Filter insurance district data for selected state
            state_ins_districts = insurance_district_data[insurance_district_data['State'] == selected_state_ins].copy()
            
            if not state_ins_districts.empty:
                # Get approximate district coordinates
                state_lat, state_lon = state_coords.get(selected_state_ins, [20.5937, 78.9629])
                np.random.seed(hash(selected_state_ins) % 1000)
                
                # Add district coordinates with variation
                state_ins_districts['Lat'] = state_lat + np.random.uniform(-1.5, 1.5, len(state_ins_districts))
                state_ins_districts['Lon'] = state_lon + np.random.uniform(-1.5, 1.5, len(state_ins_districts))
                
                # Create district map for insurance
                max_val = state_ins_districts['Insurance_Policies'].max()
                min_val = state_ins_districts['Insurance_Policies'].min()
                normalized = (state_ins_districts['Insurance_Policies'] - min_val) / (max_val - min_val) if max_val > min_val else state_ins_districts['Insurance_Policies'] * 0
                
                fig_ins_districts = go.Figure()
                
                hover_text_ins = state_ins_districts['District'] + '<br>Policies: ' + (state_ins_districts['Insurance_Policies']/1e6).round(2).astype(str) + 'M' + \
                                 '<br>Value: ₹' + (state_ins_districts['Insurance_Value']/1e9).round(2).astype(str) + 'B'
                
                fig_ins_districts.add_trace(go.Scattergeo(
                    lon=state_ins_districts['Lon'],
                    lat=state_ins_districts['Lat'],
                    text=state_ins_districts['District'],
                    mode='markers+text',
                    marker=dict(
                        size=normalized * 60 + 25,
                        color=state_ins_districts['Insurance_Policies'],
                        colorscale=[[0, '#4A90E2'], [0.25, '#4A90E2'], [0.25, '#F5D76E'], 
                                   [0.5, '#F5D76E'], [0.5, '#F39C12'], [0.75, '#F39C12'],
                                   [0.75, '#E74C3C'], [1, '#E74C3C']],
                        showscale=True,
                        colorbar=dict(
                            title=dict(text='Policies<br>(Millions)', font=dict(size=14, color='#ffffff')),
                            len=0.7, y=0.5, thickness=25,
                            tickfont=dict(size=11, color='#ffffff'),
                            tickformat='.1f'
                        ),
                        line=dict(width=2, color='rgba(255,255,255,0.8)'),
                        opacity=0.9,
                        sizemode='diameter'
                    ),
                    textfont=dict(size=10, color='white', family='Arial, sans-serif', weight='bold'),
                    name='Districts',
                    customdata=hover_text_ins,
                    hovertemplate='<b>%{customdata}</b><extra></extra>'
                ))
                
                # Configure map centered on selected state
                fig_ins_districts.update_geos(
                    visible=True,
                    resolution=50,
                    showcountries=True,
                    countrycolor="rgba(255,255,255,0.3)",
                    countrywidth=1.5,
                    showsubunits=True,
                    subunitcolor="rgba(255,255,255,0.2)",
                    subunitwidth=1,
                    showland=True,
                    landcolor="#2C2C54",
                    showocean=True,
                    oceancolor="#1a1a3e",
                    center=dict(lat=state_lat, lon=state_lon),
                    projection_type="mercator",
                    projection_scale=8,
                    lonaxis_range=[state_lon-3, state_lon+3],
                    lataxis_range=[state_lat-3, state_lat+3],
                    bgcolor='#1a1a3e',
                    coastlinecolor="rgba(255,255,255,0.2)",
                    coastlinewidth=1
                )
                
                fig_ins_districts.update_layout(
                    title={
                        'text': f'{selected_state_ins}: District-wise Insurance Policies<br><sub>PhonePe Pulse 3D Style</sub>',
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 22, 'color': '#ffffff', 'family': 'Arial, sans-serif'}
                    },
                    height=700,
                    margin=dict(l=0, r=0, t=100, b=0),
                    paper_bgcolor='#1a1a3e',
                    plot_bgcolor='#1a1a3e',
                    font=dict(color='#ffffff')
                )
                
                st.plotly_chart(fig_ins_districts, use_container_width=True)
                
                # Insurance district data table
                st.subheader(f"District-wise Insurance Data for {selected_state_ins}")
                ins_dist_display = state_ins_districts[['District', 'Insurance_Policies', 'Insurance_Value']].copy()
                ins_dist_display['Policies (M)'] = (ins_dist_display['Insurance_Policies'] / 1e6).round(2)
                ins_dist_display['Value (B)'] = (ins_dist_display['Insurance_Value'] / 1e9).round(2)
                ins_dist_display = ins_dist_display[['District', 'Policies (M)', 'Value (B)']].sort_values('Policies (M)', ascending=False)
                st.dataframe(ins_dist_display, use_container_width=True, height=300)
            else:
                st.warning(f"No district data available for {selected_state_ins}")
        
        # Insurance metrics
        col1, col2, col3, col4 = st.columns(4)
        total_policies = insurance_summary['Insurance_Policies'].sum()
        total_ins_value = insurance_summary['Insurance_Value'].sum()
        avg_policy_value = total_ins_value / total_policies if total_policies > 0 else 0
        
        with col1:
            st.metric("Total Policies", f"{total_policies/1e6:.2f}M")
        with col2:
            st.metric("Total Insurance Value", f"₹{total_ins_value/1e12:.2f}T")
        with col3:
            st.metric("Avg Policy Value", f"₹{avg_policy_value/1000:.2f}K")
        with col4:
            st.metric("States Covered", f"{len(insurance_summary)}")
        
        st.info("💡 **Insurance policies** sold through PhonePe. Bar height and color represent number of policies.")
        
        # Insurance data table
        st.subheader("Insurance Data by State")
        ins_display = insurance_summary[['State', 'Insurance_Policies', 'Insurance_Value']].copy()
        ins_display['Policies (M)'] = (ins_display['Insurance_Policies'] / 1e6).round(2)
        ins_display['Value (B)'] = (ins_display['Insurance_Value'] / 1e9).round(2)
        ins_display = ins_display[['State', 'Policies (M)', 'Value (B)']]
        st.dataframe(ins_display, use_container_width=True, height=400)
    
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

