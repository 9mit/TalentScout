"""
Privacy UI - Streamlit Interface for Privacy Management
GDPR Compliance Dashboard
"""

import streamlit as st
from src.privacy_manager import PrivacyManager, show_privacy_notice
import os


def privacy_settings_page():
    """Streamlit page for privacy settings and GDPR compliance"""
    
    st.markdown("## 🔒 Privacy & Data Management")
    st.markdown("### GDPR Compliance Dashboard")
    st.markdown("---")
    
    pm = PrivacyManager()
    
    # Create tabs for different privacy features
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Privacy Policy", 
        "✅ Consent Management", 
        "📥 Data Export", 
        "🗑️ Data Deletion",
        "📊 Data Summary"
    ])
    
    # TAB 1: Privacy Policy
    with tab1:
        st.markdown("### Privacy Policy")
        
        if os.path.exists("PRIVACY_POLICY.md"):
            with open("PRIVACY_POLICY.md", 'r') as f:
                policy_content = f.read()
            st.markdown(policy_content)
        else:
            st.warning("Privacy policy file not found.")
        
        st.markdown("---")
        st.info("💡 **Your Rights:** You have the right to access, rectify, erase, and export your data at any time.")
    
    # TAB 2: Consent Management
    with tab2:
        st.markdown("### Consent Management")
        st.markdown("Manage your data processing consents")
        
        # Show current consents
        consents = pm.get_all_consents()
        
        if consents:
            st.markdown("#### Current Consent Status")
            for consent_type, details in consents.items():
                status = "✅ Given" if details.get('given') else "❌ Withdrawn"
                date = details.get('date', 'Unknown')
                st.write(f"**{consent_type.replace('_', ' ').title()}:** {status} (Date: {date})")
        else:
            st.info("No consent records found.")
        
        st.markdown("---")
        st.markdown("#### Update Consent")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Give Consent for Data Collection", use_container_width=True):
                pm.record_consent('data_collection', True)
                pm.record_consent('analytics', True)
                pm.record_consent('ai_processing', True)
                st.success("✅ Consent recorded!")
                st.rerun()
        
        with col2:
            if st.button("❌ Withdraw All Consent", use_container_width=True):
                pm.record_consent('data_collection', False)
                pm.record_consent('analytics', False)
                pm.record_consent('ai_processing', False)
                st.warning("⚠️ Consent withdrawn. Some features may be limited.")
                st.rerun()
        
        st.markdown("---")
        st.markdown("#### What Each Consent Means")
        st.info("""
        **Data Collection:** Allows storing quiz results and performance data
        
        **Analytics:** Allows processing data for performance insights
        
        **AI Processing:** Allows sending anonymized data to Google Gemini for question generation
        """)
    
    # TAB 3: Data Export
    with tab3:
        st.markdown("### Data Export (Right to Access)")
        st.markdown("Download all your data in a portable format")
        
        st.info("📋 **GDPR Right to Access:** You can request a copy of all data we have about you.")
        
        export_format = st.selectbox(
            "Select Export Format",
            ["JSON", "Excel"],
            help="Choose the format for your data export"
        )
        
        if st.button("📥 Export All My Data", use_container_width=True, type="primary"):
            with st.spinner("Exporting your data..."):
                format_map = {"JSON": "json", "Excel": "excel"}
                filename = pm.export_all_user_data(format=format_map[export_format])
                
                if filename:
                    st.success(f"✅ Data exported successfully!")
                    st.info(f"📁 **File saved:** {filename}")
                    
                    # Offer download
                    if os.path.exists(filename):
                        with open(filename, 'rb') as f:
                            file_data = f.read()
                        
                        st.download_button(
                            label="⬇️ Download Export File",
                            data=file_data,
                            file_name=filename,
                            mime="application/octet-stream"
                        )
                else:
                    st.error("❌ Export failed. Please try again.")
        
        st.markdown("---")
        st.markdown("#### What's Included in the Export?")
        st.write("""
        - All quiz results and scores
        - Practice history
        - Candidate data (if applicable)
        - Consent records
        - Timestamps and metadata
        """)
    
    # TAB 4: Data Deletion
    with tab4:
        st.markdown("### Data Deletion (Right to Erasure)")
        st.markdown("Permanently delete your data")
        
        st.warning("⚠️ **Warning:** Data deletion is permanent and cannot be undone!")
        
        st.info("📋 **GDPR Right to Erasure:** You have the right to request deletion of your personal data.")
        
        st.markdown("---")
        
        # Selective deletion
        st.markdown("#### Selective Deletion")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Delete Quiz Data Only", use_container_width=True):
                if 'confirm_quiz_delete' not in st.session_state:
                    st.session_state.confirm_quiz_delete = True
                    st.warning("⚠️ Click again to confirm deletion of quiz data")
                else:
                    pm.delete_quiz_data(confirm=True)
                    st.success("✅ Quiz data deleted!")
                    del st.session_state.confirm_quiz_delete
                    st.rerun()
        
        with col2:
            if st.button("🗑️ Delete Candidate Data Only", use_container_width=True):
                if 'confirm_candidate_delete' not in st.session_state:
                    st.session_state.confirm_candidate_delete = True
                    st.warning("⚠️ Click again to confirm deletion of candidate data")
                else:
                    pm.delete_candidate_data(confirm=True)
                    st.success("✅ Candidate data deleted!")
                    del st.session_state.confirm_candidate_delete
                    st.rerun()
        
        st.markdown("---")
        
        # Complete deletion
        st.markdown("#### Complete Deletion")
        st.error("🚨 This will delete ALL your data permanently!")
        
        delete_confirmation = st.text_input(
            "Type 'DELETE ALL MY DATA' to confirm complete deletion:",
            key="delete_confirm_text"
        )
        
        if st.button("🗑️ DELETE ALL DATA", use_container_width=True, type="primary"):
            if delete_confirmation == "DELETE ALL MY DATA":
                pm.delete_all_user_data(confirm=True)
                st.success("✅ All data has been permanently deleted!")
                st.balloons()
            else:
                st.error("❌ Confirmation text does not match. Data not deleted.")
    
    # TAB 5: Data Summary
    with tab5:
        st.markdown("### Data Summary & Transparency")
        st.markdown("Overview of data stored in the system")
        
        summary = pm.get_data_summary()
        
        if summary:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Quiz Results", summary.get('quiz_results_count', 0))
            with col2:
                st.metric("Prep History", summary.get('prep_history_count', 0))
            with col3:
                st.metric("Candidates", summary.get('candidates_count', 0))
            with col4:
                st.metric("DB Size (MB)", f"{summary.get('database_size_mb', 0):.2f}")
        
        st.markdown("---")
        
        # Access log
        st.markdown("#### Recent Data Access Log")
        st.markdown("Audit trail of data access and modifications")
        
        access_log = pm.get_access_log(limit=20)
        
        if not access_log.empty:
            st.dataframe(
                access_log[['access_type', 'table_name', 'purpose', 'access_date']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No access log entries found.")
        
        st.markdown("---")
        
        # Anonymization
        st.markdown("#### Data Anonymization")
        st.info("Automatically anonymize data older than 90 days to protect privacy")
        
        if st.button("🔒 Anonymize Old Data (90+ days)", use_container_width=True):
            with st.spinner("Anonymizing old data..."):
                success = pm.anonymize_old_data(days_old=90)
                if success:
                    st.success("✅ Old data anonymized successfully!")
                else:
                    st.error("❌ Anonymization failed.")
        
        st.markdown("---")
        st.markdown("#### Data Retention Policy")
        st.write("""
        - **Quiz Data:** Retained indefinitely unless manually deleted
        - **Candidate Data:** Retained until manually deleted
        - **Analytics Data:** Aggregated and anonymized after 90 days
        - **Access Logs:** Retained for audit purposes
        """)


# Add to main app
def add_privacy_notice_banner():
    """Add privacy notice banner to app"""
    st.info("""
    🔒 **Privacy Notice:** This app stores data locally. You have full control over your data. 
    Visit the Privacy Settings page to manage your data and consents.
    """)
