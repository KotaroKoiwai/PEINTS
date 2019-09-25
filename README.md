# PEINTS
A batch molecular replacement program for protein crystallography
ビームタイムに収集したデータを一括分子置換、ターゲットサイトの電子密度図も取得します。

PEINTS performs molecular replacement by MOLREP and REFMAC5 in the CCP4 program suite, 
and captures images your target site by COOT.


Dependency:
1) Python2.7 or Python3 is installed.
2) The CCP4 program suit is installed.
3) Optionally, the PHNENIX package is installed.

Usage:
1) Execute GUI via following command:

$   cctbx.python <peints_directory>/peints_gui.py

2) Push "Template" button and select your template pdb file (.pdb)
3) Push "Sequence" button and select your sequence file (.txt or .seq)
3) Push "Beamtime directory" button and select your beamtime directory*.
  * The beamtime directory usually includes puck directories which includes datasets processed by XDS for each crystals.
4) Push "Target site" button and input atom(s) of your target site.
  If you input single atom ID, peints will get images focusing the atom.
  If you input a pair of atom IDs, peints will place pseudoatom between the atoms, 
  and will get images focusing the pseudoatom.
  
  Format:
  
    [chainID]/[residue No.]/[atomID]
    or
    [chainID]/[residue No.]/[atomID]_[chainID]/[residue No.]/[atomID]
  
  For example:
  
    A/110/CZ
    or
    A/110/CZ_A/39/CZ
    
5) Input a spacegroup name.

  Default:
  
    Spacegroup_suggested_by_POINTLESS
    
6) Select a file name of processed dataset.

    aimless.mtz or XDS_ASCII.HKL
    
7) Choose options.

    If MR is ON, PEINTS do MR with MOLREP and refinement with REFMAC5.
    If MR is OFF, PEINTS only do refinement with REFMAC5.
    
8) Push RUN PEINTS.
9) Browse peints_result.html using your web browser.



References:

  POINTLESS:
  
    Evans P (2006) Scaling and assessment of data quality. 
    Acta Crystallogr Sect D Biol Crystallogr 62(1):72–82.
    
  AIMLESS:
  
    Evans PR, Murshudov GN (2013) How good are my data and what is the resolution? 
    Acta Crystallogr Sect D Biol Crystallogr 69(7):1204–1214.
    
  MOLREP:
  
    Vagin A, Teplyakov A (1997) MOLREP : an Automated Program for Molecular Replacement. 
    J Appl Crystallogr 30(6):1022–1025.
    
  REFMAC5:
  
    Murshudov GN, Vagin AA, Dodson EJ (1997) Refinement of Macromolecular Structures by the Maximum-Likelihood Method. 
    Acta Crystallogr Sect D Biol Crystallogr 53(3):240–255.
    
  COOT:
  
    Emsley P, Lohkamp B, Scott WG, Cowtan K (2010) Features and development of Coot. 
    Acta Crystallogr Sect D Biol Crystallogr 66(4):486–501.
    
  PHENIX.REFINE:
  
    Afonine P V, et al. (2012) Towards automated crystallographic structure refinement with phenix.refine. 
    Acta Crystallogr D Biol Crystallogr 68(Pt 4):352–367.
    
  XDS:
  
    Kabsch W (2010) Xds. 
    Acta Crystallogr Sect D Biol Crystallogr 66(2):125–132.
  
