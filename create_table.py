import os, sys, glob, numpy



def table(args):

    project_dir = os.path.abspath(args[1])
    os.chdir(project_dir)

    statistics_list = [["date", "beamline", "crystal_id", "wavelength", "", "resolution", "completeness", "rmerge", "multiplicity",
         "I/s(I)", "spacegroup","", "cell_length", "cell_angle", "", "Rwork", "Rfree", "", "No._atoms", "", "B factor",
         "", "RMS_bond", "RMS_angle"]]
    aimless_log_list_2 = glob.glob("*/*/*aimless.log")
    aimless_log_list_3 = glob.glob("*/*/*/*aimless.log")
    aimless_log_list_4 = glob.glob("*/*/*/*/*aimless.log")
    aimless_log_list_5 = glob.glob("*/*/*/*/*/*aimless.log")
    
    aimless_log_list = []
    for i in aimless_log_list_2:
        aimless_log_list.append(i)
    for i in aimless_log_list_3:
        aimless_log_list.append(i)
    for i in aimless_log_list_4:
        aimless_log_list.append(i)
    for i in aimless_log_list_5:
        aimless_log_list.append(i)


    if len(aimless_log_list) > 0:
        for aimless in aimless_log_list:
            print aimless
            reso_min = "0"
            reso_max = "0"
            reso_min_in1 = "0"
            reso_min_in2 = "0"
            completeness_all = "0"
            completeness_in = "0"
            rmerge_all = "1"
            rmerge_in = "1"
            multiplicity_all = "0"
            multiplicity_in = "0"
            isigma_all = "0"
            isigma_in = "0"
            wavelength = "0"
            spacegroup = "P1"
            rwork = "1"
            rfree = "1"
            n_atom = "0"
            b_factor = "0"
            rms_bond = "0"
            rms_angle = "0"
            
            statistics = []

            date        = project_dir.split("/")[-1].split("_")[0]
            beamline    = project_dir.split("/")[-1].split("_")[1]
            crystal_id  = aimless.split("/")[0] +"_"+ aimless.split("/")[1]


            f = open(aimless, "r")
            lines = f.readlines()
            for line in lines:
                if line.startswith("         Wavelength:"):
                    wavelength = line.split()[1]

                elif line.startswith("Low resolution limit"):
                    reso_min = line.split()[3]
                    reso_min_in1 = line.split()[5]

                elif line.startswith("High resolution limit"):
                    reso_max = line.split()[3]
                    reso_min_in2 = line.split()[5]

                elif line.startswith("Rmerge  (within I+/I-)"):
                    rmerge_all = line.split()[3]
                    rmerge_in  = line.split()[5]

                elif line.startswith("Completeness"):
                    completeness_all = line.split()[1]
                    completeness_in  = line.split()[3]

                elif line.startswith("Multiplicity"):
                    multiplicity_all = line.split()[1]
                    multiplicity_in  = line.split()[3]

                elif line.startswith("Mean((I)/sd(I))"):
                    isigma_all = line.split()[1]
                    isigma_in  = line.split()[3]

                elif line.startswith("Mean((I)/sd(I))"):
                    isigma_all = line.split()[1]
                    isigma_in  = line.split()[3]

                elif line.startswith("Space group:"):
                    spacegroup = line.split(":")[1].replace(" ", "").replace("\n", "")

                elif line.startswith("Average unit cell:"):
                    cell_a, cell_b, cell_c = line.split()[3], line.split()[4], line.split()[5]
                    cell_alpha, cell_beta, cell_gamma = line.split()[6], line.split()[7], line.split()[8]

            f.close()

            refmac_pdb = os.path.join(os.path.dirname(aimless), "refmac1.pdb")

            if os.path.exists(refmac_pdb):
                f = open(refmac_pdb, "r")
                lines = f.readlines()
                for line in lines:
                    if line.startswith("REMARK   3   R VALUE            (WORKING SET) :"):
                        rwork = line.split()[7]
                    elif line.startswith("REMARK   3   FREE R VALUE                     :"):
                        rfree = line.split()[6]
                    elif line.startswith("ATOM"):
                        n_atom = line.split()[1]
                    elif line.startswith("REMARK   3   MEAN B VALUE      (OVERALL, A**2) :"):
                        b_factor = line.split()[8]
                    elif line.startswith("REMARK   3   BOND LENGTHS REFINED ATOMS        (A):"):
                        rms_bond = line.split()[9]
                    elif line.startswith("REMARK   3   BOND ANGLES REFINED ATOMS   (DEGREES):"):
                        rms_angle = line.split()[9]
                f.close()



            resolution_output = reso_min + " - " + reso_max + " (" + reso_min_in1 + " - " + reso_min_in2 +")"
            completeness_output = completeness_all + " ("+completeness_in+")"
            rmerge_output = rmerge_all + " ("+rmerge_in+")"
            multiplicity_output = multiplicity_all + " ("+multiplicity_in+")"
            isigma_output = isigma_all + " ("+isigma_in+")"
            cell_length_output = cell_a+" "+cell_b+" "+cell_c
            cell_angle_output  = cell_alpha+ " "+cell_beta+" "+cell_gamma


            statistics.append(date)
            statistics.append(beamline)
            statistics.append(crystal_id)
            statistics.append(wavelength)
            statistics.append("")
            statistics.append(resolution_output)
            statistics.append(completeness_output)
            statistics.append(rmerge_output)
            statistics.append(multiplicity_output)
            statistics.append(isigma_output)
            statistics.append(spacegroup)
            statistics.append("")
            statistics.append(cell_length_output)
            statistics.append(cell_angle_output)
            statistics.append("")
            statistics.append(rwork)
            statistics.append(rfree)
            statistics.append("")
            statistics.append(n_atom)
            statistics.append("")
            statistics.append(b_factor)
            statistics.append("")
            statistics.append(rms_bond)
            statistics.append(rms_angle)



            statistics_list.append(statistics)
            print statistics_list

        value = 0
        body  = ""
        for statistics in statistics_list:
            for factor in statistics:
                if value == 0:
                    body = factor + "\t"
                    value = 1
                else:
                    body = body + factor +"\t"
            body = body + "\n"
        f = open("statistics_table.txt", "w")
        f.write(body)
        f.close()

        array = numpy.array(statistics_list)
        print array
        array_translate = array.T
        print array_translate
        value = 0
        body  = ""
        for statistics in array_translate:
            for factor in statistics:
                if value == 0:
                    body = factor + "\t"
                    value = 1
                else:
                    body = body + factor +"\t"
            body = body + "\n"
        f = open("statistics_table_2.txt", "w")
        f.write(body)
        f.close()



args = sys.argv
table(args)






