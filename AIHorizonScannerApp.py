import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
from PIL import Image
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import base64
from io import BytesIO

# ---------------------------------------------------------------------------------------------------------

# Configure page
st.set_page_config(
    page_title="Democratizing AI Development Knowledge",
    page_icon=":bar_chart:",
    layout="wide")

# Load data (placeholder - replace with actual data loading)
@st.cache_data
def load_data():
    # These would be replaced with actual data loading
    return {'dev': pd.read_parquet('./data/df_cost_hardware.parquet', engine = 'pyarrow'),
            'geo': pd.read_parquet('./data/df_cumu.parquet', engine = 'pyarrow'),
            'inno': pd.read_parquet('./data/df_patent_world.parquet', engine = 'pyarrow'),
            'invest': pd.read_parquet('./data/df_investment.parquet', engine = 'pyarrow'),
            'public': pd.read_parquet('./data/df_view_country.parquet', engine = 'pyarrow')}

data = load_data()

# Custom CSS
st.markdown("""
    <style>
    .kpi-box {
        border-radius: 5px;
        padding: 15px;
        background-color: #f8f9fa;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .kpi-title {
        font-size: 14px;
        color: #6c757d;
        margin-bottom: 5px;
    }
    .kpi-value {
        font-size: 24px;
        font-weight: bold;
        color: #343a40;
    }
    .chart-explanation {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 5px;
        margin-top: 10px;
        border-left: 4px solid #3498db;
    }
    .section-header {
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
        padding-bottom: 5px;
        margin-top: 20px;
    }
    .reference-link {
        font-size: 0.8em;
        color: #6c757d;
        margin-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.title("Democratizing AI Development Knowledge")

# Weekly Spotlight
current_week = datetime.now().strftime("%U")
with st.expander(f"📌 Weekly Spotlight (Week {current_week})", expanded=True):
    st.markdown("""
    **Key Finding:** The cost to train state-of-the-art AI systems has increased 100x in the last 5 years, 
    with language models now costing over $100 million to train. This rapid escalation raises important 
    questions about equitable access to AI development capabilities.
    """)

# Sidebar navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to:", [
    "Section 1: AI Development",
    "Section 2: Geographic Distribution",
    "Section 3: Innovation",
    "Section 4: Investment",
    "Section 5: Public View",
    "Comparison Tool"])


def show_explanation(explanation, reference=None):
    # Create a unique key for this explanation section
    explanation_key = f"explanation_{hash(explanation)}"
    
    # Check if explanation should be shown (stored in session state)
    if explanation_key not in st.session_state:
        st.session_state[explanation_key] = False
    
    # Toggle button
    if st.button("Explain This Chart ▲" if st.session_state[explanation_key] else "Explain This Chart ▼", 
                key=f"btn_{explanation_key}"):
        st.session_state[explanation_key] = not st.session_state[explanation_key]
    
    # Show explanation if toggled on
    if st.session_state[explanation_key]:
        explanation_content = f"""
        <div class="chart-explanation">
            {explanation}
        explanation_content += "</div>"
        
        st.markdown(explanation_content, unsafe_allow_html=True)

# Section content
if section == "Section 1: AI Development":
    st.header("AI Development")
    
    
    # Cost to Train AI Systems Plot
    st.subheader("Cost to Train AI Systems")
    color_discrete_map = {
        'Language': 'rgb(237,37,78)', 'Speech': 'rgb(69,56,35)', 
        'Vision & ImageGeneration': 'rgb(144,103,189)', 'Vision': 'rgb(64,89,173)', 
        'ImageGeneration': 'rgb(4,129,188)', 'Multimodal': 'rgb(163,59,32)', 
        'Other': 'rgb(118,66,72)', 'Biology': 'rgb(12,206,187)', 'Games': 'rgb(242,158,76)'
    }
    
    fig = px.scatter(
        data['dev'], x="day", y="cost__inflation_adjusted", color="domain",
        log_y=True, color_discrete_map=color_discrete_map,
        labels={"cost__inflation_adjusted": "Cost (USD)", "day": "Time", "entity": "AI System", "Domain": "Domain"},
        title="Energy Cost to Train AI Systems",
        width=1200, height=500
    )
    fig.update_traces(
        marker=dict(size=8, opacity=0.8, line=dict(width=0.5, color='black')),
        textposition="top center", showlegend=True,
        textfont=dict(size=8, style="italic", color='black')
    )
    fig.update_layout(
        xaxis_title="Year", legend_title="Domain", hovermode="closest",
        yaxis=dict(type="log", tickvals=[163, 164, 165, 166, 167]),
        yaxis_title="Cost (USD, inflation adjusted)", title_x=0.3,
        margin=dict(l=5, r=5, t=35, b=5), plot_bgcolor='rgba(240,247,244,0.5)'
    )
    st.plotly_chart(fig, use_container_width=True)
    show_explanation(
        "This chart shows the inflation-adjusted cost to train notable AI systems over time, broken down by domain. The logarithmic scale reveals the exponential growth in training costs, particularly for language models.",
        reference="AI Index Report 2023, Stanford HAI")
    

elif section == "Section 2: Geographic Distribution":
    st.header("Geographic Distribution")
    
    
    
    st.markdown("Why This Matters: The geographic concentration of AI development affects global power dynamics 
    and determines which cultural perspectives are embedded in these influential technologies.")
    
    # Cumulative Number of Large-Scale AI Systems by Country
    st.subheader("Cumulative Number of Large-Scale AI Systems by Country")
    color_discrete_map = {
        'Canada': 'rgb(192, 43, 61)', 'China': 'rgb(20, 19, 1)', 
        'Finland': 'rgb(206, 162, 172)', 'France': 'rgb(166, 117, 161)', 
        'Germany': 'rgb(252, 100, 113)', 'Hong Kong': 'rgb(163, 67, 133)', 
        'Israel': 'rgb(112, 110, 96)', 'Japan': 'rgb(170, 83, 98)', 
        'Russia': 'rgb(237, 174, 73)', 'Saudi Arabia': 'rgb(223, 87, 188)', 
        'Singapore': 'rgb(249, 220, 92)', 'South Korea': 'rgb(297, 40, 61)', 
        'United Arab Emirates': 'rgb(183, 181, 179)', 'United Kingdom': 'rgb(237, 174, 73)', 
        'United States': 'rgb(184, 12, 9)'
    }
    
    fig = px.line(
        data['geo'], x="year", y="cumulative_count", color="entity",
        markers=True, color_discrete_map=color_discrete_map,
        labels={"entity": "Country", "year": "Year", "cumulative_count": "AI System Count"},
        title="Cumulative Number of Large-Scale AI Systems by Country",
        width=1200, height=500
    )
    fig.update_traces(
        text=data['geo']['entity'] + ": " + data['geo']['cumulative_count'].astype(str),
        hoverinfo="text+name", marker=dict(size=7, opacity=0.8, line=dict(width=0.5, color='black'))
    )
    fig.update_layout(
        yaxis=dict(tickmode="linear", dtick=1), legend_title="Country",
        yaxis_title="Cumulative AI System Count", title_x=0.17,
        margin=dict(l=5, r=5, t=35, b=5), plot_bgcolor='rgba(229, 231, 230, 0.5)'
    )
    st.plotly_chart(fig, use_container_width=True)
    show_explanation(
        "This chart tracks the cumulative count of notable AI systems developed by country over time, revealing the geographic concentration of AI development capabilities.",
        reference="AI Index Report 2023, Crunchbase analysis")

elif section == "Section 3: Innovation":
    st.header("Innovation")
    
    
    
    st.markdown("""
    **Why This Matters:** Tracking innovation through patents and research affiliations helps us 
    understand where AI capabilities are being developed and who controls this intellectual property.
    """)
    
    # Worldwide AI Related Patent Applications by Status
    st.subheader("Worldwide AI Related Patent Applications by Status")
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data['inno']['year'], name="Granted",
        y=data['inno']['num_patent_granted_field_all'],
        text=data['inno']['num_patent_granted_field_all'],
        textfont=dict(size=10, weight='bold'),
        marker_color='rgb(97, 152, 142)'
    ))
    fig.add_trace(go.Bar(
        x=data['inno']['year'], name="Applied",
        y=data['inno']['num_patent_applications_field_all'],
        text=data['inno']['num_patent_applications_field_all'],
        textfont=dict(size=10, weight='bold'),
        marker_color='rgb(222, 143, 110)'
    ))
    fig.update_traces(
        hoverinfo="text+name", marker=dict(opacity=0.8)
    )
    fig.update_layout(
        barmode="stack", yaxis=dict(title="Patent Count"),
        xaxis=dict(title="Year", tickmode="linear", dtick=1, tickangle=0),
        legend_title="Status", hovermode="x unified", width=1200, height=500,
        margin=dict(l=10, r=5, t=35, b=5, pad=5), plot_bgcolor='rgba(249, 248, 248, 0.5)',
        title="Worldwide AI Related Patent Applications by Status", title_x=0.25
    )
    st.plotly_chart(fig, use_container_width=True)
    show_explanation(
        "This stacked bar chart shows the number of AI-related patent applications and grants over time, indicating the rapid growth of AI intellectual property claims.",
        reference="PatentsView database, WIPO statistics")


