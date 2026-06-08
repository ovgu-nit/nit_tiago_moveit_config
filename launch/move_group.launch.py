from launch import LaunchDescription
from launch.actions import OpaqueFunction
from launch_ros.actions import Node
from launch_pal.arg_utils import read_launch_argument
from launch_pal.robot_arguments import CommonArgs
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():

    moveit_config = (
        MoveItConfigsBuilder("tiago", package_name="tiago_moveit_config")
        .robot_description_semantic(file_path="config/tiago.srdf")
        .trajectory_execution(file_path="config/controllers/controllers_pal-gripper.yaml")
    )

    ld = LaunchDescription()

    for arg in [CommonArgs.use_sim_time, CommonArgs.use_sensor_manager]:
        ld.add_action(arg)

    ld.add_action(OpaqueFunction(function=start_move_group, args=[moveit_config]))

    return ld


def start_move_group(context, *args, **kwargs):
    moveit_config = args[0]

    use_sim_time = read_launch_argument("use_sim_time", context)
    use_sensor_manager = read_launch_argument("use_sensor_manager", context)

    if use_sensor_manager == "True":
        moveit_config.sensors_3d(file_path="config/sensors_3d.yaml")

    moveit_config = moveit_config.to_moveit_configs()

    move_group_params = [
        moveit_config.to_dict(),
        {"use_sim_time": use_sim_time.lower() == "true"},
    ]

    return [
        Node(
            package="moveit_ros_move_group",
            executable="move_group",
            output="screen",
            emulate_tty=True,
            parameters=move_group_params,
        )
    ]
