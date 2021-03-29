# -*- coding: utf-8 -*-

import glob
import os
import shutil
import datetime
import subprocess
from Bio import PDB
parser = PDB.PDBParser()

import peints_result

class Run():
    def __init__(self, logger, version, progdir, xds_dir, data_name, new_coot_lines, targetsite, targetsite_for_coot,
                 template, sequence, beamtime_dir, spacegroup, cutoff_ios,
                 flag_molrep, flag_coot, flag_pr, flag_sa, flag_water, cpu_num, xds_dirs, run_date):

        self.logger = logger
        self.version = version
        self.progdir = progdir
        self.template = template
        self.sequence = sequence
        self.beamtime_dir = beamtime_dir
        self.spacegroup = spacegroup
        self.cutoff_ios = cutoff_ios
        self.data_name = data_name
        self.new_coot_lines = new_coot_lines
        self.targetsite = targetsite
        self.targetsite_for_coot = targetsite_for_coot
        self.flag_molrep = flag_molrep
        self.flag_coot = flag_coot
        self.flag_pr = flag_pr
        self.flag_water = flag_water
        self.flag_sa = flag_sa
        self.cpu_num = cpu_num
        self.xds_dirs = xds_dirs
        self.run_date = run_date

        self.run(xds_dir)

    def run(self, xds_dir):
        self.logger.debug("\n"
                          "peints "+xds_dir+" started on "+str(datetime.datetime.now())+"\n")
        peints_dir = "../peints_"+os.path.basename(xds_dir)
        try:
            os.makedirs(peints_dir)
        except:
            pass
        os.chdir(peints_dir)
        f = open("peints_coot.py", "w")
        f.write(self.new_coot_lines)
        f.close()

        self.template_name = os.path.basename(self.template)
        if self.template != self.template_name:
            shutil.copy(self.template, self.template_name)

        if os.path.isfile(self.sequence):
            self.sequence_name = os.path.basename(self.sequence)
            if self.sequence != self.sequence_name:
                shutil.copy(self.sequence, self.sequence_name)

        reprocess_flag = self.re_process(self.spacegroup, xds_dir)

        if reprocess_flag == True:
            xds_dir = "."
        else:
            xds_dir = os.path.join("../", os.path.basename(xds_dir))

        cmd = "bash "+ self.progdir+ "/peints.sh " + \
                       xds_dir + " "+ \
                       self.template_name + " " + \
                       str(self.flag_molrep) + " " + \
                       self.sg_aimless
        self.logger.debug("command for peints.sh  :  "+cmd)
        self.logger.debug("peints.sh "+xds_dir+" started on "+str(datetime.datetime.now()))
        p_mr = subprocess.Popen(cmd, shell=True)
        p_mr.wait()
        self.logger.debug(xds_dir+"  :  peints.sh  FINISH     "+str(datetime.datetime.now()))

        output_pdb = "refmac1.pdb"
        output_mtz = "refmac1.mtz"

        files = os.listdir("./")
        if output_pdb in files:
            if self.flag_pr == "True":
                cmd = "phenix.refine refmac1.mtz refmac1.pdb " \
                      "sequence="+self.sequence_name + \
                      " nproc="+str(int(self.cpu_num/len(self.xds_dirs))) + \
                      " output.prefix=phenix" + \
                      " simulated_annealing=" + str(self.flag_sa) + \
                      " ordered_solvent=" + str(self.flag_water)
                self.logger.debug("phenix.refine "+xds_dir+" started on "+str(datetime.datetime.now()))
                p_pr = subprocess.Popen(cmd, shell=True)
                p_pr.wait()
                self.logger.debug(xds_dir+"  :  phenix.refine  FINISH     "+str(datetime.datetime.now()))

                output_pdb = "phenix_001.pdb"
                output_mtz = "phenix_001.mtz"

            if self.flag_coot == "True":
                if self.targetsite_for_coot == "'U',0,'U'":
                    output_pdb_ed = self.put_pseudoatom(output_pdb)
                else:
                    output_pdb_ed = output_pdb

                cmd = "coot "+output_pdb_ed+" "+output_mtz+" --script peints_coot.py"
                self.logger.debug("image capture "+xds_dir+" started on "+str(datetime.datetime.now()))
                p_coot = subprocess.Popen(cmd, shell=True)
                p_coot.wait()
                self.logger.debug(xds_dir+"  :  image capture  FINISH     "+str(datetime.datetime.now()))

        else:
            pass

        os.chdir(self.beamtime_dir)
        peints_result.result(self.logger, self.progdir,
                             self.run_date, self.version,
                             self.beamtime_dir, self.template,
                             self.sequence, self.targetsite,
                             self.spacegroup,
                             self.cutoff_ios, self.flag_pr)

    def re_process(self, spacegroup, xds_dir):
        reprocess_flag = False
        if self.data_name != "aimless.mtz":
            if spacegroup == "Spacegroup_suggested_by_POINTLESS":
                spacegroup = "none"
            elif spacegroup != "Spacegroup_suggested_by_POINTLESS":
                files = os.listdir(os.path.join("../", os.path.basename(xds_dir)))
                self.logger.debug(files)
            reprocess_flag = self.pointless_aimless(spacegroup, xds_dir)

        else:
            if spacegroup == "Spacegroup_suggested_by_POINTLESS":
                self.logger.debug(xds_dir+"   :   PEINTS doesn't re_process by POINTLESS")
            elif spacegroup != "Spacegroup_suggested_by_POINTLESS":
                files = os.listdir(os.path.join("../", os.path.basename(xds_dir)))
                self.logger.debug(files)
                if not os.path.join("pointless.log") in files:
                    self.logger.debug(xds_dir+"   :   pointless.log was not found")
                else:
                    f = open(os.path.join("../", os.path.basename(xds_dir), "pointless.log"), "r")
                    lines = f.readlines()
                    f.close()
                    spacegroup_by_premo = ""
                    for line in lines:
                        if line.startswith(" * Space group ="):
                            spacegroup_by_premo = line.split("'")[1].replace(" ", "")
                            self.logger.debug(xds_dir+" spacegroup_by_PReMo  :  "+str(spacegroup_by_premo))
                            break

                    if spacegroup == spacegroup_by_premo:
                        self.logger.debug(xds_dir+" input spacegroup was identical to spacegroup by PReMo")
                    else:
                        reprocess_flag = self.pointless_aimless(spacegroup, xds_dir)

        return reprocess_flag


    def pointless_aimless(self, spacegroup, xds_dir):
        self.logger.debug("Re-processing by pointless and aimless")

        if spacegroup == "none":
            sg_line = ""
        else:
            sg_line = "spacegroup "+spacegroup+"\n"

        cmd = "pointless hklin "+ os.path.join("../", os.path.basename(xds_dir), "XDS_ASCII.HKL") + \
                        " hklout pointless.mtz <<eof | tee pointless.log\n" + \
                        sg_line + \
                        "END\n" \
                        "eof\n"
        self.logger.debug("command for pointless  :  "+cmd)
        p_pa = subprocess.Popen(cmd, shell=True)
        p_pa.wait()

        cmd = "aimless hklin pointless.mtz hklout aimless.mtz <<eof | tee aimless.log.1\n" \
                        "onlymerge\n" \
                        "analysis isigminimum "+str(self.cutoff_ios)+"\n" \
                        "spacegroup "+spacegroup+"\n" \
                        "END\n" \
                        "eof\n"
        self.logger.debug("command for aimless  :  "+cmd)
        p_pa = subprocess.Popen(cmd, shell=True)
        p_pa.wait()

        maxreso = "10"
        f = open("aimless.log.1", "r")
        lines = f.readlines()
        f.close()
        value = 0
        for line in lines:
            if line.startswith("Estimates of resolution limits: overall"):
                value = 1
            if value == 1 and line.startswith("   from Mn(I/sd) >  "+str('{:.02f}'.format(float(self.cutoff_ios)))):
                maxreso = str(line.split()[-1])[:-1]
                value = 2

        cmd = "aimless hklin pointless.mtz hklout aimless.mtz <<eof | tee aimless.log\n" \
              "onlymerge\n" \
              "RESO "+maxreso + "\n" \
              "spacegroup "+spacegroup+"\n" \
              "END\n" \
              "eof\n"
        self.logger.debug("command for aimless  :  "+cmd)
        p_pa = subprocess.Popen(cmd, shell=True)
        p_pa.wait()

        if spacegroup == "none":
            f = open("aimless.log", "r")
            lines = f.readlines()
            f.close()
            for line in lines:
                if line.startswith("Space group"):
                    sg_line_aimless = line.split()[2:]
            self.sg_aimless = ""
            for sg_compo in sg_line_aimless:
                self.sg_aimless += sg_compo

        elif spacegroup != "Spacegroup_suggested_by_POINTLESS":
            self.sg_aimless = spacegroup

        reprocess_flag = True
        return reprocess_flag


    def put_pseudoatom(self, output_pdb):
        target_1 = self.targetsite.split("_")[0]
        target_2 = self.targetsite.split("_")[1]

        chain_1 = target_1.split("/")[0]
        resi_1  = target_1.split("/")[1]
        atom_1  = target_1.split("/")[2]

        chain_2 = target_2.split("/")[0]
        resi_2  = target_2.split("/")[1]
        atom_2  = target_2.split("/")[2]

        structure = parser.get_structure("X", output_pdb)
        model = structure[0]
        chain1   = model[chain_1]
        chain2   = model[str(chain_2)]
        residue1 = chain1[int(resi_1)]
        residue2 = chain2[int(resi_2)]
        coord_atom_1 = residue1[str(atom_1)].get_coord()
        coord_atom_2 = residue2[str(atom_2)].get_coord()

        self.logger.debug("Coordinate targetsite_1  :  " + str(coord_atom_1))
        self.logger.debug("Coordinate targetsite_2  :  " + str(coord_atom_2))

        middle = (coord_atom_1 + coord_atom_2)/2
        self.logger.debug("Coodinate middle_point  :  "+str(middle))

        model = structure.get_list()
        chains = model[0].get_list()
        residues = chains[-1].get_list()
        atoms = residues[-1].get_list()
        last_atom_num = atoms[-1].get_serial_number()

        coord = ""
        for num in middle:
            space = ""
            if num > 0:
                if num > 1000:
                    space = ""
                elif num > 100 and num < 1000:
                    space = " "
                elif num > 10 and num < 100:
                    space = "  "
                elif num > 0 and num < 10:
                    space = "   "
            elif num < 0:
                if num < -1000:
                    space = ""
                elif num < -100 and num > -1000:
                    space = ""
                elif num < -10 and num > -100:
                    space = " "
                elif num < 0 and num > -10:
                    space = "  "
            coord += space + str(round(num, 3))

        space = ""
        if last_atom_num > 0 and last_atom_num < 100:
            space = "  "
        elif last_atom_num > 99 and last_atom_num < 1000:
            space = " "
        new_atom_line = "HETATM "+space+str(int(last_atom_num)+1)+"  U   UNK U   0    "+coord+"  0.00  0.00           U \n"

        f = open(output_pdb, "r")
        lines = f.readlines()
        f.close()

        new_line = ""
        for line in lines:
            if line.startswith("END"):
                line = ""
            new_line += line
        new_line += new_atom_line + "END\n"

        output_pdb_ed = os.path.join(output_pdb.split(".")[0]+"_ed.pdb")
        f = open(output_pdb_ed, "w")
        f.write(new_line)
        f.close()

        return output_pdb_ed
