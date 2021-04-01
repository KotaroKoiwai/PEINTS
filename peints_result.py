# -*- coding: utf-8 -*-
import sys, re, os, glob, string
import cgitb
cgitb.enable()


def result(logger, progdir, run_date, version, beamtime_dir, template, sequence, targetsite, spacegroup, cutoff_ios, flag_pr):
    #=========================================
    # create HTML header & table_index
    #=========================================

    html_body = \
    "<html>" \
    "<script type='text/javascript' src='file://" + progdir + "/css/d3.v5.min.js'></script>\n" \
    "<LINK rel='stylesheet' type='text/css' href='file://" + progdir + "/css/style.css'>\n" \
    "<body leftmargin='50'>\n" \
    "<TITLE>Results of PEINTS</TITLE>\n" \
    "<H1>Results of PEINTS</H1>\n" \
    "<H2 font size='10'>Input parameters</H2>\n" \
    "Run date    :     "+run_date+"<br>\n" \
    "PEINTS ver. :     "+version+"<br>\n" \
    "Project directory:     "+beamtime_dir+"<br>\n" \
    "Template PDB:     "+template+"<br>\n" \
    "Sequence    :     "+sequence+"<br>\n" \
    "Target site :     "+targetsite+"<br>\n" \
    "Space group :     "+spacegroup+"<br>\n" \
    "Data_cut-off:     "+cutoff_ios+"<br>\n" \
    "<br>\n" \
    "<table border='1' style='background-color'><caption class=g2-2le>RESULTS</caption>\n" \
    "<tr>\n" \
    "<th>Unipuck</th>" \
    "<th>Crystal</th>" \
    "<th>Data</th>" \
    "<th>Space group</th>" \
    "<th>Unit cell</th>" \
    "<th>Resolution high</th>" \
    "<th>Resolution low</th>" \
    "<th>Data process</th>" \
    "<th>Rwork</th>" \
    "<th>Rfree</th>" \
    "<th>Overall</th>" \
    "<th>Pocket_1</th>" \
    "<th>Pocket_2</th>" \
    "</tr>\n"


    #=========================================
    # create inclusion of tables
    #=========================================

    method = "refmac1"
    if flag_pr == "False":
        method = "refmac1"
    elif flag_pr == "True":
        method = "phenix_001"
    pdb = method+".pdb"

    logger.debug("Method  :  "+method)

    n = 0
    peints_dirs = []
    peints_dirs_1 = glob.glob('*/*/*/peints_*')
    for dir in peints_dirs_1:
        if os.path.isdir(dir):
            peints_dirs.append(dir)
    peints_dirs_1 = glob.glob('*/*/peints_*')
    for dir in peints_dirs_1:
        if os.path.isdir(dir):
            peints_dirs.append(dir)
    peints_dirs_1 = glob.glob('*/peints_*')
    for dir in peints_dirs_1:
        if os.path.isdir(dir):
            peints_dirs.append(dir)

    for dir in peints_dirs:
        spacegroup = ""
        cell = ""
        reso_high = ""
        reso_low = ""
        data_process = ""
        data_process_color = ""
        rwork = ""
        rwork_color = ""
        rfree = ""
        rfree_color = ""
        data = dir.split("peints_")[1]
        lines = []

        files = os.listdir(dir)
        if pdb in files:
            data_process = "SUCCESS"
            data_process_color = "lightgreen"
            f = open(os.path.join(dir, pdb), "r")
            lines = f.readlines()
            f.close()
        if not "molrep.pdb" in files:
            data_process = "FAILED at MOLREP"
        if not "peints.mtz" in files:
            data_process = "FAILED between CTRUNCATE and MOLREP"
        if not "ctruncate.mtz" in files:
            data_process = "FAILED after AIMLESS"
        if not "aimless.mtz" in files:
            data_process = "FAILED at AIMLESS"


        unipuck_id = dir.split("/")[0]
        crystal_id = dir.split("/")[1]
        overallpng  = os.path.join(dir, method+"_all.png")
        targetsitepng1 = os.path.join(dir, method+"_targetsite_1.png")
        targetsitepng2 = os.path.join(dir, method+"_targetsite_2.png")

        if lines != []:
            for line in lines:
                if line.startswith("REMARK   3   RESOLUTION RANGE HIGH (ANGSTROMS) :"):
                    reso_high = line.split()[-1]
                if line.startswith("REMARK   3   RESOLUTION RANGE LOW  (ANGSTROMS) :"):
                    reso_low = line.split()[-1]
                if line.startswith("REMARK   3   R VALUE            (WORKING SET) :"):
                    rwork = str(round(float(line.split()[-1]),3))
                    if float(rwork) < 0.35:
                        rwork_color = "lightgreen"
                if line.startswith("REMARK   3   FREE R VALUE                     :"):
                    rfree = str(round(float(line.split()[-1]),3))
                    if float(rfree) < 0.35:
                        rfree_color = "lightgreen"
                if line.startswith("CRYST1"):
                    cell = '  '.join(line.split()[1:7])
                    spacegroup = ''.join(line.split()[7:])
                    break

        logger.debug(dir + "   :  " + \
                     "  Cell = "+str(cell) +"\n"+ \
                     "  Spacegroup = "+str(spacegroup) +"\n"+ \
                     "  MaxReso = "+str(reso_high) +"\n"+ \
                     "  Rwork = "+str(rwork) +"\n"+ \
                     "  Rfree = "+str(rfree))

        html_body += \
    "<tr>" \
    "<td>"+unipuck_id+"</td>" \
    "<td>"+crystal_id+"</td>" \
    "<td>"+data+"</td>" \
    "<td>"+spacegroup+"</td>" \
    "<td>"+cell+"</td>" \
    "<td>"+reso_high+"</td>" \
    "<td>"+reso_low+"</td>" \
    "<td bgcolor="+data_process_color+">"+data_process+"</td>" \
    "<td bgcolor="+rwork_color+">"+rwork+"</td>" \
    "<td bgcolor="+rfree_color+">"+rfree+"</td>" \
    "<td><img src="+overallpng+" width='200'></td>" \
    "<td><a href="+targetsitepng1+" target='_blank'><img src="+targetsitepng1+" width='200'></a></td>" \
    "<td><a href="+targetsitepng2+" target='_blank'><img src="+targetsitepng2+" width='200'></a></td>" \
    "</tr>\n"
        n += 1

    html_body += "</table></html>"
    result = open("peints_result.html", "w")
    result.write(html_body)
    result.close()

    logger.debug("peints_result.html updated")


