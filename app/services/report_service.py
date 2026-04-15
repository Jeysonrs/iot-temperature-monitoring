import io
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def format_datetime(value):
    if value is None:
        return "N/A"
    return value.strftime("%Y-%m-%d %H:%M:%S UTC")


def calculate_average(values):
    if not values:
        return 0.0
    return round(sum(values) / len(values), 2)


def build_temperature_chart(temperatures):
    if not temperatures:
        return None

    timestamps = [t.timestamp.strftime("%H:%M:%S") for t in temperatures]
    values = [t.value for t in temperatures]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(timestamps, values, marker="o")
    ax.set_title("Temperature Trend")
    ax.set_xlabel("Time")
    ax.set_ylabel("Temperature (°C)")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight")
    plt.close(fig)
    buffer.seek(0)
    return buffer


def generate_trip_report_pdf(trip, temperatures, alerts):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
    )

    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    normal_style = styles["BodyText"]

    small_style = ParagraphStyle(
        name="Small",
        parent=normal_style,
        fontSize=9,
        leading=11,
    )

    elements = []

    elements.append(Paragraph("Cold-Chain Trip Report", title_style))
    elements.append(Spacer(1, 0.4 * cm))
    elements.append(
        Paragraph(
            f"Generated on: {format_datetime(datetime.utcnow())}",
            small_style,
        )
    )
    elements.append(Spacer(1, 0.5 * cm))

    user_name = trip.user.full_name if trip.user else "N/A"
    user_email = trip.user.email if trip.user else "N/A"
    user_role = trip.user.role if trip.user else "N/A"

    trip_info_data = [
        ["Trip ID", str(trip.id)],
        ["User", user_name],
        ["Email", user_email],
        ["Role", user_role],
        ["Product Type", trip.product_type],
        ["Allowed Range", f"{trip.min_temp} °C to {trip.max_temp} °C"],
        ["Status", "Active" if trip.active else "Finished"],
        ["Start Time", format_datetime(trip.start_time)],
        ["End Time", format_datetime(trip.end_time)],
    ]

    elements.append(Paragraph("Trip Information", heading_style))
    elements.append(Spacer(1, 0.2 * cm))

    trip_table = Table(trip_info_data, colWidths=[5 * cm, 11 * cm])
    trip_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#D9EAF7")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    elements.append(trip_table)
    elements.append(Spacer(1, 0.5 * cm))

    values = [t.value for t in temperatures]
    out_of_range_count = sum(1 for v in values if v < trip.min_temp or v > trip.max_temp)

    summary_data = [
        ["Total Readings", str(len(temperatures))],
        ["Minimum Temperature", f"{min(values):.2f} °C" if values else "N/A"],
        ["Maximum Temperature", f"{max(values):.2f} °C" if values else "N/A"],
        ["Average Temperature", f"{calculate_average(values):.2f} °C" if values else "N/A"],
        ["Total Alerts", str(len(alerts))],
        ["Out-of-Range Readings", str(out_of_range_count)],
    ]

    elements.append(Paragraph("Trip Summary", heading_style))
    elements.append(Spacer(1, 0.2 * cm))

    summary_table = Table(summary_data, colWidths=[6 * cm, 10 * cm])
    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EAF4E2")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    elements.append(summary_table)
    elements.append(Spacer(1, 0.5 * cm))

    chart_buffer = build_temperature_chart(temperatures)
    elements.append(Paragraph("Temperature Chart", heading_style))
    elements.append(Spacer(1, 0.2 * cm))

    if chart_buffer:
        chart = Image(chart_buffer, width=16 * cm, height=7 * cm)
        elements.append(chart)
    else:
        elements.append(Paragraph("No temperature records available.", normal_style))

    elements.append(Spacer(1, 0.5 * cm))

    elements.append(Paragraph("Temperature Records", heading_style))
    elements.append(Spacer(1, 0.2 * cm))

    temperature_data = [["#", "Timestamp", "Value (°C)", "Status"]]
    for idx, temp in enumerate(temperatures, start=1):
        status = "OK"
        if temp.value < trip.min_temp or temp.value > trip.max_temp:
            status = "OUT OF RANGE"

        temperature_data.append(
            [
                str(idx),
                format_datetime(temp.timestamp),
                f"{temp.value:.2f}",
                status,
            ]
        )

    temperature_table = Table(
        temperature_data,
        colWidths=[1.2 * cm, 6 * cm, 3 * cm, 5.8 * cm],
        repeatRows=1,
    )
    temperature_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#BFD7EA")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("PADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    elements.append(temperature_table)
    elements.append(Spacer(1, 0.5 * cm))

    elements.append(Paragraph("Alert Records", heading_style))
    elements.append(Spacer(1, 0.2 * cm))

    if alerts:
        alert_data = [["#", "Timestamp", "Value (°C)", "Message"]]
        for idx, alert in enumerate(alerts, start=1):
            alert_data.append(
                [
                    str(idx),
                    format_datetime(alert.created_at),
                    f"{alert.temperature_value:.2f}",
                    alert.message,
                ]
            )

        alert_table = Table(
            alert_data,
            colWidths=[1.2 * cm, 4.5 * cm, 2.3 * cm, 8 * cm],
            repeatRows=1,
        )
        alert_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F4CCCC")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                    ("PADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )
        elements.append(alert_table)
    else:
        elements.append(Paragraph("No alerts were generated for this trip.", normal_style))

    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes