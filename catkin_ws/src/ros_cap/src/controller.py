#!/usr/bin/env python

import rospy #importar ros para python
from std_msgs.msg import String, Int32 # importar mensajes de ROS tipo String y tipo Int32
from geometry_msgs.msg import Twist # importar mensajes de ROS tipo geometry / Twist
from sensor_msgs.msg import Image # importar mensajes de ROS tipo Image
from geometry_msgs.msg import Point
import cv2 # importar libreria opencv
from cv_bridge import CvBridge # importar convertidor de formato de imagenes
import numpy as np # importar libreria numpy
from duckietown_msgs.msg import Twist2DStamped, BoolStamped

class Template(object):
	def __init__(self, args):
		super(Template, self).__init__()
		self.args = args
		self.subscriber1=rospy.Subscriber('/duckiebot/posicionPato/geometry_msgs/Point', Point, self.callback2)
		self.subscriber2=rospy.Subscriber('/duckiebot/possible_cmd', Twist2DStamped, self.callback1)
		self.publisher=rospy.Publisher('/duckiebot/wheels_driver_node/car_cmd',Twist2DStamped,queue_size=10)
		self.pato_detectado=False
		self.dstamped=Twist2DStamped()
	#def publicar(self):

	def callback1(self,msg):
		self.pato_detectado=True
		self.dstamped=msg
		
	def callback2(self,msg):
		twist= Twist2DStamped()
		#msg.x= coor x
		#msg.y= coor y
# casos:
# pato en el medio
#pato izq
#pato der
		if msg.z>=12.0 and msg.z<=13.0:
			twist.v=0.0
			twist.omega=0.0
			self.publisher.publish(twist)			
			#if msg.x<160.0:# pato a la izq (doblar der)
			#	while #este detectando algo:
			#		twist.omega = +1.0
			#	twist.v=10
			#		self.publisher(twist)	
		else:
			
				#while #no este detectando:
					#cmd.omega= --
 			self.publisher.publish(self.dstamped)
def main():
	rospy.init_node('test3') #creacion y registro del nodo!

	obj = Template('args') # Crea un objeto del tipo Template, cuya definicion se encuentra arriba

	#objeto.publicar() #llama al metodo publicar del objeto obj de tipo Template

	rospy.spin() #funcion de ROS que evita que el programa termine -  se debe usar en  Subscribers


if __name__ =='__main__':
	main()
