import tensorflow as tf

from data import daily
from data.daily import WorkdayAccessor


def get_training_data():
    byn_accessor = WorkdayAccessor([daily.bynusd])
    all_accessor = WorkdayAccessor(daily.get_all())

    y = byn_accessor.get_latest(2)
    x = [all_accessor.get_previous(e['date']) for e in y]

    def to_array(entry):
        return [v for k, v in entry.items() if k != 'date']

    y_array = [to_array(e) for e in y]
    x_array = [to_array(e) for e in x]

    return x_array, y_array


x_in = tf.placeholder(tf.float32, [None, 4])
y_out = tf.placeholder(tf.float32, [None, 1])

w = tf.Variable(tf.random_normal([4, 1]))
b = tf.Variable(tf.random_normal([1]))

sess = tf.InteractiveSession()
tf.global_variables_initializer().run()

y = tf.matmul(x_in, w) + b

squared = tf.square(y - y_out)
error = tf.reduce_sum(squared)

optimizer = tf.train.GradientDescentOptimizer(0.01)
train = optimizer.minimize(error)

def test():
    x_data, y_data = get_training_data()

    for i in range(10):
        sess.run(train, {
            x_in: x_data,
            y_out: y_data
        })


    res = sess.run(y, {
        x_in: x_data
    })
    print(res)