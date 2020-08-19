import ROOT as rt
import sys
import CMS_lumi, tdrstyle

tdrstyle.setTDRStyle()

#rt.gStyle.SetPalette(54,0)
rt.gROOT.SetBatch(True)
rt.gStyle.SetOptStat(0)

def histmake(histL,histH, histN, name): # name is "ISR" or "FSR" etc.
# Drawing the histograms on the same plot
	histL.SetLineStyle(7)
	histH.SetLineStyle(7)
	histL.SetLineWidth(2)
	histH.SetLineWidth(2)

	H=700
	W=700

	H_ref = 700
	W_ref = 700

	T = 0.08*H_ref
	B = 0.12*H_ref
	L = 0.12*W_ref
	R = 0.08*W_ref

	c = rt.TCanvas("c","canvas",0,0,W,H)
	c.SetFillColor(0);
	c.SetBorderMode(0);
	c.SetFrameFillStyle(0);
	c.SetFrameBorderMode(0);
	#c.SetLeftMargin( 0.15 );#L/W        
	c.SetRightMargin(0.04);                                                                                                                             
	#c.SetRightMargin( R/W );
	c.SetTopMargin( T/H );
	#c.SetBottomMargin(0.2);
	c.SetTickx(0);
	c.SetTicky(0);
	c.Draw()

	# define stack of bkgHistos

	histL.SetDirectory(0)
	histL.SetLineColor(rt.kRed)
	histH.SetDirectory(0)
	histH.SetLineColor(rt.kBlue)
	histN.SetDirectory(0)
	histN.SetLineColor(rt.kBlack)

	stack = rt.THStack()
	stack.Add(histL)
	stack.Add(histN)
	stack.Add(histH)
	# Upper plot will be in pad1
	pad1 = rt.TPad("pad1", "pad1", 0, 0.25, 1, 0.95)
	pad1.SetBottomMargin(0.05)
	pad1.SetRightMargin(0.04)
	#pad1.SetGridx()         # Vertical grid
	#pad1.SetGridy()         # Horizontal grid
	pad1.SetLogy()
	pad1.Draw()             # Draw the upper pad: pad1
	pad1.cd()               # pad1 becomes the current pad
	#stack.SetStats(0)       # No statistics on upper plot
	#data.SetStats(0)       # No statistics on upper plot
#	stack.SetMinimum(1)
#	stack.SetMaximum(2200)
	stack.Draw("nostackHIST")

	stack.GetXaxis().SetLabelOffset(999)
	stack.GetXaxis().SetLabelSize(0)	
	stack.GetYaxis().SetTitle("Events")
	stack.GetYaxis().SetTitleSize(30)
	stack.GetYaxis().SetTitleFont(43)
	stack.GetYaxis().SetTitleOffset(1.35)
	stack.GetYaxis().SetLabelFont(43)
	stack.GetYaxis().SetLabelSize(25)
	stack.SetMaximum(6000)

	leg = rt.TLegend(0.65,0.7,0.85,0.9)
	leg.SetTextFont(42)
	leg.SetHeader("SVJ_3000_20_0.3_peak")
	leg.AddEntry(histN, "central", "l")
	leg.AddEntry(histH, name+" Up", "l")
	leg.AddEntry(histL, name+" Down", "l")
	leg.SetTextSize(.04)
	leg.Draw("same")

	# lower plot will be in pad2
	c.cd()          # Go back to the main canvas before defining pad2
	pad2 = rt.TPad("pad2", "pad2", 0, 0, 1, 0.25)
	pad2.SetTopMargin(0.05)
	pad2.SetBottomMargin(0.37)
	pad2.SetRightMargin(0.04)
	#pad2.SetGridx() # vertical grid
	#pad2.SetGridy()         # Horizontal grid
	pad2.Draw()
	pad2.cd()       # pad2 becomes the current pad

	# Define the ratio plot for histL
	h3 = histL.Clone("h3")
	h3.SetMarkerColor(rt.kRed)
	h3.SetMinimum(0.78)  # Define Y ..
	h3.SetMaximum(1.22) # .. range
	h3.Sumw2()
	h3.SetStats(0)      # No statistics on lower plot
	h3.Divide(histN)
	h3.SetMarkerStyle(8)
	h3.Draw("EX0P")       # Draw the ratio plot

	# Ratio plot (h3) settings
	h3.SetTitle("") # Remove the ratio title

	# Y axis ratio plot settings
	h3.GetYaxis().SetTitle("syst/central")
	h3.GetYaxis().SetNdivisions(503)
	h3.GetYaxis().SetTitleSize(30)
	h3.GetYaxis().SetTitleFont(43)
	h3.GetYaxis().SetTitleOffset(1.1)
	h3.GetYaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
	h3.GetYaxis().SetLabelSize(22)

	# X axis ratio plot settings
	h3.GetXaxis().SetTitle("M_{T} [GeV]")
	h3.GetXaxis().SetTitleSize(33)
	h3.GetXaxis().SetTitleFont(43)
	h3.GetXaxis().SetTitleOffset(3.5)
	h3.GetXaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
	h3.GetXaxis().SetLabelSize(22)
	h3.GetXaxis().SetLabelOffset(0.03)

	# Define the ratio plot for histL
	h4 = histH.Clone("h4")
	h4.SetMarkerColor(rt.kBlue)
	h4.SetMinimum(0.80)  # Define Y ..
	h4.SetMaximum(1.20) # .. range
	h4.Sumw2()
	h4.SetStats(0)      # No statistics on lower plot
	h4.Divide(histN)
	h4.SetMarkerStyle(8)
	h4.Draw("EX0P SAME")       # Draw the ratio plot


	pad1.Update()
	pad2.Update()
	c.Update()
	const = rt.TF1("const", '[0]', h3.GetXaxis().GetXmin(), h3.GetXaxis().GetXmax())
	line = rt.TF1("line", '[0]+[1]*x', h3.GetXaxis().GetXmin(), h3.GetXaxis().GetXmax())
	one = rt.TF1("one", '1', h3.GetXaxis().GetXmin(), h3.GetXaxis().GetXmax())
	one.SetLineStyle(2)
	#h3.Fit("const","Q")
	one.SetLineColor(rt.kRed)
	one.Draw("same")
	#h3.Fit("line","Q+")
	#save as .png

	# CMS style
	CMS_lumi.lumi_sqrtS = "41.5 fb^{-1} (13 TeV)"
	CMS_lumi.extraText   = "  Simulation"

	iPeriod = 0
	iPos = 0

	CMS_lumi.CMS_lumi(c, iPeriod, iPos)
	c.cd()
	c.Update();
	c.RedrawAxis()

	plotname = name+idString+".pdf"
	c.SaveAs(idString + "/" + plotname)
	c.Delete()

