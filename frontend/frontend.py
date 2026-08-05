import pandas as pd
import requests
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Textile Waste Intelligence Platform",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Executive Dark Theme with Dynamic Wave & Particle Background
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

    /* Modern Text Inputs & Selectboxes */
    .stTextInput > div > div > input, .stSelectbox > div > div {
        background: rgba(22, 30, 46, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 10px !important;
        color: #f9fafb !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #10b981 !important;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.3) !important;
    }

    /* Action Buttons & Form Submit Buttons */
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

    /* Keep Password Eye Toggle Clean */
    button[aria-label="Show password"], 
    button[aria-label="Hide password"],
    .stTextInput button {
        background: transparent !important;
        box-shadow: none !important;
        border: none !important;
        transform: none !important;
        width: auto !important;
        padding: 0 !important;
    }

    /* Tab Formatting */
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
    st.session_state["auth_page"] = "register"
if "username" not in st.session_state:
    st.session_state["username"] = ""


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
            st.markdown(
                "<div class='card-title'>🧵 JOIN TWIP</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div class='card-subtitle'>Register your account to start managing waste streams</div>",
                unsafe_allow_html=True,
            )

            reg_user = st.text_input("USERNAME", placeholder="Choose a username")
            reg_email = st.text_input("EMAIL", placeholder="Enter your email")
            reg_role = st.selectbox(
                "ROLE",
                options=[
                    "Select your role",
                    "Administrator",
                    "Recycling Facility Operator",
                    "Sustainability Manager",
                    "Textile Manufacturer",
                ],
            )
            reg_pass = st.text_input(
                "PASSWORD", type="password", placeholder="••••••••"
            )
            confirm_pass = st.text_input(
                "CONFIRM PASSWORD", type="password", placeholder="••••••••"
            )
            st.write("")

            if st.form_submit_button(
                "Create Account", use_container_width=True
            ):
                if (
                    not reg_user
                    or not reg_email
                    or not reg_pass
                    or reg_role == "Select your role"
                ):
                    st.warning("All input fields and role selection are required.")
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
                            st.success(
                                "Account created successfully! Redirecting to login..."
                            )
                            st.session_state["auth_page"] = "login"
                            st.rerun()
                        else:
                            st.error(
                                res.json().get("detail", "Registration failed.")
                            )
                    except Exception:
                        st.error("Could not connect to backend server.")

        st.write("")
        if st.button(
            "Already have an account? Login here", use_container_width=True
        ):
            st.session_state["auth_page"] = "login"
            st.rerun()


# --- LOGIN PAGE ---
def show_login_page():
    render_header()
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            st.markdown(
                "<div class='card-title'>Sign In</div>", unsafe_allow_html=True
            )
            st.markdown(
                "<div class='card-subtitle'>Enter credentials to access executive controls</div>",
                unsafe_allow_html=True,
            )

            login_user = st.text_input(
                "Username", placeholder="Enter your username"
            )
            login_pass = st.text_input(
                "Password", type="password", placeholder="••••••••"
            )
            st.write("")

            if st.form_submit_button(
                "Authenticate System Access", use_container_width=True
            ):
                if login_user != "":
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = login_user
                    st.success("Authentication successful!")
                    st.rerun()
                else:
                    st.error("Please enter valid credentials.")

        st.write("")
        if st.button("Need an account? Register Here", use_container_width=True):
            st.session_state["auth_page"] = "register"
            st.rerun()


# --- DASHBOARD ---
def show_dashboard():
    render_header()

    st.sidebar.image("https://img.icons8.com/color/96/recycle.png", width=50)
    st.sidebar.title("Textile Platform")
    st.sidebar.markdown(f"🟢 Active User: **{st.session_state['username']}**")
    st.sidebar.write("---")

    navigation = st.sidebar.radio(
        "Navigation",
        ["Overview", "Waste Inventory", "Dataset Upload", "System Health"],
    )

    st.sidebar.write("---")
    if st.sidebar.button("Logout Session", use_container_width=True):
        st.session_state["logged_in"] = False
        st.session_state["auth_page"] = "login"
        st.rerun()

    if navigation == "Overview":
        st.title("📊 Executive Overview")
        st.caption("Real-time textile waste tracking & intelligence dashboard")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Waste Processed", "12,450 kg", "+8.2%")
        m2.metric("Recycle Rate", "74.5%", "+3.1%")
        m3.metric("Carbon Saved", "18.2 Tons", "+12.0%")
        m4.metric("Active Streams", "4 Categories", "Stable")

    elif navigation == "Waste Inventory":
        st.title("📦 Waste Inventory Management")

        tab_view, tab_add = st.tabs(["📋 View Inventory", "➕ Add New Batch"])

        with tab_view:
            if st.button("🔄 Sync Database Batches"):
                try:
                    res = requests.get(f"{API_URL}/inventory")
                    if res.status_code == 200:
                        data = res.json().get("data", [])
                        if data:
                            st.dataframe(
                                pd.DataFrame(data), use_container_width=True
                            )
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
                    f_type = st.selectbox(
                        "Fabric Type",
                        ["Cotton", "Polyester", "Wool", "Silk", "Blend"],
                    )
                    src = st.text_input("Source Factory", value="Facility C")
                with col_b:
                    qty = st.number_input(
                        "Quantity (kg)", min_value=1.0, value=100.0
                    )
                    clr = st.text_input("Color", value="Green")
                    cnd = st.selectbox(
                        "Condition", ["Recyclable", "Reusable", "Contaminated"]
                    )

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

        st.markdown("---")
        st.subheader("🛠️ Manage Inventory Items")
        try:
            res = requests.get(f"{API_URL}/inventory")
            if res.status_code == 200:
                items = res.json().get("data", [])
                if items:
                    item_indices = list(range(len(items)))
                    selected_index = st.selectbox(
                        "Select Item Index to Manage",
                        options=item_indices,
                        format_func=lambda i: f"Index {i}: {items[i].get('fabric_type', 'Material')} ({items[i].get('quantity_kg', 0)} kg)",
                    )
                    current_item = items[selected_index]
                    col1, col2 = st.columns(2)
                    with col1:
                        new_material = st.text_input(
                            "Fabric Type",
                            value=current_item.get("fabric_type", ""),
                        )
                        new_weight = st.number_input(
                            "Weight (kg)",
                            value=float(current_item.get("quantity_kg", 0.0)),
                        )
                        new_condition = st.selectbox(
                            "Condition",
                            ["Recyclable", "Reusable", "Contaminated"],
                            index=0,
                        )
                        if st.button("Update Item"):
                            payload = {
                                "fabric_type": new_material,
                                "quantity_kg": new_weight,
                                "condition": new_condition,
                            }
                            upd_res = requests.put(
                                f"{API_URL}/inventory/{selected_index}",
                                json=payload,
                            )
                            if upd_res.status_code == 200:
                                st.success(upd_res.json().get("message"))
                                st.rerun()
                    with col2:
                        st.warning(
                            f"Are you sure you want to delete Index {selected_index}?"
                        )
                        if st.button("Delete Item", type="primary"):
                            del_res = requests.delete(
                                f"{API_URL}/inventory/{selected_index}"
                            )
                            if del_res.status_code == 200:
                                st.success(del_res.json().get("message"))
                                st.rerun()
                else:
                    st.info("No inventory items found to manage.")
        except Exception:
            st.info("Backend offline or inventory empty.")

    elif navigation == "Dataset Upload":
        st.title("📁 Waste CSV Dataset Ingestion")
        st.caption("Upload raw CSV datasets to analyze real-time statistics.")
        uploaded_file = st.file_uploader("Choose CSV Dataset", type=["csv"])

        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.success("Dataset Loaded Successfully!")
                st.dataframe(df, use_container_width=True)

                if st.button("Process & Save to Database"):
                    with st.spinner("Saving data to database..."):
                        files = {
                            "file": (
                                uploaded_file.name,
                                uploaded_file.getvalue(),
                                "text/csv",
                            )
                        }
                        res = requests.post(f"{API_URL}/upload-csv", files=files)
                        if res.status_code == 200:
                            st.success("Data successfully processed!")
                        else:
                            st.error("Failed to upload CSV.")
            except Exception as e:
                st.error(f"Error: {e}")

    elif navigation == "System Health":
        st.subheader("🔌 Backend Core Diagnostics")
        if st.button("Run Connection Diagnostic"):
            try:
                res = requests.get(f"{API_URL}/")
                if res.status_code == 200:
                    st.success(
                        f"System Response: {res.json().get('message')}"
                    )
            except Exception:
                st.error("Backend Core unreachable.")


# 4. View Router
if not st.session_state["logged_in"]:
    if st.session_state["auth_page"] == "register":
        show_register_page()
    else:
        show_login_page()
else:
    show_dashboard()