#!/usr/bin/python 
#!Func: to get the certain dimension elements
import tensorflow as tf
import numpy as np
print("first test 1d tensor")
t=np.random.randint(1,10,5)
g1=tf.gather(t,[2,1,4])
sess=tf.Session()
print(t)
print(sess.run(g1))

print("now test 2d tensor")
t=np.random.randint(1,10,[4,5])
g2=tf.gather(t,[1,2,2],axis=0)
g3=tf.gather(t,[1,2,2],axis=1)
print(t)
print(sess.run(g2))
print(sess.run(g3))
