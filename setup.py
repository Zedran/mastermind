import cx_Freeze
# python "setup.py" build
# python setup.py bdist_msi  -- installer, use ascii chars in path exclusively


executables = [cx_Freeze.Executable(
    script="Mastermind.pyw",
    base="Win32GUI",
    targetName="Mastermind",
    icon="dev_res/m.ico")
]

cx_Freeze.setup(
    name="Mastermind",
    description="",
    version="1.0.5",
    options={
        "build_exe": {
            "packages": ["pygame"],
            "include_files": ["m.png"],
            "excludes": ['pandas', 'matplotlib', 'PyQT5', 'scipy', 'numpy', 'tkinter', 'PyQT4',
                         'email', 'html', 'http', 'json', 'lib2to3', 'multiprocessing', 'test', 'unittest',
                         'urllib', 'logging', 'distutils', 'ctypes', 'pkg_resources', 'pydoc_data']
        }
    },
    executables=executables
)
