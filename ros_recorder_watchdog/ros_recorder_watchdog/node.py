import time
import lgpio

import rclpy
from rclpy.node import Node

from rosbag2_interfaces.msg import WriteSplitEvent

BUZZER_PIN = 23
CHIP = 4

class RosRecorderWatchdog(Node):

    def __init__(self):
        super().__init__('ros_recorder_watchdog')

        self.h = lgpio.gpiochip_open(CHIP)
        lgpio.gpio_claim_output(self.h, BUZZER_PIN)
        
        self.subscription = self.create_subscription(WriteSplitEvent, '/events/write_split', self.listener_callback, rclpy.qos.qos_profile_services_default)
        self.get_logger().info(f'Monitoring {self.subscription.topic_name} for new messages ...')

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.closed_file)
        self.beep_buzzer()

    def beep_buzzer(self):
        lgpio.gpio_write(self.h, BUZZER_PIN, 1)
        time.sleep(0.1)
        lgpio.gpio_write(self.h, BUZZER_PIN, 0)

    def destroy_node(self):
        lgpio.gpiochip_close(self.h)
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)

    ros_recorder_watchdog = RosRecorderWatchdog()
    rclpy.spin(ros_recorder_watchdog)

    # Destroy the node explicitly and shutdown rclpy
    ros_recorder_watchdog.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
