# -*- coding: utf-8 -*-
#!/usr/bin/python3
##  check_download_XDS_ASCII.HKL ##

import sys, os

class Manage():
    def __init__(self, orig_dir, target_dir):

        self.orig_dir = orig_dir
        self.target_dir = target_dir
        self.find_xds_files()
        self.compare_path_header()

    def find_xds_files(self):
        os.chdir(self.target_dir)
        self.xds_file_list = []
        for current, subfolders, subfiles in os.walk(self.target_dir):
            for subfile in subfiles:
                if subfile == "XDS_ASCII.HKL":
                    self.xds_file_list.append(os.path.join(os.path.abspath(current), subfile))

        print(self.xds_file_list)

        os.chdir(self.orig_dir)

    def compare_path_header(self):
        body = "file_path,header_path,result\n"
        for xds_file in self.xds_file_list:
            file_puck_id = xds_file.split("/")[-5]
            file_crystal_id = xds_file.split("/")[-4]

            f = open(xds_file, "r")
            lines = f.readlines()
            f.close()

            for line in lines:
                if line.startswith("!NAME_TEMPLATE_OF_DATA_FRAMES="):
                    header_puck_id = line.split("/")[-4]
                    header_crystal_id = line.split("/")[-3]
                elif line.startswith("!DATA_RANGE="):
                    break

            file_id = file_puck_id+"/"+file_crystal_id
            header_id = header_puck_id+"/"+header_crystal_id

            if file_id == header_id:
                result = "FINE\n"
            else:
                result = "WRONG\n"

            body += file_id+","+header_id+","+result

        f = open(os.path.join(self.target_dir, "check_download_xds_file.log"), "w")
        f.write(body)
        f.close()



#=================================================
# main function
#=================================================
if __name__  == '__main__':
    args = sys.argv
    orig_dir = os.getcwd()
    target_dir = args[1]
    Manage(orig_dir, target_dir)
