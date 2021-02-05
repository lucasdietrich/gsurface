# Build command

First upgrade *wheel* package

`pip install --upgrade wheel`

Build the package

```
python setup.py bdist_wheel -d wheel
```

Delete *build* and *gsurface.egg-info* dirs

Wheel in *wheel* directory