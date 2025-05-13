#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from sqlalchemy import create_engine

from machine_tools_3.app.core.config import get_settings

settings = get_settings()
engine = create_engine(settings.DATABASE_URL)
