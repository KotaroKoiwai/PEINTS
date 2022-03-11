bt_dir='/Users/chemistry1/Downloads/2021-03-01_BL-17A'
mkdir ${bt_dir}
cd ${bt_dir}

container_dir=(KP-002 KP-005 KP-001 KP-003 KP-004 KP-006 KP-008)
for dir in ${container_dir[@]};
do
mkdir ${dir}
done

directory=(1_rs2_20210301_001 2_rs2_20210301_002 3_rs2_20210301_003 4_rs2_20210301_004 5_rs2_20210301_005 6_rs2_20210301_006 7_rs2_20210301_007 8_rs2_20210301_008 9_rs2_20210301_009 10_rs2_20210301_010 11_rs2_20210301_011 12_rs2_20210301_012 13_rs1_20210301_001 14_rs1_20210301_002)

cd KP-002
for dir in ${directory[@]};
do
mkdir ${dir}
mkdir ${dir}/premo
mkdir ${dir}/premo/fastxds_1
done

cd ../KP-005
directory=(1_rs2_20210301_013 2_rs2_20210301_014 3_rs2_20210301_015 4_rs2_20210301_016 5_rs2_20210301_017 6_rs2_20210301_018 7_m2_20210301_001 8_m2_20210301_002 9_m2_20210301_003 10_m2_20210301_004 11_m2_20210301_005 12_m2_20210301_006 13_m2_20210301_007 14_m2_20210301_008 15_m2_20210301_009)

for dir in ${directory[@]};
do
mkdir ${dir}
mkdir ${dir}/premo
mkdir ${dir}/premo/fastxds_1
done

cd ../KP-001
directory=(1_m2_20210301_010 2_m2_20210301_011 3_m2_20210301_012 4_m2_20210301_013 5_m2_20210301_014 6_m2_20210301_015 7_m2_20210301_016 8_m2_20210301_017 9_m2_20210301_018 10_m2_20210301_019 11_m2_20210301_020 12_m2_20210301_021 13_m2_20210301_022 14_m2_20210301_023 15_m2_20210301_024)
for dir in ${directory[@]};
do
mkdir ${dir}
mkdir ${dir}/premo
mkdir ${dir}/premo/fastxds_1
done


cd ../KP-003
directory=(1_m2_20210301_025 2_m2_20210301_026 3_m2_20210301_027 4_m2_20210301_028 5_m2_20210301_029 6_m2_20210301_030 7_m2_20210301_031 8_m2_20210301_032 9_m2_20210301_033 10_m2_20210301_034 11_m2_20210301_035 12_m2_20210301_036 13_m2_20210301_037 14_m2_20210301_038 15_m2_20210301_039)
for dir in ${directory[@]};
do
mkdir ${dir}
mkdir ${dir}/premo
mkdir ${dir}/premo/fastxds_1
done


cd ../KP-004
directory=(1_m2_20210301_040 2_m2_20210301_041 3_m2_20210301_042 4_m2_20210301_043 5_m2_20210301_044 6_MT2L_20210301_001 7_MT2L_20210301_002 8_MT2L_20210301_003 9_MT2L_20210301_004 10_MT2L_20210301_005 11_D2T_20210301_001 12_D2T_20210301_002 13_D2T_20210301_003 14_D2T_20210301_004 15_D2T_20210301_005)
for dir in ${directory[@]};
do
mkdir ${dir}
mkdir ${dir}/premo
mkdir ${dir}/premo/fastxds_1
done

cd ../KP-006
directory=(1_D2T_20210301_006 2_D2T_20210301_007 3_D2T_20210301_008 4_D2T_20210301_009 5_D2T_20210301_010 6_D2T_20210301_011 7_D2T_20210301_012 8_D2T_20210301_013 9_D2T_20210301_014 10_D2T_20210301_015 11_D2T_20210301_016 12_D2T_20210301_017 13_D2T_20210301_018 14_D2T_20210301_019 15_D2T_20210301_020)
for dir in ${directory[@]};
do
mkdir ${dir}
mkdir ${dir}/premo
mkdir ${dir}/premo/fastxds_1
done

cd ../KP-008
directory=(1_D2T_20210301_021 2_D2T_20210301_022 3_D2T_20210301_023 4_D2T_20210301_024 5_D2T_20210301_025 6_D2T_20210301_026 7_m2_20210301_045 8_m2_20210301_046 9_m2_20210301_047 10_m2_20210301_048 11_m2_20210301_049 12_m2_20210301_050 13_m2_20210301_051 14_m2_20210301_052 15_m2_20210301_053)
for dir in ${directory[@]};
do
mkdir ${dir}
mkdir ${dir}/premo
mkdir ${dir}/premo/fastxds_1
done