import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
import time

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Service Platform",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# Custom CSS & Animations (Dark Mode + High Contrast) - الكود المُعدّل يبدأ هنا
# -----------------------------
st.markdown("""
    <style>
    /* Global Styles (Kept as is for styling consistency) */
    @import url('https://fonts.fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: #0b0f19; /* Very Dark Blue/Black */
        color: #ffffff !important; 
        font-size: 16px; 
    }
    
    /* Main Background Gradient - REMOVED DEFAULT PADDING */
    .stApp {
        background: linear-gradient(135deg, #0b0f19 0%, #1a1f35 50%, #251e3e 100%);
        background-attachment: fixed;
    }
    
    /* Ensure the main block is full width and padding is only inside the content container */
    .main > div {
        max-width: 100%; /* Important for full width sections */
        padding: 0; 
    }
    
    /* Content Padding (Apply padding only to the content area, not the full width sections like footer) */
    .block-container {
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px; /* Keep content centered/constrained */
    }

    /* Top Navigation Bar */
    .nav-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        padding: 15px 30px;
        background: rgba(20, 25, 45, 0.98); 
        backdrop-filter: blur(15px);
        border-radius: 15px;
        box-shadow: 0 4px 25px rgba(0,0,0,0.6);
        margin-bottom: 30px;
        position: sticky;
        top: 10px;
        z-index: 1000;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-enter {
        animation: fadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    /* Hero Section Styles (Enlarged - KEPT) */
    .hero-section {
        text-align: center; 
        padding: 80px 50px !important; 
        background: rgba(30, 35, 60, 0.5); 
        border-radius: 25px !important; 
        box-shadow: 0 15px 50px rgba(0,0,0,0.7) !important; 
        border: 1px solid #6c5ce7; 
        margin-bottom: 50px;
    }

    /* 🔥🔥🔥 قاعدة شاملة لجميع نصوص العنوان الأساسية والفقرات لضمان اللون الأبيض 🔥🔥🔥 */
    h1, h2, h3, h4, h5, h6, p, span, div, li, a {
        color: #ffffff !important; 
    }

    /* الاستثناءات/القواعد الخاصة التي يجب أن يكون لونها مختلف (مثل الألوان البنفسجية) */
    .hero-section h1 {
        color: #a29bfe !important; /* لون العنوان البنفسجي في الهيرو سيكشن */
    }
    .hero-section p {
        color: #e0e0e0 !important; /* رمادي فاتح للهيرو ديسكربشن */
    }
    
    /* Service Cards (MODIFIED) */
    .service-card {
        background: #1e233c; 
        border-radius: 18px;
        padding: 28px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.15);
        height: 320px; 
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin-bottom: 20px; 
    }

    .card-icon {
        font-size: 40px; 
        margin-bottom: 10px;
    }

    .card-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff !important; 
        margin-bottom: 5px;
    }
    
    .badge-cat {
        display: inline-block;
        background: #a29bfe;
        color: #ffffff !important; 
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 10px;
        width: fit-content;
    }

    .card-desc {
        color: #ffffff !important; 
        flex-grow: 1; 
        margin-bottom: 15px;
    }

    .card-price {
        font-size: 1.3rem;
        font-weight: 700;
        color: #ffffff !important; 
        margin-top: 10px;
    }

    /* === Buttons (UNIFIED STYLING FOR ALL FORM BUTTONS: LOGIN, REGISTER, CONFIRM BOOKING, SELECT) === */
    /* هذا يستهدف زر Streamlit الافتراضي st.button */
    .stButton > button {
        background: linear-gradient(135deg, #6c5ce7 0%, #8e44ad 100%);
        color: white !important;
        border: none;
        padding: 14px 28px;
        border-radius: 14px;
        font-weight: 700;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 6px 20px rgba(108, 92, 231, 0.5); 
        font-size: 17px;
        letter-spacing: 0.5px;
    }
    
    /* Hover state for all general buttons */
    .stButton > button:hover {
        transform: scale(1.02); /* تغيير بسيط في الحجم */
        background: linear-gradient(135deg, #8e44ad 0%, #6c5ce7 100%); 
        color: white !important; 
        box-shadow: 0 0 35px rgba(108, 92, 231, 0.9); /* ظل أقوى */
    }

    /* 🔥🔥🔥 التأكد من أن زر Submit Form (Confirm Booking, Login, Register) يتبع نفس التنسيق */
    div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #6c5ce7 0%, #8e44ad 100%) !important;
        color: white !important;
        box-shadow: 0 6px 20px rgba(108, 92, 231, 0.5) !important; 
    }
    div[data-testid="stFormSubmitButton"] > button:hover {
        background: linear-gradient(135deg, #8e44ad 0%, #6c5ce7 100%) !important; 
        box-shadow: 0 10px 25px rgba(108, 92, 231, 0.6) !important;
    }

    /* Input Field Labels/Text (Crucial for contrast) */
    div[data-testid="stForm"] label, 
    div[data-testid="stTextInput"] label,
    div[data-testid="stSelectbox"] label,
    div[data-testid="stDateInput"] label,
    div[data-testid="stRadio"] label,
    div[data-testid="stTextArea"] label {
        color: #ffffff !important; /* التسميات الرئيسية بيضاء */
        font-weight: 600;
    }
    
    /* Ensures text inside the radio button options is white */
    div[data-testid="stRadio"] .stMarkdown,
    div[data-testid="stRadio"] label p {
        color: #ffffff !important;
    }
    
    /* 🔥🔥🔥 تفعيل اللون الأبيض لعناصر الإدخال والقوائم المنسدلة */
    input[type="text"], input[type="password"], textarea, 
    div.stDateInput, 
    div.stSelectbox div[data-baseweb="select"] { 
        background-color: #1a1f35 !important;
        color: #ffffff !important; /* 🔥🔥🔥 تأكيد النص المدخل أبيض */
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 8px;
    }
    
    /* ----------------------------------------------------------------------------------- */
    /* 🔥🔥🔥 FINAL FIX: FORCE EVERYTHING BLACK (Box + List) 🔥🔥🔥 */
            


    /* === PART 1: THE SELECT BOX (The main button you click) === */
    /* This targets the container of the selected value */
    div[data-baseweb="select"] > div {
        background-color: #000000 !important; /* Force Black Background */
        color: #ffffff !important;             /* Force White Text */
        border: 1px solid #6c5ce7 !important;  /* Dark Border */
    }
    
    /* Force the text inside the box (e.g., "All") to be white */
    div[data-baseweb="select"] span {
        color: #ffffff !important;
    }
    
    /* Force the arrow icon to be white */
    div[data-baseweb="select"] svg {
        fill: #ffffff !important;
        color: #ffffff !important;
    }

    /* === PART 2: THE DROPDOWN LIST (The popup menu) === */
    /* Target the popover container and the list itself */
    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    ul[data-baseweb="menu"] {
        background-color: #000000 !important; /* Force Black Background */
        border: 1px solid #333333 !important;
    }

    /* Target the individual options */
    li[data-baseweb="option"] {
        background-color: #4a2985 !important;
        color: #ffffff !important;
    }

    /* Target the text inside the options */
    li[data-baseweb="option"] div {
        color: #ffffff !important; 
    }

    /* Hover State (Dark Grey) */
    li[data-baseweb="option"]:hover {
        background-color: #6c5ce7 !important;
    }
    
    /* Selected Item (Purple) */
    li[data-baseweb="option"][aria-selected="true"] {
        background-color: #5f27cd !important;
    }
            
    div[data-baseweb="popover"] div[style*="overflow"] {
        background-color: #000000 !important;
        border: 1px solid #5f27cd !important;
    }
    /* ----------------------------------------------------------------------------------- */


    /* Styling for Home Page Auth Buttons (LOGIN/REGISTER on HOME page) */
    .home-auth-button button {
        background: linear-gradient(135deg, #8e44ad 0%, #6c5ce7 100%);
        padding: 15px 30px !important;
        border-radius: 10px;
        font-size: 1.1rem;
        box-shadow: 0 6px 20px rgba(108, 92, 231, 0.5);
    }
    .home-auth-button button:hover {
        transform: scale(1.05) translateY(-2px);
    }

    /* Style for Role Selection Buttons on Register Page (Kept as is) */
    .auth-role-button button {
        background: #1e233c !important; 
        border: 2px solid #a29bfe !important; 
        color: #ffffff !important;
        padding: 15px 30px !important;
        border-radius: 10px;
        font-size: 1.1rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        transition: all 0.3s ease;
        font-weight: 600;
        margin-bottom: 20px;
    }

    .auth-role-button button:hover {
        transform: translateY(-3px) scale(1.05);
        background: #282e4f !important; 
        border-color: #6c5ce7 !important;
        box-shadow: 0 10px 20px rgba(108, 92, 231, 0.3);
    }

    .auth-role-button-selected button {
        background: linear-gradient(135deg, #6c5ce7 0%, #8e44ad 100%) !important;
        border: 2px solid #ffffff !important; 
        transform: scale(1.02);
        box-shadow: 0 8px 20px rgba(108, 92, 231, 0.7) !important;
    }
    /* =================================================================== */
    
    /* About Us Cards Styling (Kept from last fix, confirming white text) */
    .about-card {
        background: #1e233c; 
        border-radius: 18px;
        padding: 30px;
        margin-top: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
        border: 1px solid rgba(255, 255, 255, 0.15);
        height: 100%;
        text-align: center;
        transition: all 0.3s ease;
    }
    .about-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.6);
        border-color: #6c5ce7; 
    }
    .about-icon {
        font-size: 50px;
        color: #a29bfe; 
        margin-bottom: 15px;
    }
    .about-title {
        font-size: 24px;
        font-weight: 700;
        color: #ffffff !important;
        margin-bottom: 10px;
    }
    .about-text {
        color: #ffffff !important;
        font-size: 16px;
        line-height: 1.6;
    }

    /* Footer Styling (KEPT) */
    .footer-container {
        width: 100vw; 
        position: relative;
        left: 50%;
        right: 50%;
        margin-left: -50vw;
        margin-right: -50vw;
        margin-top: 80px; 
        padding: 0; 
        margin-bottom: 0 !important; 
        padding-bottom: 0 !important;
        overflow: hidden; 
    }

    .footer {
        padding: 30px 0 15px 0; 
        background: rgba(10, 15, 30, 0.95);
        border-top: 3px solid #6c5ce7; 
        box-shadow: 0 -5px 15px rgba(0,0,0,0.5); 
        color: #ffffff !important;
        text-align: center;
        width: 100%;
    }
    .footer-content {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 30px; 
    }
    .footer p {
        margin: 5px 0;
        font-size: 14px;
        color: #ffffff !important; /* 🔥🔥 تأكيد النص في الفوتر أبيض */
    }
    .footer a {
        color: #a29bfe;
        text-decoration: none;
        transition: color 0.3s ease;
    }
    .footer a:hover {
        color: #ffffff;
    }
    .social-links a {
        margin: 0 12px;
        font-size: 22px;
        display: inline-block;
        color: #a29bfe;
    }

    /* 🔥🔥🔥 قاعدة إضافية لضمان لون النص الأبيض في جميع مكونات Streamlit */
    [data-testid*="st"] span, [data-testid*="st"] p, [data-testid*="st"] div {
        color: #ffffff !important;
    }
            
    </style>
""", unsafe_allow_html=True)
# -----------------------------
# Custom CSS & Animations (Dark Mode + High Contrast) - الكود المُعدّل ينتهي هنا
# -----------------------------

