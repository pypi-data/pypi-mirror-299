import sys
from setuptools import setup

print(sys.argv)
if len(sys.argv) < 3:
    raise RuntimeError("Bad parameters to build the package")

ACTION: str = sys.argv[1]
PACKAGE_NAME: str = sys.argv[2]
PACKAGE_VERSION: str = "0.0.8"

sys.argv.remove(PACKAGE_NAME)

ERROR_MSG: str = """


################################################################################################
The package you are trying to install is only a placeholder project on PyPI.org repository.
This package is hosted on SqueezeBits Python Package Index.

This package can be installed as:
```
$ pip install owlite --extra-index-url https://pypi.squeezebits.com/
```

Please visit us at https://www.squeezebits.com or github.com/SqueezeBits/owlite for further information.
################################################################################################



"""


def main():
    global ACTION, PACKAGE_NAME, PACKAGE_VERSION, README_MD
    setup(
        name="owlite",
        version=PACKAGE_VERSION,
        description="A fake package to warn the user they are not installing the correct package.",
        url="https://github.com/SqueezeBits/owlite",
        author="SqueezeBits Inc.",
        author_email="owlite@squeezebits.com",
        classifiers=[
            "Development Status :: 1 - Planning",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: Apache Software License",
            "Topic :: Scientific/Engineering",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
            "Topic :: Software Development",
            "Topic :: Software Development :: Libraries",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],
        keywords=["torch", "onnx", "graph", "quantization", "owlite"],
    )


if ACTION == "sdist":
    main()
else:
    raise RuntimeError(ERROR_MSG)

