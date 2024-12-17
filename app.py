from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Routing-mappe til at matche event-typer med modtagende mikroservices
EVENT_ROUTES = {
    "new_car_added": "https://skade-demo-b2awcyb4gedxdnhj.northeurope-01.azurewebsites.net/damage"  # Damage Service endpoint
}

@app.route('/events', methods=['POST'])
def handle_event():
    event = request.json
    event_type = event.get("type")
    event_data = event.get("data")

    if not event_type or not event_data:
        return jsonify({"error": "Event must include type and data"}), 400

    service_url = EVENT_ROUTES.get(event_type)
    if not service_url:
        return jsonify({"error": f"No handler for event type: {event_type}"}), 400

    try:
        response = requests.post(service_url, json=event_data)
        if response.status_code == 200:
            print(f"Event '{event_type}' routed successfully to {service_url} with data: {event_data}")
            return jsonify({"message": "Event routed successfully"}), 200
        else:
            print(f"Failed to send event to {service_url}. Status: {response.status_code}, Response: {response.text}")
            return jsonify({"error": f"Failed to send event to {service_url}"}), 500
    except Exception as e:
        print(f"Error forwarding event: {e}")
        return jsonify({"error": f"Error forwarding event: {str(e)}"}), 500
    


# test route så vi ikke får 404
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "service": "Event Service",
        "version": "1.0.0",
        "description": "A RESTful API for managing Events"
    })

if __name__ == '__main__':
    app.run()



