"""
Visualization Scripts for PhonePe Pulse Data Analysis
Creates 4 types of visualizations as per requirements
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.offline import plot
import folium
from folium.plugins import HeatMap
import os
import json
import requests


class PhonePeVisualizations:
    def __init__(self, processed_data, output_dir='outputs'):
        self.data = processed_data
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
    
    def plot_yearly_transaction_growth(self):
        """
        1️⃣ Year-wise transaction growth
        Line chart: Total transactions vs Year
        """
        yearly_data = self.data['yearly_summary']
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(yearly_data['Year'], yearly_data['Transactions'], 
                marker='o', linewidth=3, markersize=10, color='#2E86AB')
        ax.fill_between(yearly_data['Year'], yearly_data['Transactions'], 
                        alpha=0.3, color='#2E86AB')
        
        ax.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax.set_ylabel('Total Transactions', fontsize=12, fontweight='bold')
        ax.set_title('Year-wise Digital Payment Transaction Growth in India', 
                     fontsize=16, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # Format y-axis to show in millions
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
        
        # Add value labels on points
        for year, trans in zip(yearly_data['Year'], yearly_data['Transactions']):
            ax.annotate(f'{trans/1e6:.1f}M', 
                       (year, trans), 
                       textcoords="offset points", 
                       xytext=(0,10), 
                       ha='center', fontsize=9)
        
        plt.tight_layout()
        output_path = os.path.join(self.output_dir, '1_yearly_transaction_growth.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Saved: {output_path}")
        return output_path
    
    def plot_transaction_amount_growth(self):
        """
        2️⃣ Transaction amount growth
        Line / bar chart
        """
        yearly_data = self.data['yearly_summary']
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Line Chart
        ax1.plot(yearly_data['Year'], yearly_data['Amount'], 
                marker='s', linewidth=3, markersize=10, color='#A23B72')
        ax1.fill_between(yearly_data['Year'], yearly_data['Amount'], 
                        alpha=0.3, color='#A23B72')
        ax1.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Total Amount (INR)', fontsize=12, fontweight='bold')
        ax1.set_title('Transaction Amount Growth (Line Chart)', 
                     fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3, linestyle='--')
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/1e9:.1f}B'))
        
        # Bar Chart
        bars = ax2.bar(yearly_data['Year'], yearly_data['Amount'], 
                      color='#F18F01', alpha=0.8, edgecolor='black', linewidth=1.5)
        ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Total Amount (INR)', fontsize=12, fontweight='bold')
        ax2.set_title('Transaction Amount Growth (Bar Chart)', 
                     fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3, linestyle='--', axis='y')
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/1e9:.1f}B'))
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax2.annotate(f'₹{height/1e9:.1f}B',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        plt.suptitle('Digital Payment Transaction Amount Growth in India', 
                     fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        output_path = os.path.join(self.output_dir, '2_transaction_amount_growth.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Saved: {output_path}")
        return output_path
    
    def plot_top_states(self, top_n=10):
        """
        3️⃣ Top states by transactions
        Bar chart
        """
        state_data = self.data['state_summary'].head(top_n)
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        bars = ax.barh(state_data['State'], state_data['Transactions'], 
                      color='#06A77D', alpha=0.8, edgecolor='black', linewidth=1.5)
        
        ax.set_xlabel('Total Transactions', fontsize=12, fontweight='bold')
        ax.set_ylabel('State', fontsize=12, fontweight='bold')
        ax.set_title(f'Top {top_n} States by Digital Payment Transactions', 
                     fontsize=16, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle='--', axis='x')
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
        
        # Add value labels
        for i, (state, trans) in enumerate(zip(state_data['State'], state_data['Transactions'])):
            ax.annotate(f'{trans/1e6:.1f}M',
                       xy=(trans, i),
                       xytext=(5, 0),
                       textcoords="offset points",
                       va='center', fontsize=10, fontweight='bold')
        
        # Invert y-axis to show highest at top
        ax.invert_yaxis()
        
        plt.tight_layout()
        output_path = os.path.join(self.output_dir, '3_top_states_by_transactions.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Saved: {output_path}")
        return output_path
    
    def plot_india_map_choropleth(self):
        """
        4️⃣ India map (state-wise transactions)
        Choropleth map (VERY IMPRESSIVE)
        """
        state_data = self.data['state_summary'].copy()
        
        # State coordinates (approximate center of each state)
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
        
        # Create a base map centered on India
        india_map = folium.Map(
            location=[20.5937, 78.9629],
            zoom_start=5,
            tiles='CartoDB positron'
        )
        
        # Create a dictionary for choropleth
        state_dict = dict(zip(state_data['State'], state_data['Transactions']))
        
        # Add markers with color coding based on transaction volume
        max_transactions = state_data['Transactions'].max()
        min_transactions = state_data['Transactions'].min()
        
        # Color scale function
        def get_color(value, min_val, max_val):
            """Get color based on value"""
            normalized = (value - min_val) / (max_val - min_val)
            if normalized < 0.2:
                return 'green'
            elif normalized < 0.4:
                return 'lightgreen'
            elif normalized < 0.6:
                return 'yellow'
            elif normalized < 0.8:
                return 'orange'
            else:
                return 'red'
        
        # Add circles for each state
        for state, transactions in state_dict.items():
            if state in state_coords:
                lat, lon = state_coords[state]
                color = get_color(transactions, min_transactions, max_transactions)
                
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=transactions / max_transactions * 30 + 5,  # Scale radius
                    popup=folium.Popup(
                        f'<b>{state}</b><br>Transactions: {transactions/1e6:.2f}M',
                        max_width=200
                    ),
                    tooltip=f'{state}: {transactions/1e6:.2f}M transactions',
                    color='black',
                    weight=1,
                    fill=True,
                    fillColor=color,
                    fillOpacity=0.7
                ).add_to(india_map)
        
        # Try to add GeoJSON choropleth if available
        try:
            geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(geojson_url, timeout=5)
            if response.status_code == 200:
                geojson_data = response.json()
                
                # Create state name mapping for GeoJSON
                state_name_mapping = {}
                for feature in geojson_data.get('features', []):
                    props = feature.get('properties', {})
                    state_name = props.get('NAME_1', '')
                    state_name_mapping[state_name] = state_name
                
                # Prepare data for choropleth
                choropleth_data = {}
                for state, transactions in state_dict.items():
                    # Try to match state names
                    for geojson_state in state_name_mapping.keys():
                        if state.lower() in geojson_state.lower() or geojson_state.lower() in state.lower():
                            choropleth_data[geojson_state] = transactions
                            break
                
                if choropleth_data:
                    folium.Choropleth(
                        geo_data=geojson_data,
                        data=choropleth_data,
                        columns=['State', 'Transactions'],
                        key_on='feature.properties.NAME_1',
                        fill_color='YlOrRd',
                        fill_opacity=0.7,
                        line_opacity=0.2,
                        legend_name='Transactions (Millions)'
                    ).add_to(india_map)
        except Exception as e:
            print(f"   Note: GeoJSON overlay not available, using markers only")
        
        # Add title
        title_html = '''
        <div style="position: fixed; 
                    top: 10px; left: 50%; transform: translateX(-50%);
                    width: 600px; height: 60px; 
                    background-color: white; border: 2px solid black;
                    z-index:9999; font-size:20px; font-weight: bold;
                    text-align: center; padding: 10px">
        <p>India: State-wise Digital Payment Transactions</p>
        <p style="font-size:14px;">Choropleth Map Visualization</p>
        </div>
        '''
        india_map.get_root().html.add_child(folium.Element(title_html))
        
        # Save HTML
        html_path = os.path.join(self.output_dir, '4_india_map_choropleth.html')
        india_map.save(html_path)
        print(f"✅ Saved: {html_path} (Interactive)")
        
        # For static PNG, we'll create a plotly version as fallback
        png_path = os.path.join(self.output_dir, '4_india_map_choropleth.png')
        try:
            # Create a simple plotly scatter map as backup
            fig = go.Figure()
            
            for state, transactions in state_dict.items():
                if state in state_coords:
                    lat, lon = state_coords[state]
                    fig.add_trace(go.Scattergeo(
                        lon=[lon],
                        lat=[lat],
                        text=[f'{state}<br>{transactions/1e6:.2f}M'],
                        mode='markers+text',
                        marker=dict(
                            size=transactions / max_transactions * 50 + 10,
                            color=transactions,
                            colorscale='Viridis',
                            showscale=True,
                            colorbar=dict(title="Transactions (Millions)")
                        ),
                        name=state,
                        hovertemplate=f'<b>{state}</b><br>Transactions: {transactions/1e6:.2f}M<extra></extra>'
                    ))
            
            fig.update_geos(
                visible=True,
                resolution=50,
                showcountries=True,
                countrycolor="Black",
                showsubunits=True,
                subunitcolor="Blue",
                center=dict(lat=20.5937, lon=78.9629),
                projection_scale=4.5,
                lonaxis_range=[68, 98],
                lataxis_range=[6, 37]
            )
            
            fig.update_layout(
                title={
                    'text': 'India: State-wise Digital Payment Transactions<br><sub>Choropleth Map Visualization</sub>',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 20}
                },
                height=800,
                geo=dict(
                    bgcolor='lightblue',
                    lakecolor='blue',
                    landcolor='lightgray'
                )
            )
            
            fig.write_image(png_path, width=1400, height=800, scale=2)
            print(f"✅ Saved: {png_path} (Static)")
        except Exception as e:
            print(f"⚠️  Note: Static PNG not saved: {str(e)}")
            print(f"   HTML map is available and fully interactive!")
        
        return html_path, png_path
    
    def generate_all_visualizations(self):
        """Generate all 4 visualizations"""
        print("\n" + "="*60)
        print("📊 Generating PhonePe Pulse Data Visualizations")
        print("="*60 + "\n")
        
        self.plot_yearly_transaction_growth()
        self.plot_transaction_amount_growth()
        self.plot_top_states(top_n=10)
        self.plot_india_map_choropleth()
        
        print("\n" + "="*60)
        print("✅ All visualizations generated successfully!")
        print(f"📁 Output directory: {self.output_dir}")
        print("="*60 + "\n")

