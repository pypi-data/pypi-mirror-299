# -*- coding: utf-8 -*-
"""
MAT-Tools: Python Framework for Multiple Aspect Trajectory Data Mining

The present application offers a tool, to support the user in the preprocessing of multiple aspect trajectory data. It integrates into a unique framework for multiple aspects trajectories and in general for multidimensional sequence data mining methods.
Copyright (C) 2022, MIT license (this portion of code is subject to licensing from source project distribution)

Created on Dec, 2023
Copyright (C) 2023, License GPL Version 3 or superior (see LICENSE file)

Authors:
    - Tarlis Portela
"""
import glob2 as glob

from matdata.util.parsers import json2movelet

def read_all_movelets(path_name, name='movelets'):
    count = 0
    path_to_file = glob.glob(os.path.join(path_name, '**', 'moveletsOnTrain.json'), recursive=True)

    movelets = []
    for file_name in path_to_file:
        aux_mov = read_movelets(file_name, name, count)
        movelets = movelets + aux_mov
        count = len(movelets)

    return movelets
    
def read_movelets(file_name, name='movelets', count=0):
    with open(file_name) as f:
        return json2movelet(f, name, count)
    return []