import PIL.Image
import pandas as pd
import plotly.express as px
import requests
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Textile Waste Intelligence Platform",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Executive Dark Theme with Dynamic Wave & Particle Background (Original CSS Kept Intact)
st.markdown(
    """
    <style>
    /* Dark Space Background with SVG Geometric Waves & Bokeh Orbs */
    .stApp {
        background-color: #060b13;
        background-image: 
            /* Floating Glowing Bokeh Particles */
            radial-gradient(circle at 10% 80%, rgba(16, 185, 129, 0.12) 0%, transparent 20%),
            radial-gradient(circle at 88% 25%, rgba(6, 182, 212, 0.15) 0%, transparent 22%),
            radial-gradient(circle at 92% 70%, rgba(16, 185, 129, 0.08) 0%, transparent 18%),
            radial-gradient(circle at 15% 15%, rgba(56, 189, 248, 0.1) 0%, transparent 25%),
            /* Abstract Dynamic Wavy Mesh Overlay */
            url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="900" viewBox="0 0 1440 900" preserveAspectRatio="none"><path fill="none" stroke="rgba(20, 184, 166, 0.15)" stroke-width="1.2" d="M-100,600 C300,300 700,800 1540,300 M-100,620 C300,320 700,820 1540,320 M-100,640 C300,340 700,840 1540,340 M-100,660 C300,360 700,860 1540,360 M-100,680 C300,380 700,880 1540,380 M-100,700 C300,400 700,900 1540,400 M-100,720 C300,420 700,920 1540,420 M-100,740 C300,440 700,940 1540,440"/><path fill="none" stroke="rgba(16, 185, 129, 0.08)" stroke-width="1" d="M-100,200 C400,600 800,100 1540,500 M-100,230 C400,630 800,130 1540,530 M-100,260 C400,660 800,160 1540,560 M-100,290 C400,690 800,190 1540,590"/></svg>'),
            /* Base Radial Vignette */
            radial-gradient(circle at 50% 50%, #0c1322 0%, #050811 100%);
        background-attachment: fixed;
        background-size: cover;
        color: #f3f4f6;
    }

    /* Top Highlight Banner for Platform Title */
    .top-banner {
        background: linear-gradient(90deg, rgba(16, 185, 129, 0.15) 0%, rgba(6, 182, 212, 0.15) 100%);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        padding: 1.2rem 1rem;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.15);
    }

    .top-banner-title {
        background: linear-gradient(135deg, #10b981 0%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 2.2rem;
        letter-spacing: 1px;
        margin: 0;
        text-transform: uppercase;
    }

    .top-banner-sub {
        color: #9ca3af;
        font-size: 0.9rem;
        margin-top: 4px;
        letter-spacing: 0.5px;
    }
    
    /* Glassmorphism Card Container Matching UI */
    div[data-testid="stForm"] {
        background: rgba(13, 19, 33, 0.82) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 20px !important;
        padding: 2.5rem !important;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.7), 0 0 40px rgba(16, 185, 129, 0.05) !important;
    }

    .card-title {
        color: #10b981;
        font-weight: 800;
        text-align: center;
        font-size: 1.8rem;
        margin-bottom: 0.2rem;
        letter-spacing: 1px;
        text-shadow: 0 0 12px rgba(16, 185, 129, 0.4);
    }
    
    .card-subtitle {
        color: #9ca3af;
        text-align: center;
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
    }

    /* Custom Metric & Chart Card Containers */
    .metric-card {
        background: rgba(13, 19, 33, 0.82);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.2rem;
        backdrop-filter: blur(20px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }

    .metric-title {
        color: #9ca3af;
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .metric-value {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 800;
        margin: 4px 0;
    }

    .metric-delta-up {
        color: #10b981;
        font-size: 0.8rem;
        font-weight: 600;
    }

    .metric-delta-down {
        color: #ef4444;
        font-size: 0.8rem;
        font-weight: 600;
    }

    .chart-card {
        background: rgba(13, 19, 33, 0.82);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.25rem;
        backdrop-filter: blur(20px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }

    .chart-header {
        color: #ffffff;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 1rem;
    }

    /* Inputs & Selectboxes */
    .stTextInput > div > div > input, .stSelectbox > div > div {
        background: rgba(22, 30, 46, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 10px !important;
        color: #f9fafb !important;
    }

    /* Buttons */
    div.stButton > button, 
    div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #059669 0%, #0284c7 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease-in-out !important;
        box-shadow: 0 4px 20px rgba(5, 150, 105, 0.3) !important;
        width: 100% !important;
    }

    div.stButton > button:hover, 
    div[data-testid="stFormSubmitButton"] > button:hover {
        background: linear-gradient(135deg, #10b981 0%, #38bdf8 100%) !important;
        box-shadow: 0 6px 25px rgba(16, 185, 129, 0.5) !important;
        transform: translateY(-2px);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(31, 41, 55, 0.5);
        border-radius: 10px;
        padding: 10px 20px;
        color: #9ca3af;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .stTabs [aria-selected="true"] {
        background: rgba(16, 185, 129, 0.15) !important;
        color: #34d399 !important;
        border: 1px solid rgba(16, 185, 129, 0.4) !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

API_URL = "http://127.0.0.1:8000/api"

# 3. Session State Initialization
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "auth_page" not in st.session_state:
    st.session_state["auth_page"] = "login"
if "username" not in st.session_state:
    st.session_state["username"] = "pr"
if "role" not in st.session_state:
    st.session_state["role"] = "Administrator"


# --- TOP HIGHLIGHTED HEADER ---
def render_header():
    st.markdown(
        """
        <div class="top-banner">
            <h1 class="top-banner-title">🧵 Textile Waste Intelligence Platform</h1>
            <p class="top-banner-sub">Enterprise Analytics • Sustainable Supply Chain • Waste Inventory Management</p>
        </div>
    """,
        unsafe_allow_html=True,
    )


# --- REGISTER PAGE ---
def show_register_page():
    render_header()
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        with st.form("register_form"):
            st.markdown("<div class='card-title'>🧵 JOIN TWIP</div>", unsafe_allow_html=True)
            st.markdown("<div class='card-subtitle'>Register your account to start managing waste streams</div>", unsafe_allow_html=True)

            reg_user = st.text_input("USERNAME", placeholder="Choose a username")
            reg_email = st.text_input("EMAIL", placeholder="Enter your email")
            reg_role = st.selectbox(
                "ROLE",
                options=[
                    "Administrator",
                    "Recycling Facility Operator",
                    "Sustainability Manager",
                    "Textile Manufacturer",
                ],
            )
            reg_pass = st.text_input("PASSWORD", type="password", placeholder="••••••••")
            confirm_pass = st.text_input("CONFIRM PASSWORD", type="password", placeholder="••••••••")
            st.write("")

            if st.form_submit_button("Create Account", use_container_width=True):
                if not reg_user or not reg_email or not reg_pass:
                    st.warning("All input fields are required.")
                elif reg_pass != confirm_pass:
                    st.error("Passwords do not match!")
                else:
                    try:
                        res = requests.post(
                            f"{API_URL}/auth/register",
                            json={
                                "username": reg_user,
                                "email": reg_email,
                                "role": reg_role,
                                "password": reg_pass,
                            },
                        )
                        if res.status_code in [200, 201]:
                            st.success("Account created successfully! Redirecting to login...")
                            st.session_state["auth_page"] = "login"
                            st.rerun()
                        else:
                            st.error(res.json().get("detail", "Registration failed."))
                    except Exception:
                        st.error("Could not connect to backend server.")

        st.write("")
        if st.button("Already have an account? Login here", use_container_width=True):
            st.session_state["auth_page"] = "login"
            st.rerun()


# --- LOGIN PAGE ---
def show_login_page():
    render_header()
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            st.markdown("<div class='card-title'>Sign In</div>", unsafe_allow_html=True)
            st.markdown("<div class='card-subtitle'>Enter credentials to access executive controls</div>", unsafe_allow_html=True)

            login_user = st.text_input("Username", value="pr")
            login_pass = st.text_input("Password", type="password", value="••••••••")
            st.write("")

            if st.form_submit_button("Authenticate System Access", use_container_width=True):
                if login_user:
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = login_user
                    st.session_state["role"] = "Administrator"
                    st.success("Authentication successful!")
                    st.rerun()
                else:
                    st.error("Please enter valid credentials.")

        st.write("")
        if st.button("Need an account? Register Here", use_container_width=True):
            st.session_state["auth_page"] = "register"
            st.rerun()


# --- OVERVIEW TAB CONTENT (SCREENSOT 2 LAYOUT & CHARTS) ---
def render_overview():
    st.title("DASHBOARD OVERVIEW")
    st.caption("Real-time intelligence on textile waste flows.")

    # 4 Metric Cards from Screenshot 2
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-title">TOTAL BATCHES</div>
                <div class="metric-value">1,248</div>
                <div class="metric-delta-up">↑ +12.5% from last month</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-title">TOTAL WEIGHT (KG)</div>
                <div class="metric-value">85,400</div>
                <div class="metric-delta-up">↑ +5.2% from last month</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-title">AVG RECYCLABILITY</div>
                <div class="metric-value">68%</div>
                <div class="metric-delta-up">↑ +2.1% from last month</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m4:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-title">CARBON SAVED (TONS)</div>
                <div class="metric-value">342</div>
                <div class="metric-delta-down">↓ -1.4% from last month</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    st.write("")

    # Visual Analytics Row (Donut & Bar Chart)
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-header">Material Distribution</div>', unsafe_allow_html=True)
        
        material_df = pd.DataFrame({
            "Material": ["Cotton", "Polyester", "Wool", "Silk", "Blends"],
            "Share": [40, 25, 12, 8, 15]
        })
        
        fig_donut = px.pie(
            material_df, 
            values="Share", 
            names="Material", 
            hole=0.6,
            color_discrete_sequence=["#10b981", "#06b6d4", "#f59e0b", "#ec4899", "#a855f7"]
        )
        fig_donut.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff"),
            margin=dict(t=10, b=10, l=10, r=10),
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05)
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_chart2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-header">Waste Categories</div>', unsafe_allow_html=True)
        
        categories_df = pd.DataFrame({
            "Category": ["Recyclable", "Reusable", "Repairable", "Hazardous", "Compostable"],
            "Volume": [35000, 22000, 16000, 3000, 10000]
        })
        
        fig_bar = px.bar(
            categories_df, 
            x="Category", 
            y="Volume",
            color_discrete_sequence=["#38bdf8"]
        )
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff"),
            xaxis=dict(showgrid=False, title=""),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.08)", title="Volume (kg)"),
            margin=dict(t=10, b=10, l=10, r=10)
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# --- DASHBOARD NAVIGATION ---
def show_dashboard():
    render_header()

    st.sidebar.markdown(
        """
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 1.8rem;">🧵</span>
            <span style="font-size: 1.5rem; font-weight: 900; color: #10b981;">TWIP</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.write("---")

    navigation = st.sidebar.radio(
        "Navigation",
        [
            "Overview",
            "Inventory",
            "Classification",
            "Reports",
            "Upload Data",
            "Analytics",
            "Profile",
        ],
    )

    st.sidebar.write("---")
    st.sidebar.markdown(f"**{st.session_state['username']}**")
    st.sidebar.caption(f"{st.session_state['role']}")
    
    if st.sidebar.button("Log Out", use_container_width=True):
        st.session_state["logged_in"] = False
        st.session_state["auth_page"] = "login"
        st.rerun()

    # Route navigation
    if navigation == "Overview":
        render_overview()

    elif navigation == "Inventory":
        st.title("📦 Waste Inventory Management")
        tab_view, tab_add = st.tabs(["📋 View Inventory", "➕ Add New Batch"])

        with tab_view:
            if st.button("🔄 Sync Database Batches"):
                try:
                    res = requests.get(f"{API_URL}/inventory")
                    if res.status_code == 200:
                        data = res.json().get("data", [])
                        if data:
                            st.dataframe(pd.DataFrame(data), use_container_width=True)
                        else:
                            st.info("No waste batches registered yet.")
                    else:
                        st.error("Failed to fetch inventory dataset.")
                except Exception:
                    st.error("Backend connection error.")

        with tab_add:
            with st.form("add_batch_form"):
                col_a, col_b = st.columns(2)
                with col_a:
                    b_id = st.text_input("Batch ID", value="BATCH-003")
                    f_type = st.selectbox("Fabric Type", ["Cotton", "Polyester", "Wool", "Silk", "Blend"])
                    src = st.text_input("Source Factory", value="Facility C")
                with col_b:
                    qty = st.number_input("Quantity (kg)", min_value=1.0, value=100.0)
                    clr = st.text_input("Color", value="Green")
                    cnd = st.selectbox("Condition", ["Recyclable", "Reusable", "Contaminated"])

                if st.form_submit_button("Commit Batch Record"):
                    payload = {
                        "batch_id": b_id,
                        "fabric_type": f_type,
                        "source": src,
                        "quantity_kg": qty,
                        "color": clr,
                        "condition": cnd,
                    }
                    try:
                        res = requests.post(f"{API_URL}/inventory", json=payload)
                        if res.status_code == 200:
                            st.success("Batch successfully committed!")
                        else:
                            st.error("Error committing batch.")
                    except Exception:
                        st.error("Backend server connection error.")

    elif navigation == "Upload Data":
        st.title("📁 Waste CSV Dataset Ingestion")
        uploaded_file = st.file_uploader("Choose CSV Dataset", type=["csv"])

        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.success("Dataset Loaded Successfully!")
                st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")

    elif navigation == "Classification":
        st.title("🧵 Fabric Material Classification Engine")
        st.caption("Upload a textile sample image to perform automated material composition analysis.")

        uploaded_file = st.file_uploader("Upload Fabric Sample Image", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            image = PIL.Image.open(uploaded_file)
            st.image(image, caption=f"Sample: {uploaded_file.name}", width=350)

            if st.button("Run Image Analysis & Material Classification"):
                with st.spinner("Analyzing textile texture, patterns, and composition..."):
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    
                    try:
                        print("TARGET URL:", f"{API_URL}/classify/material")
                        res = requests.post("http://127.0.0.1:8000/api/classify/material", files=files)
                        
                        if res.status_code == 200:
                            result = res.json().get("analysis", {})
                            st.success("Analysis Complete!")

                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric(label="Detected Material", value=result.get("material_detected", "N/A"))
                            with col2:
                                conf = result.get("confidence", 0)
                                st.metric(label="Confidence Rating", value=f"{round(conf * 100, 1)}%")
                            with col3:
                                qual = result.get("quality_score", 0)
                                st.metric(label="Quality Score", value=f"{int(qual * 100)} / 100")

                            st.divider()

                            st.subheader("🔍 Material Characteristics")
                            c_a, c_b, c_c = st.columns(3)
                            with c_a:
                                st.write(f"**Texture:** {result.get('texture', 'N/A').title()}")
                            with c_b:
                                st.write(f"**Pattern:** {result.get('pattern', 'N/A').title()}")
                            with c_c:
                                st.write(f"**Color Detected:** {result.get('color_detected', 'N/A')}")

                            st.write(f"**Defects Identified:** {result.get('defects_detected', 'N/A').title()}")

                        else:
                            st.error(f"Backend Server Error (Status Code: {res.status_code})")

                    except Exception as e:
                        st.error(f"Failed to connect to backend server: {e}")

    else:
        st.title(f"{navigation}")
        st.info("Module active and operating normally.")


# 4. View Router
if not st.session_state["logged_in"]:
    if st.session_state["auth_page"] == "register":
        show_register_page()
    else:
        show_login_page()
else:
    show_dashboard()