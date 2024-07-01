from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument,ExecuteProcess,IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
import xacro 
import os 
from ament_index_python.packages import get_package_share_path
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')    

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [PathJoinSubstitution([FindPackageShare("gazebo_ros"), "launch", "gazebo.launch.py"])]
        ),
        launch_arguments={"verbose": "false"}.items(),
    )

    # Get URDF via xacro
    stalker_desc_path = get_package_share_path('stacker_description')
    stalker_xacro_file = xacro.process_file(os.path.join(stalker_desc_path,"urdf/Stacker_simple.xacro.urdf"))
    stalker_descrption = stalker_xacro_file.toxml()
    robot_description = {'robot_description':stalker_descrption}


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

    spawn_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
        output="screen",
    )


    return LaunchDescription(
        [
            DeclareLaunchArgument(
                'use_sim_time', 
                default_value='false',
                description='use simulataion clock if true'
            ),

            # ExecuteProcess(
            #     cmd = ['gazebo','--verbose','-s','./lingbazebo_ros_factory.so'],
            #     output='screen'
            # ),
            gazebo,
            node_robot_state_publisher,
            spawn_entity,
            # spawn_controller,
        ]
    )

    