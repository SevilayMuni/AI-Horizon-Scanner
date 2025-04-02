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

# Configure page
st.set_page_config(
    page_title="Democratizing AI Development Knowledge",
    page_icon=":bar_chart:",
    layout="wide")

# Load data
@st.cache_data
def load_dev_data():
    df_hardware = pd.read_parquet("./data/df_hardware.parquet", engine = 'pyarrow')
    df_computation = pd.read_parquet("./data/df_comput.parquet", engine = 'pyarrow')
    df_datapoint = pd.read_parquet("./data/df_data.parquet", engine = 'pyarrow')
    df_parameter = pd.read_parquet("./data/df_param.parquet", engine = 'pyarrow')
    df_cost_hardware = pd.read_parquet("./data/df_cost_hardware.parquet", engine = 'pyarrow')
    df_cumulative2 = pd.read_parquet("./data/df_cumu2.parquet", engine = 'pyarrow')
    return df_hardware, df_computation, df_datapoint, df_parameter, df_cost_hardware, df_cumulative2

df_hardware, df_computation, df_datapoint, df_parameter, df_cost_hardware, df_cumulative2 = load_dev_data()

@st.cache_data
def load_geo_data():
    df_cumulative = pd.read_parquet("./data/df_cumu.parquet", engine = 'pyarrow')
    df_patent_agg = pd.read_parquet("./data/df_patent_agg.parquet", engine = 'pyarrow')
    df_bill = pd.read_parquet("./data/df_bill.parquet", engine = 'pyarrow')
    return df_cumulative, df_patent_agg, df_bill

df_cumulative, df_patent_agg, df_bill = load_geo_data()

@st.cache_data
def load_inno_invest_data():
    df_affiliation = pd.read_parquet("./data/df_affiliation.parquet", engine = 'pyarrow')
    df_patent_world = pd.read_parquet("./data/df_patent_world.parquet", engine = 'pyarrow')
    df_patent_world2 = pd.read_parquet("./data/df_patent_world2.parquet", engine = 'pyarrow')
    df_investment = pd.read_parquet("./data/df_investment.parquet", engine = 'pyarrow')
    df_investment1 = pd.read_parquet("./data/df_investment1.parquet", engine = 'pyarrow')
    df_investment2 = pd.read_parquet("./data/df_investment2.parquet", engine = 'pyarrow')
    df_investment3 = pd.read_parquet("./data/df_investment3.parquet", engine = 'pyarrow')
    return df_affiliation, df_patent_world, df_patent_world2, df_investment, df_investment1, df_investment2, df_investment3

df_affiliation, df_patent_world, df_patent_world2, df_investment, df_investment1, df_investment2, df_investment3 = load_inno_invest_data()

@st.cache_data
def load_public_data():
    df_automated_survey = pd.read_parquet("./data/df_automated_survey.parquet", engine = 'pyarrow')
    df_view_country = pd.read_parquet("./data/df_view_country.parquet", engine = 'pyarrow')
    df_view_continent21 = pd.read_parquet("./data/df_view_continent2021.parquet", engine = 'pyarrow')
    df_view_gender = pd.read_parquet("./data/df_view_gender.parquet", engine = 'pyarrow')
    df_view3 = pd.read_parquet("./data/df_view3.parquet", engine = 'pyarrow')
    return df_automated_survey, df_view_country, df_view_continent21, df_view_gender, df_view3

