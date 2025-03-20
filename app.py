from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
import streamlit as st
from io import BytesIO

def generate_invoice(data, download_count):
    # Create a buffer to hold the PDF
    buffer = BytesIO()

    # Create a PDF document
    pdf = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Triplicate logic
    if download_count == 1:
        triplicate_text = ""
    elif download_count == 2:
        triplicate_text = "DUPLICATE"
    else:
        triplicate_text = "TRIPLICATE"

    # Header Section
    header_data = [
        ["TAX INVOICE", "", triplicate_text],
        ["KINGTOP", "", ""],
        ["417/1(A/P), Madras Cross Road, Pantoor G.P. Pallur Post, Gudipala Mandal, Chittoor district-517132", "", ""],
        ["GSTIN: 37AHOPD2862Q1Z0", "", ""],
        ["PAN: AHOPD2862Q", "", ""],
        ["Cell No: 9490960611", "", ""],
        ["Email: mskingtop@gmail.com", "", ""]
    ]
    header_table = Table(header_data, colWidths=[pdf.width / 3.0] * 3)
    header_table.setStyle(TableStyle([
        ('SPAN', (0, 0), (2, 0)),
        ('SPAN', (0, 1), (2, 1)),
        ('SPAN', (0, 2), (2, 2)),
        ('SPAN', (0, 3), (2, 3)),
        ('SPAN', (0, 4), (2, 4)),
        ('SPAN', (0, 5), (2, 5)),
        ('SPAN', (0, 6), (2, 6)),
        ('ALIGN', (0, 0), (2, 0), 'CENTER'),
        ('ALIGN', (0, 1), (2, 1), 'CENTER'),
        ('ALIGN', (0, 2), (2, 2), 'CENTER'),
        ('ALIGN', (0, 3), (2, 3), 'CENTER'),
        ('ALIGN', (0, 4), (2, 4), 'CENTER'),
        ('ALIGN', (0, 5), (2, 5), 'CENTER'),
        ('ALIGN', (0, 6), (2, 6), 'CENTER'),
        ('FONTSIZE', (0, 0), (2, 6), 8),
    ]))
    elements.append(header_table)

    # Consignee Section
    consignee_data = [
        ["Consignee Details"],
        [f"Name: {data['consignee_name']}"],
        [f"Address: {data['consignee_address']}"],
        [f"GSTIN: {data['consignee_gstin']}"],
        [f"PAN: {data['consignee_pan']}"]
    ]
    consignee_table = Table(consignee_data, colWidths=[pdf.width])
    consignee_table.setStyle(TableStyle([
        ('SPAN', (0, 0), (-1, 0)),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))
    elements.append(consignee_table)

    # Invoice Details Section
    invoice_details_data = [
        [f"Invoice No: {data['invoice_no']}", f"Date: {data['invoice_date']}", f"Vehicle No: {data['vehicle_number']}"]
    ]
    invoice_details_table = Table(invoice_details_data, colWidths=[pdf.width / 3.0] * 3)
    invoice_details_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))
    elements.append(invoice_details_table)

    # Item Details Section
    item_details_data = [["Sl.No", "Description", "HSN", "QTY", "UNIT", "RATE", "TOTAL"]]
    for item in data['items']:
        item_details_data.append([
            item['sl_no'], item['description'], item['hsn'], item['qty'], item['unit'], item['rate'], item['total']
        ])
    item_details_table = Table(item_details_data, colWidths=[20 * mm, 50 * mm, 20 * mm, 20 * mm, 20 * mm, 20 * mm, 30 * mm])
    item_details_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))
    elements.append(item_details_table)

    # Tax Details Section
    tax_details_data = [
        ["SGST @6%", data['sgst']],
        ["CGST @6%", data['cgst']],
        ["IGST @0%", data['igst']]
    ]
    tax_details_table = Table(tax_details_data, colWidths=[pdf.width / 2.0] * 2)
    tax_details_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))
    elements.append(tax_details_table)

    # Total Section
    total_data = [
        ["Total Quantity", data['total_quantity']],
        ["Total Amount", data['total_amount']],
        ["Total Amount in Words", data['total_amount_in_words']]
    ]
    total_table = Table(total_data, colWidths=[pdf.width / 2.0] * 2)
    total_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))
    elements.append(total_table)

    # Footer Section
    footer_data = [
        ["Bank Details"],
        [f"Account Number: {data['bank_account_number']}"],
        [f"IFS Code: {data['ifs_code']}"],
        [f"Branch: {data['branch']}"]
    ]
    footer_table = Table(footer_data, colWidths=[pdf.width])
    footer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))
    elements.append(footer_table)

    # Build the PDF
    pdf.build(elements)

    # Get the value of the BytesIO buffer and return it.
    pdf_value = buffer.getvalue()
    buffer.close()
    return pdf_value

