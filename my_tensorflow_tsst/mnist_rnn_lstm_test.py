import numpy as np
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import os

tf.set_random_seed(1)  # set random seed
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
# hyperparameters
lr = 0.001  # learning rate
training_iters = 100000  # train step 上限
batch_size = 128
n_inputs = 28  # MNIST data input (img shape: 28*28)
n_steps = 28  # time steps
n_hidden_units = 128  # neurons in hidden layer
n_classes = 10  # MNIST classes (0-9 digits)

# x y placeholder
x = tf.placeholder(tf.float32, [None, n_steps, n_inputs])
y = tf.placeholder(tf.float32, [None, n_classes])

# 对 weights biases 初始值的定义
weights = {
    # shape (28, 128)
    'in': tf.Variable(tf.random_normal([n_inputs, n_hidden_units])),
    # shape (128, 10)
    'out': tf.Variable(tf.random_normal([n_hidden_units, n_classes]))
}
biases = {
    # shape (128, )
    'in': tf.Variable(tf.constant(0.1, shape=[n_hidden_units, ])),
    # shape (10, )
    'out': tf.Variable(tf.constant(0.1, shape=[n_classes, ]))
}


def RNN(X, weights, biases):
    # 原始的 X 是 3 维数据, 我们需要把它变成 2 维数据才能使用 weights 的矩阵乘法
    # X ==> (128 batches * 28 steps, 28 inputs)
    X = tf.reshape(X, [-1, n_inputs])

    # X_in = W*X + b
    X_in = tf.matmul(X, weights['in']) + biases['in']
    # X_in ==> (128 batches, 28 steps, 128 hidden) 换回3维
    X_in = tf.reshape(X_in, [-1, n_steps, n_hidden_units])

    # 使用 basic LSTM Cell.
    lstm_cell = tf.contrib.rnn.BasicLSTMCell(n_hidden_units, forget_bias=1.0, state_is_tuple=True)
    init_state = lstm_cell.zero_state(batch_size, dtype=tf.float32)  # 初始化全零 state

    outputs, final_state = tf.nn.dynamic_rnn(lstm_cell, X_in, initial_state=init_state, time_major=False)

    # 把 outputs 变成 列表 [(batch, outputs)..] * steps
    outputs = tf.unstack(tf.transpose(outputs, [1, 0, 2]))
    results = tf.matmul(outputs[-1], weights['out']) + biases['out']  # 选取最后一个 output
    return results




x = tf.placeholder("float", [None, 784])  # 数据库输入占位符,手写数据28*28,输入为一维随意，二维为784长度的数据
y_ = tf.placeholder("float", [None, 10])  # 数据库输出占位符,结果数据0到9，输入为一维随意，二维为10长度的数据
# 处理输入的数据,[0]的意思为无视输入维度，全平展 [1][2]的意思是以28x28为一个模型,[3]的意思是通道,黑白只有一个通道
x_image = tf.reshape(x, [-1, 28, 28, 1])

# 第一层卷积加池化
W_conv1 = weight_variable([5, 5, 1, 32], "W_conv1")  # 卷积计算5x5的patch，输入通道为1，输出通道为32
b_conv1 = bias_variable([32], "b_conv1")  # 输出通道为32，当然这也要是32
# 卷积输出图片的大小没有变化依然是28x28，只是厚度变厚了，因此现在的输出大小就变成了28x28x32
h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)  # 卷积后加偏移再使用relu激励函数
h_pool1 = max_pool_2x2(h_conv1)  # 卷积后池化，经过池化的处理后，输出大小就变为了14x14x32

# 第二层卷积加池化
W_conv2 = weight_variable([5, 5, 32, 64], "W_conv2")  # 卷积计算5x5的patch，输入通道为上一层输出32，这再输出通道为64
b_conv2 = bias_variable([64], "b_conv2")  # 输出通道为64，当然这也要是64
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)  # 现在的输出大小就变成了14x14x64
h_pool2 = max_pool_2x2(h_conv2)  # 再次池化后，输出大小就变为了7x7x64

# 密集连接层
W_fc1 = weight_variable([7 * 7 * 64, 1024], "W_fc1")  # 第二层卷积输出数据为7x7x64，所以这也有此数。现将图片输出张昰导入个1024个神经元的全连接层
b_fc1 = bias_variable([1024], "b_fc1")  # 随上面参数的第二维数
h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])  # 输出值从一个三维的变为一维的数据, -1表示先不考虑输入图片例子维度, 将上一个输出结果展平.
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)  # 不使用卷积了，用的向量乘

keep_prob = tf.placeholder("float")
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)  # 过拟合处理,tf.nn.dropout操作会自动处理神经元输出值的scale

W_fc2 = weight_variable([1024, 10], "W_fc2")
b_fc2 = bias_variable([10], "b_fc2")
y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)  # softmax 回归，softmax分类器 计算

cross_entropy = -tf.reduce_sum(y_ * tf.log(y_conv))  # 预测值和真值计算交叉熵
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)  # 用ADAM 优化器（亚当优化器？）优化结果
# 正确的预测,预测结果和真值对比 tf.argmax 是行或列的最大值下标向量 第二个参数为1时是按行0是按列
correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))  # 计算正确率

save_path = "data/cnn/save_net_cnn.ckpt"
saver = tf.train.Saver()

sess = tf.InteractiveSession()
if os.path.exists('data/cnn/checkpoint'):  # 判断模型是否存在
    # load date
    print("load data")
    saver.restore(sess, save_path)  # 存在就从模型中恢复变量
else:
    print("no save")
    sess.run(tf.global_variables_initializer())

for i in range(20000):
    batch = mnist.train.next_batch(50)
    train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})
    print("test␣%d␣accuracy␣%g" % (i, accuracy.eval(
        feed_dict={x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0})))
    if i % 10 == 0:  # 每十步保存下数据
        saver.save(sess, save_path)
        print("Save to path: ", save_path)
