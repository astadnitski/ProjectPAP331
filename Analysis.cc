#include <iostream>
#include "TFile.h"
#include "TTree.h"

using namespace std;

//float HLT_DoubleIsoMu20_eta2p1(float pT, float eta) { return pT >= 20 && eta >= -2.1 && eta <= 2.1; } 
//float HLT_DoubleIsoMu30(float pT) { return pT >= 30; }

void analyze(string channel) {

    TFile* file = TFile::Open(("Root/" + channel + ".root").c_str(), "READ");
    //events -> Write();
    file -> Close();

}

int main() {
    analyze("signal");
    analyze("drellyan");
    analyze("ttbar");
    cout << "This doesn't do anything yet" << endl;
    return 0;
}