# -----------------------------
# Session State Initialization (Kept as is)
# -----------------------------
if 'users' not in st.session_state:
    st.session_state['users'] = [
        {'email': 'user@example.com', 'password': 'user', 'role': 'user', 'name': 'Demo User'},
        {'email': 'tech@example.com', 'password': 'tech', 'role': 'technical', 'name': 'Demo Technician'} 
    ]

if 'services' not in st.session_state:
    st.session_state['services'] = [
        {'id': 1, 'name': 'House Cleaning', 'category': 'Home', 'price': 50, 'description': 'Deep cleaning for living room, kitchen, and bath.', 'icon': '🧹'},
        {'id': 2, 'name': 'Plumbing Repair', 'category': 'Maintenance', 'price': 80, 'description': 'Fix leaks and unclog drains.', 'icon': '🔧'},
        {'id': 3, 'name': 'Tech Support', 'category': 'Tech', 'price': 60, 'description': 'Remote PC/Mac troubleshooting.', 'icon': '🖥️'},
        {'id': 20, 'name': 'Mobile Mechanic', 'category': 'Auto', 'price': 90, 'description': 'Oil change and battery replacement at home.', 'icon': '🛠️'},
        {'id': 23, 'name': 'Locksmith', 'category': 'Maintenance', 'price': 60, 'description': 'Emergency lockout or lock replacement.', 'icon': '🔐'},
        {'id': 40, 'name': 'Home Lighting Installation', 'category': 'Maintenance', 'price': 80, 'description': 'Install ceiling lights and lamps.', 'icon': '💡'}
    ]

