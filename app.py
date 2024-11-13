from flask import Flask, render_template, request, redirect, url_for
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_cost', methods=['POST'])
def get_cost():
    aws_access_key_id = request.form.get('aws_access_key_id')
    aws_secret_access_key = request.form.get('aws_secret_access_key')
    
    if not aws_access_key_id or not aws_secret_access_key:
        return "Please provide both AWS Access Key ID and Secret Access Key.", 400

    try:
        # Create a session using the provided credentials
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name='us-east-1'  # Specify the AWS region, modify as needed
        )

        # Use the session to get the Cost Explorer client
        client = session.client('ce')

        # Get the cost and usage data for the current month
        response = client.get_cost_and_usage(
            TimePeriod={
                'Start': '2024-11-01',  # Update this to the current month's start
                'End': '2024-11-30'     # Update this to the current month's end
            },
            Granularity='MONTHLY',
            Metrics=['BlendedCost']
        )

        # Extract the total cost from the response
        total_cost = float(response['ResultsByTime'][0]['Total']['BlendedCost']['Amount'])
        
        # Round the cost to 2 decimal places
        total_cost = round(total_cost, 2)
        
        return render_template('results.html', total_cost=total_cost)

    except (NoCredentialsError, PartialCredentialsError):
        return "Invalid AWS credentials. Please check your Access Key ID and Secret Access Key.", 400
    except Exception as e:
        return f"An error occurred: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
