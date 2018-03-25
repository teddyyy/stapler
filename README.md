stapler
===============

CLI tool to release from multiple git repositories collectively

setup
--------------

```
$ git clone https://github.com/teddyyy/stapler.git
$ cd stapler
$ export GITHUB_ACCESS_TOKEN=XXX
$ pip install -r requirements.txt
$ cd config
$ cp sample.yml config.yml
```
edit config.yml to work properly

run
---------------

Create release

```
$ python stapler.py -f config.yaml
```

Delete tag and release

```
$ python stapler.py -f config.yaml -d
```
