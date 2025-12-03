# admin_dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import random
from datetime import datetime, timedelta
import sqlite3
import logging
import altair as alt
from io import StringIO  # Added for CSV export functionality

# Set up logging for better debugging and monitoring
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Page configuration for consistent UI
st.set_page_config(
    page_title="TechPro Manager - Enterprise Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Color Scheme - Enhanced and centralized
COLORS = {
    'primary': '#2563eb',
    'secondary': '#7c3aed', 
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'dark': '#1f2937',
    'light': '#f8fafc',
    'accent': '#06b6d4',
    'info': '#3b82f6',
    'gradient_start': '#667eea',
    'gradient_end': '#764ba2',
    'dark_gradient_start': '#1e3a8a',
    'dark_gradient_end': '#7e22ce'
}

# Enhanced Custom CSS with modern design - Kept as is but added comments for sections
st.markdown(f"""
<style>
    /* Font Import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {{
        font-family: 'Inter', sans-serif;
    }}
    
    /* Main Header Styles */
    .main-header {{
        background: linear-gradient(135deg, {COLORS['dark_gradient_start']} 0%, {COLORS['dark_gradient_end']} 100%);
        padding: 3rem;
        border-radius: 24px;
        margin-bottom: 2.5rem;
        color: white;
        animation: slideInDown 0.8s ease-out;
        box-shadow: 0 20px 60px rgba(37, 99, 235, 0.3);
        position: relative;
        overflow: hidden;
    }}
    
    .main-header::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 100" fill="%23ffffff" opacity="0.1"><polygon points="0,0 1000,50 1000,100 0,100"/></svg>');
        background-size: cover;
    }}
    
    /* Metric Card Styles */
    .metric-card {{
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 40px rgba(0,0,0,0.12);
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }}
    
    .metric-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, {COLORS['primary']}, {COLORS['secondary']});
    }}
    
    .metric-card::after {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        transition: all 0.6s ease;
    }}
    
    .metric-card:hover {{
        transform: translateY(-12px) scale(1.02);
        box-shadow: 0 20px 60px rgba(0,0,0,0.2);
    }}
    
    .metric-card:hover::after {{
        transform: rotate(45deg) translate(50%, 50%);
    }}
    
    /* Status Styles */
    .status-pending {{ 
        border-left: 5px solid {COLORS['warning']};
        background: linear-gradient(135deg, #fff7ed 0%, #ffffff 100%);
    }}
    .status-progress {{ 
        border-left: 5px solid {COLORS['accent']};
        background: linear-gradient(135deg, #ecfeff 0%, #ffffff 100%);
    }}
    .status-completed {{ 
        border-left: 5px solid {COLORS['success']};
        background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 100%);
    }}
    .status-cancelled {{ 
        border-left: 5px solid {COLORS['danger']};
        background: linear-gradient(135deg, #fef2f2 0%, #ffffff 100%);
    }}
    
    /* Animations */
    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(60px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    @keyframes slideInDown {{
        from {{
            opacity: 0;
            transform: translateY(-80px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    .pulse {{
        animation: pulse 3s ease-in-out infinite;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ 
            transform: scale(1); 
            opacity: 1; 
        }}
        50% {{ 
            transform: scale(1.08); 
            opacity: 0.9; 
        }}
    }}
    
    .floating-icon {{
        animation: float 6s ease-in-out infinite;
    }}
    
    @keyframes float {{
        0%, 100% {{ 
            transform: translateY(0px) rotate(0deg); 
        }}
        50% {{ 
            transform: translateY(-20px) rotate(8deg); 
        }}
    }}
    
    .rotate-icon {{
        animation: rotate 8s linear infinite;
    }}
    
    @keyframes rotate {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
    }}
    
    .bounce-icon {{
        animation: bounce 3s infinite;
    }}
    
    @keyframes bounce {{
        0%, 20%, 50%, 80%, 100% {{ 
            transform: translateY(0) scale(1); 
        }}
        40% {{ 
            transform: translateY(-15px) scale(1.1); 
        }}
        60% {{ 
            transform: translateY(-8px) scale(1.05); 
        }}
    }}
    
    /* Activity Item Styles */
    .activity-item {{
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 16px;
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        transition: all 0.4s ease;
        border-left: 5px solid {COLORS['primary']};
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        position: relative;
        overflow: hidden;
    }}
    
    .activity-item::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(37, 99, 235, 0.05), transparent);
        transition: left 0.6s ease;
    }}
    
    .activity-item:hover::before {{
        left: 100%;
    }}
    
    .activity-item:hover {{
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
        transform: translateX(12px) scale(1.03);
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    }}
    
    /* Sidebar Styles */
    .sidebar-header {{
        background: linear-gradient(135deg, {COLORS['dark']} 0%, #374151 100%);
        padding: 2.5rem 1rem;
        border-radius: 0 0 24px 24px;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
        color: white;
        position: relative;
        overflow: hidden;
    }}
    
    .sidebar-header::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at top right, {COLORS['primary']}20, transparent 50%);
    }}
    
    /* Nav Item Styles */
    .nav-item {{
        padding: 1rem 1.2rem;
        margin: 0.4rem 0;
        border-radius: 12px;
        transition: all 0.4s ease;
        cursor: pointer;
        border: none;
        background: none;
        width: 100%;
        text-align: left;
        font-weight: 500;
        position: relative;
        overflow: hidden;
    }}
    
    .nav-item::before {{
        content: '';
        position: absolute;
        left: -100%;
        top: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, {COLORS['primary']}15, transparent);
        transition: left 0.6s ease;
    }}
    
    .nav-item:hover::before {{
        left: 100%;
    }}
    
    .nav-item:hover {{
        background: {COLORS['primary']}10;
        transform: translateX(8px);
        box-shadow: 0 4px 15px {COLORS['primary']}20;
    }}
    
    .nav-item.active {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        color: white;
        box-shadow: 0 6px 20px {COLORS['primary']}40;
        transform: translateX(5px);
    }}
    
    /* Stats Badge Styles */
    .stats-badge {{
        background: linear-gradient(135deg, {COLORS['primary']}, {COLORS['secondary']});
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 25px;
        font-size: 0.85rem;
        font-weight: 600;
        animation: bounce 2s infinite;
        box-shadow: 0 4px 15px {COLORS['primary']}30;
    }}
    
    /* Button Styles */
    .stButton > button {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 1.5rem;
        transition: all 0.4s ease;
        font-weight: 600;
        box-shadow: 0 4px 15px {COLORS['primary']}30;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 25px {COLORS['primary']}40;
    }}
    
    /* Data Table Styles */
    .data-table {{
        background: white;
        border-radius: 20px;
        box-shadow: 0 8px 40px rgba(0,0,0,0.12);
        padding: 1.5rem;
        border: 1px solid rgba(0,0,0,0.05);
    }}
    
    /* Progress Bar Styles */
    .progress-bar {{
        background: linear-gradient(90deg, {COLORS['success']}, {COLORS['accent']});
        height: 8px;
        border-radius: 10px;
        margin-top: 0.5rem;
    }}
    
    /* Feature Card Styles */
    .feature-card {{
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 40px rgba(0,0,0,0.1);
        transition: all 0.4s ease;
        text-align: center;
        border: 1px solid rgba(0,0,0,0.05);
    }}
    
    .feature-card:hover {{
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
    }}
    
    /* Notification Dot Styles */
    .notification-dot {{
        position: absolute;
        top: 8px;
        right: 8px;
        width: 12px;
        height: 12px;
        background: {COLORS['danger']};
        border-radius: 50%;
        animation: pulse 2s infinite;
    }}
</style>
""", unsafe_allow_html=True)

# Initialize session state with enhanced defaults
if 'refresh_key' not in st.session_state:
    st.session_state.refresh_key = 0
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'notifications' not in st.session_state:
    st.session_state.notifications = [
        {"type": "info", "message": "System update available", "time": "5 min ago"},
        {"type": "warning", "message": "3 pending approvals", "time": "10 min ago"},
        {"type": "success", "message": "Monthly target achieved", "time": "1 hour ago"}
    ]

# Enhanced Professional Database Manager with improved error handling and docstrings
class ProfessionalDBManager:
    """
    Manages the SQLite database for the TechPro Enterprise Dashboard.
    Handles connections, table creation, data seeding, and CRUD operations with enhanced error handling.
    """
    def __init__(self, db_path="techpro_enterprise.db"):
        self.db_path = db_path
        self.conn = None
        self._connect()
        self._create_tables()
        self.seed_data_if_empty()
    
    def _connect(self):
        """Establishes connection to the SQLite database with thread safety disabled for Streamlit."""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.execute("PRAGMA foreign_keys = ON")
            logger.info("Enterprise database connection established.")
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            st.error("🚨 Failed to connect to database. Please try again later.")
    
    def _create_tables(self):
        """Creates necessary database tables if they do not exist."""
        if self.conn:
            try:
                cursor = self.conn.cursor()
                
                # Enhanced Technicians table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS technicians (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        phone TEXT,
                        specialty TEXT,
                        location TEXT,
                        skills TEXT,
                        rating REAL DEFAULT 0.0,
                        completed_jobs INTEGER DEFAULT 0,
                        hourly_rate INTEGER,
                        status TEXT DEFAULT 'Pending',
                        join_date TEXT,
                        experience TEXT,
                        certifications TEXT,
                        performance_score INTEGER DEFAULT 0,
                        last_active TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Enhanced Service Requests table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS service_requests (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        client_name TEXT NOT NULL,
                        description TEXT,
                        status TEXT DEFAULT 'Pending',
                        assigned_tech_id INTEGER,
                        created_date TEXT,
                        priority TEXT DEFAULT 'Medium',
                        estimated_hours INTEGER,
                        actual_hours INTEGER,
                        client_rating INTEGER,
                        revenue DECIMAL(10,2),
                        due_date TEXT,
                        FOREIGN KEY (assigned_tech_id) REFERENCES technicians(id)
                    )
                ''')
                
                # Enhanced Support Tickets table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS support_tickets (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        client_name TEXT NOT NULL,
                        issue TEXT,
                        status TEXT DEFAULT 'Open',
                        created_date TEXT,
                        priority TEXT DEFAULT 'Medium',
                        category TEXT,
                        resolution_time INTEGER,
                        satisfaction_score INTEGER
                    )
                ''')
                
                # Analytics table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS analytics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        metric_name TEXT,
                        metric_value REAL,
                        recorded_date TEXT,
                        category TEXT
                    )
                ''')
                
                self.conn.commit()
                logger.info("Database tables created or verified.")
            except sqlite3.Error as e:
                logger.error(f"Error creating tables: {e}")
                st.error("🚨 Failed to create database tables.")
    
    def seed_data_if_empty(self):
        """Seeds the database with initial data if tables are empty."""
        if self.conn:
            try:
                cursor = self.conn.cursor()
                
                # Enhanced technicians seeding
                cursor.execute("SELECT COUNT(*) FROM technicians")
                if cursor.fetchone()[0] == 0:
                    specialties = ['Hardware Repair', 'Software Development', 'Network Security', 'Data Recovery', 'Mobile Services', 'Cloud Infrastructure']
                    locations = ['Cairo HQ', 'Alexandria Branch', 'Giza Center', 'Luxor Office', 'Aswan Station']
                    skills = ['Python', 'Java', 'Networking', 'Security', 'Database', 'Cloud', 'AI/ML', 'DevOps']
                    certifications = ['AWS Certified', 'Cisco CCNA', 'Microsoft MVP', 'Google Cloud', 'Security+']
                    
                    data = []
                    for i in range(25):
                        join_date = (datetime.now() - timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d')
                        last_active = (datetime.now() - timedelta(hours=random.randint(0, 72))).strftime('%Y-%m-%d %H:%M')
                        skills_str = ','.join(random.sample(skills, random.randint(3, 5)))
                        certs_str = ','.join(random.sample(certifications, random.randint(1, 3)))
                        
                        data.append((
                            f'{"Mohamed Ahmed Ali Hassan Mahmoud".split()[i % 5]} {["Al","Ibn","El"][i % 3]} {"Tech Solutions Services Experts".split()[i % 3]}',
                            f'tech.{i+1}@techpro.com',
                            f'+20 1{random.randint(0,9)}{random.randint(0,9)} {random.randint(100,999)} {random.randint(1000,9999)}',
                            random.choice(specialties),
                            random.choice(locations),
                            skills_str,
                            round(random.uniform(4.2, 5.0), 1),
                            random.randint(20, 300),
                            random.randint(120, 600),
                            random.choices(['Active', 'Pending', 'Inactive'], weights=[75, 15, 10])[0],
                            join_date,
                            f'{random.randint(2, 10)} years',
                            certs_str,
                            random.randint(75, 98),
                            last_active
                        ))
                    
                    cursor.executemany('''
                        INSERT INTO technicians (name, email, phone, specialty, location, skills, rating, 
                        completed_jobs, hourly_rate, status, join_date, experience, certifications, 
                        performance_score, last_active) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', data)
                
                # Enhanced service requests seeding
                cursor.execute("SELECT COUNT(*) FROM service_requests")
                if cursor.fetchone()[0] == 0:
                    statuses = ['Pending', 'In Progress', 'Completed', 'Cancelled']
                    priorities = ['Low', 'Medium', 'High', 'Critical']
                    data = []
                    
                    for i in range(50):
                        created_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d %H:%M')
                        due_date = (datetime.now() + timedelta(days=random.randint(1, 14))).strftime('%Y-%m-%d')
                        
                        data.append((
                            f'Enterprise Client {i+1}',
                            f'Comprehensive service request #{i+1} for system maintenance and optimization',
                            random.choice(statuses),
                            random.randint(1, 25),
                            created_date,
                            random.choice(priorities),
                            random.randint(2, 8),
                            random.randint(1, 10) if random.random() > 0.3 else None,
                            random.randint(3, 5) if random.random() > 0.5 else None,
                            round(random.uniform(500, 5000), 2),
                            due_date
                        ))
                    
                    cursor.executemany('''
                        INSERT INTO service_requests (client_name, description, status, assigned_tech_id, 
                        created_date, priority, estimated_hours, actual_hours, client_rating, revenue, due_date) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', data)
                
                self.conn.commit()
                logger.info("Enhanced data seeding completed successfully.")
            except sqlite3.Error as e:
                logger.error(f"Error seeding data: {e}")
                st.error("🚨 Failed to seed initial data.")
    
    def get_dashboard_stats(self):
        """Retrieves dashboard statistics with error handling."""
        try:
            current_time = datetime.now()
            base_users = 1560 + int(current_time.minute / 2)
            base_requests = 678 + int(current_time.minute / 3)
            
            cursor = self.conn.cursor()
            
            # Calculate additional metrics
            cursor.execute("SELECT SUM(revenue) FROM service_requests WHERE status = 'Completed'")
            total_revenue = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT AVG(client_rating) FROM service_requests WHERE client_rating IS NOT NULL")
            avg_rating = cursor.fetchone()[0] or 4.5
            
            return {
                'total_users': base_users,
                'total_technicians': self._get_count('technicians'),
                'active_technicians': self._get_count('technicians', "status = 'Active'"),
                'total_requests': self._get_count('service_requests'),
                'pending_requests': self._get_count('service_requests', "status = 'Pending'"),
                'in_progress_requests': self._get_count('service_requests', "status = 'In Progress'"),
                'completed_requests': self._get_count('service_requests', "status = 'Completed'"),
                'open_tickets': self._get_count('support_tickets', "status = 'Open'"),
                'total_revenue': total_revenue,
                'satisfaction_rate': round(avg_rating * 20, 1),  # Convert 5-star to percentage
                'avg_response_time': '8 min',
                'on_time_delivery': '94%'
            }
        except sqlite3.Error as e:
            logger.error(f"Error getting dashboard stats: {e}")
            return {
                'total_users': 1560,
                'total_technicians': 0,
                'active_technicians': 0,
                'total_requests': 0,
                'pending_requests': 0,
                'in_progress_requests': 0,
                'completed_requests': 0,
                'open_tickets': 0,
                'total_revenue': 0,
                'satisfaction_rate': 90.0,
                'avg_response_time': 'N/A',
                'on_time_delivery': 'N/A'
            }
    
    def _get_count(self, table, where=None):
        """Helper method to get row count from a table with optional where clause."""
        try:
            cursor = self.conn.cursor()
            query = f"SELECT COUNT(*) FROM {table}"
            if where:
                query += f" WHERE {where}"
            return cursor.execute(query).fetchone()[0]
        except sqlite3.Error as e:
            logger.error(f"Error counting rows in {table}: {e}")
            return 0
    
    def get_recent_activity(self):
        """Returns a list of recent activities for the dashboard."""
        # This can be expanded to query from DB in future
        activities = [
            {"user": "Ahmed Mohamed", "action": "requested premium hardware repair for MacBook Pro M2", "time": "2 mins ago", "type": "request", "icon": "💻", "priority": "high", "amount": "$450"},
            {"user": "Nour Tech Solutions", "action": "completed enterprise network security audit", "time": "15 mins ago", "type": "completion", "icon": "🛡️", "priority": "medium", "amount": "$1,200"},
            {"user": "Sarah Johnson", "action": "submitted critical support ticket #TKT-7842", "time": "25 mins ago", "type": "ticket", "icon": "🎫", "priority": "critical", "amount": "Urgent"},
            {"user": "Tech Masters Corp", "action": "joined as enterprise technician partner", "time": "1 hour ago", "type": "registration", "icon": "⭐", "priority": "low", "amount": "Premium"},
            {"user": "Mohamed Ali", "action": "rated service 5 stars - Exceptional performance!", "time": "2 hours ago", "type": "rating", "icon": "✨", "priority": "medium", "amount": "5.0⭐"}
        ]
        return activities
    
    def get_technicians_data(self):
        """Retrieves all technicians data with error handling."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM technicians ORDER BY performance_score DESC")
            columns = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()
            technicians = []
            for row in data:
                tech = dict(zip(columns, row))
                tech['skills'] = tech['skills'].split(',') if tech['skills'] else []
                tech['certifications'] = tech['certifications'].split(',') if tech['certifications'] else []
                technicians.append(tech)
            return technicians
        except sqlite3.Error as e:
            logger.error(f"Error getting technicians data: {e}")
            return []
    
    def approve_technician(self, tech_id):
        """Approves a technician by setting status to Active."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE technicians SET status = 'Active' WHERE id = ?", (tech_id,))
            if cursor.rowcount == 0:
                raise ValueError(f"Technician ID {tech_id} not found")
            self.conn.commit()
            logger.info(f"Approved technician ID: {tech_id}")
            st.session_state.notifications.append({
                "type": "success", 
                "message": f"Technician #{tech_id} approved successfully", 
                "time": "Just now"
            })
        except (sqlite3.Error, ValueError) as e:
            logger.error(f"Error approving technician {tech_id}: {e}")
            st.error(f"🚨 Failed to approve technician: {e}")
    
    def update_technician(self, tech_id, updates):
        """Updates technician details."""
        try:
            cursor = self.conn.cursor()
            set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
            values = list(updates.values()) + [tech_id]
            cursor.execute(f"UPDATE technicians SET {set_clause} WHERE id = ?", values)
            if cursor.rowcount == 0:
                raise ValueError(f"Technician ID {tech_id} not found")
            self.conn.commit()
            logger.info(f"Updated technician ID: {tech_id}")
        except (sqlite3.Error, ValueError) as e:
            logger.error(f"Error updating technician {tech_id}: {e}")
            st.error(f"🚨 Failed to update technician: {e}")
    
    def delete_technician(self, tech_id):
        """Deletes a technician from the database."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM technicians WHERE id = ?", (tech_id,))
            if cursor.rowcount == 0:
                raise ValueError(f"Technician ID {tech_id} not found")
            self.conn.commit()
            logger.info(f"Deleted technician ID: {tech_id}")
            st.session_state.notifications.append({
                "type": "warning", 
                "message": f"Technician #{tech_id} removed from system", 
                "time": "Just now"
            })
        except (sqlite3.Error, ValueError) as e:
            logger.error(f"Error deleting technician {tech_id}: {e}")
            st.error(f"🚨 Failed to delete technician: {e}")
    
    def get_service_requests(self):
        """Retrieves all service requests with joined technician data."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT sr.id, sr.client_name, sr.description, sr.status, sr.priority, t.name as tech_name, sr.revenue, sr.created_date, t.specialty as tech_specialty
                FROM service_requests sr 
                LEFT JOIN technicians t ON sr.assigned_tech_id = t.id
                ORDER BY sr.created_date DESC
            """)
            columns = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()
            return [dict(zip(columns, row)) for row in data]
        except sqlite3.Error as e:
            logger.error(f"Error getting service requests: {e}")
            return []
    
    def update_request_status(self, req_id, new_status):
        """Updates the status of a service request."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE service_requests SET status = ? WHERE id = ?", (new_status, req_id))
            if cursor.rowcount == 0:
                raise ValueError(f"Request ID {req_id} not found")
            self.conn.commit()
            logger.info(f"Updated request ID: {req_id} to status: {new_status}")
        except (sqlite3.Error, ValueError) as e:
            logger.error(f"Error updating request {req_id}: {e}")
            st.error(f"🚨 Failed to update request: {e}")
    
    def get_support_tickets(self):
        """Retrieves all support tickets."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM support_tickets ORDER BY created_date DESC")
            columns = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()
            return [dict(zip(columns, row)) for row in data]
        except sqlite3.Error as e:
            logger.error(f"Error getting support tickets: {e}")
            return []
    
    def update_ticket_status(self, ticket_id, new_status):
        """Updates the status of a support ticket."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE support_tickets SET status = ? WHERE id = ?", (new_status, ticket_id))
            if cursor.rowcount == 0:
                raise ValueError(f"Ticket ID {ticket_id} not found")
            self.conn.commit()
            logger.info(f"Updated ticket ID: {ticket_id} to status: {new_status}")
        except (sqlite3.Error, ValueError) as e:
            logger.error(f"Error updating ticket {ticket_id}: {e}")
            st.error(f"🚨 Failed to update ticket: {e}")
    
    def get_performance_data(self):
        """Returns performance data for charts."""
        # This can be expanded to query from analytics table
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        base_revenue = [45000, 52000, 48000, 65000, 72000, 68000, 75000, 82000, 78000, 85000, 92000, 98000]
        return {
            'months': months,
            'revenue': [r + random.randint(-5000, 5000) for r in base_revenue],
            'requests': [320, 380, 350, 420, 480, 450, 500, 550, 520, 580, 600, 650],
            'satisfaction': [94, 95, 93, 96, 97, 95, 98, 96, 97, 98, 96, 97],
            'new_clients': [45, 52, 48, 65, 72, 68, 75, 82, 78, 85, 92, 98]
        }
    
    def get_analytics_data(self):
        """Retrieves analytics data for reports."""
        try:
            cursor = self.conn.cursor()
            
            # Top performing technicians
            cursor.execute("""
                SELECT name, completed_jobs, rating, performance_score 
                FROM technicians 
                WHERE status = 'Active' 
                ORDER BY performance_score DESC 
                LIMIT 5
            """)
            top_techs = cursor.fetchall()
            
            # Request distribution
            cursor.execute("""
                SELECT status, COUNT(*) as count 
                FROM service_requests 
                GROUP BY status
            """)
            request_dist = cursor.fetchall()
            
            # Additional KPIs from data
            cursor.execute("SELECT AVG(rating) FROM technicians WHERE status = 'Active'")
            avg_tech_rating = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT AVG(client_rating) FROM service_requests WHERE client_rating IS NOT NULL")
            avg_client_satisfaction = cursor.fetchone()[0] or 0
            
            # Improved repeat business calculation: clients with >1 completed request
            cursor.execute("""
                SELECT client_name, COUNT(*) as count 
                FROM service_requests 
                WHERE status = 'Completed' 
                GROUP BY client_name 
                HAVING count > 1
            """)
            repeat_clients = len(cursor.fetchall())
            
            cursor.execute("SELECT AVG(actual_hours) FROM service_requests WHERE actual_hours IS NOT NULL")
            avg_resolution_time = cursor.fetchone()[0] or 0
            
            kpis = [
                {"name": "Average Technician Rating", "value": f"{avg_tech_rating:.2f}/5", "target": "4.5/5"},
                {"name": "Client Satisfaction", "value": f"{avg_client_satisfaction:.2f}/5", "target": "4.5/5"},
                {"name": "Repeat Clients", "value": f"{repeat_clients}", "target": "20"},
                {"name": "Avg Resolution Time", "value": f"{avg_resolution_time:.1f} hours", "target": "8 hours"}
            ]
            
            return {
                'tech_performance': pd.DataFrame(top_techs, columns=['Technician', 'Completed Jobs', 'Rating', 'Performance Score']) if top_techs else pd.DataFrame(),
                'request_distribution': pd.DataFrame(request_dist, columns=['Status', 'Count']) if request_dist else pd.DataFrame(),
                'kpis': kpis
            }
        except sqlite3.Error as e:
            logger.error(f"Error getting analytics data: {e}")
            return {
                'tech_performance': pd.DataFrame(),
                'request_distribution': pd.DataFrame(),
                'kpis': []
            }
    
    def close(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed.")

# Use Streamlit cache for DB manager to optimize performance
@st.cache_resource
def get_db_manager():
    return ProfessionalDBManager()

db = get_db_manager()

def refresh_data():
    """Refreshes the application data and reruns the script."""
    st.session_state.refresh_key += 1
    st.session_state.last_refresh = datetime.now()
    st.rerun()

def create_performance_chart(performance_data):
    """Creates an Altair chart for performance data."""
    df = pd.DataFrame({
        'Month': performance_data['months'],
        'Revenue': performance_data['revenue'],
        'Requests': performance_data['requests']
    })
    
    revenue_chart = alt.Chart(df).mark_line(color=COLORS['primary'], point=True, strokeWidth=3).encode(
        x='Month',
        y='Revenue',
        tooltip=['Month', 'Revenue']
    )
    
    requests_chart = alt.Chart(df).mark_bar(opacity=0.4, color=COLORS['accent']).encode(
        x='Month',
        y='Requests',
        tooltip=['Month', 'Requests']
    )
    
    chart = alt.layer(revenue_chart, requests_chart).resolve_scale(
        y='independent'
    ).properties(
        title='Monthly Revenue and Requests',
        width='container',
        height=300
    )
    return chart

def create_metric_card(title, value, change, icon, color=COLORS['primary']):
    """Creates HTML for a metric card."""
    return f"""
    <div class='metric-card' style='border-left-color: {color};'>
        <div style='display: flex; justify-content: space-between; align-items: start;'>
            <div class='bounce-icon' style='font-size: 2.8rem;'>{icon}</div>
            <div class='stats-badge' style='background: {color};'>{change}</div>
        </div>
        <h3 style='margin: 1.2rem 0 0.8rem; color: {COLORS["dark"]}; font-size: 1.1rem;'>{title}</h3>
        <h1 style='margin: 0; font-size: 3rem; color: {color}; font-weight: 700;'>{value}</h1>
        <div style='margin-top: 1rem;'>
            <div class='progress-bar' style='width: 85%;'></div>
        </div>
    </div>
    """

# Enhanced Professional Sidebar
with st.sidebar:
    st.markdown("""
    <div class='sidebar-header'>
        <div class='floating-icon' style='font-size: 4rem;'>⚡</div>
        <h1 style='margin: 0; font-size: 2rem; font-weight: 700;'>TechPro Enterprise</h1>
        <p style='margin: 0; opacity: 0.9; font-size: 1rem;'>Advanced Management Platform</p>
        <div style='margin-top: 1rem;'>
            <span class='stats-badge'>v4.2.1</span>
            <span class='stats-badge' style='background: {success}; margin-left: 0.5rem;'>Live</span>
        </div>
    </div>
    """.format(success=COLORS['success']), unsafe_allow_html=True)
    
    # Enhanced Navigation with icons
    menu_options = {
        "Dashboard": "📊",
        "Team Management": "👥", 
        "Service Requests": "🔧",
        "Support Tickets": "🎫",
        "Analytics": "📈",
        "Revenue": "💰",
        "Settings": "⚙️"
    }
    
    selected = st.radio(
        "Navigation",
        options=list(menu_options.keys()),
        index=list(menu_options.keys()).index(st.session_state.current_page),
        format_func=lambda x: f"{menu_options[x]} {x}"
    )
    st.session_state.current_page = selected
    
    st.markdown("---")
    
    # Enhanced Quick Stats
    st.markdown("### 🚀 Quick Insights")
    stats = db.get_dashboard_stats()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Active Tech", stats['active_technicians'], "+3")
        st.metric("Revenue", f"${stats['total_revenue']/1000:.1f}K", "+8.2%")
    with col2:
        st.metric("Live Jobs", stats['in_progress_requests'], "-2")
        st.metric("Satisfaction", f"{stats['satisfaction_rate']}%", "+1.5%")
    
    st.markdown("---")
    
    # Notifications Section
    st.markdown("### 🔔 Notifications")
    if st.session_state.notifications:
        for notif in st.session_state.notifications[-3:]:  # Show last 3
            emoji = {"info": "ℹ️", "warning": "⚠️", "success": "✅"}.get(notif["type"], "📢")
            st.info(f"{emoji} {notif['message']}")
    
    if st.button("Clear All Notifications"):
        st.session_state.notifications = []
        st.rerun()
    
    st.markdown("---")
    
    # Enhanced User Info
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem; background: linear-gradient(135deg, {light} 0%, #ffffff 100%); 
                border-radius: 16px; margin: 1rem 0; box-shadow: 0 4px 20px rgba(0,0,0,0.08);'>
        <div style='width: 70px; height: 70px; background: linear-gradient(135deg, {primary}, {secondary}); 
                    border-radius: 50%; margin: 0 auto 1rem; display: flex; align-items: center; 
                    justify-content: center; color: white; font-size: 1.8rem; font-weight: bold; 
                    box-shadow: 0 4px 15px {primary}40;'>AM</div>
        <h4 style='margin: 0; color: {dark};'>Admin Manager</h4>
        <p style='margin: 0; color: #6b7280; font-size: 0.9rem;'>Enterprise Administrator</p>
        <p style='margin: 0; color: #9ca3af; font-size: 0.8rem;'>Last sync: {}</p>
    </div>
    """.format(
        st.session_state.last_refresh.strftime('%H:%M:%S'),
        light=COLORS['light'],
        primary=COLORS['primary'],
        secondary=COLORS['secondary'],
        dark=COLORS['dark']
    ), unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh", use_container_width=True):
            refresh_data()
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            st.info("👋 Session ended successfully")
            time.sleep(1)
            st.stop()

# Enhanced Main Header
st.markdown(f"""
<div class='main-header'>
    <div style='display: flex; justify-content: space-between; align-items: center; position: relative; z-index: 2;'>
        <div>
            <h1 style='margin: 0; font-size: 3rem; font-weight: 800;'>
                {st.session_state.current_page}
            </h1>
            <p style='margin: 0; font-size: 1.3rem; opacity: 0.9; font-weight: 400;'>
                Real-time enterprise monitoring & advanced analytics
            </p>
        </div>
        <div style='display: flex; gap: 1rem; align-items: center;'>
            <div class='floating-icon' style='font-size: 4rem;'>⚡</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Dashboard Content with enhanced features
if st.session_state.current_page == "Dashboard":
    stats = db.get_dashboard_stats()
    
    # Enhanced Top Metrics with improved cards
    cols = st.columns(4)
    
    with cols[0]:
        st.markdown(create_metric_card(
            "Total Enterprise Users", 
            f"{stats['total_users']:,}", 
            "+12.5%", 
            "👥", 
            COLORS['primary']
        ), unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown(create_metric_card(
            "Active Service Jobs", 
            f"{stats['in_progress_requests']}", 
            "Live", 
            "🔧", 
            COLORS['accent']
        ), unsafe_allow_html=True)
    
    with cols[2]:
        st.markdown(create_metric_card(
            "Completed Projects", 
            f"{stats['completed_requests']}", 
            "98%", 
            "✅", 
            COLORS['success']
        ), unsafe_allow_html=True)
    
    with cols[3]:
        st.markdown(create_metric_card(
            "Quarterly Revenue", 
            f"${stats['total_revenue']/1000:.1f}K", 
            "↑8.2%", 
            "💰", 
            COLORS['secondary']
        ), unsafe_allow_html=True)
    
    # Enhanced Charts and Analytics Section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 Advanced Performance Analytics")
        performance_data = db.get_performance_data()
        chart = create_performance_chart(performance_data)
        st.altair_chart(chart, use_container_width=True)
        
        # Additional mini metrics
        col1a, col2a, col3a = st.columns(3)
        with col1a:
            st.metric("Avg Response", stats['avg_response_time'], "-2 min")
        with col2a:
            st.metric("On Time Delivery", stats['on_time_delivery'], "+4%")
        with col3a:
            st.metric("Client Satisfaction", f"{stats['satisfaction_rate']}%", "+2.1%")
    
    with col2:
        st.subheader("🎯 Performance Insights")
        
        insights = [
            {"title": "Productivity Score", "value": "94%", "trend": "+5%", "icon": "📊"},
            {"title": "Team Efficiency", "value": "88%", "trend": "+3%", "icon": "⚡"},
            {"title": "Quality Rating", "value": "4.8/5", "trend": "+0.2", "icon": "⭐"},
            {"title": "Client Retention", "value": "96%", "trend": "+2%", "icon": "💎"}
        ]
        
        for insight in insights:
            st.markdown(f"""
            <div class='feature-card' style='margin-bottom: 1rem; padding: 1.5rem;'>
                <div style='display: flex; align-items: center; justify-content: space-between;'>
                    <div>
                        <div style='font-size: 1.5rem;'>{insight['icon']}</div>
                        <h4 style='margin: 0.5rem 0; color: {COLORS["dark"]};'>{insight['title']}</h4>
                    </div>
                    <div style='text-align: right;'>
                        <h3 style='margin: 0; color: {COLORS["primary"]};'>{insight['value']}</h3>
                        <small style='color: {COLORS["success"]}; font-weight: 600;'>{insight['trend']}</small>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Enhanced Recent Activity with filtering
    st.subheader("🔄 Live Activity Stream")
    
    # Activity filters
    col1b, col2b = st.columns([3, 1])
    with col2b:
        activity_filter = st.selectbox("Filter Activities", ["All", "Requests", "Completions", "Tickets", "Ratings"])
    
    activities = db.get_recent_activity()
    
    # Filter activities if needed
    if activity_filter != "All":
        activities = [a for a in activities if a['type'] == activity_filter.lower()]
    
    # Display activities in an enhanced layout
    with st.container():
        for activity in activities:
            priority_color = {
                'high': COLORS['warning'],
                'critical': COLORS['danger'],
                'medium': COLORS['accent'], 
                'low': COLORS['success']
            }.get(activity['priority'], COLORS['primary'])
            
            st.markdown(f"""
            <div class='activity-item'>
                <div style='display: flex; align-items: center; gap: 20px;'>
                    <span style='font-size: 2.2em;' class='bounce-icon'>{activity['icon']}</span>
                    <div style='flex-grow: 1;'>
                        <strong style='color: {COLORS['dark']}; font-size: 1.1em;'>{activity['user']}</strong> 
                        <span style='color: {COLORS['dark']}; opacity: 0.9;'>{activity['action']}</span><br>
                        <small style='color: {COLORS['primary']}; font-weight: 600; font-size: 0.9em;'>{activity['time']}</small>
                    </div>
                    <div style='display: flex; flex-direction: column; align-items: end; gap: 8px;'>
                        <div style='background: {priority_color}; color: white; padding: 8px 16px; 
                                    border-radius: 20px; font-size: 0.85em; font-weight: 700; text-transform: uppercase;'>
                            {activity['type']}
                        </div>
                        <div style='color: {COLORS['secondary']}; font-weight: 700; font-size: 0.9em;'>
                            {activity['amount']}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

elif st.session_state.current_page == "Team Management":
    st.title("👥 Advanced Team Management")
    
    # Advanced Search and Filters
    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
    with col1:
        search_query = st.text_input("🔍 Search technicians...", placeholder="Name, email, skills, certifications...")
    with col2:
        status_filter = st.selectbox("Status", ["All", "Active", "Pending", "Inactive"])
    with col3:
        location_filter = st.selectbox("Location", ["All"] + sorted(set(t['location'] for t in db.get_technicians_data() if t['location'])))
    with col4:
        specialty_filter = st.selectbox("Specialty", ["All"] + sorted(set(t['specialty'] for t in db.get_technicians_data() if t['specialty'])))
    with col5:
        min_rating = st.slider("Min Rating", 0.0, 5.0, 0.0, 0.1)
    
    technicians_data = db.get_technicians_data()
    df = pd.DataFrame(technicians_data)
    
    # Apply enhanced filters
    if status_filter != "All":
        df = df[df['status'] == status_filter]
    if location_filter != "All":
        df = df[df['location'] == location_filter]
    if specialty_filter != "All":
        df = df[df['specialty'] == specialty_filter]
    if min_rating > 0:
        df = df[df['rating'] >= min_rating]
    if search_query:
        df = df[
            df['name'].str.contains(search_query, case=False) | 
            df['email'].str.contains(search_query, case=False) |
            df['certifications'].str.contains(search_query, case=False) |
            df.apply(lambda row: any(search_query.lower() in s.lower() for s in row['skills']), axis=1)
        ]
    
    st.subheader(f"👨‍💼 Technical Team Overview ({len(df)} Professionals)")
    
    # Enhanced data display with tabs
    tab1, tab2, tab3 = st.tabs(["📋 Data View", "📊 Performance", "🎯 Quick Actions"])
    
    with tab1:
        # Interactive data table
        if not df.empty:
            st.dataframe(
                df[['id', 'name', 'email', 'specialty', 'location', 'rating', 'performance_score', 'status']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No technicians found matching the criteria.")
        
        # Added export functionality for professionalism
        csv = StringIO()
        df.to_csv(csv, index=False)
        st.download_button(
            label="📥 Download Team Data as CSV",
            data=csv.getvalue(),
            file_name="team_data.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with tab2:
        # Performance metrics
        if not df.empty:
            col1, col2, col3 = st.columns(3)
            with col1:
                avg_rating = df['rating'].mean()
                st.metric("Average Rating", f"{avg_rating:.1f}/5.0")
            with col2:
                total_jobs = df['completed_jobs'].sum()
                st.metric("Total Jobs Completed", f"{total_jobs:,}")
            with col3:
                avg_performance = df['performance_score'].mean()
                st.metric("Avg Performance", f"{avg_performance:.0f}%")
            
            # Performance chart
            perf_df = df.nlargest(10, 'performance_score')[['name', 'performance_score']]
            chart = alt.Chart(perf_df).mark_bar().encode(
                x='performance_score:Q',
                y=alt.Y('name:N', sort='-x'),
                color=alt.Color('performance_score:Q', scale=alt.Scale(scheme='viridis')),
                tooltip=['name', 'performance_score']
            ).properties(title='Top Performing Technicians', height=300)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("No data available for performance analysis.")
    
    with tab3:
        st.info("🚀 Quick team management actions")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📧 Send Team Update", use_container_width=True):
                st.success("Team update scheduled!")
        with col2:
            if st.button("🔄 Sync Performance Data", use_container_width=True):
                st.success("Performance data synchronized!")
    
    # Enhanced technician editing interface
    st.subheader("✏️ Technician Management")
    
    if not df.empty:
        selected_id = st.selectbox(
            "Select Technician for Detailed Management", 
            options=df['id'].tolist(), 
            format_func=lambda x: f"#{x} - {df[df['id'] == x]['name'].values[0]}"
        )
        
        if selected_id:
            tech = df[df['id'] == selected_id].iloc[0]
            
            # Enhanced form with tabs
            edit_tab1, edit_tab2, edit_tab3 = st.tabs(["📝 Basic Info", "🛠️ Professional Details", "⚡ Quick Actions"])
            
            with edit_tab1:
                with st.form("edit_tech_basic_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        name = st.text_input("Full Name", tech['name'])
                        email = st.text_input("Email Address", tech['email'])
                        phone = st.text_input("Phone Number", tech['phone'])
                    with col2:
                        specialty = st.text_input("Specialty", tech['specialty'])
                        location = st.selectbox("Location", ["Cairo HQ", "Alexandria Branch", "Giza Center", "Luxor Office", "Aswan Station"], index=["Cairo HQ", "Alexandria Branch", "Giza Center", "Luxor Office", "Aswan Station"].index(tech['location']))
                        status = st.selectbox("Status", ["Active", "Pending", "Inactive"], index=["Active", "Pending", "Inactive"].index(tech['status']))
                    
                    if st.form_submit_button("💾 Save Basic Information"):
                        updates = {'name': name, 'email': email, 'phone': phone, 'specialty': specialty, 'location': location, 'status': status}
                        db.update_technician(selected_id, updates)
                        st.success("✅ Basic information updated successfully!")
                        refresh_data()
            
            with edit_tab2:
                with st.form("edit_tech_pro_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        skills = st.text_area("Skills (comma-separated)", ','.join(tech['skills']))
                        certifications = st.text_area("Certifications", ','.join(tech['certifications']))
                        experience = st.text_input("Experience", tech['experience'])
                    with col2:
                        rating = st.slider("Rating", 0.0, 5.0, float(tech['rating']), 0.1)
                        completed_jobs = st.number_input("Completed Jobs", value=int(tech['completed_jobs']))
                        hourly_rate = st.number_input("Hourly Rate ($)", value=int(tech['hourly_rate']))
                        performance_score = st.slider("Performance Score", 0, 100, int(tech['performance_score']))
                    
                    if st.form_submit_button("💼 Update Professional Details"):
                        updates = {
                            'skills': skills, 'certifications': certifications, 'experience': experience,
                            'rating': rating, 'completed_jobs': completed_jobs, 'hourly_rate': hourly_rate,
                            'performance_score': performance_score
                        }
                        db.update_technician(selected_id, updates)
                        st.success("✅ Professional details updated successfully!")
                        refresh_data()
            
            with edit_tab3:
                st.warning("Quick actions for immediate changes")
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("✅ Approve Technician", use_container_width=True) and tech['status'] == 'Pending':
                        db.approve_technician(selected_id)
                        st.success("Technician approved!")
                        refresh_data()
                with col2:
                    if st.button("🔄 Reset Password", use_container_width=True):
                        st.info("Password reset link sent to technician's email")
                with col3:
                    if st.button("🗑️ Remove Technician", use_container_width=True, type="secondary"):
                        if st.checkbox("Confirm deletion"):
                            db.delete_technician(selected_id)
                            st.success("Technician removed from system!")
                            refresh_data()

elif st.session_state.current_page == "Service Requests":
    st.title("🔧 Advanced Service Requests Management")
    
    requests_data = db.get_service_requests()
    df = pd.DataFrame(requests_data)
    
    # Enhanced filtering
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        search_query = st.text_input("Search requests...", placeholder="Client, description, technician...")
    with col2:
        status_filter = st.selectbox("Status Filter", ["All", "Pending", "In Progress", "Completed", "Cancelled"])
    with col3:
        priority_filter = st.selectbox("Priority Filter", ["All", "Low", "Medium", "High", "Critical"])
    with col4:
        date_filter = st.selectbox("Time Frame", ["All Time", "Last 7 Days", "Last 30 Days", "Last 90 Days"])
    
    # Apply enhanced filters
    if status_filter != "All":
        df = df[df['status'] == status_filter]
    if priority_filter != "All":
        df = df[df['priority'] == priority_filter]
    if search_query:
        df = df[
            df['client_name'].str.contains(search_query, case=False) |
            df['description'].str.contains(search_query, case=False) |
            df['tech_name'].str.contains(search_query, case=False)
        ]
    
    st.subheader(f"📋 Service Requests Overview ({len(df)} requests)")
    
    # Enhanced display with metrics
    if not df.empty:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_revenue = df[df['status'] == 'Completed']['revenue'].sum()
            st.metric("Total Revenue", f"${total_revenue:,.0f}")
        with col2:
            avg_rating = df['client_rating'].mean()
            st.metric("Avg Client Rating", f"{avg_rating:.1f}/5" if not pd.isna(avg_rating) else "N/A")
        with col3:
            pending_count = len(df[df['status'] == 'Pending'])
            st.metric("Pending Approval", pending_count)
        with col4:
            critical_count = len(df[df['priority'] == 'Critical'])
            st.metric("Critical Issues", critical_count, delta_color="inverse")
    
        # Enhanced data table
        display_columns = ['id', 'client_name', 'description', 'status', 'priority', 'tech_name', 'revenue', 'created_date']
        st.dataframe(
            df[display_columns],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No service requests found matching the criteria.")
    
    # Added export functionality
    csv = StringIO()
    df.to_csv(csv, index=False)
    st.download_button(
        label="📥 Download Requests Data as CSV",
        data=csv.getvalue(),
        file_name="service_requests.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    # Enhanced request management
    if not df.empty:
        st.subheader("🛠️ Request Management")
        selected_req = st.selectbox(
            "Select Request for Management", 
            options=df['id'].tolist(), 
            format_func=lambda x: f"#{x} - {df[df['id'] == x]['client_name'].values[0]} - {df[df['id'] == x]['priority'].values[0]}"
        )
        
        if selected_req:
            req = df[df['id'] == selected_req].iloc[0]
            
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write(f"**Client:** {req['client_name']}")
                st.write(f"**Description:** {req['description']}")
                st.write(f"**Assigned Technician:** {req['tech_name'] or 'Unassigned'}")
                st.write(f"**Revenue:** ${req['revenue'] or '0'}")
            
            with col2:
                new_status = st.selectbox(
                    "Update Status", 
                    ["Pending", "In Progress", "Completed", "Cancelled"], 
                    index=["Pending", "In Progress", "Completed", "Cancelled"].index(req['status'])
                )
                
                if st.button("🔄 Update Request Status", use_container_width=True):
                    db.update_request_status(selected_req, new_status)
                    st.success("✅ Request status updated successfully!")
                    refresh_data()

elif st.session_state.current_page == "Support Tickets":
    st.title("🎫 Enterprise Support Tickets Management")
    
    tickets_data = db.get_support_tickets()
    df = pd.DataFrame(tickets_data)
    
    # Basic filtering
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox("Status", ["All", "Open", "In Progress", "Resolved", "Closed"])
    with col2:
        priority_filter = st.selectbox("Priority", ["All", "Low", "Medium", "High", "Critical"])
    
    if status_filter != "All":
        df = df[df['status'] == status_filter]
    if priority_filter != "All":
        df = df[df['priority'] == priority_filter]
    
    st.subheader(f"🎫 Support Tickets ({len(df)} tickets)")
    
    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No support tickets found.")
    
    # Added export functionality
    csv = StringIO()
    df.to_csv(csv, index=False)
    st.download_button(
        label="📥 Download Tickets Data as CSV",
        data=csv.getvalue(),
        file_name="support_tickets.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    if not df.empty:
        selected_ticket = st.selectbox("Select Ticket to Manage", options=df['id'].tolist(), 
                                       format_func=lambda x: f"#{x} - {df[df['id'] == x]['client_name'].values[0]}")
        if selected_ticket:
            ticket = df[df['id'] == selected_ticket].iloc[0]
            new_status = st.selectbox("Update Status", ["Open", "In Progress", "Resolved", "Closed"], 
                                      index=["Open", "In Progress", "Resolved", "Closed"].index(ticket['status']))
            if st.button("Update Status"):
                db.update_ticket_status(selected_ticket, new_status)
                st.success("Status updated!")
                refresh_data()

elif st.session_state.current_page == "Analytics":
    st.title("📊 Advanced Business Analytics")
    
    analytics_data = db.get_analytics_data()
    performance_data = db.get_performance_data()
    
    # Comprehensive analytics dashboard
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Top Performing Technicians")
        if not analytics_data['tech_performance'].empty:
            st.dataframe(analytics_data['tech_performance'], use_container_width=True)
            
            # Interactive performance chart with enhanced styling
            tech_chart = alt.Chart(analytics_data['tech_performance']).mark_bar(size=30).encode(
                x=alt.X('Technician:N', sort='-y', axis=alt.Axis(labelAngle=-45)),
                y='Completed Jobs:Q',
                color=alt.Color('Rating:Q', scale=alt.Scale(scheme='viridis'), legend=alt.Legend(title="Rating")),
                tooltip=['Technician', 'Completed Jobs', 'Rating', 'Performance Score']
            ).properties(title='Technician Performance Overview', height=350, width='container').interactive()
            st.altair_chart(tech_chart, use_container_width=True)
            
            # Export top techs
            csv = StringIO()
            analytics_data['tech_performance'].to_csv(csv, index=False)
            st.download_button(
                label="📥 Download Top Technicians",
                data=csv.getvalue(),
                file_name="top_technicians.csv",
                mime="text/csv"
            )
        else:
            st.info("No active technicians available for performance analysis.")
    
    with col2:
        st.subheader("📈 Request Distribution Analytics")
        
        if not analytics_data['request_distribution'].empty:
            # Enhanced bar chart instead of pie for better readability
            bar_chart = alt.Chart(analytics_data['request_distribution']).mark_bar(size=40).encode(
                x=alt.X('Status:N', sort='-y'),
                y='Count:Q',
                color=alt.Color('Status:N', scale=alt.Scale(domain=['Pending', 'In Progress', 'Completed', 'Cancelled'], range=[COLORS['warning'], COLORS['accent'], COLORS['success'], COLORS['danger']])),
                tooltip=['Status', 'Count']
            ).properties(title='Service Request Status Distribution', height=350, width='container').interactive()
            st.altair_chart(bar_chart, use_container_width=True)
            
            # Export distribution
            csv = StringIO()
            analytics_data['request_distribution'].to_csv(csv, index=False)
            st.download_button(
                label="📥 Download Request Distribution",
                data=csv.getvalue(),
                file_name="request_distribution.csv",
                mime="text/csv"
            )
        else:
            st.info("No service requests available for distribution analysis.")
        
        # Dynamic KPIs
        st.subheader("📊 Key Performance Indicators")
        kpis = analytics_data['kpis']
        
        for kpi in kpis:
            with st.container():
                st.write(f"**{kpi['name']}**")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Value", kpi['value'])
                with col2:
                    st.metric("Target", kpi['target'])
    
    # Additional section for trends
    st.subheader("📉 Performance Trends")
    trend_chart = create_performance_chart(performance_data)
    st.altair_chart(trend_chart, use_container_width=True)

elif st.session_state.current_page == "Revenue":
    st.title("💰 Advanced Revenue Analytics")
    
    performance_data = db.get_performance_data()
    df = pd.DataFrame({
        'Month': performance_data['months'],
        'Revenue': performance_data['revenue'],
        'New Clients': performance_data['new_clients']
    })
    
    # Advanced revenue visualization using Altair
    base = alt.Chart(df).encode(x='Month:O')
    
    revenue_line = base.mark_line(color=COLORS['primary'], strokeWidth=3).encode(
        y=alt.Y('Revenue:Q', axis=alt.Axis(title='Revenue ($)', titleColor=COLORS['primary'])),
        tooltip=['Month', 'Revenue']
    )
    
    clients_bar = base.mark_bar(color=COLORS['accent'], opacity=0.6).encode(
        y=alt.Y('New Clients:Q', axis=alt.Axis(title='New Clients', titleColor=COLORS['accent'])),
        tooltip=['Month', 'New Clients']
    )
    
    chart = alt.layer(revenue_line, clients_bar).resolve_scale(
        y='independent'
    ).properties(
        title='Revenue Growth & Client Acquisition',
        height=400
    )
    
    st.altair_chart(chart, use_container_width=True)
    
    # Revenue breakdown
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📅 Revenue Details")
        st.dataframe(df, use_container_width=True)
        
        # Added export
        csv = StringIO()
        df.to_csv(csv, index=False)
        st.download_button(
            label="📥 Download Revenue Data",
            data=csv.getvalue(),
            file_name="revenue_data.csv",
            mime="text/csv"
        )
    
    with col2:
        st.subheader("🎯 Revenue Insights")
        insights = [
            {"period": "Current Month", "revenue": "$98,450", "growth": "+12%"},
            {"period": "Quarter-to-Date", "revenue": "$285,600", "growth": "+8%"},
            {"period": "Year-to-Date", "revenue": "$1,245,800", "growth": "+15%"},
            {"period": "Projected Annual", "revenue": "$1,580,000", "growth": "+18%"}
        ]
        
        for insight in insights:
            with st.container():
                st.write(f"**{insight['period']}**")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Revenue", insight['revenue'])
                with col2:
                    st.metric("Growth", insight['growth'])
                st.markdown("---")

elif st.session_state.current_page == "Settings":
    st.title("⚙️ Enterprise System Configuration")
    
    # Settings in tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔧 General", "🔔 Notifications", "🔒 Security", "📊 Preferences"])
    
    with tab1:
        st.subheader("General Settings")
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Enable Email Notifications", value=True)
            st.checkbox("Enable SMS Alerts", value=True)
            st.checkbox("Auto-backup Database", value=True)
        with col2:
            st.number_input("Session Timeout (minutes)", min_value=5, max_value=120, value=30)
            st.selectbox("Default Language", ["English", "Arabic", "French", "Spanish"])
            st.selectbox("Theme", ["Light", "Dark", "Auto"])
        
        if st.button("💾 Save General Settings"):
            st.success("General settings saved successfully!")
    
    with tab2:
        st.subheader("Notification Preferences")
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("New Service Requests", value=True)
            st.checkbox("Support Tickets", value=True)
            st.checkbox("System Alerts", value=True)
        with col2:
            st.checkbox("Performance Reports", value=True)
            st.checkbox("Revenue Updates", value=False)
            st.checkbox("Team Notifications", value=True)
        
        st.slider("Notification Frequency (hours)", 1, 24, 4)
        
        if st.button("💾 Save Notification Settings"):
            st.success("Notification preferences updated!")
    
    with tab3:
        st.subheader("Security Configuration")
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Two-Factor Authentication", value=True)
            st.checkbox("IP Whitelisting", value=False)
            st.checkbox("Session Logging", value=True)
        with col2:
            st.number_input("Password Expiry (days)", min_value=30, max_value=365, value=90)
            st.number_input("Max Login Attempts", min_value=3, max_value=10, value=5)
        
        if st.button("🔒 Update Security Settings"):
            st.success("Security configuration updated!")
    
    with tab4:
        st.subheader("User Preferences")
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Default Dashboard View", ["Overview", "Analytics", "Performance"])
            st.selectbox("Date Format", ["YYYY-MM-DD", "DD/MM/YYYY", "MM/DD/YYYY"])
        with col2:
            st.selectbox("Time Zone", ["UTC", "EST", "CST", "PST"])
            st.checkbox("Compact View", value=False)
        
        if st.button("💾 Save Preferences"):
            st.success("User preferences saved!")

# Enhanced Enterprise Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: {COLORS['dark']}; padding: 3rem; background: linear-gradient(135deg, {COLORS['light']} 0%, #ffffff 100%); 
            border-radius: 24px; margin-top: 3rem; box-shadow: 0 4px 20px rgba(0,0,0,0.08);'>
    <div style='font-size: 3rem; margin-bottom: 1rem;'>
        <span class='rotate-icon'>⚡</span>
    </div>
    <h3 style='margin: 0; color: {COLORS['primary']}; font-size: 1.8rem;'>TechPro Enterprise Manager v4.2</h3>
    <p style='margin: 0; opacity: 0.8; font-size: 1.1rem;'>Advanced Service Management Platform</p>
    <div style='margin-top: 1.5rem; display: flex; justify-content: center; gap: 2rem;'>
        <span style='color: {COLORS['success']}; font-weight: 600;'>🟢 System Operational</span>
        <span style='color: {COLORS['primary']};'>Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</span>
        <span style='color: {COLORS['secondary']};'>Server: Enterprise-Cluster-01</span>
    </div>
    <div style='margin-top: 1rem;'>
        <small style='opacity: 0.6;'>© 2024 TechPro Enterprises. All rights reserved.</small>
    </div>
</div>
""", unsafe_allow_html=True)

# Close DB connection
if 'db' in globals():
    db.close()