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