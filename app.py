import os
from io import BytesIO

import dash
from dash import Dash, Input, Output, State, dcc, html
from dash.dash_table import DataTable
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px


# ---------- Sample data ----------
projects_data = [
    # فناوری اطلاعات
    {
        "department": "فناوری اطلاعات",
        "manager": "علی رضایی",
        "project_name": "راه‌اندازی پلتفرم ابری داخلی",
        "start_date": "2025-01-15",
        "status": "در حال انجام",
        "score": 89,
    },
    {
        "department": "فناوری اطلاعات",
        "manager": "علی رضایی",
        "project_name": "اتوماسیون فرایندهای اداری",
        "start_date": "2025-03-02",
        "status": "در حال انجام",
        "score": 92,
    },
    {
        "department": "فناوری اطلاعات",
        "manager": "مریم کریمی",
        "project_name": "به‌روزرسانی زیرساخت شبکه",
        "start_date": "2024-11-20",
        "status": "نزدیک به اتمام",
        "score": 85,
    },
    {
        "department": "فناوری اطلاعات",
        "manager": "مریم کریمی",
        "project_name": "پیاده‌سازی سیستم مانیتورینگ",
        "start_date": "2025-02-10",
        "status": "در حال انجام",
        "score": 81,
    },
    # مالی
    {
        "department": "مالی",
        "manager": "حسین موسوی",
        "project_name": "سیستم مدیریت بودجه",
        "start_date": "2025-01-05",
        "status": "در حال انجام",
        "score": 78,
    },
    {
        "department": "مالی",
        "manager": "حسین موسوی",
        "project_name": "دیجیتالی‌سازی اسناد مالی",
        "start_date": "2024-12-10",
        "status": "در حال انجام",
        "score": 83,
    },
    {
        "department": "مالی",
        "manager": "نگار احمدی",
        "project_name": "بازطراحی ساختار گزارش‌دهی مالی",
        "start_date": "2025-03-12",
        "status": "در حال انجام",
        "score": 80,
    },
    # منابع انسانی
    {
        "department": "منابع انسانی",
        "manager": "سارا محمدی",
        "project_name": "پیاده‌سازی سیستم ارزیابی عملکرد",
        "start_date": "2025-01-25",
        "status": "در حال انجام",
        "score": 90,
    },
    {
        "department": "منابع انسانی",
        "manager": "سارا محمدی",
        "project_name": "برنامه توسعه مهارت مدیران",
        "start_date": "2025-02-18",
        "status": "در حال انجام",
        "score": 88,
    },
    {
        "department": "منابع انسانی",
        "manager": "مجتبی نوری",
        "project_name": "سیستم جذب و استخدام آنلاین",
        "start_date": "2024-12-01",
        "status": "نزدیک به اتمام",
        "score": 86,
    },
    # بازاریابی
    {
        "department": "بازاریابی",
        "manager": "الهام صادقی",
        "project_name": "کمپین دیجیتال برندینگ",
        "start_date": "2025-01-10",
        "status": "در حال انجام",
        "score": 91,
    },
    {
        "department": "بازاریابی",
        "manager": "الهام صادقی",
        "project_name": "تحلیل رفتار مشتریان",
        "start_date": "2025-02-05",
        "status": "در حال انجام",
        "score": 87,
    },
    {
        "department": "بازاریابی",
        "manager": "امیر تقوی",
        "project_name": "طراحی باشگاه مشتریان",
        "start_date": "2024-11-30",
        "status": "در حال انجام",
        "score": 84,
    },
    # تحقیق و توسعه
    {
        "department": "تحقیق و توسعه",
        "manager": "رضا کاظمی",
        "project_name": "پروژه هوش مصنوعی پیش‌بینی فروش",
        "start_date": "2025-01-20",
        "status": "در حال انجام",
        "score": 94,
    },
    {
        "department": "تحقیق و توسعه",
        "manager": "رضا کاظمی",
        "project_name": "تحقیق بازار محصولات جدید",
        "start_date": "2025-03-01",
        "status": "در حال انجام",
        "score": 89,
    },
    {
        "department": "تحقیق و توسعه",
        "manager": "نسیم رستگار",
        "project_name": "آزمایش نمونه اولیه محصول",
        "start_date": "2024-12-15",
        "status": "نزدیک به اتمام",
        "score": 88,
    },
]

df = pd.DataFrame(projects_data)


# ---------- Aggregations ----------
dept_summary = (
    df.groupby("department")
    .agg(
        active_projects=("project_name", "count"),
        avg_score=("score", "mean"),
    )
    .reset_index()
)
dept_summary["avg_score"] = dept_summary["avg_score"].round(1)


