# (C) 2018 OpenEye Scientific Software Inc. All rights reserved.
#
# TERMS FOR USE OF SAMPLE CODE The software below ("Sample Code") is
# provided to current licensees or subscribers of OpenEye products or
# SaaS offerings (each a "Customer").
# Customer is hereby permitted to use, copy, and modify the Sample Code,
# subject to these terms. OpenEye claims no rights to Customer's
# modifications. Modification of Sample Code is at Customer's sole and
# exclusive risk. Sample Code may require Customer to have a then
# current license or subscription to the applicable OpenEye offering.
# THE SAMPLE CODE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED.  OPENEYE DISCLAIMS ALL WARRANTIES, INCLUDING, BUT
# NOT LIMITED TO, WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. In no event shall OpenEye be
# liable for any damages or liability in connection with the Sample Code
# or its use.

from floe.api import WorkFloe
from cuberecord import (DataSetReaderCube, DataSetWriterCube)
from {{cookiecutter.module_name}} import MyCube


# Declare and document floe
my_floe = WorkFloe('my_floe')
my_floe.title = "My Floe"
my_floe.description = "Floe that passes records through unchanged"
my_floe.classification = [["Examples"]]
my_floe.tags = ["Examples", "I didn't edit the tags"]

# Declare Cubes
input_cube = DataSetReaderCube('input_cube')
my_cube = MyCube('my_cube')
output_cube = DataSetWriterCube('output_cube')

# Add cubes to floe
my_floe.add_cube(input_cube)
my_floe.add_cube(my_cube)
my_floe.add_cube(output_cube)

# Connect the cubes
input_cube.success.connect(my_cube.intake)
my_cube.success.connect(output_cube.intake)

# Promote parameters
input_cube.promote_parameter('data_in', promoted_name='in', title='Input data set of records')
output_cube.promote_parameter('data_out', promoted_name='out', title='Output File of Molecules')

if __name__ == "__main__":
    my_floe.run()