#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '将main python项目转换为exe文件'
__author__ = 'hc'
__email__ = 'he-128@163.com'
"""
from PyInstaller.__main__ import run

if __name__ == '__main__':
    opts = ['modbus-rtu.py', 
    		'-F', 
    		'-w', 
    		'--icon=F:\python\Modbus-RTU\png\\title.ico',
    		]
    run(opts)