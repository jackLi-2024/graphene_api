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


class BaseApi():
    name = "base_api"
    description = "测试"

    class Argument:
        pass

    class Return:
        pass

    def create_class(self, rename, parent_class="Argument,graphene.InputObjectType"):
        class_str = "class {}({}):pass;".format(rename, parent_class)
        exec(class_str)
        return eval(rename)

    @property
    def api(self):
        arg = self.Argument()
        ret = self.Return()
        arg_list = []
        ret_list = []
        for a in arg.__dir__():
            if a[:2] == "__" or a[-2:] == "__":
                continue
            elif "graphene" in str(type(eval("arg.{}".format(a)))) or "graphene" in str(eval("arg.{}".format(a))):
                arg_list.append(a)
        for a in ret.__dir__():

            if a[:2] == "__" or a[-2:] == "__":
                continue

            elif "graphene" in str(type(eval("ret.{}".format(a)))) or "graphene" in str(eval("ret.{}".format(a))):
                ret_list.append(a)
            else:
                print(type(eval("ret.{}".format(a))))
        if ret_list and arg_list:
            return graphene.Field(
                self.create_class(rename="{}_return".format(self.name), parent_class="self.Return,graphene.ObjectType"),
                condition=self.create_class(rename="{}_argument".format(self.name),
                                            parent_class="self.Argument,graphene.InputObjectType")(),
                description=self.description)
        elif ret_list:
            return graphene.Field(
                self.create_class(rename="{}_return".format(self.name), parent_class="self.Return,graphene.ObjectType"),
                description=self.description)
        else:
            raise Exception("该模型{}创建失败: 请给指定返回模型".format(self.name))

    def auth(self, info, **kwargs):
        pass

    def entrance(self, info, **kwargs):
        self.arguments = kwargs.get("condition", {})
        self.page_num = self.arguments.get("page_num", 1)
        self.page_size = self.arguments.get("page_size", 10)
        self.sort_field = self.arguments.get("sort_field", {})
        self.token = self.auth(info, **kwargs)
        return self.deal(self.token, **kwargs)

    def deal(self, token, **kwargs):
        return
