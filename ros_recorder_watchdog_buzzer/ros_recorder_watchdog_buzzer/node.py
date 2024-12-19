from gpiozero import Buzzer
from time import sleep

import rclpy
from rclpy.node import Node

from rosbag2_interfaces.msg import WriteSplitEvent

class RosRecorderWatchdogBuzzer(Node):

    def __init__(self):
        super().__init__('ros_recorder_watchdog_buzzer')
        self.buzzer = Buzzer(18)

        self.subscription = self.create_subscription(WriteSplitEvent,'/events/write_split',self.listener_callback,rclpy.qos.qos_profile_services_default) 
        self.get_logger().info(f'Monitoring {self.subscription.topic_name} for new messages ...')

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.closed_file)
        self.beep_buzzer()

    def beep_buzzer(self):
        self.buzzer.on()
        time.sleep(0.1)
        self.buzzer.off()

    def destroy_node(self):
        self.buzzer.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)

    ros_recorder_watchdog_buzzer = RosRecorderWatchdogBuzzer()

    rclpy.spin(ros_recorder_watchdog_buzzer)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    ros_recorder_watchdog_buzzer.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
