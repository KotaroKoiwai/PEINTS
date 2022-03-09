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
        self.initial_param()
        self.read_prerun()

        self.master = master
        tk.Frame.__init__(self, self.master)
        self.frame = tk.Frame(self.master, padx=30, pady=10)
        self.create_gui()


    def create_gui(self):
        self.template_btn = tk.Button(self.frame, text="Template", width=10, height=2, command=self.askstr_tmpl)
        self.template_btn.grid(row=0,column=0)
        self.label_temp = tk.Label(self.frame, text="No template indicated.", padx=5)
        self.label_temp.grid(row=0,column=1,columnspan=3, sticky="w")

        self.seq_btn = tk.Button(self.frame, text="Sequence", width=10, height=2, command=self.askstr_seq)
        self.seq_btn.grid(row=1,column=0)
        self.label_seq = tk.Label(self.frame, text="No sequence indicated.", padx=5)
        self.label_seq.grid(row=1,column=1,columnspan=3, sticky="w")

        self.BT_dir_btn = tk.Button(self.frame, text="Beamtime\ndirectory", width=10, height=2, command=self.askstr_bt_dir)
        self.BT_dir_btn.grid(row=2,column=0)
        self.label_bt_dir = tk.Label(self.frame, text="Select a beamtime directory.", padx=5)
        self.label_bt_dir.grid(row=2,column=1, columnspan=3, sticky="w")

        self.act_site_btn = tk.Button(self.frame, text="Target site", width=10, height=2, command=self.askstr_activesite)
        self.act_site_btn.grid(row=3,column=0)
        self.label_actsite = tk.Label(self.frame, text="Input active site", padx=5)
        self.label_actsite.grid(row=3,column=1, columnspan=3, sticky="w")

        self.sg_btn = tk.Button(self.frame, text="Space\ngroup", width=10, height=2, command=self.askstr_sg)
        self.sg_btn.grid(row=4,column=0)
        self.label_sg = tk.Label(self.frame, text="Space group  :  automatic", padx=5)
        self.label_sg.grid(row=4,column=1, columnspan=3, sticky="w")

        self.cutoff_ios_btn = tk.Button(self.frame, text="Cut-off\nI/sigma(I)", width=10, height=2,
                                        command=self.askstr_cutoff)
        self.cutoff_ios_btn.grid(row=5,column=0)
        self.label_cutoff_ios = tk.Label(self.frame, text="Cut-off I/sigma(I)  :  2.0", padx=5)
        self.label_cutoff_ios.grid(row=5,column=1, columnspan=3, sticky="w")

        self.run_mode = {"overwrite": self.flag_overwrite, "skip": self.flag_skip_processed_data}
        run_mode_frame = LabelFrame(self.frame, text="Run mode")
        self.run_mode_var = IntVar()
        self.run_mode_var.set(0)

        def change_state_run_mode():
            checked = self.run_mode_var.get()
            if checked == 0:
                self.run_mode_process_all_rbtn.configure(state="active")
                self.flag_skip_processed_data = False
            elif checked == 1:
                self.run_mode_skip_processed_rbtn.configure(state="active")
                self.flag_skip_processed_data = True
            self.run_mode["skip"] = self.flag_skip_processed_data

        self.run_mode_process_all_rbtn = tk.Radiobutton(run_mode_frame,
                                                        text="Process all data",
                                                        variable=self.run_mode_var,
                                                        value=0,
                                                        width=16,
                                                        height=2,
                         #                               justify="left",
                                                        command=change_state_run_mode)
        self.run_mode_skip_processed_rbtn = tk.Radiobutton(run_mode_frame,
                                                           text="Skip processed data",
                                                           variable=self.run_mode_var,
                                                           value=1,
                                                           width=16,
                                                           height=2,
                         #                                  justify="left",
                                                           command=change_state_run_mode)

        self.run_mode_process_all_rbtn.grid(row=0, column=0, padx=10)
        self.run_mode_skip_processed_rbtn.grid(row=0, column=1, padx=10)

        self.flag_overwrite_blv = BooleanVar()
        self.flag_overwrite_blv.set(False)
        v = IntVar()
        v.set(0)
        buttons = []

        def cmd_overwrite():
            self.flag_overwrite = self.flag_overwrite_blv.get()
            if self.flag_overwrite:
                print("PEINTS overwrites output files")
            else:
                print("PEINTS does NOT overwrite output files")
            self.run_mode["flag_overwrite"] = self.flag_overwrite

        overwrite_cbtn = Checkbutton(run_mode_frame,
                                     text="overwrite",
                                     variable=self.flag_overwrite_blv,
                                     command=cmd_overwrite)
        overwrite_cbtn.grid(row=1, column=0, columnspan=2)
        run_mode_frame.grid(row=6,column=0,columnspan=4)

        self.data_name = "XDS_ASCII.HKL"
        data_name_frame = LabelFrame(self.frame, text="Data name", width=36)
        self.data_name_var = IntVar()
        self.data_name_var.set(0)

        self.data_name_xds = tk.Radiobutton(data_name_frame,
                                          text="XDS_ASCII.HKL",
                                          variable=self.data_name_var,
                                          value=0,
                                          width=16,
                                          height=2,
                                          justify="left",
                                          command=self.change_state_data)
        self.data_name_aimless = tk.Radiobutton(data_name_frame,
                                          text="aimless.mtz",
                                          variable=self.data_name_var,
                                          value=1,
                                          width=16,
                                          height=2,
                                          justify="left",
                                          command=self.change_state_data)
        self.data_name_xds.pack(side="left", padx=10)
        self.data_name_aimless.pack(side="right", padx=10)
        data_name_frame.grid(row=7,column=0,columnspan=4)

        # =================================================
        # entrybox for number of processors
        # =================================================
        #        self.label5 = tk.Label(frame,text="Input number of CPU")
        # self.label5.pack(anchor="w", padx=20)
        # self.EditBox = tk.Entry(frame)
        # self.EditBox.insert(tk.END,"number of CPU")
        # self.EditBox.pack(anchor="w", padx=10)

        self.run_btn = tk.Button(self.frame, text=" RUN PEINTS ", height=2, width=10, command=self.run_peints, fg="green")
        self.run_btn.grid(row=8,column=0)
        self.quit_btn = tk.Button(self.frame, text=" QUIT ", height=2,command=quit)
        self.quit_btn.grid(row=8,column=1)
        self.result_btn = tk.Button(self.frame, text="View result", height=2,width=10,command=self.view_result)
        self.result_btn.grid(row=8,column=2)
        self.prep_dir_btn = tk.Button(self.frame, text="Prep\ndirectories", height=2,width=10, fg="blue", command=self.prep_dir)
        self.prep_dir_btn.grid(row=8,column=3)

        # =================================================
        # checkbox for MR by MOLREP
        # =================================================
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

        option_frame = LabelFrame(self.frame, text="Options", width=35)
        molrep_run_cbtn = Checkbutton(option_frame, text="MR", variable=self.flag_molrep_blv, command=cmd_molrep)
        molrep_run_cbtn.grid(row=0,column=0)
        buttons.append(molrep_run_cbtn)


        # =================================================
        # checkbox for image capture by coot
        # =================================================
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

        image_capture_cbtn = Checkbutton(option_frame,
                                         text="image capture by coot",
                                         variable=self.flag_coot_blv,
                                         command=cmd_coot)
        #option_frame = LabelFrame(option_frame, labelwidget=image_capture_cbtn)
        image_capture_cbtn.grid(row=0,column=1)
        buttons.append(image_capture_cbtn)
        option_frame.grid(row=9,column=0, columnspan=4, sticky="w,e")

        # =================================================
        # checkbox for PHENIX
        # =================================================
        self.flag_phenix_blv = BooleanVar()
        self.flag_phenix_blv.set(False)
        self.flag_phaser_blv = BooleanVar()
        self.flag_phaser_blv.set(False)
        self.flag_sa_blv = BooleanVar()
        self.flag_sa_blv.set(False)
        self.flag_water_blv = BooleanVar()
        self.flag_water_blv.set(False)


        v = IntVar()
        v.set(0)
        buttons = []

        def phenix_change_state():
            self.flag_phenix = self.flag_phenix_blv.get()
            self.flag_pr = self.flag_phenix_blv.get()
            if self.flag_phenix:
                new_state = 'normal'
                print("PEINTS will use PHENIX")
                self.flag_phaser_blv.set(True)
                self.data_name_xds.configure(state="active")
                self.data_name_var.set(0)
                self.flag_phaser = True
