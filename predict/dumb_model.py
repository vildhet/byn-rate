import json
import tensorflow as tf

from data import daily
from data.daily import WorkdayAccessor


byn_accessor = WorkdayAccessor([daily.bynusd])
all_accessor = WorkdayAccessor(daily.get_all())


NUMBER_OF_DAYS = 100

# Helpers

def print_json(data):
    print(json.dumps(data, indent=4))


def to_one_hot(value, size):
    assert type(value) == int
    assert value < size

    array = [0] * size
    array[value] = 1
    return array

# Data

def gen_output_data(byn_data):
    it = iter(byn_data)
    previous_day = next(it)

    y_data = list()

    for day_data in it:
        value = int(day_data['bynusd'] > previous_day['bynusd'])
        # [0, 1] increased
        # [1, 0] decreased
        y_data.append(to_one_hot(value, 2))
        previous_day = day_data
    return y_data
    

def gen_input_data(date):
    # print('Input for date', date)
    previous_entries = all_accessor.get_latest(3, date)[:-1]
    # print_json(previous_entries)

    x_data = []

    # brent
    # byneur
    # bynusd
    # eurrub

    for key in sorted(previous_entries[0].keys()):
        if key == 'date':
            continue
        value = int(previous_entries[1][key] > previous_entries[0][key])
        x_data += to_one_hot(value, 2)

    return x_data

def get_training_data(to_date):
    byn_data = byn_accessor.get_latest(NUMBER_OF_DAYS + 1, to_date)
    byn_output = byn_data[1:]

    y_data = gen_output_data(byn_data)
    x_data = [gen_input_data(e['date']) for e in byn_output]

    # print(y_data)
    # print(x_data)
    return x_data, y_data


# Training code begins

IN_SIZE = 8
H_SIZE = 100
OUT_SIZE = 2


x_in = tf.placeholder(tf.float32, [None, IN_SIZE])
y_out = tf.placeholder(tf.float32, [None, OUT_SIZE])

# input -> hidden
w = tf.Variable(tf.random_normal([IN_SIZE, H_SIZE]))
b = tf.Variable(tf.random_normal([H_SIZE]))

# hidden -> output
w2 = tf.Variable(tf.random_normal([H_SIZE, OUT_SIZE]))
b2 = tf.Variable(tf.random_normal([OUT_SIZE]))

sess = tf.InteractiveSession()
tf.global_variables_initializer().run()

# Create model
m = tf.matmul(x_in, w) + b
m = tf.sigmoid(m)

m = tf.matmul(m, w2) + b2
y = tf.nn.sigmoid(m)

# Loss
squared = tf.square(y - y_out)
error = tf.reduce_sum(squared)

optimizer = tf.train.GradientDescentOptimizer(0.01)
train = optimizer.minimize(error)

def test():
    print('Increased:', to_one_hot(1, 2))
    print('Decreased:', to_one_hot(0, 2))

    x_data, y_data = get_training_data('2017-07-20')

    for i in range(100):
        sess.run(train, {
            x_in: x_data,
            y_out: y_data
        })

    res = sess.run(y, {
        x_in: x_data
    })
    # print(res)
    # print(y_data)

    # x_control_day = [gen_input_data('2017-07-21')]
    # brent byneur bynusd eurrub
    x_control_day = [[1, 0, 1, 0, 1, 0, 0, 1]]

    res = sess.run(y, {
        x_in: x_control_day
    })

    print(res)
