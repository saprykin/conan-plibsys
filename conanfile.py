#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class PlibsysConan(ConanFile):
    name = "plibsys"
    version = "0.0.3"
    url = "https://github.com/saprykin/conan-plibsys"
    homepage = "https://github.com/saprykin/plibsys"
    description = "Highly portable C system library"
    license = "LGPL-2.1"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    source_subfolder = "source_subfolder"

    def source(self):
        source_url = "https://github.com/saprykin/plibsys"
        tools.get("{0}/archive/{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["PLIBSYS_TESTS"] = False 
        cmake.definitions["PLIBSYS_BUILD_STATIC"] = not self.options.shared
        cmake.definitions["PLIBSYS_COVERAGE"] = False 
        cmake.configure()
        return cmake
    
    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        self.copy(pattern="COPYING", dst="licenses", src=self.source_subfolder)

    def package_info(self):
        if self.options.shared:
            self.cpp_info.libs = ['plibsys']
        else:
            self.cpp_info.libs = ['plibsysstatic']

        self.cpp_info.includedirs.append(os.path.join('include', 'plibsys'))
        
