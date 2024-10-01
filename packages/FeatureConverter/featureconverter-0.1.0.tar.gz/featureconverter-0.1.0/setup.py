from setuptools import setup, find_packages

setup(
    name="FeatureConverter",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # List your app dependencies here
        "matplotlib",
        "numpy",
        "insightface",
        "onnx",
        "onnxruntime"
    ],
    author="Joachim de Lipthay Behrend",
    author_email="Joachim_dlb@hotmail.com",
    description="This app makes it possible to share research data by anonymizing the face of the subject",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/JoachimBehrend",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "my_project_command = my_package.main:main_function",
        ]
    },
    python_requires='>=3.6',
)
