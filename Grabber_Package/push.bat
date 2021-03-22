python setup.py sdist && twine upload --skip-existing dist/*
python setup.py install
rmdir /S /Q EL1T3.egg-info
rmdir /S /Q dist
rmdir /S /Q build