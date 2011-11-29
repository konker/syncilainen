
class UnknownAPIException(Exception): pass

try:
    from impl.git import VCSImpl
except ImportError:
    raise UnknownAPIException()


def VCS(repo_directory):
    return VCSImpl(repo_directory)

