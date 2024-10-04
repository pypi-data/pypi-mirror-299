from setuptools import setup, find_packages

setup(
    name='slyvek-setup',
    version='0.1.8',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'slyvek_setup': ['scripts/*.sh', 'templates/*'],
    },
    install_requires=[
        # Liste des dépendances Python si nécessaire
    ],
    entry_points={
        'console_scripts': [
            'slyvek-setup = slyvek_setup.main:main',
        ],
    },
    author='guiguito',
    description='Un paquet pour configurer un serveur VPS automatiquement.',
)
