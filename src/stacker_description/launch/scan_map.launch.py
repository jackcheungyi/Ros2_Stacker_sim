import os 
import xacro 
from ament_index_python.packages import get_package_share_path
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),
             )
    stalker_desc_path = get_package_share_path('stacker_description')
    stalker_xacro_file = xacro.process_file(os.path.join(stalker_desc_path,"urdf/Stacker_simple.xacro.urdf"))
    stalker_descrption = stalker_xacro_file.toxml()
    params = {'robot_description':stalker_descrption}
    
    lua_configuration_directory = os.path.join(stalker_desc_path, 'config')
    lua_configuration_name = 'cart_slam_2d.lua'

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                    arguments=['-topic', 'robot_description',
                                '-entity', 'stacker','-z',"0.06"],
                    output='screen')
    
    load_joint_state_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'joint_state_broadcaster'],
        output='screen'
    )

    load_tricycle_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'tricycle_controller'],
        output='screen'
    )


    cartographer = Node(
        package='cartographer_ros',
        executable='cartographer_node',
        name='cartographer_node',
        arguments=['-configuration_directory', lua_configuration_directory,
                   '-configuration_basename', lua_configuration_name ],
        remappings = [('scan', 'scan')],
        output='screen',
    )

    cartographer_map = Node(
        package='cartographer_ros',
        executable='cartographer_occupancy_grid_node',
        name='cartographer_occupancy_grid_node',
        arguments=['-resolution', '0.05'],
        output='screen',
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        arguments=[
            "-d",
            os.path.join(stalker_desc_path, "config/config.rviz"),
        ],
        output="screen",
    )
    

  

    return LaunchDescription([
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=spawn_entity,
                on_exit=[load_joint_state_controller],
            )
        ),
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=load_joint_state_controller,
                on_exit=[load_tricycle_controller],
            )
        ),
        gazebo,
        rviz,
        node_robot_state_publisher,
        cartographer,
        cartographer_map,
        spawn_entity,
    ])