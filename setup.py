"""Setup script for WHO BMI Calculator."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="who-bmi-calculator",
    version="1.0.0",
    author="WHO BMI Calculator Team",
    author_email="",
    description="基于WHO儿童生长标准的BMI计算器",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/who-bmi-calculator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
    ],
    python_requires=">=3.7",
    install_requires=[],
    keywords="bmi, who, children, growth, health, percentile",
)
