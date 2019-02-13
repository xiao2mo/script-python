#!/usr/bin/python 
#!Func: to get the certain span elements
import tensorflow as tf
import numpy as np
input=[[[1,1,1],[2,2,2]],
       [[3,3,3],[4,4,4]],
       [[5,5,5],[6,6,6]]]
t1=tf.slice(input,[1,0,0],[1,1,3])
t2=tf.slice(input,[1,0,0],[1,2,3])
t3=tf.slice(input,[1,0,0],[2,1,3])
t4=tf.gather(input,[0,2])
sess=tf.Session()
print(sess.run(t1))
print("--------------------------")
print(sess.run(t2))
print("--------------------------")
print(sess.run(t3))
print("--------------------------")
print(sess.run(t4))
