from cuberecord import OERecordCube


class MyCube(OERecordCube):
    # Cube documentation.
    title = "Pass Through Cube"
    classification = [["Examples"]]
    tags = ["Example", "I didn't edit the tags"]
    description = "A cube that passes records through to the success port"

    # Uncomment this and implement if you need to initialize the cube
    # def begin(self):
    #     pass

    # Records are passed to this function for processing.
    def process(self, record, port):
            self.success.emit(record)

    # Uncomment this and implement to cleanup the cube at the end of the run
    # def end(self):
    #     pass
