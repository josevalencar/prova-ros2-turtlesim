# Prova

Este repositório é responsável por estabelecar uma comunicação com ROS através publishers e filas em um tópico.

## Como executar

Após rodar o turtlesim com: 
```bash
ros2 run turtlesim turtlesim_node
```


Pode-se rodar o arquivo deste repositório com:

```bash 
python3 cli.py 0.0 1.0 0.0 1000
```

Onde os argumentos 1, 2, 3 e 4 referem-se a vx vy vtheta tempo_em_ms, respectivamente. 


## Código 
O código abaixo é responsável por criar uma classe TurtleController através de um Nó do ROS, que cria um publisher, uma função de enviar valores e um timer_callback. 

```python
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
```
ESta função main é responsável por estanciar a classe e adicionar ao deque da fila. 

```python 
def main(args=None):
    rclpy.init(args=args)
    tc = TurtleController()
    dq.append(tc)
    tc.timer = tc.create_timer(tc.timer_period, tc.timer_callback)

    dq.pop()
    rclpy.spin(tc)
    tc.destroy_node()
    rclpy.shutdown()
```

## Demonstração

![imagem](./image.png)