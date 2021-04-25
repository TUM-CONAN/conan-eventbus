from conans import ConanFile, CMake, tools
import os


class EventbusConan(ConanFile):
    name = "eventbus"
    version = "3.0.0"
    generators = "cmake"
    settings = {"os": None, "arch": ["x86_64", "x86"], "compiler": None, "build_type": None}

    options = {"shared": [True, False]}
    default_options = "shared=True"
    exports_sources = "include*", "src*", "cmake*", "CMakeLists.txt"

    exports = ["CMakeLists.txt"]

    license = "Licensed under the Apache License, Version 2.0"
    description = "Simple and very fast event bus."

    scm = {
        "type": "git",
        "subfolder": "sources",
        "url": "https://github.com/ulricheck/EventBus.git",
        "revision": "v%s" % version,
    }

    def _cmake_configure(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.definitions["ENABLE_TEST"] = "OFF"
        cmake.configure()
        return cmake
    
    def build(self):
        #disable building usecases
        tools.replace_in_file(os.path.join("sources", "CMakeLists.txt"),
            """add_subdirectory(use_case/)""",
            """#add_subdirectory(use_case/)""")

        cmake = self._cmake_configure()
        cmake.build()

    def package(self):
        cmake = self._cmake_configure()
        cmake.install()
        
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)