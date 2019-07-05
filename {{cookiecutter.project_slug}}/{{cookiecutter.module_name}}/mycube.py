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

from floe.api import BooleanParameter, ComputeCube
from orionplatform.mixins import RecordPortsMixin


class MyCube(RecordPortsMixin, ComputeCube):
    # Cube documentation.  This documentation for this cube, and all other cubes in this repository, can be converted
    # to html by calling 'invoke docs' from the root directory of this repository.  This documentation will also
    # appear in the Orion Floe editor.
    title = "My Fancy Cube"
    classification = [["Examples"]]
    tags = ["Example", "I didn't edit the tags"]
    description = "A cube that passes records to the success or failure port depending on the switch parameter"

    # The first variable passed to a parameter must always be the variable the parameter is assigned to as a string.
    switch = BooleanParameter(
        "switch",
        required=True,
        title="Switch",
        description="If true records are sent to the success, otherwise they are send to "
        "the failure port.",
    )

    # Uncomment this and implement if you need to initialize the cube
    # def begin(self):
    #     pass

    # Records are passed to this function for processing.
    def process(self, record, port):
        if self.args.switch:
            self.success.emit(record)
        else:
            self.failure.emit(record)

    # Uncomment this and implement to cleanup the cube at the end of the run
    # def end(self):
    #     pass
