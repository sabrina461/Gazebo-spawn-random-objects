# ~/ros2_ws/src/spawn_random_shape/spawn_random_shape/spawn_random_shape.py
import rclpy
from rclpy.node import Node
from gazebo_msgs.srv import SpawnEntity
import random

class SpawnRandomShape(Node):
    def __init__(self):
        super().__init__('spawn_random_shape')
        self.cli = self.create_client(SpawnEntity, '/spawn_entity')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = SpawnEntity.Request()

    def send_request(self):
        shapes = ['box', 'sphere', 'cylinder']
        shape = random.choice(shapes)
        self.req.name = shape
        self.req.xml = f"""
        <sdf version='1.6'>
          <model name='{shape}'>
            <pose>0 0 1 0 0 0</pose>
            <link name='link'>
              <pose>0 0 1 0 0 0</pose>
              <collision name='collision'>
                <geometry>
                  <{shape}>
                    <size>1 1 1</size>
                  </{shape}>
                </geometry>
              </collision>
              <visual name='visual'>
                <geometry>
                  <{shape}>
                    <size>1 1 1</size>
                  </{shape}>
                </geometry>
              </visual>
            </link>
          </model>
        </sdf>
        """
        self.req.robot_namespace = ''
        self.req.initial_pose.position.x = random.uniform(-4, 4)
        self.req.initial_pose.position.y = random.uniform(-4, 4)
        self.req.initial_pose.position.z = 0.5
        self.future = self.cli.call_async(self.req)

def main(args=None):
    rclpy.init(args=args)
    spawn_random_shape = SpawnRandomShape()
    spawn_random_shape.send_request()

    while rclpy.ok():
        rclpy.spin_once(spawn_random_shape)
        if spawn_random_shape.future.done():
            try:
                response = spawn_random_shape.future.result()
            except Exception as e:
                spawn_random_shape.get_logger().info(
                    'Service call failed %r' % (e,))
            else:
                spawn_random_shape.get_logger().info(
                    'Shape spawned successfully')
            break

    spawn_random_shape.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()