import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta, date
from streamlit_option_menu import option_menu
import numbers
import decimal
import graphviz
import pytz

st.set_page_config(
    page_title="Snowflake Enterprise Analytics",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'date_range' not in st.session_state:
    st.session_state.date_range = 'last_7_days'
if 'start_date' not in st.session_state:
    st.session_state.start_date = datetime.now().date() - timedelta(days=7)
if 'end_date' not in st.session_state:
    st.session_state.end_date = datetime.now().date()

st.markdown(
    """
    <style>
        .css-18e3th9 {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        header, .block-container {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Corporate Dashboard Styling
def load_corporate_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700;800&display=swap');

    :root {
        --blue: #1e3a8a;
        --blue-light: #3b82f6;
        --blue-dark: #1e40af;
        --gray-50: #f9fafb;
        --gray-100: #f3f4f6;
        --gray-200: #e5e7eb;
        --gray-300: #d1d5db;
        --gray-400: #9ca3af;
        --gray-500: #6b7280;
        --gray-600: #4b5563;
        --gray-700: #374151;
        --gray-800: #1f2937;
        --gray-900: #111827;
        --green: #065f46;
        --red: #991b1b;
        --orange: #c2410c;
        --shadow: 0 1px 3px rgba(0,0,0,0.1);
        --shadow-md: 0 4px 6px rgba(0,0,0,0.12);
        --shadow-lg: 0 10px 20px rgba(0,0,0,0.15);
    }

    body, [class*="block-container"] {
        font-family: 'IBM Plex Sans', sans-serif !important;
        background: var(--gray-50) !important;
    }

    /* Reset & Base */
    #MainMenu, footer, header, .stDeployButton {
        display: none !important;
        visibility: hidden !important;
    }
    
    .main .block-container {
        padding: 0;
        max-width: 100%;
        background: var(--corporate-gray-50);
        min-height: 100vh;
        font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Option menu link styles */
    .nav-link {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 14px;
        font-weight: 500;
        padding: 12px 20px !important;
        border-radius: 8px !important;
        margin: 4px 8px !important;
        color: #374151 !important; /* gray-700 */
        background-color: transparent !important;
        transition: background-color 0.3s ease, color 0.3s ease !important;
    }

    /* Hover effect */
    .nav-link:hover {
        background-color: #e0e7ff !important;  /* light blue hover */
        color: #1e3a8a !important;
        font-weight: 600 !important;
    }

    /* Selected tab styling */
    .nav-link-selected {
        background-color: #1e3a8a !important;  /* corporate blue */
        color: white !important;
        font-weight: 700 !important;
        border-left: 4px solid #3b82f6 !important;  /* corporate-blue-light */
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }

    .corporate-header {
        background: linear-gradient(120deg, var(--blue) 0%, var(--blue-light) 100%);
        padding: 0rem 1.5rem; /* reduced padding */
        margin-top: 0 !important;
        padding-top: 0 !important;
        margin-bottom: 1.5rem; 
        border-radius: 1rem;
        box-shadow: var(--shadow-lg);
        position: relative;
        overflow: hidden;
    }

    .corporate-header::before, .corporate-header::after {
        content: '';
        position: absolute;
        border-radius: 50%;
        background: rgba(255,255,255,0.08);
        animation: float 12s linear infinite;
    }
    .corporate-header::before { width: 200px; height: 200px; top: -60px; right: -60px; }
    .corporate-header::after { width: 150px; height: 150px; bottom: -40px; left: -50px; }

    @keyframes float {
        0%,100% { transform: translate(0,0); }
        50% { transform: translate(20px,-20px); }
    }

    .corporate-header h1 {
        font-size: 1.75rem; /* smaller font size */
        font-weight: 700; 
        margin: 0;
        background: linear-gradient(90deg, #fff, #e0f2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .corporate-header p {
        font-size: 0.9rem;
        color: rgba(255,255,255,0.9);
        margin-top: 0.5rem;
    }

    .header-stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(125px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
    .header-stat {
        background: rgba(255,255,255,0.12);
        backdrop-filter: blur(5px);
        border-radius: 0.75rem;
        text-align: center;
        padding: 1rem;
        transition: transform .3s ease, background .3s ease;
    }
    .header-stat:hover {
        background: rgba(255,255,255,0.18);
        transform: translateY(-4px);
    }
    .header-stat .value {
        font-size: 1.25rem;
        font-weight: 700;
        color: #fff;
    }
    .header-stat .label {
        font-size: 0.75rem;
        color: rgba(255,255,255,0.7);
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }

    .header-stat {
        text-align: center;
    }

    .header-stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.25rem;
        display: block;
    }

    .header-stat-label {
        font-size: 0.875rem;
        color: rgba(255, 255, 255, 0.7);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 500;
    }

    /* Corporate Card System */
    .corporate-card {
        background: white;
        border: 1px solid var(--corporate-gray-200);
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow-corporate);
        transition: all 0.2s ease;
        position: relative;
    }
    
    .corporate-card:hover {
        box-shadow: var(--shadow-corporate-md);
        border-color: var(--corporate-gray-300);
    }

    .corporate-card-header {
        display: flex;
        align-items: center;
        justify-content: between;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--corporate-gray-100);
    }

    .corporate-card-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--corporate-gray-900);
        margin: 0;
        font-family: 'IBM Plex Sans', sans-serif;
    }

    /* Metric Cards Grid */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); /* reduced min width */
        gap: 1.25rem; /* slightly reduced gap */
    }

    /* Smaller Metric Boxes */
    .metric-card-corporate {
        background: #fff;
        border: 1px solid var(--gray-200);
        border-left: 4px solid var(--blue);
        border-radius: 0.75rem;
        padding: 0.5rem 0.75rem;  /* reduced padding */
        box-shadow: var(--shadow);
        transition: transform .2s ease, box-shadow .2s ease;
        min-width: 0;  /* allow shrinking */
    }
    
    .metric-card-corporate.success {
        border-left-color: var(--green);
    }
    
    .metric-card-corporate.warning {
        border-left-color: var(--orange);
    }
    
    .metric-card-corporate.danger {
        border-left-color: var(--red);
    }
    
    .metric-card-corporate:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-md);
    }

    /* Smaller font sizes to fit content */
    .metric-header {
        display: flex;
        align-items: center;
        justify-content: flex-start;   
        gap: 0.4rem; /* slightly reduced gap */
        margin-bottom: 0.5rem; /* reduced margin */
    }

    .metric-icon {
        background: var(--blue);
        width: 28px;  /* smaller icon */
        height: 28px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 6px;
        font-size: 1rem;  /* smaller font */
        color: white;
        margin-right: 0.4rem;
    }

    .metric-icon.success { background: var(--green); }
    .metric-icon.warning { background: var(--orange); }
    .metric-icon.danger { background: var(--red); }

    .metric-title-corporate {
        font-size: 0.75rem; /* smaller title font */
        color: var(--gray-600);
        text-transform: uppercase;
        font-weight: 600;
    }

    .metric-value-corporate {
        font-size: 1.25rem; /* smaller main value font */
        font-weight: 700;
        color: var(--gray-900);
        display: flex;
        align-items: baseline;
        gap: 0.3rem;
        margin-top: 0.3rem;
    }

    .metric-main-value {
        flex-shrink: 1;
        min-width: 0;
    }

    .metric-change {
        font-size: 0.7rem; /* smaller change font */
        font-weight: 600;
    }

    /* Responsive adjustments */
    @media (max-width: 1024px) {
        .metric-value-corporate {
            font-size: 1.5rem;   /* smaller on medium screens */
        }
    }

    @media (max-width: 1024px) {
        .metric-value-corporate {
            font-size: 1.1rem;   /* smaller on medium */
        }
        .metrics-grid {
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 1rem;
        }
    }
    }
    @media (max-width: 768px) {
        .corporate-header {
            padding: 1.5rem;
        }
        .corporate-header h1 {
            font-size: 1.75rem;
        }
        .header-stats {
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
        }
        .metric-value-corporate {
            font-size: 1rem;
        }
        .metrics-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
    }



    .metric-change.positive { color: var(--green); }
    .metric-change.negative { color: var(--red); }
    .metric-change.neutral { color: var(--corporate-gray-500); }

    /* Chart Container */
    .chart-container-corporate {
        background: white;
        border: 1px solid var(--corporate-gray-200);
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow-corporate);
        transition: all 0.2s ease;
    }

    .chart-container-corporate:hover {
        box-shadow: var(--shadow-corporate-md);
    }

    .chart-header-corporate {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--corporate-gray-100);
    }

    .chart-title-corporate {
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--corporate-gray-900);
        margin: 0;
        font-family: 'IBM Plex Sans', sans-serif;
    }

    .chart-subtitle {
        font-size: 0.875rem;
        color: var(--corporate-gray-500);
        margin: 0.25rem 0 0 0;
        font-weight: 400;
    }

    /* Section Headers */
    .section-header-corporate {
        font-size: 1.2rem;
        font-weight: 700;
        color: var(--gray-900);
        margin: 0rem 0 1rem 0;
        padding-left: 1rem;
        position: relative;
    }
    .section-header-corporate::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 5px;
        background: linear-gradient(180deg, var(--blue), var(--blue-light));
        border-radius: 3px;
    }

    /* Layout Grid */
    .dashboard-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
        margin-bottom: 2rem;
    }

    .dashboard-grid-3 {
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: 1.5rem;
        margin-bottom: 2rem;
    }

    .full-width {
        grid-column: 1 / -1;
    }

    /* Status Indicators */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        padding: 0.375rem 0.75rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .status-indicator.active {
        background: rgba(5, 95, 70, 0.1);
        color: var(--corporate-green);
        border: 1px solid rgba(5, 95, 70, 0.2);
    }
    
    .status-indicator.inactive {
        background: rgba(194, 65, 12, 0.1);
        color: var(--corporate-orange);
        border: 1px solid rgba(194, 65, 12, 0.2);
    }
    
    .status-indicator.critical {
        background: rgba(153, 27, 27, 0.1);
        color: var(--corporate-red);
        border: 1px solid rgba(153, 27, 27, 0.2);
    }

    /* Tables */
    .dataframe {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 0.875rem;
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 8px;
        overflow: hidden;
        background: white;
        box-shadow: var(--shadow-corporate);
        border: 1px solid var(--corporate-gray-200);
        margin-top: 1rem;
    }
    
    .dataframe th {
        background: var(--corporate-gray-50);
        color: var(--corporate-gray-700);
        font-weight: 600;
        font-size: 0.75rem;
        padding: 1rem;
        text-align: left;
        border-bottom: 1px solid var(--corporate-gray-200);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .dataframe td {
        padding: 1rem;
        border-bottom: 1px solid var(--corporate-gray-100);
        color: var(--corporate-gray-700);
        font-weight: 400;
    }

    .dataframe tr:hover {
        background: var(--corporate-gray-50);
    }

    /* Responsive Design */
    @media (max-width: 1024px) {
        .dashboard-grid {
            grid-template-columns: 1fr;
        }
        .dashboard-grid-3 {
            grid-template-columns: 1fr;
        }
        .metrics-grid {
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        }
    }

    @media (max-width: 768px) {
        .corporate-header {
            padding: 1.5rem;
        }
        .corporate-header h1 {
            font-size: 1.75rem;
        }
        .header-stats {
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
        }
        .metric-value-corporate {
            font-size: 1.75rem;
        }
        .metrics-grid {
            grid-template-columns: 1fr;
        }
    }

    /* Loading Animation */
    @keyframes pulse-corporate {
        0%, 100% { 
            opacity: 1; 
            transform: scale(1);
        }
        50% { 
            opacity: 0.8; 
            transform: scale(0.98);
        }
    }
    
    .loading-corporate {
        animation: pulse-corporate 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--corporate-gray-100);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--corporate-gray-400);
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--corporate-gray-500);
    }

    /* Focus States for Accessibility */
    .corporate-card:focus-within,
    .metric-card-corporate:focus-within {
        outline: 2px solid var(--corporate-blue);
        outline-offset: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

load_corporate_css()

CORPORATE_COLORS = {
    'primary': '#1e3a8a',
    'primary_light': '#3b82f6', 
    'success': '#065f46',
    'warning': '#c2410c',
    'danger': '#991b1b',
    'gray_600': '#4b5563',
    'gray_700': '#374151',
    'gray_800': '#1f2937'
}

CORPORATE_CHART_COLORS = [
    '#1e3a8a', '#065f46', '#c2410c', '#991b1b', '#d97706',
    '#7c3aed', '#db2777', '#0891b2', '#059669', '#1d4ed8'
]

CORPORATE_COLORS = {
    'primary': '#1e3a8a',
    'primary_light': '#3b82f6', 
    'success': '#065f46',
    'warning': '#c2410c',
    'danger': '#991b1b',
    'gray_600': '#4b5563',
    'gray_700': '#374151',
    'gray_800': '#1f2937'
}

CORPORATE_CHART_COLORS = [
    '#1e3a8a', '#065f46', '#c2410c', '#991b1b', '#d97706',
    '#7c3aed', '#db2777', '#0891b2', '#059669', '#1d4ed8'
]

conn = st.connection("snowflake")

def render_corporate_header(title, subtitle, stats=None, image_path=None):
    #col1, col2 = st.columns([5, 1])  # Adjust column width ratio as needed

    #with col1:
    stats_html = ""
    if stats:
        stats_html = '<div class="header-stats">'
        for stat in stats:
            stats_html += f"""
                <div class="header-stat">
                    <div class="value">{stat['value']}</div>
                    <div class="label">{stat['label']}</div>
                </div>
            """
        stats_html += "</div>"

    st.markdown(f"""
        <div class="corporate-header">
            <h1>❄️ {title}</h1>
            <p>{subtitle}</p>
            {stats_html}
        </div>
        """, unsafe_allow_html=True)

    #with col2:
            #st.image("assets/cost_sense.png", width=120)
   

def render_corporate_metric_card(title, value, icon, color_class="primary", change=None, format_type="number",
                                value_font_size=None, change_font_size=None, change_translate_y=None):
    
    color_map = {
        "primary": "#1e3a8a",
        "success": "#065f46",
        "warning": "#c2410c",
        "danger": "#991b1b",
        "info": "#3b82f6"
    }
    icon_bg_color = color_map.get(color_class, "#1e3a8a")  # fallback to primary

    # Format value
    if format_type == "currency":
        display_value = f"${value:,.2f}" if isinstance(value, numbers.Number) else str(value)
    elif format_type == "percentage":
        display_value = f"{value:.1f}%" if isinstance(value, numbers.Number) else str(value)
    elif format_type == "number":
        display_value = f"{value:,.1f}" if isinstance(value, float) and value % 1 != 0 else f"{int(value):,}" if isinstance(value, numbers.Number) else str(value)
    else:
        display_value = str(value)

    # Format change badge for absolute change (no % sign)
    change_html = ""
    if change is not None:
        change_class = "positive" if change > 0 else "negative" if change < 0 else "neutral"
        change_icon = "↗" if change > 0 else "↘" if change < 0 else "→"
        change_style = ""
        if change_font_size:
            change_style += f"font-size:{change_font_size};"
        if change_translate_y:
            change_style += f"transform: translateY({change_translate_y});"
        change_html = f'<div class="metric-change {change_class}" style="{change_style}">{change_icon} {abs(change):,.1f}</div>'

    value_style = f"style='font-size:{value_font_size};'" if value_font_size else ""

    # Return HTML for metric card with icon and title side by side, value and change below title
    return f"""
    <div class="metric-card-corporate {color_class}">
        <div class="metric-header" style="display:flex; align-items:center;">
            <div class="metric-icon" style="
                background:{icon_bg_color};
                color:white;
                font-size:1.25rem;
                width:40px;
                height:40px;
                border-radius:50%;
                display:flex;
                align-items:center;
                justify-content:center;
            ">{icon}</div>
            <div class="metric-title-corporate" style="margin-left:0.75rem; display:flex; flex-direction: column;">
                <div>{title}</div>
                <div class="metric-value-corporate" style="margin-top:0.5rem;">
                    <span class="metric-main-value" {value_style}>{display_value}</span>
                    {change_html}
    </div>
    """

def configure_corporate_chart(fig, title="", subtitle=""):
    fig.update_layout(
        title={
            'text': f"<b>{title}</b><br><sub>{subtitle}</sub>" if subtitle else f"<b>{title}</b>",
            'x': 0,
            'xanchor': 'left',
            'font': {'size': 14, 'color': CORPORATE_COLORS['gray_800'], 'family': 'IBM Plex Sans'}
        },
        plot_bgcolor='rgba(249, 250, 251, 0.5)',
        paper_bgcolor='white',
        font={'family': 'IBM Plex Sans', 'color': CORPORATE_COLORS['gray_700'], 'size': 11},
        margin=dict(l=40, r=40, t=60, b=40),
        colorway=CORPORATE_CHART_COLORS,
        
    )

    if any(isinstance(trace, go.Pie) for trace in fig.data):
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont_size=12,
            hovertemplate='<b>%{label}</b><br>Value: %{value}<extra></extra>'
        )
        fig.update_layout(height=400, showlegend=True)
    elif any(isinstance(trace, go.Bar) for trace in fig.data):
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
        fig.update_xaxes(showgrid=False)
        if any(trace.orientation == 'h' for trace in fig.data):
            fig.update_layout(yaxis=dict(autorange="reversed"))
    elif any(isinstance(trace, go.Scatter) for trace in fig.data):
        fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
        fig.update_traces(mode='lines+markers', marker=dict(size=6), line=dict(width=3))
    return fig

def safe_get_first_value(df, column, default=0):
            if column in df.columns and not df.empty:
                val = df[column].iloc[0]
                if isinstance(val, decimal.Decimal):
                    val = float(val)
                return val
            else:
                return default


def render_hover_sidebar_header(
    
    menu_options=None,
    icons=None,
    default_index=0
    ):
    
    st.markdown(f"""
    <style>
    /* Modern Navigation Container */
    .hover-sidebar {{
        position: sticky;
        top: 0;
        margin: 0;
        padding: 0rem 1.2rem 1.8rem 1.2rem;
        border-radius: 16px;
        background: linear-gradient(180deg, {CORPORATE_COLORS['primary']} 0%, {CORPORATE_COLORS['primary_light']} 100%);
        border-right: 2px solid rgba(255,255,255,0.12);
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        box-shadow: 0 8px 32px rgba(0,0,0,0.12);
        padding-top: 0 !important;
        margin-top: 0 !important;
    }}
    
    /* Modern Title Styling */
    .hover-sidebar h2 {{
        font-size: 1.15rem;
        margin: 0 0 0.4rem 0;
        color: #ffffff;
        font-weight: 700;
        letter-spacing: -0.01em;
        text-align: center;
        line-height: 1.3;
    }}
    
    /* Subtitle Styling */
    .hover-sidebar p {{
        margin: 0 0 1.5rem 0;
        color: rgba(255,255,255,0.85);
        font-size: 0.8rem;
        text-align: center;
        font-weight: 400;
        line-height: 1.4;
    }}
    
    /* White Rounded Menu Items with Dark Text */
    .hover-sidebar .nav-link {{
        background: rgba(255,255,255,0.95) !important;
        color: #1f2937 !important;
        border-radius: 12px !important;
        margin: 6px 0 !important;
        padding: 12px 16px !important;
        font-size: 0.86rem !important;
        font-weight: 500 !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
        transition: all 0.25s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        position: relative !important;
        display: flex !important;
        align-items: center !important;
    }}
    
    /* Hover Effects - Enhanced White Background */
    .hover-sidebar .nav-link:hover {{
        background: rgba(255,255,255,1) !important;
        color: #111827 !important;
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15) !important;
        border-color: rgba(255,255,255,0.4) !important;
    }}
    
    /* Active/Selected State - Bright White with Strong Shadow */
    .hover-sidebar .nav-link-selected {{
        background: rgba(255,255,255,1) !important;
        color: #111827 !important;
        font-weight: 600 !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2) !important;
        border: 2px solid rgba(255,255,255,0.6) !important;
        transform: translateY(-2px) scale(1.02) !important;
        position: relative !important;
    }}
    
    /* Active item indicator dot */
    .hover-sidebar .nav-link-selected::after {{
        content: '';
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        width: 8px;
        height: 8px;
        background: {CORPORATE_COLORS['primary']};
        border-radius: 50%;
        opacity: 1;
    }}
    
    /* Icon Styling - Dark for White Backgrounds */
    .hover-sidebar .nav-link i {{
        margin-right: 10px !important;
        font-size: 0.95rem !important;
        opacity: 0.8 !important;
        min-width: 16px !important;
        color: #374151 !important;
    }}
    
    /* Selected item icon */
    .hover-sidebar .nav-link-selected i {{
        opacity: 1 !important;
        color: #111827 !important;
    }}
    
    /* Hover state icon */
    .hover-sidebar .nav-link:hover i {{
        opacity: 1 !important;
        color: #111827 !important;
    }}
    
    /* Focus States for Accessibility */
    .hover-sidebar .nav-link:focus {{
        outline: 2px solid {CORPORATE_COLORS['primary']} !important;
        outline-offset: 2px !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15), 0 0 0 3px rgba(59, 130, 246, 0.3) !important;
    }}
    
    /* Text Selection Prevention */
    .hover-sidebar .nav-link {{
        -webkit-user-select: none !important;
        -moz-user-select: none !important;
        -ms-user-select: none !important;
        user-select: none !important;
    }}
    
    /* Menu Container Styling */
    .hover-sidebar > div[data-testid="stVerticalBlock"] {{
        background: transparent !important;
        padding: 0 !important;
    }}
    
    /* Responsive Design */
    @media (max-width: 768px) {{
        .hover-sidebar {{
            padding: 1.5rem 1rem;
            border-radius: 12px;
        }}
        .hover-sidebar .nav-link {{
            padding: 10px 14px !important;
            font-size: 0.84rem !important;
            margin: 4px 0 !important;
        }}
        .hover-sidebar h2 {{
            font-size: 1.05rem;
        }}
    }}
    
    /* Logo Enhancement */
    .sidebar .sidebar-content .block-container img {{
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease;
    }}
    
    .sidebar .sidebar-content .block-container img:hover {{
        transform: scale(1.03);
    }}
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        selected = option_menu(
            menu_title=None,
            options=menu_options,
            icons=icons,
            default_index=default_index,
            styles={
                "container": {"background": "transparent", "padding": "0", "margin": "0"},
                "nav-link": {
                    "font-size": "0.86rem",
                    "font-weight": "500",
                    "background": "rgba(255,255,255,0.95)",
                    "color": "#1f2937",
                    "border-radius": "12px",
                    "margin": "6px 0",
                    "padding": "12px 16px",
                    "border": "1px solid rgba(255,255,255,0.2)",
                    "box-shadow": "0 2px 8px rgba(0,0,0,0.08)",
                    "transition": "all 0.25s cubic-bezier(0.25, 0.8, 0.25, 1)",
                    "display": "flex",
                    "align-items": "center",
                },
                "nav-link-selected": {
                    "background": "rgba(255,255,255,1)",
                    "color": "#111827",
                    "font-weight": "600",
                    "box-shadow": "0 8px 25px rgba(0,0,0,0.2)",
                    "border": "2px solid rgba(255,255,255,0.6)",
                    "transform": "translateY(-2px) scale(1.02)",
                },
                "icon": {
                    "font-size": "0.95rem",
                    "margin-right": "10px",
                    "opacity": "0.8",
                    "min-width": "16px",
                    "color": "#374151",
                }
            }
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    return selected

def render_date_filter():

    st.sidebar.markdown("---")
    #st.sidebar.markdown("###  Date Filter")

    date_option = st.sidebar.selectbox(
        "Select Time Period",
        options=['last_7_days', 'last_month', 'last_3_months', 'last_6_months', 'custom', 'all_time'],
        format_func=lambda x: {
            'last_7_days': 'Last 7 Days',
            'last_month': 'Last Month',
            'last_3_months': 'Last 3 Months',
            'last_6_months': 'Last 6 Months',
            'custom': 'Custom Range',
            'all_time': 'All Time'
        }[x],
        index=0
    )

    end_date = datetime.now().date()

    if date_option == 'last_7_days':
        start_date = end_date - timedelta(days=7)
    elif date_option == 'last_month':
        start_date = end_date - timedelta(days=30)
    elif date_option == 'last_3_months':
        start_date = end_date - timedelta(days=90)
    elif date_option == 'last_6_months':
        start_date = end_date - timedelta(days=180)
    elif date_option == 'all_time':
        start_date = datetime(2020, 1, 1).date() 
    else: 
        st.sidebar.markdown("**Custom Date Range:**")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            start_date = st.date_input(
                "Start",
                value=st.session_state.get('start_date', end_date - timedelta(days=7)),
                max_value=end_date
            )
        with col2:
            end_date = st.date_input(
                "End",
                value=st.session_state.get('end_date', end_date),
                max_value=datetime.now().date()
            )

    st.session_state.start_date = start_date
    st.session_state.end_date = end_date

    days_diff = (end_date - start_date).days
    return start_date, end_date

with st.sidebar:
    st.sidebar.image("assets/Boolean-logo.png", use_container_width=True)
    start_date, end_date = render_date_filter()
    menu_items = ["Dashboard", "Storage", "Warehouse",  "Roles", "Miscellaneous"]
    menu_icons = ['speedometer2','hdd','graph-up','people','file-text']

    selected = render_hover_sidebar_header(
        menu_options=menu_items,
        icons=menu_icons
    )


def account_overview():
    try:
        start_date = st.session_state.start_date
        end_date = st.session_state.end_date

        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')

        env_info = conn.query("SELECT CURRENT_REGION() AS REGION, CURRENT_ACCOUNT() AS ACCOUNT_NAME")

        total_users = conn.query(f"""
            SELECT COUNT(*) AS USERS 
            FROM SNOWFLAKE.ACCOUNT_USAGE.USERS 
            WHERE DELETED_ON IS NULL
            AND CREATED_ON <= '{end_date_str}'
        """)

        total_queries = conn.query(f"""
            SELECT COUNT(QUERY_ID) AS NO_OF_QUERIES 
            FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY 
            WHERE START_TIME >= '{start_date_str}' 
              AND START_TIME <= '{end_date_str}'
        """)

        credits_data = conn.query(f"""
            SELECT SUM(CREDITS_USED) AS TOTAL_CREDITS 
            FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
            WHERE START_TIME >= '{start_date_str}' 
              AND START_TIME <= '{end_date_str}'
        """)

        avg_duration = conn.query(f"""
            SELECT AVG(TOTAL_ELAPSED_TIME/1000) AS AVG_DURATION_SEC
            FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
            WHERE START_TIME >= '{start_date_str}' 
              AND START_TIME <= '{end_date_str}'
        """)

        failed_queries = conn.query(f"""
            SELECT COUNT(*) AS FAILED_COUNT
            FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
            WHERE START_TIME >= '{start_date_str}' 
              AND START_TIME <= '{end_date_str}'
            AND EXECUTION_STATUS = 'FAIL'
        """)

        header_stats = {
            'users': safe_get_first_value(total_users, 'USERS'),
            'queries': safe_get_first_value(total_queries, 'NO_OF_QUERIES'),
            'credits': safe_get_first_value(credits_data, 'TOTAL_CREDITS'),
            'region': env_info.iloc[0]['REGION'] if not env_info.empty else "N/A"
        }

        render_corporate_header(
            "Account Overview",
            f"Comprehensive analysis of your Snowflake environment | {start_date.strftime('%b %d, %Y')} - {end_date.strftime('%b %d, %Y')}",
        )

        st.markdown('<div class="section-header-corporate"> Environment Information</div>', unsafe_allow_html=True)

        large_query_percentage = conn.query(f"""
            SELECT 
                COUNT(*) AS TOTAL,
                COUNT(CASE WHEN (BYTES_WRITTEN_TO_RESULT / 1000000000) > 1 THEN 1 END) AS LARGE,
                COUNT(CASE WHEN (BYTES_WRITTEN_TO_RESULT / 1000000000) <= 1 THEN 1 END) AS SMALL,
                (COUNT(CASE WHEN (BYTES_WRITTEN_TO_RESULT / 1000000000) > 1 THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0)) AS LARGE_QUERY_PERCENTAGE,
                (COUNT(CASE WHEN (BYTES_WRITTEN_TO_RESULT / 1000000000) <= 1 THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0)) AS SMALL_QUERY_PERCENTAGE
            FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
            WHERE START_TIME >= '{start_date_str}' 
              AND START_TIME <= '{end_date_str}'
        """)

        def get_metric_value_for_date(conn, query_template, date):
            query = query_template.format(date=date)
            result = conn.query(query)
            return safe_get_first_value(result, list(result.columns)[0], None) if result is not None else None

        def get_current_and_7day_change(conn, query_template):
            today = date.today()
            seven_days_ago = today - timedelta(days=7)


            current_value = get_metric_value_for_date(conn, query_template, today.strftime('%Y-%m-%d'))
            past_value = get_metric_value_for_date(conn, query_template, seven_days_ago.strftime('%Y-%m-%d'))

            if current_value is None or past_value is None:
                return None, None

            change = current_value - past_value
            return current_value, change

        metric_queries = {
            "active_users": """
                SELECT COUNT(*) AS USERS FROM SNOWFLAKE.ACCOUNT_USAGE.USERS
                WHERE DELETED_ON IS NULL AND OWNER IS NOT NULL
            """,
            "total_roles": """
                SELECT COUNT(*) AS ROLES  FROM SNOWFLAKE.ACCOUNT_USAGE.ROLES
                WHERE DELETED_ON IS NULL AND ROLE_TYPE = 'ROLE'
            """,
            "total_queries_30d": """
                SELECT COUNT(*) AS NO_OF_QUERIES FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
                WHERE START_TIME >= DATEADD(day, -30, DATE '{date}')
                AND START_TIME < DATE '{date}'
            """,
            "avg_query_time": """
                SELECT AVG(TOTAL_ELAPSED_TIME)/1000.0 AS AVG_DURATION_SEC FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
                WHERE START_TIME >= DATEADD(day, -30, DATE '{date}')
                AND START_TIME < DATE '{date}'
            """,
            "failed_queries": """
                SELECT COUNT(*) AS FAILED_COUNT FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
                WHERE START_TIME >= DATEADD(day, -30, DATE '{date}')
                AND START_TIME < DATE '{date}'
                AND EXECUTION_STATUS = 'FAILURE'
            """,
            "large_query_percentage": """
                SELECT 100.0 * SUM(CASE WHEN BYTES_WRITTEN_TO_RESULT > 1000000000 THEN 1 ELSE 0 END)/NULLIF(COUNT(*), 0) AS LARGE_QUERY_PERCENTAGE
                FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
                WHERE START_TIME >= DATEADD(day, -30, DATE '{date}')
                AND START_TIME < DATE '{date}'
            """,
            "small_query_percentage": """
                SELECT 100.0 * SUM(CASE WHEN BYTES_WRITTEN_TO_RESULT <= 1000000000 THEN 1 ELSE 0 END)/NULLIF(COUNT(*), 0) AS SMALL_QUERY_PERCENTAGE
                FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
                WHERE START_TIME >= DATEADD(day, -30, DATE '{date}')
                AND START_TIME < DATE '{date}'
            """,
            "compute_credits": """
                SELECT SUM(CREDITS_USED_COMPUTE) AS COMPUTE_CREDITS
                FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
                WHERE DATE_TRUNC('DAY', START_TIME) = DATE '{date}'
            """,
            "cloud_credits": """
                SELECT SUM(CREDITS_USED_CLOUD_SERVICES) AS CLOUD_CREDITS
                FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
                WHERE DATE_TRUNC('DAY', START_TIME) = DATE '{date}'
            """,
            "total_credits": """
                SELECT SUM(CREDITS_USED) AS TOTAL_CREDITS
                FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
                WHERE DATE_TRUNC('DAY', START_TIME) = DATE '{date}'
            """
        }

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.write(render_corporate_metric_card(
                "Region",
                env_info.iloc[0]['REGION'] if not env_info.empty else "N/A",
                "🗺",
                "primary",
                change=None,
                format_type="number",
                value_font_size="1.2rem"
            ), unsafe_allow_html=True)

        with col2:
            st.markdown(render_corporate_metric_card(
                "Account Name",
                env_info.iloc[0]['ACCOUNT_NAME'] if not env_info.empty else "Unknown",
                "🏷",
                "primary",
                change=None,
                format_type="number",
                value_font_size="1.2rem"
            ), unsafe_allow_html=True)

        with col3:
            current_users, change_users = get_current_and_7day_change(conn, metric_queries["active_users"])
            st.markdown(render_corporate_metric_card(
                "Active Users",
                current_users if current_users is not None else safe_get_first_value(total_users, 'USERS'),
                "🧑‍🚀",
                "primary",
                change=None,
                format_type="number"
            ), unsafe_allow_html=True)

        with col4:
            current_roles, change_roles = get_current_and_7day_change(conn, metric_queries["total_roles"])
            st.markdown(render_corporate_metric_card(
                "Total Roles",
                current_roles if current_roles is not None else "N/A",
                "🛡",
                "primary",
                change=None,
                format_type="number"
            ), unsafe_allow_html=True)

        st.markdown('---')
        st.markdown('<div class="section-header-corporate"> Key Performance Metrics</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(render_corporate_metric_card(
                "Total Queries",
                safe_get_first_value(total_queries, 'NO_OF_QUERIES'),
                "❄",
                "primary",
                change=None,
                format_type="number"
            ), unsafe_allow_html=True)
        with col2:
            avg_time_val = safe_get_first_value(avg_duration, 'AVG_DURATION_SEC')
            st.markdown(render_corporate_metric_card(
                "Avg Query Time (sec)",
                round(avg_time_val, 1) if avg_time_val else 0,
                "⏱",
                "primary",
                change=None,
                format_type="number"
            ), unsafe_allow_html=True)
        with col3:
            st.markdown(render_corporate_metric_card(
                "Failed Queries",
                safe_get_first_value(failed_queries, 'FAILED_COUNT'),
                "⚠",
                "danger",
                change=None,
                format_type="number"
            ), unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('---')
        st.markdown('<div class="section-header-corporate"> Credit Breakdown</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        credits_breakdown = conn.query(f"""
            SELECT 
                SUM(CREDITS_USED_COMPUTE) AS COMPUTE_CREDITS,
                SUM(CREDITS_USED_CLOUD_SERVICES) AS CLOUD_CREDITS,
                SUM(CREDITS_USED) AS TOTAL_CREDITS
            FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
            WHERE START_TIME >= '{start_date_str}' 
              AND START_TIME <= '{end_date_str}'
        """)

        with col1:
            compute_val = safe_get_first_value(credits_breakdown, 'COMPUTE_CREDITS')
            st.markdown(render_corporate_metric_card(
                "Compute Credits",
                round(compute_val, 2) if compute_val else 0,
                "⚙",
                "primary",
                change=None,
                format_type="number"
            ), unsafe_allow_html=True)
        with col2:
            cloud_val = safe_get_first_value(credits_breakdown, 'CLOUD_CREDITS')
            st.markdown(render_corporate_metric_card(
                "Cloud Service Credits",
                round(cloud_val, 2) if cloud_val else 0,
                "☁",
                "primary",
                change=None,
                format_type="number"
            ), unsafe_allow_html=True)
        with col3:
            total_val = safe_get_first_value(credits_data, 'TOTAL_CREDITS')
            st.markdown(render_corporate_metric_card(
                "Total Credits Used",
                round(total_val, 2) if total_val else 0,
                "💳",
                "primary",
                change=None,
                format_type="number"
            ), unsafe_allow_html=True)

        st.markdown('---')
        st.markdown('<div class="section-header-corporate"> Performance Analytics</div>', unsafe_allow_html=True)

        database_storage = conn.query(f"""
            WITH daily AS (
                SELECT
                    database_name,
                    usage_date,
                    MAX(database_id) AS object_id,
                    MAX(AVERAGE_DATABASE_BYTES + AVERAGE_FAILSAFE_BYTES + AVERAGE_HYBRID_TABLE_STORAGE_BYTES) AS database_storage_bytes
                FROM snowflake.account_usage.database_storage_usage_history
                WHERE usage_date >= TO_TIMESTAMP_LTZ('{start_date_str}', 'auto')
                    AND usage_date <  TO_TIMESTAMP_LTZ('{end_date_str}',   'auto')
                GROUP BY database_name, usage_date
                )
                SELECT
                database_name,
                ROUND(AVG(database_storage_bytes) / 1000000000, 2) AS STORAGE_GB
                FROM daily
                GROUP BY database_name
                ORDER BY STORAGE_GB DESC
                LIMIT 10;
        """)

        credits_trend = conn.query(f"""
            SELECT DATE(START_TIME) AS usage_date, SUM(CREDITS_USED) AS daily_credits
            FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
            WHERE START_TIME >= '{start_date_str}' 
              AND START_TIME <= '{end_date_str}'
            GROUP BY DATE(START_TIME)
            ORDER BY usage_date
        """)

        col1, col2 = st.columns(2)

        chart_height = 400

        container_style = """
            background: #fff;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            padding: 1rem;
        """

        BASE_COLORS = [
            "#1f77b4",  # Blue
            "#ff7f0e",  # Orange
            "#2ca02c",  # Green
            "#d62728",  # Red
            "#9467bd",  # Purple
            "#8c564b",  # Brown
            "#e377c2",  # Pink
            "#7f7f7f",  # Gray
            "#bcbd22",  # Olive
            "#17becf",  # Cyan
        ]

        # Function to slightly lighten/darken a hex color for gradient effect
        def adjust_color(hex_color, factor=0.8):
            hex_color = hex_color.lstrip('#')
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            r = min(int(r * factor), 255)
            g = min(int(g * factor), 255)
            b = min(int(b * factor), 255)
            return f'#{r:02x}{g:02x}{b:02x}'

        # Generate gradient colors for slices
        gradient_colors = []
        for i, color in enumerate(BASE_COLORS):
            gradient_colors.append(adjust_color(color, factor=0.85))
            gradient_colors.append(adjust_color(color, factor=1.1))  # slightly lighter

        with col1:
            st.markdown(f'<div style="{container_style}">Database Storage Distribution</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            database_storage.columns = [col.upper() for col in database_storage.columns]
            if not database_storage.empty:
                # Bright & Bold Professional Palette
                snowflake_colors = ['#4F46E5', '#7C3AED', '#EC4899', '#F59E0B', '#10B981', 
                                '#3B82F6', '#8B5CF6', '#EF4444', '#06B6D4', '#14B8A6']
                
                # Calculate percentage for each database
                total_storage = database_storage['STORAGE_GB'].sum()
                database_storage['PERCENTAGE'] = (database_storage['STORAGE_GB'] / total_storage * 100).round(2)
                
                # Sort by storage for better visualization
                database_storage_sorted = database_storage.sort_values('STORAGE_GB', ascending=True)
                
                # Create a display value with minimum bar width for visibility
                max_storage = database_storage_sorted['STORAGE_GB'].max()
                min_visible_width = max_storage * 0.02  # Minimum 2% of max for visibility
                database_storage_sorted['DISPLAY_VALUE'] = database_storage_sorted['STORAGE_GB'].apply(
                    lambda x: max(x, min_visible_width) if x > 0 else x
                )
                
                fig_storage = px.bar(
                    database_storage_sorted,
                    x='DISPLAY_VALUE',  # Use display value instead of actual storage
                    y='DATABASE_NAME',
                    orientation='h',  # Horizontal bar chart
                    color='DATABASE_NAME',
                    color_discrete_sequence=snowflake_colors[:len(database_storage)],
                    custom_data=['STORAGE_GB', 'PERCENTAGE']  # Pass actual values for hover
                )

                fig_storage.update_traces(
                    hovertemplate="<b>%{y}</b><br>Storage: %{customdata[0]:.2f} GB (%{customdata[1]:.2f}%)<extra></extra>",
                    marker=dict(line=dict(color='white', width=2))
                )
                
                # Create annotations for percentages aligned in a single vertical line
                annotations = []
                for idx, row in database_storage_sorted.iterrows():
                    annotations.append(
                        dict(
                            x=max_storage * 1.05,  # Fixed x position for all percentages
                            y=row['DATABASE_NAME'],
                            text=f"{row['PERCENTAGE']:.2f}%",
                            showarrow=False,
                            xanchor='left',  # Align text to the left from the x position
                            font=dict(size=11, color='#374151', family='Inter, sans-serif', weight='bold')
                        )
                    )
                
                fig_storage.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='Inter, sans-serif', color='#374151', size=12),
                    margin=dict(l=20, r=100, t=40, b=20),  # Increased right margin for percentage labels
                    showlegend=False,  # Removes the legend
                    height=chart_height,
                    xaxis=dict(
                        title='Storage (GB)',
                        showgrid=True,
                        gridcolor='rgba(200, 200, 200, 0.2)',
                        zeroline=False,
                        range=[0, max_storage * 1.2]  # Extend x-axis to accommodate percentage labels
                    ),
                    yaxis=dict(
                        title='',  # Remove y-axis title since database names are self-explanatory
                        showgrid=False
                    ),
                    annotations=annotations  # Add the annotations
                )

                st.plotly_chart(configure_corporate_chart(fig_storage), use_container_width=True)
        with col2:
            st.markdown(f'<div style="{container_style}">Daily Credit Consumption', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            if not credits_trend.empty:
                # Bright indigo for area chart
                fig_credits = px.area(
                    credits_trend, 
                    x='USAGE_DATE', 
                    y='DAILY_CREDITS', 
                    color_discrete_sequence=['#4F46E5']  # Deep indigo
                )
                fig_credits.update_traces(
                    line=dict(width=3, color='#6366F1'),  # Brighter indigo border
                    fillcolor='rgba(79, 70, 229, 0.2)'  # Indigo fill with transparency
                )
                fig_credits.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Credits Used",
                    hovermode="x unified",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='Inter, sans-serif', color='#374151'),
                    margin=dict(l=20, r=20, t=20, b=20),
                    height=chart_height
                )
                st.plotly_chart(configure_corporate_chart(fig_credits), use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        chart_height = 400
        with col1:
            st.markdown(f'<div style="{container_style}">Query Count per User', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            top_users = conn.query(f"""
                SELECT USER_NAME, COUNT(*) AS QUERY_COUNT
                FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
                WHERE START_TIME >= '{start_date_str}' 
                AND START_TIME <= '{end_date_str}'
                AND USER_NAME IS NOT NULL 
                GROUP BY USER_NAME
                ORDER BY QUERY_COUNT DESC
                LIMIT 20
            """)

            if not top_users.empty:
                fig_top_users = px.bar(
                    top_users,
                    y='USER_NAME',
                    x='QUERY_COUNT',
                    orientation='h',
                    title=f"Top 10 Active Users"
                )
                fig_top_users.update_traces(marker_color='#7C3AED')  # Deep purple
                fig_top_users.update_layout(
                    yaxis=dict(autorange='reversed'),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='IBM Plex Sans', color='#374151'),
                    margin=dict(l=100, r=20, t=40, b=20),
                    height=350
                )
                st.plotly_chart(configure_corporate_chart(fig_top_users), use_container_width=True)


        with col2:
            st.markdown(f'<div style="{container_style}"> Daily Login Activity</div>', unsafe_allow_html=True)

            # Fetch all active users
            user_list = conn.query("""
                SELECT DISTINCT NAME
                FROM SNOWFLAKE.ACCOUNT_USAGE.USERS
                WHERE DELETED_ON IS NULL
                ORDER BY NAME
            """)

            # User filter dropdown
            selected_user = None
            if not user_list.empty:
                selected_user = st.selectbox(
                    "Select a user to view login activity:",
                    options=user_list['NAME'].tolist(),
                    index=None,
                    placeholder="Choose a user..."
                )

            if selected_user:
                # Aggregate logins per day
                user_logins = conn.query(f"""
                    SELECT EVENT_TIMESTAMP::DATE AS LOGIN_DATE,
                        COUNT(*) AS LOGIN_COUNT
                    FROM SNOWFLAKE.ACCOUNT_USAGE.LOGIN_HISTORY
                    WHERE USER_NAME = '{selected_user}'
                    AND EVENT_TIMESTAMP::DATE BETWEEN '{st.session_state.start_date}' AND '{st.session_state.end_date}'
                    AND IS_SUCCESS = 'YES'
                    GROUP BY LOGIN_DATE
                    ORDER BY LOGIN_DATE ASC
                """)

                if not user_logins.empty:
                    # Area chart with teal color
                    fig_logins = px.area(
                        user_logins,
                        x='LOGIN_DATE',
                        y='LOGIN_COUNT',
                        color_discrete_sequence=['#14B8A6']  # Bright teal
                    )
                    fig_logins.update_traces(
                        line=dict(width=3, color='#0D9488'),  # Darker teal border
                        fillcolor='rgba(20, 184, 166, 0.2)'
                    )
                    fig_logins.update_layout(
                        xaxis_title="Date",
                        yaxis_title="Number of Logins",
                        hovermode="x unified",
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(family='IBM Plex Sans', color='#374151'),
                        margin=dict(l=20, r=20, t=20, b=20),
                        height=chart_height
                    )
                    st.plotly_chart(configure_corporate_chart(fig_logins), use_container_width=True)
                else:
                    st.info(f"No logins for **{selected_user}** between {st.session_state.start_date} and {st.session_state.end_date}.")
            else:
                st.info("Please select a user to view login activity.")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div style="{container_style}"> Database Usage Details', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            database_detail = conn.query(f"""
                SELECT d.DATABASE_NAME, 
                DATEDIFF(day, MIN(DATE(d.CREATED)), CURRENT_DATE) AS AGE,
                MAX(lq.START_TIME) AS LAST_QUERY_TIME,
                DATEDIFF(day, MAX(lq.START_TIME), CURRENT_TIMESTAMP) AS DAYS_SINCE_LAST_QUERY,
                lq.QUERY_COUNT
            FROM SNOWFLAKE.ACCOUNT_USAGE.DATABASES d
            LEFT JOIN (
                SELECT DATABASE_NAME, MAX(START_TIME) AS START_TIME, COUNT(*) AS QUERY_COUNT
                FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
                WHERE DATABASE_NAME IS NOT NULL
                AND START_TIME >= '{start_date_str}'
                AND START_TIME <= '{end_date_str}'
                GROUP BY DATABASE_NAME
            ) lq ON d.DATABASE_NAME = lq.DATABASE_NAME
            WHERE d.TYPE='STANDARD' AND d.DELETED IS NULL
            AND lq.QUERY_COUNT >= 1
            GROUP BY d.DATABASE_NAME, lq.QUERY_COUNT
            ORDER BY DAYS_SINCE_LAST_QUERY DESC
            LIMIT 10
            """)

            if not database_detail.empty:
                database_detail_sorted = database_detail.sort_values(by='DAYS_SINCE_LAST_QUERY', ascending=False)

                fig_db_detail = px.bar(
                    database_detail_sorted,
                    y='DATABASE_NAME',
                    x='DAYS_SINCE_LAST_QUERY',
                    orientation='h',
                    title="Days Since Last Query per Database"
                )

                fig_db_detail.update_traces(marker_color='#F59E0B')  # Bright amber
                fig_db_detail.update_layout(
                    yaxis=dict(autorange='reversed'),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='IBM Plex Sans', color='#374151'),
                    margin=dict(l=40, r=20, t=40, b=20),
                    height=350
                )

                st.plotly_chart(configure_corporate_chart(fig_db_detail), use_container_width=True)
            else:
                st.info("No database details available for selected period.")

        with col2:
            st.markdown(f'<div style="{container_style}"> Warehouse Credits Consumption', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            warehouse_credits = conn.query(f"""
                SELECT
                WAREHOUSE_NAME,
                SUM(CREDITS_USED) AS TOTAL_CREDITS_USED
                FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
                WHERE START_TIME >= '{start_date_str}' 
                AND START_TIME <= '{end_date_str}'
                GROUP BY WAREHOUSE_NAME
                HAVING SUM(CREDITS_USED) > 0
                ORDER BY TOTAL_CREDITS_USED DESC
                LIMIT 10
            """)

            if not warehouse_credits.empty:
                # Convert Decimal to float to avoid type errors
                warehouse_credits['TOTAL_CREDITS_USED'] = warehouse_credits['TOTAL_CREDITS_USED'].fillna(0).apply(float)
                max_credits = float(warehouse_credits['TOTAL_CREDITS_USED'].max())
                
                fig_warehouse_credits = px.bar(
                    warehouse_credits,
                    x='TOTAL_CREDITS_USED',
                    y='WAREHOUSE_NAME',
                    orientation='h',
                    title=f"Total Credits Consumed by Warehouse",
                    labels={'TOTAL_CREDITS_USED': 'Credits Used', 'WAREHOUSE_NAME': 'Warehouse'}
                )
                fig_warehouse_credits.update_traces(marker_color='#10B981')  # Bright emerald green
                fig_warehouse_credits.update_layout(
                    yaxis=dict(autorange="reversed"),
                    xaxis=dict(range=[0, max_credits * 1.1]),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='IBM Plex Sans', color='#374151'),
                    margin=dict(l=40, r=20, t=40, b=20),
                    height=350
                )
                st.plotly_chart(configure_corporate_chart(fig_warehouse_credits), use_container_width=True)
            else:
                st.info(f"No warehouse credit consumption data available for selected period.")

        st.markdown(f'<div style="{container_style}"> Long-running Queries (>10 mins) Trend', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        long_query_sql = f"""
        SELECT 
        DATE_TRUNC('day', START_TIME) AS QUERY_DAY,
        USER_NAME,
        WAREHOUSE_NAME,
        QUERY_TYPE,
        COUNT(*) AS LONG_QUERIES_COUNT
        FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
        WHERE START_TIME >= '{start_date_str}'
        AND START_TIME <= '{end_date_str}'
        AND TOTAL_ELAPSED_TIME > 600000
        GROUP BY QUERY_DAY, USER_NAME, WAREHOUSE_NAME, QUERY_TYPE
        ORDER BY QUERY_DAY
        """

        long_queries_data = conn.query(long_query_sql)

        if not long_queries_data.empty:
            users = long_queries_data['USER_NAME'].dropna().unique().tolist()
            selected_user = st.selectbox("Filter by User", options=["All"] + users)

            warehouses = long_queries_data['WAREHOUSE_NAME'].dropna().unique().tolist()
            selected_warehouse = st.selectbox("Filter by Warehouse", options=["All"] + warehouses)

            df_filtered = long_queries_data.copy()
            if selected_user != "All":
                df_filtered = df_filtered[df_filtered['USER_NAME'] == selected_user]
            if selected_warehouse != "All":
                df_filtered = df_filtered[df_filtered['WAREHOUSE_NAME'] == selected_warehouse]

            if not df_filtered.empty:
                df_pivot = df_filtered.pivot_table(
                    index='QUERY_DAY',
                    columns='QUERY_TYPE',
                    values='LONG_QUERIES_COUNT',
                    aggfunc='sum',
                    fill_value=0
                ).reset_index()

                df_melted = df_pivot.melt(id_vars='QUERY_DAY', var_name='QUERY_TYPE', value_name='LONG_QUERIES_COUNT')

                # Bright & Bold Professional Palette
                snowflake_colors = ['#4F46E5', '#7C3AED', '#EC4899', '#F59E0B', '#10B981', '#3B82F6', '#8B5CF6', '#EF4444', '#06B6D4', '#14B8A6']
                color_sequence = snowflake_colors * ((df_melted['QUERY_TYPE'].nunique() // len(snowflake_colors)) + 1)

                fig = px.area(
                    df_melted,
                    x='QUERY_DAY',
                    y='LONG_QUERIES_COUNT',
                    color='QUERY_TYPE',
                    color_discrete_sequence=color_sequence,
                    title='Long-running Queries (>10 mins) by Query Type',
                    labels={'LONG_QUERIES_COUNT': 'Query Count', 'QUERY_DAY': 'Date'}
                )

                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='IBM Plex Sans', color='#374151'),
                    margin=dict(l=20, r=20, t=40, b=20),
                    height=400
                )
                st.plotly_chart(configure_corporate_chart(fig), use_container_width=True)
            else:
                st.info("No data found for selected filters.")
        else:
            st.info(f"No long-running queries (>10 mins) found for selected period.")


    except Exception as e:
        st.error(f"⚠️ Error loading dashboard data: {str(e)}")
        st.info("Please check your Snowflake connection and account permissions.")

if selected == "Dashboard":
    account_overview()
elif selected == "Warehouse":
    def warehouse_analytics():
        try:
            # === SESSION DATES ===
            start_date = st.session_state.start_date
            end_date = st.session_state.end_date
            start_date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')

            # === HEADER ===
            render_corporate_header(
                "Warehouse Analytics",
                f"Comprehensive warehouse performance and cost monitoring | {start_date.strftime('%b %d, %Y')} - {end_date.strftime('%b %d, %Y')}",
                None
            )

            # === Helper for alias-safe warehouse filter ===
            def build_wh_filter(alias: str = ""):
                prefix = f"{alias}." if alias else ""
                if selected_warehouse != "All Warehouses":
                    return f"AND {prefix}WAREHOUSE_NAME = '{selected_warehouse}'"
                return ""

            # === SECTION 1: OVERVIEW ===
            st.markdown('<div class="section-header-corporate"> Warehouse Overview</div>', unsafe_allow_html=True)

            warehouse_summary = conn.query(f"""
                SELECT 
                    SUM(CREDITS_USED) AS TOTAL_CREDITS,
                    SUM(CREDITS_USED_COMPUTE) AS COMPUTE_CREDITS,
                    SUM(CREDITS_USED_CLOUD_SERVICES) AS CLOUD_CREDITS,
                    COUNT(DISTINCT WAREHOUSE_NAME) AS TOTAL_WAREHOUSES
                FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
                WHERE START_TIME >= '{start_date_str}' 
                AND START_TIME <= '{end_date_str}'
            """)

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(render_corporate_metric_card(
                    "Total Warehouses",
                    safe_get_first_value(warehouse_summary, 'TOTAL_WAREHOUSES', 0),
                    "🏭",
                    "primary",
                    format_type="number"
                ), unsafe_allow_html=True)

            with col2:
                st.markdown(render_corporate_metric_card(
                    "Total Credits",
                    round(safe_get_first_value(warehouse_summary, 'TOTAL_CREDITS', 0), 2),
                    "💳",
                    "primary",
                    format_type="number"
                ), unsafe_allow_html=True)

            with col3:
                st.markdown(render_corporate_metric_card(
                    "Warehouse Credits",
                    round(safe_get_first_value(warehouse_summary, 'COMPUTE_CREDITS', 0), 2),
                    "⚙️",
                    "primary",
                    format_type="number"
                ), unsafe_allow_html=True)

            with col4:
                st.markdown(render_corporate_metric_card(
                    "Storage Credits",
                    round(safe_get_first_value(warehouse_summary, 'CLOUD_CREDITS', 0), 2),
                    "☁️",
                    "primary",
                    format_type="number"
                ), unsafe_allow_html=True)

            st.markdown('---')

            # === SECTION 2: CONFIGURATION TABLE ===
            st.markdown('<div class="section-header-corporate"> Warehouse Configuration & Statistics</div>', unsafe_allow_html=True)

            def show_warehouses(conn) -> pd.DataFrame:
                cursor = conn.cursor()
                cursor.execute("SHOW WAREHOUSES")
                rows = cursor.fetchall()
                columns = [desc[0].upper() for desc in cursor.description]
                cursor.close()
                return pd.DataFrame(rows, columns=columns)

            wh_stats_df = show_warehouses(conn)
            cols = ['NAME', 'SIZE', 'MIN_CLUSTER_COUNT', 'MAX_CLUSTER_COUNT', 'AUTO_SUSPEND', 'AUTO_RESUME', 'RESOURCE_MONITOR']
            wh_stats_df = wh_stats_df[[c for c in cols if c in wh_stats_df.columns]]

            if 'AUTO_SUSPEND' in wh_stats_df.columns:
                wh_stats_df['AUTO_SUSPEND'] = wh_stats_df['AUTO_SUSPEND'].fillna(0)

            # Conditional color styles
            def color_auto_suspend(val):
                if val == 0 or pd.isna(val):
                    return 'background-color:#ffc4c4'
                elif val >= 540:
                    return 'background-color:#ffc4c4'
                elif val >= 300:
                    return 'background-color:#ffd6ac'
                elif val >= 180:
                    return 'background-color:#fff0ac'
                return 'background-color:#d2f8d2'

            def color_auto_resume(val):
                return 'background-color:#d2f8d2' if str(val).lower() == 'true' else 'background-color:#ffc4c4'

            def color_resource_monitor(val):
                return 'background-color:#ffc4c4' if val is None or str(val).lower() == 'null' else 'background-color:#d2f8d2'

            st.dataframe(
                wh_stats_df.style
                .applymap(color_auto_suspend, subset=['AUTO_SUSPEND'])
                .applymap(color_auto_resume, subset=['AUTO_RESUME'])
                .applymap(color_resource_monitor, subset=['RESOURCE_MONITOR']),
                use_container_width=True
            )

            # === SECTION 3: SELECTOR ===
            st.markdown('<div class="section-header-corporate"> Warehouse Deep Dive</div>', unsafe_allow_html=True)
            warehouses_list = conn.query(f"""
                SELECT DISTINCT WAREHOUSE_NAME
                FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
                WHERE START_TIME >= '{start_date_str}' AND START_TIME <= '{end_date_str}'
                ORDER BY WAREHOUSE_NAME
            """)
            warehouse_options = ["All Warehouses"] + warehouses_list['WAREHOUSE_NAME'].tolist()
            selected_warehouse = st.selectbox("Select Warehouse for Detailed Analysis", warehouse_options)
            wh_filter = build_wh_filter("a")


            # === SECTION 4: CREDITS OVER TIME ===
            container_style = """
                background: #fff;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                padding: 1rem;
                margin-bottom: 1rem;
            """
            st.markdown(f'<div style="{container_style}"> Warehouse Credits Consumed Over Time</div>', unsafe_allow_html=True)

            credits_timeline = conn.query(f"""
                SELECT 
                    a.WAREHOUSE_NAME,
                    TO_DATE(a.END_TIME) AS DATE,
                    SUM(a.CREDITS_USED) AS TOTAL_CREDITS
                FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY a
                WHERE a.END_TIME >= DATEADD(day, -90, '{end_date_str}')
                AND a.END_TIME <= '{end_date_str}'
                {wh_filter}
                GROUP BY a.WAREHOUSE_NAME, DATE
                ORDER BY DATE DESC
            """)

            if not credits_timeline.empty:
                fig = px.bar(
                    credits_timeline,
                    x='DATE',
                    y='TOTAL_CREDITS',
                    color='WAREHOUSE_NAME',
                    hover_data=['DATE', 'TOTAL_CREDITS'],
                    labels={'DATE': 'Date', 'TOTAL_CREDITS': 'Credits Used'},
                    color_discrete_sequence=CORPORATE_CHART_COLORS
                )
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='IBM Plex Sans', color='#374151'),
                    margin=dict(l=20, r=20, t=20, b=40),
                    height=400,
                    showlegend=True
                )
                st.plotly_chart(configure_corporate_chart(fig, title="Warehouse Credits - Last 90 Days"), use_container_width=True)
            else:
                st.info("No credit consumption data available")

            col1, col2 = st.columns(2)

            # Chart 1: Warehouse Age
            with col1:
                st.markdown(f'<div style="{container_style}"> Top 10 Warehouses by Age</div>', unsafe_allow_html=True)
                wh_filter_age = build_wh_filter("a")
                warehouse_age = conn.query(f"""
                    SELECT 
                        a.WAREHOUSE_NAME, 
                        DATEDIFF(day, MIN(DATE(a.START_TIME)), CURRENT_DATE) AS AGE,
                        COALESCE(CAST(DATEDIFF(day, MAX(DATE(a.START_TIME)), CURRENT_DATE) AS VARCHAR), 'Never Used') AS LAST_USED
                    FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY a
                    LEFT JOIN SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_EVENTS_HISTORY b 
                        ON a.WAREHOUSE_NAME = b.WAREHOUSE_NAME  
                    WHERE a.START_TIME >= '{start_date_str}' AND a.START_TIME <= '{end_date_str}'
                    {wh_filter_age}
                    GROUP BY a.WAREHOUSE_NAME
                    ORDER BY AGE DESC
                    LIMIT 10
                """)
                if not warehouse_age.empty:
                    warehouse_age= warehouse_age.sort_values(by='AGE', ascending=True)
                    fig = px.bar(warehouse_age, y='WAREHOUSE_NAME', x='AGE', orientation='h', color_discrete_sequence=['#1e3a8a'])
                    fig.update_layout(height=370, margin=dict(l=20, r=20, t=20, b=40))
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No warehouse age data available")

            # Chart 2: Warehouse Credits (Top 10)
            with col2:
                st.markdown(f'<div style="{container_style}"> Top 10 Warehouse Credits</div>', unsafe_allow_html=True)
                wh_filter_top10 = build_wh_filter("a")

                credits_30d = conn.query(f"""
                    WITH top_wh AS (
                        SELECT 
                            a.WAREHOUSE_NAME,
                            SUM(a.CREDITS_USED_COMPUTE + a.CREDITS_USED_CLOUD_SERVICES) AS TOTAL_CREDITS
                        FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY a
                        WHERE a.END_TIME::DATE BETWEEN '{start_date_str}' AND '{end_date_str}'
                        {wh_filter_top10}
                        GROUP BY a.WAREHOUSE_NAME
                        ORDER BY TOTAL_CREDITS DESC
                        LIMIT 10
                    )
                    SELECT 
                        wmh.WAREHOUSE_NAME,
                        CAST(wmh.END_TIME AS DATE) AS USAGE_DATE,
                        SUM(wmh.CREDITS_USED_COMPUTE + wmh.CREDITS_USED_CLOUD_SERVICES) AS DAILY_CREDITS
                    FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY wmh
                    JOIN top_wh t ON wmh.WAREHOUSE_NAME = t.WAREHOUSE_NAME
                    WHERE wmh.END_TIME::DATE BETWEEN '{start_date_str}' AND '{end_date_str}'
                    GROUP BY wmh.WAREHOUSE_NAME, USAGE_DATE
                    ORDER BY USAGE_DATE ASC
                """)

                #chart_type = st.selectbox("Select chart type:", ("Line Chart", "Stacked Area Chart"), key="warehouse_chart_type")

                if not credits_30d.empty:
                    
                    fig = px.line(credits_30d, x='USAGE_DATE', y='DAILY_CREDITS', color='WAREHOUSE_NAME', markers=True)
                    

                    fig.update_layout(
                        height=400,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=20, r=20, t=30, b=40)
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No warehouse credit usage found for the selected date range.")

            col1, col2 = st.columns(2)

            # Chart 3: Query Count per Warehouse
            with col1:
                st.markdown(f'<div style="{container_style}"> Query Count per Warehouse</div>', unsafe_allow_html=True)
                wh_filter_qh = build_wh_filter("QH")
                query_activity = conn.query(f"""
                    SELECT 
                        QH.WAREHOUSE_NAME,
                        COUNT(*) AS QUERY_COUNT
                    FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY QH
                    WHERE QH.START_TIME::DATE BETWEEN '{start_date_str}' AND '{end_date_str}'
                    {wh_filter_qh}
                    GROUP BY QH.WAREHOUSE_NAME
                    ORDER BY QUERY_COUNT DESC
                    LIMIT 10
                """)

                if not query_activity.empty:
                    fig = px.bar(query_activity, y='WAREHOUSE_NAME', x='QUERY_COUNT', color='WAREHOUSE_NAME', orientation='h')
                    fig.update_layout(
                        height=370,
                        margin=dict(l=20, r=20, t=30, b=40),
                        showlegend=False,
                        xaxis=dict(showgrid=False),
                        yaxis=dict(showgrid=False) 
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No query history data available for the selected date range.")

            # Chart 4: Average Query Duration per Warehouse
            with col2:
                st.markdown(f'<div style="{container_style}"> Average Query Duration per Warehouse</div>', unsafe_allow_html=True)
                wh_filter_qh = build_wh_filter("QH")
                avg_duration = conn.query(f"""
                    SELECT 
                        QH.WAREHOUSE_NAME,
                        AVG(DATEDIFF(seconds, QH.START_TIME, QH.END_TIME)) AS AVG_EXECUTION_TIME
                    FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY QH
                    WHERE QH.START_TIME::DATE BETWEEN '{start_date_str}' AND '{end_date_str}'
                    AND QH.END_TIME IS NOT NULL
                    {wh_filter_qh}
                    GROUP BY QH.WAREHOUSE_NAME
                    ORDER BY AVG_EXECUTION_TIME DESC
                    LIMIT 10
                """)

                if not avg_duration.empty:
                    avg_duration = avg_duration.sort_values(by='AVG_EXECUTION_TIME', ascending=True)
                    fig = px.bar(
                        avg_duration,
                        y='WAREHOUSE_NAME',
                        x='AVG_EXECUTION_TIME',
                        orientation='h',
                        color_discrete_sequence=['#2563eb']
                    )
                    fig.update_layout(height=370, margin=dict(l=20, r=20, t=30, b=40))
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No query duration data available for the selected range.")

            with col1:
                st.markdown(f'<div style="{container_style}"> Partner Tools Credit Consumption</div>', unsafe_allow_html=True)
                
                def build_wh_filter_for_partner_tools():
                    if selected_warehouse != "All Warehouses":
                        return f"AND WAREHOUSE_NAME = '{selected_warehouse}'"
                    return ""
                
                # ✅ REMOVE THESE TWO LINES - the variables are already defined in warehouse_analytics() scope!
                # start_date_str = st.session_state.get('startdate', ...).strftime('%Y-%m-%d')
                # end_date_str = st.session_state.get('enddate', ...).strftime('%Y-%m-%d')

                partner_tools = conn.query(f"""
                    WITH CLIENT_HOUR_EXECUTION_CTE AS (
                        SELECT
                            CASE
                                WHEN CLIENT_APPLICATION_ID LIKE 'Go %' THEN 'Go'
                                WHEN CLIENT_APPLICATION_ID LIKE 'Snowflake UI %' THEN 'Snowflake UI'
                                WHEN CLIENT_APPLICATION_ID LIKE 'SnowSQL %' THEN 'SnowSQL'
                                WHEN CLIENT_APPLICATION_ID LIKE 'JDBC %' THEN 'JDBC'
                                WHEN CLIENT_APPLICATION_ID LIKE 'PythonConnector %' THEN 'Python'
                                WHEN CLIENT_APPLICATION_ID LIKE 'ODBC %' THEN 'ODBC'
                                ELSE 'NOT YET MAPPED: ' || CLIENT_APPLICATION_ID
                            END AS CLIENT_APPLICATION_NAME,
                            WAREHOUSE_NAME,
                            DATE_TRUNC('hour', START_TIME) AS START_TIME_HOUR,
                            SUM(EXECUTION_TIME) AS CLIENT_HOUR_EXECUTION_TIME
                        FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY QH
                        JOIN SNOWFLAKE.ACCOUNT_USAGE.SESSIONS SE ON SE.SESSION_ID = QH.SESSION_ID
                        WHERE WAREHOUSE_NAME IS NOT NULL
                            AND EXECUTION_TIME > 0
                            AND START_TIME >= '{start_date_str}'
                            AND START_TIME <= '{end_date_str}'
                            {build_wh_filter_for_partner_tools()}
                        GROUP BY 1,2,3
                    ),
                    HOUR_EXECUTION_CTE AS (
                        SELECT
                            START_TIME_HOUR,
                            WAREHOUSE_NAME,
                            SUM(CLIENT_HOUR_EXECUTION_TIME) AS HOUR_EXECUTION_TIME
                        FROM CLIENT_HOUR_EXECUTION_CTE
                        GROUP BY 1,2
                    ),
                    APPROXIMATE_CREDITS AS (
                        SELECT
                            A.CLIENT_APPLICATION_NAME,
                            A.WAREHOUSE_NAME,
                            (A.CLIENT_HOUR_EXECUTION_TIME / B.HOUR_EXECUTION_TIME) * C.CREDITS_USED AS APPROXIMATE_CREDITS_USED
                        FROM CLIENT_HOUR_EXECUTION_CTE A
                        JOIN HOUR_EXECUTION_CTE B 
                            ON A.START_TIME_HOUR = B.START_TIME_HOUR 
                            AND B.WAREHOUSE_NAME = A.WAREHOUSE_NAME
                        JOIN SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY C 
                            ON C.WAREHOUSE_NAME = A.WAREHOUSE_NAME 
                            AND C.START_TIME = A.START_TIME_HOUR
                    )
                    SELECT
                        CLIENT_APPLICATION_NAME,
                        WAREHOUSE_NAME,
                        SUM(APPROXIMATE_CREDITS_USED) AS APPROXIMATE_CREDITS_USED
                    FROM APPROXIMATE_CREDITS
                    GROUP BY 1,2
                    ORDER BY 3 DESC
                """)

                if not partner_tools.empty:
                    warehouse_totals = partner_tools.groupby('WAREHOUSE_NAME')['APPROXIMATE_CREDITS_USED'].sum().reset_index()
                    warehouse_totals = warehouse_totals.sort_values(by='APPROXIMATE_CREDITS_USED', ascending=False)
                    warehouse_order = warehouse_totals['WAREHOUSE_NAME'].tolist()
                    
                    fig = px.bar(
                        partner_tools,
                        y='WAREHOUSE_NAME',
                        x='APPROXIMATE_CREDITS_USED',
                        color='CLIENT_APPLICATION_NAME',
                        labels={'WAREHOUSE_NAME': 'Warehouse', 'APPROXIMATE_CREDITS_USED': 'Credits Used'},
                        hover_data=['APPROXIMATE_CREDITS_USED'],
                        color_discrete_sequence=CORPORATE_CHART_COLORS,
                        orientation='h',
                        category_orders={'WAREHOUSE_NAME': warehouse_order}
                    )
                    
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(family='IBM Plex Sans', color='#374151'),
                        margin=dict(l=20, r=20, t=20, b=40),
                        height=370,
                        showlegend=False,
                        xaxis=dict(showgrid=False),
                        yaxis=dict(showgrid=False)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No partner tools data available")
                    
            # Chart 6: Most Expensive Queries (Detailed)
            with col2:
                st.markdown(f'<div style="{container_style}"> Most Expensive Queries (by User)</div>', unsafe_allow_html=True)

                wh_filter = build_wh_filter("QH")

                expensive_queries_detailed = conn.query(f"""
                    WITH WAREHOUSE_SIZE AS (
                        SELECT 'X-SMALL' AS WAREHOUSE_SIZE, 1 AS NODES
                        UNION ALL SELECT 'SMALL', 2
                        UNION ALL SELECT 'MEDIUM', 4
                        UNION ALL SELECT 'LARGE', 8
                        UNION ALL SELECT 'X-LARGE', 16
                        UNION ALL SELECT '2X-LARGE', 32
                        UNION ALL SELECT '3X-LARGE', 64
                        UNION ALL SELECT '4X-LARGE', 128
                    ),
                    QUERY_HISTORY AS (
                        SELECT 
                            QH.QUERY_ID,
                            QH.QUERY_TEXT,
                            QH.USER_NAME,
                            QH.ROLE_NAME,
                            QH.EXECUTION_TIME,
                            QH.WAREHOUSE_SIZE
                        FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY QH
                        WHERE START_TIME >= '{start_date_str}'
                        AND START_TIME <= '{end_date_str}'
                        {wh_filter}
                    )
                    SELECT 
                        QH.USER_NAME,
                        QH.ROLE_NAME,
                        (QH.EXECUTION_TIME / (1000 * 60)) AS EXECUTION_TIME_MINUTES,
                        WS.WAREHOUSE_SIZE,
                        WS.NODES,
                        (QH.EXECUTION_TIME / (1000 * 60 * 60)) * WS.NODES AS RELATIVE_PERFORMANCE_COST
                    FROM QUERY_HISTORY QH
                    JOIN WAREHOUSE_SIZE WS ON WS.WAREHOUSE_SIZE = UPPER(QH.WAREHOUSE_SIZE)
                    ORDER BY RELATIVE_PERFORMANCE_COST DESC
                    LIMIT 10
                """)

                if not expensive_queries_detailed.empty:
                    # ✅ Aggregate by user to get total execution time per user
                    user_totals = expensive_queries_detailed.groupby('USER_NAME')['EXECUTION_TIME_MINUTES'].sum().reset_index()
                    user_totals = user_totals.sort_values(by='EXECUTION_TIME_MINUTES', ascending=False)
                    
                    # ✅ Create ordered list for category order (highest to lowest)
                    user_order = user_totals['USER_NAME'].tolist()
                    
                    fig = px.bar(
                        expensive_queries_detailed,
                        y='USER_NAME',
                        x='EXECUTION_TIME_MINUTES',
                        color='WAREHOUSE_SIZE',
                        labels={'USER_NAME': 'User', 'EXECUTION_TIME_MINUTES': 'Execution Time (Minutes)'},
                        hover_data=['ROLE_NAME', 'WAREHOUSE_SIZE', 'NODES', 'RELATIVE_PERFORMANCE_COST'],
                        color_discrete_sequence=CORPORATE_CHART_COLORS,
                        orientation='h',
                        category_orders={'USER_NAME': user_order}
                    )
                    
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(family='IBM Plex Sans', color='#374151'),
                        margin=dict(l=20, r=20, t=20, b=40),
                        height=370,
                        showlegend=False,
                        xaxis=dict(showgrid=False),
                        yaxis=dict(showgrid=False)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No detailed expensive queries data available")

            st.markdown(f'<div style="{container_style}"> Top 10 Materialized Views by Cost</div>', unsafe_allow_html=True)
            
            materialized_views = conn.query(f"""
                SELECT
                    TO_DATE(START_TIME) AS DATE,
                    DATABASE_NAME,
                    SCHEMA_NAME,
                    TABLE_NAME,
                    SUM(CREDITS_USED) AS CREDITS_USED
                FROM SNOWFLAKE.ACCOUNT_USAGE.MATERIALIZED_VIEW_REFRESH_HISTORY
                WHERE START_TIME >= DATEADD(month, -1, '{end_date_str}')
                AND START_TIME <= '{end_date_str}'
                GROUP BY 1, 2, 3, 4
                ORDER BY 5 DESC 
                LIMIT 10
            """)
            
            if not materialized_views.empty:
                fig = px.bar(
                    materialized_views,
                    x='TABLE_NAME',
                    y='CREDITS_USED',
                    color='SCHEMA_NAME',
                    labels={'TABLE_NAME': 'Materialized View', 'CREDITS_USED': 'Credits Used'},
                    hover_data=['DATABASE_NAME', 'SCHEMA_NAME'],
                    color_discrete_sequence=CORPORATE_CHART_COLORS
                )
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='IBM Plex Sans', color='#374151'),
                    margin=dict(l=20, r=20, t=20, b=40),
                    height=400,
                    showlegend=False,
                    xaxis_tickangle=-45,
                    xaxis=dict(categoryorder='total descending')
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No materialized view cost data available")
            
        except Exception as e:
            st.error(f"⚠️ Error loading warehouse analytics: {str(e)}")
            st.info("Please check your Snowflake connection and account permissions.")
    
    warehouse_analytics()
elif selected == "Storage":
    def storage_analytics():
        try:
            start_date = st.session_state.start_date
            end_date = st.session_state.end_date
            start_date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')
            
            # Calculate days for dynamic queries
            days_back = (end_date - start_date).days
            
            render_corporate_header(
                "Storage Analytics", 
                f"Comprehensive storage utilization and optimization insights | {start_date.strftime('%b %d, %Y')} - {end_date.strftime('%b %d, %Y')}",
                None
            )
            
            # ===== SECTION 1: OBJECT COUNTS =====
            st.markdown('<div class="section-header-corporate"> Storage Objects Overview</div>', unsafe_allow_html=True)
            
            # Query all counts in one go (optimized)
            object_counts = conn.query(f"""
                SELECT 
                    (SELECT count(*) FROM SNOWFLAKE.ACCOUNT_USAGE.DATABASES WHERE DELETED IS NULL and DATABASE_OWNER is not null) AS DATABASE_COUNT,
                    (SELECT COUNT(*) FROM SNOWFLAKE.ACCOUNT_USAGE.SCHEMATA WHERE DELETED IS NULL AND CATALOG_NAME <> 'SNOWFLAKE') AS SCHEMA_COUNT,
                    (SELECT COUNT(*) FROM SNOWFLAKE.ACCOUNT_USAGE.TABLES WHERE DELETED IS NULL and TABLE_CATALOG <> 'SNOWFLAKE') AS TABLE_COUNT,
                    (SELECT COUNT(*) FROM SNOWFLAKE.ACCOUNT_USAGE.VIEWS WHERE DELETED IS NULL and TABLE_CATALOG <> 'SNOWFLAKE') AS VIEW_COUNT
            """)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(render_corporate_metric_card(
                    "Total Databases",
                    safe_get_first_value(object_counts, 'DATABASE_COUNT', 0),
                    "🗄️",
                    "primary",
                    change=None,
                    format_type="number"
                ), unsafe_allow_html=True)
            
            with col2:
                st.markdown(render_corporate_metric_card(
                    "Total Schemas",
                    safe_get_first_value(object_counts, 'SCHEMA_COUNT', 0),
                    "📂",
                    "primary",
                    change=None,
                    format_type="number"
                ), unsafe_allow_html=True)
            
            with col3:
                st.markdown(render_corporate_metric_card(
                    "Total Tables",
                    safe_get_first_value(object_counts, 'TABLE_COUNT', 0),
                    "📋",
                    "primary",
                    change=None,
                    format_type="number"
                ), unsafe_allow_html=True)
            
            with col4:
                st.markdown(render_corporate_metric_card(
                    "Total Views",
                    safe_get_first_value(object_counts, 'VIEW_COUNT', 0),
                    "👁️",
                    "primary",
                    change=None,
                    format_type="number"
                ), unsafe_allow_html=True)
            
            st.markdown('---')
            
            # ===== SECTION 2: STORAGE METRICS =====
            st.markdown('<div class="section-header-corporate"> Storage Consumption Metrics</div>', unsafe_allow_html=True)
            
            # Optimized storage metrics query
            storage_metrics = conn.query("""
                SELECT 
                    COALESCE(ROUND(SUM(CASE WHEN TABLE_ENTERED_FAILSAFE IS NOT NULL 
                        THEN FAILSAFE_BYTES/1000000000 END), 2), 0) AS FAILSAFE_GB,
                    COALESCE(ROUND(SUM(CASE WHEN TABLE_DROPPED IS NULL AND IS_TRANSIENT='NO' 
                        THEN ACTIVE_BYTES/1000000000 END), 2), 0) AS PERMANENT_GB,
                    COALESCE(ROUND(SUM(CASE WHEN TABLE_DROPPED IS NULL AND IS_TRANSIENT='YES' 
                        THEN ACTIVE_BYTES/1000000000 END), 2), 0) AS TRANSIENT_GB
                FROM SNOWFLAKE.ACCOUNT_USAGE.TABLE_STORAGE_METRICS
            """)
            
            # Materialized views and stage bytes
            mv_stage = conn.query(f"""
                SELECT 
                    (SELECT COALESCE(SUM(BYTES/1000000000), 0) 
                    FROM SNOWFLAKE.ACCOUNT_USAGE.TABLES 
                    WHERE CREATED >= DATEADD(month, -1, CURRENT_TIMESTAMP())
                    AND TABLE_TYPE = 'MATERIALIZED VIEW' 
                    AND DELETED IS NULL) AS MV_GB,
                    (SELECT COALESCE(ROUND(SUM(AVERAGE_STAGE_BYTES/1000000000), 2), 0)
                    FROM SNOWFLAKE.ACCOUNT_USAGE.STAGE_STORAGE_USAGE_HISTORY 
                    WHERE USAGE_DATE = DATEADD(DAY, -1, CURRENT_DATE())) AS STAGE_GB
            """)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(render_corporate_metric_card(
                    "Permanent Tables",
                    safe_get_first_value(storage_metrics, 'PERMANENT_GB', 0),
                    "💿",
                    "primary",
                    change=None,
                    format_type="number"
                ), unsafe_allow_html=True)
                st.caption("Active bytes (GB)")
            
            with col2:
                st.markdown(render_corporate_metric_card(
                    "Transient Tables",
                    safe_get_first_value(storage_metrics, 'TRANSIENT_GB', 0),
                    "⚡",
                    "warning",
                    change=None,
                    format_type="number"
                ), unsafe_allow_html=True)
                st.caption("Active bytes (GB)")
            
            with col3:
                st.markdown(render_corporate_metric_card(
                    "Failsafe Storage",
                    safe_get_first_value(storage_metrics, 'FAILSAFE_GB', 0),
                    "🛡️",
                    "danger",
                    change=None,
                    format_type="number"
                ), unsafe_allow_html=True)
                st.caption("Failsafe bytes (GB)")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(render_corporate_metric_card(
                    "Materialized Views",
                    safe_get_first_value(mv_stage, 'MV_GB', 0),
                    "🔄",
                    "success",
                    change=None,
                    format_type="number"
                ), unsafe_allow_html=True)
                st.caption("Last 30 days (GB)")
            
            with col2:
                st.markdown(render_corporate_metric_card(
                    "Stage Storage",
                    safe_get_first_value(mv_stage, 'STAGE_GB', 0),
                    "📦",
                    "primary",
                    change=None,
                    format_type="number"
                ), unsafe_allow_html=True)
                st.caption("Yesterday's average (GB)")
            
            st.markdown('---')
            
            # ===== SECTION 3: STORAGE TRENDS =====
            st.markdown('<div class="section-header-corporate"> Storage Trends & Analytics</div>', unsafe_allow_html=True)
            
            # Professional container styling matching the cost estimator theme
            container_style = """
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                padding: 1.25rem;
                margin-bottom: 1rem;
                font-family: 'Inter', sans-serif;
                font-weight: 600;
                color: #1f2937;
                font-size: 1.1rem;
            """
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f'<div style="{container_style}"> Storage Consumption Trend</div>', unsafe_allow_html=True)

                storage_history = conn.query(f"""
                    SELECT 
                        db.USAGE_DATE AS USAGE_DATE,
                        ROUND(SUM(db.AVERAGE_DATABASE_BYTES/(1024*1024*1024)), 2) AS AVERAGE_DATABASE_GB,
                        ROUND(SUM(db.AVERAGE_FAILSAFE_BYTES/(1024*1024*1024)), 2) AS AVERAGE_FAILSAFE_GB,
                        ROUND(SUM(stage.AVERAGE_STAGE_BYTES/(1024*1024*1024)), 2) AS AVERAGE_STAGE_GB
                    FROM SNOWFLAKE.ACCOUNT_USAGE.DATABASE_STORAGE_USAGE_HISTORY db
                    LEFT JOIN SNOWFLAKE.ACCOUNT_USAGE.STAGE_STORAGE_USAGE_HISTORY stage
                        ON db.USAGE_DATE = stage.USAGE_DATE
                    WHERE db.USAGE_DATE >= '{start_date_str}'
                    AND db.USAGE_DATE <= '{end_date_str}'
                    GROUP BY db.USAGE_DATE
                    ORDER BY db.USAGE_DATE
                """)

                if not storage_history.empty:
                    import decimal
                    storage_history = storage_history.applymap(
                        lambda x: float(x) if isinstance(x, decimal.Decimal) else x
                    )

                    # Fill missing values (if any)
                    storage_history.fillna(0, inplace=True)

                    # Add total column
                    storage_history['TOTAL'] = (
                        storage_history['AVERAGE_DATABASE_GB'] +
                        storage_history['AVERAGE_FAILSAFE_GB'] +
                        storage_history['AVERAGE_STAGE_GB']
                    )

                    storage_history = storage_history.sort_values(by='TOTAL', ascending=False)
                    
                    date_order = storage_history['USAGE_DATE'].tolist()

                    
                    fig = px.bar(
                        storage_history,
                        y='USAGE_DATE',
                        x=['AVERAGE_DATABASE_GB', 'AVERAGE_FAILSAFE_GB', 'AVERAGE_STAGE_GB'],
                        labels={
                            'USAGE_DATE': 'Date',
                            'value': 'Storage (GB)',
                            'variable': 'Storage Type'
                        },
                        color_discrete_sequence=['#667eea', '#764ba2', '#f093fb'],
                        orientation='h',
                        category_orders={'USAGE_DATE': date_order}  # ✅ Explicit descending order
                    )
                    
                    # Apply professional styling
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(family='Inter, sans-serif', color='#374151', size=12),
                        margin=dict(l=20, r=20, t=40, b=20),
                        height=400,
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1,
                            bgcolor="rgba(255,255,255,0.8)",
                            bordercolor="#e5e7eb",
                            borderwidth=1
                        ),
                        hovermode='y unified',
                        xaxis=dict(
                            gridcolor='#f3f4f6',
                            showgrid=False,
                            title_font=dict(color='#6b7280')
                        ),
                        yaxis=dict(
                            gridcolor='#f3f4f6',
                            showgrid=False,
                            title_font=dict(color='#6b7280')
                        )
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No storage history data available for selected period")


            with col2:
                st.markdown(f'<div style="{container_style}"> Top 10 Databases by Size</div>', unsafe_allow_html=True)
                
                top_databases = conn.query(f"""
                    SELECT 
                        b.DATABASE_NAME,
                        ROUND(SUM(a.AVERAGE_DATABASE_BYTES/1000000000), 2) + 
                        ROUND(SUM(a.AVERAGE_FAILSAFE_BYTES/1000000000), 2) AS TOTAL_GB
                    FROM SNOWFLAKE.ACCOUNT_USAGE.DATABASES b
                    LEFT JOIN SNOWFLAKE.ACCOUNT_USAGE.DATABASE_STORAGE_USAGE_HISTORY a
                        ON b.DATABASE_NAME = a.DATABASE_NAME
                    WHERE a.USAGE_DATE = DATEADD(DAY, -1, CURRENT_DATE())
                    AND b.DELETED IS NULL
                    AND b.DATABASE_NAME NOT IN ('SNOWFLAKE', 'SNAPSHOT')  -- exclude system DBs
                    GROUP BY b.DATABASE_NAME
                    ORDER BY TOTAL_GB DESC
                    LIMIT 10
                """)

                
                if not top_databases.empty:
                    top_databases = top_databases.sort_values(by='TOTAL_GB', ascending=True)
                    fig = px.bar(
                        top_databases,
                        y='DATABASE_NAME',
                        x='TOTAL_GB',
                        orientation='h',
                        labels={'DATABASE_NAME': 'Database', 'TOTAL_GB': 'Size (GB)'},
                        color_discrete_sequence=['#1849A0'],  # Professional blue
                        
                    )
                    
                    # Apply consistent professional styling
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(family='Inter, sans-serif', color='#374151', size=12),
                        margin=dict(l=20, r=20, t=40, b=40),
                        height=400,
                        
                        xaxis=dict(
                            tickangle=0,
                            gridcolor='#f3f4f6',
                            showgrid=False,
                            title_font=dict(color='#6b7280')
                        ),
                        yaxis=dict(
                            gridcolor='#f3f4f6',
                            showgrid=False,
                            title_font=dict(color='#6b7280')
                        )
                    )
                    
                    # Professional hover template
                    fig.update_traces(
                        hovertemplate='<br>Size:%{x} GB<extra></extra>'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No database storage data available")
            
            # ===== SECTION 4: TABLE ANALYTICS =====
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f'<div style="{container_style}"> Top 10 Tables by Size</div>', unsafe_allow_html=True)

                # Fetch top_tables from Snowflake
                top_tables = conn.query("""
                    SELECT 
                        TABLE_NAME,
                        ROUND(SUM(BYTES/1000000000), 2) AS TOTAL_GB
                    FROM SNOWFLAKE.ACCOUNT_USAGE.TABLES
                    WHERE DELETED IS NULL and TABLE_CATALOG != 'SNOWFLAKE'
                    GROUP BY TABLE_NAME
                    ORDER BY TOTAL_GB DESC
                    LIMIT 10;
                """)

                if not top_tables.empty:
                    top_tables = top_tables.sort_values(by='TOTAL_GB', ascending=True)
                    fig = px.bar(
                        top_tables,
                        x='TOTAL_GB',           # Size (GB) on the x-axis
                        y='TABLE_NAME',         # Table Name on the y-axis (horizontal bars)
                        labels={'TABLE_NAME': '', 'TOTAL_GB': 'Size (GB)'},  # ← Remove y-axis label
                        color_discrete_sequence=['#10b981'],  # Professional green
                       
                        orientation='h'         # Horizontal bars
                    )

                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(family='Inter, sans-serif', color='#374151', size=12),
                        margin=dict(l=120, r=20, t=40, b=60),  # More left margin for longer names!
                        height=400,
                        
                        xaxis=dict(
                            tickangle=0,
                            showgrid=False,  # Remove X axis grid lines
                            title='Size (GB)',
                            title_font=dict(color='#6b7280')
                        ),
                        yaxis=dict(
                            showgrid=False,  # Remove Y axis grid lines
                            title='',        # Remove y-axis label
                            automargin=True,
                            tickfont=dict(size=12)
                        )
                    )

                    fig.update_traces(
                        hovertemplate='<b>%{y}</b><br>Size: %{x:.2f} GB<extra></extra>'
                    )

                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No table data available")
            
            with col2:
                st.markdown(f'<div style="{container_style}"> Internal Stages Storage</div>', unsafe_allow_html=True)
                
                internal_stages = conn.query(f"""
                SELECT 
                    a.STAGE_NAME,
                    DATE(a.CREATED) AS CREATED_DATE,
                    b.USAGE_DATE,
                    ROUND(b.AVERAGE_STAGE_BYTES/1000000, 2) AS SIZE_MB
                FROM SNOWFLAKE.ACCOUNT_USAGE.STAGES a
                JOIN SNOWFLAKE.ACCOUNT_USAGE.STAGE_STORAGE_USAGE_HISTORY b
                    ON DATE(a.CREATED) = b.USAGE_DATE
                WHERE a.DELETED IS NULL 
                AND a.STAGE_TYPE = 'Internal Named'
                AND a.stage_name <> '__snowflake_temp_import_files__'
                AND b.USAGE_DATE >= '{start_date_str}'
                AND b.USAGE_DATE <= '{end_date_str}'
                ORDER BY a.CREATED DESC
                LIMIT 10
                """)

                
                
                if not internal_stages.empty:
                    
                    # Convert SIZE_MB to float to avoid Decimal issues
                    internal_stages['SIZE_MB'] = internal_stages['SIZE_MB'].astype(float)
                    
                    # Only keep the latest usage record per stage (so each stage appears once)
                    internal_stages_latest = (
                        internal_stages
                        .sort_values(by="USAGE_DATE")
                        .groupby("STAGE_NAME", as_index=False)
                        .last()
                        .sort_values(by="SIZE_MB", ascending=True)
                    )

                    # Get max value for proper range calculation (convert to float)
                    max_size = float(internal_stages_latest['SIZE_MB'].max())

                    fig = px.bar(
                        internal_stages_latest,
                        x='SIZE_MB',
                        y='STAGE_NAME',
                        labels={'STAGE_NAME': 'Stage Name', 'SIZE_MB': 'Size (MB)'},
                        text='SIZE_MB',
                        orientation='h'
                    )
                    
                    fig.update_traces(
                        marker_color='#1849A0',
                        texttemplate='%{text:.2f}',  # Removed 'MB' to save space, add if needed
                        textposition='outside',
                        textfont=dict(size=11, color='#374151', weight='bold'),
                        marker=dict(line=dict(color='white', width=2))
                    )
                    
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(family='Inter, sans-serif', color='#374151', size=12),
                        margin=dict(l=20, r=100, t=40, b=60),  # Increased right margin
                        height=max(400, len(internal_stages_latest) * 60),  # Dynamic height based on number of bars
                        xaxis=dict(
                            gridcolor='#f3f4f6',
                            showgrid=True,
                            title='Size (MB)',
                            title_font=dict(color='#6b7280'),
                            range=[0, max_size * 1.15]  # Extend range by 15% to fit text labels
                        ),
                        yaxis=dict(
                            gridcolor='#f3f4f6',
                            showgrid=False,
                            title_font=dict(color='#6b7280'),
                            title=''
                        )
                    )

                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No internal stage data available for selected period")
                st.markdown('---')
                   
            # ===== SECTION 5: PIPE ANALYTICS =====
            st.markdown('<div class="section-header-corporate"> Data Pipeline Analytics</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f'<div style="{container_style}"> Top 5 Pipes by Credits</div>', unsafe_allow_html=True)
                
                top_pipes = conn.query(f"""
                    
                SELECT 
                    PIPE_NAME,
                    ROUND(SUM(CREDITS_USED), 2) AS TOTAL_CREDITS
                FROM SNOWFLAKE.ACCOUNT_USAGE.PIPE_USAGE_HISTORY
                WHERE START_TIME >= '{start_date_str}'
                AND START_TIME <= '{end_date_str}'
                GROUP BY PIPE_NAME
                HAVING ROUND(SUM(CREDITS_USED), 2) > 0
                ORDER BY TOTAL_CREDITS DESC
                LIMIT 5;
                """)
                
                if not top_pipes.empty:
                    top_pipes = top_pipes.sort_values(by='TOTAL_CREDITS', ascending=True)
                    fig = px.bar(
                        top_pipes,
                        x='TOTAL_CREDITS',
                        y='PIPE_NAME',
                        labels={'PIPE_NAME': 'Pipe Name', 'TOTAL_CREDITS': 'Credits Used'},
                        color_discrete_sequence=['#f59e0b'],  # Professional orange/amber
                     
                        orientation='h'
                    )
                    
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(family='Inter, sans-serif', color='#374151', size=12),
                        margin=dict(l=20, r=20, t=40, b=60),
                        height=400,
                        
                        xaxis=dict(
                            tickangle=-45,
                            gridcolor='#f3f4f6',
                            showgrid=False,
                            title_font=dict(color='#6b7280')
                        ),
                        yaxis=dict(
                            gridcolor='#f3f4f6',
                            showgrid=False,
                            title_font=dict(color='#6b7280'),
                            title=''
                        )
                    )
                    
                    fig.update_traces(
                        hovertemplate='<b>%{x}</b><br>Credits: %{y:.2f}<extra></extra>'
                    )
                   
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No pipe usage data available for selected period")
            
            with col2:
                st.markdown(f'<div style="{container_style}"> Pipe Credits Trend</div>', unsafe_allow_html=True)
                
                pipe_trend = conn.query(f"""
                    SELECT 
                        DATE(END_TIME) AS USAGE_DATE,
                        PIPE_NAME,
                        ROUND(SUM(CREDITS_USED), 2) AS DAILY_CREDITS
                    FROM SNOWFLAKE.ACCOUNT_USAGE.PIPE_USAGE_HISTORY
                    WHERE END_TIME >= '{start_date_str}'
                    AND END_TIME <= '{end_date_str}'
                    GROUP BY DATE(END_TIME), PIPE_NAME
                    HAVING ROUND(SUM(CREDITS_USED), 2) > 0
                    ORDER BY USAGE_DATE
                """)
                
                if not pipe_trend.empty:
                
                    # Professional color palette for multiple pipes
                    professional_colors = ['#667eea', '#764ba2', '#f093fb', '#1849A0', '#10b981', 
                                        '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#84cc16']
                    pipe_trend = pipe_trend.sort_values(by='DAILY_CREDITS', ascending=True)
                    fig = px.bar(
                        pipe_trend,
                        x='DAILY_CREDITS',
                        y='USAGE_DATE',
                        color='PIPE_NAME',
                        labels={'USAGE_DATE': 'Date', 'DAILY_CREDITS': 'Credits Used'},
                        color_discrete_sequence=professional_colors,
                        
                        
                    )
                    
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(family='Inter, sans-serif', color='#374151', size=12),
                        margin=dict(l=20, r=20, t=40, b=20),
                        height=400,
                        
                        showlegend=True,
                        legend=dict(
                            orientation="v",
                            yanchor="top",
                            y=1,
                            xanchor="left",
                            x=1.02,
                            bgcolor="rgba(255,255,255,0.8)",
                            bordercolor="#e5e7eb",
                            borderwidth=1
                        ),
                        hovermode='x unified',
                        xaxis=dict(
                            gridcolor='#f3f4f6',
                            showgrid=False,
                            title_font=dict(color='#6b7280')
                        ),
                        yaxis=dict(
                            gridcolor='#f3f4f6',
                            showgrid=False,
                            title_font=dict(color='#6b7280'),

                        )
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No pipe trend data available")
            
            # ===== SECTION 6: DATA TRANSFER =====
            st.markdown(f'<div style="{container_style}"> Files Transfered Through Pipes</div>', unsafe_allow_html=True)
           
            bytes_transferred = conn.query(f"""
                SELECT 
                    DATE(END_TIME) AS TRANSFER_DATE,
                    PIPE_NAME,
                    
                    SUM(FILES_INSERTED) AS FILES_COUNT
                FROM SNOWFLAKE.ACCOUNT_USAGE.PIPE_USAGE_HISTORY
                WHERE START_TIME >= '{start_date_str}'
                AND START_TIME <= '{end_date_str}'
                GROUP BY DATE(END_TIME), PIPE_NAME
                ORDER BY TRANSFER_DATE
            """)

            if not bytes_transferred.empty:
                professional_colors = ['#667eea', '#764ba2', '#f093fb', '#1849A0', '#10b981', 
                                        '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#84cc16']
                bytes_transferred = bytes_transferred.sort_values(by='TRANSFER_DATE', ascending=True)
            
                fig = px.bar(
                    bytes_transferred,
                    x='TRANSFER_DATE',
                    y='FILES_COUNT',
                    color='PIPE_NAME',
                    labels={'TRANSFER_DATE': 'Date', 'FILES_COUNT': 'Files Transferred'},
                    color_discrete_sequence=professional_colors,
                    hover_data=['FILES_COUNT'],
                    
                )

                
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='Inter, sans-serif', color='#374151', size=12),
                    margin=dict(l=20, r=20, t=40, b=20),
                    height=400,
                   
                    showlegend=True,
                    legend=dict(
                        orientation="v",
                        yanchor="top",
                        y=1,
                        xanchor="left",
                        x=1.02,
                        bgcolor="rgba(255,255,255,0.8)",
                        bordercolor="#e5e7eb",
                        borderwidth=1
                    ),
                    hovermode='x unified',
                    xaxis=dict(
                        gridcolor='#f3f4f6',
                        showgrid=False,
                        title_font=dict(color='#6b7280')
                    ),
                    yaxis=dict(
                        gridcolor='#f3f4f6',
                        showgrid=False,
                        title_font=dict(color='#6b7280')
                    )
                )
                
                
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No File Transfer information available")
            
            st.markdown('---')
            
            # ===== SECTION 7: OPTIMIZATION INSIGHTS =====
            st.markdown('<div class="section-header-corporate"> Storage Optimization Insights</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f'<div style="{container_style}"> Top 10 Unused Tables</div>', unsafe_allow_html=True)
                
                unused_tables = conn.query("""
                    SELECT 
                        TABLE_NAME,
                        ROW_COUNT,
                        ROUND(BYTES/1000000000, 2) AS SIZE_GB,
                        DATEDIFF(DAY, DATE(CREATED), CURRENT_TIMESTAMP()) AS DAYS_SINCE_CREATED,
                        DATEDIFF(DAY, DATE(LAST_ALTERED), CURRENT_TIMESTAMP()) AS DAYS_SINCE_USED
                    FROM SNOWFLAKE.ACCOUNT_USAGE.TABLES
                    WHERE DELETED IS NULL
                    ORDER BY SIZE_GB DESC, DAYS_SINCE_USED DESC
                    LIMIT 10
                """)
                
                if not unused_tables.empty:
                    unused_tables = unused_tables.sort_values(by='SIZE_GB', ascending=True)
                    fig = px.bar(
                        unused_tables,
                        x='SIZE_GB',
                        y='TABLE_NAME',
                        labels={'TABLE_NAME': 'Table Name', 'SIZE_GB': 'Size (GB)'},
                        hover_data=['ROW_COUNT', 'DAYS_SINCE_USED'],
                        color_discrete_sequence=['#ef4444'],  # Professional red for warnings
                        
                        orientation='h'
                    )
                    
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(family='Inter, sans-serif', color='#374151', size=12),
                        margin=dict(l=20, r=20, t=40, b=60),
                        height=400,
                        
                        xaxis=dict(
                            tickangle=0,
                            gridcolor='#f3f4f6',
                            showgrid=False,
                            title_font=dict(color='#6b7280')
                        ),
                        yaxis=dict(
                            gridcolor='#f3f4f6',
                            showgrid=False,
                            title_font=dict(color='#6b7280'),
                            title=''
                        )
                    )
                    
                    fig.update_traces(
                        hovertemplate='<br>Size: %{x} GB<br>Days since used: %{customdata[1]}<extra></extra>'
                    )
                    
                
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No unused table data available")
            
            with col2:
                st.markdown(f'<div style="{container_style}"> Unused Cloned Tables</div>', unsafe_allow_html=True)
                
                cloned_tables = conn.query("""
                    WITH clone_data AS (
                        SELECT 
                            a.TABLE_NAME AS BASE_TABLE,
                            b.TABLE_NAME AS CLONE_TABLE,
                            b.TABLE_CREATED,
                            c.LAST_ALTERED
                        FROM SNOWFLAKE.ACCOUNT_USAGE.TABLE_STORAGE_METRICS a
                        JOIN SNOWFLAKE.ACCOUNT_USAGE.TABLE_STORAGE_METRICS b
                            ON a.ID = b.CLONE_GROUP_ID AND a.TABLE_NAME <> b.TABLE_NAME
                        JOIN SNOWFLAKE.ACCOUNT_USAGE.TABLES c
                            ON b.TABLE_NAME = c.TABLE_NAME
                        WHERE c.DELETED IS NULL
                    )
                    SELECT 
                        BASE_TABLE,
                        CLONE_TABLE,
                        DATEDIFF(DAY, DATE(TABLE_CREATED), CURRENT_DATE()) AS DAYS_SINCE_CREATED,
                        DATEDIFF(DAY, DATE(LAST_ALTERED), CURRENT_DATE()) AS DAYS_SINCE_USED
                    FROM clone_data
                    ORDER BY DAYS_SINCE_USED DESC
                    LIMIT 10
                """)
                
                if not cloned_tables.empty:
                    cloned_tables = cloned_tables.sort_values(by='DAYS_SINCE_USED', ascending=True)
                    fig = px.bar(
                        cloned_tables,
                        x='DAYS_SINCE_USED',
                        y='CLONE_TABLE',
                        labels={'CLONE_TABLE': 'Clone Table', 'DAYS_SINCE_USED': 'Days Since Last Use'},
                        hover_data=['BASE_TABLE', 'DAYS_SINCE_CREATED'],
                        color_discrete_sequence=['#f59e0b'],
                       
                        orientation='h'
                    )
                    
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(family='Inter, sans-serif', color='#374151', size=12),
                        margin=dict(l=20, r=20, t=40, b=60),
                        height=400,
                        
                        xaxis=dict(
                            tickangle=0,
                            gridcolor='#f3f4f6',
                            showgrid=False,
                            title_font=dict(color='#6b7280')
                        ),
                        yaxis=dict(
                            gridcolor='#f3f4f6',
                            showgrid=False,
                            title_font=dict(color='#6b7280'),
                            title=''
                        )
                    )
                    
                    fig.update_traces(
                        hovertemplate='<b>%{x}</b><br>Days idle: %{y}<br>Base: %{customdata[0]}<extra></extra>'
                    )
                    
                
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No cloned table data available")
            
            # ===== SECTION 8: SHORT-LIVED TABLES & IDLE SCHEMAS =====
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f'<div style="{container_style}"> Short-Lived Tables</div>', unsafe_allow_html=True)
                
                short_lived = conn.query(f"""
                    SELECT 
                        TABLE_NAME,
                        ROW_COUNT,
                        ROUND(BYTES/1000000, 2) AS SIZE_MB,
                        DATEDIFF(DAY, DATE(CREATED), DATE(DELETED)) AS LIFESPAN_DAYS
                    FROM SNOWFLAKE.ACCOUNT_USAGE.TABLES
                    WHERE DELETED IS NOT NULL
                    AND TABLE_TYPE = 'BASE TABLE'
                    AND IS_TRANSIENT = 'NO'
                    AND DATEDIFF(DAY, DATE(CREATED), DATE(DELETED)) = 1
                    AND DATE(CREATED) >= '{start_date_str}'
                    AND DATE(CREATED) <= '{end_date_str}'
                    ORDER BY SIZE_MB DESC
                    LIMIT 10
                """)
                
                if not short_lived.empty:
                    short_lived = short_lived.sort_values(by='SIZE_MB', ascending=True)
                    fig = px.bar(
                        short_lived,
                        x='SIZE_MB',
                        y='TABLE_NAME',
                        labels={'TABLE_NAME': 'Table Name', 'SIZE_MB': 'Size (MB)'},
                        hover_data=['ROW_COUNT', 'LIFESPAN_DAYS'],
                        color_discrete_sequence=['#f59e0b'],
                    
                        orientation='h'
                    )
                    
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(family='Inter, sans-serif', color='#374151', size=12),
                        margin=dict(l=20, r=20, t=40, b=60),
                        height=400,
                        
                        xaxis=dict(
                            tickangle=0,
                            gridcolor='#f3f4f6',
                            showgrid=False,
                            title_font=dict(color='#6b7280')
                        ),
                        yaxis=dict(
                            gridcolor='#f3f4f6',
                            showgrid=False,
                            title_font=dict(color='#6b7280'),
                            title=''
                        )
                    )
                    
                    fig.update_traces(
                        hovertemplate='<br>Size: %{x} MB<br>Lifespan: %{customdata[1]} day(s)<extra></extra>'
                    )
                    
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info(f"No short-lived tables found for period {start_date_str} to {end_date_str}")
            
            with col2:
                st.markdown(f'<div style="{container_style}"> Top 10 Idle Schemas</div>', unsafe_allow_html=True)
                
                idle_schemas = conn.query("""
                    SELECT 
                        a.TABLE_SCHEMA,
                        DATEDIFF(DAY, DATE(b.SCHEMA_CREATED), CURRENT_DATE()) AS DAYS_SINCE_CREATED,
                        DATEDIFF(DAY, MAX(DATE(a.LAST_ALTERED)), CURRENT_DATE()) AS DAYS_SINCE_USED
                    FROM SNOWFLAKE.ACCOUNT_USAGE.TABLES a
                    LEFT JOIN SNOWFLAKE.ACCOUNT_USAGE.TABLE_STORAGE_METRICS b
                        ON b.TABLE_SCHEMA = a.TABLE_SCHEMA
                    WHERE a.DELETED IS NULL 
                    AND b.DELETED = 'FALSE'
                    GROUP BY a.TABLE_SCHEMA, b.SCHEMA_CREATED
                    ORDER BY DAYS_SINCE_USED DESC
                    LIMIT 10
                """)
                
                if not idle_schemas.empty:
                    idle_schemas = idle_schemas.sort_values(by='DAYS_SINCE_USED', ascending=True)
                    fig = px.bar(
                        idle_schemas,
                        x='DAYS_SINCE_USED',
                        y='TABLE_SCHEMA',
                        labels={'TABLE_SCHEMA': 'Schema Name', 'DAYS_SINCE_USED': 'Days Idle'},
                        hover_data=['DAYS_SINCE_CREATED'],
                        color_discrete_sequence=['#8b5cf6'],  # Professional purple
                        
                        orientation='h'
                    )
                    
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(family='Inter, sans-serif', color='#374151', size=12),
                        margin=dict(l=20, r=20, t=40, b=60),
                        height=400,
                        
                        xaxis=dict(
                            tickangle=0,
                            gridcolor='#f3f4f6',
                            showgrid=False,
                            title_font=dict(color='#6b7280')
                        ),
                        yaxis=dict(
                            gridcolor='#f3f4f6',
                            showgrid=False,
                            title_font=dict(color='#6b7280'),
                            title=''
                        )
                    )
                    
                    fig.update_traces(
                        hovertemplate='<br>Schema: %{y}<br>Days since created: %{customdata[0]}<extra></extra>'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No idle schema data available")
            
        except Exception as e:
            st.error(f"⚠️ Error loading storage analytics: {str(e)}")
            st.info("Please check your Snowflake connection and account permissions.")

    # Call the function
    storage_analytics()

elif selected == "Roles":
    def role_management():
    
        try:
            start_date = st.session_state.start_date
            end_date = st.session_state.end_date
            start_date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')

            # Header
            render_corporate_header(
                "Role Analytics & Hierarchy",
                f"Comprehensive role hierarchy, user access, and security analytics | {start_date.strftime('%b %d, %Y')} - {end_date.strftime('%b %d, %Y')}",
                None
            )

           
            # ===== SECTION 1: ROLE METRICS =====
            st.markdown('<div class="section-header-corporate"> Role Distribution & Statistics</div>', unsafe_allow_html=True)

            # Fetch all admin role counts in optimized single query
            admin_roles = conn.query(f"""
                SELECT 
                    DEFAULT_ROLE,
                    COUNT(DISTINCT NAME) as user_count
                FROM SNOWFLAKE.ACCOUNT_USAGE.USERS
                WHERE DEFAULT_ROLE IN ('ACCOUNTADMIN', 'SYSADMIN', 'SECURITYADMIN', 'USERADMIN')
                    AND DELETED_ON IS NULL
                    AND CREATED_ON <= '{end_date_str}'
                GROUP BY DEFAULT_ROLE
            """)

            # Create dict for easy access
            admin_dict = {row['DEFAULT_ROLE']: row['USER_COUNT'] for _, row in admin_roles.iterrows()}

            # Custom roles count
            custom_roles_count = conn.query("""
                SELECT COUNT(NAME) as custom_role_count
                FROM SNOWFLAKE.ACCOUNT_USAGE.ROLES 
                WHERE OWNER IS NOT NULL
            """)

            # Orphan roles (roles with grant option but not granted to other roles)
            orphan_roles = conn.query("""
                SELECT COUNT(DISTINCT a.ROLE) as orphan_count
                FROM SNOWFLAKE.ACCOUNT_USAGE.GRANTS_TO_USERS a
                JOIN SNOWFLAKE.ACCOUNT_USAGE.GRANTS_TO_ROLES b
                    ON a.ROLE = b.NAME
                WHERE b.GRANT_OPTION = TRUE
                    AND a.ROLE NOT IN (
                        SELECT GRANTEE_NAME 
                        FROM SNOWFLAKE.ACCOUNT_USAGE.GRANTS_TO_ROLES 
                        WHERE GRANTED_ON = 'ROLE' 
                            AND GRANTED_TO = 'ROLE' 
                            AND GRANT_OPTION = FALSE
                            AND GRANTED_BY IS NOT NULL
                    )
            """)

            # Display metrics in grid
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(render_corporate_metric_card(
                    "ACCOUNTADMIN",
                    admin_dict.get('ACCOUNTADMIN', 0),
                    "👑",
                    "danger",
                    change=None,
                    format_type="number"
                ), unsafe_allow_html=True)

            with col2:
                st.markdown(render_corporate_metric_card(
                    "SECURITYADMIN",
                    admin_dict.get('SECURITYADMIN', 0),
                    "🔐",
                    "warning",
                    change=None,
                    format_type="number"
                ), unsafe_allow_html=True)

            with col3:
                st.markdown(render_corporate_metric_card(
                    "USERADMIN",
                    admin_dict.get('USERADMIN', 0),
                    "👥",
                    "primary",
                    change=None,
                    format_type="number"
                ), unsafe_allow_html=True)

            with col4:
                st.markdown(render_corporate_metric_card(
                    "SYSADMIN",
                    admin_dict.get('SYSADMIN', 0),
                    "⚙️",
                    "primary",
                    change=None,
                    format_type="number"
                ), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(render_corporate_metric_card(
                    "Custom Roles",
                    safe_get_first_value(custom_roles_count, 'CUSTOM_ROLE_COUNT', 0),
                    "🎯",
                    "success",
                    change=None,
                    format_type="number"
                ), unsafe_allow_html=True)

            with col2:
                orphan_count = safe_get_first_value(orphan_roles, 'ORPHAN_COUNT', 0)
                if orphan_count > 0:
                    st.markdown(render_corporate_metric_card(
                        "Orphan Roles",
                        orphan_count,
                        "⚠️",
                        "danger",
                        change=None,
                        format_type="number"
                    ), unsafe_allow_html=True)
                    st.caption("Roles with grant option but not properly integrated")

            st.markdown('---')

            # ===== SECTION 2: ROLE HIERARCHY GRAPH =====
            st.markdown('<div class="section-header-corporate"> Role Hierarchy Visualization</div>', unsafe_allow_html=True)

            role_hierarchy = conn.query("""
                SELECT DISTINCT 
                    NAME,
                    GRANTEE_NAME 
                FROM SNOWFLAKE.ACCOUNT_USAGE.GRANTS_TO_ROLES 
                WHERE GRANTED_ON = 'ROLE' 
                ORDER BY GRANTEE_NAME
                LIMIT 500
            """)

            if not role_hierarchy.empty:
                # Create graphviz diagram
                graph = graphviz.Digraph()
                graph.attr(rankdir='TB', size='12,8')
                graph.attr('node', shape='box', style='rounded,filled', fillcolor='#e0f2fe', 
                        fontname='IBM Plex Sans', fontsize='10')
                graph.attr('edge', color='#1e3a8a', penwidth='1.5')

                # Add edges
                for _, row in role_hierarchy.iterrows():
                    graph.edge(row['GRANTEE_NAME'], row['NAME'])

                st.graphviz_chart(graph, use_container_width=True)
            else:
                st.info("No role hierarchy data available")

            st.markdown('---')

            # ===== SECTION 3: ROLE ANALYTICS CHARTS =====
            st.markdown('<div class="section-header-corporate"> Role Usage Analytics</div>', unsafe_allow_html=True)

            container_style = """
                background: #fff;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                padding: 1rem;
                margin-bottom: 1rem;
            """

            col1, col2 = st.columns(2)

            # Top 5 Roles by Users
            with col1:
                st.markdown(f'<div style="{container_style}"> Top 5 Roles by User Count</div>', unsafe_allow_html=True)


                top_roles = conn.query(f"""
                    SELECT 
                        ROLE, 
                        COUNT(ROLE) as no_of_users 
                    FROM SNOWFLAKE.ACCOUNT_USAGE.GRANTS_TO_USERS 
                    WHERE DELETED_ON IS NULL
                    GROUP BY ROLE
                    ORDER BY no_of_users DESC 
                    LIMIT 5
                """)


                if not top_roles.empty:
                    fig = px.bar(
                        top_roles,
                        y='ROLE',
                        x='NO_OF_USERS',
                        orientation='h',
                        labels={'ROLE': 'Role Name', 'NO_OF_USERS': 'Number of Users'},
                        color_discrete_sequence=['#1e3a8a']
                    )
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(family='IBM Plex Sans', color='#374151'),
                        margin=dict(l=40, r=20, t=20, b=40),
                        height=400,
                        yaxis=dict(autorange='reversed'),
                        showlegend=False
                    )
                    st.plotly_chart(configure_corporate_chart(fig), use_container_width=True)
                else:
                    st.info("No role assignment data available")


            # Idle Roles (Not used in 15+ days)
            with col2:
                st.markdown(f'<div style="{container_style}"> Idle Roles</div>', unsafe_allow_html=True)


                idle_roles = conn.query(f"""
                    SELECT 
                        a.NAME,
                        b.last_used 
                    FROM SNOWFLAKE.ACCOUNT_USAGE.ROLES a  
                    JOIN (
                        SELECT DISTINCT 
                            ROLE_NAME,
                            DATEDIFF(day, MAX(END_TIME), CURRENT_TIMESTAMP()) as last_used
                        FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
                        GROUP BY ROLE_NAME
                        HAVING last_used > 15
                    ) b ON b.ROLE_NAME = a.NAME
                    WHERE a.DELETED_ON IS NULL
                    ORDER BY b.last_used DESC
                    LIMIT 10
                """)


                if not idle_roles.empty:
                    fig = px.bar(
                        idle_roles,
                        y='NAME',
                        x='LAST_USED',
                        orientation='h',
                        labels={'NAME': 'Role Name', 'LAST_USED': 'Days Since Last Use'},
                        color_discrete_sequence=['#c2410c']
                    )
                    fig.update_traces(
                        marker=dict(color='#c2410c', line=dict(color='#991b1b', width=1))
                    )
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(family='IBM Plex Sans', color='#374151'),
                        margin=dict(l=40, r=20, t=20, b=40),
                        height=400,
                        yaxis=dict(autorange='reversed'),
                        showlegend=False
                    )
                    st.plotly_chart(configure_corporate_chart(fig), use_container_width=True)
                else:
                    st.info("All roles are actively used")

            # ===== SECTION 4: USER CREDIT CONSUMPTION =====
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f'<div style="{container_style}"> Top 10 Users by Credit Consumption </div>', unsafe_allow_html=True)

                # Dynamic date calculation for last 30 days
                credits_end = datetime.now().date()
                credits_start = credits_end - timedelta(days=30)

                user_credits = conn.query(f"""
                    WITH USER_HOUR_EXECUTION_CTE AS (
                        SELECT 
                            USER_NAME,
                            WAREHOUSE_NAME,
                            DATE_TRUNC('hour', START_TIME) as START_TIME_HOUR,
                            SUM(EXECUTION_TIME) as USER_HOUR_EXECUTION_TIME
                        FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
                        WHERE WAREHOUSE_NAME IS NOT NULL
                            AND EXECUTION_TIME > 0
                            AND START_TIME >= '{credits_start}'
                            AND START_TIME <= '{credits_end}'
                        GROUP BY 1, 2, 3
                    ),
                    HOUR_EXECUTION_CTE AS (
                        SELECT 
                            START_TIME_HOUR,
                            WAREHOUSE_NAME,
                            SUM(USER_HOUR_EXECUTION_TIME) as HOUR_EXECUTION_TIME
                        FROM USER_HOUR_EXECUTION_CTE
                        GROUP BY 1, 2
                    ),
                    APPROXIMATE_CREDITS AS (
                        SELECT 
                            A.USER_NAME,
                            C.WAREHOUSE_NAME,
                            (A.USER_HOUR_EXECUTION_TIME / B.HOUR_EXECUTION_TIME) * C.CREDITS_USED as APPROXIMATE_CREDITS_USED
                        FROM USER_HOUR_EXECUTION_CTE A
                        JOIN HOUR_EXECUTION_CTE B 
                            ON A.START_TIME_HOUR = B.START_TIME_HOUR
                            AND B.WAREHOUSE_NAME = A.WAREHOUSE_NAME
                        JOIN SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY C 
                            ON C.WAREHOUSE_NAME = A.WAREHOUSE_NAME
                            AND C.START_TIME = A.START_TIME_HOUR
                    ),
                    ACTIVE_USERS AS (
                        SELECT DISTINCT NAME 
                        FROM SNOWFLAKE.ACCOUNT_USAGE.USERS 
                        WHERE DELETED_ON IS NULL
                    )
                    SELECT 
                        a.USER_NAME,
                        a.WAREHOUSE_NAME,
                        SUM(a.APPROXIMATE_CREDITS_USED) as APPROXIMATE_CREDITS_USED
                    FROM APPROXIMATE_CREDITS a
                    JOIN ACTIVE_USERS b ON a.USER_NAME = b.NAME
                    GROUP BY 1, 2
                    ORDER BY 3 DESC
                    LIMIT 10
                """)

                if not user_credits.empty:
                    # ✅ Sort in ASCENDING order for proper visual display (lowest to highest in data)
                    user_credits = user_credits.sort_values(by='APPROXIMATE_CREDITS_USED', ascending=True)

                    fig = px.bar(
                        user_credits,
                        y='USER_NAME',
                        x='APPROXIMATE_CREDITS_USED',
                        orientation='h',
                        color='WAREHOUSE_NAME',
                        labels={
                            'USER_NAME': 'User', 
                            'APPROXIMATE_CREDITS_USED': 'Credits Used',
                            'WAREHOUSE_NAME': 'Warehouse'
                        },
                        color_discrete_sequence=CORPORATE_CHART_COLORS
                    )

                    # --- Remove all gridlines and make background white ---
                    fig.update_xaxes(
                        showgrid=False, zeroline=False, showline=False,
                        ticks='', showticklabels=True, minor=dict(showgrid=False)
                    )
                    fig.update_yaxes(
                        showgrid=False, zeroline=False, showline=False,
                        ticks='', showticklabels=True, minor=dict(showgrid=False)
                    )

                    fig.update_layout(
                        paper_bgcolor='white',
                        plot_bgcolor='white',
                        font=dict(family='IBM Plex Sans', color='#374151'),
                        margin=dict(l=100, r=20, t=20, b=20),
                        height=400,
                        showlegend=True,
                        yaxis={'categoryorder': 'total descending'}  # ✅ Highest at top, lowest at bottom
                    )

                    st.plotly_chart(configure_corporate_chart(fig), use_container_width=True)
                else:
                    st.info("No credit consumption data available for the last 30 days")

            # Role to User Assignment Table
            with col2:
                st.markdown(f'<div style="{container_style}"> Role Assignment Summary</div>', unsafe_allow_html=True)

                role_summary = conn.query("""
                    SELECT 
                        ROLE,
                        COUNT(DISTINCT GRANTEE_NAME) AS USER_COUNT,
                        MIN(CREATED_ON) AS FIRST_ASSIGNED,
                        MAX(CREATED_ON) AS LAST_MODIFIED
                    FROM SNOWFLAKE.ACCOUNT_USAGE.GRANTS_TO_USERS
                    WHERE DELETED_ON IS NULL
                    GROUP BY ROLE
                    ORDER BY USER_COUNT DESC
                """)

                if not role_summary.empty:
                    fig = go.Figure(data=[go.Table(
                        header=dict(
                            values=['<b>Role</b>', '<b>Users</b>', '<b>First Assigned</b>', '<b>Last Assigned</b>'],
                            fill_color='#1e3a8a',
                            font=dict(color='white', size=12, family='IBM Plex Sans'),
                            align='left'
                        ),
                        cells=dict(
                            values=[
                                role_summary['ROLE'],
                                role_summary['USER_COUNT'],
                                role_summary['FIRST_ASSIGNED'].dt.strftime('%Y-%m-%d'),
                                role_summary['LAST_MODIFIED'].dt.strftime('%Y-%m-%d')
                            ],
                            fill_color='#f9fafb',
                            font=dict(color='#374151', size=11, family='IBM Plex Sans'),
                            align='left',
                            height=30
                        )
                    )])

                    fig.update_layout(
                        margin=dict(l=0, r=0, t=0, b=0),
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No role assignment summary available")
            st.markdown('---')
            
            # ===== SECTION 5: SECURITY INSIGHTS =====
            st.markdown('<div class="section-header-corporate"> Security & Compliance Insights</div>', unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f'<div style="{container_style}"> Roles with Elevated Privileges</div>', unsafe_allow_html=True)


                elevated_roles = conn.query("""
                    SELECT 
                        GRANTEE_NAME as role_name,
                        COUNT(DISTINCT PRIVILEGE) as privilege_count,
                        LISTAGG(DISTINCT PRIVILEGE, ', ') as privileges
                    FROM SNOWFLAKE.ACCOUNT_USAGE.GRANTS_TO_ROLES
                    WHERE GRANTED_ON = 'ACCOUNT'
                        AND DELETED_ON IS NULL
                        AND GRANTEE_NAME NOT IN ('ACCOUNTADMIN', 'SECURITYADMIN')
                    GROUP BY GRANTEE_NAME
                    HAVING privilege_count > 3
                    ORDER BY privilege_count DESC
                    LIMIT 10
                """)


                if not elevated_roles.empty:
                    fig = px.bar(
                        elevated_roles,
                        y='ROLE_NAME',
                        x='PRIVILEGE_COUNT',
                        orientation='h',
                        labels={'ROLE_NAME': 'Role', 'PRIVILEGE_COUNT': 'Number of Account Privileges'},
                        color_discrete_sequence=['#991b1b']
                    )
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(family='IBM Plex Sans', color='#374151'),
                        margin=dict(l=40, r=20, t=20, b=40),
                        height=400,
                        yaxis=dict(autorange='reversed')
                    )
                    st.plotly_chart(configure_corporate_chart(fig), use_container_width=True)
                else:
                    st.info("No roles with excessive account-level privileges detected")


            with col2:
                st.markdown(f'<div style="{container_style}"> Users with Multiple Admin Roles</div>', unsafe_allow_html=True)

                multi_admin = conn.query("""
                    SELECT 
                        GRANTEE_NAME as user_name,
                        COUNT(DISTINCT ROLE) as admin_role_count,
                        LISTAGG(DISTINCT ROLE, ', ') as admin_roles
                    FROM SNOWFLAKE.ACCOUNT_USAGE.GRANTS_TO_USERS
                    WHERE ROLE IN ('ACCOUNTADMIN', 'SECURITYADMIN', 'SYSADMIN', 'USERADMIN')
                        AND DELETED_ON IS NULL
                    GROUP BY GRANTEE_NAME
                    HAVING admin_role_count > 1
                    ORDER BY admin_role_count DESC
                """)

                if not multi_admin.empty:
                    fig = px.bar(
                        multi_admin,
                        y='USER_NAME',
                        x='ADMIN_ROLE_COUNT',
                        labels={'USER_NAME': 'User', 'ADMIN_ROLE_COUNT': 'Admin Roles Assigned'},
                        color_discrete_sequence=['#c2410c'],
                        orientation='h'
                    )
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(family='IBM Plex Sans', color='#374151'),
                        margin=dict(l=40, r=20, t=20, b=40),
                        height=400,
                        xaxis=dict(showgrid=False)
                    )
                    st.plotly_chart(configure_corporate_chart(fig), use_container_width=True)
                else:
                    st.info(" No users with multiple admin roles")

        except Exception as e:
            st.error(f"⚠️ Error loading role management data: {str(e)}")
            st.info("Please check your Snowflake connection and ACCOUNT_USAGE permissions.")
    role_management()
elif selected == "Costs":
    render_corporate_header("Cost Analysis", "Credit consumption and cost optimization", None)
    st.info("Cost analysis module coming soon...")
elif selected == "Miscellaneous":
    def miscellaneous_analytics():

        try:
            start_date = st.session_state.start_date
            end_date = st.session_state.end_date
            start_date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')
            
            render_corporate_header(
                "Miscellaneous Analytics", 
                f"Functions, Security, Tasks & Data Loading Analysis | {start_date.strftime('%b %d, %Y')} - {end_date.strftime('%b %d, %Y')}",
                None
            )
            
            # ===== SECTION 1: FUNCTION METRICS =====
            st.markdown('<div class="section-header-corporate"> Function Statistics</div>', unsafe_allow_html=True)
            
            # Get function counts and duplicates
            function_metrics = conn.query("""
                WITH duplicate_functions AS (
                    SELECT 
                        FUNCTION_NAME,
                        FUNCTION_LANGUAGE,
                        COUNT(*) as function_duplicate_count
                    FROM SNOWFLAKE.ACCOUNT_USAGE.FUNCTIONS
                    WHERE DELETED IS NULL
                    GROUP BY FUNCTION_LANGUAGE, FUNCTION_NAME
                    HAVING COUNT(*) > 1
                )
                SELECT 
                    (SELECT COUNT(DISTINCT FUNCTION_NAME) 
                    FROM SNOWFLAKE.ACCOUNT_USAGE.FUNCTIONS 
                    WHERE DELETED IS NULL) as total_functions,
                    COALESCE(SUM(function_duplicate_count), 0) as total_duplicate_functions
                FROM duplicate_functions
            """)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(render_corporate_metric_card(
                    "Total Functions",
                    safe_get_first_value(function_metrics, 'TOTAL_FUNCTIONS', 0),
                    "⚙️",
                    "primary",
                    change=None,
                    format_type="number"
                ), unsafe_allow_html=True)
            
            with col2:
                st.markdown(render_corporate_metric_card(
                    "Probable Duplicate Functions",
                    safe_get_first_value(function_metrics, 'TOTAL_DUPLICATE_FUNCTIONS', 0),
                    "⚠️",
                    "warning",
                    change=None,
                    format_type="number"
                ), unsafe_allow_html=True)
            
            st.markdown('---')
            
            # ===== SECTION 2: EXECUTED PROCEDURES & UDFs =====
            st.markdown('<div class="section-header-corporate"> Function Execution Analytics</div>', unsafe_allow_html=True)
            
            container_style = """
                background: #fff;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                padding: 1rem;
                margin-bottom: 1rem;
            """
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f'<div style="{container_style}"> Similar Executed Procedures</div>', unsafe_allow_html=True)
                
                # Executed Procedures Query
                store_procedure = conn.query(f"""
                    SELECT 
                        f.FUNCTION_NAME AS function_name,
                        f.FUNCTION_SCHEMA AS function_schema,
                        f.ARGUMENT_SIGNATURE AS argument_signature,
                        qh.QUERY_TYPE AS query_type,
                        qh.QUERY_TEXT AS query_text,
                        COUNT(DISTINCT qh.QUERY_ID) AS total_no_execute
                    FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY qh
                    INNER JOIN SNOWFLAKE.ACCOUNT_USAGE.FUNCTIONS f 
                        ON qh.SCHEMA_ID = f.FUNCTION_SCHEMA_ID
                    WHERE qh.QUERY_TYPE = 'CALL'
                        AND f.DELETED IS NULL
                        AND qh.START_TIME >= '{start_date_str}'
                        AND qh.START_TIME <= '{end_date_str}'
                    GROUP BY 
                        f.FUNCTION_NAME,
                        f.FUNCTION_SCHEMA,
                        f.ARGUMENT_SIGNATURE,
                        qh.QUERY_TYPE,
                        qh.QUERY_TEXT
                    ORDER BY total_no_execute DESC
                    LIMIT 25
                """)

                if not store_procedure.empty:
                    # Sort for clean display
                    store_procedure = store_procedure.sort_values('TOTAL_NO_EXECUTE', ascending=True)

                    # Create horizontal bar chart
                    fig = px.bar(
                        store_procedure, 
                        x="TOTAL_NO_EXECUTE",
                        y="FUNCTION_NAME",
                        orientation='h',
                        color='FUNCTION_NAME',
                        labels={
                            "TOTAL_NO_EXECUTE": "Number of Executions",
                            "FUNCTION_NAME": "Function Name"
                        },
                        hover_name="FUNCTION_NAME",
                        hover_data=["TOTAL_NO_EXECUTE", "QUERY_TEXT", "FUNCTION_SCHEMA"]
                    )

                    # --- Layout Customization ---
                    fig.update_layout(
                        showlegend=False,
                        yaxis={"categoryorder": "total ascending"},
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(family='IBM Plex Sans', color='#374151'),
                        height=450,
                        margin=dict(l=100, r=40, t=20, b=40),
                    )

                    # --- Fully Remove Grids, Zero Lines, and Tick Lines ---
                    fig.update_xaxes(
                        showgrid=False,
                        zeroline=False,
                        showticklabels=True,
                        ticks='',
                        showline=False
                    )
                    fig.update_yaxes(
                        showgrid=False,
                        zeroline=False,
                        showticklabels=True,
                        ticks='',
                        showline=False
                    )

                    # Render clean chart
                    st.plotly_chart(configure_corporate_chart(fig), use_container_width=True)

                else:
                    st.info("No stored procedures executed in selected period.")

            
            with col2:
                st.markdown(f'<div style="{container_style}"> Similar Executed UDFs</div>', unsafe_allow_html=True)
                
                # Executed UDFs
                udf = conn.query(f"""
                    SELECT 
                        f.FUNCTION_NAME as function_name,
                        f.FUNCTION_SCHEMA as function_schema,
                        f.ARGUMENT_SIGNATURE as argument_signature,
                        qh.QUERY_TYPE as query_type,
                        qh.QUERY_TEXT as query_text,
                        COUNT(DISTINCT qh.QUERY_ID) as total_no_execute
                    FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY qh
                    INNER JOIN SNOWFLAKE.ACCOUNT_USAGE.FUNCTIONS f 
                        ON qh.SCHEMA_ID = f.FUNCTION_SCHEMA_ID
                    WHERE f.FUNCTION_DEFINITION IS NULL
                        AND qh.QUERY_TYPE = 'SELECT'
                        AND f.DELETED IS NULL
                        AND qh.START_TIME >= '{start_date_str}'
                        AND qh.START_TIME <= '{end_date_str}'
                    GROUP BY 
                        f.FUNCTION_NAME,
                        f.FUNCTION_SCHEMA,
                        f.ARGUMENT_SIGNATURE,
                        qh.QUERY_TYPE,
                        qh.QUERY_TEXT
                    ORDER BY total_no_execute DESC
                    LIMIT 25
                """)
                
                if not udf.empty:
                    fig = px.bar(
                        udf, 
                        x="function_name", 
                        y="total_no_execute",
                        color='function_name',
                        labels={
                            "function_name": "Function Name",
                            "total_no_execute": "Executions"
                        },
                        hover_name="function_name", 
                        hover_data=["total_no_execute", 'query_text', 'function_schema']
                    )
                    fig.update_layout(
                        showlegend=False,
                        xaxis={"categoryorder": "total descending"},
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(family='IBM Plex Sans', color='#374151'),
                        height=370,
                        margin=dict(l=20, r=20, t=20, b=80),
                        xaxis_tickangle=-45
                    )
                    st.plotly_chart(configure_corporate_chart(fig), use_container_width=True)
                else:
                    st.info("No UDFs executed in selected period")
            
            st.markdown('---')
            
            # ===== SECTION 3: FAILED LOGINS ANALYSIS =====
            st.markdown('<div class="section-header-corporate"> Security & Login Analytics</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f'<div style="{container_style}"> Failed Logins by Day</div>', unsafe_allow_html=True)
                
                fail_logins_per_day = conn.query(f"""
                    SELECT 
                        REPORTED_CLIENT_TYPE as reported_client_type,
                        USER_NAME as user_name,
                        DATE(EVENT_TIMESTAMP) as date,
                        COUNT(*) as total_fail_login
                    FROM SNOWFLAKE.ACCOUNT_USAGE.LOGIN_HISTORY
                    WHERE IS_SUCCESS = 'NO'
                        AND EVENT_TIMESTAMP >= '{start_date_str}'
                        AND EVENT_TIMESTAMP <= '{end_date_str}'
                    GROUP BY 
                        DATE(EVENT_TIMESTAMP),
                        USER_NAME,
                        REPORTED_CLIENT_TYPE
                    ORDER BY total_fail_login DESC
                """)
                
                if not fail_logins_per_day.empty:
                    fig = px.bar(
                    fail_logins_per_day, 
                    x='DATE',
                    y='TOTAL_FAIL_LOGIN',
                    color='REPORTED_CLIENT_TYPE',
                    labels={
                        'DATE': 'Date', 
                        'TOTAL_FAIL_LOGIN': 'Failed Logins'
                    },
                    hover_name='USER_NAME'
                )

                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(family='IBM Plex Sans', color='#374151'),
                        height=370,
                        margin=dict(l=20, r=20, t=20, b=20)
                    )
                    st.plotly_chart(configure_corporate_chart(fig), use_container_width=True)
                else:
                    st.info("No failed logins in selected period")
            
            with col2:
                st.markdown(f'<div style="{container_style}"> Failed Login Timeline (Snowflake UI)</div>', unsafe_allow_html=True)

                failed_login = conn.query(f"""
                    SELECT 
                        TO_DATE(EVENT_TIMESTAMP) as date,
                        TO_TIME(EVENT_TIMESTAMP) as time,
                        USER_NAME as user_name,
                        EVENT_TYPE as event_type,
                        REPORTED_CLIENT_TYPE as reported_client_type,
                        IS_SUCCESS as is_success,
                        ERROR_MESSAGE as error_message,
                        CLIENT_IP as ip_address
                    FROM SNOWFLAKE.ACCOUNT_USAGE.LOGIN_HISTORY
                    WHERE EVENT_TYPE = 'LOGIN'
                        AND REPORTED_CLIENT_TYPE = 'SNOWFLAKE_UI'
                        AND IS_SUCCESS = 'NO'
                        AND EVENT_TIMESTAMP >= '{start_date_str}'
                        AND EVENT_TIMESTAMP <= '{end_date_str}'
                    ORDER BY EVENT_TIMESTAMP DESC
                """)

                if not failed_login.empty:
                    # --- Group by date and user for bar chart ---
                    timeline_data = (
                        failed_login.groupby(['DATE', 'USER_NAME'])
                        .size().reset_index(name='FAILED_ATTEMPTS')
                    )

                    # --- Stacked bar chart for failed logins ---
                    fig = px.bar(
                        timeline_data,
                        x='DATE',
                        y='FAILED_ATTEMPTS',
                        color='USER_NAME',
                        labels={"DATE": "Date", "FAILED_ATTEMPTS": "Failed Login Attempts"},
                        hover_data=['USER_NAME'],
                    )

                    # --- Absolutely remove all gridlines, zero lines, and axis lines ---
                    fig.update_xaxes(
                        showgrid=False,
                        showline=False,
                        zeroline=False,
                        showticklabels=True,
                        ticks='',
                        mirror=False,
                        minor=dict(showgrid=False)
                    )
                    fig.update_yaxes(
                        showgrid=False,
                        showline=False,
                        zeroline=False,
                        showticklabels=True,
                        ticks='',
                        mirror=False,
                        minor=dict(showgrid=False)
                    )

                    # --- Layout: fully white, no background tint ---
                    fig.update_layout(
                        paper_bgcolor='white',
                        plot_bgcolor='white',
                        font=dict(family='IBM Plex Sans', color='#374151'),
                        height=370,
                        margin=dict(l=20, r=20, t=20, b=20),
                        barmode='stack',
                        showlegend=True,
                        legend=dict(title='User', orientation='v', yanchor='top', y=1)
                    )

                    # --- Render chart ---
                    st.plotly_chart(configure_corporate_chart(fig), use_container_width=True)

                else:
                    st.info("No failed Snowflake UI logins in selected period.")

                st.markdown('---')
  
            # ===== SECTION 4: QUERY PERFORMANCE & TASKS =====
            st.markdown('<div class="section-header-corporate"> Performance & Task Analytics</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f'<div style="{container_style}"> Top 10 Inefficient Queries</div>', unsafe_allow_html=True)
                
                warehouse_performance_laging = conn.query(f"""
                    SELECT DISTINCT 
                        q.USER_NAME as user_name,
                        q.QUERY_ID as query_id,
                        q.WAREHOUSE_NAME as warehouse_name,
                        q.SCHEMA_NAME as schema_name,
                        q.START_TIME as start_time,
                        q.END_TIME as end_time,
                        q.WAREHOUSE_SIZE as warehouse_size,
                        ROUND((q.BYTES_SPILLED_TO_REMOTE_STORAGE/1073741824), 3) as data_storage_gb_remote,
                        q.QUERY_TEXT as query_text
                    FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY q
                    WHERE q.BYTES_SPILLED_TO_REMOTE_STORAGE >= 1
                        AND q.START_TIME >= '{start_date_str}'
                        AND q.START_TIME <= '{end_date_str}'
                    ORDER BY data_storage_gb_remote DESC
                    LIMIT 10
                """)
                
                if not warehouse_performance_laging.empty:
                    fig = px.bar(
                        warehouse_performance_laging, 
                        x="user_name", 
                        y="data_storage_gb_remote",
                        color="query_text",
                        labels={
                            "user_name": "User",
                            "data_storage_gb_remote": "Remote Storage (GB)"
                        },
                        hover_name="user_name", 
                        hover_data=['data_storage_gb_remote', 'query_text', 'warehouse_size']
                    )
                    fig.update_layout(
                        showlegend=False,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(family='IBM Plex Sans', color='#374151'),
                        height=370,
                        margin=dict(l=20, r=20, t=20, b=80),
                        xaxis_tickangle=-45
                    )
                    st.plotly_chart(configure_corporate_chart(fig), use_container_width=True)
                else:
                    st.info("No inefficient queries with remote spillage found")
            
            with col2:
                st.markdown(f'<div style="{container_style}"> Top 10 Failed Tasks</div>', unsafe_allow_html=True)
                
                failed_tasks = conn.query(f"""
                    WITH task_credits AS (
                        SELECT 
                            t.NAME as name,
                            t.SCHEMA_NAME as schema_name,
                            t.ERROR_MESSAGE as error_message,
                            DATE(t.COMPLETED_TIME) as date,
                            t.STATE as state,
                            q.QUERY_TEXT as query_text,
                            COUNT(DISTINCT t.QUERY_ID) as total_execution,
                            COALESCE(SUM(w.CREDITS_USED), 0) as total_credits
                        FROM SNOWFLAKE.ACCOUNT_USAGE.TASK_HISTORY t
                        INNER JOIN SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY q 
                            ON q.QUERY_ID = t.QUERY_ID
                        LEFT JOIN SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY w 
                            ON q.WAREHOUSE_ID = w.WAREHOUSE_ID
                            AND DATE_TRUNC('HOUR', q.START_TIME) = w.START_TIME
                        WHERE t.STATE = 'FAILED'
                            AND t.COMPLETED_TIME >= '{start_date_str}'
                            AND t.COMPLETED_TIME <= '{end_date_str}'
                        GROUP BY 
                            t.NAME,
                            t.SCHEMA_NAME,
                            t.ERROR_MESSAGE,
                            DATE(t.COMPLETED_TIME),
                            t.STATE,
                            q.QUERY_TEXT
                    )
                    SELECT *
                    FROM task_credits
                    ORDER BY total_execution DESC
                    LIMIT 10
                """)

                if not failed_tasks.empty:
                    # Sort ascending for horizontal bar readability
                    failed_tasks = failed_tasks.sort_values('TOTAL_EXECUTION', ascending=True)

                    # Create horizontal bar chart (swapped axes)
                    fig = px.bar(
                        failed_tasks,
                        x='TOTAL_EXECUTION',   # X-axis: execution count
                        y='NAME',              # Y-axis: task name
                        orientation='h',       # Horizontal bars
                        color='NAME',
                        labels={
                            "NAME": "Task Name",
                            "TOTAL_EXECUTION": "Failed Executions"
                        },
                        hover_data=['TOTAL_CREDITS', 'QUERY_TEXT', 'DATE']
                    )

                    # --- Layout Customization ---
                    fig.update_layout(
                        showlegend=False,
                        yaxis={"categoryorder": "total ascending"},
                        paper_bgcolor ='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(family='IBM Plex Sans', color='#374151'),
                        height=400,
                        margin=dict(l=100, r=40, t=20, b=40),
                    )

                    # --- Completely remove all gridlines, ticks, and axis lines ---
                    fig.update_xaxes(
                        showgrid=False,       # Removes major gridlines
                        showspikes=False,     # Disables hover gridline spikes
                        zeroline=False,       # Removes zero axis line
                        showline=False,       # Removes axis border line
                        ticks='',             # Removes tick marks
                        showticklabels=True,  # Keeps labels visible
                        minor=dict(showgrid=False)  # Removes minor gridlines if enabled
                    )

                    fig.update_yaxes(
                        showgrid=False,       # Removes major gridlines
                        showspikes=False,     # Disables hover gridline spikes
                        zeroline=False,       # Removes zero axis line
                        showline=False,       # Removes axis border line
                        ticks='',             # Removes tick marks
                        showticklabels=True,  # Keeps labels visible
                        minor=dict(showgrid=False)  # Removes minor gridlines if enabled
                    )

                    # Optional: Transparent background for clean UI
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                    )

                    # Display chart
                    st.plotly_chart(configure_corporate_chart(fig), use_container_width=True)

                else:
                    st.info("No failed tasks in selected period.")

            
            st.markdown('---')
            
            # ===== SECTION 5: DATA LOADING FAILURES =====
            st.markdown('<div class="section-header-corporate"> Data Loading Analytics</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f'<div style="{container_style}"> Top 10 Failed Loads via Snowpipe</div>', unsafe_allow_html=True)
                
                snowpipe_failures = conn.query(f"""
                    SELECT
                    TO_DATE(c.LAST_LOAD_TIME) AS load_date,
                    c.STATUS AS status,
                    c.TABLE_CATALOG_NAME AS database_name,
                    c.TABLE_SCHEMA_NAME AS schema_name,
                    c.TABLE_NAME AS table_name,
                    CASE WHEN c.PIPE_NAME IS NULL THEN 'COPY' ELSE 'SNOWPIPE' END AS ingest_method,
                    SUM(c.ROW_COUNT) AS row_count,
                    SUM(c.ROW_PARSED) AS rows_parsed,
                    ROUND(SUM(c.FILE_SIZE)/POWER(1024,3), 2) AS total_file_size_gb
                FROM SNOWFLAKE.ACCOUNT_USAGE.COPY_HISTORY c
                WHERE c.STATUS = 'Load failed'
                    AND c.PIPE_NAME IS NOT NULL
                    AND c.LAST_LOAD_TIME >= '{start_date_str}'
                    AND c.LAST_LOAD_TIME <= '{end_date_str}'
                GROUP BY 
                    TO_DATE(c.LAST_LOAD_TIME),
                    c.STATUS,
                    c.TABLE_CATALOG_NAME,
                    c.TABLE_SCHEMA_NAME,
                    c.TABLE_NAME,
                    CASE WHEN c.PIPE_NAME IS NULL THEN 'COPY' ELSE 'SNOWPIPE' END
                HAVING ROUND(SUM(c.FILE_SIZE)/POWER(1024,3), 2) > 0   -- ✅ only include nonzero sizes
                ORDER BY total_file_size_gb DESC
                LIMIT 10;

                """)
                
                if not snowpipe_failures.empty:
                    fig = px.bar(
                    snowpipe_failures, 
                    y="TABLE_NAME", 
                    x="TOTAL_FILE_SIZE_GB",
                    orientation='h',
                    color='TOTAL_FILE_SIZE_GB',
                    labels={
                        "TABLE_NAME": "Table Name",
                        "TOTAL_FILE_SIZE_GB": "Failed Load Size (GB)"
                    },
                    hover_name="TABLE_NAME",
                    hover_data=['TABLE_NAME', 'SCHEMA_NAME', 'TOTAL_FILE_SIZE_GB', 'ROW_COUNT']
                )
                    fig.update_layout(
                    showlegend=False,
                    coloraxis_showscale=False,  # 🔹 hides the blue gradient legend
                    xaxis=dict(
                        showgrid=False,
                        zeroline=False,
                        showticklabels=True,
                        categoryorder="total descending"
                    ),
                    yaxis=dict(
                        showgrid=False,
                        zeroline=False,
                        showticklabels=True
                    ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='IBM Plex Sans', color='#374151'),
                    height=370,
                    margin=dict(l=20, r=20, t=20, b=80),
                    xaxis_tickangle=-45
                )
                    st.plotly_chart(configure_corporate_chart(fig), use_container_width=True)
                else:
                    st.info("No Snowpipe load failures in selected period")
            with col2:
                st.markdown(f'<div style="{container_style}"> Top 10 Failed Loads via COPY Command</div>', unsafe_allow_html=True)
                
                copy_failures = conn.query(f"""
                    SELECT
                        TO_DATE(c.LAST_LOAD_TIME) as load_date,
                        c.STATUS as status,
                        c.TABLE_CATALOG_NAME as database_name,
                        c.TABLE_SCHEMA_NAME as schema_name,
                        c.TABLE_NAME as table_name,
                        CASE WHEN c.PIPE_NAME IS NULL THEN 'COPY' ELSE 'SNOWPIPE' END as ingest_method,
                        SUM(c.ROW_COUNT) as row_count,
                        SUM(c.ROW_PARSED) as rows_parsed,
                        ROUND(SUM(c.FILE_SIZE)/POWER(1024,3), 2) as total_file_size_gb
                    FROM SNOWFLAKE.ACCOUNT_USAGE.COPY_HISTORY c
                    WHERE c.STATUS = 'Load failed'
                        AND c.PIPE_NAME IS NULL
                        AND c.LAST_LOAD_TIME >= '{start_date_str}'
                        AND c.LAST_LOAD_TIME <= '{end_date_str}'
                    GROUP BY 
                        TO_DATE(c.LAST_LOAD_TIME),
                        c.STATUS,
                        c.TABLE_CATALOG_NAME,
                        c.TABLE_SCHEMA_NAME,
                        c.TABLE_NAME,
                        CASE WHEN c.PIPE_NAME IS NULL THEN 'COPY' ELSE 'SNOWPIPE' END
                    HAVING ROUND(SUM(c.FILE_SIZE)/POWER(1024,3), 2) > 0  
                    ORDER BY total_file_size_gb DESC
                    LIMIT 10
                """)
                
                if not copy_failures.empty:
                    fig = px.bar(
                        copy_failures, 
                        y="TABLE_NAME", 
                        x="TOTAL_FILE_SIZE_GB",
                        orientation='h',
                        color='TOTAL_FILE_SIZE_GB',
                        labels={
                            "TABLE_NAME": "Table Name",
                            "TOTAL_FILE_SIZE_GB": "Failed Load Size (GB)"
                        },
                        hover_name="TABLE_NAME",
                        hover_data=['TABLE_NAME', 'SCHEMA_NAME', 'TOTAL_FILE_SIZE_GB', 'ROW_COUNT']
                    )

                    fig.update_layout(
                        showlegend=False,
                        coloraxis_showscale=False,  
                        xaxis=dict(
                            showgrid=False,      
                            zeroline=False,
                            showticklabels=True,
                            categoryorder="total descending"
                        ),
                        yaxis=dict(
                            showgrid=False,          
                            zeroline=False,
                            showticklabels=True
                        ),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(family='IBM Plex Sans', color='#374151'),
                        height=370,
                        margin=dict(l=20, r=20, t=20, b=80),
                    )

                    st.plotly_chart(configure_corporate_chart(fig), use_container_width=True)
                else:
                    st.info("No COPY command load failures in selected period")
            
        except Exception as e:
            st.error(f"⚠️ Error loading miscellaneous analytics: {str(e)}")
            st.info("Please check your Snowflake connection and account permissions.")
    miscellaneous_analytics()