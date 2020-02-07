from keras.datasets import mnist
from keras.utils import to_categorical
from keras import models, layers


def main():
    ((train_images, train_labels),
     (test_images, test_labels)) = mnist.load_data()
    net = models.Sequential()
    net.add(layers.Dense(512, activation='relu', input_shape=(28 * 28,)))
    net.add(layers.Dense(10, activation='softmax'))
    net.compile(optimizer='rmsprop',
                loss='categorical_crossentropy',
                metrics=['accuracy'])

    train_images = train_images.reshape((60000, 28 * 28))
    train_images = train_images.astype('float32') / 255
    test_images = test_images.reshape((10000, 28 * 28))
    test_images = test_images.astype('float32') / 255
    train_labels = to_categorical(train_labels)
    test_labels = to_categorical(test_labels)

    net.fit(train_images, train_labels, epochs=5, batch_size=128)
    test_loss, test_acc = net.evaluate(test_images, test_labels)
    print('test_acc:', test_acc)


if __name__ == '__main__':
    main()
