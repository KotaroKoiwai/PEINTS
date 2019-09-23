# -*- coding: utf-8 -*-
#!/usr/bin/python3

import Tkinter as tk
import os
import tkSimpleDialog as sd
import webbrowser
from Tkinter import *
from tkFileDialog import *



#=================================================
# peints_GUI
#=================================================


class main_window(tk.Frame):

    def __init__(self, master):

        args = sys.argv
        self.progdir = os.path.dirname(os.path.abspath(args[0]))
        self.workdir = os.getcwd()
        self.path_name = ""
        self.template = ""
        self.sequence = ""
        self.targetsite = ""

        tk.Frame.__init__(self, master)
        self.label_top = tk.Label(master,text="MR for ligand screening")
        self.label_top.pack()

        frame = tk.Frame(master)
        frame.pack()

        self.template = tk.Button(frame, text="Template", width=35, command=self.askstr_tmpl)
        self.template.pack()
        self.label_temp = tk.Label(master, text="No template indicated.")
        self.label_temp.pack(anchor="w", padx=20)

        self.sequence = tk.Button(frame, text="Sequence", width=35, command=self.askstr_seq)
        self.sequence.pack()
        self.label_seq = tk.Label(master, text="No sequence indicated.")
        self.label_seq.pack(anchor="w", padx=20)

        self.project = tk.Button(frame, text="Beamtime directory", width=35, command=self.askstr_prjct)
        self.project.pack()
        self.label_projctdir = tk.Label(master, text="Select a beamtime directory.")
        self.label_projctdir.pack(anchor="w", padx=20)

        self.activesite = tk.Button(frame,text="Target site", width=35, command=self.askstr_activesite)
        self.activesite.pack()
        self.label_actsite = tk.Label(master, text="Input active site")
        self.label_actsite.pack(anchor="w", padx=20)
        
        self.spacegroup = tk.Entry(frame,text="Space group", width=37, justify="center")
        self.spacegroup.pack()
        self.spacegroup.insert(0, "Spacegroup_suggested_by_POINTLESS")
        self.label_spacegroup = tk.Label(master, text="Space group  :  As suggested by PReMo.")
        self.label_spacegroup.pack(anchor="w", padx=20)

