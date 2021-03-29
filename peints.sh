#!/usr/bin/
# conding: utf-8
#  peints_main.sh

XDSDIR=${1}
TEMPpdb=${2}
MR_FLAG=${3}
sg=${4}

ctruncate -mtzin ${XDSDIR}/aimless.mtz -mtzout ctruncate.mtz -colin '/*/*/[IMEAN,SIGIMEAN]' -colano '/*/*/[I(+),SIGI(+),I(-),SIGI(-)]' <<eof | tee ctruncate.log

eof

reso_temp=(`grep "Resolution range of data:" ctruncate.log`)
uc_temp=(`grep "^Cell parameters:" ctruncate.log`)

echo ${reso_temp[@]}
echo ${sg_temp[@]}
echo ${uc_temp[@]}
uc="${uc_temp[2]} ${uc_temp[3]} ${uc_temp[4]} ${uc_temp[5]} ${uc_temp[6]} ${uc_temp[7]}"
reso=${reso_temp[6]}


echo "$uc"
echo "$sg"
echo "$reso"

unique hklin ctruncate.mtz HKLOUT unique.mtz <<eof-unique | tee freerflag.log
RESOLUTION $reso
CELL $uc
SYMMETRY $sg
LABOUT F=FUNI SIGF=SIGFUNI
END
eof-unique

freerflag HKLIN 'unique.mtz' HKLOUT 'freerflag.mtz' <<eof-frf | tee -a freerflag.log
FREERFRAC 0.05
END
eof-frf

cad HKLIN2 "freerflag.mtz" HKLIN1 "ctruncate.mtz" HKLOUT "cad.mtz"  <<eof-cad | tee -a freerflag.log
LABI FILE 2  E1=FreeR_flag
LABI FILE 1  ALLIN
END
eof-cad

freerflag HKLIN "cad.mtz" HKLOUT "peints.mtz" <<eof-freer | tee -a freerflag.log
COMPLETE FREE=FreeR_flag
END
eof-freer

echo "MR_FLAG  "${MR_FLAG}
if [ ${MR_FLAG} = True ]; then
    molrep -f peints.mtz -m ${TEMPpdb} | tee molrep.log
    REFMAC_IN=molrep.pdb
elif [ ${MR_FLAG} = False ]; then
    REFMAC_IN=${TEMPpdb}
fi
refmac5 hklin peints.mtz xyzin ${REFMAC_IN} hklout refmac1.mtz xyzout refmac1.pdb <<eof-refmac | tee refmac.log
END
eof-refmac
