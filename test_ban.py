import tensorflow as tf
import numpy as np
import random

# FLAGS = tf.flags.FLAGS
# # Our data is coming in via multiple inputs, so to apply the same model to each
# # we will need to use variable sharing.
# train_data = get_training_data()
# test_data = get_test_data()
#
# # Make two linear modules, to form a Multi Layer Perceptron. Override the
# # default names (which would end up being 'linear', 'linear_1') to provide
# # interpretable variable names in TensorBoard / other tools.
# lin_to_hidden = snt.Linear(output_size=FLAGS.hidden_size, name='inp_to_hidden')
# hidden_to_out = snt.Linear(output_size=FLAGS.output_size, name='hidden_to_out')
#
# # Sequential is a module which applies a number of inner modules or ops in
# # sequence to the provided data. Note that raw TF ops such as tanh can be
# # used interchangeably with constructed modules, as they contain no variables.
# mlp = snt.Sequential([lin_to_hidden, tf.sigmoid, hidden_to_out])
#
# # Connect the sequential into the graph, any number of times.
# train_predictions = mlp(train_data)
# test_predictions = mlp(test_data)


# # 创建数据
# x_data = np.random.rand(100).astype(np.float32)  # 输入 100个随机数字
# y_data = x_data * 0.1 + 0.3  # 输出
#
# Weights = tf.Variable(tf.random_uniform([1], 0, 100.0))  # 变量,一位未知数，范围为(-2,2)
# biases = tf.Variable(tf.zeros([1]))  # 变量,一位可为零的未知数，
#
# y = Weights * x_data + biases  # 推导公式
#
# loss = tf.reduce_mean(tf.square(y - y_data))  # 误差
#
# optimizer = tf.train.GradientDescentOptimizer(0.3)  # 梯度下降优化
# train = optimizer.minimize(loss)  # 训练
#
# init = tf.global_variables_initializer()  # 替换成这样就好
#
# sess = tf.Session()
# sess.run(init)  # Very important
#
# for step in range(2001):
#     sess.run(train)
#     if step % 20 == 0:
#         print(step, sess.run(Weights), sess.run(biases))


# import pandas as pd
#
# data = pd.read_csv("C:/Users/yf29/Desktop/TEST.csv", header=0, sep=',')
# print(data[0:1])
# print(data)

ball_set = []
temp_set = np.array([])


def init_data():
    global ball_set

    total_ball_count = 1000000

    A = 1607 / 46
    B = 1022 / 46
    C = 618 / 46
    D = 65 / 46
    ball_set = [0] * int(A / 72 * total_ball_count) + [1] * int(B / 72 * total_ball_count) + [2] * int(
        C / 72 * total_ball_count) + [3] * int(D / 72 * total_ball_count)

    ball_l = len(ball_set)
    if ball_l < total_ball_count:
        for temp in range(total_ball_count - ball_l):
            ball_set.append(0)


def get_input_data():
    return temp_set


def get_result():
    global temp_set

    result = np.array(random.sample(ball_set, 1))
    temp_set = np.append(temp_set, result)
    return result


def print_round():
    print("[===, ===, ===, ===, ===, ===, ===, ===, ===, ===, ===, ===]")
    for i, val in enumerate(temp_set):
        print(int(val), end=" ")
        if i != 0 and i % 11 == 0:
            print()
    print()
    print("[===, ===, ===, ===, ===, ===, ===, ===, ===, ===, ===, ===]\n")


def do_prediction(a_count, b_count, c_count, d_count, a, b, c, d):
    pass


if __name__ == "__main__":
    x_data = np.linspace(1, 100, 100).tolist()[2-100:]
    print(x_data)

if __name__ == "__main2__":
    init_data()

    print(np.random.randint(0, 4, 10))

    a = [0, 1, 2, 3]
    x = tf.Variable(0, expected_shape=a, dtype=tf.float32)
    input_data = tf.placeholder(tf.float32)
    x_result = tf.placeholder(tf.float32)

    y = tf.reduce_sum(input_data) + x  # 推导公式
    y_data = tf.reduce_sum(input_data) + x_result  # 推导公式

    loss = y_data - y  # 误差

    optimizer = tf.train.GradientDescentOptimizer(1)  # 梯度下降优化
    train = optimizer.minimize(loss)  # 训练

    init = tf.global_variables_initializer()  # 替换成这样就好
    sess = tf.Session()
    sess.run(init)  # Very important

    for step in range(100):
        # print_round()
        input = get_input_data()
        result = get_result()
        p = sess.run(train, feed_dict={input_data: input, x_result: result})
        print(step, "bot check next:" + str(sess.run(x)))
