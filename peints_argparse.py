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
    |        -m/--model          :     Full path of a template model for MR             |  
    |        -seq/--sequence     :     Full path of a sequence file                     |    
    |        -bt/--beamtime_dir  :     Full path of a beamtime directory                |      
    |        -t/--targetsite     :     Your target site:                                |
    |                                  e.g. A/110/CZ,                                   |
    |                                       or A/39/CZ_A/110/CZ                         | 
    |        -data/--data_name   :     aimless.mtz or XDS_ASCII.HKL                     | 
    |                                                                                   |
    |     * Optional parameters                                                         |      
    |        -sg/--spacegroup    :     Spacegroup name                                  |     
    |        -skip_mr/--skip_mr  :     Do NOT MR, only refine                           |       
    |        -no_png/--no_png    :     Do not capture images by coot                    |     
    |        -pr/--phenix_refine :     Refinement with phenix.refine                    |
    |                                  after REFMAC5                                    |     
    |        -sa/--simulated_annealing :     phenix.refine with simulated annealing     |    
    |        -water/--water      :     input water molecules in phenix.refine           |     
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
    |        -m/--model          :     Full path of a template model for MR             |  
    |        -seq/--sequence     :     Full path of a sequence file                     |    
    |        -bt/--beamtime_dir  :     Full path of a beamtime directory                |      
    |        -t/--targetsite     :     Your target site:                                |
    |                                  e.g. A/110/CZ,                                   |
    |                                       or A/39/CZ_A/110/CZ                         |
    |        -data/--data_name   :     aimless.mtz or XDS_ASCII.HKL                     | 
    |                                                                                   | 
    |     * Optional parameters                                                         |      
    |        -sg/--spacegroup    :     Spacegroup name                                  |     
    |        -skip_mr/--skip_mr  :     Do NOT MR, only refine                           |       
    |        -no_png/--no_png    :     Do not capture images by coot                    |     
    |        -pr/--phenix_refine :     Refinement with phenix.refine                    |
    |                                  after REFMAC5                                    |     
    |        -sa/--simulated_annealing :     phenix.refine with simulated annealing     |    
    |        -water/--water      :     input water molecules in phenix.refine           |     
    |                                                                                   |
    |                                                                                   |
    +-----------------------------------------------------------------------------------+""",
        epilog='end',  # description after help
        add_help=True,  # help option
    )
    parser.add_argument("program",
                        nargs=1)
    parser.add_argument("-m", "--model",
                        default="",
                        required=True,
                        help='A template model for MR')
    parser.add_argument("-seq", "--sequence",
                        default="",
                        type=str,
                        required=True,
                        help='A sequence file')
    parser.add_argument("-bt", "--beamtime_dir",
                        default="",
                        required=True,
                        type=str,
                        help='A beamtime directory')
    parser.add_argument("-t", "--targetsite",
                        type=str,
                        required=True,
                        default="A/110/CZ",
                        help='Your target site: e.g. A/110/CZ, or A/39/CZ_A/110/CZ')

    parser.add_argument("-sg", "--spacegroup",
                        type=str,
                        default="Spacegroup_suggested_by_PReMo",
                        help='Spacegroup name: e.g. P212121')

    parser.add_argument("-data", "--data_name",
                        type=str,
                        default="aimless.mtz",
                        help='Data name  :  aimless.mtz or XDS_ASCII.HKL')

    parser.add_argument("-skip_mr", "--skip_mr",
                        action="store_true",
                        required=False,
                        help='Do not MR')

    parser.add_argument("-no_png", "--no_png",
                        action="store_true",
                        required=False,
                        help='Do or do not capture images by coot')

    parser.add_argument("-pr", "--phenix_refine",
                        action="store_true",
                        required=False,
                        help='phenix.refine after REFMAC5')

    parser.add_argument("-sa", "--simulated_annealing",
                        action="store_true",
                        required=False,
                        help='phenix.refine with simulated annealing')

    parser.add_argument("-water", "--water",
                        action="store_true",
                        required=False,
                        help='input water molecules in phenix.refine')

    print parser.parse_args(args)
    input_parser = parser.parse_args(args)
    return input_parser


if __name__  == '__main__':
    import sys
    args = sys.argv
    input_parser = peints_argparse(args)
