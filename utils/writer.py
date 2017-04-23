"""
A module serving as a writer of the dependencies to a file
"""
from utils.slugify import slugify

__author__ = 'Ma Zijun'
__date__ = '2017-04-23'


class Writer(object):
    """
    Class serves as a file writer
    """
    def __init__(self):
        pass

    @classmethod
    def to_expression(cls, dependency):
        """
        Generate a formatted dependency expression
        :param dependency: the function dependency derived from TANE algorithm
        :return: a string representing the expression
        """
        return slugify(dependency[0], ' ') + ' -> ' + str(dependency[1])

    @classmethod
    def write_dependency_to_file(cls, dependencies, output_file_name):
        """
        Write dependency to output file
        :param dependencies: dependency list derived from TANE algorithm
        :param output_file_name: name of the output file
        """
        result = list()
        for dependency in dependencies:
            result.append(Writer.to_expression(dependency))
        try:
            with open(output_file_name, 'w') as f:
                f.writelines('\n'.join(result))
        except IOError as e:
            print(e)
            exit(1)
