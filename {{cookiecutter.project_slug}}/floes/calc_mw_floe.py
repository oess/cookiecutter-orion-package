from floe.api import WorkFloe
from cuberecord import (DataSetReaderCube, DataSetWriterCube)
from {{cookiecutter.module_name}} import MWCube


# Declare and document floe
my_floe = WorkFloe('my_mw_floe')
my_floe.title = "My MW Floe"
my_floe.description = "Compute Molecular Weight Floe"
my_floe.classification = [["Examples"]]
my_floe.tags = ["Examples", "Molecules", "Properties"]

# Declare Cubes
input_cube = DataSetReaderCube('input_cube')
mw_cube = MWCube('mw_cube')
output_cube = DataSetWriterCube('output_cube')

# Add cubes to floe
my_floe.add_cube(input_cube)
my_floe.add_cube(mw_cube)
my_floe.add_cube(output_cube)

# Connect the cubes
input_cube.success.connect(mw_cube.intake)
mw_cube.success.connect(output_cube.intake)

# Promote parameters
input_cube.promote_parameter('data_in', promoted_name='in', title='Input data set of records')
output_cube.promote_parameter('data_out', promoted_name='out', title='Output File of Molecules')

if __name__ == "__main__":
    my_floe.run()