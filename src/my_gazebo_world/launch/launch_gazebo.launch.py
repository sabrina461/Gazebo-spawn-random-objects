# ~/ros2_ws/src/my_gazebo_world/launch/launch_gazebo.launch.py
from launch import LaunchDescription
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        ExecuteProcess(
            cmd=['gazebo', '--verbose', '~/ros2_ws/src/my_gazebo_world/worlds/my_world.world', '-s', 'libgazebo_ros_factory.so'],
            output='screen'
        ),
    ])