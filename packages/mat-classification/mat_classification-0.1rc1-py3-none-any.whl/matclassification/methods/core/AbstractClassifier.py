# -*- coding: utf-8 -*-
'''
MAT-Tools: Python Framework for Multiple Aspect Trajectory Data Mining

The present package offers a tool, to support the user in the task of data analysis of multiple aspect trajectories. It integrates into a unique framework for multiple aspects trajectories and in general for multidimensional sequence data mining methods.
Copyright (C) 2022, MIT license (this portion of code is subject to licensing from source project distribution)

Created on Dec, 2021
Copyright (C) 2022, License GPL Version 3 or superior (see LICENSE file)

Authors:
    - Tarlis Portela
'''
# --------------------------------------------------------------------------------
import os 
import numpy as np
import pandas as pd
import itertools
from numpy import argmax
from datetime import datetime

from tqdm.auto import tqdm
# --------------------------------------------------------------------------------
from tensorflow import random
from matdata.preprocess import trainTestSplit
from matclassification.methods._lib.datahandler import prepareTrajectories
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from tensorflow.keras.utils import to_categorical

from sklearn.metrics import classification_report
from matclassification.methods._lib.metrics import *
#from matclassification.methods._lib.pymove.models import metrics
# --------------------------------------------------------------------------------
import warnings
# --------------------------------------------------------------------------------
from abc import ABC, abstractmethod
# TODO implement rounds

# Replicated in matview.result:
from enum import Enum, auto
class Approach(Enum):
    NN   = auto()
    RF   = auto()
    DT   = auto()
    SVM  = auto()
    XGB  = auto()

# Simple Abstract Classifier Model
class AbstractClassifier(ABC):
    """
    Simple Abstract Classifier Model.

    This abstract class defines the core structure for a machine learning classifier model. 
    It provides common methods such as model creation, and evaluation, 
    while specific implementations of the model must be defined in derived classes by overriding 
    the `create()` method.

    Attributes:
    -----------
    name : str
        Name of the classifier implementation (default: 'NN').
    model : object
        The actual machine learning model to be defined in the subclass.
    le : object
        Label encoder (optional).
    approach : Enum
        The category of approach used (default: Approach.NN).
    isverbose : bool
        Flag to control verbosity of model's output (default: based on `verbose` parameter).
    save_results : bool
        Indicates whether to save results (default: False).
    validate : bool
        Indicates whether validation should be performed (default: False).
    config : dict
        Dictionary of configuration parameters.
        
    y_test_true : array-like
        True labels for the test dataset (available after call to predict).
    y_test_pred : array-like
        Predicted labels for the test dataset (available after call to predict).

    Parameters:
    -----------
    name : str, optional
        Classifier name (default: 'NN').
    n_jobs : int, optional
        Number of parallel jobs to run (default: -1 for using all processors).
    verbose : int, optional
        Verbosity level (default: 0).
    random_state : int, optional
        Random seed for reproducibility (default: 42).
    filterwarnings : str, optional
        Warning filter level (default: 'ignore').

    Methods:
    --------
    add_config(**kwargs):
        Updates the configuration with additional parameters.
    
    grid_search(*args):
        Defines the grid of hyperparameters to search over.
    
    duration():
        Returns the duration in milliseconds since the start of model execution.
    
    message(pbar, text):
        Logs a message if verbosity is enabled.

    labels:
        Returns the unique labels in the test data.

    create():
        Abstract method to be overridden in subclasses to define the model.
    
    clear():
        Clears the model from memory.

    fit(X_train, y_train, X_val, y_val):
        Trains the model on the training data and evaluates it on validation data.
    
    predict(X_test, y_test):
        Generates predictions on the test data and returns a performance summary.

    score(y_test, y_pred):
        Computes various evaluation metrics (accuracy, precision, recall, F1, etc.) from 
        the true and predicted labels.

    summary():
        Returns a summary of the test performance.

    cm():
        Plots the confusion matrix for the test results.

    save_model(dir_path='.', modelfolder='model', model_name=''):
        Saves the trained model to the specified directory.

    save(dir_path='.', modelfolder='model'):
        Saves the prediction, classification report, and performance metrics to files.
    """
    
    def __init__(self, 
                 name='NN',
                 
                 n_jobs=-1,
                 verbose=0,
                 random_state=42,
                 filterwarnings='ignore'):
        
        self.name = name
        self.y_test_pred = None
        self.model = None
        self.le = None
        
        # When creating new methods, choose an approach category
        self.approach = Approach.NN
        
        self.isverbose = verbose >= 0
        
        self.save_results = False # TODO
        self.validate = False
        topK = 5
        
        self.config = dict()
        self.add_config(topK=topK,
                        n_jobs=n_jobs,
                        verbose=verbose,
                        random_state=random_state)
        
        
        if filterwarnings:
            warnings.filterwarnings(filterwarnings)
        
        if self.isverbose:
            print(datetime.now())
            print('\n['+self.name+':] Building model')
    
    def add_config(self, **kwargs):
        self.config.update(kwargs)
    
    def grid_search(self, *args):
        params = []
        for arg in args:
            if not isinstance(arg, list):
                arg = [arg]
            params.append(arg)
        
        self.grid = list(itertools.product(*params))
        
    def duration(self):
        return (datetime.now()-self.start_time).total_seconds() * 1000
    
    def message(self, pbar, text):
        if isinstance(pbar, list):
            if self.isverbose:
                print(text)
        else:
            pbar.set_postfix_str(text)
    
    @property
    def labels(self):
        return dict.fromkeys(self.y_test_true).keys()
