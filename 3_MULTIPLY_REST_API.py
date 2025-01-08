from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/multiply', methods=['POST'])
def multiply():
    try:
        # Parse JSON request data
        data = request.get_json()

        # Extract numbers from the JSON payload
        num1 = data.get('num1')
        num2 = data.get('num2')

        # Validate inputs
        if num1 is None or num2 is None:
            return jsonify({'error': 'num1 and num2 are required'}), 400
        if not isinstance(num1, (int, float)) or not isinstance(num2, (int, float)):
            return jsonify({'error': 'num1 and num2 must be numbers'}), 400

        # Perform multiplication
        result = num1 * num2

        # Return the result as JSON
        return jsonify({'num1': num1, 'num2': num2, 'result': result}), 200

    except Exception as e:
        return jsonify({'error': 'Something went wrong', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
