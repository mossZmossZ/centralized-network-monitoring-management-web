import os
import pandas as pd
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, Image, Table, TableStyle
)

###############################################################################
# 1) Header & Footer Function
###############################################################################
def header_footer(canvas, doc):
    """
    Draws the header and footer on each page.
    'doc.page' gives the current page number.
    """
    # Header (top of page)
    canvas.setFont("Helvetica-Bold", 12)
    # Left side: "Centralized Monitoring Daily Report"
    canvas.drawString(doc.leftMargin, A4[1] - 50, "Centralized Monitoring Daily Report")
    # Right side: page number
    page_number = f"Page {doc.page}"
    canvas.drawRightString(A4[0] - doc.rightMargin, A4[1] - 50, page_number)

    # Footer (bottom of page)
    canvas.setFont("Helvetica", 10)
    footer_y = 20  # 20 points from the bottom
    # Left-aligned text
    canvas.drawString(doc.leftMargin, footer_y, "Centralized Monitoring Daily Report")
    # Right-aligned text
    canvas.drawRightString(A4[0] - doc.rightMargin, footer_y, "Report Date: 2025-02-10")

###############################################################################
# 2) Chart-Generating Function
###############################################################################
def generate_chart(data, chart_type, filename, colors_list=None,
                   labels=None, ylim=None, figsize=(6,4), dpi=150):
    """
    Generates and saves a chart (bar, pie, line) as an image file using Matplotlib.
    """
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
def build_report(filename):
    """
    Creates a multi-page PDF that automatically flows content,
    with repeated header and footer on each page, and includes charts.
    """
    # List of generated chart files to remove later
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
    
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
    
    template = PageTemplate(id='PageTemplate', frames=[frame], onPage=header_footer)
    doc.addPageTemplates([template])
    
    # We'll build up a list of Flowables (story) in order
    styles = getSampleStyleSheet()
    story = []
    
    ###########################################################################
    # B) TITLE PAGE-LIKE CONTENT
    ###########################################################################
    story.append(Paragraph("Centralized Monitoring Daily Report", styles["Title"]))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Report Date: 2025-02-10", styles["Normal"]))
    story.append(Paragraph("Data Range: 2025-02-09 13:00 -- 2025-02-10 12:59 GMT+7", styles["Normal"]))
    story.append(Spacer(1, 0.5*inch))
    
    ###########################################################################
    # C) NETWORK DEVICES SECTION (Table + Line Chart)
    ###########################################################################
    story.append(Paragraph("Network Devices Section", styles["Heading2"]))
    
    network_data = [
        ["Time", "Host", "Problem", "Duration"],
        ["2025-03-10 12:47:49 PM", "Switch 3750 Comcenter",
         "Interface Gi1/0/40(): Link down", "2d 4h 59m"]
    ]
    t_network = Table(
        network_data,
        colWidths=[doc.width*0.25, doc.width*0.25, doc.width*0.3, doc.width*0.2]
    )
    t_network.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    story.append(t_network)
    story.append(Spacer(1, 0.3*inch))
    
    # Problem History (LINE CHART)
    problem_data = pd.DataFrame({
        "Link Down": [4, 3, 3, 5],
        "Speed Change": [2, 4, 2, 3],
        "Port Failure": [2, 3, 4, 5]
    }, index=["28/2/2025 21:13", "30/2/2025 21:13:58", "X", "Y"])
    
    problem_chart = "problem_history.png"
    generate_chart(
        data=problem_data,
        chart_type="line",
        filename=problem_chart,
        colors_list=["#1f77b4", "#ff7f0e", "#2ca02c"],
        labels={"title": "Problem History"},
        ylim=(0, 6),
        figsize=(5, 3),
        dpi=150
    )
    chart_files.append(problem_chart)
    
    story.append(Paragraph("Problem History", styles["Heading3"]))
    story.append(Image(problem_chart, width=5*inch, height=3*inch))
    story.append(Spacer(1, 0.5*inch))
    
    ###########################################################################
    # D) OPERATING SYSTEMS SECTION (Table + Line Chart)
    ###########################################################################
    story.append(Paragraph("Operating Systems Section", styles["Heading2"]))
    
    os_data = [
        ["Time", "Host", "Problem", "Duration"],
        ["2025-02-28 09:13:58 PM", "Host1", "High CPU Load", "12h 30m"],
        ["2025-02-28 10:15:22 PM", "Host2", "Memory Usage High", "8h 20m"]
    ]
    t_os = Table(
        os_data,
        colWidths=[doc.width*0.25, doc.width*0.25, doc.width*0.3, doc.width*0.2]
    )
    t_os.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    story.append(t_os)
    story.append(Spacer(1, 0.3*inch))
    
    # CPU Load (LINE CHART)
    cpu_data = pd.DataFrame({
        "Host1": [30, 50, 70, 90],
        "Host2": [20, 60, 40, 80],
        "Host3": [50, 60, 80, 90]
    }, index=["00:00", "06:00", "12:00", "18:00"])
    
    cpu_chart = "cpu_load.png"
    generate_chart(
        data=cpu_data,
        chart_type="line",
        filename=cpu_chart,
        colors_list=["#1f77b4", "#ff7f0e", "#2ca02c"],
        labels={"title": "CPU Load Over Time"},
        ylim=(0, 100),
        figsize=(5, 3),
        dpi=150
    )
    chart_files.append(cpu_chart)
    
    story.append(Paragraph("CPU Load Over Time", styles["Heading3"]))
    story.append(Image(cpu_chart, width=5*inch, height=3*inch))
    story.append(Spacer(1, 0.5*inch))
    
    ###########################################################################
    # E) WEB APPLICATION SECTION (Table + Bar Chart)
    ###########################################################################
    story.append(Paragraph("Web Application Section", styles["Heading2"]))
    
    web_data = [
        ["Time", "Host", "Status", "Massage"],
        ["2025-03-11 11:06:28", "ECE ENG", "Down", "Request failed with status code 500"]
    ]
    t_web = Table(
        web_data,
        colWidths=[doc.width*0.25, doc.width*0.25, doc.width*0.2, doc.width*0.3]
    )
    t_web.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    story.append(t_web)
    story.append(Spacer(1, 0.3*inch))
    
    web_downtime_data = pd.DataFrame({
        "ECE ENG": [2, 3, 4, 5],
        "ENG KMUTNB": [3, 4, 2, 1],
        "ECC": [4, 3, 2, 5]
    }, index=["Web App 1", "Web App 2", "Web App 3", "Web App 4"])
    
    web_downtime_chart = "web_downtime.png"
    generate_chart(
        data=web_downtime_data,
        chart_type="bar",
        filename=web_downtime_chart,
        colors_list=["#1f77b4", "#ff7f0e", "#2ca02c"],
        labels={"title": "Web Downtime"},
        figsize=(7, 4),
        dpi=150
    )
    chart_files.append(web_downtime_chart)
    
    story.append(Paragraph("Web Downtime", styles["Heading3"]))
    story.append(Image(web_downtime_chart, width=5*inch, height=3*inch))
    story.append(Spacer(1, 0.5*inch))
    
    ###########################################################################
    # F) INCIDENT SUMMARY BY CATEGORY (Pie Chart)
    ###########################################################################
    story.append(Paragraph("Incident Summary by Category", styles["Heading2"]))
    
    incident_data = pd.Series({
        "Network Devices": 10,
        "Operating Systems": 5,
        "Web Application": 3
    })
    incident_chart = "incident_summary_pie.png"
    generate_chart(
        data=incident_data,
        chart_type="pie",
        filename=incident_chart,
        colors_list=["#1f77b4", "#ff7f0e", "#2ca02c"],
        labels={"title": "Issue Count by Section"},
        figsize=(4,4),
        dpi=150
    )
    chart_files.append(incident_chart)
    
    story.append(Paragraph("Issue Count by Section", styles["Heading3"]))
    story.append(Image(incident_chart, width=3*inch, height=3*inch))
    story.append(Spacer(1, 0.5*inch))
    
    ###########################################################################
    # G) THREATS DETECTED SECTION (Table + Line Chart)
    ###########################################################################
    story.append(Paragraph("Threats Detected", styles["Heading2"]))
    
    threats_data = [
        ["Time", "Categories of Cyber Threats", "Count"],
        ["2025-03-15 10:25:00", "Malware Name", "5"],
        ["2025-03-15 10:30:00", "Malware Name2", "3"],
        ["2025-03-15 11:00:00", "Malware Name3", "4"]
    ]
    t_threats = Table(
        threats_data,
        colWidths=[doc.width*0.25, doc.width*0.5, doc.width*0.25]
    )
    t_threats.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    story.append(t_threats)
    story.append(Spacer(1, 0.3*inch))
    
    threats_history_df = pd.DataFrame({
        "Malware Name": [1, 2, 3, 4, 5],
        "Malware Name2": [2, 3, 2, 5, 3],
        "Malware Name3": [3, 2, 4, 3, 6]
    }, index=["28/2/2025 21:13", "30/2/2025 21:13:58", "X", "Y", "Z"])
    
    threats_chart = "threats_history.png"
    generate_chart(
        data=threats_history_df,
        chart_type="line",
        filename=threats_chart,
        colors_list=["#1f77b4", "#ff7f0e", "#2ca02c"],
        labels={"title": "Treats History"},
        figsize=(5, 3),
        dpi=150
    )
    chart_files.append(threats_chart)
    
    story.append(Paragraph("Treats History", styles["Heading3"]))
    story.append(Image(threats_chart, width=5*inch, height=3*inch))
    story.append(Spacer(1, 0.5*inch))
    
    ###########################################################################
    # H) Build the PDF
    ###########################################################################
    doc.build(story)

    ###########################################################################
    # I) Remove Temporary Chart Files AFTER Building the PDF
    ###########################################################################
    for chart_file in chart_files:
        if os.path.exists(chart_file):
            os.remove(chart_file)

###############################################################################
# 4) Run the Report
###############################################################################
if __name__ == "__main__":
    build_report("Centralized_Monitoring_Report_Platypus.pdf")
