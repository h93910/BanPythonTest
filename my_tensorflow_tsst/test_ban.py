import tensorflow as tf
import numpy as np
import random


class TensorflowBanCaicaile:
    def __init__(self, ):
        self.ball_set = []
        self.temp_set = np.array([])
        self.my_date_type = tf.float32

        self.__init_data()
        self.__init_tensorflow()

    def __init_data(self):
        total_ball_count = 1000000
        A = 1607 / 46
        B = 1022 / 46
        C = 618 / 46
        D = 65 / 46
        self.ball_set = [1] * int(A / 72 * total_ball_count) + [2] * int(B / 72 * total_ball_count) + [3] * int(
            C / 72 * total_ball_count) + [4] * int(D / 72 * total_ball_count)

        ball_l = len(self.ball_set)
        if ball_l < total_ball_count:
            for temp in range(total_ball_count - ball_l):
                self.ball_set.append(1)

    def __my_train_next_batch(self, group):
        train_x = []
        train_y = []
        for i in range(group):
            r = random.randint(0, 72)
            node = np.zeros(72, dtype="int").tolist()
            for j in range(r - 1):
                node[j] = random.sample(self.ball_set, 1)[0]
            train_x.append(node)

            result = np.zeros(4, dtype="int").tolist()
            result[random.sample(self.ball_set, 1)[0] - 1] = 1
            train_y.append(result)

        return np.array(train_x), np.array(train_y)

    def __init_tensorflow(self):
        print("----------init----------")
        x = tf.placeholder(self.my_date_type, [None, 72])
        y_ = tf.placeholder(self.my_date_type, [None, 4])

        W = tf.Variable(tf.zeros([72, 4]))  # 变量参数,初始化为全零的二维矩阵，784行，10列，因为要做矩阵乘法
        b = tf.Variable(tf.zeros([4]))  # 变量偏移参数,初始化为全零的一维矩阵，1行，为结果集
        y = tf.nn.softmax(tf.matmul(x, W) + b)  # 计算公式
        cross_entropy = -tf.reduce_sum(y_ * tf.log(y))  # 交叉熵公式

        train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)  # 训练，使用梯度下降法优化交叉熵

        # 正确的预测,预测结果和真值对比 tf.argmax 是行或列的最大值下标向量 第二个参数为1时是按行0是按列
        correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

        init = tf.global_variables_initializer()  # 全局变量初始化
        self.sess = tf.Session()
        self.sess.run(init)  # Very important

        for tt in range(10):
            batch_xs, batch_ys = self.__my_train_next_batch(1000)
            self.sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})  # 开始练习
            print("%d round:%g" % (tt, self.sess.run(accuracy, feed_dict={x: batch_xs, y_: batch_ys})))  # 打印准确率
        print("----------complete----------")

    def do_prediction(self, last_ico):
        pass


if __name__ == "__main__":
    print("hello")
