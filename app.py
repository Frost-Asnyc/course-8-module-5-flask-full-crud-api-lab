from flask import Flask, jsonify, request 

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop"),
    Event(3, "Data Science Conference"),
    Event(4, "AI Summit")
    
]

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Events API"})

@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events])

# TODO: Task 1 - Define the Problem
# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json(silent=True)
    title = data.get("title") if isinstance(data, dict) else None

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "A non-empty title is required"}), 400

    event_id = max((event.id for event in events), default=0) + 1
    event = Event(event_id, title.strip())
    events.append(event)

    return jsonify(event.to_dict()), 201

# TODO: Task 1 - Define the Problem
# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json(silent=True)
    title = data.get("title") if isinstance(data, dict) else None

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "A non-empty title is required"}), 400

    for event in events:
        if event.id == event_id:
            event.title = title.strip()
            return jsonify(event.to_dict()), 200

    return jsonify({"error": "Event not found"}), 404

# TODO: Task 1 - Define the Problem
# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    for event in events:
        if event.id == event_id:
            events.remove(event)
            return "", 204

    return jsonify({"error": "Event not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
    
