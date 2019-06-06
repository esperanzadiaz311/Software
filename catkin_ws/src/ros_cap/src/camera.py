#!/usr/bin/env python

import rospy #importar ros para python
from std_msgs.msg import String, Int32 # importar mensajes de ROS tipo String y tipo Int32
from geometry_msgs.msg import Twist # importar mensajes de ROS tipo geometry / Twist
from sensor_msgs.msg import Image # importar mensajes de ROS tipo Image
from geometry_msgs.msg import Point
import cv2 # importar libreria opencv
from cv_bridge import CvBridge # importar convertidor de formato de imagenes
import numpy as np # importar libreria numpy


class Template(object):
	def __init__(self, args):
		super(Template, self).__init__()
		self.args = args
		self.subscriber= rospy.Subscriber('/duckiebot/camera_node/image/rect', Image, self.procesar_img)
		self.publisher= rospy.Publisher('/duckiebot/camera/detections',Image)
		self.publisherp=rospy.Publisher('/duckiebot/posicionPato/geometry_msgs/Point', Point)
		
		


	#def publicar(self):

	#def callback(self,msg):
		

	def procesar_img(self, img):
		
		bridge= CvBridge()
		image = bridge.imgmsg_to_cv2(img,'bgr8')
		
		
		# Cambiar espacio de color
		image_out= cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

		# Filtrar rango util
		cota1= np.array([10,140,140])
		cota2= np.array([100,255,255])
		
		# Aplicar mascara
		mask= cv2.inRange(image_out, cota1, cota2)
		
		# Aplicar transformaciones morfologicas
		kernel= np.ones((5,5),np.uint8)
		#image_out= cv2.erode(image,kernel,iterations=1)
		image_out= cv2.dilate(image,kernel,iterations=1)
		# Definir blobs
		_, contours, hierarchy= cv2.findContours(mask,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		# Dibujar rectangulos de cada blob

		fx=162.69421850460648
		fy=165.43607084854378
		P= Point()
		for i in contours:
			x,y,w,h= cv2.boundingRect(i)
			if w*h>1000:
				cv2.rectangle(image,(x,y),(x+w,y+h),(0,250,0),1)
				#D1=(fx*3.0)/h                        
				D2=(fy*3.0)/h
				P.z=D2
				P.x=x+(w/2.0)
				P.y=y+(h/2.0)
				self.publisherp.publish(P)
				print P                                                                                                                                                                                                                          
		# Publicar imagen final
		msg = bridge.cv2_to_imgmsg(image, 'bgr8')
		msg_image_out = bridge.cv2_to_imgmsg(image, 'bgr8')
		
		self.publisher.publish(msg_image_out)



#dp=[3,3.7,3.65]# alto,ancho,largo

		
def main():
	rospy.init_node('test') #creacion y registro del nodo!


	obj = Template('args') # Crea un objeto del tipo Template, cuya definicion se encuentra arriba

	#objeto.publicar() #llama al metodo publicar del objeto obj de tipo Template

	rospy.spin() #funcion de ROS que evita que el programa termine -  se debe usar en  Subscribers


if __name__ =='__main__':
	main()
