#!flask-venv/bin/python
"""Shylock Service"""

from flask import Flask, jsonify, request
import os
import time
import json

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

#consists of a dict of user -> [beacon, timestamp]
latest_pos_users = {}

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
  #json.loads(request.text)
  if len(beacon_events) == 0:
    new_id = 0
  else:
    new_id = beacon_events[-1]['id'] + 1
  beacon_event = {
    'id': new_id,
    'uuid': str(request.json['uuid']).encode('latin1') ,
    'timestamp': str(request.json['timestamp']).encode('latin1'),
    'beacon_id': str(request.json['beacon_id']).encode('latin1'),
    'distance': request.json['distance']
  }
  beacon_events.append(beacon_event)
  print 'beacon event:::: ', str(beacon_event)

  #update latest_pos_users --> Extremely hacky
  latest_pos_users[beacon_event['uuid']] = [beacon_event['beacon_id'], beacon_event['timestamp']]
  print "latest_pos_users == ",  str(latest_pos_users)

  return jsonify({'beacon_event': beacon_event}),201

@app.route(ROUTE_PREFIX+'getAllBeaconEvents', methods=['GET'])
def get_all_beacon_events():
  return jsonify({'beacon_events': beacon_events})


@app.route(ROUTE_PREFIX+'getBeaconEventForBeaconId/<int:beacon_id>', methods=['GET'])
def get_beacon_event_for_beacon_id(beacon_id):
  result_events = []
  for event in beacon_events:
    print 'event going through ===', event['beacon_id']
    if event['beacon_id'] == str(beacon_id):
      result_events.append(event)
  return jsonify({'beacon_events': result_events})

'''
@app.route(ROUTE_PREFIX+'getEventsForTimestampRangeByBeaconId', methods=['GET'])
def get_events_for_timestamp_range_by_beacon_id():
  start_timestamp = request.args.get("start_timestamp")
  end_timestamp = request.args.get("end_timestamp")
  beacon_id = request.args.get("beacon_id")

  for event in beacon_events:
    if event['beacon_id'] 


  result_events = []

'''

# checks last 20 seconds
@app.route(ROUTE_PREFIX+'getLiveHeatMap', methods=['GET'])
def get_live_heat_map():
  heat_maps = []
  curr_time_ms = int(time.time())*1000
  WINDOW = 200000
  threshold_time = curr_time_ms-WINDOW
  for user,pos in latest_pos_users.iteritems():
    beacon_id = pos[0]
    timestamp = pos[1]
    heat_map = {}
    print 'user ', user, 'bid ', beacon_id, 'ts ', timestamp
    print 'thresh time ', threshold_time
    if int(timestamp) > threshold_time:
      heat_map['uuid'] = user
      heat_map['beacon_id'] = beacon_id
    heat_maps.append(heat_map)

  return jsonify({'heat_map': heat_maps})


@app.route('/')
def hello_world():
  return 'Hello World! Welcome to ShylockService. We run on port ' + str(port)

@app.route(ROUTE_PREFIX)
def hello_world2():
  return 'Hello World! Welcome to ShylockService. We run on port ' + str(port)



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=port)
