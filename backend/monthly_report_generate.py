import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.ticker as mticker  # Import ticker for formatting
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, Image, Table, TableStyle
)
from datetime import datetime, timedelta
from reportlab.lib import colors
# Import your existing function
from monthlyReport.monthly_zabbix import get_month_zabbix_problem,get_problem_graph,get_month_server_problem,get_month_cpu_usage
from monthlyReport.monthly_zabbix import count_today_problems,count_today_server_problems
from monthlyReport.monthly_uptimekuma import get_down_count_month,get_graph_down_month,get_monitor_down_month
from monthlyReport.monthly_suricata import get_graph_threats,get_threat_summary

zabbix_network_issues = get_month_zabbix_problem()
zabbix_problem_history = get_problem_graph()
zabbix_os_issues = get_month_server_problem()
zabbix_cpu_uses = get_month_cpu_usage()
zabbix_count_problem = count_today_problems()
zabbix_count_server = count_today_server_problems()

uptime_web_issue = json.loads(get_monitor_down_month())
uptime_web_downtime = json.loads(get_graph_down_month())
uptime_count_day = json.loads(get_down_count_month())

suricata_threat = get_threat_summary()
suricata_graph = get_graph_threats()

def generate_report_timestamp():
    now = datetime.now()
    start_time = now - timedelta(days=31)
    
    report_date = now.strftime("%Y-%m-%d")
    data_range = f"{start_time.strftime('%Y-%m-%d %H:%M')} -- {now.strftime('%Y-%m-%d %H:%M')} GMT+7"
    
    return {
        "report_date": report_date,
        "data_range": data_range
    }

timestamps = generate_report_timestamp()
api_response = {
    "report_date": timestamps["report_date"],
    "data_range": timestamps["data_range"],

    "network_issues": zabbix_network_issues.get("network_issues", []),

    'problem_history': zabbix_problem_history.get("problem_history", []),

    "os_issues": zabbix_os_issues.get("os_issues", []),

    "cpu_usage": zabbix_cpu_uses.get("cpu_usage", []),

    "web_issues": uptime_web_issue.get("web_issues", []),

    "web_downtime": uptime_web_downtime.get("web_downtime", []),
 
    "incident_summary": {
        "Network Devices": zabbix_count_problem,
        "Operating Systems": zabbix_count_server,
        "Web Application": uptime_count_day.get("Web Application", [])
    },

    'threats_detected': suricata_threat.get("threats_detected", []),
    'threats_history': suricata_graph.get("threats_history", []),
}
###############################################################################
# 1) Header & Footer Function
###############################################################################
from reportlab.lib import colors

def header_footer(canvas, doc):
    page_width, page_height = A4
    footer_y = 20 

    # ---------------- HEADER ----------------
    canvas.setFont("Helvetica-Bold", 12)
    # Left-aligned: Report title
    canvas.drawString(doc.leftMargin, page_height - 50, "Centralized Monitoring Monthly Report")
    # Right-aligned: Page number
    page_number = f"Page {doc.page}"
    canvas.drawRightString(page_width - doc.rightMargin, page_height - 50, page_number)

    # ---------------- FOOTER ----------------
    canvas.setFont("Helvetica", 10)
    canvas.drawString(doc.leftMargin, footer_y, "Centralized Monitoring Monthly Report")
    canvas.setFont("Helvetica-Bold", 10)
    canvas.setFillColor(colors.red)
    canvas.drawCentredString(page_width / 2, footer_y, "Confidential for internal use")
    canvas.setFillColor(colors.black)  
    report_date = api_response.get("report_date", "Unknown Date")  # Default if missing
    canvas.drawRightString(page_width - doc.rightMargin, footer_y,report_date)

###############################################################################
# 2) Chart-Generating Function
###############################################################################
def generate_chart(data, chart_type, filename, colors_list=None,
                   labels=None, ylim=None, figsize=(6,4), dpi=150):
    plt.figure(figsize=figsize, dpi=dpi)
    
    if chart_type == "bar":
        data.plot(kind="bar", color=colors_list, edgecolor='black')
    elif chart_type == "pie":
        # Pie charts typically use a Series or single column in a DataFrame
        data.plot(kind="pie", autopct="%1.1f%%", colors=colors_list,
                  startangle=140, wedgeprops={'edgecolor': 'black'})
        plt.ylabel("")  # Remove default y-label
    elif chart_type == "line":
        # Each column becomes one line
        for col, color in zip(data.columns, colors_list):
            plt.plot(data.index, data[col], marker="o", label=col,
                     color=color, linewidth=2)
        plt.legend()
    
    if ylim:
        plt.ylim(ylim)
    
    if labels:
        plt.title(labels.get("title", ""), fontsize=14, fontweight='bold')
        plt.xlabel(labels.get("xlabel", ""))
        plt.ylabel(labels.get("ylabel", ""))
    
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight', transparent=True, dpi=dpi)
    plt.close()

