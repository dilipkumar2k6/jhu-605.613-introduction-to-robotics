import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, PoseStamped
from tf2_ros import Buffer, TransformListener
import math

class DiffDrivePID(Node):
    def __init__(self):
        super().__init__('diffdrive_pid')
        
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        self.goal_sub = self.create_subscription(
            PoseStamped,
            '/goal_pose',
            self.goal_callback,
            10
        )
        
        self.cmd_vel_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )
        
        self.timer = self.create_timer(1.0 / 30.0, self.timer_callback)
        
        self.goal_x = None
        self.goal_y = None
        self.goal_theta = None
        
        self.prev_x = None
        self.prev_y = None
        self.prev_theta = None
        self.prev_time = None
        
        # PD Gains
        self.kp_v = 1.0
        self.kd_v = 0.2
        self.kp_omega = 2.0
        self.kd_omega = 0.2
        
        self.get_logger().info('DiffDrive PID Controller Node started.')

    def goal_callback(self, msg):
        self.goal_x = msg.pose.position.x
        self.goal_y = msg.pose.position.y
        
        q = msg.pose.orientation
        siny_cosp = 2 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
        self.goal_theta = math.atan2(siny_cosp, cosy_cosp)
        
        self.get_logger().info(f'New goal received: x={self.goal_x:.2f}, y={self.goal_y:.2f}, theta={self.goal_theta:.2f}')

    def timer_callback(self):
        if self.goal_x is None:
            return
            
        try:
            # Look up transform from odom to chassis
            t = self.tf_buffer.lookup_transform('odom', 'chassis', rclpy.time.Time())
        except Exception as e:
            # self.get_logger().warn(f'Could not get transform: {e}')
            return
            
        current_time = self.get_clock().now()
        
        current_x = t.transform.translation.x
        current_y = t.transform.translation.y
        q = t.transform.rotation
        
        siny_cosp = 2 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
        current_theta = math.atan2(siny_cosp, cosy_cosp)
        
        if self.prev_time is None:
            self.prev_x = current_x
            self.prev_y = current_y
            self.prev_theta = current_theta
            self.prev_time = current_time
            return
            
        dt = (current_time - self.prev_time).nanoseconds / 1e9
        if dt <= 0:
            return
            
        # Update velocity by comparing against previous position
        dx_robot = current_x - self.prev_x
        dy_robot = current_y - self.prev_y
        dtheta_robot = current_theta - self.prev_theta
        dtheta_robot = math.atan2(math.sin(dtheta_robot), math.cos(dtheta_robot))
        
        # We need signed velocity. If moving backwards, it should be negative.
        # Project the displacement vector onto the robot's heading vector.
        current_v = (dx_robot * math.cos(current_theta) + dy_robot * math.sin(current_theta)) / dt
        current_omega = dtheta_robot / dt
        
        # Calculate errors
        dx_goal = self.goal_x - current_x
        dy_goal = self.goal_y - current_y
        distance_error = math.sqrt(dx_goal**2 + dy_goal**2)
        
        angle_to_goal = math.atan2(dy_goal, dx_goal)
        heading_error = angle_to_goal - current_theta
        heading_error = math.atan2(math.sin(heading_error), math.cos(heading_error))
        
        # If we are very close to the goal, just fix the final orientation
        if distance_error < 0.05:
            distance_error = 0.0
            heading_error = self.goal_theta - current_theta
            heading_error = math.atan2(math.sin(heading_error), math.cos(heading_error))
            
        # PD Control
        # u = Kp * e - Kd * current_velocity
        v_cmd = self.kp_v * distance_error - self.kd_v * current_v
        omega_cmd = self.kp_omega * heading_error - self.kd_omega * current_omega
        
        # Limit velocities
        v_cmd = max(min(v_cmd, 1.0), -1.0)
        omega_cmd = max(min(omega_cmd, 2.0), -2.0)
        
        # If distance is small and heading is small, stop
        if distance_error < 0.05 and abs(heading_error) < 0.05:
            v_cmd = 0.0
            omega_cmd = 0.0
            self.goal_x = None # Goal reached
            self.get_logger().info('Goal reached!')
            
        # Publish commands
        twist = Twist()
        twist.linear.x = float(v_cmd)
        twist.angular.z = float(omega_cmd)
        self.cmd_vel_pub.publish(twist)
        
        # Update previous values
        self.prev_x = current_x
        self.prev_y = current_y
        self.prev_theta = current_theta
        self.prev_time = current_time

def main(args=None):
    rclpy.init(args=args)
    node = DiffDrivePID()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
