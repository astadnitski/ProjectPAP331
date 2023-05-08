from ROOT import *
from array import array
import random
import os
import numpy as np

def filtering(channel):

    FILE = TFile.Open(('Root/Level1/' + channel + '.root'), 'READ')
    Muons = FILE.Get('Muons')
    Pions = FILE.Get('Pions')
    
    FILE_F = TFile.Open(('Root/Level2/' + channel + '.root'), 'RECREATE')
    Muons_F = TTree('Muons', 'Muons passing the second set of triggers')

    Event_mu = array('i', [0])
    Muons_F.Branch('Event', Event_mu, 'Event/I')

    mu_pT = array('f', [0])
    Muons_F.Branch('pT', mu_pT, 'pT/F')

    mu_eta = array('f', [0])
    Muons_F.Branch('eta', mu_eta, 'eta/F')

    mu_charge = array('f', [0])
    Muons_F.Branch('charge', mu_charge, 'charge/F')

    mu_phi = array('f', [0])
    Muons_F.Branch('phi', mu_phi, 'phi/F')

    mu_theta = array('f', [0])
    Muons_F.Branch('theta', mu_theta, 'theta/F')

    mu_m = array('f', [0])
    Muons_F.Branch('m', mu_m, 'm/F')

    np.random.seed(3)
    pions = []
    for j, pion in enumerate(Pions):
        pions.append([pion.Event, pion.pT, pion.eta, pion.phi, pion.m])
            
    muons = []
    for i, muon in enumerate(Muons):
        
        # https://www.desmos.com/calculator/oj6mh6anxe
        rng = np.random.normal(0, 0.2, 3)

        Event_number = muon.Event
        muonpT = muon.pT + 0.01 * rng[0]
        muonphi = muon.phi + 0.002 * rng[1]
        muontheta = muon.theta + 0.002 * rng[2]
        muoneta = -1 * np.log(np.tan((muontheta / 2)))        ### CHECK THAT THIS IS CORRECT
        muoncharge = muon.charge
        muonm = muon.m
        muons.append([Event_number, muonpT, muoneta, muonphi, muonm, muoncharge, muontheta])
    
    temp = []    
    for particle in muons: #Filtering and isolating the muons
        pion_pTs = []
        event_pions = []
        muon_vector = TLorentzVector()
        muon_vector.SetPtEtaPhiM(particle[1],particle[2],particle[3],particle[4])
        for subparticle in pions:
            if subparticle[0] == particle[0]:
                pion_vector = TLorentzVector()
                pion_vector.SetPtEtaPhiM(subparticle[1],subparticle[2],subparticle[3],subparticle[4])
                if muon_vector.DeltaR(pion_vector) < 0.3:
                    pion_pTs.append(subparticle[1])
        if particle[1] > 30.0 and sum(pion_pTs) < 1.5:
                temp.append(particle)
                
                
    finish = temp[-1][0]    
    filtered = []
    
    for i in range(finish): #Filtering all the events that have >1 muons and have even number of muons
        temp2 = []
        for particle in temp:
            if particle[0] == i:
                temp2.append(particle)
        if len(temp2) > 1 and len(temp2)%2 == 0:
            filtered.append(temp2)
            #print(temp2)
            
    for element in filtered: #Filling and writing the Level 2 ROOT file with the filtered muons
        for particle in element:
            Event_mu[0] = particle[0]
            mu_pT[0] = particle[1]
            mu_phi[0] = particle[3]
            mu_theta[0] = particle[6]
            mu_eta[0] = particle[2]
            mu_charge[0] = particle[5]
            mu_m[0] = particle[4]
            Muons_F.Fill()               

    FILE.Close()
    Muons_F.Write()
    FILE_F.Close()
    #print(filtered)
    
def main():

    filtering('signal')
    filtering('drellyan')
    filtering('ttbar') 

if __name__ == '__main__': main() 
