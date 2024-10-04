# coding: utf-8
# Copyright 2009-2014 The txmongo authors.  All rights reserved.
# Use of this source code is governed by the Apache License that can be
# found in the LICENSE file.

import sys
import warnings

from txmongo.connection import (
    MongoConnection,
    MongoConnectionPool,
    lazyMongoConnection,
    lazyMongoConnectionPool,
)
from txmongo.database import Database
from txmongo.protocol import MongoProtocol, Query

assert Database
assert MongoProtocol
assert Query
assert MongoConnection
assert MongoConnectionPool
assert lazyMongoConnection
assert lazyMongoConnectionPool

if sys.version_info < (3, 8):
    warnings.warn(
        "Only Python 3.8+ will be supported in the next version of TxMongo",
        DeprecationWarning,
    )
