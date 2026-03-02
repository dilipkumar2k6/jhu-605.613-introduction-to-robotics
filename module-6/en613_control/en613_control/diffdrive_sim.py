import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TransformStamped
from sensor_msgs.msg import JointState
from example_interfaces.srv import Trigger
from tf2_ros import TransformBroadcaster
import math

class DiffDriveSim(Node):
    def __init__(self):
        super().__init__('diffdrive_sim')
        
        # Robot parameters
        self.wheel_radius = 0.4
        self.track_width = 0.875
        
        # State
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.left_wheel_angle = 0.0
        self.right_wheel_angle = 0.0
        
        # Velocities
        self.v = 0.0
        self.omega = 0.0
        
        # Time
        self.last_time = self.get_clock().now()
        
        # Subscribers
        self.cmd_vel_sub = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )
        
        # Publishers
        self.joint_state_pub = self.create_publisher(
            JointState,
            '/joint_states',
            10
        )
        
        # TF Broadcaster
        self.tf_broadcaster = TransformBroadcaster(self)
        
        # Services
        self.reset_srv = self.create_service(
            Trigger,
            '/robot_pose_reset',
            self.reset_callback
        )
        
        # Timer
        self.timer_period = 1.0 / 30.0  # 30 Hz
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
        
        self.get_logger().info('DiffDrive Simulator Node has been started.')

    def cmd_vel_callback(self, msg):
        self.v = msg.linear.x
        self.omega = msg.angular.z

    def reset_callback(self, request, response):
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.left_wheel_angle = 0.0
        self.right_wheel_angle = 0.0
        self.v = 0.0
        self.omega = 0.0
        
        response.success = True
        response.message = ""
        self.get_logger().info('Robot pose and joints reset to [0, 0, 0].')
        return response

    def timer_callback(self):
        current_time = self.get_clock().now()
        dt = (current_time - self.last_time).nanoseconds / 1e9
        self.last_time = current_time
        
        # Update pose
        self.x += self.v * math.cos(self.theta) * dt
        self.y += self.v * math.sin(self.theta) * dt
        self.theta += self.omega * dt
        
        # Update wheel angles
        v_left = self.v - self.omega * self.track_width / 2.0
        v_right = self.v + self.omega * self.track_width / 2.0
        
        self.left_wheel_angle += (v_left / self.wheel_radius) * dt
        self.right_wheel_angle += (v_right / self.wheel_radius) * dt
        
        # Publish TF
        t = TransformStamped()
        t.header.stamp = current_time.to_msg()
        t.header.frame_id = 'odom'
        t.child_frame_id = 'chassis'
        
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0
        
        # Quaternion from Euler (roll=0, pitch=0, yaw=theta)
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = math.sin(self.theta / 2.0)
        t.transform.rotation.w = math.cos(self.theta / 2.0)
        
        self.tf_broadcaster.sendTransform(t)
        
        # Publish Joint States
        js = JointState()
        js.header.stamp = current_time.to_msg()
        js.name = ['left_wheel_joint', 'right_wheel_joint']
        js.position = [self.left_wheel_angle, self.right_wheel_angle]
        
        self.joint_state_pub.publish(js)

def main(args=None):
    rclpy.init(args=args)
    node = DiffDriveSim()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
