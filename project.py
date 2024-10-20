# This file is the final bridge between the building and linking machines
# The general work flow is to pass in a linkconfig and buildconfig file with project name
# It then creates sub_objects that handle these individual steps and talk to each other
import typing
import build
import linker
import os
from utils.executefiles import execute_and_dump, execute

class Project:

    def __init__(self, build_config: typing.Union[str, None], linker_config: typing.Union[str, None] = None,
                 project_name="default"):
        # you HAVE to have a build config

        # define the subclasses for linker and builder
        self.build_machine = build.BuildMachine.use_config(build_config)

        if linker_config is not None:
            self.linker_machine = linker.LinkerMachine(linker_config)

        # make sure that the source_dir being used by both is being prefixed by the project name
        # also create the dir if it doesn't exist

        self.project_source = project_name
        self.build_machine.source_dir = self.project_source + self.build_machine.source_dir  # note for the linking,
        # the project name is passed into link_dir_to_exec
        self.build_machine.output_dir = self.project_source + self.build_machine.output_dir
        self.build_machine.output_dir_objectfiles = self.project_source + self.build_machine.output_dir_objectfiles
        self.build_machine.output_dir_executables = self.project_source + self.build_machine.output_dir_executables
        self.linker_machine.source_dir = self.project_source + self.linker_machine.source_dir
        self.linker_machine.out_dir = self.project_source + self.linker_machine.out_dir

        os.makedirs(self.build_machine.source_dir, exist_ok=True)
        os.makedirs(self.build_machine.output_dir, exist_ok=True)

        os.makedirs(self.build_machine.output_dir_executables, exist_ok=True)
        os.makedirs(self.build_machine.output_dir_objectfiles, exist_ok=True)

        os.makedirs(self.linker_machine.source_dir, exist_ok=True)

    def compile_to_object_files(self):
        self.build_machine.compile_to_obj_and_dump()

    def link_to_executable(self):
        self.linker_machine.link_dir_to_exec(project_name=self.project_source)

    def run_executable(self, extra_args=None, log_the_results=False):
        if log_the_results:
            execute_and_dump(self.linker_machine.results, self.linker_machine.output_binary)

        else:
            execute(self.build_machine.os_type, self.linker_machine.output_binary, extra_args=extra_args)


my_prj = Project('buildconfig.json', 'linkerconfig.json')
my_prj.compile_to_object_files()
my_prj.link_to_executable()
# my_prj.run_executable(log_the_results=True)
