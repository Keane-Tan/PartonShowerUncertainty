# create a root file for each signal sample with a histogram with 4 bins
import ROOT as rt

paraList = [
["3000","20","0.3","peak"],
["2000","20","0.3","peak"],
["4000","20","0.3","peak"],
["3000","50","0.3","peak"],
["3000","100","0.3","peak"],
["3000","20","0.5","peak"],
["3000","20","0.7","peak"],
["3000","20","0.3","low"],
["3000","20","0.3","high"]]

saveDir = "plots_ANbins_3/"
for mZprime, mDark, rInv, Alpha in paraList:
	idString = "mZ{}_mD{}_r{}_al{}".format(mZprime, mDark, rInv, Alpha)
	fileid = "mZprime-{}_mDark-{}_rinv-{}_alpha-{}_n-5000".format(mZprime, mDark, rInv, Alpha)	

# open the root file
	_fileBase = rt.TFile.Open(idString+"/genmassanalysis_"+fileid+".root","read")
	tree = _fileBase.Get("GenMassAnalyzer/tree")

# turn on only relevant branches
	tree.SetBranchStatus("*",0)
	tree.SetBranchStatus("weight",1)

	nEvents = tree.GetEntries()

	totiLo = 0
	totiHi = 0
	totfLo = 0
	totfHi = 0
	npass = 0

	for iEvent in range(nEvents):
		tree.GetEntry(iEvent)

		parW = tree.weight
# parW is a vector of different kinds of weights: [0] nominal, [1] Baseline, [2] isrRedHi, ..., [6] isrDefHi, [7] fsrDefHi, [8] isrDefLo, [9] fsrDefLo, ... see https://twiki.cern.ch/twiki/bin/viewauth/CMS/HowToPDF#Parton_shower_weights

# relative weight per event
		iHi_wrel = parW[6]/parW[0]
		iLo_wrel = parW[8]/parW[0]
		fHi_wrel = parW[7]/parW[0]
		fLo_wrel = parW[9]/parW[0]

		if iHi_wrel > 10 or iLo_wrel > 10 or fHi_wrel > 10 or fLo_wrel > 10:
			continue

		totiHi += iHi_wrel
		totiLo += iLo_wrel
		totfHi += fHi_wrel
		totfLo += fLo_wrel

		npass += 1

# Open the output file and save the results
	outfilename = idString+"/sumow.txt"
	sfile = open(outfilename,'w+')
	sfile.truncate(0) # clear the previously saved results

	sf = sfile.readlines()
	sf.append("(Sum of Relative Weight)/NGen\n")
	sf.append(str(totiHi/nEvents)+"\n")
	sf.append(str(totiLo/nEvents)+"\n")
	sf.append(str(totfHi/nEvents)+"\n")
	sf.append(str(totfLo/nEvents)+"\n")
	sfile.seek(0) 	# this together with .truncate() allows us to overwrite the text file
	sfile.writelines(sf)
	sfile.truncate()

	sfile.close()

	print("'Signal efficiency' is :")
	print float(npass)/float(nEvents)
