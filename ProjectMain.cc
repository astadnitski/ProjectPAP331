#include "TFile.h"
#include "TTree.h"
#include "Pythia8/Pythia.h"
#include <string.h>
using namespace Pythia8;
using namespace std;

#define Nevents 10000

bool HLT_DoubleIsoMu20_eta2p1(float pT, float eta) {
    if (pT <= 20) return false;
    if (eta >= 2.1) return false;
    if (eta <= -2.1) return false;
    return true;
}

bool HLT_DoubleIsoMu30(float pT) { return pT >= 30;}


void gen(string channel, TFile *events) {

    // Root initialization

    /// STEP 1: (Pythia) INITIALIZATION ///

    Pythia pythia;
    pythia.readString("Beams:eCM = 13600.");

    pythia.readString(channel + " = on");
    if (!(strcmp(channel.c_str(), "Top:gg2ttbar"))) pythia.readString("Top:qqbar2ttbar = on");

    pythia.readString("25:onMode = off");
    //pythia.readString("25:m0 = 125");
    pythia.readString("25:onIfMatch = -13 13");
    pythia.readString("Next:numberShowEvent = 0");

    pythia.init();

    /// STEP 2: EVENT GENERATION LOOP ///

    Hist transverse("Transverse momentum", 100, 0., 100.);
    Hist pseudo("Pseudorapidity", 100, 0., 100.);

    TTree* muon = new TTree("muon", "muon events generated with Pythia");
    TTree* antimuon = new TTree("antimuon", "antimuon events generated with Pythia");

    int isMuon, isAntimuon;
    float mu_pT, mu_eta, mu_m, mu_charge, mu_phi;
    float antimu_pT, antimu_eta, antimu_m, antimu_charge, antimu_phi;

    muon -> Branch("mu_pT", &mu_pT, "mu_pT/F");
    muon -> Branch("mu_eta", &mu_eta, "mu_eta/F");
    muon -> Branch("mu_m", &mu_m, "mu_m/F");
    muon -> Branch("mu_charge", &mu_charge, "mu_charge/F"); 
    muon -> Branch("mu_phi", &mu_phi, "mu_phi/F");

    antimuon -> Branch("antimu_pT", &antimu_pT, "antimu_pT/F");
    antimuon -> Branch("antimu_eta", &antimu_eta, "antimu_eta/F");
    antimuon -> Branch("antimu_m", &antimu_m, "antimu_m/F");
    antimuon -> Branch("antimu_charge", &antimu_charge, "antimu_charge/F");
    antimuon -> Branch("antimu_phi", &antimu_phi, "antimu_phi/F");

    float trigger_efficiency1;
    int Nmuonpassed = 0, Nantimuonpassed = 0;
    int Nmuontotal = 0, Nantimuontotal = 0;

    for (int i = 0; i < Nevents; i++) {

        if (!pythia.next()) continue;

        isMuon = 0;
        isAntimuon = 0;

        for (int j = 0; j < pythia.event.size(); j++)
        {
            if (pythia.event[j].id() == -13)
            {
                isMuon = j;
                Nmuontotal++;

                mu_pT = pythia.event[isMuon].pT();
                mu_eta = pythia.event[isMuon].eta();

                transverse.fill(mu_pT);
                pseudo.fill(mu_eta);

                 if (HLT_DoubleIsoMu20_eta2p1(mu_pT, mu_eta)) 
                 {
                    // if (HLT_DoubleIsoMu30(mu_pT)) 
                    // {
                        mu_m = pythia.event[isMuon].m();
                        mu_charge = pythia.event[isMuon].charge();
                        mu_phi = pythia.event[isMuon].phi();

                        Nmuonpassed++;

                        muon -> Fill();
                    // }
                } 

            }

            else if (pythia.event[j].id() == 13)
            {
                isAntimuon = j;
                Nantimuontotal++;

                antimu_pT = pythia.event[isAntimuon].pT();
                antimu_eta = pythia.event[isAntimuon].eta();

                transverse.fill(antimu_pT);
                pseudo.fill(antimu_eta);
                 
                 if (HLT_DoubleIsoMu20_eta2p1(antimu_pT, antimu_eta)) 
                 {
                    // if (HLT_DoubleIsoMu30(antimu_pT)) 
                    // {

                        antimu_m = pythia.event[isAntimuon].m();
                        antimu_charge = pythia.event[isAntimuon].charge();
                        antimu_phi = pythia.event[isAntimuon].phi();

                        Nantimuonpassed++;

                        antimuon -> Fill();
                    // }
                } 

            }

            else continue;
        }
        
        cout << endl;
    }

    int Ntotal = Nmuontotal + Nantimuontotal;
    int Npassed = Nmuonpassed + Nantimuonpassed;

    trigger_efficiency1 = 100.0*Npassed/Ntotal;

    /// STEP 3: PRINT AND SAVE DATA ///

    pythia.stat();
    cout << transverse;
    cout << pseudo;

    cout << endl << "trigger_efficiency = " << trigger_efficiency1 << "%" << endl;

    muon -> Write();
    antimuon -> Write();

    events -> Close();
    //exit(0);
}

int main() {

    // TFile* events = TFile::Open("events_test.root", "RECREATE");

    // TTree* signal = new TTree("signal", "Signal events generated with Pythia");
    // TTree* DrellYan = new TTree("DrellYan", "Drell-Yan background events generated with Pythia");
    // TTree* ttbar = new TTree("ttbar", "Ttbar background  generated with Pythia");

    TFile* signal = TFile::Open("signal.root", "RECREATE");
    //TFile* DrellYan = TFile::Open("DrellYan.root", "RECREATE");
    //TFile* ttbar = TFile::Open("ttbar.root", "RECREATE");

    gen("HiggsSM:all", signal); // Signal (Higgs) 
    //gen("WeakSingleBoson:ffbar2gmZ", events, DrellYan); // Drell-Yan background 
    //gen("Top:gg2ttbar", events, ttbar); // ttbar background #0

    //gen("Top:qqbar2ttbar"); // ttbar background #1

    return 0;

}

// == NOTES ==
/*
чому не прац дерева всі

інвар мас

селекшн 30

зробити лаб 11, 12



*/