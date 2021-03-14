======
htm2md
======

htm2md is a Python library to convert html to markdown.

Demo
====

.. sourcecode:: python

  import htm2md

  # convert html to markdown
  md = htm2md.convert("<p>This is <a href='https://example.com'>example</a>.</p>")
  
  # output: This is [example](https://example.com).
  print(md)

License
=======

`MIT <https://choosealicense.com/licenses/mit/>`_
