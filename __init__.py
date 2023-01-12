# -*- coding: utf-8 -*-

import subprocess

from albert import *

__doc__="""
Qalculate!
Synopsis: `<trigger> <expression>`
"""

md_iid = "0.5"
md_version = "0.1"
md_name = "Qalculate!"
md_description = "Qalculate!"
md_license = "MIT"
md_url = "https://github.com/hankliao87/albert-qalculate"
md_maintainers = "@hankliao87"
md_bin_dependencies = ["qalc"]

trigger = "qc "

class Plugin(QueryHandler):
    iconPath = ["xdg:qalculate"]

    def id(self):
        return __name__

    def name(self):
        return md_name

    def description(self):
        return md_description

    def synopsis(self) -> str:
        return "<expression>"

    def defaultTrigger(self) -> str:
        return trigger

    def handleQuery(self, query):
        query_string = query.string.strip()

        if query_string == '':
            item = Item(id=__name__, icon=self.iconPath)
            item.text = "Enter an expression"
            item.subtext = ""
            query.add(item)
            return
        else:
            try:
                proc_result = subprocess.run(['qalc', '-s', 'upxrates 0', '-t', query_string], stdout=subprocess.PIPE, text=True, timeout=10)
                proc_expression = subprocess.run(['qalc', '-s', 'upxrates 0', query_string], stdout=subprocess.PIPE, text=True, timeout=10)

                result = proc_result.stdout.replace('\n','')
                result_with_expression = proc_expression.stdout.replace('\n','')
            except Exception as ex:
                item = Item(
                    id=__name__,
                    icon=self.iconPath,
                    actions=[
                        Action(
                            id="copy-clipboard",
                            text="Copy error message to clipboard",
                            callable=lambda u=str(ex): setClipboardText(u)),
                        Action(
                            id="copy-repo-url",
                            text="Copy repo url to clipboard",
                            callable=lambda: setClipboardText(md_url)),
                    ]
                )
                item.text = "Error: " + str(ex)
                item.subtext = f"Please create an issue in {md_url}"
                query.add(item)
                return

            item = Item(
                id=__name__,
                icon=self.iconPath,
                actions=[
                    Action(
                        id="copy-clipboard",
                        text="Copy result to clipboard",
                        callable=lambda u=str(result): setClipboardText(u)),
                    Action(
                        id="copy-clipboard-expression",
                        text="Copy result with expression to clipboard",
                        callable=lambda u=str(result_with_expression): setClipboardText(u)),
                ]
            )
            item.text = str(result)
            item.subtext = query_string
            query.add(item)
            return