elif section == "Section 4: Investment":
    st.header("Investment")
    
    
    
    st.markdown("""
    **Why This Matters:** Investment patterns reveal which AI applications and regions are attracting 
    capital, shaping the future direction of AI development and commercialization.
    """)
    
    # Annual Private Investment in AI by Location
    st.subheader("Annual Private Investment in AI by Location")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['invest']['year'], y=data['invest']['China'],
        name="China", mode='lines+markers', marker_color='rgb(150, 2, 0)',
        marker_size=8, opacity=0.7
    ))
    fig.add_trace(go.Scatter(
        x=data['invest']['year'], y=data['invest']['United_states'],
        name="United States", mode='lines+markers', marker_size=8,
        marker_color='rgb(225, 188, 41)', opacity=0.7
    ))
    fig.add_trace(go.Scatter(
        x=data['invest']['year'], y=data['invest']['European_union_and_United_kingdom'],
        name="European Union & United Kingdom", mode='lines+markers',
        marker_color='rgb(36, 30, 78)', marker_size=8, opacity=0.7
    ))
    fig.add_trace(go.Scatter(
        x=data['invest']['year'], y=data['invest']['world'],
        name="World", mode='lines+markers', marker_size=8,
        marker_color='rgb(63, 124, 172)', opacity=0.7
    ))
    fig.update_layout(
        xaxis=dict(title="Year", tickmode="linear", dtick=1, tickangle=0),
        yaxis=dict(title="Private Investment (USD)"), legend_title="Location",
        margin=dict(l=5, r=5, t=35, b=5, pad=5), hovermode="x unified",
        title="Annual Private Investment in AI by Location", title_x=0.2,
        plot_bgcolor='rgba(248, 247, 255, 0.7)', width=1200, height=500
    )
    st.plotly_chart(fig, use_container_width=True)
    show_explanation(
        "This line chart tracks private investment in AI by major geographic regions, showing the competitive landscape of AI funding.",
        reference="Crunchbase data, CB Insights reports")

