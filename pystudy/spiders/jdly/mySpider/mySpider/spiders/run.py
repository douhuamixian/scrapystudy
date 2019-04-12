#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Author: zouyuxiao
#@File  : run.py
from scrapy import cmdline


name = 'jder'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())