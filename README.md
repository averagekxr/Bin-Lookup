# BIN Lookup API with Rate Limiting and Logging

A simple Flask API for looking up BIN (Bank Identification Number) information with rate limiting and logging features.

## Features
- **BIN Lookup**: Search for BIN numbers in a CSV database.
- **Rate Limiting**: Limit API requests to prevent abuse (10 requests per second).
- **Logging**: Log each request and response in the terminal.
- **Formatted Responses**: Responses are formatted for better readability.

## Requirements
- Python 3.x
- Flask
- pandas
- Flask-Limiter

## Usage
1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Run the API using `python app.py`.
4. Use the API by visiting `http://localhost:5000/bin_lookup?bin=YOUR_BIN_NUMBER`.

## API Endpoints
- **GET /bin_lookup**: Lookup BIN information.

## Parameters
- **bin**: The BIN number to search for.
- **beautify**: Optional parameter to format the response for better readability.

## Response Format
- **Success**: JSON response with BIN details and metadata.
- **Error**: JSON response with error message and code.

## Contributing
Contributions are welcome! Please submit a pull request with your changes.
