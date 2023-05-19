# PAP331 Project Work

## Structure of the project

The project has two main components: a Simulation script, which generates events, and an Analysis script, which selects events based on the given criteria. The project as a whole can be run with the Makefile, or piece-by-piece with e.g. `make simulate` or `make analyze`.

## Part 1: Event generation

Events generated using Pythia in `Simulation.cc` and saved to ROOT files in `/Root/Level0`.

The trigger efficiencies are calculated to be

- Signal:

- Drell-Yan: 

- TTbar:

## Part 2: Event analysis

Events analyzed with multiple functions in `Analysis.py` and saved to in two subdirectories:

- `/Root/Level1` contains only events that pass the HLT_DoubleIsoMu20_eta2p1 trigger

- `/Root/Level2` contains only events that pass the criteria given in 2A

The efficiencies at this stage are 

- Signal:

- Drell-Yan: 

- TTbar:

Reconstructing the invariant mass:

Plots are saved to the `/Plots` subdirectory.

## Part 3: Project assessment

- Gaussian smearing negatives for theta x

- Normalization

- Trigger efficiency

- Reconstruction leading order x

- Using simulations and not detector simulations x

- Something about the phase space limitation on Drell-Yan background x

- Statistical significance: check sigma x

- Optimize selection


The results are not perfect. The main reason is because Pythia is a generator-level simulation program. The results of the invariant mass and everything else should also be simulated with a detector-level simulator such as GEANT4. After simulations with GEANT4, the results would be closer to the actual data values. Another reason is that the program only includes some of the backgrounds and not all. In this program, only Drell-Yan and ttbar backgrounds are taken into the account. There are also multiple other backgrounds that should be taken into account (for example W-boson and jets). By including the other backgrounds, the results would be more realistic. The Drell-Yan background has also the phase space limited to 120-130. By changing these limits to something else, the amount of events that pass through the filters will also change for the Drell-Yan background. 

There are also parts in the code that make the results unreliable. One of them is in the Gaussian smearing. Some of the values for Muons' thetas were so close to zero that after Gaussian smearing, some of the values became negative. This is not possible because they are outside the domain. This was prevented by not doing the Gaussian smearing on those values (aka they were not smeared for the final, filtered data). Another one is doing the reconstruction by leading order of transverse momenta. Some of the events had produced more than two muons and antimuons (three or more). The program only reads the leading order values of transverse momenta for muon and antimuon, and reconstructs the invariant mass using only these two. This could also be done by using different permutations of the muon and antimuon pairs to get more accurate data and results.

The statistical significance obtained from the program is 1.8σ which is way under the 5σ threshold for discovery. However, this statistical significance result becomes more realistic after doing the generator-level simulations and taking into account other backgrounds or next-to or next-to-next-to leading order processes.

# Questions and things in progress

- Look for background processes in Appendix A of Pythia documentation?

- Which channels should be switched on?

- Explain the Drell-Yan and ttbar processes with Feynman diagrams

-- See image

- Is there an option for  HLT DoubleIsoMu20 eta2p1 in Pythia or is it just what the parameters for the trigger are called?

-- Just what the parameters are called

- What does part 2B mean (each entry in the histogram corresponds to a correct amount of cross-section)?

-- Use Pythia to calculate the cross-section (when you simulate the events, you always get it) (calculated anyway for part 1)

- Part 2C: background plot is both backgrounds?

-- Subtract plot with background from plot with background and signal to get signal plot

Should we limit mass phase space?

Advice:

Use Landau distribution for fits. Or try Gaussian or something it's a good approximation. For the signal Breit-Wigner is probably best
