#-*-coding:utf8-*-
__author__ = '何斌'

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

#添加神经层
def add_layer(inputs,in_size,out_size,activation_function=None):
    Weights=tf.Variable(tf.random_normal([in_size,out_size]))
    biases=tf.Variable(tf.zeros([1,out_size])+0.1)
    Wx_plus_b=tf.matmul(inputs,Weights)+biases
    if activation_function is None:
        outputs=Wx_plus_b
    else:
        outputs=activation_function(Wx_plus_b)
    return outputs

#生成训练数据
x_data=np.linspace(-1,1,300)[:,np.newaxis]
noise=np.random.normal(0,0.05,x_data.shape)
y_data=np.square(x_data)-0.5+noise

#神经层定义
xs=tf.placeholder(tf.float32,[None,1])
ys=tf.placeholder(tf.float32,[None,1])
#第一层layer1
l1=add_layer(xs,1,10,activation_function=tf.nn.relu)
prediction=add_layer(l1,10,1,activation_function=None)

#损失值（平方误差之和）
loss=tf.reduce_mean(tf.reduce_sum(tf.square(y_data-prediction),
	reduction_indices=[1]))
#梯度下降
train_step=tf.train.AdamOptimizer(0.01).minimize(loss)

init=tf.global_variables_initializer()
sess=tf.Session()
sess.run(init)

fig=plt.figure()
ax=fig.add_subplot(1,1,1)
ax.scatter(x_data,y_data)
plt.ion()
plt.show()

for i in range(1000):
	sess.run(train_step,feed_dict={xs:x_data,ys:y_data})
	if i%50==0:
		#print(sess.run(loss,feed_dict={xs:x_data,ys:y_data}))
		#先抹除再画图
		try:
			ax.lines.remove(lines[0])
		except Exception as e:
			pass
		prediction_value=sess.run(prediction,
			feed_dict={xs:x_data,ys:y_data})
		lines=ax.plot(x_data,prediction_value,"r-",lw=5)
		plt.pause(0.1)