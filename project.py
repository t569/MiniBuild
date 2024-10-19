# This file is the final bridge between the building and linking machines
# The general work flow is to pass in a linkconfig and buildconfig file with project name
# It then creates sub_objects that handle these individual steps and talk to each other
import typing
import build
import linker
import os
class Project:

    def __init__(self, build_config: typing.Union[str, None], linker_config: typing.Union[str, None] = None, project_name="default"):
        # you HAVE to have a build config

        self.build_machine = build.BuildMachine.use_config(build_config)

        if linker_config is not None:
            self.linker_machine = linker.LinkerMachine(linker_config)


        # make sure that the source_dir being used by both is being prefixed by the project name
        os.makedirs(project_name)
        self.project_source = project_name


    def build_project(self, executeFlag=False):
        pass

    # define the subclasses for linker and builder