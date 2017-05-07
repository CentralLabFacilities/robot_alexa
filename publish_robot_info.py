#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import json
import requests
import numpy as np
from matplotlib import path



from geometry_msgs.msg import PoseWithCovarianceStamped
from people_msgs.msg import People
#-busy state (bool)
#-CALL (bool)

robotname="tobi"
serverurl="http://warp1337.com:5000/"

def pointInPoly(point,polygon):

    poly = path.Path(polygon)
    ret = poly.contains_point(point)
    return ret

#maytheforcebewithyou___


p1 = (21.3727885433, 15.6410491484)
p2 = (16.2695416468, 13.1730274330)
p3 = (16.0496030221, 12.9604788694)
p4 = (16.1739002240, 13.4186044880)
p5 = (17.4055268696, 12.9224151701)
p6 = (16.2853452109, 12.2126815204)
p7 = (14.0308842158, 16.5344211887)
p8 = (18.1530704985, 12.1831861028)
p9 = (15.7761750146, 14.8226271020)

diningroom = [p9, p8, p5, p6]
livingroom = [p1, p2, p5, p4]
kitchen = [p4, p5, p8, p7]
bedroom = [p2, p3, p6, p5]

def updateRobotInfo():
    rospy.init_node('updateRobotInfos', anonymous=True)
    #pub = rospy.Publisher('/pepper_robot/pose/joint_angles', JointAnglesWithSpeed, queue_size=10)
    rate = rospy.Rate(10)
    #is_driving = time.time()

    print "init updater"


    def checkForNavGoal():
        headers = {'Content-type': 'application/json'}
        r = requests.get(serverurl + robotname + "/setlocation", headers=headers)
        print r.json()


    def positionCB(data):
        x =data.pose.pose.position.x
        y =data.pose.pose.position.y

        print "callback: "+str(x)+", "+str(y)

        # get location from Position  (e.g "kitchen")

        if(pointInPoly((x,y),kitchen)):
            location="kitchen"
        elif(pointInPoly((x,y),livingroom)):
            location="living room"
        elif(pointInPoly((x,y),bedroom)):
            location="bedroom"
        elif(pointInPoly((x,y),diningroom)):
            location="dining room"
        else:
            location="outside_arena"

            
        # send curl -i -H 'Content-Type: application/json' -X PUT -d '"kitchen"' http://localhost:5000/pepper/location
        headers = {'Content-type': 'application/json'}
        payload = location
        r = requests.put(serverurl+robotname+"/location", headers=headers, data=json.dumps(payload))
        print r.json()


    def personsCB(data):
        numberOfPeople = str(len(data.people))
        # get number of persons from Persons (e.g. "2")
        # send curl -i -H 'Content-Type: application/json' -X PUT -d '"2"' http://localhost:5000/pepper/persons
        headers = {'Content-type': 'application/json'}
        payload = numberOfPeople
        r = requests.put(serverurl + robotname + "/numDetectedPeople", headers=headers, data=json.dumps(payload))
        print r.json()

    position_sub = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, positionCB)
    person_sub = rospy.Subscriber('/people_tracker/people', People, personsCB)

    checkForNavGoal()
    while not rospy.is_shutdown():
            rate.sleep()


if __name__ == '__main__':
    try:
        updateRobotInfo()
    except rospy.ROSInterruptException:
        pass
