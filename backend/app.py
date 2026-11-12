
from flask import Flask, jsonify, request
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "success",
        "message": "AI DevOps Assistant Backend is running!",
        "technology": "Python Flask"
    })


# Log analysis API
@app.route('/api/analyze', methods=['POST'])
def analyze_logs():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON input"}), 400

    log_type = data.get('logType', '').strip().lower()
    log_content = data.get('logContent', '').strip()

    if log_type not in ['linux', 'docker', 'jenkins']:
        return jsonify({"error": "Unsupported log type"}), 400

    if not log_content:
        return jsonify({"error": "Log content is required"}), 400


    # Rule-based error detection
    log = log_content.lower()

    if 'port is already allocated' in log or 'bind for' in log:

        port_match = re.search(r':(\d+)\s+failed', log)
        port = port_match.group(1) if port_match else None

        if port:
            recommendation = (
                f"Port {port} is already in use. "
                f"Run 'docker ps --filter publish={port}' "
                f"to identify the container using this port. "
                f"Alternatively, use a different host port."
            )
        else:
            recommendation = (
                "Run 'docker ps' to inspect running containers "
                "and 'sudo ss -ltnp' to inspect listening ports."
            )

        result = {
            "error": "Port Conflict",
            "severity": "High",
            "root_cause": (
                f"Host port {port} is already allocated."
                if port else
                "The requested port is already being used."
            ),
            "recommendation": recommendation
        }

    elif 'permission denied' in log:
        result = {
            "error": "Permission Denied",
            "severity": "Medium",
            "root_cause": "The current user does not have sufficient permissions.",
            "recommendation": "Check file permissions using ls -l and review the required user permissions."
        }
    elif 'no such file or directory' in log:
        result = {
            "error": "File or Directory Not Found",
            "severity": "Medium",
            "root_cause": "The requested file or directory does not exist at the specified path.",
            "recommendation": "Verify the file path using pwd and ls -l."
        }

    elif 'connection refused' in log:
        result = {
            "error": "Connection Refused",
            "severity": "High",
            "root_cause": "The target service may not be running or listening on the requested port.",
            "recommendation": "Check the service status and verify the configured host and port."
        }
    elif log_type == 'jenkins' and (
        'finished: failure' in log or
        'script returned exit code' in log
    ):
        result = {
            "error": "Jenkins Build Failure",
            "severity": "High",
            "root_cause": "The Jenkins pipeline or one of its execution steps failed.",
            "recommendation": "Review the Jenkins Console Output and identify the failed pipeline stage and error message."
        }    

    else:
        result = {
            "error": "Unknown or Unmatched Error",
            "severity": "Low",
            "root_cause": "No matching error pattern was found in the current rule set.",
            "recommendation": "Review the complete log and investigate the surrounding error messages."
        }

    return jsonify({
        "status": "success",
        "technology": log_type,
        "analysis": result
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
