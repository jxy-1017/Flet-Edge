import tensorflow as tf
from tensorflow.keras import layers, Model, Sequential


class ConvBNReLU(layers.Layer):
    def __init__(self,
                 filters: int = 1,
                 kernel_size: int = 1,
                 strides: int = 1,
                 padding: str = 'same',
                 **kwargs):
        super(ConvBNReLU, self).__init__(**kwargs)

        self.conv = layers.Conv2D(filters=filters,
                                  kernel_size=kernel_size,
                                  strides=strides,
                                  padding=padding,
                                  use_bias=False,
                                  kernel_regularizer=tf.keras.regularizers.l2(4e-5),
                                  name="conv1")
        self.bn = layers.BatchNormalization(momentum=0.9, name="bn")
        self.relu = layers.ReLU()

    def call(self, inputs, training=None, **kwargs):
        x = self.conv(inputs)
        x = self.bn(x, training=training)
        x = self.relu(x)
        return x


class DWConvBN(layers.Layer):
    def __init__(self,
                 kernel_size: int = 3,
                 strides: int = 1,
                 padding: str = 'same',
                 **kwargs):
        super(DWConvBN, self).__init__(**kwargs)
        self.dw_conv = layers.DepthwiseConv2D(kernel_size=kernel_size,
                                              strides=strides,
                                              padding=padding,
                                              use_bias=False,
                                              kernel_regularizer=tf.keras.regularizers.l2(4e-5),
                                              name="dw1")
        self.bn = layers.BatchNormalization(momentum=0.9, name="bn")

    def call(self, inputs, training=None, **kwargs):
        x = self.dw_conv(inputs)
        x = self.bn(x, training=training)
        return x


class ChannelShuffle(layers.Layer):
    def __init__(self, shape, groups: int = 2, **kwargs):
        super(ChannelShuffle, self).__init__(**kwargs)
        batch_size, height, width, num_channels = shape
        assert num_channels % 2 == 0
        channel_per_group = num_channels // groups

        self.reshape1 = layers.Reshape((height, width, groups, channel_per_group))
        self.reshape2 = layers.Reshape((height, width, num_channels))

    def call(self, inputs, **kwargs):
        x = self.reshape1(inputs)
        x = tf.transpose(x, perm=[0, 1, 2, 4, 3])
        x = self.reshape2(x)
        return x


class ChannelSplit(layers.Layer):
    def __init__(self, num_splits: int = 2, **kwargs):
        super(ChannelSplit, self).__init__(**kwargs)
        self.num_splits = num_splits

    def call(self, inputs, **kwargs):
        b1, b2 = tf.split(inputs,
                          num_or_size_splits=self.num_splits,
                          axis=-1)
        return b1, b2


def shuffle_block_s1(inputs, output_c: int, stride: int, prefix: str):
    if stride != 1:
        raise ValueError("illegal stride value.")

    assert output_c % 2 == 0
    branch_c = output_c // 2

    x1, x2 = ChannelSplit(name=prefix + "/split")(inputs)

    x2 = ConvBNReLU(filters=branch_c, name=prefix + "/b2_conv1")(x2)
    x2 = DWConvBN(kernel_size=3, strides=stride, name=prefix + "/b2_dw1")(x2)
    x2 = ConvBNReLU(filters=branch_c, name=prefix + "/b2_conv2")(x2)

    x = layers.Concatenate(name=prefix + "/concat")([x1, x2])
    x = ChannelShuffle(x.shape, name=prefix + "/channelshuffle")(x)

    return x


def shuffle_block_s2(inputs, output_c: int, stride: int, prefix: str):
    if stride != 2:
        raise ValueError("illegal stride value.")

    assert output_c % 2 == 0
    branch_c = output_c // 2

    x1 = DWConvBN(kernel_size=3, strides=stride, name=prefix + "/b1_dw1")(inputs)
    x1 = ConvBNReLU(filters=branch_c, name=prefix + "/b1_conv1")(x1)

    x2 = ConvBNReLU(filters=branch_c, name=prefix + "/b2_conv1")(inputs)
    x2 = DWConvBN(kernel_size=3, strides=stride, name=prefix + "/b2_dw1")(x2)
    x2 = ConvBNReLU(filters=branch_c, name=prefix + "/b2_conv2")(x2)

    x = layers.Concatenate(name=prefix + "/concat")([x1, x2])
    x = ChannelShuffle(x.shape, name=prefix + "/channelshuffle")(x)

    return x


