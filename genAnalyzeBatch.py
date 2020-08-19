import ROOT
import os

inputdir = "root://cmseos.fnal.gov//store/user/keanet/myProduction10/"

paraL = [["3000",
	"20",
	"0.3",
	"peak"],

	["2000",
	"20",
	"0.3",
	"peak"],

	["4000",
	"20",
	"0.3",
	"peak"],

	["3000",
	"50",
	"0.3",
	"peak"],

	["3000",
	"100",
	"0.3",
	"peak"],

	["3000",
	"20",
	"0.5",
	"peak"],

	["3000",
	"20",
	"0.7",
	"peak"],

	["3000",
	"20",
	"0.3",
	"low"],

	["3000",
	"20",
	"0.3",
	"high"]]

# making the directories
for i in range(len(paraL)):
	mZp = paraL[i][0]
	mD = paraL[i][1]
	rinv = paraL[i][2]
	alpha = paraL[i][3]

	foldername = "outputROOT10/mZ"+mZp+"_mD"+mD+"_r"+rinv+"_al"+alpha

	if os.path.exists(foldername):
		os.system("rm -r "+foldername)
	os.system("mkdir "+foldername)

# prepare to hadd
	ofilepre = foldername+"/genmassanalysis_mZprime-"+mZp+"_mDark-"+mD+"_rinv-"+rinv+"_alpha-"+alpha+"_n-5000.root"
	hcom = "hadd -f " + ofilepre + " "

# making analyzed root files
	for j in range(1,21):
		com = "cmsRun runSVJ.py config=SVJ.Production.genmassanalyzer_cfg output=TFileService outpre="+foldername+"/genmassanalysis inpre="+inputdir+"step1_GEN mZprime="+mZp+" mDark="+mD+" rinv="+rinv+" alpha="+alpha+" part="+str(j)+" maxEvents=5000"
		os.system(com)
		hcom = hcom + ofilepre[:-5]+"_part-"+str(j)+".root "
# hadding all the analyzed root files
	os.system(hcom)
	
