#paraList = [
#["3000","20","0.3","peak"],
#["2000","20","0.3","peak"],
#["4000","20","0.3","peak"],
#["3000","50","0.3","peak"],
#["3000","100","0.3","peak"],
#["3000","20","0.5","peak"],
#["3000","20","0.7","peak"],
#["3000","20","0.3","low"],
#["3000","20","0.3","high"]]
paraList = [["3000","20","0.3","peak"]]

for mZprime, mDark, rInv, Alpha in paraList:
	idString = "mZ{}_mD{}_r{}_al{}".format(mZprime, mDark, rInv, Alpha)
	fileid = "mZprime-{}_mDark-{}_rinv-{}_alpha-{}_n-5000".format(mZprime, mDark, rInv, Alpha)	
	# color xH red for half
	# color xD blue for Double
	# color rf black for base

# open the root file
	_fileBase = rt.TFile.Open(idString+"/genmassanalysis_"+fileid+".root","read")
	tree = _fileBase.Get("GenMassAnalyzer/tree")

# open the file with the sum of relative weight/nEvent
	outfilename = idString+"/sumow.txt"
	sfile = open(outfilename,'r+')
	sf = sfile.readlines()
	ratiHi = float(sf[1][:-2])
	ratiLo = float(sf[2][:-2])
	ratfHi = float(sf[3][:-2])
	ratfLo = float(sf[4][:-2])

# open the file that saves the total weights
	tfilename = idString+"/totalweights.txt"
	tfile = open(tfilename,'w+')
	tf = tfile.readlines()

# turn on only relevant branches
	tree.SetBranchStatus("*",0)
	tree.SetBranchStatus("GenJetsAK8" ,1)
	tree.SetBranchStatus("MT",1)
	tree.SetBranchStatus("MET",1)
	tree.SetBranchStatus("weight",1)

	nEvents = tree.GetEntries()

	histMax = 4000
	if mZprime == "2000":
		histMax = 2500
	elif mZprime == "4000":
		histMax = 4500


	hist_iHi = rt.TH1F(idString+"M_{T}","M_{T}",24,1500,histMax) 
	hist_iLo = rt.TH1F(idString+"M_{T}","M_{T}",24,1500,histMax)  
	hist_fHi = rt.TH1F(idString+"M_{T}","M_{T}",24,1500,histMax) 
	hist_fLo = rt.TH1F(idString+"M_{T}","M_{T}",24,1500,histMax) 
 
	hist_n = rt.TH1F(idString+"M_{T}","M_{T}",24,1500,histMax)

	for iEvent in range(nEvents):
		tree.GetEntry(iEvent)

		# important variables
		FJets = tree.GenJetsAK8
		eventMET = tree.MET
		eventMT = tree.MT
		parW = tree.weight
# parW is a vector of different kinds of weights: [0] nominal, [1] Baseline, [2] isrRedHi, ..., [6] isrDefHi, [7] fsrDefHi, [8] isrDefLo, [9] fsrDefLo, ... see https://twiki.cern.ch/twiki/bin/viewauth/CMS/HowToPDF#Parton_shower_weights

# Setting up the normalized relative weights
		reliHi = parW[6]/parW[0]
		reliLo = parW[8]/parW[0]
		relfHi = parW[7]/parW[0]
		relfLo = parW[9]/parW[0]

		if reliHi > 10 or reliLo > 10 or relfHi > 10 or relfLo > 10:
			continue

		normiHi = reliHi/ratiHi
		normiLo = reliLo/ratiLo
		normfHi = relfHi/ratfHi
		normfLo = relfLo/ratfLo


		if len(FJets) < 2:
			continue

		jet0Pt = FJets[0].Pt()
		jet1Pt = FJets[1].Pt()
		jet0Eta = FJets[0].Eta()
		jet1Eta = FJets[1].Eta()
		eventRT = eventMET/eventMT
	
# Applying preselection
		if (jet0Pt>200 and jet1Pt>200) and (abs(jet0Eta)<2.4) and (abs(jet1Eta)<2.4) and (abs(jet0Eta-jet1Eta)<1.5) and (eventRT>0.15) and (eventMT>1500):
			continue

# Filling the histograms
		hist_iHi.Fill(eventMT,normiHi)
		hist_iLo.Fill(eventMT,normiLo)
		hist_fHi.Fill(eventMT,normfHi)
		hist_fLo.Fill(eventMT,normfLo)
		hist_n.Fill(eventMT)


	tfile.seek(0) 	# this together with .truncate() allows us to overwrite the text file
	tfile.writelines(tf)
	tfile.truncate()

	histmake(hist_iLo,hist_iHi,hist_n,"ISR")
	histmake(hist_fLo,hist_fHi,hist_n,"FSR")