df_automated_survey, df_view_country, df_view_continent21, df_view_gender, df_view3 = load_public_data()

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
st.title("AI Horizon Scanner App")
st.subheader("Democratizing AI Development Knowledge")

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
    "🔧 AI Development",
    "🌍 Geographic Distribution",
    "💡 Innovation",
    "💵 Investment",
    "👥 Public View",
    "🔍 Comparison Tool"])

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
        """
        explanation_content += "</div>"
        
        st.markdown(explanation_content, unsafe_allow_html=True)

# Section content
if section == "🔧 AI Development":
    st.header("🔧 AI Development Interactive Plots")
    with st.expander(f"Why This Matters❓❓", expanded=False):
        st.markdown("""**Understanding the resources required to develop AI systems helps us assess who can participate in AI development and how access to these technologies might be distributed.**""")
    
    # Cost to Train AI Systems Plot
    color_discrete_map = {
        'Language': 'rgb(237,37,78)', 'Speech': 'rgb(69,56,35)', 
        'Vision & ImageGeneration': 'rgb(144,103,189)', 'Vision': 'rgb(64,89,173)', 
        'ImageGeneration': 'rgb(4,129,188)', 'Multimodal': 'rgb(163,59,32)', 
        'Other': 'rgb(118,66,72)', 'Biology': 'rgb(12,206,187)', 'Games': 'rgb(242,158,76)'}
    fig = px.scatter(
        df_hardware, x="day", y="cost__inflation_adjusted", color="domain", text = 'entity',
        log_y=True, color_discrete_map=color_discrete_map,
        labels={"cost__inflation_adjusted": "Cost (USD)", "day": "Time", "entity": "AI System", "Domain": "Domain"},
        title="Energy Cost to Train AI Systems",
        width=1200, height=500)
    fig.update_traces(
        marker=dict(size=8, opacity=0.8, line=dict(width=0.5, color='black')),
        textposition="top center", showlegend=True,
        textfont=dict(size=7, style="italic", color='black'))
    fig.update_layout(
        xaxis_title="Year", legend_title="Domain", hovermode="closest",
        yaxis=dict(type="log", tickvals=[1e3, 1e4, 1e5, 1e6, 1e7], ticktext=["1K", "10K", "100K", "1M", "10M"]),
        yaxis_title="Cost ($, inflation adjusted)", title_x=0.3,
        margin=dict(l=5, r=5, t=35, b=5), plot_bgcolor='rgba(240,247,244,0.5)')
    st.plotly_chart(fig, use_container_width=True)

    # 'Computation Used to Train AI Systems' Plot
    tickvals = [10**i for i in range(-12, 11)]
    color_discrete_map2={'Language': 'rgb(4, 139, 168)', 'Speech': 'rgb(242, 66, 54)', 'Vision': 'rgb(144, 103, 198)', 'Image Generation': 'rgb(98, 0, 179)',
                         'Multiple Domains': 'rgb(240, 56, 107)', 'Other': 'rgb(118, 66, 72)','Biology': 'rgb(138, 155, 104)', 'Games': 'rgb(242, 158, 76)'}
    fig2 = px.scatter(df_computation, x="day", y="training_computation_petaflop", color="domain", log_y=True, color_discrete_map=color_discrete_map2, 
                      labels={"training_computation_petaflop": "Computation", "day": "Time", "entity": "AI System", "domain": "Domain"},
                      title="Computation Used to Train AI Systems", width=1000, height=500)
    fig2.update_traces(marker=dict(size=8, opacity=0.7, line=dict(width=0.5, color='black')), textposition="top center", showlegend=True, textfont=dict(size=9, style="italic"))
    # Improve layout
    fig2.update_layout(yaxis=dict(type="log", tickvals=tickvals), xaxis_title="Year", yaxis_title="Training Computation (petaFLOP)", hovermode="closest", 
                       legend_title="AI Domain", margin=dict(l=5, r=5, t=35, b=5), plot_bgcolor='rgba(240, 247, 244, 0.5)', title_x=0.27)
    st.plotly_chart(fig2, use_container_width=True)

    # 'Datapoints Used to Train AI Systems' Plot
    tickvals3 = [10**i for i in range(1, 13)]
    color_discrete_map3={'Language': 'rgb(4, 139, 168)', 'Speech': 'rgb(242, 66, 54)', 'Vision': 'rgb(144, 103, 198)', 'Image Generation': 'rgb(98, 0, 179)',
                         'Multiple Domains': 'rgb(240, 56, 107)', 'Other': 'rgb(118, 66, 72)', 'Biology': 'rgb(138, 155, 104)', 'Games': 'rgb(242, 158, 76)'}
    fig3 = px.scatter(df_datapoint, x="day", y="training_dataset_size__datapoints", color="domain", log_y=True, color_discrete_map=color_discrete_map3,
                      labels={"training_dataset_size__datapoints": "Size", "day": "Time", "entity": "AI System", "domain": "Domain"}, 
                      title="Datapoints Used to Train AI Systems", hover_data = ['entity', 'domain'], width=1000, height=500)
    fig3.update_traces(marker=dict(size=8, opacity=0.7, line=dict(width=0.5, color='black')), textposition="top center", showlegend=True, textfont=dict(size=9, style="italic"))
    fig3.update_layout(yaxis=dict(type="log", tickvals=tickvals3), xaxis_title="Year", yaxis_title="Training Datapoints", legend_title="AI Domain", 
                       hovermode="closest", margin=dict(l=5, r=5, t=35, b=5), plot_bgcolor='rgba(240, 247, 244, 0.5)', title_x=0.28)
    st.plotly_chart(fig3, use_container_width=True)

    # 'Number of Parameter Used to Train AI' Plot
    tickvals4 = [10**i for i in range(1, 13)]
    color_discrete_map4={'Academia & Industry Collab': 'rgb(179, 136, 235)', 'Industry': 'rgb(255, 90, 95)', 'Other': 'rgb(52, 46, 55)', 'Academia': 'rgb(8, 126, 139)'}
    fig4 = px.scatter(df_parameter, x="day", y="parameters", color="organization_categorization", log_y=True, title="Number of Parameter Used to Train AI",
                      labels={"parameters": "Parameters", "day": "Time", "entity": "AI System", "organization_categorization": "Organization"}, 
                      hover_data = ['entity', 'organization_categorization'], width=1000, height=500, color_discrete_map=color_discrete_map4)
    fig4.update_traces(marker=dict(size=8, opacity=0.7, line=dict(width=0.5, color='black')), textposition="top center", showlegend=True, textfont=dict(size=9, style="italic"))
    fig4.update_layout(yaxis=dict(type="log", tickvals=tickvals4), xaxis_title="Year", yaxis_title="Number of Adjusted Parameters", hovermode="closest",
                      legend_title="Organization", margin=dict(l=5, r=5, t=35, b=5), title_x=0.21, plot_bgcolor='rgba(240, 247, 244, 0.5)')
    st.plotly_chart(fig4, use_container_width=True)

    # 'Training Computation vs. Parameters in AI Systems by Organization' Plot
    ytickvals = [10**i for i in range(-12, 11)]
    xtickvals = [10**i for i in range(1, 13)]
    color_discrete_map5={'Academia & Industry Collab': 'rgb(179, 136, 235)', 'Other': 'rgb(52, 46, 55)', 'Industry': 'rgb(255, 90, 95)', 'Academia': 'rgb(8, 126, 139)'}
    fig5 = px.scatter(df_cost_hardware, x="parameters", y="training_computation_petaflop", color="organization_categorization", log_y=True,
                      labels={"parameters": "Parameters", "training_computation_petaflop": "Computation", "entity": "AI System", "organization_categorization": "Organization"},
                      title="Training Computation vs. Parameters in AI Systems by Organization", hover_data = ['entity', 'organization_categorization'], 
                      width=1000, height=500, color_discrete_map=color_discrete_map5)
    fig5.update_traces(marker=dict(size=8, opacity=0.7, line=dict(width=0.5, color='black')),textposition="top center", showlegend=True,textfont=dict(size=9, style="italic"))
    fig5.update_layout(yaxis=dict(type="log", tickvals = ytickvals), xaxis_title="Number of Adjusted Parameters", xaxis=dict(type="log", tickvals = xtickvals),
                       yaxis_title="Training Computation (petaFLOP)", legend_title="Organization", hovermode="closest", margin=dict(l=5, r=5, t=35, b=5), title_x=0.12, plot_bgcolor='rgba(240, 247, 244, 0.5)')
    st.plotly_chart(fig5, use_container_width=True)

# ---------------------------------------------------------------------------------------------------------
elif section == "🌍 Geographic Distribution":
    st.header("🌍 Geographic Distribution Interactive Plots")
    
    # Cumulative Number of Large-Scale AI Systems by Country
    color_discrete_map6 = {'Canada': 'rgb(192, 43, 61)', 'China': 'rgb(20, 19, 1)', 'Finland': 'rgb(206, 162, 172)', 'France': 'rgb(166, 117, 161)', 'Germany': 'rgb(252, 100, 113)', 
                           'Hong Kong': 'rgb(163, 67, 133)', 'Israel': 'rgb(112, 110, 96)', 'Japan': 'rgb(170, 83, 98)', 'Russia': 'rgb(237, 174, 73)', 'Saudi Arabia': 'rgb(223, 87, 188)', 
                           'Singapore': 'rgb(249, 220, 92)', 'South Korea': 'rgb(297, 40, 61)', 'United Arab Emirates': 'rgb(183, 181, 179)', 'United Kingdom': 'rgb(237, 174, 73)', 'United States': 'rgb(184, 12, 9)'}
    
    fig6 = px.line(df_cumulative, x="year", y="cumulative_count", color="entity", markers=True, color_discrete_map=color_discrete_map, 
                   labels={"entity": "Country", "year": "Year", "cumulative_count": "AI System Count"}, title="Cumulative Number of Large-Scale AI Systems by Country", width=1200, height=500)
    fig6.update_traces(text=df_cumulative["entity"] + ": " + df_cumulative["cumulative_count"].astype(str), hoverinfo="text+name", 
                       marker=dict(size=7, opacity=0.8, line=dict(width=0.5, color='black')))
    fig6.update_layout(xaxis=dict(tickmode="linear", dtick=10), legend_title="Country", yaxis=dict(title="Cumulative AI System Count"), title_x=0.17, 
                       margin=dict(l=5, r=5, t=35, b=5), plot_bgcolor='rgba(229, 231, 230, 0.5)')
    st.plotly_chart(fig6, use_container_width=True)

elif section == "Section 3: Innovation":
    st.header("Innovation")
    
    # Worldwide AI Related Patent Applications by Status
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data['inno']['year'], name="Granted",
        y=data['inno']['num_patent_granted__field_all'],
        text=data['inno']['num_patent_granted__field_all'],
        textfont=dict(size=10, weight='bold'),
        marker_color='rgb(97, 152, 142)'
    ))
    fig.add_trace(go.Bar(
        x=data['inno']['year'], name="Applied",
        y=data['inno']['num_patent_applications__field_all'],
        text=data['inno']['num_patent_applications__field_all'],
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
    
    # Annual Private Investment in AI by Location
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['invest']['year'], y=data['invest']['china'],
        name="China", mode='lines+markers', marker_color='rgb(150, 2, 0)',
        marker_size=8, opacity=0.7
    ))
    fig.add_trace(go.Scatter(
        x=data['invest']['year'], y=data['invest']['united_states'],
        name="United States", mode='lines+markers', marker_size=8,
        marker_color='rgb(225, 188, 41)', opacity=0.7
    ))
    fig.add_trace(go.Scatter(
        x=data['invest']['year'], y=data['invest']['european_union_and_united_kingdom'],
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
    # Americans Opinion About Their Work Being Automated
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