elif section == "Section 5: Public View":
    st.header("Public View")
    
    
    st.markdown("""
    **Why This Matters:** Public perception influences policy decisions, adoption rates, and the 
    social license for AI development, making it crucial to understand diverse perspectives.
    """)
    
    # Americans Opinion About Their Work Being Automated
    st.subheader("Americans Opinion About Their Work Being Automated")
    color_discrete_map = {
        "Don't Know": 'rgb(38, 45, 58)', "Worried": 'rgb(221, 96, 49)',
        "Not Worried": 'rgb(68, 114, 202)', "Very Worried": 'rgb(147, 3, 48)'
    }
    
    fig = px.bar(
        data['public'], x="year", y="opinion_count", color='opinion',
        barmode='stack', facet_col='entity', color_discrete_map=color_discrete_map,
        labels={'entity': 'Age Group', 'opinion': 'Opinion', 'year': 'Year', 'opinion_count': 'Count'}
    )
    fig.update_traces(
        marker_line_color='rgb(66, 68, 60)',
        marker_line_width=1.5, marker_opacity=0.8
    )
    fig.update_layout(
        title_text='Americans Opinion About Their Work Being Automated',
        xaxis_title='Year', yaxis_title='Opinion Count',
        legend_title="Opinion", width=1200, height=500,
        plot_bgcolor='rgb(258, 249, 248)'
    )
    st.plotly_chart(fig, use_container_width=True)
    show_explanation(
        "This grouped bar chart shows how Americans' concerns about job automation vary by age group over time, revealing generational differences in AI anxiety.",
        reference="Pew Research Center surveys")
    
    # Mini-poll
    st.subheader("What's Your AI Opinion?")
    with st.form("ai_opinion_poll"):
        opinion = st.radio(
            "How do you think AI will impact society in the next 20 years?",
            ["Mostly helpful", "Mostly harmful", "Both equally", "Not sure"]
        )
        age_group = st.selectbox(
            "Your age group",
            ["Under 30", "30-49", "50-64", "65+"]
        )
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.success("Thanks for sharing your opinion!")

elif section == "Comparison Tool":
    st.header("Comparison Tool")
    st.markdown("Use this tool to compare different aspects of AI development across countries, domains, or time periods.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        comparison_type = st.selectbox(
            "Compare by:",
            ["Country", "Domain", "Organization Type"]
        )
    
    with col2:
        metric = st.selectbox(
            "Metric:",
            ["Investment", "Patents", "System Count", "Training Cost"]
        )
    
    if st.button("Generate Comparison"):
        # Placeholder for comparison logic
        st.write("Comparison results would appear here based on selected parameters")
        
        # Example visualization
        fig = px.bar(
            x=["USA", "China", "EU", "Other"],
            y=[45, 38, 12, 5],
            labels={'x': 'Region', 'y': f'{metric} (Billions)'},
            title=f"{metric} Comparison by {comparison_type}"
        )
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
