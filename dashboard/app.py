"""
PhonePe Pulse Data Visualization Dashboard
Interactive Streamlit dashboard with geo-visualization and insights
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database.db_connection import get_db_connection

# Page configuration
st.set_page_config(
    page_title="PhonePe Pulse Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #5f27cd;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #5f27cd;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False


@st.cache_data(ttl=300)
def load_data_from_db():
    """
    Load all data from MySQL database.
    
    Returns:
        dict: Dictionary of DataFrames
    """
    connection = None
    try:
        connection = get_db_connection()
        data = {}
        
        # Load aggregated transactions
        query = "SELECT * FROM aggregated_transactions"
        data['transactions'] = pd.read_sql(query, connection)
        
        # Load aggregated users
        query = "SELECT * FROM aggregated_users"
        data['users'] = pd.read_sql(query, connection)
        
        # Load map transactions
        query = "SELECT * FROM map_transactions"
        data['map_transactions'] = pd.read_sql(query, connection)
        
        # Load map users
        query = "SELECT * FROM map_users"
        data['map_users'] = pd.read_sql(query, connection)
        
        # Load top transactions
        query = "SELECT * FROM top_transactions"
        data['top_transactions'] = pd.read_sql(query, connection)
        
        # Load top users
        query = "SELECT * FROM top_users"
        data['top_users'] = pd.read_sql(query, connection)
        
        return data
    except Exception as e:
        st.error(f"Error loading data from database: {e}")
        return None
    finally:
        if connection and connection.is_connected():
            connection.close()


def main():
    """Main dashboard application."""
    
    # Header
    st.markdown('<h1 class="main-header">📊 PhonePe Pulse Data Visualization Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    data = load_data_from_db()
    
    if data is None or data['transactions'].empty:
        st.error("⚠️ No data found in database. Please run the ETL pipeline first using: python main.py")
        st.info("Make sure you have:")
        st.info("1. MySQL database set up")
        st.info("2. .env file configured with database credentials")
        st.info("3. Run main.py to populate the database")
        return
    
    # Sidebar filters - 10+ Interactive Dropdown Options
    st.sidebar.header("🔍 Filters & Options")
    
    # Dropdown 1: Year filter
    years = sorted(data['transactions']['year'].unique(), reverse=True)
    selected_year = st.sidebar.selectbox("1️⃣ Select Year", years, index=0)
    
    # Dropdown 2: Quarter filter
    quarters = sorted(data['transactions'][data['transactions']['year'] == selected_year]['quarter'].unique())
    selected_quarter = st.sidebar.selectbox("2️⃣ Select Quarter", quarters, index=len(quarters)-1)
    
    # Dropdown 3: State filter
    states = ['All'] + sorted(data['map_transactions']['state'].unique().tolist())
    selected_state = st.sidebar.selectbox("3️⃣ Select State", states)
    
    # Dropdown 4: District filter (conditional on state)
    districts = ['All']
    if selected_state != 'All':
        state_districts = data['map_transactions'][data['map_transactions']['state'] == selected_state]['district'].unique().tolist()
        districts = ['All'] + sorted([d for d in state_districts if d and d != selected_state])
    selected_district = st.sidebar.selectbox("4️⃣ Select District", districts)
    
    # Dropdown 5: Transaction type filter
    transaction_types = ['All'] + sorted(data['transactions']['transaction_type'].unique().tolist())
    selected_transaction_type = st.sidebar.selectbox("5️⃣ Select Transaction Type", transaction_types)
    
    # Dropdown 6: Metric type filter
    metric_types = ['Transaction Amount', 'Transaction Count', 'Registered Users', 'App Opens', 'All Metrics']
    selected_metric = st.sidebar.selectbox("6️⃣ Select Primary Metric", metric_types)
    
    # Dropdown 7: Chart type for geo visualization
    geo_chart_types = ['Scatter Map', 'Choropleth Map (if available)', 'Bar Chart', 'Both Map and Chart']
    selected_geo_chart = st.sidebar.selectbox("7️⃣ Geo Visualization Type", geo_chart_types)
    
    # Dropdown 8: Top N selection
    top_n_options = [5, 10, 15, 20, 25, 'All']
    selected_top_n = st.sidebar.selectbox("8️⃣ Show Top N Items", top_n_options)
    
    # Dropdown 9: Color scheme
    color_schemes = ['Viridis', 'Plasma', 'Inferno', 'Blues', 'Reds', 'Greens', 'Oranges', 'Purples', 'Rainbow']
    selected_color_scheme = st.sidebar.selectbox("9️⃣ Color Scheme", color_schemes)
    
    # Dropdown 10: View mode
    view_modes = ['Summary View', 'Detailed View', 'Comparison View', 'Trend Analysis']
    selected_view_mode = st.sidebar.selectbox("🔟 View Mode", view_modes)
    
    # Dropdown 11: Aggregation method
    aggregation_methods = ['Sum', 'Average', 'Maximum', 'Minimum', 'Count']
    selected_aggregation = st.sidebar.selectbox("1️⃣1️⃣ Aggregation Method", aggregation_methods)
    
    # Dropdown 12: Time period comparison
    time_comparison = ['Single Period', 'Compare with Previous Quarter', 'Compare with Previous Year', 'Year-over-Year']
    selected_time_comparison = st.sidebar.selectbox("1️⃣2️⃣ Time Comparison", time_comparison)
    
    # Filter data based on selections
    filtered_transactions = data['transactions'][
        (data['transactions']['year'] == selected_year) &
        (data['transactions']['quarter'] == selected_quarter)
    ]
    
    if selected_transaction_type != 'All':
        filtered_transactions = filtered_transactions[
            filtered_transactions['transaction_type'] == selected_transaction_type
        ]
    
    filtered_users = data['users'][
        (data['users']['year'] == selected_year) &
        (data['users']['quarter'] == selected_quarter)
    ]
    
    filtered_map_transactions = data['map_transactions'][
        (data['map_transactions']['year'] == selected_year) &
        (data['map_transactions']['quarter'] == selected_quarter)
    ]
    
    if selected_state != 'All':
        filtered_map_transactions = filtered_map_transactions[
            filtered_map_transactions['state'] == selected_state
        ]
        
    if selected_district != 'All' and selected_district in filtered_map_transactions['district'].values:
        filtered_map_transactions = filtered_map_transactions[
            filtered_map_transactions['district'] == selected_district
        ]
    
    filtered_map_users = data['map_users'][
        (data['map_users']['year'] == selected_year) &
        (data['map_users']['quarter'] == selected_quarter)
    ]
    
    if selected_state != 'All':
        filtered_map_users = filtered_map_users[
            filtered_map_users['state'] == selected_state
        ]
        
    if selected_district != 'All' and selected_district in filtered_map_users['district'].values:
        filtered_map_users = filtered_map_users[
            filtered_map_users['district'] == selected_district
        ]
    
    # Helper function to get pandas aggregation function
    def get_agg_func(method='Sum'):
        if method == 'Sum':
            return 'sum'
        elif method == 'Average':
            return 'mean'
        elif method == 'Maximum':
            return 'max'
        elif method == 'Minimum':
            return 'min'
        elif method == 'Count':
            return 'count'
        return 'sum'
    
    # Dashboard Info Section
    with st.expander("ℹ️ Dashboard Features & Controls", expanded=False):
        st.info("""
        **Interactive Dashboard with 12+ Dropdown Options:**
        
        1. **Year Selection** - Filter data by specific year
        2. **Quarter Selection** - Select quarter (Q1-Q4)
        3. **State Selection** - Filter by Indian state
        4. **District Selection** - Filter by district (when state selected)
        5. **Transaction Type** - Filter by transaction category
        6. **Primary Metric** - Choose main metric to display
        7. **Geo Visualization Type** - Select map display type
        8. **Top N Items** - Control how many top items to show
        9. **Color Scheme** - Choose visualization color palette
        10. **View Mode** - Summary, Detailed, Comparison, or Trend view
        11. **Aggregation Method** - Sum, Average, Max, Min, or Count
        12. **Time Comparison** - Compare across time periods
        
        **Features:**
        - Live geo visualization with interactive maps
        - Dynamic data updates from MySQL database
        - Multiple chart types and visualizations
        - Responsive and user-friendly interface
        - Real-time filtering and analysis
        """)
    
    # Key Metrics
    st.header("📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    total_transaction_amount = filtered_transactions['transaction_amount'].sum() / 1e9  # Convert to billions
    total_transaction_count = filtered_transactions['transaction_count'].sum() / 1e6  # Convert to millions
    total_registered_users = filtered_users['registered_users'].sum() / 1e6  # Convert to millions
    total_app_opens = filtered_users['app_opens'].sum() / 1e9  # Convert to billions
    
    with col1:
        st.metric("Total Transaction Amount", f"₹{total_transaction_amount:.2f}B")
    with col2:
        st.metric("Total Transaction Count", f"{total_transaction_count:.2f}M")
    with col3:
        st.metric("Total Registered Users", f"{total_registered_users:.2f}M")
    with col4:
        st.metric("Total App Opens", f"{total_app_opens:.2f}B")
    
    st.markdown("---")
    
    # INSIGHT 1: Geo Visualization - Transaction Amount by State
    st.header("🗺️ Insight 1: Transaction Amount by State (Geo Visualization)")
    
    if not filtered_map_transactions.empty:
        # Apply aggregation method
        agg_func = get_agg_func(selected_aggregation)
        state_transaction_data = filtered_map_transactions.groupby('state').agg({
            'transaction_amount': agg_func,
            'transaction_count': agg_func
        }).reset_index()
        
        # Indian state coordinates (approximate centers) - comprehensive mapping
        state_coords = {
            'andhra pradesh': (15.9129, 79.7400),
            'arunachal pradesh': (28.2180, 94.7278),
            'assam': (26.2006, 92.9376),
            'bihar': (25.0961, 85.3131),
            'chhattisgarh': (21.2787, 81.8661),
            'goa': (15.2993, 74.1240),
            'gujarat': (23.0225, 72.5714),
            'haryana': (29.0588, 76.0856),
            'himachal pradesh': (31.1048, 77.1734),
            'jharkhand': (23.6102, 85.2799),
            'karnataka': (15.3173, 75.7139),
            'kerala': (10.8505, 76.2711),
            'madhya pradesh': (22.9734, 78.6569),
            'maharashtra': (19.7515, 75.7139),
            'manipur': (24.6637, 93.9063),
            'meghalaya': (25.4670, 91.3662),
            'mizoram': (23.1645, 92.9376),
            'nagaland': (26.1584, 94.5624),
            'odisha': (20.9517, 85.0985),
            'punjab': (31.1471, 75.3412),
            'rajasthan': (27.0238, 74.2179),
            'sikkim': (27.5330, 88.5122),
            'tamil nadu': (11.1271, 78.6569),
            'telangana': (18.1124, 79.0193),
            'tripura': (23.9408, 91.9882),
            'uttar pradesh': (26.8467, 80.9462),
            'uttarakhand': (30.0668, 79.0193),
            'west bengal': (22.9868, 87.8550),
            'andaman and nicobar islands': (11.7401, 92.6586),
            'andaman & nicobar islands': (11.7401, 92.6586),
            'chandigarh': (30.7333, 76.7794),
            'dadra and nagar haveli and daman and diu': (20.1809, 73.0169),
            'dadra & nagar haveli & daman & diu': (20.1809, 73.0169),
            'delhi': (28.6139, 77.2090),
            'jammu and kashmir': (34.0837, 74.7973),
            'jammu & kashmir': (34.0837, 74.7973),
            'ladakh': (34.1526, 77.5770),
            'lakshadweep': (10.5667, 72.6417),
            'puducherry': (11.9416, 79.8083),
            # Also add title case versions for safety
            'Andhra Pradesh': (15.9129, 79.7400),
            'Arunachal Pradesh': (28.2180, 94.7278),
            'Assam': (26.2006, 92.9376),
            'Bihar': (25.0961, 85.3131),
            'Chhattisgarh': (21.2787, 81.8661),
            'Goa': (15.2993, 74.1240),
            'Gujarat': (23.0225, 72.5714),
            'Haryana': (29.0588, 76.0856),
            'Himachal Pradesh': (31.1048, 77.1734),
            'Jharkhand': (23.6102, 85.2799),
            'Karnataka': (15.3173, 75.7139),
            'Kerala': (10.8505, 76.2711),
            'Madhya Pradesh': (22.9734, 78.6569),
            'Maharashtra': (19.7515, 75.7139),
            'Manipur': (24.6637, 93.9063),
            'Meghalaya': (25.4670, 91.3662),
            'Mizoram': (23.1645, 92.9376),
            'Nagaland': (26.1584, 94.5624),
            'Odisha': (20.9517, 85.0985),
            'Punjab': (31.1471, 75.3412),
            'Rajasthan': (27.0238, 74.2179),
            'Sikkim': (27.5330, 88.5122),
            'Tamil Nadu': (11.1271, 78.6569),
            'Telangana': (18.1124, 79.0193),
            'Tripura': (23.9408, 91.9882),
            'Uttar Pradesh': (26.8467, 80.9462),
            'Uttarakhand': (30.0668, 79.0193),
            'West Bengal': (22.9868, 87.8550),
            'Andaman And Nicobar Islands': (11.7401, 92.6586),
            'Chandigarh': (30.7333, 76.7794),
            'Dadra And Nagar Haveli And Daman And Diu': (20.1809, 73.0169),
            'Delhi': (28.6139, 77.2090),
            'Jammu And Kashmir': (34.0837, 74.7973),
            'Ladakh': (34.1526, 77.5770),
            'Lakshadweep': (10.5667, 72.6417),
            'Puducherry': (11.9416, 79.8083)
        }
        
        # Normalize state names and map to coordinates (handle both lowercase and title case)
        def get_coords(state_name):
            if not state_name:
                return None, None
            state_lower = str(state_name).lower().strip()
            state_title = str(state_name).title().strip()
            # Try lowercase first, then title case, then original
            coords = state_coords.get(state_lower) or state_coords.get(state_title) or state_coords.get(state_name)
            if coords:
                return coords
            return None, None
        
        state_transaction_data['lat'] = state_transaction_data['state'].apply(lambda x: get_coords(x)[0])
        state_transaction_data['lon'] = state_transaction_data['state'].apply(lambda x: get_coords(x)[1])
        
        # Don't filter by Top N for geo map - show ALL states with data
        # Only apply Top N filter to bar chart below
        geo_data = state_transaction_data.dropna(subset=['lat', 'lon']).copy()
        
        # Debug info (optional, can be removed later)
        if selected_view_mode == 'Detailed View':
            st.info(f"📍 Found coordinates for {len(geo_data)} states out of {len(state_transaction_data)} total states in data.")
        
        # Show map based on selected chart type
        if selected_geo_chart in ['Scatter Map', 'Both Map and Chart']:
            if not geo_data.empty:
                # Create scatter geo map
                fig = px.scatter_geo(
                    geo_data,
                    lat='lat',
                    lon='lon',
                    size='transaction_amount',
                    color='transaction_amount',
                    hover_name='state',
                    hover_data={'transaction_amount': ':,.0f', 'transaction_count': ':,.0f', 'lat': False, 'lon': False},
                    size_max=50,
                    color_continuous_scale=selected_color_scheme.lower(),
                    title=f'Transaction Amount by State - Geo Map ({selected_aggregation}) (Q{selected_quarter} {selected_year})',
                    projection='natural earth'
                )
                
                # Set map center to India with proper geo settings
                fig.update_geos(
                    center=dict(lat=20, lon=77),
                    projection_scale=4,
                    visible=True,
                    showcountries=True,
                    showcoastlines=True,
                    showland=True,
                    countrycolor='lightgray',
                    coastlinecolor='gray',
                    landcolor='lightyellow',
                    bgcolor='lightblue',
                    lataxis_range=[6, 37],  # India's latitude range
                    lonaxis_range=[68, 98]   # India's longitude range
                )
                
                fig.update_layout(
                    height=700,
                    margin=dict(l=0, r=0, t=50, b=0)
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        # Show bar chart based on selection
        if selected_geo_chart in ['Bar Chart', 'Both Map and Chart']:
            st.subheader("Bar Chart View")
            display_data = state_transaction_data.sort_values('transaction_amount', ascending=False).copy()
            # Apply Top N filter only for bar chart, not for map
            if selected_top_n != 'All':
                display_data = display_data.head(selected_top_n)
            else:
                # If "All" selected, still show all states but sorted
                display_data = display_data.head(50)  # Limit to reasonable number for display
            fig_bar = px.bar(
                display_data,
                x='state',
                y='transaction_amount',
                title=f'Transaction Amount by State - Bar Chart ({selected_aggregation}) (Q{selected_quarter} {selected_year})',
                labels={'transaction_amount': 'Transaction Amount (₹)', 'state': 'State'},
                color='transaction_amount',
                color_continuous_scale=selected_color_scheme.lower()
            )
            fig_bar.update_layout(height=500, xaxis_tickangle=-45)
            st.plotly_chart(fig_bar, use_container_width=True)
    
    # INSIGHT 2: Transaction Count by State
    st.header("📊 Insight 2: Transaction Count by State")
    
    if not filtered_map_transactions.empty:
        agg_func = get_agg_func(selected_aggregation)
        state_count_data = filtered_map_transactions.groupby('state').agg({
            'transaction_count': agg_func
        }).reset_index().sort_values('transaction_count', ascending=False)
        
        display_count = selected_top_n if selected_top_n != 'All' else 10
        top_label = f'Top {display_count}' if selected_top_n != 'All' else 'Top 10'
        
        fig = px.pie(
            state_count_data.head(display_count),
            values='transaction_count',
            names='state',
            title=f'{top_label} States by Transaction Count ({selected_aggregation}) (Q{selected_quarter} {selected_year})',
            color_discrete_sequence=getattr(px.colors.sequential, selected_color_scheme, px.colors.sequential.Viridis)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # INSIGHT 3: Registered Users by State
    st.header("👥 Insight 3: Registered Users by State")
    
    if not filtered_map_users.empty:
        agg_func = get_agg_func(selected_aggregation)
        state_user_data = filtered_map_users.groupby('state').agg({
            'registered_users': agg_func
        }).reset_index().sort_values('registered_users', ascending=False)
        
        display_users = selected_top_n if selected_top_n != 'All' else 15
        top_label_users = f'Top {display_users}' if selected_top_n != 'All' else 'Top 15'
        
        fig = px.bar(
            state_user_data.head(display_users),
            x='state',
            y='registered_users',
            title=f'{top_label_users} States by Registered Users ({selected_aggregation}) (Q{selected_quarter} {selected_year})',
            labels={'registered_users': 'Registered Users', 'state': 'State'},
            color='registered_users',
            color_continuous_scale=selected_color_scheme.lower()
        )
        fig.update_layout(height=500, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    # INSIGHT 4: App Opens by State
    st.header("📱 Insight 4: App Opens by State")
    
    if not filtered_map_users.empty:
        state_app_data = filtered_map_users.groupby('state').agg({
            'app_opens': 'sum',
            'registered_users': 'sum'
        }).reset_index().sort_values('app_opens', ascending=False)
        
        fig = px.scatter(
            state_app_data,
            x='registered_users',
            y='app_opens',
            size='app_opens',
            color='state',
            title=f'App Opens vs Registered Users by State (Q{selected_quarter} {selected_year})',
            labels={'app_opens': 'App Opens', 'registered_users': 'Registered Users'},
            hover_data=['state']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # INSIGHT 5: Top N States by Transaction Amount
    top_n_label = f'Top {selected_top_n}' if selected_top_n != 'All' else 'All'
    st.header(f"🏆 Insight 5: {top_n_label} States by Transaction Amount")
    
    if not filtered_map_transactions.empty:
        agg_func = get_agg_func(selected_aggregation)
        top_states = filtered_map_transactions.groupby('state').agg({
            'transaction_amount': agg_func
        }).reset_index().sort_values('transaction_amount', ascending=False)
        
        if selected_top_n != 'All':
            top_states = top_states.head(selected_top_n)
        
        fig = px.bar(
            top_states,
            x='state',
            y='transaction_amount',
            title=f'{top_n_label} States by Transaction Amount ({selected_aggregation}) (Q{selected_quarter} {selected_year})',
            labels={'transaction_amount': 'Transaction Amount (₹)', 'state': 'State'},
            color='transaction_amount',
            color_continuous_scale=selected_color_scheme.lower()
        )
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Display table
        if selected_view_mode in ['Detailed View', 'Comparison View']:
            st.dataframe(top_states, use_container_width=True)
    
    # INSIGHT 6: Top N Districts
    top_n_label_dist = f'Top {selected_top_n}' if selected_top_n != 'All' else 'All'
    st.header(f"📍 Insight 6: {top_n_label_dist} Districts")
    
    if not filtered_map_transactions.empty:
        agg_func = get_agg_func(selected_aggregation)
        top_districts = filtered_map_transactions.groupby(['state', 'district']).agg({
            'transaction_amount': agg_func,
            'transaction_count': agg_func
        }).reset_index().sort_values('transaction_amount', ascending=False)
        
        if selected_top_n != 'All':
            top_districts = top_districts.head(selected_top_n)
        
        fig = px.bar(
            top_districts,
            x='district',
            y='transaction_amount',
            color='state',
            title=f'{top_n_label_dist} Districts by Transaction Amount ({selected_aggregation}) (Q{selected_quarter} {selected_year})',
            labels={'transaction_amount': 'Transaction Amount (₹)', 'district': 'District'},
            barmode='group',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    # INSIGHT 7: Year-wise Growth
    st.header("📈 Insight 7: Year-wise Growth Trend")
    
    if not data['transactions'].empty:
        year_wise_data = data['transactions'].groupby('year').agg({
            'transaction_amount': 'sum',
            'transaction_count': 'sum'
        }).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=year_wise_data['year'],
            y=year_wise_data['transaction_amount'] / 1e9,
            mode='lines+markers',
            name='Transaction Amount (₹B)',
            line=dict(color='#5f27cd', width=3)
        ))
        fig.add_trace(go.Scatter(
            x=year_wise_data['year'],
            y=year_wise_data['transaction_count'] / 1e6,
            mode='lines+markers',
            name='Transaction Count (M)',
            line=dict(color='#00d2d3', width=3),
            yaxis='y2'
        ))
        fig.update_layout(
            title='Year-wise Growth Trend',
            xaxis_title='Year',
            yaxis_title='Transaction Amount (₹ Billions)',
            yaxis2=dict(title='Transaction Count (Millions)', overlaying='y', side='right'),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # INSIGHT 8: Quarter-wise Comparison
    st.header("📅 Insight 8: Quarter-wise Comparison")
    
    if not data['transactions'].empty:
        quarter_data = data['transactions'][data['transactions']['year'] == selected_year].groupby('quarter').agg({
            'transaction_amount': 'sum',
            'transaction_count': 'sum'
        }).reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                quarter_data,
                x='quarter',
                y='transaction_amount',
                title=f'Quarter-wise Transaction Amount ({selected_year})',
                labels={'transaction_amount': 'Transaction Amount (₹)', 'quarter': 'Quarter'},
                color='transaction_amount',
                color_continuous_scale='Greens'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(
                quarter_data,
                x='quarter',
                y='transaction_count',
                title=f'Quarter-wise Transaction Count ({selected_year})',
                labels={'transaction_count': 'Transaction Count', 'quarter': 'Quarter'},
                markers=True
            )
            fig.update_traces(line_color='#ff6348', line_width=3)
            st.plotly_chart(fig, use_container_width=True)
    
    # INSIGHT 9: Transaction Type Distribution
    st.header("💳 Insight 9: Transaction Type Distribution")
    
    if not filtered_transactions.empty:
        transaction_type_data = filtered_transactions.groupby('transaction_type').agg({
            'transaction_amount': 'sum',
            'transaction_count': 'sum'
        }).reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(
                transaction_type_data,
                values='transaction_amount',
                names='transaction_type',
                title=f'Transaction Amount by Type (Q{selected_quarter} {selected_year})'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                transaction_type_data.sort_values('transaction_count', ascending=False),
                x='transaction_type',
                y='transaction_count',
                title=f'Transaction Count by Type (Q{selected_quarter} {selected_year})',
                labels={'transaction_count': 'Transaction Count', 'transaction_type': 'Transaction Type'},
                color='transaction_count',
                color_continuous_scale='Oranges'
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
    
    # INSIGHT 10: User Growth Trend
    st.header("👤 Insight 10: User Growth Trend")
    
    if not data['users'].empty:
        user_growth = data['users'].groupby(['year', 'quarter']).agg({
            'registered_users': 'sum',
            'app_opens': 'sum'
        }).reset_index()
        user_growth['period'] = user_growth['year'].astype(str) + '-Q' + user_growth['quarter'].astype(str)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=user_growth['period'],
            y=user_growth['registered_users'] / 1e6,
            mode='lines+markers',
            name='Registered Users (M)',
            line=dict(color='#4834d4', width=3)
        ))
        fig.add_trace(go.Scatter(
            x=user_growth['period'],
            y=user_growth['app_opens'] / 1e9,
            mode='lines+markers',
            name='App Opens (B)',
            line=dict(color='#feca57', width=3),
            yaxis='y2'
        ))
        fig.update_layout(
            title='User Growth Trend Over Time',
            xaxis_title='Period',
            yaxis_title='Registered Users (Millions)',
            yaxis2=dict(title='App Opens (Billions)', overlaying='y', side='right'),
            height=500,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Additional Insights Section
    st.markdown("---")
    st.header("🔍 Additional Analysis")
    
    # State comparison table
    if not filtered_map_transactions.empty and not filtered_map_users.empty:
        comparison_data = filtered_map_transactions.groupby('state').agg({
            'transaction_amount': 'sum',
            'transaction_count': 'sum'
        }).reset_index()
        
        user_state_data = filtered_map_users.groupby('state').agg({
            'registered_users': 'sum',
            'app_opens': 'sum'
        }).reset_index()
        
        comparison_data = comparison_data.merge(user_state_data, on='state', how='outer').fillna(0)
        comparison_data = comparison_data.sort_values('transaction_amount', ascending=False)
        
        st.subheader("State-wise Complete Comparison")
        st.dataframe(comparison_data, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>PhonePe Pulse Data Visualization Dashboard</p>
        <p>Built with Streamlit, Plotly, and MySQL</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

