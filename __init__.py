# -*- coding: utf-8 -*-
"""Qalculate!
Synopsis: <trigger> <expression>"""

import subprocess

from albert import *

__title__ = "Qalculate!"
__version__ = "0.4.0"
__triggers__ = "qc "
__authors__ = ["hankliao87"]

iconPath = iconLookup("qalculate")

def handleQuery(query):
    if query.isTriggered:
        query_string = query.string.strip()

        if query_string == '':
            item = Item(id=__title__, icon=iconPath)
            item.text = "Enter an expression"
            item.subtext = ""
            return item
        else:
            try:
                proc_result = subprocess.run(['qalc', '-t', query_string], stdout=subprocess.PIPE, text=True)
                proc_expression = subprocess.run(['qalc', query_string], stdout=subprocess.PIPE, text=True)

                result = proc_result.stdout
                result_with_expression = proc_expression.stdout
            except Exception as ex:
                item = Item(id=__title__, icon=iconPath)
                item.text = str(ex)
                item.subtext = "Error"
                return item

            item = Item(id=__title__, icon=iconPath)
            item.text = str(result)
            item.subtext = query_string
            item.addAction(ClipAction("Copy result to clipboard", str(result)))
            item.addAction(ClipAction("Copy result with expression to clipboard", str(result_with_expression)))
            return item
