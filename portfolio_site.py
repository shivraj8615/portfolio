import streamlit as st
import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Page configuration
st.set_page_config(
    page_title="Shivesh Raj - Portfolio",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with reduced white background and seamless design
st.markdown("""
<style>
    /* Remove default Streamlit padding and white backgrounds */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    /* Remove main block container background */
    .main .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
    }
    
    /* Remove header background */
    header {
        background: transparent !important;
    }
    
    /* Remove sidebar top padding */
    .css-1d391kg {
        padding-top: 0rem;
    }
    
    /* Animated background elements */
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    .floating-shapes {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        overflow: hidden;
    }
    
    .shape {
        position: absolute;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        animation: float 15s infinite linear;
    }
    
    .shape:nth-child(1) {
        width: 80px;
        height: 80px;
        top: 20%;
        left: 10%;
        animation-duration: 20s;
    }
    
    .shape:nth-child(2) {
        width: 120px;
        height: 120px;
        top: 60%;
        left: 80%;
        animation-duration: 25s;
    }
    
    .shape:nth-child(3) {
        width: 60px;
        height: 60px;
        top: 80%;
        left: 20%;
        animation-duration: 18s;
    }
    
    .shape:nth-child(4) {
        width: 100px;
        height: 100px;
        top: 30%;
        left: 70%;
        animation-duration: 22s;
    }

    /* Main content styling with reduced opacity */
    .main-content {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 3rem;
        margin: 2rem;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        position: relative;
        z-index: 1;
    }
    
    .main-header {
        font-size: 4rem;
        background: linear-gradient(45deg, #2c3e50, #3498db, #9b59b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: 800;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.1);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .sub-header {
        font-size: 2rem;
        color: #7f8c8d;
        text-align: center;
        margin-top: 0;
        font-weight: 300;
        background: rgba(255, 255, 255, 0.7);
        padding: 1rem 3rem;
        border-radius: 60px;
        display: inline-block;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .section-header {
        font-size: 2.5rem;
        color: #2c3e50;
        padding-bottom: 1rem;
        margin-top: 3rem;
        margin-bottom: 2rem;
        font-weight: 700;
        background: linear-gradient(45deg, #2c3e50, #3498db);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        border-bottom: 3px solid;
        border-image: linear-gradient(45deg, #3498db, #9b59b6) 1;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Enhanced glass cards with reduced opacity */
    .experience-card {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.85), rgba(248, 249, 250, 0.75));
        backdrop-filter: blur(15px);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        border-left: 8px solid;
        border-image: linear-gradient(45deg, #3498db, #9b59b6) 1;
        box-shadow: 0 12px 30px rgba(0,0,0,0.15);
        transition: all 0.4s ease;
        border: 1px solid rgba(255, 255, 255, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .experience-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    
    .experience-card:hover::before {
        left: 100%;
    }
    
    .experience-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    }
    
    .skill-pill {
        background: linear-gradient(45deg, #3498db, #2980b9);
        color: white;
        padding: 0.7rem 1.5rem;
        border-radius: 30px;
        margin: 0.4rem;
        display: inline-block;
        font-size: 1rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .skill-pill:hover {
        transform: scale(1.1) translateY(-3px);
        box-shadow: 0 8px 25px rgba(52, 152, 219, 0.4);
        border-color: rgba(255, 255, 255, 0.5);
    }
    
    /* Contact form styling */
    .contact-form {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.95), rgba(248, 249, 250, 0.9));
        backdrop-filter: blur(20px);
        padding: 3rem;
        border-radius: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border: 1px solid rgba(255, 255, 255, 0.4);
    }
    
    /* Project cards */
    .project-card {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.9), rgba(248, 249, 250, 0.8));
        backdrop-filter: blur(15px);
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.4);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .project-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(45deg, #3498db, #9b59b6);
    }
    
    .project-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    /* Navigation styling */
    .stButton button {
        width: 100%;
        background: linear-gradient(45deg, #3498db, #2980b9);
        color: white;
        border: none;
        padding: 1.2rem;
        border-radius: 15px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3);
        margin: 0.5rem 0;
    }
    
    .stButton button:hover {
        background: linear-gradient(45deg, #2980b9, #2471a3);
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(52, 152, 219, 0.4);
    }
    
    /* Custom metric cards */
    .metric-card {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.9), rgba(248, 249, 250, 0.8));
        backdrop-filter: blur(15px);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border: 1px solid rgba(255, 255, 255, 0.4);
        transition: all 0.3s ease;
        border-top: 6px solid;
        border-image: linear-gradient(45deg, #3498db, #9b59b6) 1;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(20px) !important;
    }
</style>

<div class="floating-shapes">
    <div class="shape"></div>
    <div class="shape"></div>
    <div class="shape"></div>
    <div class="shape"></div>
</div>
""", unsafe_allow_html=True)

# Email configuration
WEB3FORMS_ACCESS_KEY = "c91ee3ed-54c1-40b6-933b-0883f4e143e0"

def send_email_via_web3forms(name, email, subject, message):
    """
    Send email using Web3Forms free API
    """
    data = {
        "access_key": WEB3FORMS_ACCESS_KEY,
        "subject": f"Portfolio Contact: {subject}",
        "from_name": name,
        "email": email,
        "message": message,
        "reply_to": email,
    }
    
    try:
        response = requests.post("https://api.web3forms.com/submit", data=data)
        result = response.json()
        return result.get("success", False), result.get("message", "Unknown error")
    except Exception as e:
        return False, str(e)

# Sidebar Navigation
st.sidebar.markdown("""
<div style="text-align: center; margin-bottom: 2rem; padding: 1rem;">
    <h2 style="color: #2c3e50; margin-bottom: 1rem; background: linear-gradient(45deg, #3498db, #9b59b6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 700;">🚀 Navigation</h2>
</div>
""", unsafe_allow_html=True)

# Navigation buttons
nav_options = ["🏠 Home", "💼 Experience", "🚀 Projects", "🎓 Education", "🛠️ Skills", "📞 Contact"]
selected_nav = st.sidebar.radio("", nav_options, label_visibility="collapsed")

# Add some metrics in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Quick Stats")
col1, col2 = st.sidebar.columns(2)
with col1:
    st.metric("Experience", "3+ Years")
with col2:
    st.metric("Projects", "8+")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🌐 Connect With Me")
st.sidebar.markdown("""
<div style="background: rgba(255,255,255,0.8); padding: 1rem; border-radius: 15px; border: 1px solid rgba(255,255,255,0.3);">
    <p>📧 rajshivesh@yahoo.com</p>
    <p>💼 <a href="https://linkedin.com/in/shivesh-raj-bldb3bl51" target="_blank">LinkedIn</a></p>
    <p>🐙 <a href="https://github.com/shivraj8615" target="_blank">GitHub</a></p>
    <p>🐙 <a href="https://github.com/sraj-sudo" target="_blank">GitHub</a></p>
</div>
""", unsafe_allow_html=True)

# Main content container
with st.container():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)

    # Home Page
    if selected_nav == "🏠 Home":
        # Hero Section
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image("https://res.cloudinary.com/dia44jplz/image/upload/v1763004575/IMG_20221022_110023_ecehfd.jpg", 
                    use_container_width=True)
        
        with col2:
            st.markdown('<h1 class="main-header">Shivesh Raj</h1>', unsafe_allow_html=True)
            st.markdown('<p class="sub-header">Mechanical Engineer & Cloud-Native Developer</p>', unsafe_allow_html=True)
            
            st.markdown("""
            <div style='background: linear-gradient(145deg, rgba(255,255,255,0.9), rgba(248,249,250,0.8)); padding: 2.5rem; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); border: 1px solid rgba(255,255,255,0.4);'>
                <h3 style='color: #2c3e50; margin-bottom: 1.5rem; text-align: center;'>🌟 About Me</h3>
                <p style='color: #555; line-height: 1.8; font-size: 1.2rem; text-align: center;'>
                Passionate about making processes smarter, faster, and more efficient through automation and digital transformation. 
                Bridging the gap between mechanical systems and cloud-native software solutions with expertise in Docker, Kubernetes, 
                CI/CD pipelines, and cloud platforms. Mechanical Engineer turned Automation Developer with hands-on experience designing and deploying automation platforms that connect Sales, Engineering and Manufacturing workflows. Proven skills in CAD
automation (FreeCAD, CadQuery), Python-based microservices, containerized deployments (Docker, Kubernetes), and CI/CD on cloud platforms (Microsoft Azure, OCI). Passionate about building scalable
automation systems (drawing/BOM automation, workflow codification) that reduce manual effort and
accelerate engineering throughput.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Key Highlights
        st.markdown('<h2 class="section-header">🎯 Core Expertise</h2>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3 style="font-size: 3rem; margin: 0;">🤖</h3>
                <h4 style="color: #2c3e50;">Process Automation</h4>
                <p style="color: #666;">Streamlining workflows with intelligent automation</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3 style="font-size: 3rem; margin: 0;">☁️</h3>
                <h4 style="color: #2c3e50;">Cloud Native</h4>
                <p style="color: #666;">Docker, Kubernetes, GCP & OCI expertise</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3 style="font-size: 3rem; margin: 0;">🔄</h3>
                <h4 style="color: #2c3e50;">CI/CD</h4>
                <p style="color: #666;">End-to-end deployment automation</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card">
                <h3 style="font-size: 3rem; margin: 0;">🏭</h3>
                <h4 style="color: #2c3e50;">Industry 4.0</h4>
                <p style="color: #666;">Physical systems meet digital intelligence</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Vision Section
        st.markdown("---")
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 4rem; border-radius: 25px; color: white; text-align: center; margin: 3rem 0; box-shadow: 0 15px 35px rgba(0,0,0,0.2);'>
            <h2 style='color: white; margin-bottom: 2rem; font-size: 2.5rem;'>🎯 Vision</h2>
            <p style='font-size: 1.4rem; line-height: 1.8; font-weight: 300;'>
            To leverage my engineering background and cloud expertise to drive impactful automation, 
            optimize workflows, and contribute to smarter, more sustainable industries.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Experience Page
    elif selected_nav == "💼 Experience":
        st.markdown('<h1 class="main-header">💼 Professional Experience</h1>', unsafe_allow_html=True)
        
        experiences = [
            {
                "title": "Associate System Architect",
                "company": "Forbes Marshall",
                "duration": "August 2025 - Present",
                "description": "Lead system architecture and design for an enterprise automation platform integrating Sales, Engineering and cross-functional teams.",
                "icon": "🏢"
            },
            {
                "title": "System Architect",
                "company": "Forbes Marshall",
                "duration": "May 2025 - August 2025",
                "description": "Designed systems for workflow automation.",
                "icon": "💻"
            },
            {
                "title": "Graduate Trainee",
                "company": "Forbes Marshall",
                "duration": "August 2024 - May 2025",
                "description": "Assigned a project to analyse data for various clients and find out their plant performance and effect from our design. Also responsible to develop various dashboards for the Energy Services Division.",
                "icon": "📊"
            },
            {
                "title": "Research Assistant",
                "company": "Indian Institute of Technology, Guwahati",
                "duration": "July 2022 - November 2022",
                "description": "Skills: Machine Learning · Pattern Recognition · Data Science · Computer Science · Artificial Intelligence (AI)",
                "icon": "🔬"
            },
            {
                "title": "Machine Learning Engineer",
                "company": "Freelance",
                "duration": "February 2022 - November 2022",
                "description": "Skills: Computer Science · Artificial Intelligence (AI)",
                "icon": "🤖"
            },
            {
                "title": "Nvidia Developer",
                "company": "NVIDIA",
                "duration": "October 2021 - February 2022",
                "description": "Skills: Deep Learning · Pattern Recognition · TensorFlow · Data Science · Computer Science · Artificial Intelligence (AI)",
                "icon": "🎮"
            }
        ]
        
        for exp in experiences:
            st.markdown(f"""
            <div class="experience-card">
                <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                    <span style="font-size: 2.5rem; margin-right: 1.5rem;">{exp['icon']}</span>
                    <div>
                        <h3 style="color: #2c3e50; margin: 0; font-size: 1.6rem; font-weight: 700;">{exp['title']}</h3>
                        <h4 style="color: #3498db; margin: 0; font-size: 1.3rem; font-weight: 600;">{exp['company']} | {exp['duration']}</h4>
                    </div>
                </div>
                <p style="color: #555; line-height: 1.8; margin: 0; font-size: 1.1rem;">{exp['description']}</p>
            </div>
            """, unsafe_allow_html=True)

    # Projects Page
    elif selected_nav == "🚀 Projects":
        st.markdown('<h1 class="main-header">🚀 Projects</h1>', unsafe_allow_html=True)
        
        projects = [
            {"name": "Sample Webapp", "description": "A modern web application showcasing full-stack development skills", "tech": ["Django", "Docker", "GCP"], "icon": "🌐"},
            {"name": "PCB Defect Detector", "description": "AI-powered system for detecting defects in printed circuit boards", "tech": ["Computer Vision", "TensorFlow", "Python"], "icon": "🔍"},
            {"name": "Predictive Maintenance", "description": "Machine learning system for predicting equipment failures", "tech": ["ML", "IoT", "Cloud"], "icon": "📈"},
            {"name": "CAD Automation", "description": "Automating CAD processes for mechanical engineering", "tech": ["Python", "CAD", "Automation"], "icon": "⚙️"},
            {"name": "Language Detection", "description": "NLP system for automatic language detection", "tech": ["NLP", "Python", "ML"], "icon": "🗣️"},
            {"name": "Soccer Player using Unity ML", "description": "Reinforcement learning trained soccer player in Unity", "tech": ["Unity", "ML", "Reinforcement Learning"], "icon": "⚽"}
        ]
        
        cols = st.columns(2)
        
        for i, project in enumerate(projects):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="project-card">
                    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                        <span style="font-size: 2rem; margin-right: 1rem;">{project['icon']}</span>
                        <h4 style="color: #2c3e50; margin: 0; font-size: 1.3rem;">{project['name']}</h4>
                    </div>
                    <p style="color: #666; margin-bottom: 1.5rem; font-size: 1rem; line-height: 1.6;">{project['description']}</p>
                    <div style="margin-top: 1rem;">
                """, unsafe_allow_html=True)
                
                for tech in project['tech']:
                    st.markdown(f'<span class="skill-pill" style="font-size: 0.8rem; padding: 0.4rem 1rem;">{tech}</span>', unsafe_allow_html=True)
                
                st.markdown("</div></div>", unsafe_allow_html=True)

    # Education Page
    elif selected_nav == "🎓 Education":
        st.markdown('<h1 class="main-header">🎓 Education & Certifications</h1>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="experience-card">
                <h3 style='color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 1rem; margin-bottom: 2rem;'>🎓 Education</h3>
                
                <div style='margin-bottom: 2rem; padding: 1.5rem; background: rgba(255,255,255,0.5); border-radius: 15px; border-left: 4px solid #3498db;'>
                    <h4 style='color: #2c3e50; margin-bottom: 0.5rem; font-size: 1.3rem;'>Bachelor of Technology, Mechanical Engineering</h4>
                    <p style='color: #3498db; margin: 0; font-weight: 600;'>Shri Mata Vaishno Devi University</p>
                    <p style='color: #666; margin-top: 0.5rem;'>🎓 Graduated: May 2024</p>
                </div>

                <div style='margin-bottom: 2rem; padding: 1.5rem; background: rgba(255,255,255,0.5); border-radius: 15px; border-left: 4px solid #3498db;'>
                    <h4 style='color: #2c3e50; margin-bottom: 0.5rem; font-size: 1.3rem;'>Intermediate, Science</h4>
                    <p style='color: #3498db; margin: 0; font-weight: 600;'>Sri Chaitanya Junior College, Amsenpur</p>
                    <p style='color: #666; margin-top: 0.5rem;'>🎓 Completed: March 2020</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="experience-card" style="height: 100%;">
                <h3 style='color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 1rem; margin-bottom: 2rem;'>📜 Certifications</h3>
                
                <div style="max-height: 500px; overflow-y: auto; padding-right: 10px;">
            """, unsafe_allow_html=True)
            
            # Certifications list
            certifications = [
                "Professional Machine Learning Engineer Study Guide - Google Cloud Skills Boost · 2025",
                "Crash Course: Docker For Absolute Beginners - KodeKloud · 2025",
                "Crash Course: Kubernetes For Absolute Beginners - KodeKloud · 2025",
                "Mastering Retrieval-Augmented Generation (RAG) - Neo4j · 2025",
                "Jenkins - KodeKloud · 2024",
                "British Airways - Data Science Job Simulation - Forage · 2023",
                "Cypher Fundamentals - Neo4j · 2023",
                "Neo4j Fundamentals - Neo4j · 2023",
                "GIT for Beginners - KodeKloud · 2023",
                "W&B 101 - United Latino Students Association · 2023"
            ]
            
            for cert in certifications:
                st.markdown(f"• {cert}")
            
            st.markdown("</div></div>", unsafe_allow_html=True)

    # Skills Page
    elif selected_nav == "🛠️ Skills":
        st.markdown('<h1 class="main-header">🛠️ Skills & Expertise</h1>', unsafe_allow_html=True)
        
        # Industry Knowledge
        st.markdown('<h2 class="section-header">🏭 Industry Knowledge</h2>', unsafe_allow_html=True)
        
        industry_skills = [
            "CAD/CAM", "Kubernetes", "Cloud-Native Applications", 
            "CI/CD", "Version Control", "Data Structures", 
            "Computer Science", "Statistical Analysis", "Data Engineering", 
            "MLOps", "Artificial Intelligence (AI)", "Image Processing", 
            "Data Visualization", "Computer Vision", "Machine Learning", "Data Science"
        ]
        
        for skill in industry_skills:
            st.markdown(f'<span class="skill-pill">{skill}</span>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Tools & Technologies
        st.markdown('<h2 class="section-header">⚙️ Tools & Technologies</h2>', unsafe_allow_html=True)
        
        tech_skills = [
            "Django", "Google Cloud Platform (GCP)", "GitHub", "Git", "Docker", 
            "Tableau", "NoSQL", "Linux", "Keras", "SQL", "Flask", 
            "Python", "Pandas", "TensorFlow", "MATLAB", "C"
        ]
        
        for skill in tech_skills:
            st.markdown(f'<span class="skill-pill">{skill}</span>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Interpersonal Skills
        st.markdown('<h2 class="section-header">🤝 Interpersonal Skills</h2>', unsafe_allow_html=True)
        
        interpersonal_skills = [
            "Oral Communication", "Analytical Skills", "Problem Solving", 
            "Multitasking", "Writing"
        ]
        
        for skill in interpersonal_skills:
            st.markdown(f'<span class="skill-pill">{skill}</span>', unsafe_allow_html=True)

    # Contact Page
    elif selected_nav == "📞 Contact":
        st.markdown('<h1 class="main-header">📞 Contact Me</h1>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="contact-form">
                <h3 style='color: #2c3e50; margin-bottom: 2rem; text-align: center;'>💬 Let's Connect</h3>
                <p style='color: #666; line-height: 1.8; margin-bottom: 2.5rem; text-align: center; font-size: 1.1rem;'>
                I'm always open to discussing new opportunities, interesting projects, 
                or potential collaborations. Feel free to reach out!
                </p>
                
                <div style='margin-bottom: 2.5rem;'>
                    <h4 style='color: #2c3e50; margin-bottom: 1.5rem; text-align: center;'>📧 Contact Information</h4>
                    <div style="text-align: center;">
                        <p style='color: #555; font-size: 1.1rem;'><strong>Email:</strong> shiveshraj5902@gmail.com</p>
                        <p style='color: #555; font-size: 1.1rem;'><strong>LinkedIn:</strong> linkedin.com/in/shivesh-raj-bldb3bl51</p>
                    </div>
                </div>
                
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; color: white; text-align: center;'>
                    <h4 style='color: white; margin-bottom: 1rem;'>🚀 Availability</h4>
                    <p style='color: white; margin: 0; font-size: 1.1rem;'>Open to new opportunities and collaborations</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            with st.form("contact_form", clear_on_submit=True):
                st.markdown("### 📝 Send me a message")
                
                name = st.text_input("👤 Your Name", placeholder="Enter your full name")
                email = st.text_input("📧 Your Email", placeholder="Enter your email address")
                subject = st.text_input("📋 Subject", placeholder="What's this about?")
                message = st.text_area("💬 Message", height=150, placeholder="Your message here...")
                
                submitted = st.form_submit_button("🚀 Send Message")
                
                if submitted:
                    if name and email and message:
                        # Simple email simulation (replace with actual email service)
                        st.success("🎉 Thank you for your message! I'll get back to you soon.")
                        
                        # Display the message details (for demo purposes)
                        st.info(f"""
                        **Message Preview:**
                        - **From:** {name}
                        - **Email:** {email}
                        - **Subject:** {subject}
                        - **Message:** {message[:100]}...
                        """)
                    else:
                        st.error("❌ Please fill in all required fields (Name, Email, Message).")
        
        # Involvement section
        st.markdown("---")
        st.markdown('<h2 class="section-header">🌍 Involvement</h2>', unsafe_allow_html=True)
        
        involvement = [
            {"role": "Translator", "organization": "Khan Academy", "duration": "November 2020 – July 2022", "icon": "📚"},
            {"role": "Member", "organization": "Google Developer Student Clubs", "duration": "November 2020 – Present", "icon": "👥"},
            {"role": "Instructor", "organization": "AI Circle SMVDU", "duration": "September 2021 – Present", "icon": "👨‍🏫"},
            {"role": "Secretary", "organization": "Automation and Emerging Technologies (AET club) SMVDU", "duration": "September 2022 – Present", "icon": "📋"},
            {"role": "Instructor", "organization": "DEVs Dungeon", "duration": "March 2021 – Present", "icon": "💻"},
            {"role": "Student Ambassador", "organization": "Streamlit", "duration": "January 2023 – Present", "icon": "🎓"},
            {"role": "Discord Moderator", "organization": "Streamlit", "duration": "February 2023 – Present", "icon": "💬"}
        ]
        
        cols = st.columns(2)
        for i, inv in enumerate(involvement):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="project-card">
                    <div style="display: flex; align-items: center;">
                        <span style="font-size: 2rem; margin-right: 1rem;">{inv['icon']}</span>
                        <div>
                            <h5 style='color: #2c3e50; margin: 0; font-size: 1.2rem;'>{inv['role']}</h5>
                            <p style='color: #3498db; margin: 0.2rem 0; font-size: 1rem; font-weight: 600;'>{inv['organization']}</p>
                            <p style='color: #666; margin: 0; font-size: 0.9rem;'>{inv['duration']}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # Close main content container
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align: center; color: white; padding: 3rem;'>
    <p style='font-size: 1.2rem; font-weight: 300;'>© 2024 Shivesh Raj. All rights reserved. | Built with ❤️ using Streamlit</p>
    <div style='margin-top: 1.5rem;'>
        <span style='margin: 0 1rem; font-size: 2rem;'>🚀</span>
        <span style='margin: 0 1rem; font-size: 2rem;'>💻</span>
        <span style='margin: 0 1rem; font-size: 2rem;'>☁️</span>
        <span style='margin: 0 1rem; font-size: 2rem;'>🤖</span>
    </div>
</div>
""", unsafe_allow_html=True)