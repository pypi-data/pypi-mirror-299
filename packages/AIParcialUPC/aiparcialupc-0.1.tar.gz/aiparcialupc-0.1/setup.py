from setuptools import setup

readme = open("./README.md", "r")


setup(
    name='AIParcialUPC',
    packages=['AIParcialUPC'],  # this must be the same as the name above
    version='0.1',
    description='Esta es la descripcion de mi paquete',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    author='XD',
    keywords=['perceptron', 'annealing', 'ai'],
    classifiers=[ ],
    license='MIT',
    include_package_data=True
)