import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# Configure page
st.set_page_config(page_title="AI Horizon Scanner App", page_icon=":bar_chart:", layout="wide")
# Sidebar navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to:", ["🔧 AI Development", "🌍 Geographic Distribution", "💡 Innovation", "💵 Investment", "👥 Public View", "🔍 Comparison Tool"])

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
df_view_gender19 = df_view_gender[df_view_gender['year'] == 2019]
df_view_gender21 = df_view_gender[df_view_gender['year'] == 2021]

# Helper Functions
# Define function to number formating
def format_investment(value):
    if value >= 1e9:
        return f'{round(value / 1e9, 2)}B'
    elif value >= 1e6:
        return f'{round(value / 1e6, 2)}M'
    else:
        return str(value)

def calculate_volatility(df, entity_name):
    """Calculate volatility score for a specific sector"""
    sector_df = df_invest_general[df_invest_general['entity'] == entity_name].sort_values('year')
    sector_df['yoy_growth'] = sector_df['world'].pct_change() * 100
    max_growth = sector_df['yoy_growth'].max()
    max_decline = sector_df['yoy_growth'].min()
    return abs(max_growth - max_decline)

def geographic_concentration(row):
    """Calculate Herfindahl-Hirschman Index (HHI) for geographic concentration"""
    total = row['china'] + row['united_states'] + row['european_union_and_united_kingdom']
    if total == 0:
        return 0
    china_share = row['china'] / total
    us_share = row['united_states'] / total
    eu_share = row['european_union_and_united_kingdom'] / total
    return (china_share**2 + us_share**2 + eu_share**2)

info_multi = '''AI Horizon Scanner displays AI-related metrics in charts and key insights that help you track ongoing developments. 
I aim to support the growing and vital public conversation about AI with this dashboard.'''

# Header
st.header("AI Horizon Scanner App: Democratizing AI Knowledge")

