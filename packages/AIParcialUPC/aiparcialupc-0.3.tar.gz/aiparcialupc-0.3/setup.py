from setuptools import setup

readme = open("./README.md", "r")


setup(
    name='AIParcialUPC',
    packages=['AIParcialUPC'],
    version='0.3',
    description='Esta es la descripcion de mi paquete',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    author='XD',
    keywords=['perceptron', 'ramificacion', 'ai'],
    classifiers=[ ],
    license='MIT',
    include_package_data=True
)