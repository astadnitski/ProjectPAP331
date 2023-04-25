#include "TFile.h"
#include "TTree.h"
#include "Pythia8/Pythia.h"
#include <string.h>
using namespace Pythia8;
using namespace std;

#define Nevents 100

bool HLT_DoubleIsoMu20_eta2p1(float pT0, float eta0, float pT1, float eta1) {
    if (pT0 <= 20 || pT1 <= 20) return false;
    if (eta0 >= 2.1 || eta1 >= 2.1) return false;
    if (eta0 <= -2.1 || eta1 <= -2.1) return false;
    return true;
}

void gen(string channel, TFile *events, TTree *tree) {

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

<<<<<<< HEAD
    for (int i = 0; i < 1000; i++) {
=======
    int muon, antimuon;
    float mu_pT, mu_eta, mu_m, mu_charge, mu_phi;
    float antimu_pT, antimu_eta, antimu_m, antimu_charge, antimu_phi;

    tree -> Branch("mu_pT", &mu_pT, "mu_pT/F");
    tree -> Branch("mu_eta", &mu_eta, "mu_eta/F");
    tree -> Branch("mu_m", &mu_m, "mu_m/F");
    tree -> Branch("mu_charge", &mu_charge, "mu_charge/F"); 
    tree -> Branch("mu_phi", &mu_phi, "mu_phi/F");

    tree -> Branch("antimu_pT", &antimu_pT, "antimu_pT/F");
    tree -> Branch("antimu_eta", &antimu_eta, "antimu_eta/F");
    tree -> Branch("antimu_m", &antimu_m, "antimu_m/F");
    tree -> Branch("antimu_charge", &antimu_charge, "antimu_charge/F");
    tree -> Branch("antimu_phi", &antimu_phi, "antimu_phi/F");

    float trigger_efficiency1, NmuonPassed = 0;

    for (int i = 0; i < Nevents; i++) {
>>>>>>> bd84d9dceef3398234d4122544773ad2919a75ba

        if (!pythia.next()) continue;

        muon = 0;
        antimuon = 0;

        for (int j = 0; j < pythia.event.size(); j++) if (pythia.event[j].id() == -13) muon = j;
        for (int k = 0; k < pythia.event.size(); k++) if (pythia.event[k].id() == 13) antimuon = k;
        for (int l = 0; l < pythia.event.size(); l++) cout << i << " : " << pythia.event[l].id() << " : " << pythia.event[l].charge() << endl;

        mu_pT = pythia.event[muon].pT();
        mu_eta = pythia.event[muon].eta();
    
        // Plotting in Pythia output
<<<<<<< HEAD
        // Save angles also
        transverse.fill(pythia.event[muon].pT());
        pseudo.fill(pythia.event[muon].eta());
=======
        transverse.fill(mu_pT);
        pseudo.fill(mu_eta);
>>>>>>> bd84d9dceef3398234d4122544773ad2919a75ba

        cout << i << " : Mu- transverse momentum : " << mu_pT << endl;
        cout << i << " : Mu- pseudorapidity : " << mu_eta << endl;
            
        antimu_pT = pythia.event[antimuon].pT();
        antimu_eta = pythia.event[antimuon].eta();

        cout << i << " : Mu+ transverse momentum : " << antimu_pT << endl;
        cout << i << " : Mu+ pseudorapidity : " << antimu_eta << endl;

        if (HLT_DoubleIsoMu20_eta2p1(mu_pT, mu_eta, antimu_pT, antimu_eta)) {
            if (mu_pT > 30 && antimu_pT > 30) {
                mu_m = pythia.event[muon].m();
                mu_charge = pythia.event[muon].charge();
                mu_phi = pythia.event[muon].phi();

                antimu_m = pythia.event[antimuon].m();
                antimu_charge = pythia.event[antimuon].charge();
                antimu_phi = pythia.event[antimuon].phi();

                NmuonPassed++;

                tree -> Fill();
            }
        } 
        //else cout << "No" << endl;
        cout << endl;
    }

    trigger_efficiency1 = 100.0*NmuonPassed/Nevents;

    /// STEP 3: PRINT AND SAVE DATA ///

    pythia.stat();
    cout << transverse;
    cout << pseudo;

    cout << endl << "trigger_efficiency = " << trigger_efficiency1 << "%" << endl;

    tree -> Write();

    events -> Close();
    //exit(0);
}

int main() {
<<<<<<< HEAD
    
    gen("HiggsSM:all"); // Signal (Higgs) 
    //gen("WeakSingleBoson:ffbar2gmZ"); // Drell-Yan background // Maybe all?
    //gen("Top:gg2ttbar"); // ttbar background #0
=======

    TFile* events = TFile::Open("events_test.root", "RECREATE");

    TTree* signal = new TTree("signal", "Signal events generated with Pythia");
    TTree* DrellYan = new TTree("DrellYan", "Drell-Yan background events generated with Pythia");
    TTree* ttbar = new TTree("ttbar", "Ttbar background  generated with Pythia");

    gen("HiggsSM:all", events, signal); // Signal (Higgs) 
    //gen("WeakSingleBoson:ffbar2gmZ", events, DrellYan); // Drell-Yan background 
    //gen("Top:gg2ttbar", events, ttbar); // ttbar background #0

>>>>>>> bd84d9dceef3398234d4122544773ad2919a75ba
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