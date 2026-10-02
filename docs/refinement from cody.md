## **Main Proposal:** Myco-Swarm: An In-Silico Proof of Concept for Synthetic Symbiosis

---

**Abstract: untouched**

	Microplastics pervasively contaminate agricultural soils, acting as vectors for heavy metals and pathogens. Current synthetic bioremediation relies on engineering single bacterial strains for metabolic degradation. The critical engineering gap is the inability of bacteria to physically aggregate scattered microplastics in-situ, forcing reliance on ex-situ bioreactors. We propose Myco-Swarm, an in-silico proof-of-concept for a synthetic bacterial-fungal symbiosis. Our objective is to design a system where engineered bacteria bind to microplastics and emit synthetic pheromones, triggering engineered fungal networks to chemotactically swarm and physically sequester the plastics into macroscopic mats. We will validate this computationally by using AlphaFold 3 to design the plastic-binding peptides and Agent-Based Modeling to simulate the fungal chemotaxis and sequestration rate across a 3D soil matrix. This project provides a foundational theoretical framework for in-situ microplastic extraction, moving synthetic biology beyond single-cell metabolism toward ecosystem-level behavioral symbiosis.

---

**Problem: (add the size of the mps, needs to be more narrow?)**

Plastics are a critical ubiquitous material that has allowed global economies to develop and thrive since the 1950s due to their unique versatility, durability, and low cost [(Abrahms-Kavunenko, 2023\)](https://journals.sagepub.com/doi/epdf/10.1177/13591835211066808?src=getftr&utm_source=sciencedirect_contenthosting&getft_integrator=sciencedirect_contenthosting). The global demand for plastic has dramatically increased over the years and is projected to triple by 2060, alongside plastic waste ([source](https://www.oecd.org/en/publications/2022/06/global-plastics-outlook_f065ef59.html)).

The limited and improper establishment of recyclability of single use plastics has resulted in severe plastic pollution, posing a significant environmental challenge that affects public health.   
Over the years, plastic waste and fragments have been widely present in aquatic, atmospheric, and terrestrial environments. The degradation of plastic waste and fragments directly results in microplastics, small plastic particles that are ubiquitous enough to be detected in various marine species, drinking water, and numerous foods ([source](https://pmc.ncbi.nlm.nih.gov/articles/PMC9920460/)). 

Current estimates highlight that approximately 80% of plastic waste found in oceans originate from land pollutants, while around 20% stem from marine sources [(sources vary)](https://www.sciencedirect.com/science/article/abs/pii/S0304389424002024). Transportation of these land-based microplastics follow three core processes: plastic pollutants contaminating terrestrial environments, transportation of environmental plastic waste from land to rivers, and transport from rivers to the ocean ([source](https://www.sciencedirect.com/science/article/abs/pii/S0304389424002024)). Latest plastic cleanup efforts and research have targeted the aquatic environment, but terrestrial plastic contaminants still serve as the main contributor to the issue. Solid waste microplastics usually stem from landfill garbage, sludge, and food waste due to poorly established landfill infrastructure ([source](https://www.sciencedirect.com/science/article/abs/pii/S0048969720381122)). 

The critical difference between plastic waste and microplastics varies on the clean up method required. Microplastics are ridiculously small and are spread out in significantly low concentrations, while plastic waste is detectable to the human eye. Existing methods to detect microplastics are confined to lab settings, and while they work extremely well, they are extremely inefficient and lack the speed and cost effectiveness to be applied to the real world.    
**(entire paragraph needs sources/expansion)**

**Stakeholders**: 

* Emphasize the negative effects on humans and animals(microbial)  
  * Increases Soil PH \~ Decrease Microbial Activities   
    * [https://www.sciencedirect.com/science/article/abs/pii/S0929139322001020](https://www.sciencedirect.com/science/article/abs/pii/S0929139322001020)   
    * [https://www.frontiersin.org/journals/environmental-science/articles/10.3389/fenvs.2021.675803/full](https://www.frontiersin.org/journals/environmental-science/articles/10.3389/fenvs.2021.675803/full)    
    * [https://www.sciencedirect.com/science/article/abs/pii/S0167198725002429\#introduction](https://www.sciencedirect.com/science/article/abs/pii/S0167198725002429#introduction) (nuanced abt soil comp, not microbiome)  
    * [https://www.sciencedirect.com/science/article/abs/pii/S0929139322002396](https://www.sciencedirect.com/science/article/abs/pii/S0929139322002396) (new microbial community?)  
    * [https://www.sciencedirect.com/science/article/abs/pii/S0269749122009320](https://www.sciencedirect.com/science/article/abs/pii/S0269749122009320)  
    * [https://www.sciencedirect.com/science/article/pii/S0048969723000189](https://www.sciencedirect.com/science/article/pii/S0048969723000189)    
      (toxic effects on soil)  
    * [https://www.sciencedirect.com/science/article/abs/pii/S0921344922003858](https://www.sciencedirect.com/science/article/abs/pii/S0921344922003858)  
      (effect of crop health)  
  * Human health go bye bye  
    * [https://pmc.ncbi.nlm.nih.gov/articles/PMC11504192/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11504192/)   
    * [https://www.mdpi.com/2071-1050/15/14/10821](https://www.mdpi.com/2071-1050/15/14/10821)   
    * [https://pmc.ncbi.nlm.nih.gov/articles/PMC11504042/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11504042/)   
  * Animal health go bye bye  
    * [https://peerj.com/articles/13503.pdf](https://peerj.com/articles/13503.pdf)   
    * [https://www.sciencedirect.com/science/article/pii/S2666154324002953](https://www.sciencedirect.com/science/article/pii/S2666154324002953)   
    * [https://www.mdpi.com/2076-2615/13/7/1132](https://www.mdpi.com/2076-2615/13/7/1132)   
* “Larger plastics are likely to pass through the digestive tract without bioaccumulating, whereas smaller pieces can cross intestinal barriers and end up in fat stores. Once there, they stay. When a larger organism eats a smaller organism, those microplastics transfer to its fat stores, and so on up to humans. The higher up the food chain you go, the more microplastics we’d expect to find”  
* “Researchers have found that microplastics attract and transport bacteria, viruses, heavy metals, PFAS (per- and polyfluoroalkyl substances also known as ‘forever chemicals’), pesticides, pharmaceuticals, and industrial chemicals.”

**Literature Gap:**

* Current approaches: FAST-PETase, ThermoPETase  
* **“**Current bioremediation requires an *ex-situ* bioreactor because bacteria are too small to physically capture scattered microplastics in the environment.”  
* “We have discovered enzymes that can eat plastic like IsPETase, but its limitations are that it only works in warmer temps, which is why current approaches have opted to increase thermal efficiency and other factors or make it a viable solution. At the same time, these new solutions have their own drawbacks and limitations, so instead we could create a proposal to keep the same mechanism of being able to consume and eradicate the plastic but alter the enzyme using AI to design new peptides for the bacteria to adhere to the plastic.”  
* **Narrow** the focus into what specific type of microplastic our system will detect

**The Premise:** Current bioremediation requires an *ex-situ* bioreactor because bacteria are too small to physically capture scattered microplastics in the environment. We propose a synthetic predator/prey symbiosis: engineered bacteria ("Scouts") bind to microplastics and emit a synthetic pheromone, which triggers an engineered fungal network ("Harvesters") to swarm, physically envelop, and sequester the plastics.

**The Novelty (Preserved):** This is a paradigm shift from single-cell metabolic engineering to **Ecosystem-Level Behavioral Symbiosis**. It solves the impossible physical scale problem of microplastics by turning invisible dust into macroscopic, harvestable mycelial mats.

**Refined Scope & Methodology:** Physically building and validating a cross-kingdom signaling system in a wet lab is a multi-year Ph.D. project. Therefore, this project is aggressively narrowed to a **purely computational proof-of-concept**.

1. **Peptide Design (AlphaFold 3):** We will use structural ML (AlphaFold 3 / RFdiffusion) to design the surface-display peptides for the Scout bacteria that specifically bind to PET surfaces.  
2. **Ecological & Spatial Modeling (Agent-Based Simulation):** The core of the SIBRP project will be building a 3D spatial simulation (using NetLogo or a custom PyTorch environment).  
   * We will model the physical diffusion gradient of the theoretical synthetic pheromone emitted by the Scout bacteria across a simulated soil matrix.  
   * We will model the chemotactic branching behavior of a filamentous fungus (e.g., *Trichoderma*) in response to that gradient.

**Success Metric:** The deliverable is the finalized *in-silico* peptide structures and a mathematical simulation proving that a synthetic fungal-bacterial swarm can physically aggregate scattered microplastics 10x-50x faster than passive bacterial diffusion. This simulation serves as the mandatory groundwork required before any future wet-lab team attempts to build the system.  
