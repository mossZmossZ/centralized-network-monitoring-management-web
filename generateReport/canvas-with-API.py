import pandas as pd
import matplotlib.pyplot as plt
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import matplotlib.ticker as mticker  # Import ticker for formatting

def draw_footer(c,report_date):
    """
    Draws a footer on each page with three sections:
    - Left: "Centralized Monitoring Daily"
    - Center: "Confidential for internal use" (in red)
    - Right: "Report Date: 2025-02-10"
    """
    page_width, _ = A4
    footer_y = 30  # Footer position

    # Left-aligned text
    c.setFont("Helvetica", 10)
    c.drawString(30, footer_y, "Centralized Monitoring Daily Report")

    # Centered red text
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.red)
    c.drawCentredString(page_width / 2, footer_y, "Confidential for internal use")

    # Right-aligned text
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawRightString(page_width - 30, footer_y, report_date)

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

def generate_pdf(api_response,filename):
    c = canvas.Canvas(filename, pagesize=A4)
    c.setTitle(filename)

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
    # NETWORK DEVICES SECTION (Now Uses API Data)
    # ------------------------------------------------------------------------
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, page_height - 140, "Network Devices Section")

    # Fetch network issues data from API response
    network_data = [["Time", "Host", "Problem", "Duration"]] + api_response.get("network_issues", [])

    # Define table properties
    table_width = page_width - 60
    network_col_widths = [table_width * 0.25, table_width * 0.25, table_width * 0.35, table_width * 0.15]

    # Create and style table
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

    # Draw the table on the PDF
    network_table.wrapOn(c, page_width, page_height)
    network_table.drawOn(c, 30, page_height - 200)

    # ------------------------------------------------------------------------
    # PROBLEM HISTORY (Dynamically Uses API Data)
    # ------------------------------------------------------------------------

    # Fetch problem history data from API response
    api_problem_history = api_response.get("problem_history", {})

    # Define expected time slots for a 24-hour period (every 4 hours)
    time_slots = ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"]

    # Ensure all problem types have complete time slots (fill missing slots with 0s)
    formatted_problem_history = {}
    for problem, values in api_problem_history.items():
        while len(values) < len(time_slots):  # Ensure each problem type has 6 values
            values.append(0)
        formatted_problem_history[problem] = values[:len(time_slots)]  # Keep only 6 values

    # Create DataFrame with correct structure
    problem_data_df = pd.DataFrame(formatted_problem_history, index=time_slots)

    # Define chart filename
    problem_chart = "problem_history.png"

    # Generate Problem History line chart dynamically
    plt.figure(figsize=(7, 4), dpi=150)
    for col, color in zip(problem_data_df.columns, ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]):
        plt.plot(problem_data_df.index, problem_data_df[col], marker="o", label=col, color=color, linewidth=2)

    # Format Y-axis as integers
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(integer=True))  # Ensure whole numbers only

    # Set labels and title
    plt.title("Problem History", fontsize=14, fontweight='bold')
    plt.xlabel("Time")
    plt.ylabel("Count")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)

    # Save the chart
    plt.tight_layout()
    plt.savefig(problem_chart, bbox_inches='tight', transparent=True, dpi=150)
    plt.close()

    # Insert the chart into PDF
    draw_centered_image(c, problem_chart, y=page_height - 520, img_width=500, img_height=300)

    # Remove chart image file after inserting into PDF
    os.remove(problem_chart)


    
    # ------------------------------------------------------------------------
    # OPERATING SYSTEMS SECTION (Now Uses API Data)
    # ------------------------------------------------------------------------
    draw_footer(c, api_response["report_date"])  # Add footer
    c.showPage()

    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, page_height - 50, "Operating Systems Section")

    # Fetch operating system issues from API response
    os_data = [["Time", "Host", "Problem", "Duration"]] + api_response.get("os_issues", [])

    # Define table properties
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

    # Draw the table on the PDF
    os_table.wrapOn(c, page_width, page_height)
    os_table.drawOn(c, 30, page_height - 120)

    # ------------------------------------------------------------------------
    # CPU LOAD CHART (Dynamically Uses API Data)
    # ------------------------------------------------------------------------

    # Fetch CPU usage data from API response
    api_cpu_usage = api_response.get("cpu_usage", {})

    # Define expected time slots for a 24-hour period (every 6 hours)
    time_slots = ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"]

    # Ensure all hosts have complete time slots (fill missing slots with 0s)
    formatted_cpu_usage = {}
    for host, values in api_cpu_usage.items():
        while len(values) < len(time_slots):  # Ensure each host has 4 values
            values.append(0)
        formatted_cpu_usage[host] = values[:len(time_slots)]  # Keep only 4 values

    # Create DataFrame with correct structure
    cpu_data_df = pd.DataFrame(formatted_cpu_usage, index=time_slots)

    # Define chart filename
    cpu_chart = "cpu_load.png"

    # Generate CPU Load chart dynamically
    plt.figure(figsize=(7, 4), dpi=150)
    for col, color in zip(cpu_data_df.columns, ["#1f77b4", "#ff7f0e", "#2ca02c"]):
        plt.plot(cpu_data_df.index, cpu_data_df[col], marker="o", label=col, color=color, linewidth=2)

    # Format Y-axis as percentage (0% - 100%)
    plt.gca().yaxis.set_major_locator(mticker.MultipleLocator(10))  # Steps of 10%
    plt.gca().yaxis.set_major_formatter(mticker.PercentFormatter(xmax=100))  # Format as %

    # Set labels and title
    plt.title("CPU Load Over Time", fontsize=14, fontweight='bold')
    plt.xlabel("Time")
    plt.ylabel("CPU Usage (%)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)

    # Save the chart
    plt.tight_layout()
    plt.savefig(cpu_chart, bbox_inches='tight', transparent=True, dpi=150)
    plt.close()

    # Insert the chart into PDF
    draw_centered_image(c, cpu_chart, y=page_height - 420, img_width=500, img_height=300)

    # Remove chart image file after inserting into PDF
    os.remove(cpu_chart)

    
    # ------------------------------------------------------------------------
    # WEB APPLICATION SECTION (Now Uses API Data)
    # ------------------------------------------------------------------------
    draw_footer(c, api_response["report_date"])  # Add footer
    c.showPage()

    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, page_height - 50, "Web Application Section")

    # Fetch web issues data from API response
    web_data = [["Time", "Host", "Status", "Message"]] + api_response.get("web_issues", [])

    # Define table properties
    web_col_widths = [table_width * 0.25, table_width * 0.25, table_width * 0.15, table_width * 0.35]

    # Create and style table
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

    # Draw the table on the PDF
    web_table.wrapOn(c, page_width, page_height)
    web_table.drawOn(c, 30, page_height - 120)

    # ------------------------------------------------------------------------
    # WEB DOWNTIME CHART (Dynamically Uses API Data)
    # ------------------------------------------------------------------------

    # Fetch web downtime data from API response
    api_web_downtime = api_response.get("web_downtime", {})

    # Define expected time slots for a 24-hour report (6-hour intervals)
    time_slots = ["00:00 - 06:00", "06:00 - 12:00", "12:00 - 18:00", "18:00 - 00:00"]

    # Collect all unique web applications from API data
    all_apps = set(api_web_downtime.keys())

    # Ensure all expected apps are included (fill missing apps with zeros)
    formatted_web_downtime = {app: api_web_downtime.get(app, [0] * len(time_slots)) for app in all_apps}

    # Create DataFrame with correct structure
    web_downtime_data = pd.DataFrame(formatted_web_downtime, index=time_slots)

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

    # Insert the chart into PDF
    draw_centered_image(c, web_downtime_chart, y=page_height - 450, img_width=500, img_height=300)

    # Remove chart image file after inserting into PDF
    os.remove(web_downtime_chart)
    
    # ------------------------------------------------------------------------
    # INCIDENT SUMMARY SECTION (Proper Layout with Spacing Fix)
    # ------------------------------------------------------------------------
    draw_footer(c, api_response["report_date"])  # Add footer
    c.showPage()  # Ensure a new page for correct positioning

    # Title (Ensures it stays visible and well-spaced)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, page_height - 50, "Incident Summary by Category")

    # Fetch incident summary data from API response
    incident_summary_data = api_response.get("incident_summary", {})

    # Prepare table data (add headers)
    incident_summary_table_data = [["Category", "Incident Count"]] + [[key, value] for key, value in incident_summary_data.items()]

    # Define table width proportions
    incident_summary_col_widths = [table_width * 0.6, table_width * 0.4]

    # Create and style the table
    incident_summary_table = Table(incident_summary_table_data, colWidths=incident_summary_col_widths)
    incident_summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all text
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold header text
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Add padding to header
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Light background for rows
        ('GRID', (0, 0), (-1, -1), 1, colors.black)  # Add grid lines
    ]))

    # Set fixed space between table and chart
    table_start_y = page_height - 90  # Ensure title does NOT get pushed up
    table_height = 100 + (len(incident_summary_table_data) * 20)  # Adjust dynamically based on row count
    incident_summary_table.wrapOn(c, page_width, page_height)
    incident_summary_table.drawOn(c, 30, table_start_y - table_height)  # Table remains below title

    # ------------------------------------------------------------------------
    # INCIDENT SUMMARY PIE CHART (Correctly Positioned Below Table)
    # ------------------------------------------------------------------------

    # Define chart filename
    incident_summary_chart = "incident_summary_pie.png"

    # Convert data into a Pandas Series for Pie Chart
    incident_summary_series = pd.Series(incident_summary_data)

    # Generate Pie Chart Dynamically
    plt.figure(figsize=(4, 4), dpi=150)
    plt.pie(incident_summary_series, labels=incident_summary_series.index, autopct="%1.1f%%",
            colors=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"], startangle=140, wedgeprops={'edgecolor': 'black'})

    # Set Title
    plt.title("Issue Count by Section", fontsize=14, fontweight='bold')

    # Save the chart
    plt.tight_layout()
    plt.savefig(incident_summary_chart, bbox_inches='tight', transparent=True, dpi=150)
    plt.close()

    # Insert the chart into PDF **below the table** with increased spacing
    chart_y_position = table_start_y - table_height - 250  # Dynamic spacing between table and chart
    draw_centered_image(c, incident_summary_chart, y=chart_y_position, img_width=300, img_height=300)

    # Remove chart image file after inserting into PDF
    os.remove(incident_summary_chart)



    # ------------------------------------------------------------------------
    # THREATS DETECTED (Uses API Data)
    # ------------------------------------------------------------------------
    draw_footer(c, api_response["report_date"])  # Add footer
    c.showPage()
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, page_height - 50, "Threats Detected")

    # Fetch threats data from API response
    api_threats_data = api_response.get("threats_detected", [])

    # Prepare table data (add headers)
    threats_data = [["Time", "Categories of Cyber Threats", "Count"]] + api_threats_data

    # Create table with correct column widths
    threats_table = Table(threats_data, colWidths=[table_width * 0.25, table_width * 0.50, table_width * 0.25])
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

   # Fetch threats history data from API response
    api_threats_history = api_response.get("threats_history", {})

    # Define expected time slots for a 24-hour period (every 4 hours)
    time_slots = ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"]

    # Ensure all threats have complete time slots (fill missing time slots with 0s)
    formatted_threats_history = {}
    for threat, values in api_threats_history.items():
        while len(values) < len(time_slots):  # Ensure each threat has 6 values
            values.append(0)
        formatted_threats_history[threat] = values[:len(time_slots)]  # Keep only 6 values

    # Create DataFrame with correct structure
    threats_history_df = pd.DataFrame(formatted_threats_history, index=time_slots)

    # Define chart filename
    threats_chart = "threats_history.png"

    # Generate Threats History line chart dynamically
    plt.figure(figsize=(7, 4), dpi=150)
    for col, color in zip(threats_history_df.columns, ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]):
        plt.plot(threats_history_df.index, threats_history_df[col], marker="o", label=col, color=color, linewidth=2)

    # Format Y-axis as integers
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(integer=True))  # Ensure whole numbers only

    # Set labels and title
    plt.title("Threats History", fontsize=14, fontweight='bold')
    plt.xlabel("Time")
    plt.ylabel("Count")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)

    # Save the chart
    plt.tight_layout()
    plt.savefig(threats_chart, bbox_inches='tight', transparent=True, dpi=150)
    plt.close()

    # Insert the chart into PDF
    draw_centered_image(c, threats_chart, y=page_height - 450, img_width=500, img_height=300)

    # Remove chart image file after inserting into PDF
    os.remove(threats_chart)

    
    # Finally save the PDF
    c.save()

