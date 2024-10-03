import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="imageCS_utils",
    version="0.0.1",
    author="Liao Chen",
    author_email="liaochen@bjtu.edu.cn",
    description="Simple utils for deep learning image compressive sensing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://localhost",
    install_requires=["torch", "torchvision", "torchaudio", "timm", "einops", "thop", "pytorch-fid", "opencv-python"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)