import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

def generate_launch_description():

    package_name = 'mob_bot'

    # Include the simulation launch
    sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(package_name),'launch','launch_sim.launch.py'
        )])
    )

    # Map Server (direct startup, no lifecycle)
    map_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{
            'use_sim_time': True,
            'yaml_filename': os.path.join(get_package_share_directory(package_name), 'maps', 'my_map.yaml'),
            'topic_name': 'map',
            'frame_id': 'map'
        }],
        remappings=[('/map', '/map')]
    )

    # Nav2 Controller Server
    controller_server = Node(
        package='nav2_controller',
        executable='controller_server',
        name='controller_server',
        output='screen',
        parameters=[os.path.join(get_package_share_directory(package_name), 'config', 'nav2_params.yaml'),
                   {'use_sim_time': True}]
    )

    # Nav2 Planner Server
    planner_server = Node(
        package='nav2_planner',
        executable='planner_server',
        name='planner_server',
        output='screen',
        parameters=[os.path.join(get_package_share_directory(package_name), 'config', 'nav2_params.yaml'),
                   {'use_sim_time': True}]
    )

    # Nav2 BT Navigator
    bt_navigator = Node(
        package='nav2_bt_navigator',
        executable='bt_navigator',
        name='bt_navigator',
        output='screen',
        parameters=[os.path.join(get_package_share_directory(package_name), 'config', 'nav2_params.yaml'),
                   {'use_sim_time': True}]
    )

    # Static transform from map to odom (for navigation without localization)
    static_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_transform_publisher',
        output='screen',
        arguments=['0', '0', '0', '0', '0', '0', 'map', 'odom']
    )

    return LaunchDescription([
        sim,
        static_tf,
        map_server,
        controller_server,
        planner_server,
        bt_navigator
    ])
