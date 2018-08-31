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

import os
from orionclient.session import OrionSession
from artemis.wrappers import WorkFloeWrapper, DatasetWrapper, OutputDatasetWrapper
from artemis.test import FloeTestCase
from artemis.decorators import package
import pytest

from openeye.oechem import oeifstream
from datarecord import read_mol_record

import {{cookiecutter.module_name}}

PACKAGE_DIR = os.path.dirname(os.path.dirname({{cookiecutter.module_name}}.__file__))

FILE_DIR = os.path.join(PACKAGE_DIR, "tests", "test_data")
FLOES_DIR = os.path.join(PACKAGE_DIR, "floes")

session = OrionSession()


@pytest.mark.floetest
@package(PACKAGE_DIR)
class TestReadWriteFloe(FloeTestCase):

    def test_simple_run(self):
        workfloe = WorkFloeWrapper.get_workfloe(
            os.path.join(FLOES_DIR, "myfloe.py"),
            run_timeout=1200
        )
        input_file = DatasetWrapper.get_dataset(os.path.join(FILE_DIR, "10.ism"))
        output_file = OutputDatasetWrapper(extension=".oedb")
        workfloe.start(
            {
                "promoted": {
                    "in": input_file.identifier,
                    "out": output_file.identifier,
                    "switch": True,
                }
            }
        )
        # Faked locally
        self.assertEqual(workfloe.state, "complete")
        # Also faked
        self.assertEqual(
            len(workfloe.reason),
            0,
            "Failed with reason {}".format(workfloe.reason)
        )

        ifs = oeifstream()
        self.assertTrue(ifs.open(output_file.path))
        records = []
        while True:
            record = read_mol_record(ifs)
            if record is None:
                break
            records.append(record)
        ifs.close()
        count = len(records)
        self.assertEqual(count, 10)