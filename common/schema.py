#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:Lijiacai
Email:1050518702@qq.com
===========================================
CopyRight@JackLee.com
===========================================
"""

import os
import sys
import json
import graphene
import logging


class QueryMutation(graphene.ObjectType):
    users = os.listdir("resource")
    result = []
    for user in users:
        if "py" in user or "pyc" in user:
            continue
        try:
            vs = os.listdir("resource/{}/view".format(user))
        except Exception as e:
            vs = []
        for v in vs:
            if ".py" in v:
                v = v.replace(".py", "").replace(".pyc", "")
            else:
                continue
            try:
                exec("from resource.{}.view.{} import *".format(user, v))
            except Exception as e:
                continue

    vars = dict(locals())
    for k, v in vars.items():
        try:
            if v.__base__.__name__ == "BaseApi":
                result.append(v)
        except:
            pass
    for Api in result:
        m = Api()
        try:
            exec("{} = m.api".format(str(m.name)))
            exec("def resolve_{}(self, info, **kwargs): return m.entrance(info, **kwargs)".format(m.name))
        except:
            pass


schema = graphene.Schema(query=QueryMutation, mutation=QueryMutation)
