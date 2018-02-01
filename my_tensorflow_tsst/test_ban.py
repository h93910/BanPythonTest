import tensorflow as tf
import numpy as np
import random
import os


class TensorflowBanCaicaile:
    def __init__(self, ):
        self.save_directory = "data/caicaile"
        self.ball_set = []
        self.temp_set = np.array([])
        self.my_date_type = tf.float32
        self.batch_count = 100

        self.__init_data()
        self.__init_tensorflow()
        # self.test()

    def __init_data(self):
        total_ball_count = 1000000
        A = 1607 / 46
        B = 1022 / 46
        C = 618 / 46
        D = 65 / 46
        self.ball_set = [0.1] * int(A / 72 * total_ball_count) + [0.2] * int(B / 72 * total_ball_count) + [0.3] * int(
            C / 72 * total_ball_count) + [0.4] * int(D / 72 * total_ball_count)

        ball_l = len(self.ball_set)
        if ball_l < total_ball_count:
            for temp in range(total_ball_count - ball_l):
                self.ball_set.append(1)

    def __my_train_next_batch(self, group):
        train_x = []
        train_y = []
        for i in range(group):
            r = random.randint(0, 72)
            # r = 72
            node = np.zeros(72, dtype="int").tolist()
            for j in range(r - 1):
                node[j] = random.sample(self.ball_set, 1)[0]
            train_x.append(node)

            result = np.zeros(4, dtype="int").tolist()
            result[int(random.sample(self.ball_set, 1)[0] * 10) - 1] = 1
            train_y.append(result)

        return np.array(train_x), np.array(train_y)

    def __my_test_next_batch(self, last_batch, group):
        train_x, train_y = last_batch
        train_x = train_x.tolist()[group - self.batch_count:]
        train_y = train_y.tolist()[group - self.batch_count:]

        for i in range(group):
            r = random.randint(0, 72)
            # r = 72
            node = np.zeros(72, dtype="int").tolist()
            for j in range(r - 1):
                node[j] = random.sample(self.ball_set, 1)[0]
            train_x.append(node)

            result = np.zeros(4, dtype="int").tolist()
            result[int(random.sample(self.ball_set, 1)[0] * 10) - 1] = 1
            train_y.append(result)

        return np.array(train_x), np.array(train_y)

    def __my_train_next_batch_order(self, group):
        train_x = []
        train_y = []

        last_list = []
        for i in range(group):
            node = random.sample(self.ball_set, 1)[0]
            last_list.append(node)

            if len(last_list) < 72:
                zero_list = np.zeros(72 - len(last_list), dtype="int")
                result_list = np.hstack((np.array(last_list), zero_list)).tolist()
            elif len(last_list) > 72:
                result_list = np.array(last_list).tolist()[-72:]
            else:
                result_list = np.array(last_list).tolist()[0:72]
            train_x.append(result_list)

            result = np.zeros(4, dtype="int").tolist()
            result[int(node * 10) - 1] = 1
            train_y.append(result)

        return np.array(train_x), np.array(train_y)

    def __my_test_next_batch_order(self, last_batch, group):
        train_x, train_y = last_batch
        train_x = train_x.tolist()[(group - 72):]
        train_y = train_y.tolist()[(group - 72):]

        last_list = train_x[-1][:]

        for i in range(group):
            node = random.sample(self.ball_set, 1)[0]
            last_list.append(node)

            if len(last_list) < 72:
                zero_list = np.zeros(72 - len(last_list), dtype="int")
                result_list = np.hstack((np.array(last_list), zero_list)).tolist()
            elif len(last_list) > 72:
                result_list = np.array(last_list).tolist()[-72:]
            else:
                result_list = np.array(last_list).tolist()[0:72]
            train_x.append(result_list)

            result = np.zeros(4, dtype="int").tolist()
            result[int(node * 10) - 1] = 1
            train_y.append(result)

        return np.array(train_x), np.array(train_y)

    def __init_tensorflow(self):
        print("----------init----------")
        x = tf.placeholder(self.my_date_type, [None, 72])
        y_ = tf.placeholder(self.my_date_type, [None, 4])

        W = tf.Variable(tf.zeros([72, 4]), name="W")  # 变量参数,初始化为全零的二维矩阵，784行，10列，因为要做矩阵乘法
        b = tf.Variable(tf.zeros([4]), name="b")  # 变量偏移参数,初始化为全零的一维矩阵，1行，为结果集

        y = tf.nn.softmax(tf.matmul(x, W) + b)  # 计算公式
        cross_entropy = -tf.reduce_sum(y_ * tf.log(y))  # 交叉熵公式

        train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)  # 训练，使用梯度下降法优化交叉熵

        # 正确的预测,预测结果和真值对比 tf.argmax 是行或列的最大值下标向量 第二个参数为1时是按行0是按列
        y_prediction = tf.argmax(y, 1)
        correct_prediction = tf.equal(y_prediction, tf.argmax(y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

        save_path = self.save_directory + "/save.ckpt"
        saver = tf.train.Saver()
        self.sess = tf.Session()
        if os.path.exists(self.save_directory + '/checkpoint'):  # 判断模型是否存在
            # load date
            print("load data")
            saver.restore(self.sess, save_path)  # 存在就从模型中恢复变量
        else:
            print("no save")
            init = tf.global_variables_initializer()  # 全局变量初始化
            self.sess.run(init)  # Very important

        test_data = self.__load_input()
        play_data = []
        if test_data is None:
            test_data = self.__my_train_next_batch_order(self.batch_count)
        batch_xs, batch_ys = test_data
        prediction = 0
        i = 0
        loss = 0

        for j in range(100):
            precise = 0
            self.__save_input(batch_xs, batch_ys)
            while prediction != 1 or precise < 500:
                # print(self.sess.run((train_step, y_prediction), feed_dict={x: batch_xs, y_: batch_ys}))  # 开始练习
                self.sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})  # 开始练习
                # prediction = self.sess.run(accuracy, feed_dict={x: batch_xs, y_: batch_ys})
                prediction = self.sess.run(accuracy, feed_dict={x: batch_xs, y_: batch_ys})
                if prediction == 1:
                    precise += 1
                # print("%d round:%g" % (i, prediction))  # 打印准确率
                i += 1
                if i % 100 == 0:  # 每十步保存下数据
                    saver.save(self.sess, save_path)

            if len(play_data) == 0:
                play_data = test_data
            play_data = self.__my_test_next_batch_order(play_data, 1)
            batch_xs, batch_ys = play_data

            prediction = self.sess.run(accuracy, feed_dict={x: batch_xs, y_: batch_ys})
            print("round:%d %s" % (j, "win!" if prediction == 1 else "lose"))
            print(self.sess.run((tf.argmax(y_, 1), y_prediction,), feed_dict={x: batch_xs, y_: batch_ys}))
            if prediction != 1:
                loss += 1
            print("=====================")

        print("----------complete----correct:%f------" % ((20 - loss) / 20))

    def __load_input(self):
        try:
            x = np.loadtxt(self.save_directory + '/input_x.out')
            y = np.loadtxt(self.save_directory + '/input_y.out')
            return x, y
        except OSError:
            return None

    def __save_input(self, x, y):
        try:
            np.savetxt(self.save_directory + '/input_x.out', x)
            np.savetxt(self.save_directory + '/input_y.out', y)
        except OSError:
            pass

    def test(self):
        t = self.__my_train_next_batch_order(100)
        print(t)
        n = self.__my_test_next_batch_order(t, 1)
        print(n)


def do_prediction(self, last_ico):
    pass


if __name__ == "__main__":
    bot = TensorflowBanCaicaile()
