# -*- coding: utf-8 -*-
import sys, re, os, glob, string
import cgitb
cgitb.enable()


def result(logger, beamtime_dir, template, sequence, flag_pr):
    #=========================================
    # create HTML header & table_index
    #=========================================

    html_body = \
    "<html>""\
    ""<TITLE>Results of PEINTS</TITLE>""\
    ""<H1>Results of peints</H1>""\
    ""Project directory:     " + beamtime_dir + "<br>""\
    ""Template PDB:     " + template +"<br>""\
    ""Sequence    :     " + sequence +"<br>""\
    ""<table border='1' style='background-color'>""\
    ""<tr>""\
    ""<th>unipuck</th>""\
    ""<th>crystal</th>""\
    ""<th>data</th>""\
    ""<th>spacegroup</th>""\
    ""<th>unit cell</th>""\
    ""<th>resolution high</th>""\
    ""<th>resolution low</th>""\
    ""<th>Rwork</th>""\
    ""<th>Rfree</th>""\
    ""<th>overall</th>""\
    ""<th>pocket_1</th>""\
    ""<th>pocket_2</th>""\
    ""</tr>"

    f = open("peints_result.html", "w")
    f.write(html_body)
    f.close()

    #=========================================
    # create inclusion of tabels
    #=========================================

    method = "refmac1"
    if flag_pr == "False":
        method = "refmac1"
    elif flag_pr == "True":
        method = "phenix_001"
    pdb = method+".pdb"


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
        rwork = ""
        rfree = ""
        data = dir.split("peints_")[1]
        lines = []
        if pdb in os.listdir(dir):
            f = open(os.path.join(dir, pdb), "r")
            lines = f.readlines()
            f.close()

        unipuck_id = dir.split("/")[0]
        crystal_id = dir.split("/")[1]
        overallpng  = os.path.join(dir, method+"_all.png")
        targetsitepng1 = os.path.join(dir,method+"_targetsite_1.png")
        targetsitepng2 = os.path.join(dir,method+"_targetsite_2.png")

        if lines != []:
            if flag_pr == "False":
                for line in lines:
                    if line.startswith("REMARK   3   RESOLUTION RANGE HIGH (ANGSTROMS) :"):
                        reso_high = line.split()[-1]
                    if line.startswith("REMARK   3   RESOLUTION RANGE LOW  (ANGSTROMS) :"):
                        reso_low = line.split()[-1]
                    if line.startswith("REMARK   3   R VALUE            (WORKING SET) :"):
                        rwork = line.split()[-1]
                    if line.startswith("REMARK   3   FREE R VALUE                     :"):
                        rfree = line.split()[-1]
                    if line.startswith("CRYST1"):
                        cell = '  '.join(line.split()[1:7])
                        spacegroup = ''.join(line.split()[7:])
                        break

            if flag_pr == "True":
                for line in lines:
                    if line.startswith("REMARK   3   RESOLUTION RANGE HIGH (ANGSTROMS) :"):
                        reso_high = line.split()[-1]
                    if line.startswith("REMARK   3   RESOLUTION RANGE LOW  (ANGSTROMS) :"):
                        reso_low = line.split()[-1]
                    if line.startswith("REMARK   3   R VALUE            (WORKING SET) :"):
                        rwork = line.split()[-1]
                    if line.startswith("REMARK   3   FREE R VALUE                     :"):
                        rfree = line.split()[-1]
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

        body = \
    "<tr>""\
    ""<td>"+unipuck_id+"</td>""\
    ""<td>"+crystal_id+"</td>""\
    ""<td>"+data+"</td>""\
    ""<td>"+spacegroup+"</td>""\
    ""<td>"+cell+"</td>""\
    ""<td>"+reso_high+"</td>""\
    ""<td>"+reso_low+"</td>""\
    ""<td>"+rwork+"</td>""\
    ""<td>"+rfree+"</td>""\
    ""<td><img src="+overallpng+" width='200'></td>""\
    ""<td><a href="+targetsitepng1+" target='_blank'><img src="+targetsitepng1+" width='200'></a></td>""\
    ""<td><a href="+targetsitepng2+" target='_blank'><img src="+targetsitepng2+" width='200'></a></td>""\
    ""</tr>"
        result = open("peints_result.html", "a")
        result.write(body)
        result.close()

        n += 1

    endhtml = "</table></html>"
    result = open("peints_result.html", "a")
    result.write(endhtml)
    result.close()

    logger.debug("peints_result.html updated")


if __name__  == '__main__':
    import sys
    import datetime
    from logging import getLogger, FileHandler, StreamHandler, DEBUG

    args = sys.argv
    progdir = os.path.abspath(args[0])
    beamtime_dir = args[1]
    template = args[2]
    sequence = args[3]
    flag_pr = args[4]

    logfile = os.path.join(beamtime_dir, "peints_"+str(datetime.datetime.now())+".log")
    logger = getLogger(__name__)
    handler = FileHandler(filename=logfile)
    handler2 = StreamHandler()
    handler.setLevel(DEBUG)
    logger.setLevel(DEBUG)
    logger.addHandler(handler)
    logger.addHandler(handler2)
    logger.propagate = False
    logger.debug('\n\n\npeints started on ' + str(datetime.datetime.now()))
    logger.debug("progdir       :  "+progdir +"\n"
                 "template      :  "+template +"\n"
                 "sequence      :  "+sequence +"\n"
                 "beamtime_dir  :  "+beamtime_dir +"\n")
    result(logger, beamtime_dir, template, sequence, flag_pr)
