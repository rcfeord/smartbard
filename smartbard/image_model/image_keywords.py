import pandas as pd
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing.image import load_img, img_to_array


def image_to_keywords(image_path:str, num_labels=10) -> pd.DataFrame:
    """
    takes an image and uses vgg16 to associate labels
    returns a pd.DataFrame with Id, Label, and Probability
    """
    # instantiate model
    model = VGG16()
    # preprocess image
    img = load_img(image_path,target_size=(224,224))
    img = img_to_array(img)
    img = img.reshape((1,img.shape[0],img.shape[1],img.shape[2]))
    img = preprocess_input(img)
    feature = model.predict(img,verbose=0)
    # predict image labels
    label = decode_predictions(feature, top=num_labels)
    label = label[0][:]
    keyword_probabilities = pd.DataFrame(label, columns =['Id', 'Label', 'Probability'])
    return keyword_probabilities

#comment
