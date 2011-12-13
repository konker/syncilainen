# -*- coding: utf-8 -*-
#
# vcs
# 
# Dynamically loads a VCS interface implementation
#
# Authors: Konrad Markus <konker@gmail.com>
#

class UnknownVCSException(Exception): pass

OK = True
NOT_OK = False

try:
    from impl.git import VCSImpl
except ImportError:
    raise UnknownVCSException()


def VCS(repo_directory):
    return VCSImpl(repo_directory)

