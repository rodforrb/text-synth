## Project structure from flask-empty

## main.py

Holds your project class definition and factory.

## wsgi.py

This is where your project instance lives.

## config.py

Holds most of your configuration, like which extensions to use, which
blueprints to load, how looging should work, etc.

## commands.py

You can add custom commands to your project here.

## extensions.py

Your extensions are defined and loaded here. If you're adding a new
extension to your project, might be a good idea to create its instance
here (and load it through your configuration).

## mixins.py

Right now it only has a http mixin for some standard http behavior. Useful
for vanilla web projects. Not so much if you're building a web service.

## tests/

Project wide non-server dependent tests go here.
