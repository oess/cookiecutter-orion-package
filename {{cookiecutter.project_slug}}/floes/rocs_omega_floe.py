from floe.api import WorkFloe
from cuberecord import (DataSetReaderCube, DataSetWriterCube)
from {{cookiecutter.module_name}} import MyOmegaCube, MyRocsCube


# Declare and document floe
my_floe = WorkFloe('my_floe')
my_floe.title = "My Floe"
my_floe.description = "Floe that passes records through unchanged"
my_floe.classification = [["Examples"]]
my_floe.tags = ["Examples", "I didn't edit the tags"]

# Declare Cubes
input_cube = DataSetReaderCube('input_cube')
query_input_cube = DataSetReaderCube('query_input_cube')
my_omega_cube = MyOmegaCube('my_omega_cube')
my_rocs_cube = MyRocsCube('my_rocs_cube')
output_cube = DataSetWriterCube('output_cube')

# Add cubes to floe
my_floe.add_cube(input_cube)
my_floe.add_cube(query_input_cube)
my_floe.add_cube(my_omega_cube)
my_floe.add_cube(my_rocs_cube)
my_floe.add_cube(output_cube)

# Connect the cubes
input_cube.success.connect(my_omega_cube.intake)
my_omega_cube.success.connect(my_rocs_cube.intake)
query_input_cube.success.connect(my_rocs_cube.init)
my_rocs_cube.success.connect(output_cube.intake)

# Promote parameters
input_cube.promote_parameter('data_in', promoted_name='in', title='Input data set of records')
query_input_cube.promote_parameter('data_in', promoted_name='query', title="Query data set")
output_cube.promote_parameter('data_out', promoted_name='out', title='Output File of Molecules')

if __name__ == "__main__":
    my_floe.run()