if 'orders' not in st.session_state:
    st.session_state['orders'] = []

if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None

if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'Home'

if 'selected_service' not in st.session_state:
    st.session_state['selected_service'] = None

if 'selected_role_reg' not in st.session_state:
    st.session_state['selected_role_reg'] = 'user' 

# -----------------------------
# Auth Functions (Kept as is)
# -----------------------------
def login(email, password): 
    # Try logging in as 'user' first, then 'technical'
    if check_login(email, password, 'user'):
        return True, 'user'
    elif check_login(email, password, 'technical'):
        return True, 'technical'
    return False, None

def check_login(email, password, role_to_check):
    for user in st.session_state['users']:
        if user.get('email') == email and user.get('password') == password and user.get('role') == role_to_check:
            st.session_state['current_user'] = user
            if role_to_check == 'user':
                st.session_state['current_page'] = 'Services'
            elif role_to_check == 'technical':
                st.session_state['current_page'] = 'Pending Orders'
            return True
    return False

def register(email, password, name, role):
    for user in st.session_state['users']:
        if user.get('email') == email:
            return False 
    st.session_state['users'].append({
        'email': email,
        'password': password,
        'role': role,
        'name': name
    })
    return True

def logout():
    st.session_state['current_user'] = None
    st.session_state['current_page'] = 'Home'
    st.rerun()

