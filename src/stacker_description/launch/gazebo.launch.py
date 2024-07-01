import os
import xacro 
from ament_index_python.packages import get_package_share_directory,get_package_share_path
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():


     # Get URDF via xacro
    stalker_desc_path = get_package_share_path('stacker_description')
    stalker_xacro_file = xacro.process_file(os.path.join(stalker_desc_path,"urdf/Stacker_simple.xacro.urdf"))
    stalker_descrption = stalker_xacro_file.toxml()
    robot_description = {'robot_description':stalker_descrption}


    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    world = os.path.join(
        get_package_share_path('stacker_description'),'world','myworld.world'
    )


    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={'world': world}.items()
    )


    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
        )
    )

    node_robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[robot_description],
    )

    spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=["-topic", "robot_description", "-entity", "stacker"],
        output="screen",
    )

    return LaunchDescription(
        [
            

            # ExecuteProcess(
            #     cmd = ['gazebo','--verbose','-s','./lingbazebo_ros_factory.so'],
            #     output='screen'
            # ),
            gzserver_cmd,
            gzclient_cmd,
            node_robot_state_publisher,
            spawn_entity,
            # spawn_controller,
        ]
    )