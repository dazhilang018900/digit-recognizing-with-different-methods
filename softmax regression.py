# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 09:10:57 2017

@author: Miles

这是用tensorflow实现的一个最简单的MNIST数据集识别程序，
softmax回归，损失函数用的是交叉熵，优化方法是批量随机
梯度下降法，现在还是有问题。
"""

import numpy as np
import pandas as pd
import tensorflow as tf
import sklearn as sl
import matplotlib.pyplot as plt

"""
加载数据集
"""
print("loading dataset..........")
train=pd.read_csv("F:/python/digit recognize/train.csv")
train_X=(train.ix[:,1:].values).astype('float32')
train_Yv=(train.ix[:,0].values).astype('float32')
train_Y=train[['label']]
"""
test=pd.read_csv("F:/python/digit recognize/test.csv")
test_X=test.ix[:,1:].values
test_Y=test.ix[:,0].values
"""              
"""
预览数据
"""
print("visualizing dataset..........")
train_X=train_X.reshape(train_X.shape[0],28,28)
for i in range(6, 9):
    plt.subplot(330 + (i+1))
    plt.imshow(train_X[i], cmap=plt.get_cmap('gray'))
    plt.title(train_Yv[i]);
train_X=train_X.reshape(42000,28*28)

"""
one-hot-encoding
"""
enc=sl.preprocessing.OneHotEncoder(sparse=False)
train_Y=enc.fit_transform(train_Y)
"不太清楚什么原因Yd可以，Y就不行，blog.csdn.net/haramshen/article/details/53169963上面的解释和实验现象感觉对应不上"
train_Y=train_Y.astype('float32')

"""
feature standardization
"""
train_X=train_X/255
train_Y=train_Y/255

"""
designing neral network architecture
"""
print("designing architecture.........")
x=tf.placeholder(tf.float32,[None,784])
W=tf.Variable(tf.zeros([784,10]))
b=tf.Variable(tf.zeros([10]))
y=tf.nn.softmax(tf.matmul(x,W)+b)

"""
design cost function
"""
y_=tf.placeholder(tf.float32,[None,10])
cross_entropy=-tf.reduce_sum(y_*tf.log(y))

"""
train
"""
print("training...........")
train_step=tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

init=tf.global_variables_initializer()
sess=tf.Session()
sess.run(init)

import random
pin=np.linspace(0,42000-1,42000-1,dtype=int)
random.shuffle(pin)
for i in range(1000):
    batch_xs=train_X[pin[((i-1)*100):(i*100-1)],:]
    batch_ys=train_Y[pin[((i-1)*100):(i*100-1)],:]
    "batch_xs,batch_ys=mnist.train.next_batch(100)"
    sess.run(train_step,feed_dict={x:batch_xs,y_:batch_ys});
            
"""
评估模型
"""
correct_prediction=tf.equal(tf.argmax(y,1),tf.argmax(y_,1))
accuracy=tf.reduce_mean(tf.cast(correct_prediction,"float"))

print(sess.run(accuracy,feed_dict={x:train_X,y_:train_Y}))



"""
程序运行时出现过的问题及解决方案：
1.错误：92行y_写成了y，导致一直提示应该给第二个holder输入float型的数据
  分析：y_写成y，就相当于run的时候没有给第二个节点输入数据，所以运行不出结果
2.错误：56行64行定义的节点都是float32类型的，但是用ix命令从原始dataframe数
据中提取的数据都是float64型的
    解决：用对象.astype('float32')转换，之前看kaggle上的程序这样写的时候还
不明白原因，原来是这种作用
3.批量随机梯度下降法不知怎么实现，毕竟Python编程不像matlab那么方便，想怎么写
就怎么写。后来发现numpy中有linspace这个函数，和matlab中的作用是一样的，而random
库中的shuffle函数就是将数据重新排列的函数。
"""

"""
参考文献：
1.https://www.kaggle.com/poonaml/digit-recognizer/deep-neural-network-keras-way
2.http://wiki.jikexueyuan.com/project/tensorflow-zh/tutorials/mnist_beginners.html
"""

"""
准确率只有80%多，不知道怎么回事，应该在91%以上，还需要在改改
"""
