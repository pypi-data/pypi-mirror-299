import setuptools
from setuptools import find_packages
import re

with open("./autodistill_yolov11/__init__.py", 'r') as f:
    content = f.read()
    # from https://www.py4u.net/discuss/139845
    version = re.search(r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]', content).group(1)
    
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autodistill_yolov11",  
    version=version,
    author="Roboflow",
    author_email="autodistill@roboflow.com",
    description="Label data with and train YOLOv11 models.",
    long_description="Label data with and train YOLOv11 models.",
    long_description_content_type="text/markdown",
    url="https://github.com/autodistill/autodistill-yolov11",
    install_requires=[
        "autodistill",
        "ultralytics==8.3.3",
        "torch"
    ],
    packages=find_packages(exclude=("tests",)),
    extras_require={
        "dev": ["flake8", "black==22.3.0", "isort", "twine", "pytest", "wheel"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
