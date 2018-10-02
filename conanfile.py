#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class WtConan(ConanFile):
    name = "wt"
    version = "4.0.4"
    description = "Wt is a C++ library for developing web applications"
    url = "https://github.com/bincrafters/conan-wt"
    homepage = "https://github.com/emweb/wt"
    license = "GNU GPL v2"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_ssl": [True, False],
        "with_haru": [True, False],
        "with_pango": [True, False],
        "with_sqlite": [True, False],
        "with_postgres": [True, False],
        "with_firebird": [True, False],
        "with_mysql": [True, False],
        "with_mssql": [True, False],
        "with_qt4": [True, False],
        "with_test": [True, False],
        "with_dbo": [True, False],
        "with_opengl": [True, False],
        "with_unwind": [True, False],
        "no_std_locale": [True, False],
        "no_std_wstring": [True, False],
        "multi_threaded": [True, False],
        "connector_http": [True, False],
        "connector_isapi": [True, False],
        "connector_fcgi": [True, False]
    }
    default_options = "shared=False", \
    "fPIC=True", \
    "with_ssl=True", \
    "with_haru=False", \
    "with_pango=False", \
    "with_sqlite=True", \
    "with_postgres=False", \
    "with_firebird=False", \
    "with_mysql=False", \
    "with_mssql=False", \
    "with_qt4=False", \
    "with_test=True", \
    "with_dbo=True", \
    "with_opengl=False", \
    "with_unwind=False", \
    "no_std_locale=False", \
    "no_std_wstring=False", \
    "multi_threaded=True", \
    "connector_http=True", \
    "connector_isapi=True", \
    "connector_fcgi=False"

    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    requires = (
                'cmake_findboost_modular/1.66.0@bincrafters/stable',
                'boost_algorithm/1.66.0@bincrafters/stable',
                'boost_array/1.66.0@bincrafters/stable',
                'boost_asio/1.66.0@bincrafters/stable',
                'boost_assign/1.66.0@bincrafters/stable',
                'boost_config/1.66.0@bincrafters/stable',
                'boost_bind/1.66.0@bincrafters/stable',
                'boost_filesystem/1.66.0@bincrafters/stable',
                'boost_fusion/1.66.0@bincrafters/stable',
                'boost_integer/1.66.0@bincrafters/stable',
                'boost_interprocess/1.66.0@bincrafters/stable',
                'boost_lexical_cast/1.66.0@bincrafters/stable',
                'boost_pool/1.66.0@bincrafters/stable',
                'boost_math/1.66.0@bincrafters/stable',
                'boost_multi_index/1.66.0@bincrafters/stable',
                'boost_numeric_ublas/1.66.0@bincrafters/stable',
                'boost_optional/1.66.0@bincrafters/stable',
                'boost_phoenix/1.66.0@bincrafters/stable',
                'boost_pool/1.66.0@bincrafters/stable',
                'boost_program_options/1.66.0@bincrafters/stable',
                'boost_range/1.66.0@bincrafters/stable',
                'boost_serialization/1.66.0@bincrafters/stable',
                'boost_smart_ptr/1.66.0@bincrafters/stable',
                'boost_spirit/1.66.0@bincrafters/stable',
                'boost_system/1.66.0@bincrafters/stable',
                'boost_thread/1.66.0@bincrafters/stable',
                'boost_tuple/1.66.0@bincrafters/stable',
                'boost_tokenizer/1.66.0@bincrafters/stable',
                'boost_variant/1.66.0@bincrafters/stable',
                'zlib/1.2.11@conan@stable'
               )

    def requirements(self):
        if self.options.with_ssl:
            self.requires('OpenSSL/1.0.2o@conan/stable')
        if self.options.with_sqlite:
            self.requires('sqlite3/3.21.0@bincrafters/stable')

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC
            del self.options.connector_fcgi
        else:
            del self.options.connector_isapi

    def source(self):
        source_url = "https://github.com/emweb/wt"
        tools.get("{0}/archive/{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)
        if self.settings.os == 'Windows':
            # wt relies on auto-linking of boost, which we don't use
            find_boost_cmake = os.path.join(self.source_subfolder, 'cmake', 'WtFindBoost-cmake.txt')
            tools.replace_in_file(find_boost_cmake, 'SET(BOOST_WT_LIBRARIES "")',
                                  'SET(BOOST_WT_LIBRARIES '
                                  '${Boost_THREAD_LIBRARY} '
                                  '${Boost_SYSTEM_LIBRARY} '
                                  '${Boost_FILESYSTEM_LIBRARY})')
            tools.replace_in_file(find_boost_cmake, 'SET(BOOST_WTHTTP_LIBRARIES "")',
                                  'SET(BOOST_WTHTTP_LIBRARIES '
                                  '${Boost_THREAD_LIBRARY} '
                                  '${Boost_PROGRAM_OPTIONS_LIBRARY} '
                                  '${Boost_SYSTEM_LIBRARY} '
                                  '${Boost_FILESYSTEM_LIBRARY})')

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions['SHARED_LIBS'] = self.options.shared
        cmake.definitions['BUILD_EXAMPLES'] = False
        cmake.definitions['BUILD_TESTS'] = False
        cmake.definitions['ENABLE_SSL'] = self.options.with_ssl
        cmake.definitions['ENABLE_HARU'] = self.options.with_haru
        cmake.definitions['ENABLE_PANGO'] = self.options.with_pango
        cmake.definitions['ENABLE_SQLITE'] = self.options.with_sqlite
        cmake.definitions['ENABLE_POSTGRES'] = self.options.with_postgres
        cmake.definitions['ENABLE_FIREBIRD'] = self.options.with_firebird
        cmake.definitions['ENABLE_MYSQL'] = self.options.with_mysql
        cmake.definitions['ENABLE_MSSQLSERVER'] = self.options.with_mssql
        cmake.definitions['ENABLE_QT4'] = self.options.with_qt4
        cmake.definitions['ENABLE_LIBWTTEST'] = self.options.with_test
        cmake.definitions['ENABLE_LIBWTDBO'] = self.options.with_dbo
        cmake.definitions['ENABLE_OPENGL'] = self.options.with_opengl
        cmake.definitions['ENABLE_UNWIND'] = self.options.with_unwind
        cmake.definitions['WT_NO_STD_LOCALE'] = self.options.no_std_locale
        cmake.definitions['WT_NO_STD_WSTRING'] = self.options.no_std_wstring
        cmake.definitions['MULTI_THREADED'] = self.options.multi_threaded
        cmake.definitions['USE_SYSTEM_SQLITE3'] = True
        cmake.definitions['DEBUG'] = self.settings.build_type == 'Debug'
        cmake.definitions['CONNECTOR_HTTP'] = self.options.connector_http
        if self.options.with_ssl:
            # FIXME : wt doesn't see OpenSSL on Windows
            cmake.definitions['SSL_PREFIX'] = self.deps_cpp_info['OpenSSL'].rootpath
            cmake.definitions['SSL_LIBRARIES'] = ';'.join(self.deps_cpp_info['OpenSSL'].libs)
            cmake.definitions['SSL_INCLUDE_DIRS'] = ';'.join(self.deps_cpp_info['OpenSSL'].include_paths)
            cmake.definitions['SSL_FOUND'] = True
        if self.settings.os == 'Windows':
            cmake.definitions['CONNECTOR_FCGI'] = False
            cmake.definitions['CONNECTOR_ISAPI'] = self.options.connector_isapi
        else:
            cmake.definitions['CONNECTOR_FCGI'] = self.options.connector_fcgi
            cmake.definitions['CONNECTOR_ISAPI'] = False
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        cmake.configure(build_folder=self.build_subfolder)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self.source_subfolder)
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = []
        if self.options.with_test:
            self.cpp_info.libs.append('wttest')
        if self.options.with_postgres:
            self.cpp_info.libs.append('wtdbopostgres')
        if self.options.with_sqlite:
            self.cpp_info.libs.append('wtdbosqlite3')
        if self.options.with_mysql:
            self.cpp_info.libs.append('wtdbomysql')
        if self.options.with_mssql:
            self.cpp_info.libs.append('wtdbomssqlserver')
        if self.options.with_firebird:
            self.cpp_info.libs.append('wtdbofirebird')
        if self.options.with_dbo:
            self.cpp_info.libs.append('wtdbo')
        if self.options.connector_http:
            self.cpp_info.libs.append('wthttp')
        if self.settings.os == 'Windows':
            if self.options.connector_isapi:
                self.cpp_info.libs.append('wtisapi')
        else:
            if self.options.connector_fcgi:
                self.cpp_info.libs.append('wtfcgi')
        self.cpp_info.libs.append('wt')
        if self.settings.build_type == 'Debug':
            self.cpp_info.libs = ['%sd' % lib for lib in self.cpp_info.libs]
        if self.settings.os == 'Linux':
            self.cpp_info.libs.append('dl')
        elif self.settings.os == 'Windows':
            self.cpp_info.libs.extend(['ws2_32', 'mswsock', 'wsock32'])
