"""
The inner control file passes three parameters to the program: String form of worker_list, task_index, and training
parameter list in string form config_list_indir_to_change_str。

Example: worker_list_str: 192.168.1.101_192.168.1.102_192.168.1.103;
task_index: 2 (String)
config_list_indir_to_change_str: nano3_128_shufflenet05_imagenet_32_Adam_1e-05_20_391_79_cifar10;

note: The function of each method can be known by referring to its method name.
"""
import os
import tensorflow as tf
import json
import time
import tf_dt_change_models as tf_models
import sys


def worker_list_covert_to_worker_list(worker_list_str):
    worker_list_str = worker_list_str

    worker_list = worker_list_str.split("_")

    return worker_list


def config_list_str_covert_to_config_list(config_list_indir_to_change_str):
    config_list_indir_to_change_str = config_list_indir_to_change_str
    config_list_indir_to_change = config_list_indir_to_change_str.split("_")

    return config_list_indir_to_change


if __name__ == '__main__':

    worker_list_str = sys.argv[1]
    task_index = sys.argv[2]
    config_list_indir_to_change_str = sys.argv[3]
    print("worker_list_str: ", worker_list_str)
    print("task_index: ", task_index)

    worker_list = worker_list_covert_to_worker_list(worker_list_str)

    config_list_indir_to_change = config_list_str_covert_to_config_list(config_list_indir_to_change_str)

    task_index = int(task_index)

    device_name = config_list_indir_to_change[0]

    training_batchsize = config_list_indir_to_change[1]
    training_batchsize = int(training_batchsize)

    training_model_name = config_list_indir_to_change[2]

    weights = config_list_indir_to_change[3]

    training_input_size = config_list_indir_to_change[4]
    training_input_size = int(training_input_size)

    optimizer_name = config_list_indir_to_change[5]

    learning_rate_value = config_list_indir_to_change[6]
    learning_rate_value = float(learning_rate_value)

    epochs = config_list_indir_to_change[7]
    epochs = int(epochs)

    steps_per_epoch = config_list_indir_to_change[8]
    steps_per_epoch = int(steps_per_epoch)

    validation_steps = config_list_indir_to_change[9]
    validation_steps = int(validation_steps)

    dataset_name = config_list_indir_to_change[10]

    print("Distributed training of jetson nano: %s." % device_name)

    os.environ['CUDA_VISIBLE_DEVICES'] = "0"

    os.environ['TF_CONFIG'] = json.dumps({
        'cluster': {
            'worker': worker_list
        },
        'task': {'type': 'worker', 'index': task_index}
    })

    strategy = tf.distribute.experimental.MultiWorkerMirroredStrategy()


    def preprocess(x, y):
        x = tf.cast(x, dtype=tf.float32) / 255
        y = tf.cast(y, dtype=tf.int32)
        return x, y


    (x, y), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
    dbxy = tf.data.Dataset.from_tensor_slices((x, y))
    dbxy.shuffle(50000)
    dbxyt = tf.data.Dataset.from_tensor_slices((x_test, y_test))
    dbxyt.shuffle(10000)

    dbxy2 = dbxy.map(preprocess)
    dbxy3 = dbxy2.batch(training_batchsize)
    dbxyt2 = dbxyt.map(preprocess)
    dbxyt3 = dbxyt2.batch(training_batchsize)

    options = tf.data.Options()
    options.experimental_distribute.auto_shard_policy = tf.data.experimental.AutoShardPolicy.DATA
    train_datasets_no_auto_shard = dbxy3.with_options(options)
    test_datasets_no_auto_shard = dbxyt3.with_options(options)

    with strategy.scope():

        model = tf_models.mobilenetv2(weights, training_input_size)

        if training_model_name == "shufflenet05":
            model = tf_models.shufflenet05(weights, training_input_size)
        elif training_model_name == "mobilenetv2":
            model = tf_models.mobilenetv2(weights, training_input_size)
        elif training_model_name == "resnet50":
            model = tf_models.resnet50(weights, training_input_size)
        elif training_model_name == "resnet34":
            model = tf_models.resnet34(weights, training_input_size)
        elif training_model_name == "vgg19":
            model = tf_models.vgg19(weights, training_input_size)
        print(model)

        if optimizer_name == "Adam":
            model.compile(
                optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate_value),
                loss=tf.keras.losses.sparse_categorical_crossentropy,
                metrics=['acc']
            )
        if optimizer_name == "SGD":
            model.compile(
                optimizer=tf.keras.optimizers.SGD(learning_rate=learning_rate_value),
                loss=tf.keras.losses.sparse_categorical_crossentropy,
                metrics=['acc']
            )
        if optimizer_name == "Adadelta":
            model.compile(
                optimizer=tf.keras.optimizers.Adadelta(learning_rate=learning_rate_value),
                loss=tf.keras.losses.sparse_categorical_crossentropy,
                metrics=['acc']
            )
        if optimizer_name == "Adagrad":
            model.compile(
                optimizer=tf.keras.optimizers.Adagrad(learning_rate=learning_rate_value),
                loss=tf.keras.losses.sparse_categorical_crossentropy,
                metrics=['acc']
            )
        if optimizer_name == "Adamax":
            model.compile(
                optimizer=tf.keras.optimizers.Adamax(learning_rate=learning_rate_value),
                loss=tf.keras.losses.sparse_categorical_crossentropy,
                metrics=['acc']
            )
        if optimizer_name == "Ftrl":
            model.compile(
                optimizer=tf.keras.optimizers.Ftrl(learning_rate=learning_rate_value),
                loss=tf.keras.losses.sparse_categorical_crossentropy,
                metrics=['acc']
            )
        if optimizer_name == "Nadam":
            model.compile(
                optimizer=tf.keras.optimizers.Nadam(learning_rate=learning_rate_value),
                loss=tf.keras.losses.sparse_categorical_crossentropy,
                metrics=['acc']
            )
        if optimizer_name == "RMSprop":
            model.compile(
                optimizer=tf.keras.optimizers.RMSprop(learning_rate=learning_rate_value),
                loss=tf.keras.losses.sparse_categorical_crossentropy,
                metrics=['acc']
            )

    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    print("Device %s start training %s %s epoch(s) with %s dataset." % (
        device_name, training_model_name, epochs, dataset_name))

    model.fit(train_datasets_no_auto_shard, validation_data=test_datasets_no_auto_shard, epochs=epochs,
              steps_per_epoch=steps_per_epoch, validation_steps=validation_steps)
