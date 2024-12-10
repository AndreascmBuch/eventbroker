from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Routing-mappe til at matche event-typer med modtagende mikroservices
EVENT_ROUTES = {
    "new_car_added": "http://localhost:5002/damage_event"  # Damage Service endpoint
}

@app.route('/events', methods=['POST'])
def handle_event():
    event = request.json
    event_type = event.get("type")
    event_data = event.get("data")

    if not event_type or not event_data:
        return jsonify({"error": "Event must include type and data"}), 400

    # Find rigtige service at sende eventet til
    service_url = EVENT_ROUTES.get(event_type)
    if not service_url:
        return jsonify({"error": f"No handler for event type: {event_type}"}), 400

    # Send eventet videre
    try:
        response = requests.post(service_url, json=event_data)
        if response.status_code == 200:
            return jsonify({"message": "Event routed successfully"}), 200
        else:
            return jsonify({"error": f"Failed to send event to {service_url}"}), 500
    except Exception as e:
        return jsonify({"error": f"Error forwarding event: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)