def make_bar_figure() -> px.bar:
    fig = px.bar(
        dept_summary,
        x="department",
        y="active_projects",
        labels={"department": "واحد سازمانی", "active_projects": "تعداد پروژه‌ها"},
        color="department",
    )
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=40, r=20, t=30, b=80),
        xaxis_title=None,
        yaxis_title="تعداد پروژه‌ها",
        xaxis_tickangle=-25,
        hovermode="x",
        legend_title_text="واحد سازمانی",
    )
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>تعداد پروژه‌ها: %{y}<extra></extra>",
        marker_line_width=0,
    )
    return fig


def make_line_figure() -> px.line:
    fig = px.line(
        dept_summary,
        x="department",
        y="avg_score",
        markers=True,
        labels={"department": "واحد سازمانی", "avg_score": "میانگین امتیاز"},
    )
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=40, r=20, t=30, b=80),
        xaxis_title=None,
        yaxis_title="میانگین امتیاز",
        xaxis_tickangle=-25,
        hovermode="x",
    )
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>میانگین امتیاز: %{y}<extra></extra>",
        line=dict(color="#2563eb"),
        marker=dict(color="#2563eb", size=8),
    )
    return fig


def make_pie_figure() -> px.pie:
    fig = px.pie(
        dept_summary,
        names="department",
        values="active_projects",
        hole=0.45,
    )
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=40, r=160, t=10, b=10),
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05,
        ),
        legend_title_text="واحد سازمانی",
    )
    fig.update_traces(
        textinfo="percent",
        textposition="inside",
        insidetextorientation="radial",
        hovertemplate="<b>%{label}</b><br>تعداد پروژه‌ها: %{value}<extra></extra>",
    )
    return fig


bar_fig = make_bar_figure()
line_fig = make_line_figure()
pie_fig = make_pie_figure()



# ---------- App setup ----------
external_stylesheets = [dbc.themes.BOOTSTRAP]
app: Dash = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "داشبورد پروژه‌های سازمانی"

# Render/Gunicorn entrypoint
server = app.server

