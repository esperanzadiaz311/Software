#!/usr/bin/env python

import rospy #importar ros para python
from std_msgs.msg import String, Int32 # importar mensajes de ROS tipo String y tipo Int32
from geometry_msgs.msg import Twist # importar mensajes de ROS tipo geometry / Twist
from sensor_msgs.msg import Joy
from duckietown_msgs.msg import Twist2DStamped, BoolStamped


class Control(object):
	def __init__(self, args):
		super(Control, self).__init__()
		self.args = args
		self.publisher = rospy.Publisher('/duckiebot/wheels_driver_node/car_cmd', Twist2DStamped, queue_size=10)
		self.subscriber = rospy.Subscriber('/duckiebot/joy', Joy, self.callback)

	#def publicar(self):
		
		
	def callback(self,msg):
		rospy.loginfo(msg.axes)
		rospy.loginfo(msg.buttons)
		cmd= Twist2DStamped()
		cmd.v= -msg.axes[1]
		cmd.omega= 10*msg.axes[3]
		boton= msg.buttons[5]
		if boton==1:
			cmd.v=0.0
			cmd.omega=0.0
		self.publisher.publish(cmd)

			


def main():
	rospy.init_node('test') #creacion y registro del nodo!

	obj = Control('args') # Crea un objeto del tipo Template, cuya definicion se encuentra arriba

	#objeto.publicar() #llama al metodo publicar del objeto obj de tipo Template

	rospy.spin() #funcion de ROS que evita que el programa termine -  se debe usar en  Subscribers


if __name__ =='__main__':
	main()
