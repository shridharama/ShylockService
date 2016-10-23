#!flask-venv/bin/python
"""Shylock Service"""

from flask import Flask, jsonify, request
import os

ROUTE_PREFIX='/api/v1.0/'

app = Flask(__name__)

port = int(str(os.getenv('PORT',8080)))

beacon_list = [
  {
    'id': 1,
    'location': u'Guitar',
    'description': u'Beacon near the Gibson guitar', 
    'done': False
  },
  {
    'id': 2,
    'location': u'Piano',
    'description': u'Beacon near the Yamaha', 
    'done': False
  }
]

tasks = [
  {
    'id': 1
  }
]


beacon_events=[]

@app.route(ROUTE_PREFIX+'tasks', methods=['GET'])
def get_tasks():
  return jsonify({'tasks': tasks})

@app.route(ROUTE_PREFIX+'getAllBeacons', methods=['GET'])
def get_all_beacons():
    return jsonify({'beacon_list': beacon_list})

@app.route(ROUTE_PREFIX+'pushBeaconEvent', methods=['POST'])
def push_beacon_event():
	#if not request.json or not 'uuid' in request.json:
	#	abort(400)
  if len(beacon_events) == 0:
    new_id = 0
  else:
    new_id = beacon_events[-1]['id'] + 1
  beacon_event = {
    'id': new_id,
    'uuid': request.json['uuid'],
    'timestamp': request.json['timestamp'],
    'beacon_id': request.json['beacon_id'],
    'distance': request.json['distance']
  }
  beacon_events.append(beacon_event)
  return jsonify({'beacon_event': beacon_event}),201

@app.route(ROUTE_PREFIX+'getBeaconEventForBeaconId/<int:beacon_id>', methods=['GET'])
def get_beacon_event_for_beacon_id(beacon_id):
  result_events = []
  for event in beacon_events:
    if event['beacon_id'] == beacon_id:
      result_events.append(event)
  return jsonify({'beacon_events': result_events})

'''@app.route(ROUTE_PREFIX+'getEventsForTimestampRangeByBeaconId', methods=['GET'])
def get_events_for_timestamp_range_by_beacon_id:
  result_events = []
'''

@app.route('/')
def hello_world():
  return 'Hello World! Welcome to ShylockService. We run on port ' + str(port)

@app.route(ROUTE_PREFIX)
def hello_world2():
  return 'Hello World! Welcome to ShylockService. We run on port ' + str(port)



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=port)
