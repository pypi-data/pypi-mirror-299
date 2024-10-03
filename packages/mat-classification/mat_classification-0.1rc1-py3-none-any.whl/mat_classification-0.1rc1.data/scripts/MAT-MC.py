#!python
# -*- coding: utf-8 -*-
'''
MAT-Tools: Python Framework for Multiple Aspect Trajectory Data Mining

The present package offers a tool, to support the user in the task of data analysis of multiple aspect trajectories. It integrates into a unique framework for multiple aspects trajectories and in general for multidimensional sequence data mining methods.
Copyright (C) 2022, MIT license (this portion of code is subject to licensing from source project distribution)

Created on Dec, 2021
Copyright (C) 2022, License GPL Version 3 or superior (see LICENSE file)

@author: Tarlis Portela
'''
import os
#import sys, os  # TODO TEMP FOR TESTING
#sys.path.insert(0, os.path.abspath('.'))

import os
import argparse

from matclassification.methods import *
    
def parse_args():
    parse = argparse.ArgumentParser(
        description="""MAT Movelets Classification:
    This script runs classifiers for movelets input.
    
    Available classifiers are:
    - MMLP: Movelet Multi-layer Perceptron (standard)
    - MRF: Movelet Random forrest
    - MSVC: Movelet Support Vector Machine
    - MDT: Movelet Decision Tree
    - MRFHP: Movelet Random Forrest with Hiperparam Serch
    
    Example Usage:
        MAT-MC.py 'sample/results/hiper' -c 'MMLP,MSVC'
    """, formatter_class=argparse.RawTextHelpFormatter)
    parse.add_argument('results-path', type=str, help='path for the results folder')
#    parse.add_argument('folder', type=str, help='dataset name')
    parse.add_argument('-c', '--classifiers', type=str, default='MMLP,MRF,MSVC', help='classifiers methods')
    parse.add_argument('-mf', '--modelfolder', type=str, default='.', help='model folder')
    
    parse.add_argument('-r', '--random', type=int, default=1, help='random seed')

    args = parse.parse_args()
    config = vars(args)
    return config
 
config = parse_args()
#print(config)

res_path  = config["results-path"]
#folder    = config["folder"]

modelfolder  = config["modelfolder"]
random_seed  = config["random"] # TODO

classifiers  = config["classifiers"].split(',')

# ------------------------------------------------------------------------------------
def callmodel(method, train, test):    
    model = eval(method)(random_state=random_seed)
    
    model.prepare_input(train, test) # TODO Grid encoding
    model.train()
    model.test()
    ## We can visualize the training report (the same on most models):
    print(model.summary())
    
    # Saving results
    model.save(res_path, modelfolder)
# ------------------------------------------------------------------------------------
import pandas as pd
train = pd.read_csv(os.path.join(res_path, 'train.csv'))
test = pd.read_csv(os.path.join(res_path, 'test.csv'))

for method in classifiers:
    callmodel(method, train, test)