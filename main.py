#!/usr/bin/env python
from threading import Lock
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

graph1 = """
[<abstract>BUILD-CHAIR]-> 0 [GET-SCREWDRIVER_0]
[<abstract>BUILD-CHAIR]-> 1 [BUILD-LEGS_1]
[<abstract>BUILD-CHAIR]-> 2 [BUILD-BACK_2]
[<abstract>BUILD-CHAIR]-> 3 [BUILD-SEAT_3]
[<abstract>BUILD-CHAIR]-> 4 [ATTACH-BACK-AND-SEAT_4]


[GET-SCREWDRIVER_0] --> [<abstract>GET-SCREWDRIVER|get-screwdriver]

[BUILD-LEGS_1] -> [BUILD-BACK-LEG_0]
[BUILD-LEGS_1] -> [BUILD-BACK-LEG_1]
[BUILD-LEGS_1] -> [BUILD-FRONT-LEG_0]
[BUILD-LEGS_1] -> [BUILD-FRONT-LEG_1]

[BUILD-BACK-LEG_0] --> [<abstract>BACK-LEGS|get-dowel|get-leg|get-top-bracket]
[BUILD-BACK-LEG_1] --> [<abstract>BACK-LEGS|get-dowel|get-leg|get-top-bracket]


[BUILD-FRONT-LEG_0] --> [<abstract>FRONT-LEGS|get-dowel|get-leg|tighten-screw]
[BUILD-FRONT-LEG_1] --> [<abstract>FRONT-LEGS|get-dowel|get-leg|tighten-screw]


[BUILD-BACK_2] --> [<abstract>BUILD-BACK|get-board|get-bracket|tighten-screw]

[BUILD-SEAT_3] --> [<abstract>BUILD-SEAT|get-board|get-bracket|tighten-screw]

[ATTACH-BACK-AND-SEAT_4] --> [<abstract>ATTACH-BACK-AND-SEAT|get-board|get-bracket|tighten-screw]"""

graph2 = """
[<abstract>BUILD-CHAIR]-> 0 [GET-SCREWDRIVER_0]
[<abstract>BUILD-CHAIR]-> 1 [BUILD-LEGS_1]
[<abstract>BUILD-CHAIR]-> 2 [BUILD-BACK_2]
[<abstract>BUILD-CHAIR]-> 3 [BUILD-SEAT_3]
[<abstract>BUILD-CHAIR]-> 4 [ATTACH-BACK-AND-SEAT_4]


[GET-SCREWDRIVER_0] --> [get-screwdriver]

[BUILD-LEGS_1] -> [BUILD-BACK-LEG_0]
[BUILD-LEGS_1] -> [BUILD-BACK-LEG_1]
[BUILD-LEGS_1] -> [BUILD-FRONT-LEG_0]
[BUILD-LEGS_1] -> [BUILD-FRONT-LEG_1]

[BUILD-BACK-LEG_0] --> [get-dowel]
[BUILD-BACK-LEG_0] --> [get-leg]
[BUILD-BACK-LEG_0] --> [get-top-bracket]

[BUILD-BACK-LEG_1] --> [get-dowel]
[BUILD-BACK-LEG_1] --> [get-leg]
[BUILD-BACK-LEG_1] --> [get-top-bracket]

[BUILD-FRONT-LEG_0] --> [get-dowel]
[BUILD-FRONT-LEG_0] --> [get-leg]
[BUILD-FRONT-LEG_0] --> [tighten-screw]

[BUILD-FRONT-LEG_1] --> [get-dowel]
[BUILD-FRONT-LEG_1] --> [get-leg]
[BUILD-FRONT-LEG_1] --> [tighten-screw]

[BUILD-BACK_2] --> [get-board]
[BUILD-BACK_2] --> [get-bracket]
[BUILD-BACK_2] --> [tighten-screw]

[BUILD-SEAT_3] --> [get-board]
[BUILD-SEAT_3] --> [get-bracket]
[BUILD-SEAT_3] --> [tighten-screw]

[ATTACH-BACK-AND-SEAT_4] --> [get-board]
[ATTACH-BACK-AND-SEAT_4] --> [get-bracket]
[ATTACH-BACK-AND-SEAT_4] --> [tighten-screw]"""

graph3="""
[<abstract>BUILD-CHAIR]-> 0 [GET-SCREWDRIVER_0]
[<abstract>BUILD-CHAIR]-> 1 [BUILD-LEGS_1]
[<abstract>BUILD-CHAIR]-> 2 [BUILD-BACK_2]
[<abstract>BUILD-CHAIR]-> 3 [BUILD-SEAT_3]
[<abstract>BUILD-CHAIR]-> 4 [ATTACH-BACK-AND-SEAT_4]


[GET-SCREWDRIVER_0] --> [get-screwdriver]

[BUILD-LEGS_1] -> [BUILD-BACK-LEG_0]
[BUILD-LEGS_1] -> [BUILD-BACK-LEG_1]
[BUILD-LEGS_1] -> [BUILD-FRONT-LEG_0]
[BUILD-LEGS_1] -> [BUILD-FRONT-LEG_1]

[BUILD-BACK-LEG_0] --> [get-dowel_0]
[BUILD-BACK-LEG_0] --> [get-leg_0]
[BUILD-BACK-LEG_0] --> [get-top-bracket_0]

[BUILD-BACK-LEG_1] --> [get-dowel_1]
[BUILD-BACK-LEG_1] --> [get-leg_1]
[BUILD-BACK-LEG_1] --> [get-top-bracket_1]

[BUILD-FRONT-LEG_0] --> [get-dowel_2]
[BUILD-FRONT-LEG_0] --> [get-leg_2]
[BUILD-FRONT-LEG_0] --> [tighten-screw_0]

[BUILD-FRONT-LEG_1] --> [get-dowel_3]
[BUILD-FRONT-LEG_1] --> [get-leg_3]
[BUILD-FRONT-LEG_1] --> [tighten-screw_1]

[BUILD-BACK_2] --> [get-board_0]
[BUILD-BACK_2] --> [get-bracket_0]
[BUILD-BACK_2] --> [tighten-screw_2]

[BUILD-SEAT_3] --> [get-board_1]
[BUILD-SEAT_3] --> [get-bracket_1]
[BUILD-SEAT_3] --> [tighten-screw_3]

[ATTACH-BACK-AND-SEAT_4] --> [get-board_2]
[ATTACH-BACK-AND-SEAT_4] --> [get-bracket_2]
[ATTACH-BACK-AND-SEAT_4] --> [tighten-screw_4]"""

def background_thread():
    graph = graph1
    socketio.emit('serve',
                      {'data': graph},
                      namespace='/test')


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()


@socketio.on('my_ping', namespace='/test')
def ping_pong():
    emit('my_pong')


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)
    print("connected with client\n")

@socketio.on('graph1', namespace='/test')
def render_graph1():
  graph = graph1
  socketio.emit('serve',
                      {'data': graph},
                      namespace='/test')

@socketio.on('graph2', namespace='/test')
def render_graph2():
  graph = graph2
  socketio.emit('serve',
                      {'data': graph},
                      namespace='/test')

@socketio.on('graph3', namespace='/test')
def render_graph3():
  graph = graph3
  socketio.emit('serve',
                      {'data': graph},
                      namespace='/test')

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app)
