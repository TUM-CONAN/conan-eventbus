from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout, CMakeDeps
from conan.tools.scm import Git
from conan.tools.files import load, update_conandata, copy, replace_in_file, collect_libs
import os


class EventbusConan(ConanFile):
    name = "eventbus"
    version = "3.0.0-r2"
    license = "Licensed under the Apache License, Version 2.0"
    description = "Simple and very fast event bus."

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
    }
    default_options = {
        "shared": True,
    }

    def export(self):
        update_conandata(self, {"sources": {
            "commit": "v{}".format(self.version),
            "url": "https://github.com/TUM-CAMP-NARVIS/EventBus"
        }})

    def source(self):
        git = Git(self)
        sources = self.conan_data["sources"]
        git.clone(url=sources["url"], target=self.source_folder)
        git.checkout(commit=sources["commit"])

    def generate(self):
        tc = CMakeToolchain(self)

        def add_cmake_option(option, value):
            var_name = "{}".format(option).upper()
            value_str = "{}".format(value)
            var_value = "ON" if value_str == 'True' else "OFF" if value_str == 'False' else value_str
            tc.variables[var_name] = var_value

        for option, value in self.options.items():
            add_cmake_option(option, value)

        tc.cache_variables["ENABLE_TEST"] = False

        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def layout(self):
        cmake_layout(self, src_folder="source_folder")

    def build(self):
        replace_in_file(self, os.path.join(self.source_folder, "CMakeLists.txt"),
                        """add_subdirectory(use_case)""",
                        """#add_subdirectory(use_case)""")

        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, pattern="BOOST_1_0", dst="licenses", src=self.source_folder)
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = collect_libs(self)
