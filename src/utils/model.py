import tensorflow as tf
import logging
import io
import os
from src.utils.common import get_timestamp

def _get_model_summary(model):
    """To print model summary in log file

    Args:
        model (model): model

    Returns:
        _type_: summry of the model 
    """
    with io.StringIO() as stream:
        model.summary(
            print_fn=lambda x: stream.write(f"{x}\n")
        )
        summary_str = stream.getvalue()
    return summary_str

def get_VGG16_model(input_shape: list, model_path: str) -> tf.keras.models.Model:
    """saving and returning the base model extractd from VGG16 model

    Args:
        input_shape (list): shape of the input image
        model_path (str): path to save the model

    Returns:
        tf.python.keras.engine.functional.Functional: base model
    """

    model = tf.keras.applications.vgg16.VGG16(
        input_shape=input_shape,
        weights='imagenet',
        include_top=False)
    
    logging.info(f"VGG16 base model summary :\n{_get_model_summary(model)}")
    model.save(model_path)
    logging.info(f"VGG16 base model saved at : {model_path} ")

    return model

def prepare_full_model(base_model, learning_rate,CLASSES = 2, freeze_all=True, freeze_till=None) -> tf.keras.models.Model:
    """Complete Transfer learning model architecture

    Args:
        base_model (tf.keras.models.Model): base VGG16 model
        learning_rate (float): learning rate for training 
        CLASSES (int, optional): No. of classes to train for. Defaults to 2.
        freeze_all (bool, optional): freezes all the layers to male them untrainable. Defaults to True.
        freeze_till (int, optional): this is the values which defines the extent of the layers to which we want to train. Defaults to None.

    Returns:
        tf.keras.models.Model: full model architecture ready to be trained
    """

    if freeze_all:
        for layer in base_model.layers:
            layer.trainable = False
    elif(freeze_till is not None) and (freeze_till > 0):
        for layers in base_model.layers[:-freeze_till]:
            layer.trainable = False
    
    # add our layer to the base model
    flatten_in = tf.keras.layers.Flatten()(base_model.output)

    prediction = tf.keras.layers.Dense(
        units=CLASSES,
        activation="softmax"
    )(flatten_in)

    full_model = tf.keras.models.Model(
        inputs=base_model.input,
        outputs=prediction
    )

    full_model.compile(
        optimizer = tf.keras.optimizers.SGD(learning_rate=learning_rate),
        loss = tf.keras.losses.CategoricalCrossentropy(),
        metrics=["accuracy"]
    )

    logging.info(f"Custom model is compiled and ready to be trained ... \n")
    
    logging.info(f"full model summary {_get_model_summary(full_model)}")

    full_model.summary()


    return full_model


def load_full_model(untrained_full_model_path: str) -> tf.keras.models.Model:
    """To load untrained full model

    Args:
        untrained_full_model_path (str): untrained model path

    Returns:
        tf.keras.models.Model: untrained model
    """
    model = tf.keras.models.load_model(untrained_full_model_path)
    logging.info(f"untrained models is read from: {untrained_full_model_path}")
    logging.info(f"untrained full model summary: \n{_get_model_summary(model)}")
    return model

def get_unqique_path_to_save_model(trained_model_dir: str, model_name: str = "model") -> str:
    """unique path to save the trained model

    Args:
        trained_model_dir (str): trained model to be saved
        model_name (str, optional): name of the model. Defaults to "model".

    Returns:
        str: unique path
    """
    timestamp = get_timestamp(name=model_name)
    unique_model_name = f"{timestamp}_.h5"
    unique_model_path = os.path.join(trained_model_dir, unique_model_name)

    return unique_model_path