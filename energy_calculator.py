import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Energy Consumption Calculator",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for light purple theme
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #f8f4ff 0%, #f0e8ff 50%, #e6d8ff 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 25px;
        box-shadow: 0 20px 40px rgba(147, 112, 219, 0.15);
        margin-top: 1rem;
        backdrop-filter: blur(10px);
    }
    
    /* Header Styles */
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #b19cd9, #9370db, #8a2be2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        font-family: 'Poppins', sans-serif;
        text-shadow: 0 2px 4px rgba(147, 112, 219, 0.3);
    }
    
    .sub-header {
        text-align: center;
        color: #6b46c1;
        font-size: 1.3rem;
        margin-bottom: 2.5rem;
        font-weight: 400;
        opacity: 0.8;
    }
    
    /* Section Headers */
    .stMarkdown h3 {
        color: #7c3aed;
        font-weight: 600;
        font-size: 1.4rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #e0e7ff;
        padding-bottom: 0.5rem;
    }
    
    /* Input Styles */
    .stSelectbox > div > div {
        background: linear-gradient(135deg, #faf5ff, #f3e8ff);
        border: 2px solid #e0e7ff;
        border-radius: 15px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #c4b5fd;
        box-shadow: 0 4px 12px rgba(196, 181, 253, 0.3);
    }
    
    .stTextInput > div > div {
        background: linear-gradient(135deg, #faf5ff, #f3e8ff);
        border: 2px solid #e0e7ff;
        border-radius: 15px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div:hover {
        border-color: #c4b5fd;
        box-shadow: 0 4px 12px rgba(196, 181, 253, 0.3);
    }
    
    .stNumberInput > div > div {
        background: linear-gradient(135deg, #faf5ff, #f3e8ff);
        border: 2px solid #e0e7ff;
        border-radius: 15px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stNumberInput > div > div:hover {
        border-color: #c4b5fd;
        box-shadow: 0 4px 12px rgba(196, 181, 253, 0.3);
    }
    
    /* Checkbox Styles */
    .stCheckbox > label {
        background: linear-gradient(135deg, #faf5ff, #f3e8ff);
        border: 2px solid #e0e7ff;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        font-weight: 500;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .stCheckbox > label:hover {
        border-color: #c4b5fd;
        box-shadow: 0 4px 12px rgba(196, 181, 253, 0.3);
        transform: translateY(-2px);
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #a855f7, #7c3aed, #6d28d9);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1rem 2rem;
        font-size: 1.2rem;
        font-weight: 600;
        width: 100%;
        margin-top: 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 8px 20px rgba(168, 85, 247, 0.3);
        font-family: 'Poppins', sans-serif;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(168, 85, 247, 0.4);
        background: linear-gradient(135deg, #9333ea, #7c3aed, #6d28d9);
    }
    
    /* Result Container */
    .result-container {
        background: linear-gradient(135deg, #ddd6fe, #c4b5fd, #a78bfa);
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-top: 2rem;
        box-shadow: 0 15px 35px rgba(167, 139, 250, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .energy-value {
        font-size: 3rem;
        font-weight: 700;
        margin: 1rem 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    /* Metric Cards */
    .stMetric {
        background: linear-gradient(135deg, #f3e8ff, #e9d5ff);
        border-radius: 15px;
        padding: 1rem;
        border: 2px solid #e0e7ff;
        transition: all 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(196, 181, 253, 0.3);
    }
    
    /* DataFrame Styles */
    .stDataFrame {
        background: linear-gradient(135deg, #faf5ff, #f3e8ff);
        border-radius: 15px;
        border: 2px solid #e0e7ff;
        overflow: hidden;
    }
    
    /* Success/Error Messages */
    .stAlert {
        border-radius: 15px;
        border: none;
        box-shadow: 0 4px 12px rgba(196, 181, 253, 0.3);
    }
    
    /* Sidebar Styles */
    .css-1d391kg {
        background: linear-gradient(135deg, #f8f4ff, #f0e8ff);
        border-radius: 15px;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #faf5ff, #f3e8ff);
        border-radius: 15px;
    }
    
    /* Custom Cards */
    .info-card {
        background: linear-gradient(135deg, #faf5ff, #f3e8ff);
        border: 2px solid #e0e7ff;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .info-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(196, 181, 253, 0.3);
    }
    
    .tip-card {
        background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
        border: 2px solid #bae6fd;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #0ea5e9;
    }
    
    /* Animation for elements */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-fade-in {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Scrollbar Styles */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #a855f7, #7c3aed);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #9333ea, #6d28d9);
    }
</style>
""", unsafe_allow_html=True)

# App header
st.markdown('<div class="animate-fade-in">', unsafe_allow_html=True)
st.markdown('<h1 class="main-header">⚡ Energy Calculator</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Calculate your home\'s energy consumption with style</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Create columns for better layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("### 👤 Personal Information")
    name = st.text_input("Your Name", placeholder="Enter your name")
    age = st.number_input("Your Age", min_value=1, max_value=120, step=1)
    st.markdown('</div>', unsafe_allow_html=True)
    
with col2:
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("### 📍 Location Information")
    city = st.text_input("Your City", placeholder="Enter your city")
    area = st.text_input("Area Name", placeholder="Enter your area")
    st.markdown('</div>', unsafe_allow_html=True)

# Housing information
st.markdown('<div class="info-card">', unsafe_allow_html=True)
st.markdown("### 🏠 Housing Information")
col3, col4 = st.columns([1, 1])

with col3:
    housing_type = st.selectbox(
        "Housing Type",
        ["Select Type", "Flat", "Tenament"],
        format_func=lambda x: f"🏠 {x}" if x != "Select Type" else x
    )

with col4:
    facility = st.selectbox(
        "Home Size",
        ["Select Size", "1BHK", "2BHK", "3BHK"],
        format_func=lambda x: f"🏡 {x}" if x != "Select Size" else x
    )
st.markdown('</div>', unsafe_allow_html=True)

# Appliances section
st.markdown('<div class="info-card">', unsafe_allow_html=True)
st.markdown("### 🔌 Appliances")
col5, col6, col7 = st.columns([1, 1, 1])

with col5:
    ac = st.checkbox("❄️ Air Conditioner")
    
with col6:
    fridge = st.checkbox("🧊 Refrigerator")
    
with col7:
    washing_machine = st.checkbox("🌊 Washing Machine")
st.markdown('</div>', unsafe_allow_html=True)

# Calculate button
if st.button("⚡ Calculate Energy Consumption"):
    # Validation
    if not all([name, age, city, area]) or housing_type == "Select Type" or facility == "Select Size":
        st.error("Please fill in all required fields!")
    else:
        # Calculate energy consumption
        cal_energy = 0
        
        # Base energy calculation based on BHK
        if facility == "1BHK":
            cal_energy += 2 * 0.4 + 2 * 0.8  # 2.4
        elif facility == "2BHK":
            cal_energy += 3 * 0.4 + 3 * 0.8  # 3.6
        elif facility == "3BHK":
            cal_energy += 4 * 0.4 + 4 * 0.8  # 4.8
        
        # Add appliance energy
        appliance_energy = 0
        appliances_used = []
        
        if ac:
            appliance_energy += 3
            appliances_used.append("Air Conditioner")
        if fridge:
            appliance_energy += 3
            appliances_used.append("Refrigerator")
        if washing_machine:
            appliance_energy += 3
            appliances_used.append("Washing Machine")
        
        cal_energy += appliance_energy
        
        # Display results
        st.markdown(f"""
        <div class="result-container animate-fade-in">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">🔋</div>
            <div style="font-size: 1.3rem; margin-bottom: 0.5rem;"><strong>Hello {name}!</strong></div>
            <div style="font-size: 1.1rem;">Your estimated energy consumption is</div>
            <div class="energy-value">{cal_energy:.1f} kWh</div>
            <div style="font-size: 1rem; opacity: 0.9;">Based on your {facility} {housing_type.lower()} in {city}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Energy breakdown chart
        st.markdown("### 📊 Energy Breakdown")
        
        # Create data for visualization
        base_energy = cal_energy - appliance_energy
        
        fig = go.Figure()
        
        # Add base energy
        fig.add_trace(go.Bar(
            name='Base Energy (Lighting & Basic)',
            x=['Energy Consumption'],
            y=[base_energy],
            marker_color='#a855f7',
            text=f'{base_energy:.1f} kWh',
            textposition='inside',
            textfont=dict(color='white', size=14, family='Poppins')
        ))
        
        # Add appliance energy
        if appliance_energy > 0:
            fig.add_trace(go.Bar(
                name='Appliances',
                x=['Energy Consumption'],
                y=[appliance_energy],
                marker_color='#c4b5fd',
                text=f'{appliance_energy:.1f} kWh',
                textposition='inside',
                textfont=dict(color='white', size=14, family='Poppins')
            ))
        
        fig.update_layout(
            title={
                'text': 'Energy Consumption Breakdown',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#7c3aed', 'family': 'Poppins'}
            },
            xaxis_title='Category',
            yaxis_title='Energy (kWh)',
            barmode='stack',
            height=450,
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Poppins', color='#7c3aed'),
            legend=dict(
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='#e0e7ff',
                borderwidth=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed breakdown
        st.markdown("### 📋 Detailed Breakdown")
        
        breakdown_data = {
            'Category': ['Base Energy (Lighting & Basic)', 'Appliances', 'Total'],
            'Energy (kWh)': [base_energy, appliance_energy, cal_energy],
            'Percentage': [
                f"{(base_energy/cal_energy)*100:.1f}%",
                f"{(appliance_energy/cal_energy)*100:.1f}%",
                "100.0%"
            ]
        }
        
        df = pd.DataFrame(breakdown_data)
        st.dataframe(df, use_container_width=True)
        
        # Energy saving tips
        st.markdown("### 💡 Energy Saving Tips")
        
        tips = [
            "🔆 Use LED bulbs instead of incandescent bulbs",
            "🌡️ Set AC temperature to 24°C or higher",
            "🔌 Unplug electronic devices when not in use",
            "🪟 Use natural light during the day",
            "🧊 Keep refrigerator at optimal temperature (3-4°C)",
            "👔 Use cold water for washing clothes when possible"
        ]
        
        for tip in tips:
            st.markdown(f'<div class="tip-card">{tip}</div>', unsafe_allow_html=True)
        
        # Summary card
        st.markdown("### 📈 Summary")
        col8, col9, col10 = st.columns([1, 1, 1])
        
        with col8:
            st.metric("Total Energy", f"{cal_energy:.1f} kWh", delta=None)
        
        with col9:
            st.metric("Base Energy", f"{base_energy:.1f} kWh", delta=None)
        
        with col10:
            st.metric("Appliance Energy", f"{appliance_energy:.1f} kWh", delta=None)
        
        # Appliances used
        if appliances_used:
            st.markdown("### 🔌 Appliances Included")
            for appliance in appliances_used:
                st.markdown(f'<div class="tip-card">✅ {appliance}</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #7c3aed; font-size: 1rem; font-weight: 500; margin-top: 2rem;'>"
    "💜 Energy Calculator - Calculate your home's energy consumption efficiently"
    "</div>",
    unsafe_allow_html=True
)

# Sidebar information
with st.sidebar:
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("### ℹ️ About")
    st.markdown("""
    This Energy Calculator helps you estimate your home's energy consumption based on:
    
    - **Home Size**: 1BHK, 2BHK, or 3BHK
    - **Appliances**: AC, Refrigerator, Washing Machine
    - **Base Energy**: Lighting and basic electrical needs
    
    The calculation uses standard energy consumption rates for different home sizes and appliances.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("### 🔧 How to Use")
    st.markdown("""
    1. Fill in your personal information
    2. Select your housing type and size
    3. Check the appliances you use
    4. Click 'Calculate Energy Consumption'
    5. View your results and energy breakdown
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Energy Units")
    st.markdown("""
    - **kWh**: Kilowatt-hour (unit of energy)
    - **Base Energy**: 0.4 kWh per room (lighting) + 0.8 kWh per room (basic appliances)
    - **Major Appliances**: 3 kWh each (AC, Fridge, Washing Machine)
    """)
    st.markdown('</div>', unsafe_allow_html=True)