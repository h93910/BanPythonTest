import sonnet as snt

# Provide your own functions to generate data Tensors.
from sonnet.examples.brnn_ptb import FLAGS
from tensorflow.examples.tutorials.mnist import input_data

def get_training_data():
    return mnist.train.next_batch(100)  # 随机取一百个练习值


def get_test_data():
    return mnist.test.images, mnist.test.labels


mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

test_data = get_test_data()
train_data = get_training_data()

# Construct the module, providing any configuration necessary.
linear_regression_module = snt.Linear(output_size=[None, 10])

# Connect the module to some inputs, any number of times.
train_predictions = linear_regression_module(train_data)
test_predictions = linear_regression_module(test_data)

print(train_predictions)
print(test_predictions)
