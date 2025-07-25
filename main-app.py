import streamlit as st
import asyncio
import pandas as pd

from modules.data_collector import DataCollector
from modules.economic_web_analyzer import EconomicWebAnalyzer
from modules.miller_heiman_analyzer import MillerHeimanAnalyzer
from modules.opportunity_predictor import OpportunityPredictor
from modules.relationship_mapper import RelationshipMapper
from modules.intelligence_engine import IntelligenceEngine
from modules.analytics_engine import AnalyticsEngine

st.set_page_config(page_title="Strategic Account System", page_icon="🎯", layout="wide")

class StrategicAccountSystem:
    def __init__(self):
        self.data_collector = DataCollector()
        self.economic_web = EconomicWebAnalyzer()
        self.miller_heiman = MillerHeimanAnalyzer()
        self.opportunity_predictor = OpportunityPredictor()
        self.relationship_mapper = RelationshipMapper()
        self.intelligence = IntelligenceEngine()
        self.analytics = AnalyticsEngine()

    async def run_analysis(self, company_name, company_website, user_connections_df):
        try:
            st.header(f"Strategic Analysis for: {company_name}", divider='rainbow')

            with st.spinner("Step 1/5: Gathering live intelligence on the account..."):
                company_data = await self.data_collector.collect_company_data(company_name, company_website)
                if company_data.get('error'):
                    st.error(f"Could not gather data for {company_name}. Error: {company_data['error']}")
                    st.stop()
                
                initial_intelligence = self.intelligence.analyze_initial_fit(company_data, {})

            st.subheader("Initial Fit Assessment")
            col1, col2 = st.columns(2)
            col1.metric("Company Fit Score", f"{initial_intelligence.get('fit_score', 'N/A')}%")
            with st.expander("Show Key Insights"):
                for insight in initial_intelligence.get('key_insights', []):
                    st.markdown(f"• {insight}")
            
            with st.spinner("Step 2/5: Identifying top sales opportunities..."):
                adjacent_possibles = self.economic_web.identify_adjacent_possibles(company_data)
                predicted_opportunities = self.opportunity_predictor.predict_opportunities(company_data, adjacent_possibles)
            
            st.subheader("Top Sales Opportunity Identified")
            if not predicted_opportunities:
                st.warning("Could not identify a clear sales opportunity based on current data.")
                st.stop()
            top_opportunity = predicted_opportunities[0]
            st.success(f"**Opportunity:** {top_opportunity.get('name')}\n\n*Description: {top_opportunity.get('description')}*")

            with st.spinner("Step 3/5: Analyzing the strategic sales position..."):
                buying_influences = self.miller_heiman.identify_buying_influences(company_data)
                red_flags, strengths = self.miller_heiman.analyze_position(company_data, initial_intelligence)
                strategic_position = self.analytics.calculate_strategic_score(red_flags, strengths)

            st.subheader("Strategic Selling Analysis")
            st.metric("Strategic Position Score", f"{strategic_position.get('score', 'N/A')}/100", delta=strategic_position.get('trend'))

            with st.spinner("Step 4/5: Analyzing network for introduction paths..."):
                all_paths = await self.relationship_mapper.map_all_introduction_paths(user_connections_df, company_data, buying_influences)

            st.subheader("Introduction Paths to Key Buyers")
            direct_paths = [p for p in all_paths if p['type'] == 'Direct (1st Degree)']
            strategic_paths = [p for p in all_paths if p['type'] == 'Strategic (2nd Degree)']

            if not all_paths: st.warning("No clear introduction paths found.", icon="⚠️")
            if direct_paths:
                st.success("Direct Connections Found!")
                for path in direct_paths:
                    st.markdown(f"**Direct Path to {path['target']['role']}:** You are connected to **{path['target']['name']}** ({path['target']['title']}).")
            if strategic_paths:
                st.info("Strategic Introduction Paths Found!")
                for path in strategic_paths:
                    st.markdown(f"**Path to {path['target_role']}:** Ask your connection **{path['bridge_contact']['name']}** ({path['bridge_contact']['title']} at **{path['bridge_contact']['company']}**) for an introduction.")

            with st.spinner("Step 5/5: Calculating win probability and action plan..."):
                final_analysis = self.analytics.predict_win_probability(company_data, strategic_position, all_paths)
            
            st.subheader("Final Prediction & Action Plan", divider='rainbow')
            st.metric("Probability of Winning", f"{final_analysis.get('win_probability', 'N/A')}%")
            st.markdown("### How to Improve Your Chances:")
            for recommendation in final_analysis.get('recommendations', []):
                st.markdown(f"**- {recommendation}**")

        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

def main():
    st.title("🎯 Strategic Account Management System")
    with st.sidebar:
        st.header("1. Target Account Information")
        company_name = st.text_input("Company Name", "Salesforce")
        st.header("2. Your LinkedIn Connections")
        st.markdown("[How to export connections?](https://www.linkedin.com/help/linkedin/answer/a569524/)")
        uploaded_file = st.file_uploader("Upload 'Connections.csv'", type=['csv'])
        with st.expander("Data Privacy"):
            st.warning("Your data is safe. This app processes your file in memory for this session only and does not save it.", icon="🔒")
        analyze_button = st.button("🚀 Analyze Account", use_container_width=True, type="primary")

    if analyze_button:
        if not all([company_name, uploaded_file]):
            st.error("Please provide the company name and upload your Connections.csv file.")
        else:
            try:
                connections_df = pd.read_csv(uploaded_file)
                if 'Company' not in connections_df.columns:
                    st.error("Invalid CSV file. Must contain a 'Company' column.")
                else:
                    system = StrategicAccountSystem()
                    asyncio.run(system.run_analysis(company_name, "", connections_df))
            except Exception as e:
                st.error(f"Failed to process file. Error: {e}")

if __name__ == "__main__":
    main()