# Streamlit App
st.title("Invoice Generator")

# Initialize download count in session state
if 'download_count' not in st.session_state:
    st.session_state['download_count'] = 0

# Input fields
with st.form(key='invoice_form'):
    # Company and Consignee Details
    company_name = st.text_input("Company Name", value="KINGTOP")
    company_address = st.text_area("Company Address", value="417/1(A/P), Madras Cross Road, Pantoor G.P. Pallur Post, Gudipala Mandal, Chittoor district-517132")
    company_gstin = st.text_input("Company GSTIN", value="37AHOPD2862Q1Z0")
    company_pan = st.text_input("Company PAN", value="AHOPD2862Q")
    company_cell_no = st.text_input("Cell No", value="9490960611")
    company_email = st.text_input("Email", value="mskingtop@gmail.com")

    consignee_name = st.text_input("Consignee Name", value="John Doe")
    consignee_address = st.text_area("Consignee Address", value="123 Main St")
    consignee_gstin = st.text_input("Consignee GSTIN", value="GSTDUMMY")
    consignee_pan = st.text_input("Consignee PAN", value="AMQPK9452J")

    # Invoice Details
    invoice_no = st.text_input("Invoice No", value="19")
    invoice_date = st.text_input("Invoice Date", value="21.03.2025")
    vehicle_number = st.text_input("Vehicle Number", value="TN38L7605")

    # Items
    items = []
    num_items = st.number_input("Number of Items", value=1, min_value=1, max_value=5)
    for i in range(num_items):
        st.subheader(f"Item {i+1}")
        sl_no = st.text_input(f"Item {i+1} Sl.No", value=str(i+1))
        description = st.text_input(f"Item {i+1} Description", value="PaperBoard")
        hsn = st.text_input(f"Item {i+1} HSN", value="4802")
        qty = st.text_input(f"Item {i+1} QTY", value="1550")
        unit = st.text_input(f"Item {i+1} UNIT", value="Kgs")
        rate = st.text_input(f"Item {i+1} RATE", value="14")
        total = st.text_input(f"Item {i+1} TOTAL", value="21700.00")
        items.append({
            "sl_no": sl_no,
            "description": description,
            "hsn": hsn,
            "qty": qty,
            "unit": unit,
            "rate": rate,
            "total": total
        })

    # Tax and Total Details
    sgst = st.text_input("SGST @6%", value="1302.00")
    cgst = st.text_input("CGST @6%", value="1302.00")
    igst = st.text_input("IGST @0%", value="0.00")
    total_quantity = st.text_input("Total Quantity", value="1550")
    total_amount = st.text_input("Total Amount", value="24304.00")
    total_amount_in_words = st.text_area("Total Invoice Amount in Words", value="Twenty Four Thousand Three hundred and Four Only")

    # Bank Details
    bank_account_number = st.text_input("Bank Account Number", value="23560200000913")
    ifs_code = st.text_input("IFS Code", value="FDRL0002356")
    branch = st.text_input("Branch", value="Darapadavedu")

    submit_button = st.form_submit_button(label='Generate Invoice')

if submit_button:
    # Prepare data for PDF generation
    data = {
        "consignee_name": consignee_name,
        "consignee_address": consignee_address,
        "consignee_gstin": consignee_gstin,
        "consignee_pan": consignee_pan,
        "invoice_no": invoice_no,
        "invoice_date": invoice_date,
        "vehicle_number": vehicle_number,
        "items": items,
        "sgst": sgst,
        "cgst": cgst,
        "igst": igst,
        "total_quantity": total_quantity,
        "total_amount": total_amount,
        "total_amount_in_words": total_amount_in_words,
        "bank_account_number": bank_account_number,
        "ifs_code": ifs_code,
        "branch": branch
    }

    # Increment download count
    st.session_state['download_count'] += 1

    # Generate PDF
    pdf_bytes = generate_invoice(data, st.session_state['download_count'])

    # Display download button
    st.download_button(
        label="Download Invoice",
        data=pdf_bytes,
        file_name="invoice.pdf",
        mime="application/pdf",
    )