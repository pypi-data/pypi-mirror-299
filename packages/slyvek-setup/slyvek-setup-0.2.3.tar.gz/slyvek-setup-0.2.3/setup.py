from setuptools import setup, find_packages

setup(
    name='slyvek-setup',
    version='0.2.3',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'slyvek_setup': ['scripts/*.sh', 'templates/*'],
    },
    install_requires=[
        'bcrypt>=4.2.0',
    ],
    entry_points={
        'console_scripts': [
            'slyvek-setup = slyvek_setup.main:main',
        ],
    },
    author='guiguito',
    description='Un paquet pour configurer un serveur VPS automatiquement.',
)
