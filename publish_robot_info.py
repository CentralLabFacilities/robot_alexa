#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import json
import requests
import time
import logging
import numpy as np
from matplotlib import path

from geometry_msgs.msg import PoseWithCovarianceStamped
from std_msgs.msg import String
from people_msgs.msg import People
import rsb


# -busy state (bool)
# -CALL (bool)

robotname = "tobi"
serverurl = "http://warp1337.com:5000/"
current_location = ""
last_people_update = time.time()

# serverurl="http://localhost:5000/"

def pointInPoly(point, polygon):
    poly = path.Path(polygon)
    ret = poly.contains_point(point)
    return ret


# maytheforcebewithyou___


p1 = (16.3588726504, 6.30925045713)
p2 = (13.3668566439, 9.40414529184)
p3 = (9.9387360579, 13.0877831966)
p4 = (20.1978948252, 9.74892582772)
p5 = (17.198790766, 12.8383869617)
p6 = (13.6412316995, 16.646593463)
p7 = (24.0390379612, 13.6097755096)
p8 = (21.1956458327, 16.5876670178)
p9 = (17.4775239932, 20.1390011251)

p10 = (21.7561656767, 11.3351165489)
p11 = (18.6364057548, 14.3130282238)

oldkitchen = [p1, p2, p5, p4, p1]
oldlivingroom = [p4, p5, p8, p7, p4]

kitchen = [p1, p2, p11, p10, p1]
livingroom = [p10, p11, p8, p7, p10]

diningroom = [p9, p8, p5, p6, p9]
bedroom = [p2, p3, p6, p5, p2]


def resetPeople():
    global last_people_update
    last_people_update = time.time()
    headers = {'Content-type': 'application/json'}
    payload = "0"
    r = requests.put(serverurl + robotname + "/numDetectedPeople", headers=headers, data=json.dumps(payload))
    print "reset people"

def updateRobotInfo():
    rospy.init_node('updateRobotInfos', anonymous=True)
    rsb_informer = rsb.createInformer("/tobi", dataType=str)
    rate = rospy.Rate(1)
    print "init updater"

    def checkForNavGoal():
        headers = {'Content-type': 'application/json'}
        r = requests.get(serverurl + robotname + "/setlocation", headers=headers)
        # pos = r.json().split(',')
        # x = pos[0]
        # y = pos[1]
        # theta = pos[2]
        if r.json() == 'called':
            headers = {'Content-type': 'application/json'}
            payload = ''
            r = requests.put(serverurl + robotname + "/setlocation", headers=headers, data=json.dumps(payload))
            # robot_call = "komm"
            # pub_called.publish(robot_call)
            # Create an informer for strings on scope "/example/informer".
            rsb_informer.publishData("komm")

    def positionCB(data):
        global current_location
        x = data.pose.pose.position.x
        y = data.pose.pose.position.y

        print "callback: " + str(x) + ", " + str(y)

        # get location from Position  (e.g "kitchen")

        if (pointInPoly((x, y), kitchen)):
            location = "er ist in der küche"
        elif (pointInPoly((x, y), livingroom)):
            location = "er ist im wohnzimmer"
        elif (pointInPoly((x, y), bedroom)):
            location = "er ist im schlafzimmer"
        elif (pointInPoly((x, y), diningroom)):
            location = "er ist im esszimmer"
        else:
            location = "outside_arena"
        if current_location != location:
            print location
            current_location = location
            # send curl -i -H 'Content-Type: application/json' -X PUT -d '"kitchen"' http://localhost:5000/pepper/location
            headers = {'Content-type': 'application/json'}
            payload = location
            r = requests.put(serverurl + robotname + "/location", headers=headers, data=json.dumps(payload))
            print r.json()

    def personsCB(data):
        global last_people_update
        last_people_update = time.time()
        numberOfPeople = str(len(data.people))
        # get number of persons from Persons (e.g. "2")
        # send curl -i -H 'Content-Type: application/json' -X PUT -d '"2"' http://localhost:5000/pepper/persons
        headers = {'Content-type': 'application/json'}
        payload = numberOfPeople
        r = requests.put(serverurl + robotname + "/numDetectedPeople", headers=headers, data=json.dumps(payload))
        print r.json()


    position_sub = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, positionCB)
    person_sub = rospy.Subscriber('/people_tracker/people', People, personsCB)

    resetPeople()

    while not rospy.is_shutdown():
        rate.sleep()
        checkForNavGoal()
        #print "check"
        if time.time()-last_people_update>5:
            resetPeople()


if __name__ == '__main__':
    try:
        updateRobotInfo()
    except rospy.ROSInterruptException:
        pass