if section == "🔧 AI Development":
    st.info(info_multi)

    # Weekly Spotlight
    current_week = datetime.now().strftime("%U")
    with st.expander(f"📌 Weekly Spotlight (Week {current_week})", expanded=True):
        st.markdown("""
        **Key Finding:** The cost to train state-of-the-art AI systems has increased 100x in the last 5 years, 
        with language models now costing over $100 million to train. This rapid escalation raises important 
        questions about equitable access to AI development capabilities.
        """)

    # 1st KPI
    df_hardware['year'] = df_hardware['day'].dt.year
    latest_cost = df_hardware['cost__inflation_adjusted'].max()
    ai_sys = df_hardware[df_hardware['cost__inflation_adjusted'] == df_hardware['cost__inflation_adjusted'].max()].iloc[0, 0]
    # 2nd KPI
    df_computation['year'] = df_computation['day'].dt.year
    latest_comp = df_computation['training_computation_petaflop'].max()
    prev_comp = df_computation[df_computation['year'] == df_computation['year'].max()-1]['training_computation_petaflop'].max()
    delta_cost = (latest_comp - prev_comp)/prev_comp * 100
    # 3rd KPI
    avg_datapoint = df_datapoint.groupby('domain')['training_dataset_size__datapoints'].mean()
    avg_datapoint = avg_datapoint.sort_values(ascending=False).reset_index()
    # 4th KPI
    df_parameter['year'] = df_parameter['day'].dt.year
    avg_params = df_parameter.groupby('year')['parameters'].mean().iloc[-2]
    # 5th KPI
    df_cost_hardware['year'] = df_cost_hardware['day'].dt.year
    df_cost_hardware24 = df_cost_hardware[df_cost_hardware['year'] == 2024]
    df_cost_hardware24 = df_cost_hardware24.groupby('organization_categorization').agg({'training_computation_petaflop':'mean','parameters': 'mean'}).iloc[1,:]
    
    st.subheader("🔧 AI Development")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Most Expensive AI", f"{ai_sys}:", f"${latest_cost/1e6:.1f}M", help="Latest most expensive AI to train")
    col2.metric("Computation YoY:", f"{delta_cost:.1f}%", help="Year-over-Year change in training computation")
    col3.metric("Highest Training Datapoints:", f"{avg_datapoint.iloc[0, 1]/1e9:.1f}B", f"{avg_datapoint.iloc[0, 0]}", help=f"AI domain with highest average training datapoint")
    col4.metric("Avg Parameters:", f"{avg_params/1e9:.1f}B", help=f"Average adjusted parameter number in latest year")
    col5.metric("Industry Avg:", f"{df_cost_hardware24.iloc[0]/1e9:.1f}B pFLOP", f"{df_cost_hardware24.iloc[1]/1e9:.1f}B parameters", help=f"Industry developed AI systems in 2024")
    
    ai_dev_text = '''Understanding the resources required to develop AI systems helps us assess who can participate in AI development and how access to these technologies might be distributed.'''
    explain_text = '''**Trend**: Training costs have grown exponentially since 2017, with multimodal systems becoming the costliest to train.   
    **Actionable**: As costs and energy consumption continue rising, policymakers should consider implementing environmental regulations for AI training.'''
    explain_text2 = '''**Insight**: Language models require orders of magnitude more computation than other domains.    
    **Surprise**: Early vision systems from the 1960s, such as Perceptron, required remarkably high computation for their era.   
    **Implication**: The computational demands of AI may create barriers to entry for smaller organizations.'''
    explain_text3 = '''**Finding**: Modern language models use trillion-scale datasets (e.g., DeepSeek-V3's 14.8 trillion in 2024), while early vision systems used only thousands of data points.   
    **Concern**: These massive datasets raise questions about data sourcing practices and potential copyright issues.'''  
    explain_text4 = '''**Trend**: Industry collaborations now produce AI systems with the most parameters, outpacing purely academic efforts.       
    **Example**: In 2018, the Mesh Tensorflow Transformer (Industry) contained 2.8B parameters, exceeding academic collaborations of that time.'''
    explain_text5 = '''**Relationship**: There's a strong positive correlation between parameters and computation needs, though industry systems show greater parameter efficiency.   
    **Surprise**: Some academic systems use high computation despite having relatively fewer parameters.'''
    col1, col2, col3 = st.columns(3)
    with col1: 
        with st.popover("❓❓ Why This Matters"):
            st.markdown(ai_dev_text)
    with col2:
        with st.popover("💰 Explain Cost Chart"):
            st.markdown(explain_text)
    with col3:
        with st.popover("🖥️ Explain Computation Chart"):
            st.markdown(explain_text2)
            
    # Cost to Train AI Systems Plot
    color_discrete_map = {'Language': 'rgb(237,37,78)', 'Speech': 'rgb(69,56,35)','Vision & Image Generation': 'rgb(144,103,189)','Vision': 'rgb(64,89,173)', 
                          'Image Generation': 'rgb(4, 139, 168)','Multimodal': 'rgb(163,59,32)','Other': 'rgb(118,66,72)','Biology': 'rgb(12,206,187)','Games': 'rgb(242,158,76)'}
    fig = px.scatter(df_hardware, x="day", y="cost__inflation_adjusted", color="domain", text = 'entity',log_y=True, color_discrete_map=color_discrete_map,
                     labels={"cost__inflation_adjusted": "Cost (USD)", "day": "Time", "entity": "AI System", "Domain": "Domain"},
                     title="Energy Cost to Train AI Systems", width=800, height=450)
    fig.update_traces(marker=dict(size=8.5, opacity=0.8, line=dict(width=0.5, color='black')), textposition="top center", showlegend=True, 
                      textfont=dict(size=7, style="italic", color='black'))
    fig.update_layout(xaxis_title="Year", legend_title="Domain", hovermode="closest", yaxis=dict(type="log", tickvals=[1e3, 1e4, 1e5, 1e6, 1e7], ticktext=["1K", "10K", "100K", "1M", "10M"]), 
                      yaxis_title="Cost ($, inflation adjusted)", title_x=0.3, margin=dict(l=5, r=5, t=35, b=5), plot_bgcolor='rgba(240,247,244,0.5)')
    st.plotly_chart(fig, use_container_width=True)

    # 'Computation Used to Train AI Systems' Plot
    tickvals = [10**i for i in range(-12, 11)]
    color_discrete_map2={'Language': 'rgb(4, 139, 168)', 'Speech': 'rgb(242, 66, 54)', 'Vision': 'rgb(144, 103, 198)', 'Image Generation': 'rgb(98, 0, 179)',
                         'Multiple Domains': 'rgb(240, 56, 107)', 'Other': 'rgb(118, 66, 72)','Biology': 'rgb(138, 155, 104)', 'Games': 'rgb(242, 158, 76)'}
    fig2 = px.scatter(df_computation, x="day", y="training_computation_petaflop", color="domain", log_y=True, color_discrete_map=color_discrete_map2, 
                      labels={"training_computation_petaflop": "Computation", "day": "Time", "entity": "AI System", "domain": "Domain"},
                      title="Computation Used to Train AI Systems", width=400, height=400)
    fig2.update_traces(marker=dict(size=7, opacity=0.7, line=dict(width=0.5, color='black')), textposition="top center", showlegend=True, textfont=dict(size=9, style="italic"))
    fig2.update_layout(yaxis=dict(type="log", tickvals=tickvals), xaxis_title="Year", yaxis_title="Training Computation (petaFLOP)", hovermode="closest", 
                       legend_title="AI Domain", margin=dict(l=5, r=5, t=35, b=5), plot_bgcolor='rgba(240, 247, 244, 0.5)', title_x=0.3)
    st.plotly_chart(fig2, use_container_width=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.popover("📚 Explain Datapoint Chart"):
            st.markdown(explain_text3)
    with col2:
        with st.popover("📈 Explain Parameter Chart"):
            st.markdown(explain_text4)
    with col3:
        with st.popover("🔍 Explain Computation vs. Parameter"):
            st.markdown(explain_text5)

    # 'Datapoints Used to Train AI Systems' Plot
    tickvals3 = [10**i for i in range(1, 13)]
    color_discrete_map3={'Language': 'rgb(4, 139, 168)', 'Speech': 'rgb(242, 66, 54)', 'Vision': 'rgb(144, 103, 198)', 'Image Generation': 'rgb(98, 0, 179)',
                         'Multiple Domains': 'rgb(240, 56, 107)', 'Other': 'rgb(118, 66, 72)', 'Biology': 'rgb(138, 155, 104)', 'Games': 'rgb(242, 158, 76)'}
    fig3 = px.scatter(df_datapoint, x="day", y="training_dataset_size__datapoints", color="domain", log_y=True, color_discrete_map=color_discrete_map3,
                      labels={"training_dataset_size__datapoints": "Size", "day": "Time", "entity": "AI System", "domain": "Domain"}, 
                      title="Datapoints Used to Train AI Systems", hover_data = ['entity', 'domain'], width=400, height=400)
    fig3.update_traces(marker=dict(size=7, opacity=0.7, line=dict(width=0.5, color='black')), textposition="top center", showlegend=True, textfont=dict(size=9, style="italic"))
    fig3.update_layout(yaxis=dict(type="log", tickvals=tickvals3), xaxis_title="Year", yaxis_title="Training Datapoints", legend_title="AI Domain", 
                       hovermode="closest", margin=dict(l=5, r=5, t=35, b=5), plot_bgcolor='rgba(240, 247, 244, 0.5)', title_x=0.3)
    st.plotly_chart(fig3, use_container_width=True)

    # 'Number of Parameter Used to Train AI' Plot
    tickvals4 = [10**i for i in range(1, 13)]
    color_discrete_map4={'Academia & Industry Collab': 'rgb(179, 136, 235)', 'Industry': 'rgb(255, 90, 95)', 'Other': 'rgb(52, 46, 55)', 'Academia': 'rgb(8, 126, 139)'}
    fig4 = px.scatter(df_parameter, x="day", y="parameters", color="organization_categorization", log_y=True, title="Number of Parameter Used to Train AI",
                      labels={"parameters": "Parameters", "day": "Time", "entity": "AI System", "organization_categorization": "Organization"}, 
                      hover_data = ['entity', 'organization_categorization'], width=800, height=400, color_discrete_map=color_discrete_map4)
    fig4.update_traces(marker=dict(size=7.5, opacity=0.7, line=dict(width=0.5, color='black')), textposition="top center", showlegend=True, textfont=dict(size=9, style="italic"))
    fig4.update_layout(yaxis=dict(type="log", tickvals=tickvals4), xaxis_title="Year", yaxis_title="Number of Adjusted Parameters", hovermode="closest",
                      legend_title="Organization", margin=dict(l=5, r=5, t=35, b=5), title_x=0.28, plot_bgcolor='rgba(240, 247, 244, 0.5)')
    st.plotly_chart(fig4, use_container_width=True)

    # 'Training Computation vs. Parameters in AI Systems by Organization' Plot
    ytickvals = [10**i for i in range(-12, 11)]
    xtickvals = [10**i for i in range(1, 13)]
    color_discrete_map5={'Academia & Industry Collab': 'rgb(179, 136, 235)', 'Other': 'rgb(52, 46, 55)', 'Industry': 'rgb(255, 90, 95)', 'Academia': 'rgb(8, 126, 139)'}
    fig5 = px.scatter(df_cost_hardware, x="parameters", y="training_computation_petaflop", color="organization_categorization", log_y=True,
                      labels={"parameters": "Parameters", "training_computation_petaflop": "Computation", "entity": "AI System", "organization_categorization": "Organization"},
                      title="Training Computation vs. Parameters in AI Systems by Organization", hover_data = ['entity', 'organization_categorization'], 
                      width=800, height=400, color_discrete_map=color_discrete_map5)
    fig5.update_traces(marker=dict(size=7.5, opacity=0.7, line=dict(width=0.5, color='black')),textposition="top center", showlegend=True,textfont=dict(size=9, style="italic"))
    fig5.update_layout(yaxis=dict(type="log", tickvals = ytickvals), xaxis_title="Number of Adjusted Parameters", xaxis=dict(type="log", tickvals = xtickvals),
                       yaxis_title="Training Computation (petaFLOP)", legend_title="Organization", hovermode="closest", margin=dict(l=5, r=5, t=35, b=5), title_x=0.2, plot_bgcolor='rgba(240, 247, 244, 0.5)')
    st.plotly_chart(fig5, use_container_width=True)

# ---------------------------------------------------------------------------------------------------------
elif section == "🌍 Geographic Distribution":
    st.subheader("🌍 Geographic Distribution Interactive Plots")
    # KPIs
    df_cumulative25 = df_cumulative[df_cumulative['year'] == 2025]        
    us_share =(df_cumulative25[df_cumulative25['entity'] == "United States"]['cumulative_count'] / df_cumulative25['cumulative_count'].sum()).iloc[0]
    
    top_patent_country = df_patent_agg.sort_values(by='num_patent_applications__field_all', ascending=False)
    
    count = df_bill[df_bill['number_of_ai_related_bills_passed_into_law'] != 0].shape[0]
    print(f"{count}", "Country", "Passed AI-related Bill into Law")
               
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Leading Country", "USA", help="Country with highest AI systems by 2025")
    col2.metric("USA Market Share:", f"{us_share:.1%}", help="USA share in global AI systems")
    col3.metric("Highest Patent Application:", f"{top_patent_country.iloc[1,2]/1e3:.1f}K", f"{top_patent_country.iloc[1,0]}", help=f"Country with highest patent application")
    col4.metric("In Europe", f"{count}", "Country", help=f"Number of European countries passed AI-related bill into law")

    matter_text = '''The geographic concentration of AI development affects global power dynamics and determines which cultural perspectives are embedded in these influential technologies'''
    explain_text = '''**Dominance**: The US leads significantly in large-scale AI systems, followed by China, with other countries far behind.   
    **Emerging Players**: The UK and South Korea began showing notable AI development in 2021.   
    **Policy Implication**: This indicates a significant concentration of AI development power in a few nations.'''
    explain_text2 = '''**Dominance**: China leads with 365K patent applications, followed by the USA with 72K.   
    **Emerging Players**: Germany leads the EU region.'''
    explain_text3 = '''**Concern**: Few countries have enacted AI-related legislation.   
    **Finding**: The USA has passed 23 bills, with Portugal in second place.   
    **Surprise**: Despite being a major AI player, China has passed only 3 bills.'''
    col1, col2, col3, col4 = st.columns(4)
    with col1: 
        with st.popover("❓❓ Why This Matters"):
            st.markdown(matter_text)
    with col2:
        with st.popover("🤖 Explain AI Count Chart"):
            st.markdown(explain_text)
    with col3:
        with st.popover("📝 Explain Patent Chart"):
            st.markdown(explain_text2)
    with col4:
        with st.popover("💼 Explain Bill Chart"):
            st.markdown(explain_text3)
 
    # Cumulative Number of Large-Scale AI Systems by Country
    color_discrete_map6 = {'Canada': 'rgb(192, 43, 61)', 'China': 'rgb(20, 19, 1)', 'Finland': 'rgb(206, 162, 172)', 'France': 'rgb(166, 117, 161)', 'Germany': 'rgb(252, 100, 113)', 
                           'Hong Kong': 'rgb(163, 67, 133)', 'Israel': 'rgb(112, 110, 96)', 'Japan': 'rgb(170, 83, 98)', 'Russia': 'rgb(237, 174, 73)', 'Saudi Arabia': 'rgb(223, 87, 188)', 
                           'Singapore': 'rgb(249, 220, 92)', 'South Korea': 'rgb(297, 40, 61)', 'United Arab Emirates': 'rgb(183, 181, 179)', 'United Kingdom': 'rgb(237, 174, 73)', 'United States': 'rgb(184, 12, 9)'}
    
    fig6 = px.line(df_cumulative, x="year", y="cumulative_count", color="entity", markers=True, color_discrete_map=color_discrete_map6, 
                   labels={"entity": "Country", "year": "Year", "cumulative_count": "AI System Count"}, title="Cumulative Number of Large-Scale AI Systems by Country", width=550, height=450)
    fig6.update_traces(text=df_cumulative["entity"] + ": " + df_cumulative["cumulative_count"].astype(str), hoverinfo="text+name", 
                       marker=dict(size=7, opacity=0.8, line=dict(width=0.5, color='black')))
    fig6.update_layout(xaxis=dict(tickmode="linear", dtick=10), legend_title="Country", yaxis=dict(title="Cumulative AI System Count"), title_x=0.22, 
                       margin=dict(l=5, r=5, t=35, b=5), plot_bgcolor='rgba(229, 231, 230, 0.5)')
    st.plotly_chart(fig6, use_container_width=True)

    # World Map for 'Country-Wise AI-Related Total Patent Applications by 2024'
    fig7 = px.choropleth(df_patent_agg, locations='entity', locationmode="country names", color="num_patent_applications__field_all", hover_name=None, 
                         hover_data={"num_patent_applications__field_all": True}, color_continuous_scale="Viridis_r", width=500, height=400, 
                         labels={"entity": "Country", "num_patent_applications__field_all": "Application Count"}, title="Country-Wise AI-Related Total Patent Applications by 2024")
    fig7.update_layout(geo=dict(showcoastlines=True, showframe=True), title_x=0.22, margin=dict(l=5, r=5, t=25, b=5), plot_bgcolor='rgb(249, 248, 248)', coloraxis_colorbar=dict(title="Count"))
    st.plotly_chart(fig7, use_container_width=True)

    # World Map for 'AI-Related Passed Bill into Law by Country'
    fig8 = px.choropleth(df_bill, locations='entity', locationmode="country names", color="number_of_ai_related_bills_passed_into_law", 
                         hover_data={"number_of_ai_related_bills_passed_into_law": True}, hover_name=None, color_continuous_scale="Inferno_r", 
                         labels={"entity": "Country", "number_of_ai_related_bills_passed_into_law": "Passed Bill Count"}, title="Country-Wise AI-Related Passed Bill into Law by 2023", width=500, height=400)
    fig8.update_layout(geo=dict(showcoastlines=True, showframe=True), title_x=0.25, margin=dict(l=5, r=5, t=25, b=5), plot_bgcolor='rgb(249, 248, 248)', coloraxis_colorbar=dict(title="Count"))
    st.plotly_chart(fig8, use_container_width=True)

# ---------------------------------------------------------------------------------------------------------
elif section == "💡 Innovation":
    st.subheader("💡 Innovation Interactive Plots")

    # Innovation KPIs
    tot_research = df_affiliation.groupby('entity')['yearly_count'].sum()
    industry_percent = tot_research['Industry']/tot_research.sum() * 100
    df_academia = df_affiliation[df_affiliation['entity'] == 'Academia']
    prev_academia = df_academia[df_academia['year'] == 2023]['yearly_count'].sum()
    last_academia = df_academia[df_academia['year'] == 2024]['yearly_count'].sum()
    yoy_academia = (last_academia - prev_academia) / prev_academia * 100
    patents_2023 = df_patent_world['num_patent_granted__field_all'].sum()
    last_year = df_patent_world[df_patent_world['year'] == 2023]['num_patent_granted__field_all'].sum()
    prev_year = df_patent_world[df_patent_world['year'] == 2022]['num_patent_granted__field_all'].sum()
    yoy_growth = (last_year - prev_year) / prev_year * 100
    top_industry = df_patent_world2.groupby('industry')['patent_count'].sum()

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Industry Affiliation", f"{industry_percent:.1f}%", help="Percentage of industry affiliated AI system developers")
    col2.metric("Academia Affiliation YoY", f"{yoy_academia:.1f}%", help="Change in academia affiliation, 2022 → 2023")
    col3.metric("Granted AI Patents", f"{patents_2023/1e3:.1f}K", help=f"Worldwide granted AI patent count by 2023")
    col4.metric("Granted Patent YoY", f"{yoy_growth:.1f}%", help=f"Worldwide granted AI patent change, 2022 → 2023")
    col5.metric("Top Industry", f"{top_industry.max()/1e3:.1f}K", top_industry.idxmax(), help=f"Leading industry with granted AI patent")
    
    matter_text = '''Tracking innovation through patents and research affiliations helps us understand where AI capabilities are being developed and who controls this intellectual property.'''
    explain_text = '''**Shift**: Since 2015, industry involvement has grown dramatically while academic projects have declined, with no purely academic affiliations by 2024.   
    **Current State**: The Industry now produces most notable AI systems research.'''
    explain_text2 = '''**Explosion**: AI patent applications surged from 10K in 2013 to over 150K in 2021.   
    **Trend**: The percentage of granted applications increased until 2021 and then decreased, suggesting stricter approval policies.    
    **Industry Focus**: Personal Devices & Computing leads in granted patents, followed by Telecommunications. Banking & Finance holds the smallest share.'''
    col1, col2, col3 = st.columns(3)
    with col1: 
        with st.popover("❓❓ Why This Matters"):
            st.markdown(matter_text)
    with col2:
        with st.popover("💰 Explain Affiliation Chart"):
            st.markdown(explain_text)
    with col3:
        with st.popover("🖥️ Explain Patent Charts"):
            st.markdown(explain_text2)
    
    # 'Affiliation of Research Teams Building AI systems' Plot
    color_discrete_map9={'Academia': 'rgb(238, 99, 82)', 'Industry': 'rgb(121, 132, 120)', 'Academia & Industry Collab': 'rgb(76, 134, 168)', 'Other': 'rgb(170, 109, 163)'}
    fig9 = px.bar(df_affiliation, x="year", y="yearly_count", color="entity", text_auto=False, color_discrete_map = color_discrete_map9, 
                  labels={"entity": "Sector", "year": "Year", "yearly_count": "Count"}, title="Affiliation of Research Teams Building AI systems", width=700, height=400)
    fig9.update_traces(hoverinfo="text+name")
    fig9.update_layout(barmode="stack", yaxis=dict(title="Count"), xaxis=dict(title = "Publication Year", tickmode="linear", dtick=1, tickangle=-45), legend_title="Sector", 
                       hovermode="x unified", title_x = 0.22, margin=dict(l=10, r=5, t=35, b=5, pad=5), plot_bgcolor='rgb(249, 248, 248)')
    st.plotly_chart(fig9, use_container_width=True)
    
    # Worldwide AI Related Patent Applications by Status
    fig10 = go.Figure()
    fig10.add_trace(go.Bar(x=df_patent_world['year'], name="Granted", y=df_patent_world['num_patent_granted__field_all'], text=df_patent_world['num_patent_granted__field_all'],
                           textfont=dict(size=10, weight='bold'), marker_color='rgb(97, 152, 142)'))
    fig10.add_trace(go.Bar(x=df_patent_world['year'], name="Applied", y=df_patent_world['num_patent_applications__field_all'],
                           text=df_patent_world['num_patent_applications__field_all'], textfont=dict(size=10, weight='bold'), marker_color='rgb(222, 143, 110)'))
    fig10.update_traces(hoverinfo="text+name", marker=dict(opacity=0.8))
    fig10.update_layout(barmode="stack", yaxis=dict(title="Patent Count"), xaxis=dict(title="Year", tickmode="linear", dtick=1, tickangle=0), legend_title="Status", 
                        hovermode="x unified", margin=dict(l=10, r=5, t=35, b=5, pad=5), width=250, height=400, plot_bgcolor='rgba(249, 248, 248, 0.5)', 
                        title="Worldwide AI Related Patent Applications by Status", title_x=0.27)
    st.plotly_chart(fig10, use_container_width=True, width=250, height=400)

    # 'Worldwide Annual Granted AI Related Patents by Industry' Plot
    color_discrete_map11={'Banking & Finance': 'rgb(18, 19, 15)', 'Industry & Manufacturing': 'rgb(214, 143, 214)', 'Energy & Management': 'rgb(214, 69, 80)', 
                          'Business': 'rgb(119, 133, 172)', 'Security': 'rgb(139, 93, 51)', 'Life Sciences': 'rgb(134, 157, 122)', 'Transportation': 'rgb(255, 133, 82)', 
                          'Physical Sciences & Engineering': 'rgb(60, 79, 118)','Telecommunication': 'rgb(127, 5, 95)', 'Personal Devices & Computing': 'rgb(11, 122, 117)'}
    fig11 = px.bar(df_patent_world2, x="year", y="patent_count", color="industry", text_auto=False, color_discrete_map = color_discrete_map11,
                   labels={"industry": "Industry", "year": "Year", "patent_count": "Patent Count"}, title="Worldwide Annual Granted AI Related Patents by Industry", width=700, height=400)
    fig11.update_traces(hoverinfo="text+name")
    fig11.update_layout(barmode="stack", xaxis=dict(title = "Year", tickmode="linear", dtick=1, tickangle=0), yaxis=dict(title="Granted Patent Count"), 
                        legend_title="Industry", title_x=0.22, margin=dict(l=100, r=5, t=35, b=5, pad=5), plot_bgcolor='rgb(249, 248, 248)')
    st.plotly_chart(fig11, use_container_width=True)

# ---------------------------------------------------------------------------------------------------------
elif section == "💵 Investment":
    st.subheader("💵 Investment Interactive Plots")

    total_invest = df_investment['world'].sum()
    us_vs_china = (df_investment[df_investment['year'] == 2023]['united_states'].sum() / df_investment[df_investment['year'] == 2023]['china'].sum())

    volatility_scores = []
    entities = df_invest_general['entity'].unique()
    for entity in entities:
        score = calculate_volatility(df_invest_general, entity)
        volatility_scores.append({'entity': entity, 'volatility_score': score})
    volatility_df = pd.DataFrame(volatility_scores).sort_values('volatility_score', ascending=False)

    df_invest_general['geo_concentration'] = df_invest_general.apply(geographic_concentration, axis=1)
    latest_year = df_invest_general['year'].max()
    concentration_table = df_invest_general[df_invest_general['year'] == latest_year][['entity', 'geo_concentration']].sort_values('geo_concentration', ascending=False)
    
    latest = df_investment3[df_investment3['year'] == 2023]['generative_ai'].sum()
    prev = df_investment3[df_investment3['year'] == 2022]['generative_ai'].sum()
    gen_ai_growth = (latest-prev)/prev * 100

    #KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total AI Investment", f"${total_invest/1e9:.1f}B",  help="Worldwide total private investment in AI, 2013-2023")
    col2.metric("US vs China", f"{us_vs_china:.1f}x", help="Private investment USA to China ratio in 2023")
    col3.metric("Highest Volatility", f"{volatility_df.iloc[0,1]:.1f}%", volatility_df.iloc[0,0], help=f"Private investment volatility score of AI sectors")
    col4.metric("Geographic Monopoly", concentration_table.iloc[0, 0], help=f"Concentration private investment in AI sectors")
    col5.metric("Generative AI Growth", f"{gen_ai_growth:.1f}%", help=f"Generative AI private investment growth, 2022 → 2023")

    matter_text = '''Investment patterns reveal which AI applications and regions are attracting capital, shaping the future direction of AI development and commercialization.'''
    explain_text = '''**Geographic**: The US dominates investments, followed by China.    
    **Trend**: Worldwide annual private investment increased until 2021, then declined in 2022 due to the COVID-19 pandemic.    
    **Recovery:** After 2022, the USA showed elevated investment growth while China and the EU region began recovery.'''
    explain_text2 = '''**Dominance:** Natural Language Processing & Customer Support claim the largest share of private investment.    
    **Infrastructure Investment Surge**: AI Infrastructure & Governance showed massive investment spikes ($16B in 2023), suggesting a fundamental shift toward building robust AI foundations.'''
    explain_text3 = '''**Hockey Stick**: Investment exploded from $89M in 2019 to $4B in 2023—a 250x growth in 4 years.         
    **Warning Sign**: The 2022 dip suggests potential sector volatility.'''
    col1, col2, col3, col4 = st.columns(4)
    with col1: 
        with st.popover("❓❓ Why This Matters"):
            st.markdown(matter_text)
    with col2:
        with st.popover("💸 Explain Regional Chart"):
            st.markdown(explain_text)
    with col3:
        with st.popover("🧰 Explain Sectoral Charts"):
            st.markdown(explain_text2)
    with col4:
        with st.popover("🤖 Explain Generative AI Chart"):
            st.markdown(explain_text3)
    
    # Annual Private Investment in AI by Location
    fig12 = go.Figure()
    fig12.add_trace(go.Scatter(x=df_investment['year'], y=df_investment['china'], name='China', mode='lines+markers', marker_color='rgb(150, 2, 0)', marker_size = 8, opacity=0.7))
    fig12.add_trace(go.Scatter(x=df_investment['year'], y=df_investment['united_states'], name='United States', mode='lines+markers', marker_size = 8, marker_color='rgb(225, 188, 41)', opacity=0.7))
    fig12.add_trace(go.Scatter(x=df_investment['year'], y=df_investment['european_union_and_united_kingdom'], name='European Union & United Kingdom', mode='lines+markers', 
                               marker_color='rgb(36, 30, 78)', marker_size = 8, opacity=0.7))
    fig12.add_trace(go.Scatter(x=df_investment['year'], y=df_investment['world'],name='World', mode='lines+markers', marker_size = 8,marker_color='rgb(63, 124, 172)', opacity=0.7))
    fig12.update_layout(xaxis=dict(title="Year", tickmode="linear", dtick=1, tickangle=0), yaxis=dict(title="Private Investment (USD)"), legend_title="Location",
                        margin=dict(l=5, r=5, t=35, b=5, pad=5), hovermode="x unified", title="Annual Private Investment in AI by Location", title_x = 0.2, 
                        plot_bgcolor = 'rgba(248, 247, 255, 0.7)', width=700, height=400)
    st.plotly_chart(fig12, use_container_width=True)

    # 'Worldwide Annual Private Investment in AI by Domain' Plot
    color_discrete_map13={'Insurance Tech': 'rgb(128, 94, 115)', 'Marketing & Digital Ads': 'rgb(255, 93, 115)', 'Manufacturing': 'rgb(45, 70, 84)', 'Creative Content': 'rgb(183, 68, 184)',
                          'Educational Tech': 'rgb(96, 147, 93)','Energy Industry': 'rgb(198, 202, 83)','Medical & Healthcare': 'rgb(170, 80, 66)', 'Retail': 'rgb(243, 156, 107)'}
    fig13 = px.line(df_investment1, x="year", y="world", color="entity", markers=True, labels={"entity":"Domain","year": "Year", "world": "Private Investment"}, 
                    title="Worldwide Annual Private Investment in AI by Domain", width=700, height=400, color_discrete_map = color_discrete_map13)
    fig13.update_traces(text=df_investment1["entity"]+ ": " + df_investment1["world"].astype(str), hoverinfo="text+name")
    fig13.update_traces(marker=dict(size=8, opacity=0.7, line=dict(width=0.5, color='black')))
    fig13.update_layout(xaxis=dict(tickmode="linear", dtick=1, tickangle=0), yaxis=dict(title="Private Investment (USD)"), title_x = 0.195, legend_title="Domain", 
                        margin=dict(l=5, r=5, t=35, b=5, pad=5), hovermode="closest", plot_bgcolor = 'rgba(248, 247, 255, 0.7)')
    st.plotly_chart(fig13, use_container_width=True)

    # 'Worldwide Annual Private Investment in AI by Domain' Second Plot
    color_discrete_map14={'AI Infrastructure & Governance': 'rgb(74, 13, 103)', 'Hardware': 'rgb(198, 202, 83)','Augmented & Virtual Reality': 'rgb(104, 216, 155)',
                          'Autonomous Vehicles': 'rgb(255, 127, 17)', 'Quantum Computing': 'rgb(99, 105, 209)','Cybersecurity & Data Protection': 'rgb(59, 65, 60)',
                          'Data Management & Processing': 'rgb(0, 175, 185)','Facial Recognition': 'rgb(214, 69, 80)', 'NLP & Customer Support': 'rgb(227, 101, 193)'}
    fig14 = px.line(df_investment2, x="year", y="world", color="entity", markers=True, labels={"entity":"Domain","year": "Year", "world": "Private Investment"},
                    title="Worldwide Annual Private Investment in AI by Domain", width=600, height=400, color_discrete_map = color_discrete_map14)
    fig14.update_traces(text=df_investment2["entity"]+ ": " + df_investment2["world"].astype(str), hoverinfo="text+name", 
                        marker=dict(size=8, opacity=0.7, line=dict(width=0.5, color='black')))
    fig14.update_layout(xaxis=dict(tickmode="linear", dtick=1, tickangle=0), title_x = 0.157, yaxis=dict(title="Private Investment (USD)"), hovermode="closest",
                        legend_title="Domain", margin=dict(l=5, r=5, t=35, b=5, pad=5),plot_bgcolor='rgba(248, 247, 255, 0.7)')
    st.plotly_chart(fig14, use_container_width=True)

    # Volatility Visualization
    fig141 = px.bar(volatility_df, x='entity', y='volatility_score', color='volatility_score', title='<b>AI Sector Volatility Scores</b><br>Max Yearly Growth - Max Yearly Decline',
                    labels={'volatility_score': 'Volatility Score', 'entity': 'Sector'}, color_continuous_scale='thermal_r', width=700, height=400)

    fig141.update_layout(hovermode='x unified', xaxis={'categoryorder':'total descending'}, yaxis_title="Volatility Score (Percentage)", plot_bgcolor='rgba(248, 247, 255, 0.7)')
    avg_score = volatility_df['volatility_score'].mean()
    fig141.add_hline(y=avg_score, line_dash="dot", annotation_text=f'Average: {avg_score:.0f}', annotation_position="top right")
    st.plotly_chart(fig141, use_container_width=True)
    
    # 'Worldwide Private Investment in Generative AI' Bar Plot
    fig15 = px.bar(df_investment3, x="year", y="generative_ai",labels={"year": "Year", "generative_ai": "Amount($)"}, title="Worldwide Private Investment in Generative AI", width=500, height=400)
    fig15.update_traces(text=df_investment3['generative_ai'].apply(format_investment),textfont_size=12.5, textfont_weight='bold', textangle=0,textfont_color='rgb(60, 60, 60)', 
                        textposition="outside",hoverinfo="text", marker_color='rgb(255, 90, 95)', marker_opacity=0.7,marker_line_color='rgb(60, 60, 60)', marker_line_width=1.5)
    fig15.update_layout(xaxis=dict(title="Year", tickmode="linear", dtick=1, tickangle=0),yaxis=dict(title="Private Investment (USD)"), title_x = 0.3,
                        margin=dict(l=0, r=5, t=35, b=5, pad=5), plot_bgcolor='rgba(248, 247, 255, 0.7)')
    st.plotly_chart(fig15, use_container_width=True)

# ---------------------------------------------------------------------------------------------------------
elif section == "👥 Public View":
    # Mini-poll
    st.subheader("What's Your AI Opinion?")
    with st.form("ai_opinion_poll"):
        opinion = st.radio("How do you think AI will impact society in the next 20 years?", ["Mostly helpful", "Mostly harmful", "Both equally", "Not sure"])
        age_group = st.selectbox("Your age group", ["Under 30", "30-49", "50-64", "65+"])
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.success("Thanks for sharing your opinion!")
    
    st.subheader("👥 Public View Interactive Plots")
    # Americans Opinion About Their Work Being Automated
    color_discrete_map16={"Don't Know": "rgb(58, 45, 50)", "Worried": "rgb(221, 96, 49)", "Not Worried": "rgb(68, 114, 202)", "Very Worried": "rgb(147, 3, 46)"}
    fig16 = px.bar(df_automated_survey, x='year', y='opinion_count', color='opinion', barmode='stack', facet_col='entity', color_discrete_map = color_discrete_map16,
                   labels = {'entity': 'Age Group', 'opinion': 'Opinion', 'year': 'Year','opinion_count': 'Count'})
    fig16.update_traces(marker_line_color='rgb(60, 60, 60)',marker_line_width = 1.5, marker_opacity=0.8)
    fig16.update_layout(title_text='Americans Opinion About Their Work Being Automated',xaxis_title='Year', yaxis_title='Opinion Count',legend_title='Opinion', 
                        width = 1000, height = 450, plot_bgcolor='rgb(250, 249, 249)')
    st.plotly_chart(fig16, use_container_width=True)

    # 'Views on AI's Societal Impact in Next 20 Years by Country' Stacked Bar Plot
    color_discrete_map17 = {'Mostly Helpful':'rgb(0, 127, 255)', 'No Opinion':'rgb(128, 138, 159)','Mostly Harmful':'rgb(196, 32, 33)', 'Neither':'rgb(213, 137, 54)'}
    fig17 = px.bar(df_view_country, x='opinion_percent', y='entity', color='opinion', color_discrete_map = color_discrete_map17, barmode='stack',
                   labels = {'entity': 'Country', 'opinion': 'Opinion', 'year': 'Year', 'opinion_percent': 'Percentage'})
    fig17.update_traces(texttemplate='%{x:.1f}%', textposition='inside', textfont = dict(size = 10.5, weight = 'bold'), marker_line_color='rgb(60, 60, 60)', marker_line_width=1.5, marker_opacity=0.7)
    fig17.update_layout(title_text="Views on AI's Societal Impact in Next 20 Years by Country", title_x=0.165, xaxis_title = '',yaxis_title='',legend_title='Opinion',
                        margin=dict(l=100, r=5, t=35, b=5, pad=5), width=900, height=400, plot_bgcolor='rgb(250, 249, 249)')
    st.plotly_chart(fig17, use_container_width=True)

    # 'Views on AI's Societal Impact in Next 20 Years by Region' Plot
    color_discrete_map18 = {'Mostly Helpful':'rgb(14, 177, 210)', 'No Opinion':'rgb(66, 75, 84)','Mostly Harmful':'rgb(255, 0, 53)', 'Neither':'rgb(206, 141, 102)'}
    fig18 = px.bar(df_view_continent21, x='opinion_percent', y='entity', color='opinion', color_discrete_map= color_discrete_map18, barmode='stack',
                   labels = {'entity': 'Country', 'opinion': 'Opinion', 'year': 'Year', 'opinion_percent': 'Percentage'})
    fig18.update_traces(texttemplate='%{x:.1f}%', textposition='inside',textfont = dict(size = 10.5, weight = 'bold'),marker_line_color='rgb(60, 60, 60)',marker_line_width=1.5, marker_opacity=0.8)
    fig18.update_layout(title_text="Views on AI's Societal Impact in Next 20 Years by Region",title_x=0.21, xaxis_title = '',yaxis_title='',legend_title='Opinion',
                        margin=dict(l=100, r=5, t=35, b=5, pad=5),width=800, height=400, plot_bgcolor='rgb(250, 249, 249)')
    st.plotly_chart(fig18, use_container_width=True)

    # 'Male/Female Views on AI's Societal Impact' Sunburst Charts
    color_discrete_map19 = {'Mostly Helpful': 'rgb(64, 71, 109)', 'No Opinion': 'rgb(172, 190, 163)','Mostly Harmful': 'rgb(242, 71, 48)', 'Neither': 'rgb(189, 160, 188)'}
    fig19 = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]],subplot_titles=("Male/Female Views on AI's Societal Impact (2019)",
                                                                                                           "Male/Female Views on AI's Societal Impact (2021)"))
    sunburst1 = px.sunburst(df_view_gender19, path=['entity', 'opinion'], color='opinion', values='opinion_percent',color_discrete_map=color_discrete_map19,
                            custom_data=['entity', 'opinion', 'opinion_percent'],hover_data=['entity', 'opinion', 'opinion_percent'])
    sunburst2 = px.sunburst(df_view_gender21, path=['entity', 'opinion'], color='opinion', values='opinion_percent', color_discrete_map=color_discrete_map19,
                            custom_data=['entity', 'opinion', 'opinion_percent'], hover_data=['entity', 'opinion', 'opinion_percent'])
    fig19.add_trace(sunburst1.data[0], row=1, col=1)
    fig19.add_trace(sunburst2.data[0], row=1, col=2)
    fig19.update_traces(hovertemplate='<b>%{label}</b><br>Value: %{value}<br>Gender: %{customdata[0]}', texttemplate='%{label}<br>%{percentEntry:.1%}',
                        insidetextorientation='auto', textfont=dict(size=11.5))
    fig19.update_layout(margin=dict(t=50, l=30, r=0, b=0), plot_bgcolor='rgb(14, 177, 210)', width = 900, height = 450)
    st.plotly_chart(fig19, use_container_width=True)

    # 'Global Views on Self-Driving Cars by Demographic Group (2021)' Plot
    color_discrete_map20={'Feel Safe': 'rgb(23, 190, 187)', 'Not Feel Safe': 'rgb(255, 49, 46)',"Don't Know": 'rgb(242, 187, 5)', 'No Response': 'rgb(34, 12, 16)'}
    fig20 = px.bar(df_view3, y="entity", x="view_percent", color="view", text_auto=False,labels={"view": "View", "entity": "Group", "view_percent": "Percent"},
                   title="Global Views on Self-Driving Cars by Demographic Group (2021)", width=900, height=400, color_discrete_map = color_discrete_map20)
    fig20.update_traces(hoverinfo="text+name", texttemplate='%{x:.0f}%', textposition='inside',textfont = dict(size = 10.5, weight = 'bold'),
                        marker_line_color='rgb(60, 60, 60)', marker_line_width=1.5, marker_opacity=0.8)
    fig20.update_layout(barmode="stack", xaxis=dict(title = "", tickmode="linear", dtick=10, tickangle=0), title_x = 0.135, 
                        yaxis={'categoryorder': 'array', 'categoryarray': ['65+ years', '50-64 years', '30-49 years', '15-29 years', 'Poorest 20%', 'Richest 20%']},
                        yaxis_title="", legend_title="View", margin=dict(l=100, r=5, t=35, b=5, pad=5), width=800, height=400, plot_bgcolor='rgb(250, 249, 249)')
    st.plotly_chart(fig20, use_container_width=True)

# ---------------------------------------------------------------------------------------------------------
elif section == "🔍 Comparison Tool":
    st.subheader("Comparison Tool")
    st.markdown("Use this tool to compare different aspects of AI development across countries, domains, or time periods.")
    
    col1, col2 = st.columns(2)
    with col1:
        comparison_type = st.selectbox("Compare by:", ["Country", "Domain", "Organization Type"])
    with col2:
        metric = st.selectbox("Metric:", ["Investment", "Patents", "System Count", "Training Cost"])
    
    if st.button("Generate Comparison"):
        # Placeholder for comparison logic
        st.write("Comparison results would appear here based on selected parameters")
        
        # Example visualization
        fig = px.bar(x=["USA", "China", "EU", "Other"], y=[45, 38, 12, 5],labels={'x': 'Region', 'y': f'{metric} (Billions)'},title=f"{metric} Comparison by {comparison_type}")
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(''':rainbow[End-to-end project is done by] :blue-background[Sevilay Munire Girgin]''')