# Example API Data
api_response = {
    "report_date": "2025-03-16",
    "data_range": "2025-03-15 13:00 -- 2025-03-16 12:59 GMT+7",

    "network_issues": [
        ["2025-03-15 12:47:49 PM", "Switch 3750 Comcenter", "Interface Gi1/0/40(): Link down", "2d 4h 59m"]
    ],

    "problem_history": {
        "Link Down": [4, 3, 5, 6],
        "Speed Change": [2, 5, 2, 3],
        "Port Failure": [3, 4, 5, 7]
    },

    "os_issues": [
        ["2025-02-28 09:13:58 PM", "Host1", "High CPU Load", "12h 30m"]
    ],

    "cpu_usage": {
        "Host1": [30, 50, 75, 85],
        "Host2": [25, 60, 48, 78]
    },

    "web_issues": [
        ["2025-03-11 11:06:28", "ECE ENG", "Down", "Request failed with status code 500"],
        ["2025-03-11 11:06:28", "ECE ENG", "Down", "Request failed with status code 500"]
    ],

    "web_downtime": {
        "ECE ENG": [3, 4, 5, 7],
        "ECC ENG": [2,4,5,6],
        "KMUTNB" :[1,2,4,5]
    },
 
    "incident_summary": {
        "Network Devices": 15,
        "Operating Systems": 9,
        "Web Application": 6
    },

    "threats_detected": [
        ["2025-03-15 10:25:00", "Malware XYZ", "7"],
        ["2025-03-15 10:25:00", "Malware XYZ", "7"],
        ["2025-03-15 10:25:00", "Malware XYZ", "7"],
        ["2025-03-15 10:25:00", "Malware XYZ", "7"],
        ["2025-03-15 10:25:00", "Malware XYZ", "7"],
    ],

    "threats_history": {
        "Malware XYZ": [3, 5, 4, 7]
    }
}

# Generate report with API data
generate_pdf(api_response,"Centralized_Monitoring_Report.pdf")