def shufflenet_v2(num_classes: int,
                  input_shape: tuple,
                  stages_repeats: list,
                  stages_out_channels: list):
    img_input = layers.Input(shape=input_shape)
    if len(stages_repeats) != 3:
        raise ValueError("expected stages_repeats as list of 3 positive ints")
    if len(stages_out_channels) != 5:
        raise ValueError("expected stages_out_channels as list of 5 positive ints")

    x = ConvBNReLU(filters=stages_out_channels[0],
                   kernel_size=3,
                   strides=2,
                   name="conv1")(img_input)

    x = layers.MaxPooling2D(pool_size=(3, 3),
                            strides=2,
                            padding='same',
                            name="maxpool")(x)

    stage_name = ["stage{}".format(i) for i in [2, 3, 4]]
    for name, repeats, output_channels in zip(stage_name,
                                              stages_repeats,
                                              stages_out_channels[1:]):
        for i in range(repeats):
            if i == 0:
                x = shuffle_block_s2(x, output_c=output_channels, stride=2, prefix=name + "_{}".format(i))
            else:
                x = shuffle_block_s1(x, output_c=output_channels, stride=1, prefix=name + "_{}".format(i))

    x = ConvBNReLU(filters=stages_out_channels[-1], name="conv5")(x)

    x = layers.GlobalAveragePooling2D(name="globalpool")(x)

    x = layers.Dense(units=num_classes, name="fc")(x)
    x = layers.Softmax()(x)

    model = Model(img_input, x, name="ShuffleNetV2_1.0")

    return model


def shufflenet_v2_x0_5(num_classes=1000, input_shape=(224, 224, 3)):
    model = shufflenet_v2(num_classes=num_classes,
                          input_shape=input_shape,
                          stages_repeats=[4, 8, 4],
                          stages_out_channels=[24, 48, 96, 192, 1024])
    return model


def shufflenet05(weights, input_size):
    model = shufflenet_v2_x0_5(input_shape=(input_size, input_size, 3), num_classes=10)
    return model


def mobilenetv2(weights, input_size):
    base_model = tf.keras.applications.mobilenet.MobileNet(weights=weights, input_shape=(input_size, input_size, 3),
                                                           include_top=False)
    base_model.trainable = True
    model = tf.keras.Sequential([
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(10, activation="softmax")
    ])
    return model


def resnet50(weights, input_size):
    base_model = tf.keras.applications.resnet50.ResNet50(weights=weights, input_shape=(input_size, input_size, 3),
                                                         include_top=False)
    base_model.trainable = True
    model = tf.keras.Sequential([
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(10, activation="softmax")
    ])
    return model


class BasicBlock(layers.Layer):
    expansion = 1

    def __init__(self, out_channel, strides=1, down_sample=None, **kwargs):
        super(BasicBlock, self).__init__(**kwargs)
        self.conv1 = layers.Conv2D(out_channel, kernel_size=3, strides=strides, padding='SAME', use_bias=False,
                                   name='conv1')
        self.bn1 = layers.BatchNormalization(momentum=0.9, epsilon=1e-5, name='conv1/BatchNorm')

        self.conv2 = layers.Conv2D(out_channel, kernel_size=3, strides=1, padding='SAME', use_bias=False, name='conv2')
        self.bn2 = layers.BatchNormalization(momentum=0.9, epsilon=1e-5, name='conv2/BatchNorm')

        self.down_sample = down_sample
        self.add = layers.Add()
        self.relu = layers.ReLU()

    def call(self, inputs, training=False):
        if self.down_sample is not None:
            identity = self.down_sample(inputs)
        else:
            identity = inputs

        x = self.conv1(inputs)
        x = self.bn1(x, training=training)
        x = self.relu(x)

        x = self.conv2(x)
        x = self.bn2(x, training=training)

        x = self.add([identity, x])
        x = self.relu(x)

        return x


