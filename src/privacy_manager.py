"""
Privacy Manager - GDPR Compliance Module
Handles data privacy, user consent, data export, and data deletion
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd


DB_FILE = "career_suite.db"
CONSENT_FILE = "user_consent.json"


class PrivacyManager:
    """Manages data privacy and GDPR compliance features"""
    
    def __init__(self):
        """Initialize Privacy Manager"""
        self.db_file = DB_FILE
        self.consent_file = CONSENT_FILE
        self._initialize_consent_tracking()
    
    def _initialize_consent_tracking(self):
        """Initialize consent tracking table"""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS user_consent (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        consent_type TEXT NOT NULL,
                        consent_given BOOLEAN DEFAULT 0,
                        consent_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        ip_address TEXT,
                        user_agent TEXT
                    )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS data_access_log (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        access_type TEXT NOT NULL,
                        table_name TEXT,
                        record_count INTEGER,
                        access_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        purpose TEXT
                    )''')
        
        conn.commit()
        conn.close()
    
    # ============ CONSENT MANAGEMENT ============
    
    def record_consent(self, consent_type: str, consent_given: bool = True) -> bool:
        """
        Record user consent for data processing
        
        Args:
            consent_type: Type of consent (e.g., 'data_collection', 'analytics', 'ai_processing')
            consent_given: Whether consent was given (True) or withdrawn (False)
        
        Returns:
            Success status
        """
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            
            c.execute('''INSERT INTO user_consent (consent_type, consent_given)
                         VALUES (?, ?)''', (consent_type, consent_given))
            
            conn.commit()
            conn.close()
            
            # Also save to JSON file for easy access
            self._save_consent_to_file(consent_type, consent_given)
            
            return True
        except Exception as e:
            print(f"Error recording consent: {e}")
            return False
    
    def _save_consent_to_file(self, consent_type: str, consent_given: bool):
        """Save consent to JSON file"""
        consent_data = {}
        
        if os.path.exists(self.consent_file):
            with open(self.consent_file, 'r') as f:
                consent_data = json.load(f)
        
        consent_data[consent_type] = {
            'given': consent_given,
            'date': datetime.now().isoformat()
        }
        
        with open(self.consent_file, 'w') as f:
            json.dump(consent_data, f, indent=2)
    
    def check_consent(self, consent_type: str) -> bool:
        """
        Check if user has given consent for a specific type
        
        Args:
            consent_type: Type of consent to check
        
        Returns:
            True if consent given, False otherwise
        """
        if os.path.exists(self.consent_file):
            with open(self.consent_file, 'r') as f:
                consent_data = json.load(f)
                return consent_data.get(consent_type, {}).get('given', False)
        return False
    
    def get_all_consents(self) -> Dict:
        """Get all consent records"""
        if os.path.exists(self.consent_file):
            with open(self.consent_file, 'r') as f:
                return json.load(f)
        return {}
    
    # ============ DATA ACCESS (Right to Access) ============
    
    def export_all_user_data(self, format: str = 'json') -> Optional[str]:
        """
        Export all user data (GDPR Right to Access)
        
        Args:
            format: Export format ('json', 'csv', or 'excel')
        
        Returns:
            Path to exported file or None if failed
        """
        try:
            conn = sqlite3.connect(self.db_file)
            
            # Log data access
            self._log_data_access('export', 'all_tables', purpose='GDPR Right to Access')
            
            export_data = {}
            
            # Export quiz results
            df_quiz = pd.read_sql_query("SELECT * FROM quiz_results", conn)
            export_data['quiz_results'] = df_quiz.to_dict('records') if not df_quiz.empty else []
            
            # Export prep history
            try:
                df_prep = pd.read_sql_query("SELECT * FROM prep_history", conn)
                export_data['prep_history'] = df_prep.to_dict('records') if not df_prep.empty else []
            except:
                export_data['prep_history'] = []
            
            # Export candidate data (if exists)
            try:
                df_candidates = pd.read_sql_query("SELECT * FROM candidates", conn)
                export_data['candidates'] = df_candidates.to_dict('records') if not df_candidates.empty else []
            except:
                export_data['candidates'] = []
            
            # Export consent records
            export_data['consents'] = self.get_all_consents()
            
            conn.close()
            
            # Save to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if format == 'json':
                filename = f"user_data_export_{timestamp}.json"
                with open(filename, 'w') as f:
                    json.dump(export_data, f, indent=2, default=str)
                return filename
            
            elif format == 'excel':
                filename = f"user_data_export_{timestamp}.xlsx"
                with pd.ExcelWriter(filename) as writer:
                    if export_data['quiz_results']:
                        pd.DataFrame(export_data['quiz_results']).to_excel(writer, sheet_name='Quiz Results', index=False)
                    if export_data['prep_history']:
                        pd.DataFrame(export_data['prep_history']).to_excel(writer, sheet_name='Prep History', index=False)
                    if export_data['candidates']:
                        pd.DataFrame(export_data['candidates']).to_excel(writer, sheet_name='Candidates', index=False)
                return filename
            
            return None
            
        except Exception as e:
            print(f"Error exporting data: {e}")
            return None
    
    # ============ DATA DELETION (Right to Erasure) ============
    
    def delete_all_user_data(self, confirm: bool = False) -> bool:
        """
        Delete all user data (GDPR Right to Erasure / Right to be Forgotten)
        
        Args:
            confirm: Must be True to actually delete data (safety measure)
        
        Returns:
            Success status
        """
        if not confirm:
            print("⚠️ Deletion not confirmed. Set confirm=True to delete all data.")
            return False
        
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            
            # Log data deletion
            self._log_data_access('delete', 'all_tables', purpose='GDPR Right to Erasure')
            
            # Delete from all tables
            c.execute("DELETE FROM quiz_results")
            c.execute("DELETE FROM prep_history")
            c.execute("DELETE FROM candidates")
            
            conn.commit()
            conn.close()
            
            # Delete consent file
            if os.path.exists(self.consent_file):
                os.remove(self.consent_file)
            
            print("✅ All user data has been permanently deleted.")
            return True
            
        except Exception as e:
            print(f"Error deleting data: {e}")
            return False
    
    def delete_quiz_data(self, confirm: bool = False) -> bool:
        """Delete only quiz-related data"""
        if not confirm:
            return False
        
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            
            self._log_data_access('delete', 'quiz_results', purpose='User request')
            
            c.execute("DELETE FROM quiz_results")
            c.execute("DELETE FROM prep_history")
            
            conn.commit()
            conn.close()
            
            print("✅ Quiz data has been deleted.")
            return True
            
        except Exception as e:
            print(f"Error deleting quiz data: {e}")
            return False
    
    def delete_candidate_data(self, confirm: bool = False) -> bool:
        """Delete only candidate/recruiter data"""
        if not confirm:
            return False
        
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            
            self._log_data_access('delete', 'candidates', purpose='User request')
            
            c.execute("DELETE FROM candidates")
            
            conn.commit()
            conn.close()
            
            print("✅ Candidate data has been deleted.")
            return True
            
        except Exception as e:
            print(f"Error deleting candidate data: {e}")
            return False
    
    # ============ DATA ANONYMIZATION ============
    
    def anonymize_old_data(self, days_old: int = 90) -> bool:
        """
        Anonymize data older than specified days
        
        Args:
            days_old: Number of days after which to anonymize data
        
        Returns:
            Success status
        """
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            
            # Anonymize old quiz data (remove detailed quiz_data JSON)
            c.execute(f'''UPDATE quiz_results 
                         SET quiz_data = '{{\"anonymized\": true}}'
                         WHERE datetime(timestamp) < datetime('now', '-{days_old} days')''')
            
            # Anonymize old candidate data
            c.execute(f'''UPDATE candidates 
                         SET full_name = 'ANONYMIZED',
                             email = 'anonymized@example.com',
                             interview_data = '{{\"anonymized\": true}}'
                         WHERE datetime(timestamp) < datetime('now', '-{days_old} days')''')
            
            rows_affected = c.rowcount
            conn.commit()
            conn.close()
            
            self._log_data_access('anonymize', 'multiple', record_count=rows_affected, 
                                 purpose=f'Auto-anonymization after {days_old} days')
            
            print(f"✅ Anonymized {rows_affected} old records.")
            return True
            
        except Exception as e:
            print(f"Error anonymizing data: {e}")
            return False
    
    # ============ AUDIT LOGGING ============
    
    def _log_data_access(self, access_type: str, table_name: str, 
                        record_count: int = 0, purpose: str = ''):
        """Log data access for audit trail"""
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            
            c.execute('''INSERT INTO data_access_log 
                         (access_type, table_name, record_count, purpose)
                         VALUES (?, ?, ?, ?)''',
                     (access_type, table_name, record_count, purpose))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error logging data access: {e}")
    
    def get_access_log(self, limit: int = 50) -> pd.DataFrame:
        """Get data access audit log"""
        try:
            conn = sqlite3.connect(self.db_file)
            df = pd.read_sql_query(
                f"SELECT * FROM data_access_log ORDER BY access_date DESC LIMIT {limit}",
                conn
            )
            conn.close()
            return df
        except:
            return pd.DataFrame()
    
    # ============ DATA MINIMIZATION ============
    
    def get_data_summary(self) -> Dict:
        """Get summary of stored data (for transparency)"""
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            
            summary = {}
            
            # Count quiz results
            c.execute("SELECT COUNT(*) FROM quiz_results")
            summary['quiz_results_count'] = c.fetchone()[0]
            
            # Count prep history
            try:
                c.execute("SELECT COUNT(*) FROM prep_history")
                summary['prep_history_count'] = c.fetchone()[0]
            except:
                summary['prep_history_count'] = 0
            
            # Count candidates
            try:
                c.execute("SELECT COUNT(*) FROM candidates")
                summary['candidates_count'] = c.fetchone()[0]
            except:
                summary['candidates_count'] = 0
            
            # Database size
            summary['database_size_mb'] = os.path.getsize(self.db_file) / (1024 * 1024) if os.path.exists(self.db_file) else 0
            
            conn.close()
            
            return summary
            
        except Exception as e:
            print(f"Error getting data summary: {e}")
            return {}


# Convenience functions
def show_privacy_notice():
    """Display privacy notice to user"""
    notice = """
    ╔════════════════════════════════════════════════════════════════╗
    ║                    PRIVACY NOTICE                              ║
    ╚════════════════════════════════════════════════════════════════╝
    
    This application collects and stores:
    • Quiz performance data (scores, timestamps)
    • Selected languages and difficulty levels
    • Interview responses (for recruiter mode)
    
    Your data is:
    ✓ Stored locally on your machine
    ✓ Never shared with third parties (except AI processing)
    ✓ Fully under your control
    
    Your Rights:
    • Access your data (export feature)
    • Delete your data (erasure feature)
    • Withdraw consent at any time
    
    For full details, see PRIVACY_POLICY.md
    
    By using this application, you consent to data collection as described.
    """
    print(notice)


def request_consent() -> bool:
    """Request user consent for data collection"""
    show_privacy_notice()
    
    response = input("\nDo you consent to data collection? (yes/no): ").strip().lower()
    
    if response in ['yes', 'y']:
        pm = PrivacyManager()
        pm.record_consent('data_collection', True)
        pm.record_consent('analytics', True)
        pm.record_consent('ai_processing', True)
        print("\n✅ Consent recorded. Thank you!")
        return True
    else:
        print("\n⚠️ You must consent to use this application.")
        return False
