from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from utils import calculate_pages, calculate_price, send_order_email
from database.models import db, Order

app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize database
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pdf_files = request.files.getlist('pdf_files')
        page_details = []
        total_price = 0
        
        for pdf in pdf_files:
            filename = secure_filename(pdf.filename)
            pdf.save(os.path.join('uploads', filename))
            num_pages = calculate_pages(os.path.join('uploads', filename))
            
            size = request.form.get('page_size')
            color = request.form.get('color_type')
            price = calculate_price(num_pages, size, color)
            
            page_details.append({
                'filename': filename,
                'pages': num_pages,
                'size': size,
                'color': color,
                'price': price
            })
            
            total_price += price
        
        return render_template('index.html', page_details=page_details, total_price=total_price)
    
    return render_template('index.html')

@app.route('/order', methods=['POST'])
def order():
    customer_name = request.form.get('customer_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    order_details = request.form.get('order_details')
    
    new_order = Order(customer_name=customer_name, email=email, phone=phone, order_details=order_details)
    db.session.add(new_order)
    db.session.commit()
    
    send_order_email(customer_name, email, order_details)
    return render_template('order_success.html')

@app.route('/admin', methods=['GET'])
def admin():
    orders = Order.query.all()
    return render_template('admin.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True)