class Bottleneck(layers.Layer):
    expansion = 4

    def __init__(self, out_channel, strides=1, down_sample=None, **kwargs):
        super(Bottleneck, self).__init__(**kwargs)
        self.conv1 = layers.Conv2D(out_channel, kernel_size=1, use_bias=False, name='conv1')
        self.bn1 = layers.BatchNormalization(momentum=0.9, epsilon=1e-5, name='conv1/BatchNorm')

        self.conv2 = layers.Conv2D(out_channel, kernel_size=3, strides=strides, padding='SAME', use_bias=False,
                                   name='conv2')
        self.bn2 = layers.BatchNormalization(momentum=0.9, epsilon=1e-5)

        self.conv3 = layers.Conv2D(out_channel * self.expansion, kernel_size=1, use_bias=False, name='conv3')
        self.bn3 = layers.BatchNormalization(momentum=0.9, epsilon=1e-5, name='conv3/BatchNorm')

        self.down_sample = down_sample
        self.add = layers.Add()
        self.relu = layers.ReLU()

    def call(self, inputs, training=False):
        if self.down_sample is not None:
            identity = self.down_sample(inputs)
        else:
            identity = inputs

        x = self.conv1(inputs)
        x = self.bn1(x, training=training)
        x = self.relu(x)

        x = self.conv2(x)
        x = self.bn2(x, training=training)
        x = self.relu(x)

        x = self.conv3(x)
        x = self.bn3(x, training=training)

        x = self.add([identity, x])
        x = self.relu(x)

        return x


class ResNet(Model):
    def __init__(self, block, blocks_num, num_classes=1000, include_top=True, **kwargs):
        super(ResNet, self).__init__(**kwargs)
        self.include_top = include_top

        self.conv1 = layers.Conv2D(filters=64, kernel_size=7, strides=2, padding='SAME', use_bias=False, name='conv1')
        self.bn1 = layers.BatchNormalization(momentum=0.9, epsilon=1e-5, name='conv1/BatchNorm')
        self.relu1 = layers.ReLU(name='relu1')

        self.maxpool1 = layers.MaxPool2D(pool_size=3, strides=2, padding='SAME', name='maxpool1')

        self.block1 = self._make_layer(block, True, 64, blocks_num[0], name='block1')
        self.block2 = self._make_layer(block, False, 128, blocks_num[1], strides=2, name='block2')
        self.block3 = self._make_layer(block, False, 256, blocks_num[2], strides=2, name='block3')
        self.block4 = self._make_layer(block, False, 512, blocks_num[3], strides=2, name='block4')

        if self.include_top == True:
            self.avgpool = layers.GlobalAveragePooling2D(name='avgpool1')
            self.fc = layers.Dense(num_classes, name='logits')
            self.softmax = layers.Softmax()

    def call(self, inputs, training=False, **kwargs):
        x = self.conv1(inputs)
        x = self.bn1(x)
        x = self.relu1(x)
        x = self.maxpool1(x)

        x = self.block1(x, training=training)
        x = self.block2(x, training=training)
        x = self.block3(x, training=training)
        x = self.block4(x, training=training)

        if self.include_top == True:
            x = self.avgpool(x)
            x = self.fc(x)
            x = self.softmax(x)

        return x

    def _make_layer(self, block, first_block, channel, block_num, name=None, strides=1):
        down_sample = None
        if strides != 1 or first_block is True:
            down_sample = Sequential([
                layers.Conv2D(channel * block.expansion, kernel_size=1, strides=strides, use_bias=False, name='conv1'),
                layers.BatchNormalization(momentum=0.9, epsilon=1e-5, name='BatchNorm')
            ], name='shortcut')

        layers_list = []
        layers_list.append(block(channel, down_sample=down_sample, strides=strides, name="unit_1"))

        for index in range(1, block_num):
            layers_list.append(block(channel, name='unit_' + str(index + 1)))

        return Sequential(layers_list, name=name)


def resnet_34(num_classes=1000, include_top=True):
    block = BasicBlock
    block_num = [3, 4, 6, 3]
    return ResNet(block, block_num, num_classes, include_top)


def resnet34(weights, input_size):
    model = resnet_34(num_classes=10, include_top=True)
    return model


def vgg19(weights, input_size):
    base_model = tf.keras.applications.vgg19.VGG19(weights=weights, input_shape=(input_size, input_size, 3),
                                                   include_top=False)
    base_model.trainable = True
    model = tf.keras.Sequential([
        base_model,
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(4096, activation="relu"),
        tf.keras.layers.Dense(4096, activation="relu"),
        tf.keras.layers.Dense(10, activation="softmax")
    ])
    return model