# -----------------------------
# Navigation Component (Kept as is)
# -----------------------------
def top_nav():
    user = st.session_state['current_user']
    
    if not user:
        return 

    if user['role'] == 'user':
        menu_items = ["Services", "My Orders", "Profile", "Logout"]
    elif user['role'] == 'technical':
        menu_items = ["Pending Orders", "Profile", "Logout"]
    else:
        return

    cols = st.columns([1, len(menu_items), 1])
    with cols[1]:
        st.markdown('<div class="nav-container">', unsafe_allow_html=True)
        nav_cols = st.columns(len(menu_items))
        for i, item in enumerate(menu_items):
            with nav_cols[i]:
                if st.button(item, key=f"nav_{item}", use_container_width=True):
                    if item == "Logout":
                        logout()
                    else:
                        st.session_state['current_page'] = item
                        st.session_state['selected_service'] = None 
                        st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Footer Component (Kept as is)
# -----------------------------
def app_footer():
    st.markdown("""
        <div class="footer-container">
            <div class="footer">
                <div class="footer-content">
                    <h4 style="color: #a29bfe; margin-bottom: 10px;">Service Connect</h4>
                    <p>Connecting you with the best local services 🛠️</p>
                    <p style="margin-top: 15px;">
                        Contact: <a href="mailto:support@serviceconnect.com">support@serviceconnect.com</a> | Phone: (123) 456-7890
                    </p>
                    <div class="social-links" style="margin-top: 10px;">
                        <a href="#" target="_blank">🔗</a>
                        <a href="#" target="_blank">📱</a>
                        <a href="#" target="_blank">📧</a>
                    </div>
                    <p style="margin-top: 20px;">&copy; 2024 Service Connect Platform. All Rights Reserved.</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


# -----------------------------
# Pages
# -----------------------------

def home_page():
    # Only show this content if NO user is logged in
    if st.session_state['current_user']:
        if st.session_state['current_user']['role'] == 'user':
            st.session_state['current_page'] = 'Services'
        elif st.session_state['current_user']['role'] == 'technical':
            st.session_state['current_page'] = 'Pending Orders'
        st.rerun()
        return

    # --- 1. Enlarged Hero Section (Service Platform) ---
    st.markdown("""
        <div class="animate-enter hero-section">
            <h1 style="color: #a29bfe;">Service Connect Platform ✨</h1>
            <p>
                Your reliable partner for booking and providing local services across Home, Tech, Auto, and Maintenance.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # --- 2. Get Started Section (Login/Register) ---
    st.markdown("""
        <div style="margin-top: 50px; text-align: center;">
            <h2 style="color: white; margin-bottom: 30px;">Get Started Now</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Login/Register buttons 
    cols = st.columns([1.5, 2, 0.5, 2, 1.5])
    with cols[2]:
        st.markdown("<div style='height: 100%; display: flex; align-items: center; justify-content: center; font-weight: 700; color: #a29bfe; font-size: 1.5rem;'>OR</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown('<div class="home-auth-button">', unsafe_allow_html=True)
        if st.button("LOGIN", key="home_login", use_container_width=True):
            st.session_state['current_page'] = "Login"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
            
    with cols[3]:
        st.markdown('<div class="home-auth-button">', unsafe_allow_html=True)
        if st.button("REGISTER", key="home_register", use_container_width=True):
            st.session_state['current_page'] = "Register"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 3. About Us Section (6 Boxes - FINAL) ---
    st.markdown("""
        <div style="margin-top: 80px; text-align: center;">
            <h2 style="color: white; margin-bottom: 30px;">About Us: Our Mission & Values</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Row 1 (3 Boxes)
    cols_about_1 = st.columns(3)
    
    with cols_about_1[0]:
        st.markdown("""
            <div class="about-card animate-enter" style="animation-delay: 0.2s;">
                <div class="about-icon">🎯</div>
                <div class="about-title">Our Mission</div>
                <div class="about-text">
                    To connect users quickly and reliably with skilled technical professionals, ensuring quality service for every task, big or small.
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    with cols_about_1[1]:
        st.markdown("""
            <div class="about-card animate-enter" style="animation-delay: 0.4s;">
                <div class="about-icon">🤝</div>
                <div class="about-title">Trust & Transparency</div>
                <div class="about-text">
                    We vet all professionals and maintain clear, upfront pricing and communication, building trust with every interaction.
                </div>
            </div>
        """, unsafe_allow_html=True)

    with cols_about_1[2]:
        st.markdown("""
            <div class="about-card animate-enter" style="animation-delay: 0.6s;">
                <div class="about-icon">⚡</div>
                <div class="about-title">Efficiency & Quality</div>
                <div class="about-text">
                    We focus on fast response times and high-quality work, making sure your service needs are met efficiently.
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    # Row 2 (3 New Boxes - Added for the final count)
    cols_about_2 = st.columns(3)

    with cols_about_2[0]:
        st.markdown("""
            <div class="about-card animate-enter" style="animation-delay: 0.8s;">
                <div class="about-icon">🌱</div>
                <div class="about-title">Continuous Growth</div>
                <div class="about-text">
                    We constantly seek feedback and innovation to improve our platform and expand our service offerings based on community needs.
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    with cols_about_2[1]:
        st.markdown("""
            <div class="about-card animate-enter" style="animation-delay: 1.0s;">
                <div class="about-icon">🧑‍💻</div>
                <div class="about-title">Supportive Community</div>
                <div class="about-text">
                    We foster a supportive environment for both our users and the technical professionals, empowering local talent.
                </div>
            </div>
        """, unsafe_allow_html=True)

    with cols_about_2[2]:
        st.markdown("""
            <div class="about-card animate-enter" style="animation-delay: 1.2s;">
                <div class="about-icon">🗺️</div>
                <div class="about-title">Local Focus</div>
                <div class="about-text">
                    Dedicated to supporting local talent and providing community-focused services right where you need them, instantly.
                </div>
            </div>
        """, unsafe_allow_html=True)


def services_page():
    # Security check: only users can see this
    if not st.session_state['current_user'] or st.session_state['current_user']['role'] != 'user':
        st.warning("Access Denied. Please login as a **User**.")
        return
    
    # If a service is selected, show the details/payment view
    if st.session_state['selected_service']:
        service_details_page(st.session_state['selected_service'])
        return

    st.markdown("<h2 class='animate-enter' style='color: white;'>🔍 Explore All Services</h2>", unsafe_allow_html=True)
    
    # Filter
    categories = ["All"] + sorted(list({s['category'] for s in st.session_state['services']}))
    
    # 🔥🔥🔥 تعديل التنسيق هنا: نستخدم عموداً أصغر لحقل الفلترة 🔥🔥🔥
    cat_col, _ = st.columns([0.4, 3]) 
    with cat_col:
        selected_cat = st.selectbox("Filter by Category", categories)

    services = st.session_state['services']
    if selected_cat != "All":
        services = [s for s in services if s['category'] == selected_cat]

    # Grid Layout
    cols = st.columns(3)
    for i, s in enumerate(services):
        with cols[i % 3]:
            # 🔥🔥🔥 تم التعديل هنا لعرض النص الفعلي بدلاً من divs HTML tags كما ظهر في الصورة 🔥🔥🔥
            st.markdown(f"""
                <div class="service-card animate-enter" style="animation-delay: {i*0.05}s">
                    <div class="card-icon">{s['icon']}</div>
                    <div class="card-title">{s['name']}</div>
                    <div class="badge-cat">{s['category']}</div>
                    <div class="card-desc">{s['description']}</div>
                    <div class="card-price">${s['price']}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Action Button - هذا الزر سيطبق عليه تنسيق الـ .stButton > button البنفسجي
            if st.button(f"Select", key=f"srv_{s['id']}"):
                st.session_state['selected_service'] = s
                st.rerun()
            
            st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
            

def service_details_page(service):
    
    # 🔥🔥🔥 Back button: تم تضمينه في عمود صغير لتصغير الزر ليتناسب مع التصميم 🔥🔥🔥
    back_col, _ = st.columns([0.2, 1])
    with back_col:
        if st.button("← Back to List"):
            st.session_state['selected_service'] = None
            st.rerun()

    st.markdown(f"""
        <div class="animate-enter" style="background: rgba(30, 35, 60, 0.95); padding: 40px; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1); margin-top: 20px;">
            <div style="display: flex; align-items: center; gap: 25px; margin-bottom: 30px;">
                <div style="font-size: 60px; background: rgba(108, 92, 231, 0.2); width: 100px; height: 100px; display: flex; align-items: center; justify-content: center; border-radius: 50%; border: 2px solid #6c5ce7;">{service['icon']}</div>
                <div>
                    <h1 style="margin: 0; color: white; font-size: 2.5rem;">{service['name']}</h1>
                    <span style="background: #6c5ce7; color: white; padding: 6px 18px; border-radius: 20px; font-size: 14px; font-weight: 600; display: inline-block; margin-top: 10px;">{service['category']}</span>
                </div>
            </div>
            <p style="font-size: 18px; color: #ffffff; line-height: 1.6;">{service['description']}</p>
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.1);">
                <h2 style="color: #a29bfe; margin: 0;">Total Price: ${service['price']}</h2>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if not st.session_state['current_user'] or st.session_state['current_user']['role'] != 'user':
        st.warning("Please login as a **User** to complete your booking.")
        return

    st.markdown("### 🛠️ Complete Booking")
    
    with st.form("booking_form"):
        col1, col2 = st.columns(2)
        with col1:
            techs = ["Alice (Top Rated)", "Bob (Expert)", "Charlie (Fast)", "David (Premium)"]
            # 🔥🔥🔥 قائمة CHOOSE PROFESSIONAL هنا 🔥🔥🔥
            selected_tech = st.selectbox("Choose Professional", techs)
            date = st.date_input("Preferred Date", min_value=datetime.today())
        
        with col2:
            st.markdown("#### Payment Method")
            payment_method = st.radio("Select how you want to pay:", ["Credit Card (Online)", "Cash on Delivery", "Digital Wallet"], label_visibility="collapsed")
            notes = st.text_area("Special Instructions (Optional)")

        # زر Confirm Booking يتبع الآن تنسيق الأزرار البنفسجية
        submitted = st.form_submit_button("Confirm Booking")
        
        if submitted:
            # Simulate processing
            with st.spinner("Processing your request..."):
                time.sleep(1.5)
            
            # Simple order logic (Kept as is)
            order = {
                'id': str(uuid.uuid4()),
                'user_email': st.session_state['current_user']['email'],
                'user_name': st.session_state['current_user']['name'],
                'service_name': service['name'],
                'tech': selected_tech,
                'date': date.strftime('%Y-%m-%d'),
                'status': 'Pending',
                'paid': True if "Online" in payment_method or "Wallet" in payment_method else False,
                'payment_method': payment_method,
                'notes': notes,
                'price': service['price']
            }
            st.session_state['orders'].append(order)
            st.success("🎉 Booking Confirmed! Redirecting to orders...")
            time.sleep(1)
            st.session_state['selected_service'] = None
            st.session_state['current_page'] = "My Orders"
            st.rerun()

def orders_page():
    # Security check: only users can see this
    if not st.session_state['current_user'] or st.session_state['current_user']['role'] != 'user':
        st.error("Access Denied.")
        return

    st.markdown("<h2 class='animate-enter' style='color: white;'>📋 My Orders</h2>", unsafe_allow_html=True)
    
    user_email = st.session_state['current_user']['email']
    my_orders = [o for o in st.session_state['orders'] if o['user_email'] == user_email]
    
    if not my_orders:
        st.info("You haven't placed any orders yet.")
        return

    for i, o in enumerate(reversed(my_orders)):
        status_color = "#2ecc71" if o['status'] == 'Done' else ("#f1c40f" if o['status'] == 'Pending' else "#3498db")
        st.markdown(f"""
            <div class="animate-enter" style="background: rgba(30, 35, 60, 0.95); padding: 20px; border-radius: 15px; margin-bottom: 15px; border-left: 5px solid {status_color}; box-shadow: 0 5px 15px rgba(0,0,0,0.2); animation-delay: {i*0.1}s; border: 1px solid rgba(255,255,255,0.1);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="margin: 0; color: white;">{o['service_name']}</h3>
                    <span style="background: {status_color}20; color: {status_color}; padding: 5px 10px; border-radius: 10px; font-weight: bold; border: 1px solid {status_color};">{o['status']}</span>
                </div>
                <p style="color: #ffffff; margin: 10px 0;">
                    📅 <b>Date:</b> {o['date']} &nbsp;|&nbsp; 👨‍🔧 <b>Tech:</b> {o['tech']} &nbsp;|&nbsp; 💳 <b>{o['payment_method']}</b>
                </p>
                <div style="font-size: 14px; color: #dcdcdc;">Order ID: {o['id']}</div>
            </div>
        """, unsafe_allow_html=True)

def technical_orders_page():
    # Security check: only technicals can see this
    if not st.session_state['current_user'] or st.session_state['current_user']['role'] != 'technical':
        st.error("Access Denied.")
        return
        
    st.markdown("<h2 class='animate-enter' style='color: white;'>🛠️ Pending Service Requests</h2>", unsafe_allow_html=True)
    
    pending_orders = [o for o in st.session_state['orders'] if o['status'] == 'Pending']
    
    if not pending_orders:
        st.success("🎉 No pending orders! Good job!")
        return

    st.markdown(f"**Total Pending Orders:** {len(pending_orders)}")
    
    # Order display logic (Kept as is)
    cols = st.columns([1, 2, 2, 2, 1, 2])
    cols[0].markdown("**ID**")
    cols[1].markdown("**Service**")
    cols[2].markdown("**User/Date**")
    cols[3].markdown("**Tech Assigned**")
    cols[4].markdown("**Price**")
    cols[5].markdown("**Action**")
    st.markdown("---")
    
    for i, o in enumerate(pending_orders):
        order_id_short = o['id'].split('-')[0]
        
        row_cols = st.columns([1, 2, 2, 2, 1, 2])
        
        row_cols[0].markdown(f"<div style='color: #a29bfe; font-weight: bold;'>{order_id_short}...</div>", unsafe_allow_html=True)
        row_cols[1].markdown(f"**{o['service_name']}**")
        row_cols[2].markdown(f"**{o['user_name']}** ({o['date']})")
        row_cols[3].markdown(f"**{o['tech']}**")
        row_cols[4].markdown(f"**${o['price']}**")
        
        with row_cols[5]:
            # زر Mark as Done يتبع الآن تنسيق الأزرار البنفسجية
            if st.button("Mark as Done", key=f"complete_{o['id']}", use_container_width=True):
                for order in st.session_state['orders']:
                    if order['id'] == o['id']:
                        order['status'] = 'Done'
                        break
                st.toast(f"Order {order_id_short}... marked as Done!")
                time.sleep(1)
                st.rerun()

        st.markdown("<div style='margin-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.05);'></div>", unsafe_allow_html=True)


def login_page():
    # If already logged in, redirect to the correct page
    if st.session_state['current_user']:
        if st.session_state['current_user']['role'] == 'user':
            st.session_state['current_page'] = 'Services'
        elif st.session_state['current_user']['role'] == 'technical':
            st.session_state['current_page'] = 'Pending Orders'
        st.rerun()
        return

    # Back button - هذا الزر سيطبق عليه تنسيق الـ .stButton > button البنفسجي
    if st.button("← Back to Home"):
        st.session_state['current_page'] = 'Home'
        st.rerun()
        
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='animate-enter' style='text-align: center; margin-bottom: 30px;'><h2 style='color: white;'>Welcome Back! 👋</h2></div>", unsafe_allow_html=True)
        with st.form("login_form"):
            email = st.text_input("Email") 
            password = st.text_input("Password", type="password")
            
            # زر Login يتبع الآن تنسيق الأزرار البنفسجية
            if st.form_submit_button("Login"):
                success, role = login(email, password)
                if success:
                    st.success(f"Login successful as **{role.capitalize()}**! Redirecting...")
                    st.rerun() 
                else:
                    st.error("Invalid credentials.")

def register_page():
    # If already logged in, redirect
    if st.session_state['current_user']:
        if st.session_state['current_user']['role'] == 'user':
            st.session_state['current_page'] = 'Services'
        elif st.session_state['current_user']['role'] == 'technical':
            st.session_state['current_page'] = 'Pending Orders'
        st.rerun()
        return
    
    # Back button (NEW) - هذا الزر سيطبق عليه تنسيق الـ .stButton > button البنفسجي
    if st.button("← Back to Home"):
        st.session_state['current_page'] = 'Home'
        st.rerun()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='animate-enter' style='text-align: center; margin-bottom: 30px;'><h2 style='color: white;'>Join Service Connect! 🚀</h2></div>", unsafe_allow_html=True)
        
        # Role Selection UI (User or Technical)
        st.markdown("#### Select your role:")
        role_cols = st.columns(2)
        
        # User Button
        with role_cols[0]:
            is_user_selected = st.session_state['selected_role_reg'] == 'user'
            btn_class = "auth-role-button-selected" if is_user_selected else "auth-role-button"
            if st.markdown(f'<div class="{btn_class}">', unsafe_allow_html=True):
                # ملاحظة: هذه الأزرار لها تنسيق خاص (auth-role-button) وليست مثل الأزرار العامة.
                if st.button("Client/User 🧑", key="reg_user_role", use_container_width=True):
                    st.session_state['selected_role_reg'] = 'user'
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        # Technical Button
        with role_cols[1]:
            is_tech_selected = st.session_state['selected_role_reg'] == 'technical'
            btn_class = "auth-role-button-selected" if is_tech_selected else "auth-role-button"
            if st.markdown(f'<div class="{btn_class}">', unsafe_allow_html=True):
                if st.button("Technical Expert 🛠️", key="reg_tech_role", use_container_width=True):
                    st.session_state['selected_role_reg'] = 'technical'
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        role = st.session_state['selected_role_reg']
        st.markdown(f"<p style='text-align: center; color: #a29bfe; font-weight: 600;'>Registering as a: **{role.capitalize()}**</p>", unsafe_allow_html=True)
        
        # Registration Form
        with st.form("register_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            # زر Register يتبع الآن تنسيق الأزرار البنفسجية
            if st.form_submit_button("Register"):
                if not name or not email or not password or not confirm_password:
                    st.error("Please fill in all fields.")
                elif password != confirm_password:
                    st.error("Passwords do not match.")
                elif register(email, password, name, role):
                    st.success(f"Registration successful! Please login as a **{role.capitalize()}**.")
                    st.session_state['current_page'] = "Login"
                    st.session_state['selected_role_reg'] = 'user' # Reset role selection
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Email already exists. Please login or use a different email.")

def profile_page():
    if not st.session_state['current_user']:
        st.error("Please login to view your profile.")
        return

    user = st.session_state['current_user']
    
    st.markdown("<h2 class='animate-enter' style='color: white;'>👤 Your Profile</h2>", unsafe_allow_html=True)

    st.markdown(f"""
        <div class="animate-enter" style="background: rgba(30, 35, 60, 0.95); padding: 30px; border-radius: 15px; box-shadow: 0 10px 40px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1); margin-top: 20px;">
            <p style="font-size: 1.2rem; color: #a29bfe; margin-bottom: 5px;">Name: <span style="color: white; font-weight: bold;">{user['name']}</span></p>
            <p style="font-size: 1.2rem; color: #a29bfe; margin-bottom: 5px;">Email: <span style="color: white; font-weight: bold;">{user['email']}</span></p>
            <p style="font-size: 1.2rem; color: #a29bfe; margin-bottom: 0;">Role: <span style="color: #2ecc71; font-weight: bold; text-transform: capitalize;">{user['role']}</span></p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    
    # زر Logout يتبع الآن تنسيق الأزرار البنفسجية
    if st.button("Logout", key="profile_logout", use_container_width=True):
        logout()


# -----------------------------
# Main App Logic
# -----------------------------
def main():
    # 1. Navigation (always at the top after main content start)
    if st.session_state['current_user']:
        top_nav()

    # 2. Content Routing
    page = st.session_state['current_page']
    
    if page == 'Home':
        home_page()
    elif page == 'Login':
        login_page()
    elif page == 'Register':
        register_page()
    elif page == 'Services':
        services_page()
    elif page == 'My Orders':
        orders_page()
    elif page == 'Pending Orders':
        technical_orders_page()
    elif page == 'Profile':
        profile_page()

    # 3. Footer (always at the bottom)
    app_footer()

if __name__ == "__main__":
    main()