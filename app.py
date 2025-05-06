from flask import Flask, request, jsonify, send_from_directory
import random
import os

app = Flask(__name__, static_folder='')

def simulate_error(data):
    data_list = list(data)
    if random.random() < 0.5:  # 50% chance of error for demo
        index = random.randint(0, len(data) - 1)
        data_list[index] = '1' if data_list[index] == '0' else '0'
    return ''.join(data_list)

def calculate(operation, operand1, operand2):
    try:
        op1, op2 = int(operand1, 2), int(operand2, 2)
    except ValueError:
        return "Error"
    if operation == '+':
        return bin(op1 + op2)[2:]
    elif operation == '-':
        return bin(op1 - op2)[2:]
    elif operation == '*':
        return bin(op1 * op2)[2:]
    elif operation == '/':
        return bin(op1 // op2)[2:] if op2 != 0 else "Error"
    return "Error"

@app.route('/')
def index():
    # Serve the index.html file from current directory
    return send_from_directory('', 'index.html')

@app.route('/calculate', methods=['POST'])
def calculate_route():
    data = request.json
    operation = data.get('operation')
    operand1 = data.get('operand1')
    operand2 = data.get('operand2')

    # Calculate parity bit
    data_string = f"{operation},{operand1},{operand2}"
    ones_count = data_string.count('1')
    parity = '0' if ones_count % 2 == 0 else '1'

    # Simulate error on operands combined
    received_data = simulate_error(operand1 + operand2)

    # Check parity
    ones_count = received_data.count('1')
    expected_parity = '0' if ones_count % 2 == 0 else '1'
    error = "1" if parity != expected_parity else "0"

    # Calculate result if no error
    result = calculate(operation, operand1, operand2) if error == "0" else "Error"

    response = {
        'operation': operation,
        'operand1': operand1,
        'operand2': operand2,
        'result': result,
        'error': error
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True,port=5500)