app.index_string = """<!DOCTYPE html>
<html>
<head>
{%%metas%%}
<title>{%%title%%}</title>
{%%favicon%%}
{%%css%%}
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap">
<style>

*,
*::before,
*::after {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
  background: radial-gradient(circle at top left, #111827 0, #020617 45%, #020617 100%);
  font-family: "IRANSans", "Vazirmatn", "Segoe UI", -apple-system, BlinkMacSystemFont,
    "Helvetica Neue", Arial, sans-serif;
  direction: rtl;
}

.app-bg {
  padding: 24px;
}

.app-shell {
  max-width: 1200px;
  margin: 0 auto;
}

.app-row {
  align-items: flex-start;
}

.sidebar-wrapper {
  padding-left: 12px;
}

.sidebar-card {
  background: linear-gradient(145deg, #020617, #0b1120);
  border-radius: 24px;
  padding: 24px 12px;
  box-shadow: 0 18px 45px rgba(15, 23, 42, 0.35);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  height: 100%;
}

.logo-circle {
  width: 40px;
  height: 40px;
  border-radius: 999px;
  background: radial-gradient(circle at 0 0, #f97316, #6366f1);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 16px;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 6px;
  width: 100%;
}

.sidebar-item {
  background: transparent;
  border: none;
  font-size: 13px;
  padding: 8px 12px;
  border-radius: 999px;
  color: #9ca3af;
  cursor: pointer;
  text-align: center;
  transition: background-color 0.15s ease, color 0.15s ease;
  width: 100%;
}

.sidebar-item:hover {
  background-color: rgba(148, 163, 184, 0.2);
  color: #e5e7eb;
}

.sidebar-item.active {
  background: linear-gradient(135deg, #312e81, #4f46e5);
  color: #f9fafb;
}

.main-wrapper {
  padding-right: 12px;
}

.main-card {
  background-color: #f9fafb;
  border-radius: 24px;
  padding: 24px 24px 32px;
  box-shadow: 0 18px 45px rgba(15, 23, 42, 0.18);
}

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
  margin-bottom: 24px;
}

.topbar-heading {
  margin: 0;
  font-size: 22px;
  font-weight: 600;
  color: #111827;
}

.topbar-subtitle {
  margin: 4px 0 0;
  font-size: 13px;
  color: #6b7280;
}

.topbar-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.search-input {
  min-width: 220px;
  font-size: 13px;
  border-radius: 999px;
  border: 1px solid #e5e7eb;
  padding-inline: 16px;
}

.topbar-btn {
  border-radius: 999px;
  font-size: 13px;
  padding-inline: 18px;
  background: linear-gradient(135deg, #2563eb, #4f46e5);
  border: none;
}

.charts-row .chart-card {
  background-color: #ffffff;
  border-radius: 20px;
  padding: 18px 18px 12px;
  height: 100%;
}

/* Ensure Plotly graphs fill cards nicely */
.js-plotly-plot,
.js-plotly-plot .plot-container,
.js-plotly-plot .svg-container {
  width: 100% !important;
}

.card-header-line {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 4px;
}

.card-title {
  font-size: 15px;
  font-weight: 600;
  color: #111827;
}

.card-caption {
  font-size: 12px;
  color: #9ca3af;
  margin: 2px 0 0;
}

.section-card {
  margin-top: 16px;
  padding: 16px 18px 12px;
  border-radius: 20px;
  background-color: #ffffff;
}

.section-header {
  display: flex;
  flex-direction: column;
  margin-bottom: 8px;
}

.section-header-inline {
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.stat-cards {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 16px;
}

.stat-card {
  background: linear-gradient(135deg, #0f172a, #1f2937);
  border-radius: 18px;
  padding: 12px 14px;
  color: #e5e7eb;
  box-shadow: 0 14px 30px rgba(15, 23, 42, 0.5);
}

.stat-label {
  margin: 0 0 4px;
  font-size: 12px;
  color: #9ca3af;
}

.stat-value {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.filter-row {
  margin-bottom: 12px;
}

.filter-label {
  font-size: 13px;
  color: #4b5563;
  margin-bottom: 4px;
}

.filter-caption {
  margin-top: 4px;
  font-size: 12px;
  color: #6b7280;
}

.export-btn {
  border-radius: 999px;
}

/* Dash DataTable tweaks for cleaner look */
.dash-table-container .dash-spreadsheet-container table {
  border-collapse: collapse !important;
}

.dash-table-container .dash-spreadsheet-container th,
.dash-table-container .dash-spreadsheet-container td {
  border: none !important;
  font-size: 13px;
}

.dash-table-container .dash-spreadsheet-container tr:hover td {
  background-color: #eef2ff !important;
}

.dash-table-container .dash-spreadsheet-container tr:first-child th {
  border-bottom: 1px solid #e5e7eb !important;
}

@media (max-width: 992px) {
  .app-bg {
    padding: 12px;
  }

  .stat-cards {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .sidebar-wrapper {
    padding-left: 0;
    margin-bottom: 12px;
  }

  .sidebar-card {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    padding: 12px 14px;
    border-radius: 20px;
    gap: 10px;
  }

  .sidebar-nav {
    flex-direction: row;
    gap: 8px;
    width: auto;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    padding-bottom: 2px;
  }

  .sidebar-item {
    width: auto;
    white-space: nowrap;
    padding: 8px 14px;
  }

  .sidebar-logo {
    margin-bottom: 0 !important;
  }

  .main-wrapper {
    padding-right: 0;
  }

  .app-shell {
    max-width: 100%;
  }
}

@media (max-width: 576px) {
  .stat-cards {
    grid-template-columns: 1fr;
  }

  .charts-row .chart-card {
    padding: 12px;
  }

  .topbar-actions {
    width: 100%;
  }

  .search-input {
    min-width: 0;
    width: 100%;
  }
}


</style>
</head>
<body>
{%%app_entry%%}
<footer>
{%%config%%}
{%%scripts%%}
{%%renderer%%}
</footer>
</body>
</html>"""


def make_table_style():
    return {
        "style_header": {
            "backgroundColor": "#f5f5f5",
            "fontWeight": "bold",
            "border": "1px solid #ddd",
        },
        "style_cell": {
            "textAlign": "right",
            "padding": "8px",
            "border": "1px solid #eee",
            "fontFamily": "IRANSans, Vazirmatn, Segoe UI, sans-serif",
            "fontSize": "13px",
        },
        "style_table": {
            "width": "100%",
            "overflowX": "auto",
        },
        "style_data_conditional": [
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "#f9fafb",
            },
            {
                "if": {"filter_query": "{score} >= 85", "column_id": "score"},
                "backgroundColor": "#dcfce7",
                "color": "#166534",
                "fontWeight": "600",
            },
            {
                "if": {
                    "filter_query": "{score} >= 70 && {score} < 85",
                    "column_id": "score",
                },
                "backgroundColor": "#fef9c3",
                "color": "#854d0e",
                "fontWeight": "600",
            },
            {
                "if": {"filter_query": "{score} < 70", "column_id": "score"},
                "backgroundColor": "#fee2e2",
                "color": "#991b1b",
                "fontWeight": "600",
            },
        ],
    }


base_table_style = make_table_style()


