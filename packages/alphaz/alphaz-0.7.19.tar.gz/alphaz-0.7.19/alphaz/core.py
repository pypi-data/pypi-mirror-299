import os, sys

from alphaz.models.main import AlphaCore, singleton


@singleton
class Core(AlphaCore):
    def __init__(self, file: str):
        super().__init__(file)


core = Core(__file__)

DB, API, LOG = core.db, core.api, core.log
