import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

# 此用法为在计算前把计算图全部写好

x = tf.placeholder("float", [None, 784])  # 数据库输入占位符,手写数据28*28,输入为一维随意，二维为784长度的数据
y_ = tf.placeholder("float", [None, 10])  # 数据库输出占位符,结果数据0到9，输入为一维随意，二维为10长度的数据

W = tf.Variable(tf.zeros([784, 10]))  # 变量参数,初始化为全零的二维矩阵，784行，10列，因为要做矩阵乘法
b = tf.Variable(tf.zeros([10]))  # 变量偏移参数,初始化为全零的一维矩阵，1行，为结果集
y = tf.nn.softmax(tf.matmul(x, W) + b)  # 计算公式
cross_entropy = -tf.reduce_sum(y_ * tf.log(y))  # 交叉熵公式

train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)  # 训练，使用梯度下降法优化交叉熵

# 正确的预测,预测结果和真值对比 tf.argmax 是行或列的最大值下标向量 第二个参数为1时是按行0是按列
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))  # 准确率的计算,tf.cast为类型转换,由boolean转成float True为1 False为0

init = tf.global_variables_initializer()  # 全局变量初始化
sess = tf.Session()
sess.run(init)  # Very important

for i in range(10000):
    batch_xs, batch_ys = mnist.train.next_batch(100)  # 随机取一百个练习值
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})  # 开始练习

    print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))  # 打印准确率
