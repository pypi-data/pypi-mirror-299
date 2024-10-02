from setuptools import setup, find_packages

setup(
    name='josewow',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'josewow': ['*.pyd', '*.so'],  # Inclui os arquivos compilados
    },
    install_requires=[],
)
