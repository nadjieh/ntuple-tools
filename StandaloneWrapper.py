# Translate the HGCAL N-tuples to the format used for standalone calibration (SAC) by Pedro
# import ROOT
# import os
import optparse
from NtupleDataFormat import HGCalNtuple
import hgcalHelpers
import numpy as np
import pandas as pd
from itertools import repeat

class SACevent:
	def __init__(self, event):
		self.hgcEvent = event
	def getGenInfo(self):
		if hasattr(self, "genParticles"):
			return self.genId, self.genEn, self.genEt, self.genEta, self.genPhi
		self.genParticles = self.hgcEvent.getDataFrame(prefix="genpart")
		self.genId = self.genParticles.pid
		self.genEta = self.genParticles.eta
		self.genEt = self.genParticles.pt
		self.genEn = self.genParticles.energy
		self.genPhi = self.genParticles.phi
		return self.genId, self.genEn, self.genEt, self.genEta, self.genPhi
	def getRecHitInfo(self):
		if hasattr(self, "recHits"):
			return self.si_sim_sumen, self.sci_sim_sumen
		self.recHits = self.hgcEvent.getDataFrame(prefix="rechit")
		self.layers = []
		self.si_sim_sumen = []
		self.sci_sim_sumen = []
		for iRecHit in range (0,len(self.recHits)):
			isSi = (int(self.recHits.thickness[iRecHit]) == 100 or int(self.recHits.thickness[iRecHit]) == 200 or int(self.recHits.thickness[iRecHit]) == 300)
			if not self.recHits.layer[iRecHit] in self.layers:
				self.layers.append(self.recHits.layer[iRecHit])
				self.si_sim_sumen.append(0)
				self.sci_sim_sumen.append(0)
			index = self.layers.index(self.recHits.layer[iRecHit])
			if isSi:
				self.si_sim_sumen[index]+=self.recHits.energy[iRecHit]
			else:
				self.sci_sim_sumen[index]+=self.recHits.energy[iRecHit]
		return self.si_sim_sumen, self.sci_sim_sumen

	def Print(self):
		self.getGenInfo()
		self.getRecHitInfo()
		for gen in range(0,len(self.genId)):
			print "gen id = %f, energy = %f, Et = %f, eta = %f, phi = %f" %(self.genId[gen], self.genEn[gen], self.genEt[gen], self.genEta[gen], self.genPhi[gen])
		for l in range(0,len(self.layers)):
			print "Layer number %f: Si energy sum = %f, Sci energy sum = %f" %(self.layers[l], self.si_sim_sumen[l], self.sci_sim_sumen[l])



def main():
    global opt, args

    usage = ('usage: %prog [options]\n' + '%prog -h for help')
    parser = optparse.OptionParser(usage)

    # input options
    # parser.add_option('', '--files', dest='fileString', type='string',  default='root://eoscms.cern.ch//eos/cms/store/cmst3/group/hgcal/CMG_studies/Production/_SinglePiPt50Eta1p6_2p8_PhaseIITDRFall17DR-noPUFEVT_93X_upgrade2023_realistic_v2-v1_GEN-SIM-RECO/NTUP/_SinglePiPt50Eta1p6_2p8_PhaseIITDRFall17DR-noPUFEVT_93X_upgrade2023_realistic_v2-v1_GEN-SIM-RECO_NTUP_1.root', help='comma-separated file list')
    parser.add_option('', '--files', dest='fileString', type='string',  default='/afs/cern.ch/work/e/escott/public/HGCStudies/Ntuples/partGun_Pion_Pt25_93X_PU140.root', help='comma-separated file list')
    parser.add_option('', '--gunType', dest='gunType', type='string',  default='pt', help='pt or e')
    parser.add_option('', '--pid', dest='pid', type='int',  default=211, help='pdgId int')
    parser.add_option('', '--genValue', dest='genValue', type='float',  default=25, help='generated pT or energy')

    # store options and arguments as global variables
    global opt, args
    (opt, args) = parser.parse_args()

    print "files:", opt.fileString
    print "gunType:", opt.gunType
    print "pid:", opt.pid
    print "GEN_engpt:", opt.genValue

    # set sample/tree - for photons
    gun_type = opt.gunType
    pidSelected = opt.pid
    GEN_engpt = opt.genValue

    fileList = opt.fileString.split(",")

    for fileName in fileList:
        ntuple = HGCalNtuple(opt.fileString)

        for event in ntuple:
            if (event.entry() > 11):
                break
            SACEvt = SACevent(event)
            SACEvt.Print()



if __name__ == '__main__':
    main()