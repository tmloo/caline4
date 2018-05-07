# CALINE4 - Highway Emissions Dispersal Model
This repository provides the data and resources to generate highway emission dispersal models in the California Bay Area using the CALINE4 program. This project is the beginning of a larger initiative to create a platform agnostic, one-stop-shop, website to generate highway emission dispersal models for all of California. Dispersion models generated can be used as a screening tool for city planners and potentially as a exposure variable for epidemiology studies. 

Instructions:
1. Download the "bay area links and receptors.zip" and select the area you are interested in.
2. Reformat the links and receptors dataset by following the "links and receptors formatting guide" instructions.
3. Read the resulting links and receptor files into the "CALINE4 formatting" python notebook.
4. Read the resulting output file into CALINE4 to generate emission dispersal results.

Notes:
- CALINE4 and other programs are PC-based. Mac users will need to install a virtual machine to run these softwares.
- CALINE4 model parameter definitions can be found: http://www.dot.ca.gov/hq/env/air/documents/CL4Guide.pdf

Future work: 
- Spatial data from (1) will be housed online on a website and users will select from a dropdown menu.
- Step (2) will be done automatically using Python scripting in QGIS. 
- Step (3) will also be done automatically as the data can be read directly from step (2).
- CALINE4 program will be house on a platform agnostic online service. Instead of running CALINE4 directly, users will be prompted to enter model parameters through the website which will be populated into CALINE4. Step (4) will be done automatically. 
