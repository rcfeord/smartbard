# SmartBard
#### *Image-Inspired Limerick Generation using Deep Learning*

This project contains the code and data for a deep learning model that generates limericks based on input images.

The model was designed to recognize the objects and scenes depicted in the images using VGG-16, and then generate appropriate limericks using GPT-2 and BERT language models.
It was trained on a dataset of almost 65000 limericks.

The final model was able to generate limericks that were coherent and relevant to the input images. It has the potential to be used as a creative writing tool, allowing users to generate unique and amusing poetry based on their own images. It could also be used in educational settings to teach language and poetry skills in a fun and interactive way.

## Dependencies

The following libraries and frameworks are required to run the code in this repository:

-   Python 3.7 or higher
-   NumPy
-   Pandas
-  Tensorflow 2.9.0 or higher
-   PyTorch
-   transformers

## Running the Code

To generate limericks using the model, run the following command and provide the path to an input image:

`python -m smartbard path/to/image`
