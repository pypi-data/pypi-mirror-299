from setuptools import setup, find_packages
import pathlib

# Get the long description from the README file
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="oban_classifier",
    version="0.1.19.6",  # Incremented version number
    description="OBAN Classifier: A Skorch-based flexible neural network for binary and multiclass classification",
    long_description=README,  # Use the README file for long description
    long_description_content_type="text/markdown",  # Set content type as markdown
    author="Dr. Volkan OBAN",
    author_email="volkanobn@gmail.com",
    packages=find_packages(),
    python_requires='>=3.8',  # Specify minimum Python version
    install_requires=[
        'numpy', 
        'pandas', 
        'torch', 
        'scikit-learn', 
        'skorch', 
        'seaborn', 
        'matplotlib',
        'lime'  # Including LIME in the requirements
    ],
)

