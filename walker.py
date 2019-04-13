#!/usr/bin/env python3

# -*- codong: utf-8 -*-


import os
import json_processor as jp


SRC_PATH = 'journals'


for root, subdirs, files in os.walk(SRC_PATH):

    for file in files:
        if file.endswith(".json"):
            existing_json_file = os.path.join(root, file)
            # json_splitted_abs_path = existing_json_file.split(os.sep)
            jp.process_json(existing_json_file)

