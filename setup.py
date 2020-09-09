import setuptools
import os

package_name = 'dspipe'
__local__ = os.path.abspath(os.path.dirname(__file__))

# Load the package version
f_version = os.path.join(__local__, package_name, "_version.py")
exec(open(f_version).read())

# Get the long description from the relevant file
long_description = f"""{package_name}
=================================
Easy to use data science pipes.
"""

setuptools.setup(
    name=package_name,
    packages=setuptools.find_packages(),
    
    # No package information needs to be included for this
    include_package_data=False,
    
    install_requires=[
        "joblib", # Parallel code
        "wasabi", # Colored logging
        "tqdm", # Status bar
    ],
    description=f"{package_name}: Easy to use data science pipes",
    long_description=long_description,
    version=__version__,
    
    # The project's main homepage.
    url=f"https://github.com/thoppe/{package_name}",
    
    # Author details
    author="Travis Hoppe",
    author_email=f"travis.hoppe+{package_name}@gmail.com",
    
    # Choose your license
    license="CC0",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5  -Production/Stable
        "Development Status :: 5 - Production/Stable",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Education",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Utilities",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3.7",
    ],
    # What does your project relate to?
    keywords="datascience",
    tests_require=["coverage", "pytest"],
)