#                self.data_name = "XDS_ASCII.HKL"
            else:
                new_state = 'disabled'
                print("PEINTS will NOT use PHENIX")
                self.flag_phaser_blv.set(False)
                self.flag_sa_blv.set(False)
                self.flag_water_blv.set(False)

            for b in buttons:
                b.configure(state=new_state)

            self.change_state_data()

        phenix_cb = Checkbutton(self.frame,
                                text='PHENIX',
                                variable=self.flag_phenix_blv,
                                command=phenix_change_state)
        phenix_frame = LabelFrame(self.frame, labelwidget=phenix_cb)


        def cmd_phaser():
            self.flag_phaser = self.flag_phaser_blv.get()
            if self.flag_phaser:
                print("MR will be performed with PHASER")
            else:
                print("MR will be performed with MOLREP")

        phaser_cbtn = Checkbutton(phenix_frame,
                              text="PHASER",
                              variable=self.flag_phaser_blv,
                              state='disabled',
                              command=cmd_phaser)
        phaser_cbtn.pack(side="left")
        buttons.append(phaser_cbtn)

        def cmd_sa():
            self.flag_sa = self.flag_sa_blv.get()
            if self.flag_sa:
                print("PEINTS-phenix.refine with simulated annealing")
                print(self.flag_sa)
            else:
                print("PEINTS-phenix.refine without simulated annealing")
                print(self.flag_sa)

        sa_cbtn = Checkbutton(phenix_frame,
                              text="simulated annealing",
                              variable=self.flag_sa_blv,
                              state='disabled',
                              command=cmd_sa)
        sa_cbtn.pack(side="left")
        buttons.append(sa_cbtn)

        def cmd_water():
            self.flag_water = self.flag_water_blv.get()
            if self.flag_water:
                print("PEINTS-phenix.refine will put water molecules")
                print(self.flag_water)

            else:
                print("PEINTS-phenix.refine will NOT put water molecules")
                print(self.flag_water)

        water_cbtn = Checkbutton(phenix_frame,
                                 text="input water",
                                 variable=self.flag_water_blv,
                                 state='disabled',
                                 command=cmd_water)
        water_cbtn.pack(side="left")
        buttons.append(water_cbtn)
        phenix_frame.grid(row=10,column=0,columnspan=4, sticky="w,e")


        self.frame.pack()



        #=================================================
        # commands for buttons
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
                                            ('FASTA Files', '.fasta'),
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

    def askstr_sg(self):
        self.spacegroup = sd.askstring("input spacegroup",
                                       "default=automatic",
                                       initialvalue="automatic")
        self.set_sg_label()
    def set_sg_label(self):
        self.label_sg.config(text="Spacegroup  :  "+self.spacegroup)

    def set_targetsite_label(self, targetsite):
        self.label_actsite.config(text="Target site  :  " + str(targetsite))

    def askstr_cutoff(self):
        self.cutoff_ios = sd.askstring("Input I/sigma(I) for data cut-off",
                                       'default = 2.0',
                                       initialvalue='2.0')
        self.set_cutoff_label(self.cutoff_ios)
    def set_cutoff_label(self, cutoff_ios):
        self.label_cutoff_ios.config(text="Cut-off I/sigma(I)  :  " + str(cutoff_ios))

    def change_state_data(self):
        checked = self.data_name_var.get()
        if checked == 0:
            self.data_name_xds.configure(state="active")
            self.data_name = "XDS_ASCII.HKL"
            print("Data processing from XDS")
        elif checked == 1:
            self.data_name_aimless.configure(state="active")
            self.data_name = "aimless.mtz"
            print("Data processing from AIMLESS")



    def initial_param(self):
        args = sys.argv
        self.progdir = os.path.dirname(os.path.abspath(args[0]))
        self.BT_dir = os.getcwd()
        self.path_name = ""
        self.template = ""
        self.sequence = ""
        self.spacegroup = "automatic"
        self.data_name = "XDS_ASCII.HKL"
        self.targetsite = ""
        self.cutoff_ios = "2.0"
        self.flag_molrep = True
        self.flag_coot = True
        self.flag_skip_processed_data = False
        self.flag_overwrite = False
        self.flag_phenix = False
        self.flag_phaser = False
        self.flag_pr= False
        self.flag_water= False
        self.flag_sa= False
        self.flag_temp_push = 0
        self.flag_seq_push = 0
        self.flag_prgdir_push = 0


    def run_peints(self):
        if self.flag_temp_push == 1 and self.flag_prgdir_push == 1:
            if self.flag_seq_push == 0:
                self.sequence = ""
            self.update_input_csv()

            print("Run PEINTS!")
            import manage
            manage.Manage(self.input_file)

            os.chdir(self.BT_dir)
        elif self.flag_temp_push == 0:
            print("Select your template model.")
        elif self.flag_prgdir_push == 0:
            print("Select your beam time directory.")

    def read_prerun(self):
        self.input_file = os.path.join(self.progdir, "INPUT.csv")

        files = os.listdir(self.progdir)
        if self.input_file in files:
            csv_file = open(self.input_file, "r")
            f = csv.DictReader(csv_file)
            input_dict_list = [raw for raw in f]
            input_dict = input_dict_list[0]
            csv_file.close()
            print(input_dict)

            self.template = input_dict["template"]
            self.BT_dir = input_dict["beamtime_directory"]
            self.sequence = input_dict["sequence"]
            self.spacegroup = input_dict["spacegroup"]
            self.targetsite = input_dict["targetsite"]
            self.cutoff_ios = input_dict["cutoff_ios"]
            self.data_name = input_dict["data_name"]
            self.flag_molrep = input_dict["flag_molrep"]
            self.flag_coot = input_dict["flag_coot"]
            self.flag_skip_processed_data = input_dict["flag_skip_processed_data"]
            self.flag_overwrite = input_dict["flag_overwrite"]
            self.flag_phenix = input_dict["flag_phenix"]
            self.flag_phaser = input_dict["flag_phaser"]
            self.flag_pr= input_dict["flag_pr"]
            self.flag_water= input_dict["flag_water"]
            self.flag_sa = input_dict["flag_sa"]

        else:
            pass

    def update_input_csv(self):
        body = "progdir,template,beamtime_directory,sequence,spacegroup,targetsite,cutoff_ios,data_name," \
               "flag_molrep,flag_coot,flag_skip_processed_data,flag_overwrite," \
               "flag_phenix,flag_phaser,flag_pr,flag_water,flag_sa\n"
        body += self.progdir+","
        body += self.template+","
        body += self.BT_dir+","
        body += self.sequence + ","
        body += self.spacegroup + ","
        body += self.targetsite + ","
        body += self.cutoff_ios + ","
        body += self.data_name + ","
        body += str(self.flag_molrep) + ","
        body += str(self.flag_coot) + ","
        body += str(self.flag_skip_processed_data) + ","
        body += str(self.flag_overwrite) + ","
        body += str(self.flag_phenix) + ","
        body += str(self.flag_phaser) + ","
        body += str(self.flag_pr) + ","
        body += str(self.flag_water) + ","
        body += str(self.flag_sa)
        csv_file = open(self.input_file, "w")
        csv_file.write(body)
        csv_file.close()
        print("INPUT FILE UPDATED.")

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
