from setuptools import setup, find_packages

setup(
    name="Bhaskara",  # Replace with your package name
    version="1.6.4.0",
    description="Bhaskara Programming Engine",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    #url="https://github.com/username/my_package",  # Replace with your repository
    author="Prakamya Khare",
    author_email="khareprakamya27@gmail.com",
    license="MIT",  # Or other license you use
    packages=find_packages(),  # This will include your package
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[],  # List any dependencies here
)
