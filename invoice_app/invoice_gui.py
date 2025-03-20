import PySimpleGUI as sg
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import os

def generate_invoice(data):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, "Invoice")
    # Add more content based on the data
    c.drawString(100, 700, f"Client: {data['client_name']}")
    c.drawString(100, 680, f"Invoice Number: {data['invoice_number']}")
    c.drawString(100, 660, f"Date: {data['date']}")
    c.drawString(100, 640, f"Client Address: {data['client_address']}")
    c.drawString(100, 620, f"Client Contact: {data['client_contact']}")
    c.drawString(400, 700, f"Shipping Name: {data['shipping_name']}")
    c.drawString(400, 680, f"Shipping Address: {data['shipping_address']}")
    c.drawString(100, 580, f"Item Description: {data['item_description']}")
    c.drawString(200, 580, f"Quantity: {data['item_quantity']}")
    c.drawString(300, 580, f"Unit Price: {data['item_unit_price']}")
    c.drawString(400, 580, f"Subtotal: {data['subtotal']}")
    c.drawString(400, 560, f"Tax: {data['tax']}")
    c.drawString(400, 540, f"Total: {data['total']}")
    c.save()
    buffer.seek(0)
    return buffer

layout = [
    [sg.Text("Invoice Generator")],
    [sg.Text("Invoice Number"), sg.InputText(key="invoice_number")],
    [sg.Text("Date"), sg.InputText(key="date")],
    [sg.Text("Client Name"), sg.InputText(key="client_name")],
    [sg.Text("Client Address"), sg.InputText(key="client_address")],
    [sg.Text("Client Contact"), sg.InputText(key="client_contact")],
    [sg.Text("Shipping Name"), sg.InputText(key="shipping_name")],
    [sg.Text("Shipping Address"), sg.InputText(key="shipping_address")],
    [sg.Text("Item Description"), sg.InputText(key="item_description")],
    [sg.Text("Item Quantity"), sg.InputText(key="item_quantity")],
    [sg.Text("Item Unit Price"), sg.InputText(key="item_unit_price")],
    [sg.Text("Subtotal"), sg.InputText(key="subtotal")],
    [sg.Text("Tax"), sg.InputText(key="tax")],
    [sg.Text("Total"), sg.InputText(key="total")],
    [sg.Button("Generate PDF"), sg.Button("Exit")],
]

window = sg.Window("Invoice Generator", layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "Generate PDF":
        data = {
            "invoice_number": values["invoice_number"],
            "date": values["date"],
            "client_name": values["client_name"],
            "client_address": values["client_address"],
            "client_contact": values["client_contact"],
            "shipping_name": values["shipping_name"],
            "shipping_address": values["shipping_address"],
            "item_description": values["item_description"],
            "item_quantity": values["item_quantity"],
            "item_unit_price": values["item_unit_price"],
            "subtotal": values["subtotal"],
            "tax": values["tax"],
            "total": values["total"],
        }
        pdf_buffer = generate_invoice(data)
        # Implement download functionality
        filename = sg.popup_get_file("Save Invoice", save_as=True, file_types=(("PDF Files", "*.pdf"),))
        if filename:
            with open(filename, "wb") as f:
                f.write(pdf_buffer.getbuffer())
            sg.popup("Invoice saved successfully!")

window.close()