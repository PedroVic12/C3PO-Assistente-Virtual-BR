from flask import Flask, jsonify, send_file
from converters.factory import ConverterFactory
import os

app = Flask(__name__)
factory = ConverterFactory()

OUTPUT_DIR = os.path.join(os.getcwd(), "output")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

@app.route('/convert/<format_type>', methods=['GET'])
def convert_presentation(format_type):
    try:
        converter = factory.get_converter(format_type)
        output_filename = f"apresentacao.{format_type}"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        converter.convert(output_path)
        
        return send_file(output_path, as_attachment=True)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro interno: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
