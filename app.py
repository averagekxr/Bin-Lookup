from flask import Flask, request, jsonify
import pandas as pd
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["200 per minute", "50 per second"]
)

data = pd.read_csv('bin_data_all.csv')

data['BIN/IIN'] = data['BIN/IIN'].astype(str)

data['BIN/IIN'] = data['BIN/IIN'].str.strip()

@app.before_request
def log_request():
    print(f"İstek Geldi: {request.method} {request.url} - IP: {request.remote_addr}")

@app.route('/bin_lookup', methods=['GET'])
@limiter.limit("10 per second")
def bin_lookup():
    bin_number = request.args.get('bin')
    beautify = request.args.get('beautify', default=False, type=lambda x: (x.lower() == 'true'))
    
    if bin_number is None:
        response = {
            "status": "error",
            "code": 400,
            "message": "BIN numarası sağlanmalıdır.",
            "timestamp": pd.Timestamp.now().isoformat(),
            "request": {
                "method": request.method,
                "url": request.url
            },
            "metadata": {
                "rate_limit": {
                    "limit": "10 per second",
                    "period": "1 second"
                }
            }
        }
        print(f"İstek Sonucu: {response['status']} - {response['message']}")
        return jsonify(response), 400
    
    bin_number = bin_number.strip()
    
    result = data[data['BIN/IIN'] == bin_number]
    
    if result.empty:
        response = {
            "status": "error",
            "code": 404,
            "message": "BIN numarası bulunamadı.",
            "timestamp": pd.Timestamp.now().isoformat(),
            "request": {
                "method": request.method,
                "url": request.url
            },
            "metadata": {
                "rate_limit": {
                    "limit": "10 per second",
                    "period": "1 second"
                }
            }
        }
        print(f"İstek Sonucu: {response['status']} - {response['message']}")
        return jsonify(response), 404
    
    result_dict = result.to_dict(orient='records')[0]
    
    if beautify:
        response = {
            "status": "success",
            "code": 200,
            "message": "BIN numarası bulundu.",
            "timestamp": pd.Timestamp.now().isoformat(),
            "request": {
                "method": request.method,
                "url": request.url
            },
            "data": {
                "BIN/IIN": result_dict['BIN/IIN'],
                "Network": result_dict['Network'],
                "Card Type": result_dict['Card Type'],
                "Category": result_dict['Category'],
                "Issuer": result_dict['Issuer']
            },
            "metadata": {
                "rate_limit": {
                    "limit": "10 per second",
                    "period": "1 second"
                }
            }
        }
    else:
        response = {
            "status": "success",
            "code": 200,
            "message": "BIN numarası bulundu.",
            "timestamp": pd.Timestamp.now().isoformat(),
            "request": {
                "method": request.method,
                "url": request.url
            },
            "data": result_dict,
            "metadata": {
                "rate_limit": {
                    "limit": "10 per second",
                    "period": "1 second"
                }
            }
        }
    
    print(f"İstek Sonucu: {response['status']} - {response['message']}")
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
