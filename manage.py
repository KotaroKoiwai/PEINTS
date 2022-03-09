# -*- coding: utf-8 -*-

import os
import glob, csv, datetime
from logging import getLogger, FileHandler, StreamHandler, DEBUG
from multiprocessing import cpu_count
from Bio import PDB
parser = PDB.PDBParser()

import main
import peints_result


class Manage():
    def __init__(self, input_file):

        self.input_file = input_file
        self.print_logo()
        self.read_input_file()
        self.run_date = str(datetime.datetime.now())
        self.cpu_num = cpu_count()-1
        self.prep()

        logfile = os.path.join(self.workdir, "peints_"+str(datetime.datetime.now())+".log")
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
                     "cut-off I/sigma(I)        :  "+str(self.cutoff_ios) +"\n"
                     "molrep        :  "+str(self.flag_molrep) +"\n"
                     "image_capture_by_coot     :  "+str(self.flag_coot) +"\n"   
                     "PHENIX                    :  "+str(self.flag_phenix) + "\n"
                     "phenix.refine             :  "+str(self.flag_pr) + "\n"
                     "Phaser                    :  "+str(self.flag_phaser) + "\n"
                     "input_water               :  "+str(self.flag_water) +"\n"
                     "simulated_annealing       :  "+str(self.flag_sa) +"\n")

        self.manage_project()
        self.run()
        self.logger.debug("peints finished on "+str(datetime.datetime.now()))

    def print_logo(self):
        print("""
        
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
    
        """)

    def read_input_file(self):
        csv_file = open(self.input_file, "r")
        f = csv.DictReader(csv_file)
        input_dict_list = [raw for raw in f]
        input_dict = input_dict_list[0]
        csv_file.close()
        self.progdir = input_dict["progdir"]
        self.template = input_dict["template"]
        self.workdir = input_dict["beamtime_directory"]
        self.sequence = input_dict["sequence"]
        self.spacegroup = input_dict["spacegroup"]
        self.targetsite = input_dict["targetsite"]
        self.cutoff_ios = input_dict["cutoff_ios"]
        self.data_name = input_dict["data_name"]
        self.flag_molrep = input_dict["flag_molrep"]
        self.flag_coot = input_dict["flag_coot"]
        self.flag_overwrite = input_dict["flag_overwrite"]
        self.flag_skip_processed_data = input_dict["flag_skip_processed_data"]
        self.flag_phenix = input_dict["flag_phenix"]
        self.flag_phaser = input_dict["flag_phaser"]
        self.flag_pr= input_dict["flag_pr"]
        self.flag_water= input_dict["flag_water"]
        self.flag_sa = input_dict["flag_sa"]
        self.beamtime_dir = self.workdir


    def prep(self):
        self.template = os.path.abspath(self.template)
        self.sequence = os.path.abspath(self.sequence)
        self.beamtime_dir = os.path.abspath(self.beamtime_dir)

        f = open(os.path.join(self.progdir, "VERSION"), "r")
        lines = f.readlines()
        f.close()
        self.version = ""
        for line in lines:
            self.version += line

    def manage_project(self):
        self.csv_dict_list = []
        if self.template.split(".")[-1] != "csv":
            pass
        else:
            import csv
            csv_file = open(self.template, "r")
            f = csv.DictReader(csv_file)
            for raw in f:
                del raw["Barcode"], raw["Comment"], raw["Screening"], raw["Run"], \
                    raw["Start"], raw["Total_frame"], raw["Start_omega"], raw["Snap_omega"], \
                    raw["Osc_width"], raw["Exp_time"], raw["Wavelength"], raw["Max_resolution"], \
                    raw["Camera_height"], raw["Hwidth"], raw["Vwidth"], raw["Transmittance"], \
                    raw["Binning"], raw["Divergence"]
                raw["data_is"] = 0
                print(raw)
                self.csv_dict_list.append(raw)
            csv_file.close()

    def run(self):
        #=================================================
        # change Active-site of coot.py
        #=================================================
        coot_scm_orig = open(os.path.join(self.progdir, 'peints_coot.py'), 'r')
        lines = coot_scm_orig.readlines()
        coot_scm_orig.close()

        method = "refmac1"
        if self.flag_phenix == "False":
            method = "refmac1"
        elif self.flag_phenix == "True" or self.flag_pr == "True":
            method = "phenix_001"

        self.targetsite_for_coot = self.targetsite_analysis(self.targetsite)

        self.new_coot_lines = ""
        for l in lines:
            line = str(l)
            if line.startswith("screendump_image( ALL )"):
                line = "screendump_image( '"+str(method)+ "_all.png' )\n"
            if line.startswith("set_go_to_atom_chain_residue_atom_name"):
                if self.targetsite_for_coot == "":
                    line = ""
                else:
                    line = "set_go_to_atom_chain_residue_atom_name( "+self.targetsite_for_coot+" )\n"
            if line.startswith("screendump_image( PNG1 )"):
                line = 'screendump_image("'+str(method)+'_targetsite_1.png")\n'
            if line.startswith("screendump_image( PNG2 )"):
                line = 'screendump_image("'+str(method)+'_targetsite_2.png")\n'
            self.new_coot_lines += line

        #=================================================
        # RUN
        #=================================================
        self.xds_dir_model_list = []
        if self.template.split(".")[-1] != "csv":
            os.chdir(self.beamtime_dir)
            aimless_files = []
            for current, subfolders, subfiles in os.walk(self.beamtime_dir):
                for subfile in subfiles:
                    if subfile[0:3] == self.data_name[0:3] and subfile[-3:] == self.data_name[-3:]:
                        aimless_files.append(os.path.join(os.path.abspath(current), subfile))

            for file in aimless_files:
                self.logger.debug("Found data files")
                self.logger.debug(file)
                xds_dir_model = {}
                xds_dir = os.path.dirname(file)
                xds_dir_model["xds_dir"] = xds_dir
                xds_dir_model["model"] = self.template

                print("flag_skip_processed_data  :  "+str(self.flag_skip_processed_data))

                if str(self.flag_skip_processed_data) == "False":
                    self.xds_dir_model_list.append(xds_dir_model)
                elif str(self.flag_skip_processed_data) == "True":
                    peints_dirs = glob.glob(os.path.dirname(xds_dir)+"/peints_*")
                    if len(peints_dirs)>0:
                        pass
                    else:
                        self.xds_dir_model_list.append(xds_dir_model)


        else:
            for raw in self.csv_dict_list:
                xds_dir_model = {}
                beamtime_dir_name = os.path.basename(self.beamtime_dir)
                premo_dir = os.path.join(self.beamtime_dir, raw["Protein"], beamtime_dir_name, raw["ContainerID"],
                                       raw["Directory"], "premo")

                print("MAKING SELF.CSV_DICT_LIST")
                print(premo_dir)

                for current, subfolders, subfiles in os.walk(premo_dir):
                    for subfile in subfiles:
                        print(current)
                        print(subfile)
                        if subfile == self.data_name:
                            xds_dir = current
                            xds_dir_model["xds_dir"] = xds_dir
                            xds_dir_model["model"] = raw["Model"]
                            if not xds_dir.split("/")[-1][0:7] == "peints_":
                                if self.flag_overwrite == "False":
                                    if not os.path.exists(
                                            os.path.dirname(xds_dir) + "/peints_" + os.path.basename(xds_dir)):
                                        self.xds_dir_model_list.append(xds_dir_model)
                                    else:
                                        pass
                                else:
                                    self.xds_dir_model_list.append(xds_dir_model)
                            else:
                                pass

        import mypool
        p = mypool.MyPool(self.cpu_num)
        p.map(self.bash_peints, self.xds_dir_model_list)

    def targetsite_analysis(self, targetsite):
        if self.targetsite == "":
            targetsite_for_coot = ""
        else:
            if " " in targetsite:
                self.targetsite = targetsite.replace(" ", "")

            if not "_" in targetsite:
                self.logger.debug("targetsite    :   single\n")
                chain_1 = targetsite.split("/")[0]
                resi_1  = targetsite.split("/")[1]
                atom_1  = targetsite.split("/")[2]
                targetsite_for_coot = "'"+str(chain_1)+"',"+str(resi_1)+",'"+str(atom_1)+"'"

            else:
                self.logger.debug("targetsite    :   pair\n")
                targetsite_for_coot = "'U',0,'U'"
        return targetsite_for_coot


    def bash_peints(self, xds_dir_model):
        xds_dir = xds_dir_model["xds_dir"]
        model = xds_dir_model["model"]

        os.chdir(xds_dir)

        main.Run(self.logger,
                 self.version,
                 self.progdir,
                 xds_dir,
                 self.data_name,
                 self.new_coot_lines,
                 self.targetsite,
                 self.targetsite_for_coot,
                 model,
                 self.sequence,
                 self.beamtime_dir,
                 self.spacegroup,
                 self.cutoff_ios,
                 self.flag_overwrite,
                 self.flag_molrep,
                 self.flag_coot,
                 self.flag_phenix,
                 self.flag_phaser,
                 self.flag_pr,
                 self.flag_sa,
                 self.flag_water,
                 self.cpu_num,
                 self.xds_dir_model_list,
                 self.run_date)

        os.chdir(self.beamtime_dir)
        peints_result.result(self.logger, self.progdir,
                             self.run_date, self.version,
                             self.beamtime_dir, self.template,
                             self.sequence, self.targetsite,
                             self.spacegroup,
                             self.cutoff_ios,
                             self.flag_phaser, self.flag_pr)


#=================================================
# main function
#=================================================
if __name__  == '__main__':
    import sys
    import peints_argparse
    args = sys.argv
    input_parser = peints_argparse.peints_argparse(args)
    input_file = input_parser.input_file
    workdir = os.getcwd()

    Manage(input_file)