app.layout = html.Div(
    className="app-bg",
    children=[
        dcc.Store(id="selected-department"),
        dbc.Container(
            fluid=True,
            className="app-shell",
            children=[
                dbc.Row(
                    className="g-0 app-row",
                    children=[
                        # Sidebar
                        dbc.Col(
                            className="sidebar-wrapper",
                            md=2,
                            children=[
                                html.Div(
                                    className="sidebar-card",
                                    children=[
                                        html.Div(
                                            className="sidebar-logo mb-4",
                                            children=html.Div("DP", className="logo-circle"),
                                        ),
                                        html.Div(
                                            className="sidebar-nav",
                                            children=[
                                                html.Button(
                                                    "نمای کلی",
                                                    id="nav-overview",
                                                    n_clicks=0,
                                                    className="sidebar-item active",
                                                ),
                                                html.Button(
                                                    "پروژه‌ها",
                                                    id="nav-projects",
                                                    n_clicks=0,
                                                    className="sidebar-item",
                                                ),
                                                html.Button(
                                                    "تسک‌ها",
                                                    id="nav-tasks",
                                                    n_clicks=0,
                                                    className="sidebar-item",
                                                ),
                                                html.Button(
                                                    "اعضا",
                                                    id="nav-members",
                                                    n_clicks=0,
                                                    className="sidebar-item",
                                                ),
                                                html.Button(
                                                    "تنظیمات",
                                                    id="nav-settings",
                                                    n_clicks=0,
                                                    className="sidebar-item",
                                                ),
                                            ],
                                        ),
                                    ],
                                )
                            ],
                        ),
                        # Main content
                        dbc.Col(
                            md=10,
                            className="main-wrapper",
                            children=[
                                # Stats cards row
                                html.Div(
                                    className="stat-cards",
                                    children=[
                                        html.Div(
                                            className="stat-card",
                                            children=[
                                                html.P("تعداد کل پروژه‌ها", className="stat-label"),
                                                html.H3(id="stat-total-projects", className="stat-value"),
                                            ],
                                        ),
                                        html.Div(
                                            className="stat-card",
                                            children=[
                                                html.P("میانگین امتیاز کل", className="stat-label"),
                                                html.H3(id="stat-avg-score", className="stat-value"),
                                            ],
                                        ),
                                        html.Div(
                                            className="stat-card",
                                            children=[
                                                html.P("تعداد واحدها", className="stat-label"),
                                                html.H3(id="stat-dept-count", className="stat-value"),
                                            ],
                                        ),
                                        html.Div(
                                            className="stat-card",
                                            children=[
                                                html.P("تعداد مدیران", className="stat-label"),
                                                html.H3(id="stat-manager-count", className="stat-value"),
                                            ],
                                        ),
                                    ],
                                ),
                                # Overview page (default)
                                html.Div(
                                    id="overview-content",
                                    className="main-card",
                                    children=[
                                        # Top bar
                                        html.Div(
                                            className="topbar",
                                            children=[
                                                html.Div(
                                                    className="topbar-title",
                                                    children=[
                                                        html.H2(
                                                            "نمای کلی",
                                                            className="topbar-heading",
                                                        ),
                                                        html.P(
                                                            "مروری بر پروژه‌های فعال سازمان و عملکرد واحدها",
                                                            className="topbar-subtitle",
                                                        ),
                                                    ],
                                                ),
                                                html.Div(
                                                    className="topbar-actions",
                                                    children=[
                                                        dbc.Input(
                                                            type="search",
                                                            placeholder="جستجو در پروژه‌ها...",
                                                            className="search-input",
                                                        ),
                                                        dbc.Button(
                                                            "گزارش این هفته",
                                                            color="primary",
                                                            className="topbar-btn",
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            className="filter-row",
                                            children=[
                                                html.Div(
                                                    className="filter-label",
                                                    children="فیلتر بر اساس امتیاز پروژه‌ها",
                                                ),
                                                dcc.RangeSlider(
                                                    id="score-range",
                                                    min=60,
                                                    max=100,
                                                    step=1,
                                                    value=[score_min, score_max],
                                                    allowCross=False,
                                                    marks={
                                                        60: "60",
                                                        70: "70",
                                                        80: "80",
                                                        90: "90",
                                                        100: "100",
                                                    },
                                                ),
                                                html.Div(
                                                    id="score-range-text",
                                                    className="filter-caption",
                                                ),
                                            ],
                                        ),
                                        # Charts row
                                        dbc.Row(
                                            className="charts-row gy-3 mb-4",
                                            children=[
                                                dbc.Col(
                                                    md=7,
                                                    children=html.Div(
                                                        className="chart-card",
                                                        children=[
                                                            html.Div(
                                                                className="card-header-line",
                                                                children=[
                                                                    html.Div(
                                                                        [
                                                                            html.H5(
                                                                                "پروژه‌های فعال",
                                                                                className="card-title",
                                                                            ),
                                                                            html.P(
                                                                                "تعداد پروژه‌ها به تفکیک واحد سازمانی",
                                                                                className="card-caption",
                                                                            ),
                                                                        ]
                                                                    ),
                                                                ],
                                                            ),
                                                            dcc.Graph(
                                                                id="projects-per-dept-bar",
                                                                figure=initial_bar_fig,
                                                                responsive=True,
                                                                config={"displayModeBar": False, "responsive": True},
                                                            ),
                                                        ],
                                                    ),
                                                ),
                                                dbc.Col(
                                                    md=5,
                                                    children=html.Div(
                                                        className="chart-card",
                                                        children=[
                                                            html.Div(
                                                                className="card-header-line",
                                                                children=[
                                                                    html.Div(
                                                                        [
                                                                            html.H5(
                                                                                "میانگین امتیاز",
                                                                                className="card-title",
                                                                            ),
                                                                            html.P(
                                                                                "امتیاز کیفی پروژه‌ها در هر واحد",
                                                                                className="card-caption",
                                                                            ),
                                                                        ]
                                                                    ),
                                                                ],
                                                            ),
                                                            dcc.Graph(
                                                                id="avg-score-line",
                                                                figure=initial_line_fig,
                                                                responsive=True,
                                                                config={"displayModeBar": False, "responsive": True},
                                                            ),
                                                        ],
                                                    ),
                                                ),
                                            ],
                                        ),
                                        # Pie chart row (full width to avoid overlap)
                                        dbc.Row(
                                            className="gy-3 mb-3",
                                            children=[
                                                dbc.Col(
                                                    md=12,
                                                    children=html.Div(
                                                        className="chart-card",
                                                        children=[
                                                            html.Div(
                                                                className="card-header-line",
                                                                children=[
                                                                    html.Div(
                                                                        [
                                                                            html.H5(
                                                                                "سهم واحدها از پروژه‌ها",
                                                                                className="card-title",
                                                                            ),
                                                                            html.P(
                                                                                "درصد پروژه‌های هر واحد از کل پروژه‌ها",
                                                                                className="card-caption",
                                                                            ),
                                                                        ]
                                                                    ),
                                                                ],
                                                            ),
                                                            dcc.Graph(
                                                                id="dept-share-pie",
                                                                figure=initial_pie_fig,
                                                                responsive=True,
                                                                config={"displayModeBar": False, "responsive": True},
                                                            ),
                                                        ],
                                                    ),
                                                ),
                                            ],
                                        ),
                                        # Managers table (level 2)
                                        html.Div(
                                            id="dept-managers-section",
                                            className="section-card",
                                            children=[
                                                html.Div(
                                                    className="section-header",
                                                    children=[
                                                        html.H5(
                                                            "مدیران پروژه در واحد انتخاب‌شده",
                                                            className="card-title mb-1",
                                                        ),
                                                        html.P(
                                                            "برای مشاهده جزئیات، ابتدا روی نوار واحد سازمانی در نمودار بالا کلیک کنید.",
                                                            id="dept-hint-text",
                                                            className="card-caption",
                                                        ),
                                                    ],
                                                ),
                                                DataTable(
                                                    id="dept-managers-table",
                                                    columns=[
                                                        {"name": "مدیر پروژه", "id": "manager"},
                                                        {"name": "تعداد پروژه‌ها", "id": "project_count"},
                                                        {"name": "میانگین امتیاز", "id": "avg_score"},
                                                    ],
                                                    data=[],
                                                    row_selectable=False,
                                                    cell_selectable=True,
                                                    **base_table_style,
                                                ),
                                            ],
                                            style={"display": "none"},
                                        ),
                                        # Manager projects table (level 3)
                                        html.Div(
                                            id="manager-projects-section",
                                            className="section-card",
                                            children=[
                                                html.Div(
                                                    className="section-header",
                                                    children=[
                                                        html.H5(
                                                            "جزئیات پروژه‌های مدیر انتخاب‌شده",
                                                            className="card-title mb-1",
                                                        ),
                                                        html.P(
                                                            "برای مشاهده جزئیات یک مدیر، روی نام او در جدول بالا کلیک کنید.",
                                                            id="manager-hint-text",
                                                            className="card-caption",
                                                        ),
                                                    ],
                                                ),
                                                DataTable(
                                                    id="manager-projects-table",
                                                    columns=[
                                                        {"name": "نام پروژه", "id": "project_name"},
                                                        {"name": "تاریخ شروع", "id": "start_date"},
                                                        {"name": "وضعیت", "id": "status"},
                                                        {"name": "امتیاز", "id": "score"},
                                                    ],
                                                    data=[],
                                                    row_selectable=False,
                                                    cell_selectable=False,
                                                    **base_table_style,
                                                ),
                                            ],
                                            style={"display": "none"},
                                        ),
                                    ],
                                ),
                                # Projects page
                                html.Div(
                                    id="projects-content",
                                    className="main-card",
                                    style={"display": "none"},
                                    children=[
                                        html.Div(
                                            className="topbar",
                                            children=[
                                                html.Div(
                                                    className="topbar-title",
                                                    children=[
                                                        html.H2(
                                                            "پروژه‌ها",
                                                            className="topbar-heading",
                                                        ),
                                                        html.P(
                                                            "لیست همه پروژه‌ها به همراه واحد، مدیر و وضعیت.",
                                                            className="topbar-subtitle",
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            className="section-card",
                                            children=[
                                                html.Div(
                                                    className="section-header section-header-inline",
                                                    children=[
                                                        html.Div(
                                                            "لیست پروژه‌ها (با اعمال فیلتر امتیاز)",
                                                            className="card-caption",
                                                        ),
                                                        dbc.Button(
                                                            "دانلود اکسل",
                                                            id="download-projects-btn",
                                                            color="secondary",
                                                            size="sm",
                                                            className="export-btn",
                                                        ),
                                                        dcc.Download(id="projects-download"),
                                                    ],
                                                ),
                                                DataTable(
                                                    id="all-projects-table",
                                                    columns=[
                                                        {"name": "واحد سازمانی", "id": "department"},
                                                        {"name": "مدیر پروژه", "id": "manager"},
                                                        {"name": "نام پروژه", "id": "project_name"},
                                                        {"name": "تاریخ شروع", "id": "start_date"},
                                                        {"name": "وضعیت", "id": "status"},
                                                        {"name": "امتیاز", "id": "score"},
                                                    ],
                                                    data=df.to_dict("records"),
                                                    row_selectable=False,
                                                    cell_selectable=False,
                                                    sort_action="native",
                                                    **base_table_style,
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                # Tasks page (status-focused)
                                html.Div(
                                    id="tasks-content",
                                    className="main-card",
                                    style={"display": "none"},
                                    children=[
                                        html.Div(
                                            className="topbar",
                                            children=[
                                                html.Div(
                                                    className="topbar-title",
                                                    children=[
                                                        html.H2(
                                                            "وضعیت پروژه‌ها",
                                                            className="topbar-heading",
                                                        ),
                                                        html.P(
                                                            "نمایی از تعداد پروژه‌ها بر اساس وضعیت اجرا.",
                                                            className="topbar-subtitle",
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            className="section-card",
                                            children=DataTable(
                                                id="status-summary-table",
                                                columns=[
                                                    {"name": "وضعیت", "id": "status"},
                                                    {"name": "تعداد پروژه‌ها", "id": "project_count"},
                                                ],
                                                data=(
                                                    df.groupby("status")
                                                    .agg(project_count=("project_name", "count"))
                                                    .reset_index()
                                                ).to_dict("records"),
                                                row_selectable=False,
                                                cell_selectable=False,
                                                **base_table_style,
                                            ),
                                        ),
                                    ],
                                ),
                                # Members page
                                html.Div(
                                    id="members-content",
                                    className="main-card",
                                    style={"display": "none"},
                                    children=[
                                        html.Div(
                                            className="topbar",
                                            children=[
                                                html.Div(
                                                    className="topbar-title",
                                                    children=[
                                                        html.H2(
                                                            "مدیران پروژه",
                                                            className="topbar-heading",
                                                        ),
                                                        html.P(
                                                            "لیست مدیران پروژه به همراه واحد و عملکرد آن‌ها.",
                                                            className="topbar-subtitle",
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            className="section-card",
                                            children=DataTable(
                                                id="managers-summary-table",
                                                columns=[
                                                    {"name": "مدیر پروژه", "id": "manager"},
                                                    {"name": "واحد سازمانی", "id": "department"},
                                                    {"name": "تعداد پروژه‌ها", "id": "project_count"},
                                                    {"name": "میانگین امتیاز", "id": "avg_score"},
                                                ],
                                                data=(
                                                    df.groupby(["manager", "department"])
                                                    .agg(
                                                        project_count=("project_name", "count"),
                                                        avg_score=("score", "mean"),
                                                    )
                                                    .reset_index()
                                                    .assign(avg_score=lambda d: d["avg_score"].round(1))
                                                ).to_dict("records"),
                                                row_selectable=False,
                                                cell_selectable=False,
                                                **base_table_style,
                                            ),
                                        ),
                                    ],
                                ),
                                # Settings page (simple visual settings description)
                                html.Div(
                                    id="settings-content",
                                    className="main-card",
                                    style={"display": "none"},
                                    children=[
                                        html.Div(
                                            className="topbar",
                                            children=[
                                                html.Div(
                                                    className="topbar-title",
                                                    children=[
                                                        html.H2(
                                                            "تنظیمات داشبورد",
                                                            className="topbar-heading",
                                                        ),
                                                        html.P(
                                                            "برخی تنظیمات پیشنهادی ظاهری و نمایشی برای این داشبورد نمونه.",
                                                            className="topbar-subtitle",
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            className="section-card",
                                            children=[
                                                html.P(
                                                    "این نسخه‌ی نمونه است؛ در یک نسخه‌ی واقعی، می‌توانید از این بخش برای تغییر بازه‌ی زمانی پیش‌فرض، فیلتر واحدها، و تنظیمات تم گراف‌ها استفاده کنید.",
                                                    className="card-caption mb-2",
                                                ),
                                                html.Ul(
                                                    [
                                                        html.Li("بازه‌ی زمانی پیش‌فرض نمودارها: «هفته جاری»."),
                                                        html.Li("حالت نمایش: راست‌به‌چپ برای زبان فارسی."),
                                                        html.Li("تم رنگی ملایم برای نمودارها و کارت‌ها."),
                                                    ],
                                                    style={"fontSize": "13px", "color": "#4b5563"},
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                )
            ],
        ),
    ],
)


# ---------- Callbacks ----------
@app.callback(
    Output("nav-overview", "className"),
    Output("nav-projects", "className"),
    Output("nav-tasks", "className"),
    Output("nav-members", "className"),
    Output("nav-settings", "className"),
    Output("overview-content", "style"),
    Output("projects-content", "style"),
    Output("tasks-content", "style"),
    Output("members-content", "style"),
    Output("settings-content", "style"),
    Input("nav-overview", "n_clicks"),
    Input("nav-projects", "n_clicks"),
    Input("nav-tasks", "n_clicks"),
    Input("nav-members", "n_clicks"),
    Input("nav-settings", "n_clicks"),
)
def switch_page(overview_clicks, projects_clicks, tasks_clicks, members_clicks, settings_clicks):
    ctx = dash.callback_context
    active_id = "nav-overview"
    if ctx.triggered:
        active_id = ctx.triggered[0]["prop_id"].split(".")[0] or "nav-overview"

    base_class = "sidebar-item"

    def cls(item_id):
        return f"{base_class} active" if item_id == active_id else base_class

    overview_style = {"display": "block"} if active_id == "nav-overview" else {"display": "none"}
    projects_style = {"display": "block"} if active_id == "nav-projects" else {"display": "none"}
    tasks_style = {"display": "block"} if active_id == "nav-tasks" else {"display": "none"}
    members_style = {"display": "block"} if active_id == "nav-members" else {"display": "none"}
    settings_style = {"display": "block"} if active_id == "nav-settings" else {"display": "none"}

    return (
        cls("nav-overview"),
        cls("nav-projects"),
        cls("nav-tasks"),
        cls("nav-members"),
        cls("nav-settings"),
        overview_style,
        projects_style,
        tasks_style,
        members_style,
        settings_style,
    )


@app.callback(
    Output("projects-per-dept-bar", "figure"),
    Output("avg-score-line", "figure"),
    Output("dept-share-pie", "figure"),
    Output("stat-total-projects", "children"),
    Output("stat-avg-score", "children"),
    Output("stat-dept-count", "children"),
    Output("stat-manager-count", "children"),
    Output("score-range-text", "children"),
    Input("score-range", "value"),
)
def update_overview_figures(score_range):
    if not score_range:
        flt = df.copy()
        current_range = (score_min, score_max)
    else:
        lo, hi = score_range
        flt = df[(df["score"] >= lo) & (df["score"] <= hi)]
        current_range = (lo, hi)

    if flt.empty:
        # اگر فیلتر خیلی محدود بود، برای نمودارها دیتای خالی نشان می‌دهیم
        bar = build_bar_figure(df.iloc[0:0])
        line = build_line_figure(df.iloc[0:0])
        pie = build_pie_figure(df.iloc[0:0])
        total_projects = "۰"
        avg_score_text = "—"
        dept_count_text = "۰"
        manager_count_text = "۰"
    else:
        bar = build_bar_figure(flt)
        line = build_line_figure(flt)
        pie = build_pie_figure(flt)
        total_projects = f"{len(flt):,}".replace(",", "٬")
        avg_score_text = f"{flt['score'].mean():.1f}"
        dept_count_text = f"{flt['department'].nunique()}"
        manager_count_text = f"{flt['manager'].nunique()}"

    range_text = f"نمایش پروژه‌ها با امتیاز بین {current_range[0]} تا {current_range[1]}"

    return (
        bar,
        line,
        pie,
        total_projects,
        avg_score_text,
        dept_count_text,
        manager_count_text,
        range_text,
    )


@app.callback(
    Output("dept-managers-section", "style"),
    Output("dept-managers-table", "data"),
    Output("dept-hint-text", "children"),
    Output("selected-department", "data"),
    Input("projects-per-dept-bar", "clickData"),
    Input("score-range", "value"),
    State("dept-managers-section", "style"),
)
def update_managers_table(click_data, score_range, current_style):
    style = dict(current_style or {})
    if not click_data or "points" not in click_data or not click_data["points"]:
        style["display"] = "none"
        return (
            style,
            [],
            "برای مشاهده مدیران، روی نوار واحد سازمانی در نمودار بالا کلیک کنید.",
            None,
        )

    selected_department = click_data["points"][0]["x"]

    lo, hi = score_range or (score_min, score_max)
    filtered = df[
        (df["department"] == selected_department)
        & (df["score"] >= lo)
        & (df["score"] <= hi)
    ]
    if filtered.empty:
        style["display"] = "none"
        return (
            style,
            [],
            "برای این واحد، داده‌ای ثبت نشده است.",
            None,
        )

    managers_summary = (
        filtered.groupby("manager")
        .agg(
            project_count=("project_name", "count"),
            avg_score=("score", "mean"),
        )
        .reset_index()
    )
    managers_summary["avg_score"] = managers_summary["avg_score"].round(1)

    data = managers_summary.to_dict("records")
    style["display"] = "block"
    hint = f"واحد انتخاب‌شده: {selected_department} — برای مشاهده جزئیات، روی نام مدیر کلیک کنید."

    return style, data, hint, selected_department


@app.callback(
    Output("manager-projects-section", "style"),
    Output("manager-projects-table", "data"),
    Output("manager-hint-text", "children"),
    Input("dept-managers-table", "active_cell"),
    State("dept-managers-table", "data"),
    State("selected-department", "data"),
    State("manager-projects-section", "style"),
    State("score-range", "value"),
)
def update_manager_projects_table(active_cell, table_data, selected_department, current_style, score_range):
    style = dict(current_style or {})

    if not active_cell or table_data is None or selected_department is None:
        style["display"] = "none"
        return (
            style,
            [],
            "برای مشاهده جزئیات یک مدیر، روی نام او در جدول بالا کلیک کنید.",
        )

    row_index = active_cell.get("row")
    if row_index is None or row_index >= len(table_data):
        style["display"] = "none"
        return (
            style,
            [],
            "انتخاب نامعتبر است؛ لطفاً مجدداً یکی از مدیران را انتخاب کنید.",
        )

    selected_manager = table_data[row_index].get("manager")
    if not selected_manager:
        style["display"] = "none"
        return (
            style,
            [],
            "برای مشاهده جزئیات یک مدیر، روی نام او در جدول بالا کلیک کنید.",
        )

    lo, hi = score_range or (score_min, score_max)
    subset = df[
        (df["department"] == selected_department)
        & (df["manager"] == selected_manager)
        & (df["score"] >= lo)
        & (df["score"] <= hi)
    ][["project_name", "start_date", "status", "score"]].copy()

    if subset.empty:
        style["display"] = "none"
        return (
            style,
            [],
            "برای این مدیر در واحد انتخاب‌شده، پروژه فعالی ثبت نشده است.",
        )

    style["display"] = "block"
    hint = f"مدیر انتخاب‌شده: {selected_manager} — تعداد پروژه‌ها: {len(subset)}"

    return style, subset.to_dict("records"), hint


@app.callback(
    Output("projects-download", "data"),
    Input("download-projects-btn", "n_clicks"),
    State("score-range", "value"),
    prevent_initial_call=True,
)
def download_projects(n_clicks, score_range):
    lo, hi = score_range or (score_min, score_max)
    flt = df[(df["score"] >= lo) & (df["score"] <= hi)].copy()
    flt = flt.sort_values(["department", "manager", "score"], ascending=[True, True, False])
    return dcc.send_data_frame(flt.to_excel, "projects.xlsx", index=False)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8050"))
    app.run(host="0.0.0.0", port=port, debug=True)

