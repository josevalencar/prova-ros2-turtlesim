import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist

import sys

from collections import deque

dq = deque()

class TurtleController(Node):
    def __init__(self):
        super().__init__('turtle_controller') 
        self.publisher = self.create_publisher(
            msg_type=Twist, 
            topic='/turtle1/cmd_vel', 
            qos_profile=10)  
        self.timer_period = int(sys.argv[4])/1000
    
    def send_cmd_vel(self, linear_x, linear_y, angular_vel):
        msg = Twist()
        msg.linear.x = linear_x
        msg.linear.y = linear_y
        msg.angular.z = angular_vel
        self.publisher.publish(msg)
        print(f"Linear X: {linear_x}, Linear Y: {linear_y}, Angular Vel: {angular_vel}")

    async def timer_callback(self):        
        self.send_cmd_vel(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])) 

        self.timer.cancel()

def main(args=None):
    rclpy.init(args=args)
    tc = TurtleController()
    dq.append(tc)
    tc.timer = tc.create_timer(tc.timer_period, tc.timer_callback)

    dq.pop()
    rclpy.spin(tc)
    tc.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
    