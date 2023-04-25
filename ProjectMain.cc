#include "TFile.h"
#include "TTree.h"
#include "Pythia8/Pythia.h"
using namespace Pythia8;
using namespace std;

bool HLT_DoubleIsoMu20_eta2p1(float pT0, float eta0, float pT1, float eta1) {
    if (pT0 <= 20 || pT1 <= 20) return false;
    if (eta0 >= 2.1 || eta1 >= 2.1) return false;
    if (eta0 <= -2.1 || eta1 <= -2.1) return false;
    return true;
}

void gen(string channel) {

    // Root initialization

    TFile* events = TFile::Open("events.root", "RECREATE");
    TTree* tree = new TTree("tree", "Events generated with Pythia");

    Float_t n;
    tree -> Branch("n", &n, "n/F");

    /// STEP 1: (Pythia) INITIALIZATION ///

    Pythia pythia;
    pythia.readString("Beams:eCM = 13600.");
    pythia.readString(channel + " = on");
    pythia.readString("25:onMode = off");
    //pythia.readString("25:m0 = 125");
    pythia.readString("25:onIfMatch = -13 13");
    pythia.readString("Next:numberShowEvent = 0");
    pythia.init();

    /// STEP 2: EVENT GENERATION LOOP ///

    Hist transverse("Transverse momentum", 100, 0., 100.);
    Hist pseudo("Pseudorapidity", 100, 0., 100.);

    for (int i = 0; i < 1000; i++) {

        if (!pythia.next()) continue;
        int muon = 0;
        int antimuon = 0;
        for (int j = 0; j < pythia.event.size(); j++) if (pythia.event[j].id() == -13) muon = j;
        for (int k = 0; k < pythia.event.size(); k++) if (pythia.event[k].id() == 13) antimuon = k;
        for (int l = 0; l < pythia.event.size(); l++) cout << i << " : " << pythia.event[l].id() << " : " << pythia.event[l].charge() << endl;

        float mu_pT = pythia.event[muon].pT();
        float mu_eta = pythia.event[muon].eta();
        float antimu_pT = pythia.event[antimuon].pT();
        float antimu_eta = pythia.event[antimuon].eta();

        // Plotting in Pythia output
        // Save angles also
        transverse.fill(pythia.event[muon].pT());
        pseudo.fill(pythia.event[muon].eta());

        cout << i << " : Mu- transverse momentum : " << mu_pT << endl;
        cout << i << " : Mu- pseudorapidity : " << mu_eta << endl;
        cout << i << " : Mu+ transverse momentum : " << antimu_pT << endl;
        cout << i << " : Mu+ pseudorapidity : " << antimu_eta << endl;

        if (HLT_DoubleIsoMu20_eta2p1(mu_pT, mu_eta, antimu_pT, antimu_eta)) {
            cout << "Yes" << endl;
            //Plotting with ROOT
            //cout << pythia.event[muon].m() << endl; //0.106 GeV
            n = pythia.event[muon].pT();
            tree -> Fill();
        } else cout << "No" << endl;

        cout << endl;

    }

    /// STEP 3: PRINT AND SAVE DATA ///

    pythia.stat();
    cout << transverse;
    cout << pseudo;

    tree -> Write();
    events -> Close();
    exit(0);

}

int main() {
    
    gen("HiggsSM:all"); // Signal (Higgs) 
    //gen("WeakSingleBoson:ffbar2gmZ"); // Drell-Yan background // Maybe all?
    //gen("Top:gg2ttbar"); // ttbar background #0
    //gen("Top:qqbar2ttbar"); // ttbar background #1

    return 0;

}