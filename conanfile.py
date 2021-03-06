from conans import ConanFile, CMake, tools
import os


class WtConan(ConanFile):
    name = "wt"
    version = "4.3.1"
    description = "Wt is a C++ library for developing web applications"
    url = "https://github.com/bincrafters/conan-wt"
    homepage = "https://github.com/emweb/wt"
    topics = ("conan", "wt", "web", "webapp")
    license = "GPL-2.0-only"
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
    default_options = {'shared': False, 'fPIC': True, 'with_ssl': True, 'with_haru': False, 'with_pango': False, 'with_sqlite': True, 'with_postgres': False, 'with_firebird': False, 'with_mysql': False, 'with_mssql': False, 'with_qt4': False, 'with_test': True, 'with_dbo': True, 'with_opengl': False, 'with_unwind': False, 'no_std_locale': False, 'no_std_wstring': False, 'multi_threaded': True, 'connector_http': True, 'connector_isapi': True, 'connector_fcgi': False}

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    _cmake = None

    requires = ('zlib/1.2.11', 'boost/1.73.0')

    def requirements(self):
        if self.options.with_ssl:
            self.requires('openssl/1.1.1g')
        if self.options.with_sqlite:
            self.requires('sqlite3/3.31.1')

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC
            del self.options.connector_fcgi
        else:
            del self.options.connector_isapi

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.definitions['SHARED_LIBS'] = self.options.shared
        self._cmake.definitions['BUILD_EXAMPLES'] = False
        self._cmake.definitions['BUILD_TESTS'] = False
        self._cmake.definitions['ENABLE_SSL'] = self.options.with_ssl
        self._cmake.definitions['ENABLE_HARU'] = self.options.with_haru
        self._cmake.definitions['ENABLE_PANGO'] = self.options.with_pango
        self._cmake.definitions['ENABLE_SQLITE'] = self.options.with_sqlite
        self._cmake.definitions['ENABLE_POSTGRES'] = self.options.with_postgres
        self._cmake.definitions['ENABLE_FIREBIRD'] = self.options.with_firebird
        self._cmake.definitions['ENABLE_MYSQL'] = self.options.with_mysql
        self._cmake.definitions['ENABLE_MSSQLSERVER'] = self.options.with_mssql
        self._cmake.definitions['ENABLE_QT4'] = self.options.with_qt4
        self._cmake.definitions['ENABLE_LIBWTTEST'] = self.options.with_test
        self._cmake.definitions['ENABLE_LIBWTDBO'] = self.options.with_dbo
        self._cmake.definitions['ENABLE_OPENGL'] = self.options.with_opengl
        self._cmake.definitions['ENABLE_UNWIND'] = self.options.with_unwind
        self._cmake.definitions['WT_NO_STD_LOCALE'] = self.options.no_std_locale
        self._cmake.definitions['WT_NO_STD_WSTRING'] = self.options.no_std_wstring
        self._cmake.definitions['MULTI_THREADED'] = self.options.multi_threaded
        self._cmake.definitions['USE_SYSTEM_SQLITE3'] = True
        self._cmake.definitions['DEBUG'] = self.settings.build_type == 'Debug'
        self._cmake.definitions['CONNECTOR_HTTP'] = self.options.connector_http
        self._cmake.definitions['BOOST_DYNAMIC'] = self.options['boost'].shared
        self._cmake.definitions['BOOST_PREFIX'] = self.deps_cpp_info['boost'].rootpath
        boost_version = self.deps_cpp_info['boost'].version
        self._cmake.definitions['Boost_ADDITIONAL_VERSIONS'] = boost_version[0:boost_version.rindex(".")]
        self._cmake.definitions['BOOST_PREFIX_DEFAULT'] = self.deps_cpp_info['boost'].rootpath
        self._cmake.definitions['BOOST_DIR'] = self.deps_cpp_info['boost'].rootpath
        self._cmake.definitions['BOOST_ROOT'] = self.deps_cpp_info['boost'].rootpath
        self._cmake.definitions['Boost_NO_SYSTEM_PATHS'] = True
        if self.options.with_ssl:
            self._cmake.definitions['OPENSSL_PREFIX'] = self.deps_cpp_info['openssl'].rootpath
            self._cmake.definitions['OPENSSL_LIBRARIES'] = ';'.join(self.deps_cpp_info['openssl'].libs + self.deps_cpp_info['openssl'].system_libs)
            self._cmake.definitions['OPENSSL_INCLUDE_DIR'] = ';'.join(self.deps_cpp_info['openssl'].include_paths)
            self._cmake.definitions['OPENSSL_FOUND'] = True
        if self.settings.os == 'Windows':
            self._cmake.definitions['CONNECTOR_FCGI'] = False
            self._cmake.definitions['CONNECTOR_ISAPI'] = self.options.connector_isapi
        else:
            self._cmake.definitions['CONNECTOR_FCGI'] = self.options.connector_fcgi
            self._cmake.definitions['CONNECTOR_ISAPI'] = False
            self._cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        self._cmake.configure(build_folder=self._build_subfolder)
        return self._cmake

    def build(self):
        tools.replace_in_file(os.path.join(self._source_subfolder, 'CMakeLists.txt'), 'find_package(OpenSSL)', '#find_package(OpenSSL)')
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
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
