#!/usr/bin/env python2

import rospy
from nav_msgs.msg import Path
from geometry_msgs.msg import PointStamped, PoseStamped
from visualization_msgs.msg import Marker

import sys

if __name__ != '__main__':
    sys.exit(0)

FRAME_ID = '/map'

path = Path()
path_pub = rospy.Publisher('path', Path, queue_size=100)
vis_pub = rospy.Publisher('visualization_marker', Marker, queue_size=1)

def clear_all():
    m = Marker()
    m.header.stamp = rospy.Time.now();
    m.header.frame_id = FRAME_ID
    # Delete all
    m.action = 3
    vis_pub.publish(m)

def redraw_path():
    m = Marker()
    m.header.stamp = rospy.Time.now();
    m.header.frame_id = FRAME_ID
    m.action = Marker.ADD
    m.color.r = 0
    m.color.g = 0
    m.color.b = 1
    m.color.a = 1
    # Important!
    m.scale.x = 0.1
    m.type = Marker.LINE_LIST
    prev_point = None
    for p in path.poses:
        if not prev_point:
            prev_point = p
            continue
        m.points.append(prev_point.pose.position)
        m.points.append(p.pose.position)
        prev_point = p
    vis_pub.publish(m)

# PointStamped
def point_callback(msg):
    ps = PoseStamped()
    ps.pose.position = msg.point
    ps.header = msg.header
    path.poses.append(ps)

    rospy.loginfo('Got point:')
    rospy.loginfo('  x: {0}'.format(msg.point.x))
    rospy.loginfo('  y: {0}'.format(msg.point.y))

    clear_all()
    redraw_path()

# PoseStamped
def goal_callback(msg):
    rospy.loginfo('Got goal')

    clear_all()

    path.poses.append(msg)
    path.header.stamp = rospy.Time.now()
    path.header.frame_id = FRAME_ID
    path_pub.publish(path)

rospy.init_node('path_maker')

rospy.Subscriber('clicked_point', PointStamped, point_callback)
rospy.Subscriber('move_base_simple/goal', PoseStamped, goal_callback)

rospy.loginfo('Waiting for points. Use "Publish Point" in rviz')

rospy.spin()
