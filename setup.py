from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

## edit below variables as per your requirements -
REPO_NAME = "DVC-CNN-TF-pipeline"
AUTHOR_USER_NAME = "iambalakrishnan"
SRC_REPO = "src"
LIST_OF_REQUIREMENTS = [
    "pandas==1.3.5",
    "tqdm==4.64.1",
    "dvc==2.10.2",
    "tensorflow==2.10.0",
    "joblib==1.2.0"
]


setup(
    name=SRC_REPO,
    version="0.0.3",
    author=AUTHOR_USER_NAME,
    description="A small package for DVC",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    author_email="imbkrishnaa@gmail.com",
    packages=[SRC_REPO],
    license="MIT",
    python_requires=">=3.6",
    install_requires=LIST_OF_REQUIREMENTS
)
