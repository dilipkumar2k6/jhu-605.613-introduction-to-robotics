# launch/spawn_robot.launch.py
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    # 1. Paths to your package and the URDF file
    pkg_gazebo_control = get_package_share_directory('gazebo_control')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    
    urdf_file = os.path.join(pkg_gazebo_control, 'urdf', 'basic_robot.urdf')
    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()
    
    # 2. Start Gazebo with our custom world
    world_file = os.path.join(pkg_gazebo_control, 'worlds', 'my_world.sdf')
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': f'-r {world_file}'}.items(),
    )
    
    # 3. Start the Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_desc,
            'use_sim_time': True  # CRITICAL: Tells ROS to use Gazebo's clock!
        }]
    )

    # 4. The Spawner Node: Bridges URDF into Gazebo
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', 'robot_description', 
            '-name', 'my_custom_diffdrive',
            '-z', '0.5'  # Drop it slightly above the ground
        ],
        output='screen'
    )
    # Find the config file path
    bridge_params = os.path.join(
        pkg_gazebo_control,
        'config',
        'bridge_config.yaml'
    )
    # 5. Bridge ROS topics and Gazebo messages for bi-directional communication
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{'config_file': bridge_params}],
        output='screen'
    )

    # 6. Static Transform Publisher for the Lidar
    # Gazebo publishes the scan with frame_id 'my_custom_diffdrive/chassis/lidar_sensor'
    # We need to tell RViz where this frame is relative to our URDF 'chassis' link
    static_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0.3', '0', '0.0375', '0', '0', '0', 'chassis', 'my_custom_diffdrive/chassis/lidar_sensor'],
        output='screen'
    )

    # 7. Start the PID Controller Node
    pid_controller = Node(
        package='gazebo_control',
        executable='diffdrive_pid',
        name='diffdrive_pid',
        output='screen'
    )

    # 8. Start RViz2 with a saved configuration file
    rviz_config_file = os.path.join(pkg_gazebo_control, 'config', 'my_robot.rviz')
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        output='screen'
    )

    return LaunchDescription([
        gz_sim,
        robot_state_publisher,
        spawn_robot,
        bridge,
        static_tf,
        pid_controller,
        rviz
    ])
