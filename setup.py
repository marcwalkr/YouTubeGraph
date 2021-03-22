from setuptools import setup


def readme_file_contents():
    with open('README.rst') as readme_file:
        data = readme_file.read()
    return data


setup(
    name='youtubegraph',
    version='1.0.0',
    description='Analyzes mobile screenshots of the Time watched page in YouTube and estimates bar graph values',
    long_description=readme_file_contents(),
    long_description_content_type='text/x-rst',
    author='marcwalkr',
    author_email='marcwalkr@gmail.com',
    license='MIT',
    packages=['youtubegraph'],
    entry_points={
        'console_scripts': ['youtubegraph=youtubegraph.__main__:main']
    },
    zip_safe=False,
    install_requires=[
        'easyocr',
        'Pillow',
    ]
)
