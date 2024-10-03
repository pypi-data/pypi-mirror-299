#==============================================================================#
#  Author:       Dominik Müller                                                #
#  Copyright:    2024 IT-Infrastructure for Translational Medical Research,    #
#                University of Augsburg                                        #
#                                                                              #
#  This program is free software: you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by        #
#  the Free Software Foundation, either version 3 of the License, or           #
#  (at your option) any later version.                                         #
#                                                                              #
#  This program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
#==============================================================================#
#-----------------------------------------------------#
#                   Library imports                   #
#-----------------------------------------------------#
#External libraries
import unittest
import numpy as np
import pandas as pd
import tempfile
from PIL import Image
import json
import os
#Internal libraries
from aucmedi.data_processing.io_interfaces import *

#-----------------------------------------------------#
#               Unittest: IO Interfaces               #
#-----------------------------------------------------#
class IOinterfacesTEST(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        np.random.seed(1234)
        self.aif = ["png"]

    #-------------------------------------------------#
    #              Directory IO Interface             #
    #-------------------------------------------------#
    def test_Directory_testing(self):
        # Create imaging data
        tmp_data = tempfile.TemporaryDirectory(prefix="tmp.aucmedi.",
                                               suffix=".data")
        for i in range(0, 25):
            img = np.random.rand(16, 16, 3) * 255
            img_pillow = Image.fromarray(img.astype(np.uint8))
            index = "image.sample_" + str(i) + ".png"
            path_sample = os.path.join(tmp_data.name, index)
            img_pillow.save(path_sample)
        # Run Directory IO
        ds = directory_loader(tmp_data.name, self.aif, training=False)
        self.assertTrue(len(ds[0]), 25)

    def test_Directory_training(self):
        # Create imaging data with subdirectories
        tmp_data = tempfile.TemporaryDirectory(prefix="tmp.aucmedi.",
                                               suffix=".data")
        for i in range(0, 5):
            os.mkdir(os.path.join(tmp_data.name, "class_" + str(i)))
        # Fill subdirectories with images
        for i in range(0, 25):
            img = np.random.rand(16, 16, 3) * 255
            img_pillow = Image.fromarray(img.astype(np.uint8))
            index = "image.sample_" + str(i) + ".png"
            label_dir = "class_" + str((i % 5))
            path_sample = os.path.join(tmp_data.name, label_dir, index)
            img_pillow.save(path_sample)
        # Run Directory IO
        ds = directory_loader(tmp_data.name, self.aif, training=True)
        self.assertTrue(len(ds[0]), 25)
        self.assertTrue(len(ds[1]), 25)

    #-------------------------------------------------#
    #                JSON IO Interface                #
    #-------------------------------------------------#
    def test_JSON_testing(self):
        # Create imaging data
        tmp_data = tempfile.TemporaryDirectory(prefix="tmp.aucmedi.",
                                               suffix=".data")
        data = {}
        for i in range(0, 25):
            img = np.random.rand(16, 16, 3) * 255
            img_pillow = Image.fromarray(img.astype(np.uint8))
            index = "image.sample_" + str(i) + ".png"
            data[index[:-4]] = 0
            path_sample = os.path.join(tmp_data.name, index)
            img_pillow.save(path_sample)
        # Create JSON data
        tmp_json = tempfile.NamedTemporaryFile(mode="w", prefix="tmp.aucmedi.",
                                               suffix=".json")
        json.dump(data, tmp_json)
        tmp_json.flush()
        # Run JSON IO
        ds = json_loader(path_data=tmp_json.name, path_imagedir=tmp_data.name,
                         allowed_image_formats=self.aif, training=False)
        self.assertTrue(len(ds[0]), 25)

    def test_JSON_training_woOHE(self):
        # Create imaging data with subdirectories
        tmp_data = tempfile.TemporaryDirectory(prefix="tmp.aucmedi.",
                                               suffix=".data")
        data = {}
        for i in range(0, 25):
            img = np.random.rand(16, 16, 3) * 255
            img_pillow = Image.fromarray(img.astype(np.uint8))
            index = "image.sample_" + str(i) + ".png"
            data[index[:-4]] = np.random.randint(5)
            path_sample = os.path.join(tmp_data.name, index)
            img_pillow.save(path_sample)
        # Create JSON data
        tmp_json = tempfile.NamedTemporaryFile(mode="w", prefix="tmp.aucmedi.",
                                               suffix=".json")
        json.dump(data, tmp_json)
        tmp_json.flush()
        # Run JSON IO
        ds = json_loader(path_data=tmp_json.name, path_imagedir=tmp_data.name,
                         allowed_image_formats=self.aif, training=True,
                         ohe=False)
        self.assertTrue(len(ds[0]), 25)
        self.assertTrue(len(ds[1]), 25)

    def test_JSON_training_withOHE(self):
        # Create imaging data with subdirectories
        tmp_data = tempfile.TemporaryDirectory(prefix="tmp.aucmedi.",
                                               suffix=".data")
        data = {}
        for i in range(0, 25):
            img = np.random.rand(16, 16, 3) * 255
            img_pillow = Image.fromarray(img.astype(np.uint8))
            index = "image.sample_" + str(i) + ".png"
            labels_ohe = [0, 0, 0, 0]
            class_index = np.random.randint(0, 4)
            labels_ohe[class_index] = 1
            data[index[:-4]] = labels_ohe
            path_sample = os.path.join(tmp_data.name, index)
            img_pillow.save(path_sample)
        # Create JSON data
        tmp_json = tempfile.NamedTemporaryFile(mode="w", prefix="tmp.aucmedi.",
                                               suffix=".json")
        json.dump(data, tmp_json)
        tmp_json.flush()
        # Run JSON IO
        ds = json_loader(path_data=tmp_json.name, path_imagedir=tmp_data.name,
                         allowed_image_formats=self.aif, training=True,
                         ohe=True)
        self.assertTrue(len(ds[0]), 25)
        self.assertTrue(len(ds[1]), 25)

    #-------------------------------------------------#
    #                 CSV IO Interface                #
    #-------------------------------------------------#
    def test_CSV_testing(self):
        # Create imaging data
        tmp_data = tempfile.TemporaryDirectory(prefix="tmp.aucmedi.",
                                               suffix=".data")
        data = {}
        for i in range(0, 25):
            img = np.random.rand(16, 16, 3) * 255
            img_pillow = Image.fromarray(img.astype(np.uint8))
            index = "image.sample_" + str(i) + ".png"
            data[index[:-4]] = 0
            path_sample = os.path.join(tmp_data.name, index)
            img_pillow.save(path_sample)
        # Create CSV data
        tmp_csv = tempfile.NamedTemporaryFile(mode="w", prefix="tmp.aucmedi.",
                                              suffix=".csv")
        df = pd.DataFrame.from_dict(data, orient="index", columns=["class"])
        df.index.name = "index"
        df.to_csv(tmp_csv.name, index=True, header=True)

        # Run CSV IO
        ds = csv_loader(path_data=tmp_csv.name, path_imagedir=tmp_data.name,
                        allowed_image_formats=self.aif, training=False,
                        col_sample="index")
        self.assertTrue(len(ds[0]), 25)

    def test_CSV_training_woOHE(self):
        # Create imaging data with subdirectories
        tmp_data = tempfile.TemporaryDirectory(prefix="tmp.aucmedi.",
                                               suffix=".data")
        data = {}
        for i in range(0, 25):
            img = np.random.rand(16, 16, 3) * 255
            img_pillow = Image.fromarray(img.astype(np.uint8))
            index = "image.sample_" + str(i) + ".png"
            data[index[:-4]] = np.random.randint(5)
            path_sample = os.path.join(tmp_data.name, index)
            img_pillow.save(path_sample)
        # Create CSV data
        tmp_csv = tempfile.NamedTemporaryFile(mode="w", prefix="tmp.aucmedi.",
                                              suffix=".csv")
        df = pd.DataFrame.from_dict(data, orient="index", columns=["class"])
        df.index.name = "index"
        df.to_csv(tmp_csv.name, index=True, header=True)

        # Run CSV IO
        ds = csv_loader(path_data=tmp_csv.name, path_imagedir=tmp_data.name,
                        allowed_image_formats=self.aif, training=True,
                        ohe=False, col_sample="index", col_class="class")
        self.assertTrue(len(ds[0]), 25)
        self.assertTrue(len(ds[1]), 25)

    def test_CSV_training_withOHE(self):
        # Create imaging data with subdirectories
        tmp_data = tempfile.TemporaryDirectory(prefix="tmp.aucmedi.",
                                               suffix=".data")
        data = {}
        for i in range(0, 25):
            img = np.random.rand(16, 16, 3) * 255
            img_pillow = Image.fromarray(img.astype(np.uint8))
            index = "image.sample_" + str(i) + ".png"
            labels_ohe = [0, 0, 0, 0]
            class_index = np.random.randint(0, 4)
            labels_ohe[class_index] = 1
            data[index[:-4]] = labels_ohe
            path_sample = os.path.join(tmp_data.name, index)
            img_pillow.save(path_sample)
        # Create CSV data
        tmp_csv = tempfile.NamedTemporaryFile(mode="w", prefix="tmp.aucmedi.",
                                              suffix=".csv")
        df = pd.DataFrame.from_dict(data, orient="index",
                                    columns=["a", "b", "c", "d"])
        df.index.name = "index"
        df.to_csv(tmp_csv.name, index=True, header=True)

        # Run CSV IO
        ds = csv_loader(path_data=tmp_csv.name, path_imagedir=tmp_data.name,
                        allowed_image_formats=self.aif, training=True,
                        ohe=True, col_sample="index")
        self.assertTrue(len(ds[0]), 25)
        self.assertTrue(len(ds[1]), 25)
