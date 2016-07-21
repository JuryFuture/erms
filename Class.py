# -*- coding: utf-8 -*-
class MyClass(object):
    def __init__(self, name="Jury"):
        self.name = name

    def foo(self):
        print self.name


mc = MyClass("滕国栋")
mc.foo()