#        return set(self.y_test_true)

    @abstractmethod
    def create(self):
        
        # **** Method to overrite ****
        print('\n['+self.name+':] Warning! you must overwrite the create() method.')
        self.model = None
        
        return self.model
    
    def clear(self):
        del self.model 

    def fit(self, 
            X_train, 
            y_train, 
            X_val,
            y_val):
        
        self.model = self.create()
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_val)
        
        self.report = self.score(y_val, y_pred)
        
        return self.report
    
    def predict(self,                 
                X_test,
                y_test):
        
#        y_pred = self.model.predict_proba(X_test)
        y_pred = self.model.predict(X_test)
    
        if y_test.ndim == 2:
            y_test = argmax(y_test, axis = 1)
    
        self._summary = self.score(y_test, y_pred) #self.y_test_pred)
        
        self.y_test_true = y_test
        self.y_test_pred = argmax(y_pred , axis = 1)
        
        if self.le:
            self.y_test_true = self.le.inverse_transform(self.y_test_true)
            self.y_test_pred = self.le.inverse_transform(self.y_test_pred)
        
        return self._summary, y_pred 

    
    def score(self, y_test, y_pred):
        acc, acc_top5, _f1_macro, _prec_macro, _rec_macro, bal_acc = compute_acc_acc5_f1_prec_rec(np.array(y_test), np.array(y_pred), print_metrics=False)
        
        dic_model = {
            'accuracy': acc,
            'accuracyTopK5': acc_top5,
            'balanced_accuracy': bal_acc,
            'precision_macro': _f1_macro,
            'recall_macro': _prec_macro,
            'f1_macro': _rec_macro,
        } 
        
        return pd.DataFrame(dic_model, index=[0])

    def summary(self):
        return pd.DataFrame(self.test_report.mean()).T
    
    def cm(self): # Confusion Matrix Plot
        from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
        
        cfm = ConfusionMatrixDisplay(
            confusion_matrix = confusion_matrix(self.y_test_true, self.y_test_pred), 
            display_labels = self.labels
        )
        return cfm.plot()
        
    def save_model(self, dir_path='.', modelfolder='model', model_name=''):
        if not os.path.exists(os.path.join(dir_path, modelfolder)):
            os.makedirs(os.path.join(dir_path, modelfolder))
        
        self.model.save(os.path.join(dir_path, modelfolder, 'model_'+self.name.lower()+'_'+str(model_name)+'.h5'))
        
    def save(self, dir_path='.', modelfolder='model'):
        if not os.path.exists(os.path.join(dir_path, modelfolder)):
            os.makedirs(os.path.join(dir_path, modelfolder))

        prediction = self.prediction_report() 
        if prediction is not None:
            prediction.to_csv(os.path.join(dir_path, modelfolder, 'model_'+self.name.lower()+'_prediction.csv')) 
        
        report = self.classification_report()
        if report is not None:
            report.to_csv(os.path.join(dir_path, modelfolder, 'model_'+self.name.lower()+'_report.csv'), index = False)
            
        train_report = self.training_report()
        if train_report is not None:
            train_report.to_csv(os.path.join(dir_path, modelfolder, 'model_'+self.name.lower()+'_history.csv'))
            
        test_report = self.testing_report()
        if test_report is not None:
            test_report.to_csv(os.path.join(dir_path, modelfolder, 'model_'+self.name.lower()+'_summary.csv'))
    
    def prediction_report(self):
        df = pd.DataFrame(self.y_test_true, self.y_test_pred, columns=['true_label'])
        df.rename_axis(index='prediction', inplace=True)
        return df
    def classification_report(self):
        report = classification_report(self.y_test_true, self.y_test_pred, output_dict=True, zero_division=False)
        return classification_report_dict2df(report, self.approach.name.upper())
    def training_report(self):
        return self.report
    def testing_report(self):
        return self.test_report