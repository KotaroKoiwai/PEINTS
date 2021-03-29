# -*- coding: utf-8 -*-
#!/usr/bin/python3

import Tkinter as tk
import os
import csv
import tkSimpleDialog as sd
import webbrowser
from Tkinter import *
from tkFileDialog import *



#=================================================
# PEINTS_GUI
#=================================================


class main_window(tk.Frame):

    def __init__(self, master):

        args = sys.argv
        self.progdir = os.path.dirname(os.path.abspath(args[0]))
        self.BT_dir = os.getcwd()
        self.path_name = ""
        self.template = ""
        self.sequence = ""
        self.targetsite = ""
        self.cutoff_ios = "2.0"
        self.flag_molrep = True
        self.flag_coot= True
        self.flag_overwrite = True
        self.flag_pr= False
        self.flag_water= False
        self.flag_sa= False
        self.flag_temp_push = 0
        self.flag_seq_push = 0
        self.flag_prgdir_push = 0

        self.read_prerun()

        tk.Frame.__init__(self, master)
        frame = tk.Frame(master)
        frame.pack()

        self.template_btn = tk.Button(frame, text="Template", width=35,height=2, command=self.askstr_tmpl)
        self.template_btn.pack()
        self.label_temp = tk.Label(master, text="No template indicated.")
        self.label_temp.pack(anchor="w", padx=20)

        self.seq_btn = tk.Button(frame, text="Sequence", width=35, height=2, command=self.askstr_seq)
        self.seq_btn.pack()
        self.label_seq = tk.Label(master, text="No sequence indicated.")
        self.label_seq.pack(anchor="w", padx=20)

        self.BT_dir_btn = tk.Button(frame, text="Beamtime directory", width=35, height=2, command=self.askstr_bt_dir)
        self.BT_dir_btn.pack()
        self.label_bt_dir = tk.Label(master, text="Select a beamtime directory.")
        self.label_bt_dir.pack(anchor="w", padx=20)

        self.act_site_btn = tk.Button(frame,text="Target site", width=35, height=2, command=self.askstr_activesite)
        self.act_site_btn.pack()
        self.label_actsite = tk.Label(master, text="Input active site")
        self.label_actsite.pack(anchor="w", padx=20)
        
        self.sg_entry = tk.Entry(frame,text="Space group", width=34, justify="center")
        self.sg_entry.pack()
        self.sg_entry.insert(0, "Spacegroup_suggested_by_POINTLESS")
        self.label_spacegroup = tk.Label(master, text="Space group  :  As suggested by PReMo.")
        self.label_spacegroup.pack(anchor="w", padx=20)

        self.cutoff_ios_btn = tk.Button(frame,text="Cut-off I/sigma(I)", width=35, height=2, command=self.askstr_cutoff)
        self.cutoff_ios_btn.pack()
        self.label_cutoff_ios = tk.Label(master, text="Cut-off I/sigma(I)  :  2.0")
        self.label_cutoff_ios.pack(anchor="w", padx=20)

        self.data_name = "XDS_ASCII.HKL"
        data_name_frame = LabelFrame(frame, text="Data name")
        self.data_name_var = IntVar()
        self.data_name_var.set(1)
        self.data_name_1 = tk.Radiobutton(data_name_frame,
                                          text="aimless.mtz",
                                          variable=self.data_name_var,
                                          value=0,
                                          width=16,
                                          height=2,
                                          justify="left",
                                          command=self.change_state)
        self.data_name_2 = tk.Radiobutton(data_name_frame,
                                          text="XDS_ASCII.HKL",
                                          variable=self.data_name_var,
                                          value=1,
                                          width=16,
                                          height=2,
                                          justify="left",
                                          command=self.change_state)
        self.data_name_1.pack(side = "left", padx=10)
        self.data_name_2.pack(side = "right", padx=10)
        data_name_frame.pack()


        #=================================================
        # entrybox for number of processors
        #=================================================
        #        self.label5 = tk.Label(frame,text="Input number of CPU")
        #self.label5.pack(anchor="w", padx=20)
        #self.EditBox = tk.Entry(frame)
        #self.EditBox.insert(tk.END,"number of CPU")
        #self.EditBox.pack(anchor="w", padx=10)


        self.run_btn = tk.Button(frame, text=" RUN PEINTS ", height=2, command=self.run_peints, fg="green")
        self.run_btn.pack(fill="both", side="left")
        self.quit_btn = tk.Button(frame, text=" QUIT ", command=quit)
        self.quit_btn.pack(fill="both", side="right")
        self.result_btn = tk.Button(frame, text="View result", command=self.view_result)
        self.result_btn.pack(fill="both", side="right")
        self.prep_dir_btn = tk.Button(frame, text="Prep directories", fg="blue", command=self.prep_dir)
        self.prep_dir_btn.pack(fill="both", side="right")

        #=================================================
        # checkbox for MR by MOLREP
        #=================================================
        self.flag_molrep_blv = BooleanVar()
        self.flag_molrep_blv.set(True)
        v = IntVar()
        v.set(0)
        buttons = []
        def cmd_molrep():
            self.flag_molrep = self.flag_molrep_blv.get()
            if self.flag_molrep:
                print("Perform MR by MOLREP")
            else:
                print("No MR by MOLREP, only REFMAC5")
        molrep_run_cbtn = Checkbutton(root, text="MR", variable=self.flag_molrep_blv, command=cmd_molrep)
        option_frame = LabelFrame(root, labelwidget=molrep_run_cbtn)
        molrep_run_cbtn.pack(side="left")
        buttons.append(molrep_run_cbtn)
        option_frame.pack(side="left")


        #=================================================
        # checkbox for image capture by coot
        #=================================================
        self.flag_coot_blv = BooleanVar()
        self.flag_coot_blv.set(True)
        v = IntVar()
        v.set(0)
        buttons = []
        def cmd_coot():
            self.flag_coot = self.flag_coot_blv.get()
            if self.flag_coot:
                print("PEINTS will capture images with coot")
            else:
                print("PEINTS will NOT capture images with coot")
    
        image_capture_cbtn = Checkbutton(root,
                                         text="image capture by coot",
                                         variable=self.flag_coot_blv,
                                         command=cmd_coot)
        option_frame = LabelFrame(root, labelwidget=image_capture_cbtn)
        image_capture_cbtn.pack(side="left")
        buttons.append(image_capture_cbtn)
        option_frame.pack(side="left")


        #=================================================
        # checkbox for overwrite
        #=================================================
        self.flag_overwrite_blv = BooleanVar()
        self.flag_overwrite_blv.set(True)
        v = IntVar()
        v.set(0)
        buttons = []
        def cmd_overwrite():
            self.flag_overwrite = self.flag_overwrite_blv.get()
            if self.flag_overwrite:
                print("PEINTS overwrites output files")
            else:
                print("PEINTS does NOT overwrite output files")

        overwrite_cbtn = Checkbutton(root,
                                     text="overwrite",
                                     variable=self.flag_overwrite_blv,
                                     command=cmd_overwrite)
        option_frame = LabelFrame(root,
                                  labelwidget=overwrite_cbtn)
        overwrite_cbtn.pack(side="left")
        buttons.append(overwrite_cbtn)
        option_frame.pack(side="left")



        #=================================================
        # checkbox for phenix.refine
        #=================================================
        self.flag_pr_blv = BooleanVar()
        self.flag_pr_blv.set(False)
        v = IntVar()
        v.set(0)
        buttons = []
        def change_state():
            self.flag_pr = self.flag_pr_blv.get()
            if self.flag_pr:
                new_state = 'normal'
                print("PEINTS will perform phenix.refine")
            else:
                new_state = 'disabled'
                print("PEINTS will NOT perform phenix.refine")

            for b in buttons:
                b.configure(state=new_state)
        phenix_cb = Checkbutton(root,
                         text='phenix.refine',
                         variable=self.flag_pr_blv,
                         command=change_state)
        f_phenix = LabelFrame(root, labelwidget=phenix_cb)


        self.flag_sa_blv = BooleanVar()
        self.flag_sa_blv.set(False)
        def cmd_sa():
            self.flag_sa = self.flag_sa_blv.get()
            if self.flag_sa:
                print("PEINTS-phenix.refine with simulated annealing")
                print(self.flag_sa)
            else:
                print("PEINTS-phenix.refine without simulated annealing")
                print(self.flag_sa)

        sa_cbtn = Checkbutton(f_phenix,
                              text="simulated annealing",
                              variable=self.flag_sa_blv,
                              state='disabled',
                              command=cmd_sa)
        sa_cbtn.pack(side="left")
        buttons.append(sa_cbtn)


        self.flag_water_blv = BooleanVar()
        self.flag_water_blv.set(False)
        def cmd_water():
            self.flag_water = self.flag_water_blv.get()
            if self.flag_water:
                print("PEINTS-phenix.refine will put water molecules")
                print(self.flag_water)
            
            else:
                print("PEINTS-phenix.refine will NOT put water molecules")
                print(self.flag_water)

        water_cbtn = Checkbutton(f_phenix,
                                 text="input water",
                                 variable=self.flag_water_blv,
                                 state='disabled',
                                 command=cmd_water)
        water_cbtn.pack(side="left")
        buttons.append(water_cbtn)
        f_phenix.pack(padx = 5, pady = 5)


        #=================================================
        # commands for bottuns
        #=================================================
        
    def askstr_tmpl(self):
        self.flag_temp_push = 1
        self.template = askopenfilename(filetypes = [('Image Files', ('.pdb', '.cif', '.csv')),
                                            ('PDB Files', '.pdb'),
                                            ('CIF Files', '.cif'),
                                            ('CSV Files', '.csv')],
                               initialdir = os.path.dirname(self.template))
        self.set_tmpl_label(os.path.basename(self.template))
    
    def set_tmpl_label(self, template):
        self.label_temp.config(text="Template  :  " + str(template))

    def askstr_seq(self):
        self.flag_seq_push = 1
        self.sequence = askopenfilename(filetypes = [('Seq Files', ('.seq', '.pir', '.txt')),
                                            ('Seq Files', '.seq'),
                                            ('Pir Files', '.pir'),
                                            ('Txt Files', '.txt')],
                               initialdir = os.path.dirname(self.sequence))
        self.set_seq_label(os.path.basename(self.sequence))
    
    def set_seq_label(self, seq):
        self.label_seq.config(text="Sequence  :  " + str(seq))

    def askstr_bt_dir(self):
        self.flag_prgdir_push = 1
        self.BT_dir = askdirectory(initialdir=self.BT_dir)
        self.set_bt_dir_label(self.BT_dir)

    def set_bt_dir_label(self, BT_dir):
        self.label_bt_dir.config(text="Beamtime directory  :  ... " + str(BT_dir[-30:]))
    
    def askstr_activesite(self):
        self.targetsite = sd.askstring("input your target site",
                                       'chainID/residue No./atom \n'
                                       'e.g.1)      A/110/CZ\n'
                                       'e.g.2)      A/110/CZ_A/100/CA',
                                       initialvalue='A/110/CZ')
        self.set_targetsite_label(self.targetsite)
    def set_targetsite_label(self, targetsite):
        self.label_actsite.config(text="Target site is " + str(targetsite))

    def askstr_cutoff(self):
        self.cutoff_ios = sd.askstring("Input I/sigma(I) for data cut-off",
                                       'default = 2.0',
                                       initialvalue='2.0')
        self.set_cutoff_label(self.cutoff_ios)
    def set_cutoff_label(self, cutoff_ios):
        self.label_cutoff_ios.config(text="Cut-off I/sigma(I)  :  " + str(cutoff_ios))

    def change_state(self):
        checked = self.data_name_var.get()
        if checked == 0:
            self.data_name_2.configure(state="active")
            self.data_name = "aimless.mtz"
        elif checked == 1:
            self.data_name_1.configure(state="active")
            self.data_name = "XDS_ASCII.HKL"


    def run_peints(self):
        if self.flag_temp_push == 1 and self.flag_prgdir_push == 1:
            if self.flag_seq_push == 0:
                self.sequence = ""

            self.spacegroup = self.sg_entry.get()
            print("Run PEINTS!")

            self.update_prerun_csv()

            import manage
            manage.Manage(self.progdir,
                          self.BT_dir,
                          self.template,
                          self.sequence,
                          self.BT_dir,
                          self.targetsite,
                          self.spacegroup,
                          self.data_name,
                          self.cutoff_ios,
                          str(self.flag_molrep),
                          str(self.flag_coot),
                          str(self.flag_overwrite),
                          str(self.flag_pr),
                          str(self.flag_water),
                          str(self.flag_sa)
                          )
            os.chdir(self.BT_dir)
        elif self.flag_temp_push == 0:
            print("Select your template model.")
        elif self.flag_prgdir_push == 0:
            print("Select your beam time directory.")

    def read_prerun(self):
        self.prerun_file = os.path.join(self.progdir, "PRERUN.csv")

        files = os.listdir(self.progdir)
        if self.prerun_file in files:
            csv_file = open(self.prerun_file, "r")
            f = csv.DictReader(csv_file)
            prerun_dict_list = [raw for raw in f]
            prerun_dict = prerun_dict_list[0]
            csv_file.close()
            print(prerun_dict)

            self.template = prerun_dict["template"]
            self.BT_dir = prerun_dict["beamtime_directory"]
            self.sequence = prerun_dict["sequence"]
            self.targetsite = prerun_dict["targetsite"]
            self.cutoff_ios = prerun_dict["cutoff_ios"]
            self.flag_molrep = prerun_dict["flag_molrep"]
            self.flag_coot = prerun_dict["flag_coot"]
            self.flag_overwrite = prerun_dict["flag_overwrite"]
            self.flag_pr= prerun_dict["flag_pr"]
            self.flag_water= prerun_dict["flag_water"]
            self.flag_sa = prerun_dict["flag_sa"]

        else:
            pass

    def update_prerun_csv(self):
        body = "template,beamtime_directory,sequence,targetsite,cutoff_ios," \
               "flag_molrep,flag_coot,flag_overwrite,flag_pr,flag_water,flag_sa\n"
        body += self.template+","
        body += self.BT_dir+","
        body += self.sequence + ","
        body += self.targetsite + ","
        body += self.cutoff_ios + ","
        body += str(self.flag_molrep) + ","
        body += str(self.flag_coot) + ","
        body += str(self.flag_overwrite) + ","
        body += str(self.flag_pr) + ","
        body += str(self.flag_water) + ","
        body += str(self.flag_sa)
        csv_file = open(self.prerun_file, "w")
        csv_file.write(body)
        csv_file.close()
        print("PRERUN FILE UPDATE.")

    def prep_dir(self):

        print("""
        
        ---  Project-based directory-hierarchy  ---
        
        [selected_Beamtime directory]
            |
            +- [Protein directory]
            |   |
            |   +-[peints_tmp directory] 
            |   |
            |   +-[Beamtime directory]
                |    |
                |    +-[Container directory]
                     |   | 
                     |   +-[Crystal directory]
                         |   |
                         |   +-[premo directory]
                             |   |
                             |   +-[fastxds directory]
        """)
        print(self.template)

        if self.template == "":
            print("Select CSV file from Template button.")
        else:
            if self.template.split(".")[-1] != "csv":
                print("Select CSV file from Template button.")
            else:
                csv_file = open(self.template, "r")
                f = csv.DictReader(csv_file)
                csv_dict_list = []
                for raw in f:
                    csv_dict_list.append(raw)
                csv_file.close()

            ###  create protein dirs ###
            for raw in csv_dict_list:
                protein_id = raw["Protein"]
                protein_dir = os.path.join(self.BT_dir, protein_id)
                try:
                    os.makedirs(protein_dir)
                except:
                    pass

            ###  create premo dir-hierarchy ###
                protein_bt_dir = os.path.join(protein_dir, os.path.basename(self.BT_dir))
                container_dir = os.path.join(protein_bt_dir, raw["ContainerID"])
                crystal_dir = os.path.join(container_dir, raw["Directory"])
                premo_dir = os.path.join(crystal_dir, "premo")
                data_dir = os.path.join(premo_dir, "fastxds")

                try:
                    os.makedirs(protein_bt_dir)
                except:
                    pass
                try:
                    os.makedirs(container_dir)
                except:
                    pass
                try:
                    os.makedirs(crystal_dir)
                except:
                    pass
                try:
                    os.makedirs(premo_dir)
                except:
                    pass
                try:
                    os.makedirs(data_dir)
                except:
                    pass

    def view_result(self):
        browser = webbrowser.get('"/Applications/Firefox.app/Contents/MacOS/firefox" %s')
        if self.template != "":
            result = self.BT_dir + "/" + "peints_result.html"
            browser.open(result)
            browser.close()
        else:
            print("Perform PEINTS...")



#=================================================
# main function
#=================================================
if __name__  == '__main__':
    root = Tk()
    root.title(u'PEINTS -MR for ligand screening-')
#    root['bg']="#CCFFCC"
    mw = main_window(root)
    root.mainloop();
    raw_input()

    def quit():
        root.quit()
