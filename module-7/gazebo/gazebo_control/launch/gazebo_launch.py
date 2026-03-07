# launch/gazebo_launch.py
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # 1. Find the official ros_gz_sim package on your computer
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    # 2. Setup the IncludeLaunchDescription to trigger Gazebo
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        # 3. Pass arguments to Gazebo: load an empty world and run immediately (-r)
        launch_arguments={'gz_args': 'empty.sdf -r'}.items(),
    )
    # 4. Return the LaunchDescription
    return LaunchDescription([
        gz_sim
    ])
