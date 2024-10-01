![social card](https://raw.githubusercontent.com/rmnldwg/lydata/main/github-social-card.png)

## What is lyDATA?

lyDATA is a repository for datasets that report detailed patterns of lymphatic progression for head & neck squamous cell carcinoma (HNSCC).

## Motivation

HNSCC spreads though the lymphatic system of the neck and forms metastases in regional lymph nodes. Macroscopic metastases can be detected with imaging modalities like MRI, PET and CT scans. They are then consequently included in the target volume, when radiotherapy is chosen as part of the treatment. However, microscopic metastases are too small be diagnosed with current imaging techniques.

To account for this microscopic involvement, parts of the lymphatic system are often irradiated electively to increase tumor control. Which parts are included in this elective clinical target volume is currently decided based on guidelines like [[1]](#1), [[2]](#2), [[3]](#3) and [[4]](#4). These in turn are derived from reports of the prevalence of involvement per lymph node level (LNL), i.e. the portion of patients that were diagnosed with metastases in any given LNL, stratified by primary tumor location. It is recommended to include a LNL in the elective target volume if 10 - 15% of patients showed involvement in that particular level.

However, while the prevalence of involvement has been reported in the literature, e.g. in [[5]](#5) and [[6]](#6), and the general lymph drainage pathways are understood well, the detailed progression patterns of HNSCC remain poorly quantified. We believe that the risk for microscopic involvement in an LNL depends highly on the specific diagnose of a particular patient and their treatment can hence be personalized if the progression patterns were better quantified.

## Our Goal

In this repository we aim to provide data on the detailed lymphatic progression patterns extracted from patients of the University Hospital Zurich (USZ). The data can be used freely and we hope clinicians in the field find it useful as well. Ideally, we can motivate other researchers to share their data in similar detail and openness, so that large multi-centric datasets can be built.

## Available datasets

### 📂 [2021 USZ Oropharynx]

[![radonc badge](https://img.shields.io/badge/Rad%20Onc-j.radonc.2022.01.035-3e6e0e)](https://doi.org/10.1016/j.radonc.2022.01.035)
[![medRxiv badge](https://img.shields.io/badge/medR%CF%87iv-2021.12.01.21267001-0e4c92)](https://doi.org/10.1101/2021.12.01.21267001)
[![DiB badge](https://img.shields.io/badge/DiB-10.1016%2Fj.dib.2022.108345-orange)](https://doi.org/10.1016/j.dib.2022.108345)
[![zenodo badge](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.5833835-informational)](https://doi.org/10.5281/zenodo.5833835)

The first dataset we are able to share consists of 287 patients with a primary tumor in the oropharynx, treated at the University Hospital Zurich (USZ) between 2013 and 2019. It can be found in the folder `2021-usz-oropharynx` alongside a `jupyter` notebook that was used to create figures.

We have published a paper about it in *Radiotherapy & Oncology* [[9]](#9) (a preprint is also available on *medRxiv* [[10]](#10)). The dataset is described in detail and can be freely used and cited as a *Data in Brief* paper [[11]](#11).

[2021 USZ Oropharynx]: https://github.com/rmnldwg/lyDATA/tree/main/2021-usz-oropharynx

### 📂 [2021 CLB Oropharynx]

[![Green Journal](https://img.shields.io/badge/Rad%20Onc-j.radonc.2021.01.028-3e6e0e)](https://doi.org/10.1016/j.radonc.2021.01.028)
[![DiB badge](https://img.shields.io/badge/DiB-10.1016%2Fj.dib.2023.110020-orange)](https://doi.org/10.1016/j.dib.2023.110020)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10204085.svg)](https://doi.org/10.5281/zenodo.10204085)

We are glad and thankful that the research group around Prof. Vincent Grégoire from the [Centre Léon Bérard] in Lyon (France) have joined our effort to create a database of lymphatic patterns of progression by providing us with the data underlying their publication [[6]](#6). If you use this data, don't forget to cite either said publication or use the `CITATION.cff` file inside the `2021-clb-oropharynx` folder, where the `data.csv` also resides and a description of the data named `README.md`.

[2021 CLB Oropharynx]: https://github.com/rmnldwg/lyDATA/tree/main/2021-clb-oropharynx
[Centre Léon Bérard]: https://www.centreleonberard.fr/en

### 📂 [2023 ISB Multisite]

[![DiB badge](https://img.shields.io/badge/DiB-10.1016%2Fj.dib.2023.110020-orange)](https://doi.org/10.1016/j.dib.2023.110020)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10210423.svg)](https://doi.org/10.5281/zenodo.10210423)

As part of a collaboration with researchers from the [Inselspital Bern] (Switzerland) around Prof. Roland Giger, we are thankful and glad to be able to publish a large and exceptionally detailed dataset on lymphatic progression of HNSCC patients, assessed by pathology. In contrast to earlier datasets, this includes not only patients with oropharyngeal tumors, but also oral cavity, hypopharynx and larynx.

[2023 ISB Multisite]: https://github.com/rmnldwg/lyDATA/tree/main/2023-isb-multisite
[Inselspital Bern]: https://www.insel.ch/de/

### 📂 [2023 CLB Multisite]

[![DiB badge](https://img.shields.io/badge/DiB-10.1016%2Fj.dib.2023.110020-orange)](https://doi.org/10.1016/j.dib.2023.110020)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10210361.svg)](https://doi.org/10.5281/zenodo.10210361)

Completing the "2021 CLB Oropharynx" data table, these patient records detail lymphatic involvement patterns in HNSCC patients with primary tumors beyond the oropharynx. Again, they are thankfully provided by researchers in Prof. Vincent Grégoire's group and the data was extracted at the [Centre Léon Bérard].

[2023 CLB Multisite]: https://github.com/rmnldwg/lyDATA/tree/main/2023-clb-multisite

### stay tuned for more

We are in the process of collecting more data that we might publish soon. If you would like to contribute to our effort, feel free to contact us: [roman.ludwig@usz.ch]

[roman.ludwig@usz.ch]: mailto:roman.ludwig@usz.ch

## Attribution

Every folder that corresponds to a dataset also contains a `CITATION.cff` file which may be used to cite the respective dataset. To cite the entire repository with all datasets inside, use the `CITATION.cff` at the root of the repository (or just click the *Cite this repository* button on the right).

## Requirements

Besides the data, this repository provides a Python library for loading, manipulating, and validating the available datasets.

> [!WARNING]
> This Python library is still highly experimental!

[![Build](https://github.com/rmnldwg/lydata/actions/workflows/build.yml/badge.svg)](https://github.com/rmnldwg/lydata/actions/workflows/build.yml)
[![Tests](https://github.com/rmnldwg/lydata/actions/workflows/tests.yml/badge.svg)](https://github.com/rmnldwg/lydata/actions/workflows/tests.yml)
[![Documentation Status](https://readthedocs.org/projects/lydata/badge/?version=stable)](https://lydata.readthedocs.io/en/stable/?badge=stable)

If you want to install this library, clone the repo and install it. You can do so by executing these commands:

```bash
git clone https://github.com/rmnldwg/lydata
cd lydata
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install .
```

You may have noticed that there are also `requirements.*` files here. These are independent of this library and instead related to reproducing the output of the Python files in the `scripts/` folder. To reproduce these, run the following commands:

```bash
git clone https://github.com/rmnldwg/lydata
cd lydata
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

## See also

### LyProX Interface

The data in this repository can be explored interactively in our online interface [LyProX] ([GitHub repo]).

[LyProX]: https://lyprox.org
[GitHub repo]: https://github.com/rmnldwg/lyprox

### Probabilistic models

We have developed and implemented probabilistic models for lymphatic tumor progression ([[7]](#7), [[8]](#8)) that may allow for highly personalized risk predictions in the future. These models can be trained using the dataset(s) in this repository. For details on the implementation, check out the [lymph] package.

[lymph]: https://github.com/rmnldwg/lymph

## License

All patient data in this repository, e.g. all files whose names end with .xlsx or .csv, as well as figures depicting characteristics of that data, are licensed under [CC BY-SA 4.0]. Attribution must be given to the owner of the repository (see the `CITATION.cff` file at the root of the repository) and the collector(s) or curator(s) of the respective dataset (see the `CITATION.cff` file inside the corresponding dataset's folder).

The remaining material is licensed under the [MIT License]. This includes e.g. all Python files and the overall structure of the repository.

[CC BY-SA 4.0]: https://creativecommons.org/licenses/by-sa/4.0/
[MIT License]: https://mit-license.org/

## References

<a id="1">[1]</a>
Vincent Grégoire and Others,
**Selection and delineation of lymph node target volumes in head and neck conformal radiotherapy. Proposal for standardizing terminology and procedure based on the surgical experience**,
*Radiotherapy and Oncology*, vol. 56, pp. 135-150, 2000,
doi: <https://doi.org/10.1016/S0167-8140(00)00202-4>.

<a id="2">[2]</a>
Vincent Grégoire, A. Eisbruch, M. Hamoir, and P. Levendag,
**Proposal for the delineation of the nodal CTV in the node-positive and the post-operative neck**,
*Radiotherapy and Oncology*, vol. 79, no. 1, pp. 15-20, Apr. 2006,
doi: <https://doi.org/10.1016/j.radonc.2006.03.009>.

<a id="3">[3]</a>
Vincent Grégoire et al.,
**Delineation of the neck node levels for head and neck tumors: A 2013 update. DAHANCA, EORTC, HKNPCSG, NCIC CTG, NCRI, RTOG, TROG consensus guidelines**,
*Radiotherapy and Oncology*, vol. 110, no. 1, pp. 172-181, Jan. 2014,
doi: <https://doi.org/10.1016/j.radonc.2013.10.010>.

<a id="4">[4]</a>
Julian Biau et al.,
**Selection of lymph node target volumes for definitive head and neck radiation therapy: a 2019 Update**,
*Radiotherapy and Oncology*, vol. 134, pp. 1-9, May 2019,
doi: <https://doi.org/10.1016/j.radonc.2019.01.018>.

<a id="5">[5]</a>
Jatin. P. Shah, F. C. Candela, and A. K. Poddar,
**The patterns of cervical lymph node metastases from squamous carcinoma of the oral cavity**,
*Cancer*, vol. 66, no. 1, pp. 109-113, 1990,
doi: <https://doi.org/10.1002/1097-0142(19900701)66:1%3C109::AID-CNCR2820660120%3E3.0.CO;2-A>.

<a id="6">[6]</a>
Laurence Bauwens et al.,
**Prevalence and distribution of cervical lymph node metastases in HPV-positive and HPV-negative oropharyngeal squamous cell carcinoma**,
*Radiotherapy and Oncology*, vol. 157, pp. 122-129, Apr. 2021,
doi: <https://doi.org/10.1016/j.radonc.2021.01.028>.

<a id="7">[7]</a>
Bertrand Pouymayou, P. Balermpas, O. Riesterer, M. Guckenberger, and J. Unkelbach,
**A Bayesian network model of lymphatic tumor progression for personalized elective CTV definition in head and neck cancers**,
*Physics in Medicine & Biology*, vol. 64, no. 16, p. 165003, Aug. 2019,
doi: <https://doi.org/10.1088/1361-6560/ab2a18>.

<a id="8">[8]</a>
Roman Ludwig, B. Pouymayou, P. Balermpas, and J. Unkelbach,
**A hidden Markov model for lymphatic tumor progression in the head and neck**,
*Sci Rep*, vol. 11, no. 1, p. 12261, Dec. 2021,
doi: <https://doi.org/10.1038/s41598-021-91544-1>.

<a id="9">[9]</a>
Roman Ludwig et al.,
**Detailed patient-individual reporting of lymph node involvement in oropharyngeal squamous cell carcinoma with an online interface**,
*Radiotherapy and Oncology*, Feb. 2022,
doi: <https://doi.org/10.1016/j.radonc.2022.01.035>.

<a id="10">[10]</a>
Roman Ludwig, J.-M. Hoffmann, B. Pouymayou et al.,
**Detailed patient-individual reporting of lymph node involvement in oropharyngeal squamous cell carcinoma with an online interface**,
*medRxiv*, Dec. 2021.
doi: <https://doi.org/10.1101/2021.12.01.21267001>.

<a id="11">[11]</a>
Roman Ludwig, Jean-Marc Hoffmann, Bertrand Pouymayou et al.,
**A dataset on patient-individual lymph node involvement in oropharyngeal squamous cell carcinoma**,
*Data in Brief*, 2022, 108345,
doi: <https://doi.org/10.1016/j.dib.2022.108345>.
