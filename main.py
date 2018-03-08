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

graph = """
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

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(2)
        count += 1
        socketio.emit('server',
                      {'data': graph},
                      namespace='/test')


@app.route('/')
def index():
    return render_template('index2.html', async_mode=socketio.async_mode)

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


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app)
