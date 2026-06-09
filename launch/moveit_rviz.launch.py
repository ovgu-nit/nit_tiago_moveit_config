from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():

    moveit_config = (
        MoveItConfigsBuilder("tiago", package_name="tiago_moveit_config")
        .robot_description_semantic(file_path="config/tiago.srdf")
        .trajectory_execution(file_path="config/controllers/controllers_pal-gripper.yaml")
        .to_moveit_configs()
    )

    rviz_config = str(
        Path(get_package_share_directory("tiago_moveit_config"))
        / "config/moveit.rviz"
    )

    rviz_parameters = [
        moveit_config.robot_description,
        moveit_config.robot_description_semantic,
    ]

    return LaunchDescription([
        DeclareLaunchArgument("debug", default_value="false"),
        Node(
            package="rviz2",
            executable="rviz2",
            output="log",
            arguments=["-d", rviz_config],
            parameters=rviz_parameters,
        ),
    ])
