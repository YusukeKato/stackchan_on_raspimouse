import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import Int32MultiArray
from geometry_msgs.msg import TwistStamped
import cv2
import numpy as np

class FaceTracker(Node):
    def __init__(self):
        super().__init__('face_tracker_node')
        self.sub_image = self.create_subscription(
            CompressedImage,
            '/stackchan/camera/image/compressed',
            self.image_callback,
            10)
        self.sub_joint = self.create_subscription(
            Int32MultiArray,
            '/stackchan/joint_states',
            self.joint_callback,
            10)
        self.pub_joint = self.create_publisher(
            Int32MultiArray,
            '/stackchan/joint_commands',
            10)
        self.pub_cmd_vel = self.create_publisher(
            TwistStamped,
            '/cmd_vel',
            10)
        # current stackchan motor angle
        self.current_yaw = 0
        self.current_pitch = 0
        # init OpenCV
        cascade_path = '/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        # stackchan param
        self.kp_yaw = 2.0
        self.kp_pitch = 2.0
        # raspimouse param
        self.target_face_width = 90.0
        self.kp_linear = 0.003
        self.deadband = 5.0
        self.get_logger().info('Face Tracker Node has been started.')

    def joint_callback(self, msg):
        if len(msg.data) >= 2:
            self.current_yaw = msg.data[0]
            self.current_pitch = msg.data[1]

    def image_callback(self, msg):
        np_arr = np.frombuffer(msg.data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if img is None:
            return
        # detect face
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)
        height, width = img.shape[:2]
        center_x, center_y = width // 2, height // 2
        # create cmd_vel msg
        cmd_vel_msg = TwistStamped()
        cmd_vel_msg.header.stamp = self.get_clock().now().to_msg()
        cmd_vel_msg.header.frame_id = 'base_link'
        if len(faces) > 0:
            faces = sorted(faces, key=lambda x: x[2]*x[3], reverse=True)
            (x, y, w, h) = faces[0]
            # face center
            face_cx = x + w // 2
            face_cy = y + h // 2
            # diff face center - image center
            dx = face_cx - center_x
            dy = face_cy - center_y
            # calc target angle
            target_yaw = int(self.current_yaw + (self.kp_yaw * dx))
            target_pitch = int(self.current_pitch - (self.kp_pitch * dy))
            # limit angle
            target_yaw = max(-1280, min(1280, target_yaw))
            target_pitch = max(0, min(900, target_pitch))
            # publish target angle
            cmd_msg = Int32MultiArray()
            cmd_msg.data = [target_yaw, target_pitch]
            self.pub_joint.publish(cmd_msg)
            # calc cmd_vel
            size_error = self.target_face_width - w
            if abs(size_error) > self.deadband:
                cmd_vel_msg.twist.linear.x = float(size_error * self.kp_linear)
                cmd_vel_msg.twist.linear.x = max(-0.15, min(0.15, cmd_vel_msg.twist.linear.x))
            else:
                cmd_vel_msg.twist.linear.x = 0.0
            # debug
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.circle(img, (face_cx, face_cy), 2, (0, 0, 255), -1)
        else:
            cmd_vel_msg.twist.linear.x = 0.0
        # publish cmd_vel
        self.pub_cmd_vel.publish(cmd_vel_msg)
        # debug
        cv2.imshow("StackChan Face Tracking", img)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = FaceTracker()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        cv2.destroyAllWindows()
        rclpy.shutdown()

if __name__ == '__main__':
    main()