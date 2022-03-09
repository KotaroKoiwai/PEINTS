#! /Library/Frameworks/Python.framework/Versions/2.7/bin python
# -*- coding: utf-8 -*-

import argparse
import os, sys


def peints_argparse(args):
    print """
    
    
    +-----------------------------------------------------------------------------------+
    |                                                                                   |
    |                                                                                   |
    |                                      PEINTS                                       |
    |                                MR for ligand screening                            |
    |                                                                                   |
    |                             Kotaro Koiwai, Toshiya Senda                          |
    |                                                                                   |    
    |     * required parameters                                                         |    
    |        -i/--input_file          :     Full path of a PEINTS CSV file              |  
    |                                                                                   |
    |                                                                                   |
    +-----------------------------------------------------------------------------------+
    
    """
    print args

    parser = argparse.ArgumentParser(
        prog='peints_argparse.py',  # program name
        usage='peints',  # programe usage
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
    +-----------------------------------------------------------------------------------+
    |                                                                                   |
    |                                                                                   |
    |                                      PEINTS                                       |
    |                                MR for ligand screening                            |
    |                                                                                   |
    |                             Kotaro Koiwai, Toshiya Senda                          |
    |                                                                                   |    
    |     * required parameters                                                         |    
    |        -i/--input_file          :     Full path of a PEINTS CSV file              |  
    |                                                                                   |
    |                                                                                   |
    +-----------------------------------------------------------------------------------+""",
        epilog='end',  # description after help
        add_help=True,  # help option
    )
    parser.add_argument("program",
                        nargs=1)
    parser.add_argument("-i", "--input_file",
                        default="",
                        required=True,
                        help='Full path of a PEINTS CSV file')

    print parser.parse_args(args)
    input_parser = parser.parse_args(args)
    return input_parser


if __name__  == '__main__':
    import sys
    args = sys.argv
    input_parser = peints_argparse(args)
