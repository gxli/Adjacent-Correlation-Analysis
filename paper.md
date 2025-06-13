---
title: 'Adjacent Correlation Analysis; A python package for perform interactive data visualizations using adjacency informaiton'
tags:
  - Python
  - astronomy
  - dynamical systems
  - data visualization
authors:
  - name: Guang-Xing Li
    orcid: 0000-0000-0000-0000
    equal-contrib: true
    affiliation: "1, 2" # (Multiple affiliations must be quoted)

affiliations:
 - name: Guang-Xing Li, Yunnan University, China
   index: 1

date: 3 June 2025
bibliography: paper.bib

# Optional fields if submitting to a AAS journal too, see this blog post:
# https://blog.joss.theoj.org/2018/12/a-new-collaboration-with-aas-publishing
aas-doi: 10.3847/xxxxx <- update this with the DOI from AAS once you know it.
aas-journal: Astrophysical Journal <- The name of the AAS journal.
---
# Summary

Our understanding of Nature hinges on informed observations and data analysis. While finding correlations effectively describes relationships between quantities, uncovering these from*complex data has been challenging. We've found the key is to select local regions and study the correlations within them. These **locally-induced correlations** represent a new type of regularity, often overlooked when studying global correlations.

We present the **adjacent correlation analysis** method, which consists of two key components:

The **adjacent correlation analysis** derives vectors representing correlations in the parameter space. For quantities like $p_1(x, y)$ and $p_2(x, y)$, the method generates vectors that show correlations in the $p_1-p_2$ space. These vectors can then be plotted on a Probability Density Distribution (2D histogram), forming the adjacent correlation analysis, from which regularities can be discovered.

The **adjacent correlation map** provides visual representations of the relationship between $p_1$ and $p_2$. It often shows that larger regions can be separated into subregions with different correlation patterns.

---

# Statement of Need

This package is designed to reveal regularities present in data that are often missed in global distributions. This is achieved through an effective representation of correlations, derived from local changes in coordinates using **Stokes parameters**.

The adjacent correlation analysis can uncover regularities overlooked when comparing data using 2D histograms.

The adjacent correlation map is a new method that helps visualize how correlations change across space.

---

# Mathematics

The core of the method is based on the **superposition of correlation vectors**, treated as **spin-2 vectors**.

Given two quantities, $p_1(x, y)$ and $p_2(x, y)$, the correlation vector in the $p_1-p_2$ space is:

$(E_x, E_y) = (\partial p_1 / \partial x_i, \partial p_2 / \partial x_i)$,

where $x_i = (x, y)$.

The method's core involves superimposing these correlation vectors by treating
them as spin-2 vectors, which is conceptually similar to light polarization
using Stokes parameters. This converts $(E_x, E_y)$ into $i$, $q$, and $u$
parameters, which are then added together. The final correlation is computed
using $i$, $q$, and $u$.



For details of the method see `[@li2025revealinghiddencorrelationscomplex,@li2025mappingcorrelationscoherenceadjacencybased]`. The implementation
can be found at [https://github.com/gxli/Adjacent-Correlation-Analysis](https://github.com/gxli/Adjacent-Correlation-Analysis).


<!-- Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format. -->



<!-- If you want to cite a software repository URL (e.g. something on GitHub without a preferred
citation) then you can do it with the example BibTeX entry below for @fidgit.

For a quick reference, the following citation commands can be used:
- `@author:2001`  ->  "Author et al. (2001)"
- `[@author:2001]` -> "(Author et al., 2001)"
- `[@author1:2001; @author2:2001]` -> "(Author1 et al., 2001; Author2 et al., 2002)" -->

# Figures


-![Adjacent Correlation Analysis and Adjacent Correlation Map applied to MHD
simulation data](images/illus_website.png)

<!-- 
Figures can be included like this:
![Caption for example figure.\label{fig:example}](figure.png)
and referenced from text using \autoref{fig:example}.

Figure sizes can be customized by adding an optional second parameter:
![Caption for example figure.](figure.png){ width=20% } -->

# Acknowledgements

GXL acknowledges supports from NSFC grant No. 12273032 and 12033005.

# References

**Adjacent Correlation Analysis:**

* *Revealing hidden correlations from complex spatial distributions: Adjacent Correlation Analysis*, Li (2025)

**Adjacent Correlation Map:**

* *Mapping correlations and coherence: adjacency-based approach to data visualization and regularity discovery*, Li (2025)