if __name__  == '__main__':
    import sys
    import datetime
    from logging import getLogger, FileHandler, StreamHandler, DEBUG

    run_date = datetime.datetime.now()
    args = sys.argv
    progdir = os.path.abspath(args[0])
    beamtime_dir = args[1]
    template = args[2]
    sequence = args[3]
    flag_pr = args[4]
    targetsite = ""
    spacegroup = ""
    cutoff_ios = "2.0"

    f = open(os.path.join(progdir, "VERSION"), "r")
    lines = f.readlines()
    f.close()
    version = ""
    for line in lines:
        version += line

    logfile = os.path.join(beamtime_dir, "peints_"+str(datetime.datetime.now())+".log")
    logger = getLogger(__name__)
    handler = FileHandler(filename=logfile)
    handler2 = StreamHandler()
    handler.setLevel(DEBUG)
    logger.setLevel(DEBUG)
    logger.addHandler(handler)
    logger.addHandler(handler2)
    logger.propagate = False
    logger.debug('\n\n\nPEINTS started on ' + str(datetime.datetime.now()))
    logger.debug("progdir       :  "+progdir +"\n"
                 "template      :  "+template +"\n"
                 "sequence      :  "+sequence +"\n"
                 "beamtime_dir  :  "+beamtime_dir +"\n")
    result(logger, progdir, run_date, version, beamtime_dir, template, sequence, targetsite, spacegroup, cutoff_ios, flag_pr)

