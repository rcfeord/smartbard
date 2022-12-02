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

def select_keyword(keyword_df: pd.DataFrame, num_keywords=1, proba=None) -> list:
    """
    takes a pd.DataFrame with Id, Label, and Probability from image feature detection
    selects keywords based on either:
        - number of keywords
        - probability of accurate label prediction
    """
    if proba is not None:
        keyword_list = pd.Series.to_list(keyword_df['Label'][keyword_df['Probability']>proba])
    else:
        keyword_list= pd.Series.to_list(keyword_df['Label'].iloc[:num_keywords])
    return keyword_list
