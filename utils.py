import PyPDF2
import smtplib

def calculate_pages(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        return len(reader.pages)

def calculate_price(num_pages, size, color):
    if size == 'A4':
        price_per_page = 3 if color == 'color' else 1.5
    elif size == 'A5':
        price_per_page = 1.5 if color == 'color' else 0.8
    else:
        price_per_page = 0  # Add default or error handling as needed

    return num_pages * price_per_page

def send_order_email(customer_name, email, order_details):
    # Placeholder function to simulate email sending
    print(f"Order notification sent to {email} for {customer_name}: {order_details}")
