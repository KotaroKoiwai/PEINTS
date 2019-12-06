# -*- coding: utf-8 -*-

import glob
import os
import datetime
from logging import getLogger, FileHandler, StreamHandler, DEBUG
from multiprocessing import cpu_count
from Bio import PDB
parser = PDB.PDBParser()

import main
import peints_result


class Manage():
    def __init__(self, progdir, workdir, template, sequence, beamtime_dir, targetsite, spacegroup, data_name,
                 flag_molrep, flag_coot, flag_overwrite, flag_pr, flag_water, flag_sa):

        self.print_logo()

        self.progdir = progdir
        self.workdir = workdir
        self.template = template
        self.sequence = sequence
        self.beamtime_dir = beamtime_dir
        self.targetsite = targetsite
        self.spacegroup = spacegroup
        self.data_name = data_name
        self.flag_molrep = flag_molrep
        self.flag_coot = flag_coot
        self.flag_overwrite = flag_overwrite
        self.flag_pr = flag_pr
        self.flag_water = flag_water
        self.flag_sa = flag_sa

        self.cpu_num = cpu_count()-1


        logfile = os.path.join(self.beamtime_dir, "peints_"+str(datetime.datetime.now())+".log")
        self.logger = getLogger(__name__)
        handler = FileHandler(filename=logfile)
        handler2 = StreamHandler()
        handler.setLevel(DEBUG)
        self.logger.setLevel(DEBUG)
        self.logger.addHandler(handler)
        self.logger.addHandler(handler2)
        self.logger.propagate = False
        self.logger.debug('\n\n\npeints started on ' + str(datetime.datetime.now()))
        self.logger.debug("progdir       :  "+self.progdir +"\n"
                     "workdir       :  "+self.workdir +"\n"
                     "template      :  "+self.template +"\n"
                     "sequence      :  "+self.sequence +"\n"
                     "beamtime_dir  :  "+self.beamtime_dir +"\n"
                     "target_site   :  "+self.targetsite +"\n"
                     "spacegroup    :  "+self.spacegroup +"\n"
                     "data name     :  "+self.data_name + "\n"                                                          
                     "molrep        :  "+str(self.flag_molrep) +"\n"
                     "image_capture_by_coot     :  "+str(self.flag_pr) +"\n"               
                     "phenix.refine             :  "+str(self.flag_water) +"\n"                  
                     "simulated_annealing       :  "+str(self.flag_sa) +"\n")

        self.prep()
        self.run()
        self.logger.debug("peints finished on "+str(datetime.datetime.now()))

    def print_logo(self):
        print """
    
    
    +-----------------------------------------------------------------------------------+
    |                                                                                   |
    |                                                                                   |
    |                                      peints                                      |
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

    def prep(self):
        self.template = os.path.abspath(self.template)
        self.sequence = os.path.abspath(self.sequence)
        self.beamtime_dir = os.path.abspath(self.beamtime_dir)


    def run(self):
        #=================================================
        # change Active-site of coot.py
        #=================================================
        coot_scm_orig = open(os.path.join(self.progdir, 'peints_coot.py'), 'r')
        lines = coot_scm_orig.readlines()
        coot_scm_orig.close()

        method = "refmac1"
        if self.flag_pr == "False":
            method = "refmac1"
        elif self.flag_pr == "True":
            method = "phenix_001"

        self.targetsite_for_coot = self.targetsite_analysis(self.targetsite)

        self.new_coot_lines = ""
        for l in lines:
            line = str(l)
            if line.startswith("screendump_image( ALL )"):
                line = "screendump_image( '"+str(method)+ "_all.png' )\n"
            if line.startswith("set_go_to_atom_chain_residue_atom_name"):
                line = "set_go_to_atom_chain_residue_atom_name( "+self.targetsite_for_coot+" )\n"
            if line.startswith("screendump_image( PNG1 )"):
                line = 'screendump_image("'+str(method)+'_targetsite_1.png")\n'
            if line.startswith("screendump_image( PNG2 )"):
                line = 'screendump_image("'+str(method)+'_targetsite_2.png")\n'
            self.new_coot_lines += line

        #=================================================
        # RUN
        #=================================================
        os.chdir(self.beamtime_dir)
        aimless_files = []
        aimless_files_1 = glob.glob('*/*/*/*/'+self.data_name)
        for file in aimless_files_1:
            aimless_files.append(file)
        aimless_files_1 = glob.glob('*/*/*/'+self.data_name)
        for file in aimless_files_1:
            aimless_files.append(file)
        aimless_files_1 = glob.glob('*/*/'+self.data_name)
        for file in aimless_files_1:
            aimless_files.append(file)

        self.num_aimless_file = len(aimless_files)

        self.xds_dirs = []
        for file in aimless_files:
            xds_dir = os.path.dirname(file)
            if not xds_dir.split("/")[-1][0:7]=="peints_":
                if self.flag_overwrite == "False":
                    if not os.path.exists(os.path.dirname(xds_dir)+"/peints_"+os.path.basename(xds_dir)):
                        self.xds_dirs.append(xds_dir)
                else:
                    self.xds_dirs.append(xds_dir)
        self.logger.debug("xds_? dir  :  "+ str(self.xds_dirs))
        import mypool
        p = mypool.MyPool(self.cpu_num)
        p.map(self.bash_peints, self.xds_dirs)


    def targetsite_analysis(self, targetsite):
        if " " in targetsite:
            self.targetsite = targetsite.replace(" ", "")

        if not "_" in targetsite:
            self.logger.debug("targetsite    :   single")
            chain_1 = targetsite.split("/")[0]
            resi_1  = targetsite.split("/")[1]
            atom_1  = targetsite.split("/")[2]
            targetsite_for_coot = "'"+str(chain_1)+"',"+str(resi_1)+",'"+str(atom_1)+"'"

        else:
            self.logger.debug("targetsite    :   pair")
            targetsite_for_coot = "'U',0,'U'"
        return targetsite_for_coot


    def bash_peints(self, xds_dir):
        main.Run(self.logger,
                 self.progdir,
                 xds_dir,
                 self.data_name,
                 self.new_coot_lines,
                 self.targetsite,
                 self.targetsite_for_coot,
                 self.template,
                 self.sequence,
                 self.beamtime_dir,
                 self.spacegroup,
                 self.flag_molrep,
                 self.flag_coot,
                 self.flag_pr,
                 self.flag_sa,
                 self.flag_water,
                 self.cpu_num,
                 self.xds_dirs)

        os.chdir(self.beamtime_dir)
        peints_result.result(self.logger, self.progdir, self.template, self.sequence, self.flag_pr)


#=================================================
# main function
#=================================================
if __name__  == '__main__':
    import sys
    import peints_argparse
    args = sys.argv
    input_parser = peints_argparse.peints_argparse(args)

    template = input_parser.model
    sequence = input_parser.sequence
    beamtime_dir = input_parser.beamtime_dir
    targetsite = input_parser.targetsite
    spacegroup = input_parser.spacegroup
    data_name  = input_parser.data_name
    if input_parser.skip_mr == False:
        flag_molrep = "True"
    else:
        flag_molrep = "False"
    if input_parser.no_png == False:
        flag_coot = "True"
    else:
        flag_coot = "False"
    if input_parser.phenix_refine == True:
        flag_pr = "True"
    else:
        flag_pr = "False"
    if input_parser.water == True:
        flag_water = "True"
    else:
        flag_water = "False"
    if input_parser.simulated_annealing == True:
        flag_sa = "True"
    else:
        flag_sa = "False"

    progdir = os.path.dirname(os.path.abspath(args[0]))
    workdir = os.getcwd()

    Manage(progdir, workdir, template, sequence, beamtime_dir, targetsite, spacegroup, data_name,
                 flag_molrep, flag_coot, flag_pr, flag_water, flag_sa)





