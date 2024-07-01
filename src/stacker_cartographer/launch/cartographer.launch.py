import os 
import xacro 
from ament_index_python.packages import get_package_share_path
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription, RegisterEventHandler, DeclareLaunchArgument
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    stacker_carto_path = get_package_share_path('stacker_cartographer')

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    lua_configuration_directory = os.path.join(stacker_carto_path, 'config')
    lua_configuration_name = 'cart_slam_2d.lua'


    # time_arg = DeclareLaunchArgument(
    #         'use_sim_time',
    #         default_value='true',
    #         description='Use simulation (Gazebo) clock if true'),

    cartographer = Node(
        package='cartographer_ros',
        executable='cartographer_node',
        name='cartographer_node',
        parameters=[{'use_sim_time': use_sim_time}],
        arguments=['-configuration_directory', lua_configuration_directory,
                   '-configuration_basename', lua_configuration_name],
        remappings = [('odom', 'tricycle_controller/odom')],
        output='screen',
    )

    cartographer_map = Node(
        package='cartographer_ros',
        executable='cartographer_occupancy_grid_node',
        name='cartographer_occupancy_grid_node',
        parameters=[{'use_sim_time': use_sim_time}],
        arguments=['-resolution', '0.05','-publish_period_sec','1.0'],
        remappings = [('odom', 'tricycle_controller/odom')],
        output='screen',
    )

    return LaunchDescription([
        # time_arg,
        cartographer,
        cartographer_map,
    ])

