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
        # Copy license
        self.copy(pattern="COPYING", dst="licenses", src=self.source_subfolder)

        # Copy libraries
        if self.settings.os == "Windows":
            if self.options.shared:
                self.copy(pattern="*.dll", dst="bin", src=".", keep_path=False)
                self.copy(pattern="*plibsys.lib", dst="lib", src=".", keep_path=False)
                self.copy(pattern="*plibsys.lib", dst="lib", src=".", keep_path=False)
                self.copy(pattern="*plibsys.dll.a", dst="lib", src=".", keep_path=False)
            else:
                self.copy(pattern="libplibsysstatic.a", dst="lib", src=".", keep_path=False)
                self.copy(pattern="plibsysstatic.lib", dst="lib", src=".", keep_path=False)
        else:
            if self.options.shared:
                if self.settings.os == "Macos":
                    self.copy(pattern="*.dylib", dst="lib", src=".", keep_path=False)
                else:
                    self.copy(pattern="*.so*", dst="lib", src=".", keep_path=False)
            else:
                self.copy(pattern="*.a", dst="lib", src=".", keep_path=False)

        # Copy headers
        self.copy(pattern="*.h", dst="include", src=self.source_subfolder, keep_path=False)
        self.copy(pattern="*.h", dst="include", src=".", keep_path=False)

    def package_info(self):
        if self.options.shared:
            self.cpp_info.libs = ['plibsys']
        else:
            self.cpp_info.libs = ['plibsysstatic']

        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
            self.cpp_info.libs.append("rt")
            self.cpp_info.libs.append("dl")
        elif self.settings.os == "Windows":
            self.cpp_info.libs.append("ws2_32")

        self.cpp_info.includedirs.append("include")