###############################################################################
# 3) Main Report-Building Function
###############################################################################
def build_monthy_report(filename):
    chart_files = []
    ###########################################################################
    # A) Create the Document (BaseDocTemplate) and PageTemplate
    ###########################################################################
    doc = BaseDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=30,
        rightMargin=30,
        topMargin=70,     # Enough space for header
        bottomMargin=50   # Enough space for footer
    )
    doc.title = filename
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
    
    template = PageTemplate(id='PageTemplate', frames=[frame], onPage=header_footer)
    doc.addPageTemplates([template])
    styles = getSampleStyleSheet()
    story = []
    
    ###########################################################################
    # B) TITLE PAGE-LIKE CONTENT
    ###########################################################################
    # TITLE PAGE - Dynamically Insert Report Date & Data Range
    story.append(Paragraph("Centralized Monitoring Monthly Report", styles["Title"]))
    story.append(Spacer(1, 0.2*inch))

    # Fetch report date and data range from API response
    report_date = api_response.get("report_date", "Unknown Date")
    data_range = api_response.get("data_range", "No Data Range Provided")

    # Add dynamically retrieved date & data range
    story.append(Paragraph(f"Report Date: {report_date}", styles["Normal"]))
    story.append(Paragraph(f"Data Range: {data_range}", styles["Normal"]))
    story.append(Spacer(1, 0.5*inch))

    
    ###########################################################################
    # C) NETWORK DEVICES SECTION (Table + Line Chart)
    ###########################################################################
    story.append(Paragraph("Network Devices Section", styles["Heading2"]))

    # Fetch network issues data from API response
    network_issues_data = api_response.get("network_issues", [])
    network_table_data = [["Last problem", "Host", "Problem", "Count"]] + network_issues_data
    t_network = Table(
        network_table_data,
        colWidths=[doc.width*0.25, doc.width*0.25, doc.width*0.3, doc.width*0.2]
    )
    t_network.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige)
    ]))

    # Add table to the story
    story.append(t_network)
    story.append(Spacer(1, 0.3*inch))

    # ------------------------------------------------------------------------
    # PROBLEM HISTORY (Dynamic Chart Using API Data)
    # ------------------------------------------------------------------------

    # Fetch problem history data from API response
    api_problem_history = api_response.get("problem_history", {})

    # Define expected time slots for a 24-hour period (every 4 hours)
    time_slots = ["01-05","06-10", "11-15", "16-20", "21-25", "26-31"]

    # Ensure all problem types have complete time slots (fill missing slots with 0s)
    formatted_problem_history = {}
    for problem, values in api_problem_history.items():
        while len(values) < len(time_slots):  # Ensure each problem type has 6 values
            values.append(0)
        if isinstance(values, dict):
            values = list(values.values())  # แปลง Dictionary เป็น List
        elif not isinstance(values, list):
            values = []  # ถ้าไม่ใช่ List ให้ใช้ค่าเริ่มต้นเป็น List ว่าง
        formatted_problem_history[problem] = values[:len(time_slots)]

    # Convert API problem history data to DataFrame with correct structure
    problem_data = pd.DataFrame(formatted_problem_history, index=time_slots)

    # Define chart filename
    problem_chart = "problem_history.png"

    # Generate Problem History line chart dynamically
    plt.figure(figsize=(7, 4), dpi=150)
    for col, color in zip(problem_data.columns, ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]):
        plt.plot(problem_data.index, problem_data[col], marker="o", label=col, color=color, linewidth=2)

    # Format Y-axis as integers (ensuring whole numbers only)
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    # Set labels and title
    plt.title("Problem History", fontsize=14, fontweight='bold')
    plt.xlabel("Days")
    plt.ylabel("Count")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)

    # Save the chart
    plt.tight_layout()
    plt.savefig(problem_chart, bbox_inches='tight', transparent=True, dpi=150)
    plt.close()

    # Keep track of the generated chart file for cleanup later
    chart_files.append(problem_chart)

    # Add Problem History Chart to the Report
    story.append(Paragraph("Problem History", styles["Heading3"]))
    story.append(Image(problem_chart, width=5*inch, height=3*inch))
    story.append(Spacer(1, 0.5*inch))


    
    # ------------------------------------------------------------------------
    # D) OPERATING SYSTEMS SECTION (Table + Line Chart)
    # ------------------------------------------------------------------------

    # Add section title
    story.append(Paragraph("Operating Systems Section", styles["Heading2"]))

    # Fetch operating system issues from API response
    os_data = [["Time", "Host", "Problem", "Duration"]] + api_response.get("os_issues", [])

    # Define table properties
    t_os = Table(
        os_data,
        colWidths=[doc.width * 0.25, doc.width * 0.25, doc.width * 0.3, doc.width * 0.2]
    )
    t_os.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    # Add table to story
    story.append(t_os)
    story.append(Spacer(1, 0.3 * inch))

    # ------------------------------------------------------------------------
    # CPU LOAD CHART (Dynamically Uses API Data)
    # ------------------------------------------------------------------------

    # Fetch CPU usage data from API response
    api_cpu_usage = api_response.get("cpu_usage", {})

    # Define expected time slots for a 24-hour period (every 6 hours)
    time_slots_cpu = ["01-05","06-10", "11-15", "16-20", "21-25", "26-31"]
    # Ensure all hosts have complete time slots (fill missing slots with 0s)
    formatted_cpu_usage = {}
    for host, values in api_cpu_usage.items():
        while len(values) < len(time_slots_cpu):  # Ensure each host has 6 values
            values.append(0)
        formatted_cpu_usage[host] = values[:len(time_slots_cpu)]  # Keep only 6 values

    # Create DataFrame with correct structure
    cpu_data_df = pd.DataFrame(formatted_cpu_usage, index=time_slots_cpu)

    # Define chart filename
    cpu_chart = "cpu_load.png"

    # Generate CPU Load chart dynamically
    plt.figure(figsize=(7, 4), dpi=150)
    for col, color in zip(cpu_data_df.columns, ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]):
        plt.plot(cpu_data_df.index, cpu_data_df[col], marker="o", label=col, color=color, linewidth=2)

    plt.ylim(0, 80)  # Limit scale between 0% and 80%
    # Format Y-axis as percentage (0% - 100%)
    plt.gca().yaxis.set_major_locator(mticker.MultipleLocator(10))  # Steps of 10%
    plt.gca().yaxis.set_major_formatter(mticker.PercentFormatter(xmax=100))  # Format as %

    # Set labels and title
    plt.title("CPU Load Over Time", fontsize=14, fontweight='bold')
    plt.xlabel("Days")
    plt.ylabel("CPU Usage (%)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)

    # Save the chart
    plt.tight_layout()
    plt.savefig(cpu_chart, bbox_inches='tight', transparent=True, dpi=150)
    plt.close()

    # Track chart file for cleanup
    chart_files.append(cpu_chart)

    # Add chart title and image to story
    story.append(Paragraph("CPU Load Over Time", styles["Heading3"]))
    story.append(Image(cpu_chart, width=5 * inch, height=3 * inch))
    story.append(Spacer(1, 0.5 * inch))

    
    # ------------------------------------------------------------------------
    # E) WEB APPLICATION SECTION (Table + Bar Chart)
    # ------------------------------------------------------------------------

    # Add section title
    story.append(Paragraph("Web Application Section", styles["Heading2"]))

    # Fetch web issues data from API response
    web_data = [["Time", "Host", "Status", "Message"]] + api_response.get("web_issues", [])

    # Define table properties
    t_web = Table(
        web_data,
        colWidths=[doc.width * 0.25, doc.width * 0.25, doc.width * 0.2, doc.width * 0.3]
    )
    t_web.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    # Add table to story
    story.append(t_web)
    story.append(Spacer(1, 0.3 * inch))

    # ------------------------------------------------------------------------
    # WEB DOWNTIME CHART (Dynamically Uses API Data)
    # ------------------------------------------------------------------------

    # Fetch web downtime data from API response
    api_web_downtime = api_response.get("web_downtime", {})

    # Define expected time slots for a 24-hour report (6-hour intervals)
    time_slots_web = ["01-05","06-10", "11-15", "16-20", "21-25", "26-31"]

    # Collect all unique web applications from API data
    all_apps = set(api_web_downtime.keys())

    # Ensure all expected apps are included (fill missing apps with zeros)
    formatted_web_downtime = {app: api_web_downtime.get(app, [0] * len(time_slots_web)) for app in all_apps}

    # Create DataFrame with correct structure
    web_downtime_data = pd.DataFrame(formatted_web_downtime, index=time_slots_web)

    # Define chart filename
    web_downtime_chart = "web_downtime.png"

    # Generate Web Downtime chart dynamically (Stacked Bar Chart with Websites as Colors)
    generate_chart(
        data=web_downtime_data,
        chart_type="bar",
        filename=web_downtime_chart,
        colors_list=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"],  # Assign unique colors per website
        labels={"title": "Web Downtime", "xlabel": "Time Slot", "ylabel": "Downtime (minutes)"},
        figsize=(8, 5),
        dpi=150
    )

    # Track chart file for cleanup
    chart_files.append(web_downtime_chart)

    # Add chart title and image to story
    story.append(Paragraph("Web Downtime", styles["Heading3"]))
    story.append(Image(web_downtime_chart, width=5 * inch, height=3 * inch))
    story.append(Spacer(1, 0.5 * inch))

    
    # ------------------------------------------------------------------------
    # F) INCIDENT SUMMARY BY CATEGORY (Table + Pie Chart)
    # ------------------------------------------------------------------------

    # Add section title
    story.append(Paragraph("Incident Summary by Category", styles["Heading2"]))

    # Fetch incident summary data from API response
    incident_summary_data = api_response.get("incident_summary", {})

    # Convert API response into table format
    incident_summary_table_data = [
        ["Category", "Incident Count"],  # Table Headers
    ] + [[key, value] for key, value in incident_summary_data.items()]  # Dynamic Data

    # Define table properties
    t_incident_summary = Table(
        incident_summary_table_data,
        colWidths=[doc.width * 0.5, doc.width * 0.5]  # Two equal columns
    )
    t_incident_summary.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    # Add table to story
    story.append(t_incident_summary)
    story.append(Spacer(1, 0.3 * inch))

    # ------------------------------------------------------------------------
    # INCIDENT SUMMARY PIE CHART (Dynamically Uses API Data)
    # ------------------------------------------------------------------------

    # Convert API incident summary data into Pandas Series for pie chart
    incident_data = pd.Series(incident_summary_data)

    # Define chart filename
    incident_chart = "incident_summary_pie.png"

    # Generate Pie Chart
    generate_chart(
        data=incident_data,
        chart_type="pie",
        filename=incident_chart,
        colors_list=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"],  # Unique colors for each category
        labels={"title": "Issue Count by Section"},
        figsize=(4, 4),
        dpi=150
    )

    # Track chart file for cleanup
    chart_files.append(incident_chart)

    # Add chart title and image to story
    story.append(Paragraph("Issue Count by Section", styles["Heading3"]))
    story.append(Image(incident_chart, width=3 * inch, height=2 * inch))
    story.append(Spacer(1, 0.5 * inch))

    
    # ------------------------------------------------------------------------
    # G) THREATS DETECTED SECTION (Table + Line Chart)
    # ------------------------------------------------------------------------

    # Add section title
    story.append(Paragraph("Threats Detected", styles["Heading2"]))

    # Fetch threats data from API response
    api_threats_data = api_response.get("threats_detected", [])

    # Prepare table data (add headers)
    threats_table_data = [["Time", "Categories of Cyber Threats", "Count"]] + api_threats_data

    # Define table properties
    t_threats = Table(
        threats_table_data,
        colWidths=[doc.width * 0.25, doc.width * 0.5, doc.width * 0.25]
    )
    t_threats.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    # Add table to story
    story.append(t_threats)
    story.append(Spacer(1, 0.3 * inch))

    # ------------------------------------------------------------------------
    # THREATS HISTORY CHART (Dynamically Uses API Data)
    # ------------------------------------------------------------------------

    # Fetch threats history data from API response
    api_threats_history = api_response.get("threats_history", {})

    # Define expected time slots for a 24-hour period (every 4 hours)
    time_slots_threats = ["01-05","06-10", "11-15", "16-20", "21-25", "26-31"]

    # Ensure all threats have complete time slots (fill missing slots with 0s)
    formatted_threats_history = {}
    for threat, values in api_threats_history.items():
        while len(values) < len(time_slots_threats):  # Ensure each threat has 6 values
            values.append(0)
        if threat not in formatted_threats_history:
            formatted_threats_history[threat] = []  # ถ้ายังไม่มี key นี้ ให้สร้าง list เปล่า

        # แปลง dict เป็น list แล้ว slice
        formatted_threats_history[threat] = list(values.values())[:len(time_slots_threats)]

    # Create DataFrame with correct structure
    threats_history_df = pd.DataFrame(formatted_threats_history, index=time_slots_threats)

    # Define chart filename
    threats_chart = "threats_history.png"

    # Generate Threats History line chart dynamically
    plt.figure(figsize=(7, 4), dpi=150)
    for col, color in zip(threats_history_df.columns, ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]):
        plt.plot(threats_history_df.index, threats_history_df[col], marker="o", label=col, color=color, linewidth=2)

    # Format Y-axis as whole numbers
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(integer=True))  # Ensure whole numbers only

    # Set labels and title
    plt.title("Threats History", fontsize=14, fontweight='bold')
    plt.xlabel("Days")
    plt.ylabel("Count")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)

    # Save the chart
    plt.tight_layout()
    plt.savefig(threats_chart, bbox_inches='tight', transparent=True, dpi=150)
    plt.close()
    chart_files.append(threats_chart)
    story.append(Paragraph("Threats History", styles["Heading3"]))
    story.append(Image(threats_chart, width=5 * inch, height=3 * inch))
    story.append(Spacer(1, 0.5 * inch))


    doc.build(story) #Build the PDF

    #Remove Temp File
    for chart_file in chart_files:
        if os.path.exists(chart_file):
            os.remove(chart_file)
