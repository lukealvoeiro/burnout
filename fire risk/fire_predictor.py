import numpy as np
from sklearn import preprocessing
from sklearn import svm
from sklearn import metrics
import pandas as pd
from sklearn.model_selection import train_test_split  
from keras.layers import Dense, Flatten, LSTM, Conv1D, MaxPooling1D, Dropout, Activation
from keras.models import Sequential, load_model
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import pickle
from keras import backend as K
import tensorflow as tf
import skimage.io as skio
import skimage.color as skc
import skimage.morphology as skmor
import skimage.filters as skf
from skimage.measure import compare_ssim as ssim
from osgeo import gdal
import scipy.ndimage as spn
import cv2


"""
Notes:
- tried SVM with linear, gaussian, sigmoid and polynomial kernels. Linear worked the best
- normalize features
- regularization
"""
CALI_MASK = "california_mask.png"

def main():
    executeModel()
    # input_filename = "2014_188_stacked.tif"
    # output_filename = "fireprob.tif"
    # predict(input_filename, output_filename)
    
def predict(in_filename, out_filename):
    # img = skio.imread(in_filename)
    # res = predictImg(img)
    # with open('img', 'wb') as file_write:
    #     pickle.dump(res, file_write)

    with open('img', 'rb') as file_read:
        res = pickle.load(file_read)

    res = processPredictedImage(res)
    outputPredictedImage(in_filename, out_filename, res)

def processPredictedImage(img):
    mask = skc.rgb2gray(skio.imread(CALI_MASK)) > 0
    strel = np.ones((2,2))
    img = skmor.closing(img, strel)
    img = cv2.GaussianBlur(img,(13,13),0)
    # img[img == 0] = 30
    img[mask] = 0
    return img

def buildDataset(filename='data-181129.txt'):
    """
    Reads in a space separated file and turns this into a pandas dataframe that has been shuffled
    and processed to remove dead pixels. 
    """
    col_names = ["red", "nir", "green", "blue", "swir1", "swir2", "swir3", "category"]
    df = pd.read_csv(filename, names=col_names, delim_whitespace=True)
    
    category = df["category"]
    df = df.drop(columns=["category"])
    df = df[(df != -28672).all(1)]
    
    indices = col_names[:-1]
    for i in indices: df[i] = df[i] + 100

    df = df.multiply(0.0001)
    df["ndvi"] = (df["nir"] - df["red"])/(df["nir"] + df["red"])
    df["evi"] = (2.5 * (df["nir"] - df["red"])) / (df["nir"] + (6.0 * df["red"]) - (7.5 * df["blue"]) + 1.0 ) 
    df["ndwi"] = (df["green"] - df["nir"])/(df["green"] + df["nir"])
    df["ndii6"] = (df["nir"] - df["swir1"])/(df["nir"] + df["swir1"])
    df["ndii7"] = (df["nir"] - df["swir2"])/(df["nir"] + df["swir2"])
    df["grvi"] = (df["red"] - df["green"])/(df["red"] + df["green"])
    df["floodidx"] = (df["red"] - df["swir2"])/(df["red"] + df["swir2"])

    df["category"] = category
    df = df.sample(frac=1)
    df = df.dropna()
    return df

def executeModel():
    df = buildDataset()
    print(df.head())
    y = df["category"]
    X = df.drop(columns=["category"])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.15)  
    
    runNeuralNet(X_train, y_train, X_test, y_test)

def runNeuralNet(X, y, X_test, y_test):
    model = Sequential()

    model.add(Dense(14, input_dim=14, activation='relu'))
    model.add(Dense(14, activation='relu'))
    model.add(Dense(14, activation='relu'))
    model.add(Dense(14, activation='relu'))
    model.add(Dense(14, activation='relu'))
    model.add(Dense(7, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])
    history = model.fit(X, y, epochs=150, validation_split=0.2, batch_size=10)
    
    predictions = model.predict(X_test)
    rounded = [round(x[0]) for x in predictions]
    report = metrics.classification_report(y_test, rounded)
    print(report)
    model.save('nn_model.h5')

    plt.rcParams['font.family'] = 'serif'
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rc('font', family='serif')
    plt.rc('xtick', labelsize='x-small')
    plt.rc('ytick', labelsize='x-small')
    
    fig = plt.figure(figsize=(6, 4))
    plt.plot(history.history['loss'], color='k', ls='solid', label='Training')
    plt.plot(history.history['val_loss'], color='0.50', ls='dashed', label='Validation')
    plt.title('Model loss as a function of number of epochs')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Training', 'Validation'], loc='upper left')
    plt.savefig('loss.png', dpi=300, bbox_inches='tight')

    fig = plt.figure(figsize=(6, 4))
    plt.plot(history.history['acc'], color='k', ls='solid', label='Training')
    plt.plot(history.history['val_acc'], color='0.50', ls='dashed', label='Validation')
    plt.title('Model accuracy as a function of number of epochs')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Training', 'Validation'], loc='upper left')
    plt.savefig('acc.png', dpi=300, bbox_inches='tight')

def runSVM(X_train, X_test, y_train, y_test):
    svclassifier = svm.SVC(kernel='linear')
    svclassifier.fit(X_train, y_train)

    predictions = svclassifier.predict(X_test)
    report = metrics.classification_report(y_test, predictions)
    print(report)

def predictImg(img):
    model = load_model('nn_model.h5')

    rows, cols, bands = img.shape
    nn_shape = (rows*cols, bands)
    mod_img = img.flatten().reshape(nn_shape) + 100
    mod_img[mod_img[:] < 0] = 0

    mod_img = produceAdditionalBands(mod_img, nn_shape)
    predictions = model.predict(mod_img)

    res_img = predictions.reshape((rows, cols))
    res_img *= 255
    res_img = res_img.astype(np.uint8)

    return res_img
    
def outputPredictedImage(inputFilename, outputFilename, outputImage, rows = 4800, cols = 4800):
    driver = gdal.GetDriverByName("GTiff")
    outdata = driver.Create(outputFilename, rows, cols, 1, gdal.GDT_Byte)
    base = gdal.Open(inputFilename)
    outdata.SetGeoTransform(base.GetGeoTransform())
    outdata.SetProjection(base.GetProjection())
    outdata.GetRasterBand(1).WriteArray(outputImage)
    outdata = None
    base = None

def produceAdditionalBands(mod_img, dimensions):
    indices = np.zeros((dimensions[0], 7))
    indices[:,0] = (mod_img[:,1] - mod_img[:,0])/(mod_img[:,1] + mod_img[:,0]) 
    indices[:,1] = (2.5 * (mod_img[:,1] - mod_img[:,0])) / (mod_img[:,1] + (6.0 * mod_img[:,0]) - (7.5 * mod_img[:,3]) + 1.0 )
    indices[:,2] = (mod_img[:,2] - mod_img[:,1])/(mod_img[:,2] + mod_img[:,1])
    indices[:,3] = (mod_img[:,1] - mod_img[:,4])/(mod_img[:,1] + mod_img[:,4]) 
    indices[:,4] = (mod_img[:,1] - mod_img[:,5])/(mod_img[:,1] + mod_img[:,5]) 
    indices[:,5] = (mod_img[:,0] - mod_img[:,2])/(mod_img[:,0] + mod_img[:,2]) 
    indices[:,6] = (mod_img[:,0] - mod_img[:,5])/(mod_img[:,0] + mod_img[:,5])
    mod_img = np.hstack((mod_img, indices))
    return mod_img

main()

