import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="report_pkg_Karpenko",
    version="0.0.2",
    author="Viktor Karpenko",
    author_email="karpenkotakeoff@gmail.com",
    description="Create report from raw data F1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.foxminded.com.ua/karpenko_viktor/task-6-report-of-monaco-2018-racing",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
    ],
    python_requires='>=3.8',
)
