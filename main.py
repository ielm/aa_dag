# import maketree
# import mergetree
# import ontosend
# import tmrutils

# from treenode import *
from flask import Flask, send_from_directory, render_template
app = Flask(__name__)

graph = """
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

@app.route('/')
def index():

  return render_template("/index.html")



if __name__ == '__main__':
  app.run(debug=True)