Prérequis

    apt install twine
    add .pypirc file

Pour build :

    python3 setup.py sdist bdist_wheel

Pour upload :  

    twine upload dist/*