#        self.data_name = tk.Entry(frame,text="Data_name", width=36, justify="center")
#        self.data_name.pack()
#        self.data_name.insert(0, "Data name  :  aimless.mtz")
#        self.label_data_name = tk.Label(master, text="Data name  :  aimless.mtz (default)")
#        self.label_data_name.pack(anchor="w", padx=20)

        self.data_name = "aimless.mtz"
        data_name_frame = LabelFrame(frame, text="Data name")
        self.data_name_var = IntVar()
        self.data_name_var.set(0)
        self.data_name_1 = tk.Radiobutton(data_name_frame,
                                          text="aimless.mtz",
                                          variable = self.data_name_var,
                                          value = 0,
                                          width = 16,
                                          justify = "left",
                                          command = self.change_state)
        self.data_name_2 = tk.Radiobutton(data_name_frame,
                                          text="XDS_ASCII.HKL",
                                          variable = self.data_name_var,
                                          value = 1,
                                          width = 16,
                                          justify = "left",
                                          command = self.change_state)
        self.data_name_1.pack(side = "left", padx = 10)
        self.data_name_2.pack(side = "right", padx = 10)
        data_name_frame.pack()


        #=================================================
        # entrybox for number of processors
        #=================================================
        #        self.label5 = tk.Label(frame,text="Input number of CPU")
        #self.label5.pack(anchor="w", padx=20)
        #self.EditBox = tk.Entry(frame)
        #self.EditBox.insert(tk.END,"number of CPU")
        #self.EditBox.pack(anchor="w", padx=10)


        self.peints = tk.Button(frame, text="RUN PEINTS", command=self.run_peints)
        self.peints.pack(fill="both", side="left")
        self.quit = tk.Button(frame, text="QUIT", fg="red", command=quit)
        self.quit.pack(fill="both", side="right")

        self.result = tk.Button(frame, text="View result", command=self.view_result)
        self.result.pack(fill="both", side="bottom")


        #=================================================
        # checkbox for MR by molrep
        #=================================================
        self.flag_molrep = BooleanVar()
        self.flag_molrep.set(True)
        v = IntVar()
        v.set(0)
        buttons = []
        def cmd_molrep():
            if self.flag_molrep.get():
                print "Perform MR by MOLREP"
            else:
                print "Don't perform MR by MOLREP, only REFMAC5"
        molrep_run = Checkbutton(root, text = "MR", variable = self.flag_molrep, command = cmd_molrep)
        f_coot = LabelFrame(root, labelwidget = molrep_run)
        molrep_run.pack(side="left")
        buttons.append(molrep_run)
        f_coot.pack(side="left")


        #=================================================
        # checkbox for image capture by coot
        #=================================================
        self.flag_coot = BooleanVar()
        self.flag_coot.set(True)
        v = IntVar()
        v.set(0)
        buttons = []
        def cmd_coot():
            if self.flag_coot.get():
                print "image captured by coot"
            else:
                print "Don't image captured by coot"
    
        image_capture = Checkbutton(root, text = "image capture by coot", variable = self.flag_coot, command = cmd_coot)
        f_coot = LabelFrame(root, labelwidget = image_capture)
        image_capture.pack(side="left")
        buttons.append(image_capture)
        f_coot.pack(side="left")


        #=================================================
        # checkbox for phenix.refine
        #=================================================
        self.flag_pr = BooleanVar()
        self.flag_pr.set(False)
        v = IntVar()
        v.set(0)
        buttons = []
        def change_state():
            if self.flag_pr.get():
                new_state = 'normal'
                print "phenix.refine"
                
            else:
                new_state = 'disabled'
                print "do not phenix.refine"

            for b in buttons:
                b.configure(state = new_state)
        cb = Checkbutton(root, text = 'phenix.refine', variable = self.flag_pr, command = change_state)
        f_phenix = LabelFrame(root, labelwidget = cb)


        self.flag_sa = BooleanVar()
        self.flag_sa.set(False)
        def cmd_sa():
            if self.flag_sa.get():
                print "simulated annealing"
                print self.flag_sa.get()
            else:
                print "Don't simulated annealing"
                print self.flag_sa.get()

        sa = Checkbutton(f_phenix, text = "simulated annealing", variable = self.flag_sa, state = 'disabled', command = cmd_sa)
        sa.pack(side = "left")
        buttons.append(sa)


        self.flag_water = BooleanVar()
        self.flag_water.set(False)
        def cmd_water():
            if self.flag_water.get():
                print "input water molecules"
                print self.flag_water.get()
            
            else:
                print "Don't input water molecules"
                print self.flag_water.get()

        water = Checkbutton(f_phenix, text = "input water", variable = self.flag_water, state = 'disabled', command = cmd_water)
        water.pack(side = "left")
        buttons.append(water)
        f_phenix.pack(padx = 5, pady = 5)




        #=================================================
        # commands for bottuns
        #=================================================
        
    def askstr_tmpl(self):
        self.template = askopenfilename(filetypes = [('Image Files', ('.pdb', '.cif')),
                                            ('PDB Files', '.pdb'),
                                            ('CIF Files', '.cif')],
                               initialdir = self.path_name)
        self.set1(os.path.basename(self.template))
    
    def set1(self, str1):
        self.label_temp.config(text="Template  :  " + str(str1))

    def askstr_seq(self):
        self.sequence = askopenfilename(filetypes = [('Seq Files', ('.seq', '.pir', '.txt')),
                                            ('Seq Files', '.seq'),
                                            ('Pir Files', '.pir'),
                                            ('Txt Files', '.txt')],
                               initialdir = self.path_name)
        self.set2(os.path.basename(self.sequence))
        return self.sequence
    
    def set2(self, str2):
        self.label_seq.config(text="Sequence  :  " + str(str2))

    def askstr_prjct(self):
        self.project_dir = askdirectory(initialdir = self.path_name)
        self.set3(self.project_dir)

    def set3(self, str3):
        self.label_projctdir.config(text="Beamtime directory  :  ... " + str(str3[-30:]))
    
    def askstr_activesite(self):
        self.targetsite = sd.askstring("input your target site",
                                       'chainID/residue No./atom \n'
                                       'e.g.1)      A/110/CZ\n'
                                       'e.g.2)      A/110/CZ_A/100/CA',
                                       initialvalue='A/110/CZ')
        self.set4(self.targetsite)
    def set4(self, str4):
        self.label_actsite.config(text="Target site is " + str(str4))

    def change_state(self):
        checked = self.data_name_var.get()
        if checked == 0:
            self.data_name_2.configure(state = "disabled")
            self.data_name = "aimless.mtz"
        elif checked == 1:
            self.data_name_1.configure(state = "disabled")
            self.data_name = "XDS_ASCII.HKL"


    def run_peints(self):
        print("Run peints!")
        import manage
        manage.Manage(self.progdir,
                 self.workdir,
                 self.template, 
                 self.sequence, 
                 self.project_dir, 
                 self.targetsite,
                 self.spacegroup.get(),
                 self.data_name,
                 str(self.flag_molrep.get()),
                 str(self.flag_coot.get()),
                 str(self.flag_pr.get()),
                 str(self.flag_water.get()),
                 str(self.flag_sa.get())
                 )
        os.chdir(self.workdir)


    def view_result(self):
        browser = webbrowser.get('"/Applications/Firefox.app/Contents/MacOS/firefox" %s')
        result = self.project_dir + "/" + "peints_result.html"
        browser.open(result)
        browser.close()



#=================================================
# main function
#=================================================
if __name__  == '__main__':
    root = Tk()
    root.title(u'peints')
    mw = main_window(root)
    root.mainloop();
    raw_input()

    def quit():
        root.quit()
