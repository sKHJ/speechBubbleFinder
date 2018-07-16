import cv2
import numpy as np
from matplotlib import pyplot as plt
import tensorflow as tf

import itertools
import csv

data=[]
f = open('../good.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
for line in rdr:
    #horizen , vertical , blob, histo
    data.append([int(line[0]),int(line[1]),int(line[2]),int(float(line[3]))])


x_data = []
y_data= []

for d in data:
    x_data.append(d)


print(x_data)
for i in range(0, len(x_data)):
    y_data.append([1])

length = len(x_data)

f.close()

data=[]
f = open('../bad.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
for line in rdr:
    #horizen , vertical , blob, histo
    data.append([int(line[0]),int(line[1]),int(line[2]),int(float(line[3]))])

for d in data:
    x_data.append(d)


for i in range(0, len(x_data) - length):
    y_data.append([0])

print(x_data)
print(y_data)
f.close()


import tensorflow as tf
tf.set_random_seed(777)  # for reproducibility
'''
x_data = [[1, 2],
          [2, 3],
          [3, 1],
          [4, 3],
          [5, 3],
          [6, 2]]
y_data = [[0],
          [0],
          [0],
          [1],
          [1],
          [1]]

'''
# placeholders for a tensor that will be always fed.
X = tf.placeholder(tf.float32, shape=[None, 4])
Y = tf.placeholder(tf.float32, shape=[None, 1])

W = tf.Variable(tf.random_normal([4, 1]), name='weight')
b = tf.Variable(tf.random_normal([1]), name='bias')

# Hypothesis using sigmoid: tf.div(1., 1. + tf.exp(tf.matmul(X, W)))
hypothesis = tf.sigmoid(tf.matmul(X, W) + b)

# cost/loss function
cost = -tf.reduce_mean(Y * tf.log(hypothesis) + (1 - Y) *
                       tf.log(1 - hypothesis))

train = tf.train.GradientDescentOptimizer(learning_rate=0.01).minimize(cost)

# Accuracy computation
# True if hypothesis>0.5 else False
predicted = tf.cast(hypothesis > 0.5, dtype=tf.float32)
accuracy = tf.reduce_mean(tf.cast(tf.equal(predicted, Y), dtype=tf.float32))

# Launch graph
with tf.Session() as sess:
    # Initialize TensorFlow variables
    sess.run(tf.global_variables_initializer())

    for step in range(10001):
        cost_val, _ = sess.run([cost, train], feed_dict={X: x_data, Y: y_data})
        if step % 200 == 0:
            print(step, cost_val)

    # Accuracy report
    h, c, a = sess.run([hypothesis, predicted, accuracy],
                       feed_dict={X: x_data, Y: y_data})
    print("\nHypothesis: ", h, "\nCorrect (Y): ", c, "\nAccuracy: ", a)
