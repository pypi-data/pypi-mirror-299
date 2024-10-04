from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name='visor-image-suite',
    version='2024.10.0',
    author='Zijian Yi',
    author_email='zj.yi1@siat.ac.cn',
    description='A Specialized Suite for VISoR Images.',
    long_description=long_description,  # Use the README as the long description
    long_description_content_type='text/markdown',
    url='https://github.com/visor-tech/visor-image-suite',
    packages=find_packages(include=['visor_image', 'visor_image.*']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
    install_requires=requirements,  # Read requirements from requirements.txt
    include_package_data=True,
    keywords='VISoR',
)
