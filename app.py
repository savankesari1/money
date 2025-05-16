from flask import Flask, request, render_template_string, redirect
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

EXCEL_FILE = 'data.xlsx'

# Initialize Excel file if not exists
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=['Date', 'Name', 'Amount Given', 'Amount Paid', 'Commission', 'Final Amount'])
    df.to_excel(EXCEL_FILE, index=False)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Money Collector</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100 p-4 sm:p-10">
    <div class="max-w-xl mx-auto bg-white p-4 sm:p-6 rounded-xl shadow-xl">
        <h1 class="text-xl sm:text-2xl font-bold mb-4 text-center">MAHADEVI COMPUTERS WITHDRAW DATA</h1>
        <form method="POST" action="/">
            <label class="block mb-1">Name:</label>
            <input type="text" name="name" class="w-full border p-2 mb-4 rounded" required>

            <label class="block mb-1">Amount Given:</label>
            <input type="number" name="amount" step="0.01" class="w-full border p-2 mb-4 rounded" required>

            <label class="block mb-1">Amount Paid:</label>
            <input type="number" name="paid" step="0.01" class="w-full border p-2 mb-4 rounded" required>

            <label class="block mb-1">Commission (₹):</label>
            <input type="number" name="commission" step="0.01" class="w-full border p-2 mb-4 rounded" required>

            <button type="submit" class="w-full bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">Submit</button>
        </form>
        {% if result %}
        <div class="mt-6 p-4 bg-green-100 border rounded text-center">
            <p><strong>{{ result.name }}</strong> gave ₹{{ result.amount }} and paid ₹{{ result.paid }}.<br>
               After commission of ₹{{ result.commission }}, the final amount is ₹{{ result.final_amount }}.</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        name = request.form.get('name', '')
        amount = float(request.form.get('amount', 0))
        paid = float(request.form.get('paid', 0))
        commission = float(request.form.get('commission', 0))
        final_amount = round(amount - commission, 2)

        new_entry = {
            'Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Name': name,
            'Amount Given': amount,
            'Amount Paid': paid,
            'Commission': commission,
            'Final Amount': final_amount
        }

        df = pd.read_excel(EXCEL_FILE)
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)

        result = {
            'name': name,
            'amount': amount,
            'paid': paid,
            'commission': commission,
            'final_amount': final_amount
        }

    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)  # Or use int(os.environ.get("PORT", 5000))
