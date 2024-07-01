import os 
import xacro 
from ament_index_python.packages import get_package_share_path
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription, RegisterEventHandler, DeclareLaunchArgument
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

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params],
        # remappings = [('cmd_vel', 'tricycle_controller/cmd_vel')]
        
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
        # remappings = [('odom', 'tricycle_controller/odom'),('cmd_vel', 'tricycle_controller/cmd_vel')]
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        arguments=[
            "-d",
            os.path.join(stalker_desc_path, "config/config3.rviz"),
        ],
        output="screen",
    )
    
    # odom_replay = Node(
    #     package="topic_tools",
    #     executable="relay",
    #     parameters=[{'input_topic': '/tricycle_controller/odom'},{'output_topic': '/odom'}]
    # )
    
    cmdvel_replay = Node(
        package="topic_tools",
        executable="relay",
        parameters=[{'input_topic': '/cmd_vel'},{'output_topic': '/tricycle_controller/cmd_vel'}]
    )

    laser_odom =  Node(
                    package='rf2o_laser_odometry',
                    executable='rf2o_laser_odometry_node',
                    name='rf2o_laser_odometry',
                    output='screen',
                    parameters=[{
                        'laser_scan_topic' : '/scan',
                        'odom_topic' : '/odom_rf2o',
                        'publish_tf' : False,
                        'base_frame_id' : 'base_link',
                        'odom_frame_id' : 'odom',
                        'init_pose_from_topic' : '/initialpose',
                        'freq' : 10.0}],
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
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=load_tricycle_controller,
                on_exit=[rviz],
            )
        ),

        DeclareLaunchArgument(
            'world',
         default_value=[os.path.join(stalker_desc_path, 'world', 'myworld.world'), ''],
          description='SDF world file'),

        gazebo,
        # rviz,
        node_robot_state_publisher,
        laser_odom,
        spawn_entity,
        # odom_replay,
        cmdvel_replay,
    ])