from setuptools import setup, find_packages
import pathlib

# Get the long description from the README file
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()


setup(
    name="oban_classifier",
    version="0.1.15",  # Versiyon numarasını arttır
    description="OBAN Classifier: A Skorch-based flexible neural network for binary and multiclass classification",
    author="Dr. Volkan OBAN",
    author_email="volkanobn@gmail.com",
    packages=find_packages(),
    install_requires=[
        'numpy', 
        'pandas', 
        'torch', 
        'scikit-learn', 
        'skorch', 
        'seaborn', 
        'matplotlib'
    ],
)

