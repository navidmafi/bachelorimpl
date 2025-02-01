import tensorflow as tf
import matplotlib.pyplot as plt


def apply_obsv_mask(image: tf.Tensor, obvmask: tf.Tensor) -> tf.Tensor:
    return tf.multiply(image, tf.cast(obvmask, FLOAT))


def viz_grid(batch: tf.Tensor):
    batch_size: int = batch.shape[0]  # type: ignore
    fig, axes = plt.subplots(nrows=1, ncols=batch_size, figsize=(5, 5))
    for i in range(batch_size):
        # Original image
        axes[i].imshow(tf.cast(batch[i], dtype=tf.float32).numpy())  # type: ignore
        axes[i].axis("off")
    plt.tight_layout()
    plt.show()


def reconstruct(original: tf.Tensor, reconstruct: tf.Tensor, obvmask: tf.Tensor):
    return tf.add(
        tf.multiply(tf.cast(obvmask, FLOAT), original),
        tf.multiply(tf.cast(tf.logical_not(obvmask), FLOAT), reconstruct),
    )
