from distutils.core import setup, Extension

module1 = Extension('dither.c_dither',
 define_macros = [('MAJOR_VERSION', '1'), ('MINOR_VERSION', '0')],
 include_dirs = ['/usr/local/include'],
 library_dirs = ['/usr/local/lib'],
 sources = ['dither/c_dither.cpp'],
 extra_compile_args = ['-std=c++11'])

setup (name = 'Ditherer',
       version = '1.0',
       description = 'This is a demo package',
       author = 'Mohamed Essam',
       author_email = 'mohamed.essam.arafa@gmail.com',
       url = '',
       long_description = '''
This is really just a demo package.
''',
       ext_modules = [module1])
