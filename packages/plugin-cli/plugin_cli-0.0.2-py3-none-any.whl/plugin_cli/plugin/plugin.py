#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2024 zhaosonggo@gmail.com, All rights reserved.
# Licensed under the Apache License Version 2.0 that can be found in the
# LICENSE file in the root directory of this source tree


class Plugin:
    def __init__(self, name):
        self.name = name

    def help(self) -> str:
        pass

    def accept(self, args):
        pass

    def build_command_args(self, subparser):
        pass
