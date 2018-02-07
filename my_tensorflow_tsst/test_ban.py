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
        self.batch_count = 300

        self.__init_data()
        self.__init_tensorflow_test()
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
            # r = random.randint(0, self.batch_count)
            r = self.batch_count
            node = np.zeros(self.batch_count, dtype="int").tolist()
            for j in range(r):
                node[j] = random.sample(self.ball_set, 1)[0]
            train_x.append(node)

            result = np.zeros(4, dtype="int").tolist()
            result[int(random.sample(self.ball_set, 1)[0] * 10) - 1] = 1
            train_y.append(result)

        last_one = random.sample(self.ball_set, 1)[0]
        result = np.zeros(4, dtype="int").tolist()
        result[int(last_one * 10) - 1] = 1
        train_y.append(result)

        return np.array(train_x), np.array(train_y[-group:])

    def __my_test_next_batch(self, last_batch, group):
        train_x, train_y = last_batch
        train_x = train_x.tolist()[group - self.batch_count:]
        train_y = train_y.tolist()[group - self.batch_count:]

        for i in range(group):
            r = random.randint(0, self.batch_count)
            # r = self.batch_count
            node = np.zeros(self.batch_count, dtype="int").tolist()
            for j in range(r - 1):
                node[j] = random.sample(self.ball_set, 1)[0]
            train_x.append(node)

            result = np.zeros(4, dtype="int").tolist()
            result[int(random.sample(self.ball_set, 1)[0] * 10) - 1] = 1
            train_y.append(result)

        return np.array(train_x), np.array(train_y)

    def __my_train_next_batch_order(self, group):
        train_x, train_y = self.__my_train_next_batch(1)
        train_x = train_x.tolist()
        train_y = train_y.tolist()

        last_list = train_x[-1][:]

        for i in range(group):
            node = random.sample(self.ball_set, 1)[0]
            last_list.append(node)

            if len(last_list) < self.batch_count:
                zero_list = np.zeros(self.batch_count - len(last_list), dtype="int")
                result_list = np.hstack((np.array(last_list), zero_list)).tolist()
            elif len(last_list) > self.batch_count:
                result_list = np.array(last_list).tolist()[-self.batch_count:]
            else:
                result_list = np.array(last_list).tolist()[0:self.batch_count]
            train_x.append(result_list)

            result = np.zeros(4, dtype="int").tolist()
            result[int(node * 10) - 1] = 1
            train_y.append(result)

        last_one = random.sample(self.ball_set, 1)[0]
        result = np.zeros(4, dtype="int").tolist()
        result[int(last_one * 10) - 1] = 1
        train_y.append(result)

        return np.array(train_x[-group:]), np.array(train_y[-group:])

    def __my_test_next_batch_order(self, last_batch, group):
        train_x, train_y = last_batch
        train_x = train_x.tolist()[(group - self.batch_count):]
        train_y = train_y.tolist()[(group - self.batch_count):]

        last_list = train_x[-1][:]

        for i in range(group):
            node = random.sample(self.ball_set, 1)[0]
            last_list.append(node)

            if len(last_list) < self.batch_count:
                zero_list = np.zeros(self.batch_count - len(last_list), dtype="int")
                result_list = np.hstack((np.array(last_list), zero_list)).tolist()
            elif len(last_list) > self.batch_count:
                result_list = np.array(last_list).tolist()[-self.batch_count:]
            else:
                result_list = np.array(last_list).tolist()[0:self.batch_count]
            train_x.append(result_list)

            result = np.zeros(4, dtype="int").tolist()
            result[int(node * 10) - 1] = 1
            train_y.append(result)

        last_one = random.sample(self.ball_set, 1)[0]
        result = np.zeros(4, dtype="int").tolist()
        result[int(last_one * 10) - 1] = 1
        train_y.append(result)

        return np.array(train_x), np.array(train_y[-group])

    def __my_test_next_batch_order_go_next(self, last_batch, next_ico, last_test):
        train_x, train_y = last_batch
        train_x = train_x.tolist()
        train_y = train_y.tolist()

        last_list = train_x[-1][:]
        last_list.append(next_ico)
        if len(last_list) < self.batch_count:
            zero_list = np.zeros(self.batch_count - len(last_list), dtype="int")
            next_list = np.hstack((np.array(last_list), zero_list)).tolist()
        elif len(last_list) > self.batch_count:
            next_list = np.array(last_list).tolist()[-self.batch_count:]
        else:
            next_list = np.array(last_list).tolist()[0:self.batch_count]

        result = np.zeros(4, dtype="int").tolist()
        result[int(next_ico * 10) - 1] = 1

        if last_test == train_x[-1]:  # 第一回合,取的上次保存数据的最后一项，所以用此做对比
            train_y[-1] = result
        else:  # 其它回合，开始向前迭代数据
            train_x.append(last_test)
            train_y.append(result)

        return np.array(train_x[-self.batch_count:]), np.array(train_y[-self.batch_count:]), [next_list]

    def __init_tensorflow(self):
        print("----------init----------")
        x = tf.placeholder(self.my_date_type, [None, self.batch_count])
        y_ = tf.placeholder(self.my_date_type, [None, 4])

        W = tf.Variable(tf.zeros([self.batch_count, 4]), name="W")  # 变量参数,初始化为全零的二维矩阵，784行，10列，因为要做矩阵乘法
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
        if test_data is None:
            test_data = self.__my_train_next_batch_order(self.batch_count)
        batch_xs, batch_ys = test_data
        prediction = 0
        i = 0

        precise = 0
        self.__save_input(batch_xs, batch_ys)
        while prediction != 1 or precise < 500:
            # print(self.sess.run((train_step, y_prediction), feed_dict={x: batch_xs, y_: batch_ys}))  # 开始练习
            self.sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})  # 开始练习
            # prediction = self.sess.run(accuracy, feed_dict={x: batch_xs, y_: batch_ys})
            prediction = self.sess.run(accuracy, feed_dict={x: batch_xs, y_: batch_ys})
            if prediction == 1:
                precise += 1
            i += 1
            if i % 250 == 0:  # 每十步保存下数据
                print("%d round:%g" % (i, prediction))  # 打印准确率
                saver.save(self.sess, save_path)
        print("----------complete-------")

    def __init_tensorflow_test(self):
        print("----------init----------")
        x = tf.placeholder(self.my_date_type, [None, self.batch_count])
        y_ = tf.placeholder(self.my_date_type, [None, 4])

        W = tf.Variable(tf.zeros([self.batch_count, 4]), name="W")  # 变量参数,初始化为全零的二维矩阵，784行，10列，因为要做矩阵乘法
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
        test_x = []
        if test_data is None:
            test_data = self.__my_train_next_batch_order(self.batch_count)
        batch_xs, batch_ys = test_data
        prediction = 0
        i = 0
        loss = 0
        loss_combo = 0
        win_combo = 0

        round_set = 300
        test_result = [0, 0, 0, 0]
        prediction_result = [0, 0, 0, 0]
        precise = 0
        for j in range(round_set):
            self.__save_input(batch_xs, batch_ys)
            while prediction != 1 or precise < 500:
                # print(self.sess.run((train_step, y_prediction), feed_dict={x: batch_xs, y_: batch_ys}))  # 开始练习
                self.sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})  # 开始练习
                # prediction = self.sess.run(accuracy, feed_dict={x: batch_xs, y_: batch_ys})
                prediction = self.sess.run(accuracy, feed_dict={x: batch_xs, y_: batch_ys})
                if prediction == 1:
                    precise += 1
                i += 1
                if i % 250 == 0:  # 每十步保存下数据
                    print("%d round:%g" % (i, prediction))  # 打印准确率
                    saver.save(self.sess, save_path)
                    self.__save_input(batch_xs, batch_ys)

            if len(test_x) == 0:
                test_x = [batch_xs[-1].tolist()]
            prediction_bot = self.sess.run(y_prediction, feed_dict={x: test_x})[0]
            if len(play_data) == 0:
                play_data = test_data
            # prediction_bot_thinking = [0, 0, 0, 0]
            # for k in range(4):
            #     thinking_data_x, thinking_data_y = self.__my_test_next_batch_order_assign_one(play_data, (k + 1) / 10)
            #     for l in range(1000):
            #         get_prediction = self.sess.run(y_prediction, feed_dict={x: thinking_data_x, y_: thinking_data_y})
            #         prediction_bot_thinking[get_prediction[-1]] += 1
            # print("bot thinking it is:%d" % (np.argmax(prediction_bot_thinking, 0) + 1))
            # print("bot thinking it is:%s" % str(prediction_bot_thinking))

            # play_data = self.__my_test_next_batch_order(play_data, 1)
            # batch_xs, batch_ys = play_data

            real_x, real_y = self.__my_test_next_batch_order(play_data, 1)
            real_value = real_x[-1][-1]
            real_value_index = int(real_value * 10 - 1)
            test_result[real_value_index] += 1
            if prediction_bot == real_value_index:  # 此转换原理，A为0.1 B为0.2 C为0.3 D为0.4 所以对应[0,0,0,0]的显示结果
                loss_combo = 0
                win_combo += 1
                result_string = "win" + "%s" % ("" if win_combo == 1 else ("--%d combo" % win_combo))
                prediction_result[prediction_bot] += 1
                precise = -1000
            else:
                win_combo = 0
                loss_combo += 1
                result_string = "lose" + "%s" % ("" if loss_combo == 1 else ("--%d combo" % loss_combo)) \
                                + ", it is:" + str(int(real_value_index))
                loss += 1
                precise = 0

            print("round:%d try:%s %s" % (j, prediction_bot, result_string))
            batch_xs, batch_ys, test_x = self.__my_test_next_batch_order_go_next(play_data, real_value, test_x[0])
            play_data = batch_xs, batch_ys

            # prediction, get_prediction = self.sess.run((accuracy, y_prediction), feed_dict={x: batch_xs, y_: batch_ys})
            # test_key = np.argmax(batch_ys[-1], 0)
            # test_result[test_key] += 1
            # if get_prediction[-1] == test_key:
            #     result_string = "win"
            #     prediction_result[test_key] += 1
            # else:
            #     result_string = "lose"
            print("=====================")

        print("--------complete----correct:%f------" % ((round_set - loss) / round_set))
        print("=====ending report========")
        for i in range(4):
            print("%d: %d / %d = %f%%" % (
                (i + 1), prediction_result[i], test_result[i],
                prediction_result[i] / test_result[i] if test_result[i] != 0 else 0))
        prediction_result[0] *= 2
        prediction_result[1] *= 3
        prediction_result[2] *= 6
        prediction_result[3] *= 50
        print("===========cost:%d============" % (sum(prediction_result) - round_set))

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

    def do_prediction(self):
        pass


if __name__ == "__main__":
    bot = TensorflowBanCaicaile()
