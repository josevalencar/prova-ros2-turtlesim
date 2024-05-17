import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from turtlesim.srv import Spawn, Kill, SetPen

import time

class TurtleController(Node):
    def __init__(self):
        super().__init__('turtle_controller') 
        self.publisher = self.create_publisher(
            msg_type=Twist, 
            topic='/turtle2/cmd_vel', 
            qos_profile=10)  
        self.timer_period = 1.0

        # clients and services criados no construtor da classe
        self.spawn_client = self.create_client(Spawn, '/spawn') # pra spawnar a zeturguita
        self.kill_client = self.create_client(Kill, '/kill') # pra matar a coitada
        self.set_pen_client = self.create_client(SetPen, '/turtle2/set_pen') # pra mudar a cor da caneta

    def rot(self, valor):
        msg = Twist()
        msg.angular.z = valor
        self.publisher.publish(msg)

    def linear(self, valor):
        msg = Twist()
        msg.linear.x = valor
        self.publisher.publish(msg)

    def curva(self, x, z):
        msg = Twist()
        msg.linear.x = x
        time.sleep(1.0)
        msg.angular.z = z
        self.publisher.publish(msg)
        # self.get_logger().info(f'Publicando: {msg.x}, {msg.z}')

    def movimenta_zeturguita(self):
        self.rot(valor=-1.570)
        time.sleep(2.5)

        self.linear(valor=2.0)
        time.sleep(2)

        self.curva(x=4.0, z=1.570)
        time.sleep(2)

        self.rot(valor=-1.570)
        time.sleep(2.5)

        self.linear(valor=3.0)
        time.sleep(2)

        self.rot(valor=-3.14)
        time.sleep(2.5)

        self.linear(valor=3.0)
        time.sleep(2)

        self.rot(valor=-1.570)
        time.sleep(2.5)

        self.curva(x=4.0, z=1.570)
        time.sleep(2)

        self.linear(valor=2.0)
        time.sleep(2)

    def spawn_zeturguita(self):
        node = rclpy.create_node('spawn_turtle')
        spawn_client = node.create_client(Spawn, '/spawn')

        while not spawn_client.wait_for_service(timeout_sec=1.0):
            print('Zeturguita não spawnada, esperando...')

        request = Spawn.Request()
        request.x = 2.0
        request.y = 9.0
        request.theta = 0.0
        request.name = 'turtle2'

        future = spawn_client.call_async(request)
        rclpy.spin_until_future_complete(node, future)

        future = spawn_client.call_async(request)
        rclpy.spin_until_future_complete(node, future)

        if future.result() is not None:
            print('Zeturguita foi criada')
        else:
            print('Falha ao criar zeturguita')
        
    def kill_zeturguita(self):
        node = rclpy.create_node('kill_turtle')
        kill_client = node.create_client(Kill, '/kill')

        request = Kill.Request()
        request.name = 'turtle1'
        future = kill_client.call_async(request)
        rclpy.spin_until_future_complete(node, future)

        if future.result() is not None:
            print('Zeturguita foi morta')
        else:
            print('Falha ao matar zeturguita')

    async def set_pen_color(self, r, g, b):
        node = rclpy.create_node('set_pen_color')
        set_pen_client = node.create_client(SetPen, '/turtle2/set_pen')

        while not set_pen_client.wait_for_service(timeout_sec=1.0):
            print('Client set pen esperando pelo serviço...')

        request = SetPen.Request()
        request.r = r
        request.g = g
        request.b = b
        request.width = 50
        request.off = 0 

        future = set_pen_client.call_async(request)
        rclpy.spin_until_future_complete(node, future)

    async def timer_callback(self):
        self.kill_zeturguita()
        self.spawn_zeturguita()
        
        await self.set_pen_color(0, 200, 50)

        self.movimenta_zeturguita()

        self.timer.cancel()

def main(args=None):
    rclpy.init(args=args)
    tc = TurtleController()
    tc.timer = tc.create_timer(tc.timer_period, tc.timer_callback)
    
    rclpy.spin(tc)
    tc.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
    