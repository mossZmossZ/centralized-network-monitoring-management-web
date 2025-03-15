import pandas as pd
import matplotlib.pyplot as plt
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

def generate_chart(data, chart_type, filename, colors_list=None,
                   labels=None, ylim=None, figsize=(6,4), dpi=150):
    """
    Generates and saves a chart (bar, pie, line, etc.) as an image file.

    Parameters:
        data (pd.DataFrame or pd.Series): Data to plot.
        chart_type (str): "bar", "pie", "line".
        filename (str): Output filename (e.g., "chart.png").
        colors_list (list): List of colors for each series/category.
        labels (dict): Dict with possible keys "title", "xlabel", "ylabel".
        ylim (tuple): (ymin, ymax) if you want to fix vertical axis range.
        figsize (tuple): (width_in_inches, height_in_inches).
        dpi (int): Resolution of the figure in DPI.
    """
    plt.figure(figsize=figsize, dpi=dpi)
    
    if chart_type == "bar":
        data.plot(kind="bar", color=colors_list, edgecolor='black')
    elif chart_type == "pie":
        # Pie charts typically use a Series or a single column in a DataFrame
        data.plot(kind="pie", autopct="%1.1f%%", colors=colors_list,
                  startangle=140, wedgeprops={'edgecolor': 'black'})
        plt.ylabel("")  # Remove default y-label
    elif chart_type == "line":
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

def draw_centered_image(c, img_path, y, img_width, img_height):
    """
    Draws an image so that it is centered horizontally at a given 'y' coordinate.
    """
    page_width, _ = A4
    x = (page_width - img_width) / 2  # center horizontally
    c.drawImage(img_path, x, y, width=img_width, height=img_height, mask='auto')

def generate_pdf(filename):
    c = canvas.Canvas(filename, pagesize=A4)
    page_width, page_height = A4
    
    # ------------------------------------------------------------------------
    # TITLE PAGE
    # ------------------------------------------------------------------------
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(page_width / 2, page_height - 50, "Centralized Monitoring Daily Report")
    c.setFont("Helvetica", 14)
    c.drawCentredString(page_width / 2, page_height - 80, "Report Date: 2025-02-10")
    c.drawCentredString(page_width / 2, page_height - 100, "Data Range: 2025-02-09 13:00 -- 2025-02-10 12:59 GMT+7")
    
    # ------------------------------------------------------------------------
    # NETWORK DEVICES SECTION
    # ------------------------------------------------------------------------
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, page_height - 140, "Network Devices Section")
    
    network_data = [
        ["Time", "Host", "Problem", "Duration"],
        ["2025-03-10 12:47:49 PM", "Switch 3750 Comcenter",
         "Interface Gi1/0/40(): Link down", "2d 4h 59m"]
    ]
    table_width = page_width - 60
    network_col_widths = [table_width * 0.25, table_width * 0.25,
                          table_width * 0.35, table_width * 0.15]
    network_table = Table(network_data, colWidths=network_col_widths)
    network_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    network_table.wrapOn(c, page_width, page_height)
    network_table.drawOn(c, 30, page_height - 200)
    
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
    draw_centered_image(c, problem_chart, y=page_height - 520, img_width=500, img_height=300)
    os.remove(problem_chart)
    
    # ------------------------------------------------------------------------
    # OPERATING SYSTEMS SECTION
    # ------------------------------------------------------------------------
    c.showPage()
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, page_height - 50, "Operating Systems Section")
    
    os_data = [
        ["Time", "Host", "Problem", "Duration"],
        ["2025-02-28 09:13:58 PM", "Host1", "High CPU Load", "12h 30m"],
        ["2025-02-28 10:15:22 PM", "Host2", "Memory Usage High", "8h 20m"]
    ]
    os_table = Table(os_data, colWidths=network_col_widths)
    os_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    os_table.wrapOn(c, page_width, page_height)
    os_table.drawOn(c, 30, page_height - 120)
    
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
    draw_centered_image(c, cpu_chart, y=page_height - 420, img_width=500, img_height=300)
    os.remove(cpu_chart)
    
    # ------------------------------------------------------------------------
    # WEB APPLICATION SECTION
    # ------------------------------------------------------------------------
    c.showPage()
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, page_height - 50, "Web Application Section")
    
    # Table for Web Application
    web_data = [
        ["Time", "Host", "Status", "Massage"],
        ["2025-03-11 11:06:28", "ECE ENG", "Down", "Request failed with status code 500"]
    ]
    web_col_widths = [table_width * 0.25, table_width * 0.25,
                      table_width * 0.15, table_width * 0.35]
    web_table = Table(web_data, colWidths=web_col_widths)
    web_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    web_table.wrapOn(c, page_width, page_height)
    web_table.drawOn(c, 30, page_height - 120)
    
    # WEB DOWNTIME (VERTICAL BAR CHART)
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
    draw_centered_image(c, web_downtime_chart, y=page_height - 450, img_width=500, img_height=300)
    os.remove(web_downtime_chart)
    
    # ------------------------------------------------------------------------
    # INCIDENT SUMMARY BY CATEGORY (PIE CHART)
    # ------------------------------------------------------------------------
    c.showPage()
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, page_height - 50, "Incident Summary by Category")
    
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
    draw_centered_image(c, incident_chart, y=page_height - 400, img_width=300, img_height=300)
    os.remove(incident_chart)
    
    # ------------------------------------------------------------------------
    # THREATS DETECTED (NEW LAST PAGE)
    # ------------------------------------------------------------------------
    c.showPage()
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, page_height - 50, "Threats Detected")
    
    # Table: Time, Categories of Cyber Threats, Count
    threats_data = [
        ["Time", "Categories of Cyber Threats", "Count"],
        ["2025-03-15 10:25:00", "Malware Name", "5"],
        ["2025-03-15 10:30:00", "Malware Name2", "3"],
        ["2025-03-15 11:00:00", "Malware Name3", "4"]
    ]
    threats_table = Table(threats_data, colWidths=[table_width*0.25, table_width*0.50, table_width*0.25])
    threats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    threats_table.wrapOn(c, page_width, page_height)
    threats_table.drawOn(c, 30, page_height - 120)
    
    # Threats History (LINE CHART)
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
    draw_centered_image(c, threats_chart, y=page_height - 450, img_width=500, img_height=300)
    os.remove(threats_chart)
    
    # Finally save the PDF
    c.save()

# Generate the PDF
generate_pdf("Centralized_Monitoring_Report.pdf")
