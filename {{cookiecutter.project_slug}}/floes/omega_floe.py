from floe.api import WorkFloe
from cuberecord import (DataSetReaderCube, DataSetWriterCube)
from {{cookiecutter.module_name}} import MyOmegaCube


# Declare and document floe
my_floe = WorkFloe('my_omega_floe')
my_floe.title = "My Omega Floe"
my_floe.description = "Floe that passes records through unchanged"
my_floe.classification = [["Examples"]]
my_floe.tags = ["Examples", "I didn't edit the tags"]

# Declare Cubes
input_cube = DataSetReaderCube('input_cube')
my_cube = MyOmegaCube('my_cube')
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
