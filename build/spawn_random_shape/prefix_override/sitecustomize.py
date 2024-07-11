import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/romi-lab-2/ros2_ws/install/spawn_random_shape'
