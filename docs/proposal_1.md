## **Main Proposal:** Myco-Swarm: An In-Silico Proof of Concept for Synthetic Symbiosis

**The Premise:** Current bioremediation requires an *ex-situ* bioreactor because bacteria are too small to physically capture scattered microplastics in the environment. We propose a synthetic predator/prey symbiosis: engineered bacteria ("Scouts") bind to microplastics and emit a synthetic pheromone, which triggers an engineered fungal network ("Harvesters") to swarm, physically envelop, and sequester the plastics.

**The Novelty (Preserved):** This is a paradigm shift from single-cell metabolic engineering to **Ecosystem-Level Behavioral Symbiosis**. It solves the impossible physical scale problem of microplastics by turning invisible dust into macroscopic, harvestable mycelial mats.

**Refined Scope & Methodology (Addressing the Feedback):** As the TA noted, physically building and validating a cross-kingdom signaling system in a wet lab is a multi-year Ph.D. project. Therefore, for SIBRP, this project is aggressively narrowed to a **purely computational proof-of-concept**.

1. **Peptide Design (AlphaFold 3):** We will use structural ML (AlphaFold 3 / RFdiffusion) to design the surface-display peptides for the Scout bacteria that specifically bind to PET surfaces.  
2. **Ecological & Spatial Modeling (Agent-Based Simulation):** The core of the SIBRP project will be building a 3D spatial simulation (using NetLogo or a custom PyTorch environment).  
   * We will model the physical diffusion gradient of the theoretical synthetic pheromone emitted by the Scout bacteria across a simulated soil matrix.  
   * We will model the chemotactic branching behavior of a filamentous fungus (e.g., *Trichoderma*) in response to that gradient.

**Success Metric:** The deliverable is the finalized *in-silico* peptide structures and a mathematical simulation proving that a synthetic fungal-bacterial swarm can physically aggregate scattered microplastics 10x-50x faster than passive bacterial diffusion. This simulation serves as the mandatory groundwork required before any future wet-lab team attempts to build the system.

---

**Abstract:**   
	Microplastics pervasively contaminate agricultural soils, acting as vectors for heavy metals and pathogens. Current synthetic bioremediation relies on engineering single bacterial strains for metabolic degradation. The critical engineering gap is the inability of bacteria to physically aggregate scattered microplastics in-situ, forcing reliance on ex-situ bioreactors. We propose Myco-Swarm, an in-silico proof-of-concept for a synthetic bacterial-fungal symbiosis. Our objective is to design a system where engineered bacteria bind to microplastics and emit synthetic pheromones, triggering engineered fungal networks to chemotactically swarm and physically sequester the plastics into macroscopic mats. We will validate this computationally by using AlphaFold 3 to design the plastic-binding peptides and Agent-Based Modeling to simulate the fungal chemotaxis and sequestration rate across a 3D soil matrix. This project provides a foundational theoretical framework for in-situ microplastic extraction, moving synthetic biology beyond single-cell metabolism toward ecosystem-level behavioral symbiosis

---

Research Project Proposal: Myco-Swarm

## 1\. Competitive Analysis: The "Loophole" in Top-Tier Research

Recent high-impact literature and iGEM Grand Prize winners (e.g., Heidelberg 2023, Bioremediation) showcase brilliant biological platforms to upcycle mixed plastics using engineered co-cultures. 

**The Loophole:** Their systems require an **ex-situ bioreactor**. You must physically collect the plastic, place it in a vat, and let the bacteria degrade it. 

**The Grand Challenge:** The true "abyss" in bioremediation is **in-situ physical sequestration**. How do you clean up millions of invisible microplastics scattered across vast agricultural soils or complex waterways? Bacteria alone cannot do this—they are too small to physically filter an environment, and they easily wash away.

To beat the current state-of-the-art, we must move beyond single-cell metabolic engineering and engineer **Ecosystem-Level Behavioral Symbiosis**.

\---

## 2\. The Complete Project: Myco-Swarm

**Title:** ML-Optimized Synthetic Symbiosis between Bacteria and Fungi for In-Situ Microplastic Sequestration and Upcycling

We will engineer a synthetic predator/prey-style symbiosis between a fast-growing, engineered bacterium (the "Scout") and a filamentous fungal network (the "Harvester"). 

### A. The Scout (Synthetic Biology & Computational Bio)

* **Plastic Binding:** Using a "no-compromises" ML approach (AlphaFold 3, RFdiffusion, and deep mutational scanning), we will design state-of-the-art surface-display peptides for a hardy soil bacterium (like *B. subtilis*). These peptides act like molecular velcro, binding specifically to microplastics (PET, PE).  
* **The Signal:** Once the bacterium binds to the plastic, mechanical/chemical stress triggers a synthetic genetic circuit. The bacteria begin emitting a computationally designed synthetic chemoattractant (a unique pheromone not found in nature).

### B. The Harvester (Behavioral Biology & Synthetic Biology)

* **The Receptor:** We genetically engineer a fast-growing filamentous fungus (like *Trichoderma reesei*). Using advanced protein design, we insert a synthetic G-Protein Coupled Receptor (GPCR) into the fungus that specifically detects the Scout's pheromone.  
* **The Behavior:** The fungal mycelial network's behavioral biology is hijacked. It aggressively grows and branches along the chemical gradient toward the Scout bacteria.

\#\#\# C. The Ecosystem Result (Bioremediation & Dual-Functionality)

### C. The Ecosystem Result (Bioremediation & Dual-Functionality)

We are engineering a **modular, dual-functionality** system to maximize reliability and impact:

1. **Physical Extraction:** The solid mycelial-plastic mats act as biological nets that can be easily pulled out of the soil or water, solving the physical collection problem.  
2. **In-Situ Upcycling:** The fungus is simultaneously engineered to secrete intense localized enzymes (like PETase/MHETase) to degrade the trapped plastic and metabolize it into value-added biomaterials (e.g., chitin-based bioplastics) directly within the soil matrix.

\---

## 3\. Disciplinary Integration & State-of-the-Art ML Pipeline

We will utilize the absolute best tools available, with no compromises on computational rigor:

* **Machine Learning / Structural Bio:** AlphaFold 3 and RFdiffusion will be used to generate *de novo* plastic-binding peptides and the synthetic GPCR.  
* **Ecological/Spatial ML:** Deep Reinforcement Learning and Agent-Based Modeling (via PyTorch/NetLogo) will be used to simulate the diffusion of the pheromones in 3D soil matrices and predict the optimal mycelial branching behavior to maximize capture efficiency.  
* **Synthetic Biology:** Engineering cross-kingdom signaling (bacteria-to-fungus communication).  
* **Behavioral Biology:** Dictating the chemotactic growth and physical swarming behavior of a macroscopic fungal network.  
* **Bioremediation:** Solving the physical collection bottleneck of microplastics in complex environments.

