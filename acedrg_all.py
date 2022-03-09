import sys, os
import glob
import subprocess

args = sys.argv
input_dir = args[1]

os.chdir(input_dir)
sdf_files = glob.glob("*.sdf")

for sdf in sdf_files:
    output = sdf.split(".")[0]
    cmd_acedrg = "acedrg -m "+sdf+" -o "+output+" -r KYO"
    subprocess.Popen(cmd_acedrg, shell=True)
