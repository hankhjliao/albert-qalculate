# -*- coding: utf-8 -*-
"""Qalculate!
Synopsis: <trigger> <expression>"""

import subprocess

from albert import *

__title__ = "Qalculate!"
__version__ = "0.4.0"
__triggers__ = "qc "
__authors__ = ["hankliao87"]
__exec_deps__ = ["qalc"]

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
                item.text = "Error: " + str(ex)
                item.subtext = "Please create an issue in https://github.com/hankliao87/albert-qalculate"
                item.addAction(ClipAction(text="Copy error message to clipboard", clipboardText=str(ex)))
                item.addAction(ClipAction(text="Copy repo url to clipboard", clipboardText="https://github.com/hankliao87/albert-qalculate"))
                return item

            item = Item(id=__title__, icon=iconPath)
            item.text = str(result)
            item.subtext = query_string
            item.addAction(ClipAction(text="Copy result to clipboard", clipboardText=str(result)))
            item.addAction(ClipAction(text="Copy result with expression to clipboard", clipboardText=str(result_with_expression)))
            return item
