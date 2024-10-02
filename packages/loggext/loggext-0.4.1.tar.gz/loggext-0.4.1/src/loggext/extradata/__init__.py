# -*- coding=utf-8 -*-
r"""
```pycon

>>> import logging
>>> logging.getLogger().addFilter(HostnameField() | ProgramNameField())

```
"""
from .hostname import *
from .program_name import *
from .short_name import *
from .username import *
