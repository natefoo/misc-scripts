#!/usr/bin/env python

import os.path
import sys

sys.path.insert(0, 'lib')

#from galaxy.tools.deps.mulled.util import build_target, v1_image_name
from galaxy.tools.deps.conda_util import hash_conda_packages, CondaTarget

reqs = """	DEXSeq	/galaxy/main/deps/_conda/envs/mulled-v1-0ac87b39a40f44c0fe078d45b44a75214d4cdc24e1ddfc494e56a9ef42628a17	bioconductor-dexseq	1.20.1	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-0ac87b39a40f44c0fe078d45b44a75214d4cdc24e1ddfc494e56a9ef42628a17	r-getopt	1.20.0	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-0ac87b39a40f44c0fe078d45b44a75214d4cdc24e1ddfc494e56a9ef42628a17	r-rjson	0.2.15	Conda	True	
	Get RT Stop Counts		biopython	1.61	Tool_Shed_Package	True	
numpy	1.7.1	Tool_Shed_Package	True	
samtools	0.1.18	Tool_Shed_Package	True	
	BIOM metadata, Convert Biom2 to Biom1, Convert Biom1 to Biom2, Convert BIOM		biom-format	None	None	True	
	plotCorrelation, bamCompare, plotEnrichment, bigwigCompare, multiBamSummary, correctGCBias, bamCoverage, multiBigwigSummary, bamPEFragmentSize, plotCoverage, plotHeatmap, computeMatrix, plotFingerprint, plotProfile, plotPCA, computeGCBias	/galaxy/main/deps/_conda/envs/__python@2.7.10	python	2.7.10	Conda	True	
/galaxy/main/deps/_conda/envs/__deepTools@2.3.6	deepTools	2.3.6	Conda	True	
	StringTie, StringTie		stringtie	1.2.3	Tool_Shed_Package	True	
	DESeq2		deseq2	1.8.2	Tool_Shed_Package	True	
	Canonical Correlation Analysis		R	2.11.0	Tool_Shed_Package	True	
numpy	1.7.1	Tool_Shed_Package	True	
yacca	1.0	Tool_Shed_Package	True	
rpy	1.0.3	Tool_Shed_Package	True	
	phyloP		add_scores	None	None	True	
	DESeq2	/galaxy/main/deps/_conda/envs/__bioconductor-deseq2@1.14.1	bioconductor-deseq2	1.14.1	Conda	True	
	Reverse-Complement, FASTQ to FASTA, Collapse, Trim sequences, Filter by quality, Rename sequences, Barcode Splitter, Remove sequencing artifacts, Draw nucleotides distribution chart, Quality format converter, Compute quality statistics, RNA/DNA, FASTA Width, Draw quality score boxplot, Clip		fastx_toolkit	0.0.13	Tool_Shed_Package	True	
	Du Novo: Correct barcodes, Du Novo: Correct barcodes		samtools	0.1.18	Galaxy_Package	True	
/galaxy/main/deps/_conda/envs/__bowtie2@2.2.5	bowtie2	2.2.5	Conda	True	
/galaxy/main/deps/_conda/envs/__networkx@1.11	networkx	1.11	Conda	True	
/galaxy/main/deps/_conda/envs/__dunovo@2.0.6	dunovo	2.0.6	Conda	True	
	MACS2 bdgbroadcall, MACS2 bdgpeakcall		macs2	2.1.0	Tool_Shed_Package	True	
numpy	1.7.1	Tool_Shed_Package	True	
scipy	0.12.0	Tool_Shed_Package	True	
gnu_awk	4.1.0	Tool_Shed_Package	True	
	BedToIntervalList, FixMateInformation, RevertOriginalBaseQualitiesAndAddMateCigar, FilterSamReads, NormalizeFasta, AddCommentsToBam, MergeBamAlignment, MarkDuplicates, CollectWgsMetrics, ReorderSam, CleanSam, FastqToSam, SortSam, SamToFastq, AddOrReplaceReadGroups, Collect Alignment Summary Metrics, ReplaceSamHeader, EstimateLibraryComplexity, Downsample SAM/BAM, MergeSamFiles, MarkDuplicatesWithMateCigar, RevertSam, ValidateSamFile		picard	1.136	Tool_Shed_Package	True	
	Du Novo: Make families, Du Novo: Make consensus reads	/galaxy/main/deps/_conda/envs/__dunovo@2.0.6	dunovo	2.0.6	Conda	True	
	Select Variants, Select Variants, Variant Recalibrator, Validate Variants, Apply Variant Recalibration, Eval Variants, Combine Variants, Variant Filtration		gatk	1.4	Tool_Shed_Package	True	
	Reactivity Calculation		biopython	1.61	Tool_Shed_Package	True	
numpy	1.7.1	Tool_Shed_Package	True	
	TagBed, FisherBed, Convert from BED to BAM, Compute both the depth and breadth of coverage, AnnotateBed, GetFastaBed, ClusterBed, Genome Coverage, Intersect interval files, NucBed, SubtractBed, SlopBed, LinksBed, ComplementBed, Convert from BAM to BED, Intersect multiple sorted BED files, ClosestBed, JaccardBed, ReldistBed, MaskFastaBed, ExpandBed, ShuffleBed, BED12 to BED6, MultiCovBed, WindowBed, FlankBed, Convert from BEDPE to BAM, Sort BED files, MakeWindowsBed, Merge BED files, RandomBed, OverlapBed, Merge BedGraph files, MapBed, GroupByBed		bedtools	2.22	Tool_Shed_Package	True	
	GffCompare	/galaxy/main/deps/_conda/envs/__gffcompare@0.9.8	gffcompare	0.9.8	Conda	True	
	CollectInsertSizeMetrics, CollectBaseDistributionByCycle, QualityScoreDistribution, CollectGcBiasMetrics, CollectRnaSeqMetrics, MeanQualityByCycle		picard	1.136	Tool_Shed_Package	True	
R	3.1.2	Tool_Shed_Package	True	
	Convert FASTA to Bowtie color space Index, Convert FASTA to Bowtie base space Index		bowtie	0.12.7	Galaxy_Package	True	
	Du Novo: Make families, Du Novo: Make consensus reads	/galaxy/main/deps/_conda/envs/__dunovo@0.8.1	dunovo	0.8.1	Conda	True	
	Bowtie2, Bowtie2		bowtie2	2.2.6	Tool_Shed_Package	True	
samtools	1.2	Tool_Shed_Package	True	
	Du Novo: Correct barcodes		samtools	0.1.18	Galaxy_Package	True	
/galaxy/main/deps/_conda/envs/__bowtie2@2.2.5	bowtie2	2.2.5	Conda	True	
/galaxy/main/deps/_conda/envs/__networkx@1.10	networkx	1.10	Conda	True	
/galaxy/main/deps/_conda/envs/__dunovo@2.0.9	dunovo	2.0.9	Conda	True	
	Convert SAM to BAM native - without sorting, Convert BAM native to BAM		samtools	0.1.18	Galaxy_Package	False	
	Du Novo: Make families, Du Novo: Make consensus reads	/galaxy/main/deps/_conda/envs/__dunovo@2.0.8	dunovo	2.0.8	Conda	True	
	CWPair2, RepMatch, GeneTrack		anaconda	2.3.0	Tool_Shed_Package	True	
	Admixture		gd_c_tools	0.1	Tool_Shed_Package	True	
matplotlib	1.2.1	Tool_Shed_Package	True	
	Du Novo: Make families, Du Novo: Make consensus reads	/galaxy/main/deps/_conda/envs/__dunovo@0.7.6	dunovo	0.7.6	Conda	True	
	RevertOriginalBaseQualitiesAndAddMateCigar, Downsample SAM/BAM, SamToFastq, CleanSam, RevertSam, Collect Alignment Summary Metrics, MergeSamFiles, ValidateSamFile, ReorderSam, EstimateLibraryComplexity, CollectWgsMetrics, BedToIntervalList, FixMateInformation, MarkDuplicates, AddCommentsToBam, MarkDuplicatesWithMateCigar, ReplaceSamHeader, NormalizeFasta, FastqToSam, SortSam, AddOrReplaceReadGroups, MergeBamAlignment, FilterSamReads	/galaxy/main/deps/_conda/envs/__picard@2.7.1	picard	2.7.1	Conda	True	
	Phylorelatives		R	2.15.0	Tool_Shed_Package	True	
rpy2	2.2.6	Tool_Shed_Package	True	
dendropy	3.12.0	Tool_Shed_Package	True	
ape	3.0-8	Tool_Shed_Package	True	
	Histogram, Histogram		rpy	1.0.3	Tool_Shed_Package	True	
R	2.11.0	Tool_Shed_Package	True	
	BamLeftAlign	/galaxy/main/deps/_conda/envs/mulled-v1-7908c324a80939762e495764fdccb0c1e5f50e19c2712e9182b5b952060b8323	freebayes	1.1.0.46	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-7908c324a80939762e495764fdccb0c1e5f50e19c2712e9182b5b952060b8323	samtools	0.1.19	Conda	True	
	MultiGPS	/galaxy/main/deps/_conda/envs/__multigps@0.73	multigps	0.73	Conda	True	
	Perform Linear Regression, Compute RCVE, Compute partial R square, Principal Component Analysis, Perform Logistic Regression with vif		R	2.11.0	Tool_Shed_Package	True	
numpy	1.7.1	Tool_Shed_Package	True	
rpy	1.0.3	Tool_Shed_Package	True	
	LinksBed, Multiple Intersect, ShuffleBed, ClosestBed, Genome Coverage, NucBed, JaccardBed, AnnotateBed, ReldistBed, ExpandBed, SubtractBed, GroupByBed, BED12 to BED6, SlopBed, BEDPE to BAM, TagBed, Merge BedGraph files, MapBed, SortBED, BED to IGV, FlankBed, BED to BAM, FisherBed, OverlapBed, ClusterBed, MergeBED, ComplementBed, MultiCovBed, Intersect intervals, GetFastaBed, MaskFastaBed, Compute both the depth and breadth of coverage, MakeWindowsBed, RandomBed, SpacingBed, WindowBed, Convert from BAM to FastQ	/galaxy/main/deps/_conda/envs/__bedtools@2.26.0gx	bedtools	2.26.0gx	Conda	True	
	BAM to BED		bedtools	2.24	Tool_Shed_Package	True	
samtools	1.2	Tool_Shed_Package	True	
	Du Novo: Make families, Du Novo: Make consensus reads	/galaxy/main/deps/_conda/envs/__dunovo@2.0.12	dunovo	2.0.12	Conda	True	
	Convert BAM to ScIdx		java-jdk	None	None	True	
	Map with BWA for Illumina, Map with BWA for SOLiD		bwa	0.5.9	Tool_Shed_Package	True	
	Create assemblies with Unicycler		unicycler	None	None	True	
	BEDPE to BAM, MergeBED, BED to BAM, Compute both the depth and breadth of coverage, OverlapBed, GetFastaBed, Convert from BAM to FastQ, RandomBed, Genome Coverage, NucBed, SpacingBed, ShuffleBed, TagBed, ExpandBed, FisherBed, SlopBed, ClusterBed, AnnotateBed, ClosestBed, JaccardBed, MakeWindowsBed, Merge BedGraph files, ComplementBed, LinksBed, Multiple Intersect, MultiCovBed, MapBed, GroupByBed, SortBED, ReldistBed, MaskFastaBed, BED12 to BED6, Intersect intervals, FlankBed, SubtractBed, WindowBed		bedtools	2.24	Tool_Shed_Package	True	
	Du Novo: Make consensus reads, Du Novo: Make families	/galaxy/main/deps/_conda/envs/__dunovo@0.7.1	dunovo	0.7.1	Conda	True	
	Phylogenetic Tree		phast	1.3	Tool_Shed_Package	True	
quicktree	1.1	Tool_Shed_Package	True	
gd_c_tools	0.1	Tool_Shed_Package	True	
	Vegan Diversity, Vegan Diversity, Vegan Fisher Alpha, Vegan Fisher Alpha, Vegan Rarefaction, Vegan Rarefaction		R	3.2.1	Tool_Shed_Package	True	
vegan	2.3-0	Tool_Shed_Package	True	
	MAFFT, MAFFT		mafft	7.221	Tool_Shed_Package	True	
	Multi-Join, Replace	/galaxy/main/deps/_conda/envs/__perl@5.22.0.1	perl	5.22.0.1	Conda	True	
	computeMatrix, plotPCA, computeGCBias, plotFingerprint, plotCorrelation, bamCompare, bigwigCompare, correctGCBias, multiBamSummary, plotProfile, bamPEFragmentSize, multiBigwigSummary, bamCoverage, plotCoverage, plotHeatmap		python	2.7.10	Tool_Shed_Package	True	
deepTools	2.2.3	Tool_Shed_Package	True	
	PCA		eigensoft	5.0.1	Tool_Shed_Package	True	
gd_c_tools	0.1	Tool_Shed_Package	True	
	Convert BedGraph to BigWig, Wig/BedGraph-to-bigWig, Convert Wiggle to BigWig, BED-to-bigBed, Convert genome coordinates, Extract Genomic DNA		ucsc_tools	2d6bafd63401	Galaxy_Package	True	
	Kernel Principal Component Analysis, Kernel Canonical Correlation Analysis		rpy	1.0.3	Tool_Shed_Package	True	
R	2.11.0	Tool_Shed_Package	True	
kernlab	0.1-4	Tool_Shed_Package	True	
numpy	1.7.1	Tool_Shed_Package	True	
bx-python	0.7.1	Tool_Shed_Package	True	
	Convert FASTA to 2bit		ucsc_tools	2d6bafd63401	Galaxy_Package	True	
ucsc-fatotwobit	None	None	True	
	DESeq2	/galaxy/main/deps/_conda/envs/__bioconductor-deseq2@1.12.4	bioconductor-deseq2	1.12.4	Conda	True	
	FASTQ joiner		galaxy_sequence_utils	1.0.1	Tool_Shed_Package	True	
	Diamond, Diamond makedb	/galaxy/main/deps/_conda/envs/__diamond@0.8.24	diamond	0.8.24	Conda	True	
	Du Novo: Align families	/galaxy/main/deps/_conda/envs/mulled-v1-fe2ba150b6be6062d84e131f2736fe2e44c208e5722d816c050ae994ef168ee1	mafft	7.221	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-fe2ba150b6be6062d84e131f2736fe2e44c208e5722d816c050ae994ef168ee1	dunovo	2.0.6	Conda	True	
	SnpEff Download, SnpEff, SnpEff Available Databases	/galaxy/main/deps/_conda/envs/__snpEff@4.1	snpEff	4.1	Conda	True	
	CollectBaseDistributionByCycle, CollectGcBiasMetrics, MeanQualityByCycle, QualityScoreDistribution, CollectInsertSizeMetrics	/galaxy/main/deps/_conda/envs/mulled-v1-30b510597e952e9f3fcec50e1aaa5cf69f57e435ca3be0d43209b4c776701159	picard	2.7.1	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-30b510597e952e9f3fcec50e1aaa5cf69f57e435ca3be0d43209b4c776701159	r	3.3.1	Conda	True	
	Kraken, Kraken-mpa-report, Kraken-mpa-report, Kraken-report, Kraken-translate, Kraken, Kraken-filter		kraken	0.10.5	Tool_Shed_Package	True	
	htseq-count	/galaxy/main/deps/_conda/envs/__htseq@0.6.1.post1	htseq	0.6.1.post1	Conda	True	
/galaxy/main/deps/_conda/envs/__samtools@1.3.1	samtools	1.3.1	Conda	True	
	Kraken taxonomic report	/galaxy/main/deps/_conda/envs/__biopython@1.66	biopython	1.66	Conda	True	
	Text reformatting, Replace Text		gnu_coreutils	8.22	Tool_Shed_Package	True	
gnu_awk	4.1.0	Tool_Shed_Package	True	
	Rank Pathways		mechanize	0.2.5	Tool_Shed_Package	True	
networkx	1.8.1	Tool_Shed_Package	True	
fisher	0.1.4	Tool_Shed_Package	True	
	Merge.sfffiles, Align.seqs, Filter.seqs, Get.label, Clearcut, Collect.single, Get.lineage, Get.group, Classify.seqs, Get.coremicrobiome, Get.seqs, unifrac.weighted, Cluster.split, Remove.rare, Collect.shared, Reverse.seqs, Unique.seqs, Heatmap.sim, Filter.shared, Get.oturep, Summary.seqs, Sub.sample, Anosim, Pre.cluster, Chimera.perseus, List.otulabels, Phylotype, Get.dists, Make.fastq, Count.seqs, Make.sra, Pcoa, Heatmap.bin, Sort.seqs, Screen.seqs, Rarefaction.single, Chimera.slayer, Seq.error, Pairwise.seqs, Get.otus, Get.otulist, Classify.rf, Lefse, Get.rabund, Get.sabund, Parsimony, Classify.otu, Dist.shared, Hcluster, Bin.seqs, Otu.hierarchy, Make.contigs, Summary.qual, Get.mimarkspackage, Remove.groups, Cluster, Trim.seqs, Get.relabund, Split.groups, Metastats, Trim.flows, Make.shared, Consensus.seqs, Parse.list, Make.lookup, Fastq.info, Amova, Cluster.fragments, Summary.shared, Remove.dists, Remove.otulabels, Count.groups, Shhh.flows, Remove.seqs, Chimera.uchime, List.seqs, Classify.tree, Pca, Corr.axes, Chimera.check, Remove.lineage, Remove.otus, Rarefaction.shared, Get.groups, Make.biom, Merge.taxsummary, Chimera.pintail, Libshuff, Align.check, Get.sharedseqs, Chimera.ccode, Make.lefse, Phylo.diversity, Chop.seqs, Split.abund, Create.database, Make.group, Shhh.seqs, Mantel, Cooccurrence, Get.communitytype, Deunique.seqs, Dist.seqs, Nmds, Get.otulabels, Get.mimarkspackage, Cluster.classic, Primer.design, Sffinfo, Homova, Summary.single, Degap.seqs, Venn, Normalize.shared, Otu.association, Chimera.bellerophon, Sens.spec, Tree.shared, unifrac.unweighted, Deunique.tree, Summary.tax, Make Design, Merge.groups, Merge.files, Pcr.seqs, Indicator	/galaxy/main/deps/_conda/envs/__mothur@1.36.1	mothur	1.36.1	Conda	True	
	Du Novo: Make consensus reads, Du Novo: Make families		duplex	0.5	Tool_Shed_Package	True	
	Du Novo: Align families	/galaxy/main/deps/_conda/envs/mulled-v1-0353b9854731ff3065503b435bdf01c35f6bc85fc90c9e4a09f229fba1b89630	mafft	7.221	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-0353b9854731ff3065503b435bdf01c35f6bc85fc90c9e4a09f229fba1b89630	dunovo	0.8.1	Conda	True	
	FreeBayes		freebayes	0.9.4_a46483351fd0196637614121868fb5c386612b55	Galaxy_Package	True	
samtools	0.1.18	Galaxy_Package	True	
	Venn Diagram		rpy	1.0.3	Tool_Shed_Package	True	
limma	3.25.3	Tool_Shed_Package	True	
biopython	1.65	Tool_Shed_Package	True	
	Bowtie2	/galaxy/main/deps/_conda/envs/mulled-v1-cf272fa72b0572012c68ee2cbf0c8f909a02f29be46918c2a23283da1d3d76b5	bowtie2	2.3.2	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-cf272fa72b0572012c68ee2cbf0c8f909a02f29be46918c2a23283da1d3d76b5	samtools	1.3.1	Conda	True	
	Quast	/galaxy/main/deps/_conda/envs/__quast@4.1	quast	4.1	Conda	True	
	Tag pileup frequency, Fasta nucleotide color plot, Paired-end histogram	/galaxy/main/deps/_conda/envs/__openjdk@8.0.112	openjdk	8.0.112	Conda	True	
	UniProt		requests	2.7	Tool_Shed_Package	True	
	DiffBind, DiffBind		R	3.0.3	Tool_Shed_Package	True	
deseq2	1.2.10	Tool_Shed_Package	True	
diffbind	1.8.3	Tool_Shed_Package	True	
	Convert Kraken	/galaxy/main/deps/_conda/envs/mulled-v1-2eeb0c3d0c128d0707b341faba47ce7ffc169623b7cf54efa3e77b462e57cf8d	gawk	4.1.0	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-2eeb0c3d0c128d0707b341faba47ce7ffc169623b7cf54efa3e77b462e57cf8d	gb_taxonomy_tools	1.0.0	Conda	True	
	Naive Variant Caller		numpy	1.7.1	Tool_Shed_Package	True	
pyBamParser	0.0.1	Tool_Shed_Package	True	
pyBamTools	0.0.1	Tool_Shed_Package	True	
	Du Novo: Align families	/galaxy/main/deps/_conda/envs/mulled-v1-f130555a7ab5a2897b0d3a6b9195fe3b5879290766ec6b1a17ad1e97c4b1cdf6	mafft	7.221	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-f130555a7ab5a2897b0d3a6b9195fe3b5879290766ec6b1a17ad1e97c4b1cdf6	dunovo	0.7.6	Conda	True	
	Sort, Unique lines, Text transformation		gnu_coreutils	8.22	Tool_Shed_Package	True	
gnu_sed	4.2.2-sandbox	Tool_Shed_Package	True	
	MACS2 predictd, MACS2 filterdup, MACS2 callpeak, MACS2 bdgpeakcall, MACS2 randsample, MACS2 refinepeak, MACS2 bdgcmp	/galaxy/main/deps/_conda/envs/__macs2@2.1.1.20160309	macs2	2.1.1.20160309	Conda	True	
	Depth of Coverage, Print Reads, Print Reads, Realigner Target Creator, Variant Annotator, Count Covariates, Indel Realigner, Table Recalibration, Unified Genotyper		gatk	1.4	Tool_Shed_Package	True	
samtools	0.1.18	Tool_Shed_Package	True	
	Unfold	/galaxy/main/deps/_conda/envs/__python@2.7.12	python	2.7.12	Conda	True	
	Filter nucleotides, Fetch Indels		bx-python	0.7.1	Tool_Shed_Package	True	
numpy	1.7.1	Tool_Shed_Package	True	
	Convert SAM to BigWig		ucsc_tools	2d6bafd63401	Galaxy_Package	True	
samtools	0.1.18	Galaxy_Package	True	
/galaxy/main/deps/_conda/envs/__bedtools@2.26.0gx	bedtools	2.26.0gx	Conda	True	
	Join	/galaxy/main/deps/_conda/envs/mulled-v1-847ae99728bb2431b099ad2cab1cf1859b8805b4e7102e055003c26bbbe7758a	coreutils	8.25	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-847ae99728bb2431b099ad2cab1cf1859b8805b4e7102e055003c26bbbe7758a	perl	5.22.0.1	Conda	True	
	Du Novo: Align families	/galaxy/main/deps/_conda/envs/mulled-v1-14032a88b7806086b841c7e6dc7f29083c747aefb73fbec58f8f72be672163e1	mafft	7.221	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-14032a88b7806086b841c7e6dc7f29083c747aefb73fbec58f8f72be672163e1	dunovo	2.0.12	Conda	True	
	octanol, seqmatchall, noreturn, transeq, extractfeat, cai, dreg, dotpath, getorf, skipseq, tcode, notseq, dottup, pepnet, prettyplot, shuffleseq, epestfind, needle, pepwheel, palindrome, vectorstrip, pepwindow, msbar, pepinfo, digest, fuzzpro, chips, nthseq, pepcoil, charge, patmatdb, maskfeat, cai custom, preg, btwisted, plotcon, polydot, sirna, freak, codcmp, cpgplot, splitter, maskseq, cusp, matcher, tmap, merger, revseq, megamerger, etandem, textsearch, primersearch, descseq, wordmatch, banana, dotmatcher, sixpack, degapseq, equicktandem, tranalign, seqret, showfeat, pepwindowall, oddcomp, fuzztran, newcpgreport, sigcleave, pepstats, water, syco, hmoment, antigenic, fuzznuc, extractseq, lindna, plotorf, chaos, wobble, isochore, backtranseq, infoseq, helixturnhelix, geecee, pasteseq, prettyseq, diffseq, wordcount, einverted, checktrans, cpgreport, coderet, marscan, supermatcher, union, twofeat, newseq, garnier, trimest, dan, est2genome, newcpgseek, trimseq, compseq, biosed, cutseq, iep, cirdna		emboss	5.0.0	Tool_Shed_Package	True	
	VSearch chimera detection, VSearch sorting, VSearch search, VSearch masking, VSearch alignment, VSearch shuffling, VSearch dereplication, VSearch clustering		vsearch	1.1.3	Tool_Shed_Package	True	
	Heatmap		R	2.15.0	Tool_Shed_Package	True	
	correctGCBias, plotProfile, bamPEFragmentSize, multiBigwigSummary, bamCoverage, plotCoverage, plotHeatmap, computeMatrix, bamCompare, plotPCA, computeGCBias, plotFingerprint, plotCorrelation, multiBamSummary, bigwigCompare		python	2.7.10	Tool_Shed_Package	True	
deepTools	2.2.2	Tool_Shed_Package	True	
	Du Novo: Align families	/galaxy/main/deps/_conda/envs/mulled-v1-b559d765315381cd6b4be00ffc83c475ed0d4750cc08eb357d85bb02e08d1b03	mafft	7.221	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-b559d765315381cd6b4be00ffc83c475ed0d4750cc08eb357d85bb02e08d1b03	dunovo	0.7.1	Conda	True	
	LPS		lps_tool	None	None	True	
	SnpEff Available Databases, SnpEff, SnpEff Download		snpEff	4.0	Tool_Shed_Package	True	
	FASTQ joiner, FASTQ Masker, Manipulate FASTQ, FASTQ to FASTA, FASTQ Summary Statistics, FASTQ splitter, FASTQ Trimmer, Tabular to FASTQ, FASTQ Quality Trimmer, FASTQ Groomer, Combine FASTA and QUAL, Filter FASTQ, FASTQ to Tabular		galaxy_sequence_utils	1.0.0	Tool_Shed_Package	True	
	hifive	/galaxy/main/deps/_conda/envs/__hifive@1.3	hifive	1.3	Conda	True	
	PASS		pass	None	None	True	
	featureCounts	/galaxy/main/deps/_conda/envs/__subread@1.4.6p5	subread	1.4.6p5	Conda	True	
	Convert, Merge, Randomize, Convert, Merge, Randomize		bamtools	2.3.0_2d7685d2ae	Tool_Shed_Package	True	
samtools	0.1.18	Tool_Shed_Package	True	
	BedCov, Split, Reheader, CalMD, Sort, MPileup, Stats, SAM-to-BAM, IdxStats, RmDup, Slice	/galaxy/main/deps/_conda/envs/__samtools@1.3.1	samtools	1.3.1	Conda	True	
	VCFleftAlign:, VcfAllelicPrimitives:, VCFprimers:, VCFgenotype-to-haplotype:, VCFhetHomAlleles:, VCFtoTab-delimited:, VCFaddinfo:, VCFflatten:, VCFcombine:, VCFselectsamples:, VCF-VCFintersect:, VCFannotateGenotypes:, VCFannotate:, VCFfixup:, VCFgenotypes:, VCFcommonSamples:, VCFrandomSample:, VCFdistance:, VCF-BEDintersect:, VCFcheck:, VCFbreakCreateMulti:	/galaxy/main/deps/_conda/envs/__vcflib@1.0.0_rc1	vcflib	1.0.0_rc1	Conda	True	
	MAF boxplot		R	2.15.0	Tool_Shed_Package	True	
rpy2	2.2.6	Tool_Shed_Package	True	
numpy	1.7.1	Tool_Shed_Package	True	
	HISAT2, HISAT2	/galaxy/main/deps/_conda/envs/mulled-v1-2bb67013a57cac1e35f407d06d1f347baae35159f498496f1e36f84784069212	hisat2	2.0.5	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-2bb67013a57cac1e35f407d06d1f347baae35159f498496f1e36f84784069212	samtools	1.4	Conda	True	
	plotProfile, bamCompare, bamPEFragmentSize, plotPCA, computeGCBias, plotHeatmap, plotCorrelation, plotEnrichment, bigwigCompare, plotCoverage, bamCoverage, multiBigwigSummary, multiBamSummary, correctGCBias, plotFingerprint, computeMatrix	/galaxy/main/deps/_conda/envs/__python@2.7.10	python	2.7.10	Conda	True	
/galaxy/main/deps/_conda/envs/__deepTools@2.3.5	deepTools	2.3.5	Conda	True	
	BamLeftAlign	/galaxy/main/deps/_conda/envs/mulled-v1-2b107edf93f80372b6ce9328129dac3c314eb966bbb151da7760dcae4d80200d	freebayes	1.0.2.29	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-2b107edf93f80372b6ce9328129dac3c314eb966bbb151da7760dcae4d80200d	samtools	0.1.19	Conda	True	
	DESeq2	/galaxy/main/deps/_conda/envs/__r-getopt@1.20.0	r-getopt	1.20.0	Conda	True	
/galaxy/main/deps/_conda/envs/__r-gplots@2.17.0	r-gplots	2.17.0	Conda	True	
/galaxy/main/deps/_conda/envs/__r-rjson@0.2.15	r-rjson	0.2.15	Conda	True	
/galaxy/main/deps/_conda/envs/__bioconductor-deseq2@_uv_	bioconductor-deseq2	None	Conda	False	
	Trim Galore!, Trim Galore!		cutadapt	1.8	Tool_Shed_Package	True	
	Generate pileup format, Extract reads, Extract reads	/galaxy/main/deps/_conda/envs/__sra-tools@2.8.0	sra-tools	2.8.0	Conda	True	
	HISAT2		hisat	2.0	Tool_Shed_Package	True	
samtools	1.2	Tool_Shed_Package	True	
hisat2	None	None	True	
	SDF to SMILES, MOL to CML, InChI to MOL, MOL to SMILES, MOL2 to SDF, MOL2 to SMILES, InChI to CML, SMILES to InChI, InChI to SMILES, SMILES to SDF, SMILES to MOL, InChI to MOL2, CML to SDF, SMILES to MOL2, SDF to mol2, CML to mol2, MOL2 to MOL, SMILES to SMILES, MOL to MOL2, InChI to SDF, CML to SMILES, SMILES to CML, MOL2 to InChI, SDF to CML, MOL2 to CML, SDF to InChI, CML to InChI		openbabel	None	None	True	
	Split, Split, Filter, Filter		bamtools	2.3.0_2d7685d2ae	Tool_Shed_Package	True	
	Convert SAM to BAM		samtools	0.1.18	Galaxy_Package	True	
	FastQC		FastQC	0.11.2	Tool_Shed_Package	True	
	Du Novo: Align families		mafft	7.221	Tool_Shed_Package	True	
duplex	0.5	Tool_Shed_Package	True	
	Bowtie2		bowtie2	2.1.0	Tool_Shed_Package	True	
samtools	0.1.18	Tool_Shed_Package	True	
	Call SNPS with Freebayes		freebayes	0.9.6_9608597d12e127c847ae03aa03440ab63992fedf	Tool_Shed_Package	True	
samtools	0.1.16	Tool_Shed_Package	True	
	Sailfish		sailfish	0.7.6	Tool_Shed_Package	True	
	cd-hit-dup		cd-hit-auxtools	0.5-2012-03-07-fix-dan-gh-0.0.1	Tool_Shed_Package	True	
	Charts		R	3.0.3	Tool_Shed_Package	True	
charts_r_packages	1.0	Tool_Shed_Package	True	
	BamLeftAlign, FreeBayes		freebayes	freebayes-0.9.14_8a407cf5f4	Tool_Shed_Package	True	
samtools	0.1.18	Tool_Shed_Package	True	
	MACS2 randsample, MACS2 bdgcmp, MACS2 filterdup, MACS2 refinepeak, MACS2 bdgdiff		macs2	2.1.0	Tool_Shed_Package	True	
numpy	1.7.1	Tool_Shed_Package	True	
scipy	0.12.0	Tool_Shed_Package	True	
	MINE		MINE	1.0.1	Tool_Shed_Package	True	
	Cuffdiff, Cuffdiff, Cuffdiff		cufflinks	2.2.1	Tool_Shed_Package	True	
cummeRbund	2.8.2	Tool_Shed_Package	True	
	FreeBayes, FreeBayes, BamLeftAlign		freebayes	0_9_20_b040236	Tool_Shed_Package	True	
samtools	0.1.18	Tool_Shed_Package	True	
	Diamond, Diamond, Diamond makedb		diamond	0.6.13	Tool_Shed_Package	True	
	Convert uncompressed BCF to BCF, Set External Metadata, Convert BCF to uncompressed BCF		bcftools	None	None	True	
	aaChanges		ucsc_tools	2d6bafd63401	Galaxy_Package	True	
gnu_coreutils	None	None	True	
	computeGCBias, plotCoverage, multiBamSummary, plotPCA, computeMatrix, bamCoverage, correctGCBias, multiBigwigSummary, plotProfile, plotEnrichment, plotFingerprint, bamCompare, plotCorrelation, bigwigCompare, bamPEFragmentSize, plotHeatmap	/galaxy/main/deps/_conda/envs/mulled-v1-0fa290085c742a3ffee6a142d1fce47c178e1c289ff6f0c66023b506f3377842	python	2.7.10	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-0fa290085c742a3ffee6a142d1fce47c178e1c289ff6f0c66023b506f3377842	deeptools	2.5.0	Conda	True	
	Make.shared	/galaxy/main/deps/_conda/envs/__mothur@_uv_	mothur	1.27	Conda	False	
	BAM filter		pysam	0.7.7	Tool_Shed_Package	True	
	StringTie		stringtie	1.0.3	Tool_Shed_Package	True	
	Generate pileup, Generate pileup		samtools	0.1.16	Tool_Shed_Package	True	
	Plotting tool, Perform LDA, T Test for Two Samples, Draw ROC plot		R	2.11.0	Tool_Shed_Package	True	
	Du Novo: Correct barcodes		samtools	0.1.18	Galaxy_Package	True	
/galaxy/main/deps/_conda/envs/__bowtie2@2.2.5	bowtie2	2.2.5	Conda	True	
/galaxy/main/deps/_conda/envs/__networkx@1.10	networkx	1.10	Conda	True	
/galaxy/main/deps/_conda/envs/__dunovo@2.0.8	dunovo	2.0.8	Conda	True	
	Merge.sfffiles, Sort.seqs, Mantel, Summary.single, Remove.otus, Get.seqs, Tree.shared, List.seqs, Heatmap.bin, Get.otulabels, Cluster.classic, Make Design, Split.groups, Libshuff, Classify.otu, Screen.seqs, Get.oturep, Phylo.diversity, Get.coremicrobiome, Metastats, Reverse.seqs, Count.seqs, Heatmap.sim, Trim.flows, Indicator, Deunique.tree, Nmds, Amova, Bin.seqs, Chimera.uchime, Sens.spec, unifrac.weighted, unifrac.unweighted, Merge.groups, Cluster.split, Normalize.shared, Make.biom, Split.abund, Get.groups, Get.relabund, Cluster.fragments, Hcluster, Summary.seqs, Degap.seqs, Otu.hierarchy, Chimera.slayer, Parsimony, Filter.seqs, Summary.tax, Pcoa, Dist.shared, Phylotype, Summary.qual, Otu.association, Pcr.seqs, Create.database, Dist.seqs, Make.contigs, Make.group, Count.groups, Pairwise.seqs, Remove.rare, Pre.cluster, Pca, Make.fastq, Get.rabund, Consensus.seqs, Chimera.perseus, Remove.seqs, Get.otulist, Chimera.pintail, Remove.lineage, Align.check, Venn, Get.sharedseqs, Seq.error, Clearcut, Cooccurrence, Make.shared, Get.otus, Sub.sample, List.otulabels, Get.lineage, Collect.shared, Parse.list, Cluster, Anosim, Chimera.bellerophon, Get.sabund, Unique.seqs, Homova, Classify.tree, Chop.seqs, Corr.axes, Sffinfo, Shhh.flows, Trim.seqs, Remove.groups, Classify.seqs, Fastq.info, Rarefaction.single, Deunique.seqs, Align.seqs, Shhh.seqs, Rarefaction.shared, Merge.files, Chimera.check, Chimera.ccode, Collect.single, Summary.shared, Remove.otulabels, Get.group	/galaxy/main/deps/_conda/envs/__mothur@_uv_	mothur	1.33	Conda	False	
	DiffBind	/galaxy/main/deps/_conda/envs/__bioconductor-diffbind@2.0.9	bioconductor-diffbind	2.0.9	Conda	True	
	DEXSeq-Count	/galaxy/main/deps/_conda/envs/mulled-v1-98ffce4c4501f036e67e530b7fca7a55847d02e3ed12ce55610e26f6c5c66184	bioconductor-dexseq	1.20.1	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-98ffce4c4501f036e67e530b7fca7a55847d02e3ed12ce55610e26f6c5c66184	htseq	0.6.1.post1	Conda	True	
	FreeBayes	/galaxy/main/deps/_conda/envs/mulled-v1-86c3826a131601a0d3bd63754534b10e4c0fe99870b6da9494e693f2e0b6ea8a	freebayes	1.0.2.29	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-86c3826a131601a0d3bd63754534b10e4c0fe99870b6da9494e693f2e0b6ea8a	samtools	0.1.19	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-86c3826a131601a0d3bd63754534b10e4c0fe99870b6da9494e693f2e0b6ea8a	gawk	4.1.3	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-86c3826a131601a0d3bd63754534b10e4c0fe99870b6da9494e693f2e0b6ea8a	parallel	20160622	Conda	True	
	GPASS		gpass	None	None	True	
	Prokka	/galaxy/main/deps/_conda/envs/__prokka@1.12	prokka	1.12	Conda	True	
	MACS		macs	1.3.7.1	Tool_Shed_Package	True	
R	2.15.0	Tool_Shed_Package	True	
	Summary Statistics		rpy2	None	None	True	
	Du Novo: Make consensus reads, Du Novo: Make families		duplex	0.3	Tool_Shed_Package	True	
	MACS2 bdgpeakcall, MACS2 bdgbroadcall		macs2	2.1.0.20151222	Tool_Shed_Package	True	
numpy	1.7.1	Tool_Shed_Package	True	
scipy	0.12.0	Tool_Shed_Package	True	
gnu_awk	4.1.0	Tool_Shed_Package	True	
	VCFannotateGenotypes:, VCFgenotypes:, VCFcheck:, VCFannotate:, VCFcombine:, VCFprimers:, VCF-VCFintersect:, VCFcommonSamples:, VCFfixup:, VCF-BEDintersect:, VCFcombine:, VCFtoTab-delimited:, VcfAllelicPrimitives:, VCFflatten:, VCFselectsamples:, VCFrandomSample:, VCFleftAlign:, VCFgenotype-to-haplotype:, VCFhetHomAlleles:, VCFbreakCreateMulti:, VCFaddinfo:, VCFdistance:		vcflib	8a5602bf07	Tool_Shed_Package	True	
	FilterSamReads, CollectWgsMetrics, ReorderSam, CleanSam, Downsample SAM/BAM, MeanQualityByCycle, CollectRnaSeqMetrics, ValidateSamFile, CollectInsertSizeMetrics, AddCommentsToBam, RevertSam, BedToIntervalList, AddOrReplaceReadGroups, ReplaceSamHeader, MarkDuplicates, NormalizeFasta, MarkDuplicatesWithMateCigar, MergeSamFiles, MergeBamAlignment, QualityScoreDistribution, FastqToSam, CollectBaseDistributionByCycle, SortSam, SamToFastq, Collect Alignment Summary Metrics, EstimateLibraryComplexity, CollectGcBiasMetrics, FixMateInformation, RevertOriginalBaseQualitiesAndAddMateCigar		picard	1.126.0	Tool_Shed_Package	True	
	Unique lines, Sort	/galaxy/main/deps/_conda/envs/mulled-v1-e511683d0527bc680e67aa6edc3a555941fbfc7d89fdeb82b761a91f01cfbdc2	coreutils	8.25	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-e511683d0527bc680e67aa6edc3a555941fbfc7d89fdeb82b761a91f01cfbdc2	sed	4.2.3.dev0	Conda	True	
	ClustalW		clustalw2	2.1	Tool_Shed_Package	True	
	Boxplot		gnuplot	None	None	True	
	RNA Structure Prediction		rnastructure	5.7	Tool_Shed_Package	True	
biopython	1.61	Tool_Shed_Package	True	
numpy	1.7.1	Tool_Shed_Package	True	
imaging	1.1.7	Tool_Shed_Package	True	
matplotlib	1.2.1	Tool_Shed_Package	True	
vienna_rna	2.1	Tool_Shed_Package	True	
	Build base quality distribution		fontconfig	2.11.1	Tool_Shed_Package	True	
rpy	1.0.3	Tool_Shed_Package	True	
R	2.11.0	Tool_Shed_Package	True	
	Krona pie chart		krona	None	None	True	
	gffread, Cuffnorm, Cufflinks, Cuffquant, Cuffnorm, Cuffcompare, Cuffmerge		cufflinks	2.2.1	Tool_Shed_Package	True	
	Varscan		varscan	2.3.6	Tool_Shed_Package	True	
	CollectRnaSeqMetrics	/galaxy/main/deps/_conda/envs/mulled-v1-22c0de12eea3f3115fdab2aa8793bee0f918b31abefb5a08f29f19d80268b388	picard	2.7.1	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-22c0de12eea3f3115fdab2aa8793bee0f918b31abefb5a08f29f19d80268b388	r	3.3.1	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-22c0de12eea3f3115fdab2aa8793bee0f918b31abefb5a08f29f19d80268b388	ucsc-gff3togenepred	324	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-22c0de12eea3f3115fdab2aa8793bee0f918b31abefb5a08f29f19d80268b388	ucsc-gtftogenepred	324	Conda	True	
	snpFreq		R	2.11.0	Tool_Shed_Package	True	
bioc_qvalue	1.34.0	Tool_Shed_Package	True	
	MACS2 predictd		macs2	2.1.0.20151222	Tool_Shed_Package	True	
numpy	1.7.1	Tool_Shed_Package	True	
scipy	0.12.0	Tool_Shed_Package	True	
R	3.1.2	Tool_Shed_Package	True	
gnu_awk	4.1.0	Tool_Shed_Package	True	
	Convert BAM to BigWig, Convert BED, GFF, or VCF to BigWig, Convert Genomic Intervals To Coverage		ucsc_tools	2d6bafd63401	Galaxy_Package	True	
/galaxy/main/deps/_conda/envs/__bedtools@2.26.0gx	bedtools	2.26.0gx	Conda	True	
	Slice VCF, Annotate		vcftools	0.1.11	Tool_Shed_Package	True	
	Bowtie2, Bowtie2		bowtie2	2.2.4	Tool_Shed_Package	True	
samtools	0.1.18	Tool_Shed_Package	True	
	VCFfilter:	/galaxy/main/deps/_conda/envs/__vcflib@1.0.0_rc1	vcflib	1.0.0_rc1	Conda	True	
/galaxy/main/deps/_conda/envs/__htslib@1.3	htslib	1.3	Conda	True	
	Map with BWA-MEM, Map with BWA	/galaxy/main/deps/_conda/envs/mulled-v1-994f58669c7f0a5092618845c7bd05d42f5d84b22abfcc4dabae3085827efb35	bwa	0.7.15	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-994f58669c7f0a5092618845c7bd05d42f5d84b22abfcc4dabae3085827efb35	samtools	1.3.1	Conda	True	
	FLASH, FLASH	/galaxy/main/deps/_conda/envs/__flash@1.2.11	flash	1.2.11	Conda	True	
	BAM to BED	/galaxy/main/deps/_conda/envs/__bedtools@2.26.0gx	bedtools	2.26.0gx	Conda	True	
samtools	0.1.18	Galaxy_Package	False	
	Lastz		lastz	1.02.00	Tool_Shed_Package	True	
	HISAT		hisat	2.0.3	Tool_Shed_Package	True	
samtools	1.2	Tool_Shed_Package	True	
hisat2	None	None	True	
	DiffBind	/galaxy/main/deps/_conda/envs/__bioconductor-diffbind@1.16.3	bioconductor-diffbind	1.16.3	Conda	True	
	Cluster KEGG		networkx	1.8.1	Tool_Shed_Package	True	
	Krona pie chart	/galaxy/main/deps/_conda/envs/__krona@2.6.1	krona	2.6.1	Conda	True	
	Map with BWA-MEM, Map with BWA-MEM, Map with BWA, Map with BWA		bwa	0.7.12	Tool_Shed_Package	True	
samtools	1.2	Tool_Shed_Package	True	
	Scatterplot, Correlation		rpy	1.0.3	Tool_Shed_Package	True	
	TopHat		bowtie2	2.2.5	Tool_Shed_Package	True	
tophat	2.0.14	Tool_Shed_Package	True	
	Perform Best-subsets Regression		numpy	1.7.1	Tool_Shed_Package	True	
rpy	1.0.3	Tool_Shed_Package	True	
	Du Novo: Correct barcodes	/galaxy/main/deps/_conda/envs/mulled-v1-b7caf2c381afc0e1286e0fb52fe19fefc3e854ba02aa179d1113939d557b6d60	bowtie	1.1.2	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-b7caf2c381afc0e1286e0fb52fe19fefc3e854ba02aa179d1113939d557b6d60	networkx	1.10	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-b7caf2c381afc0e1286e0fb52fe19fefc3e854ba02aa179d1113939d557b6d60	dunovo	2.0.12	Conda	True	
	Search in textfiles		gnu_coreutils	8.22	Tool_Shed_Package	True	
gnu_grep	2.14	Tool_Shed_Package	True	
	MACS2 callpeak		macs2	2.1.0.20151222	Tool_Shed_Package	True	
numpy	1.7.1	Tool_Shed_Package	True	
scipy	0.12.0	Tool_Shed_Package	True	
R	3.1.2	Tool_Shed_Package	True	
	Extract reads in Fastq/a, Download and Extract Reads in FASTA/Q, Generate pileup format, Extract reads in BAM	/galaxy/main/deps/_conda/envs/__sra-tools@2.8.1	sra-tools	2.8.1	Conda	True	
	Kraken-report, Kraken-filter, Kraken, Kraken-translate, Kraken-mpa-report		kraken	0.10.6-eaf8fb68	Tool_Shed_Package	True	
/galaxy/main/deps/_conda/envs/__kraken@0.10.6_eaf8fb68	kraken	0.10.6_eaf8fb68	Conda	True	
	Cut, Column Join, Join, Select first, Unfold, tac, Unique, Create text file, Concatenate datasets, Select last		gnu_coreutils	8.22	Tool_Shed_Package	True	
	Du Novo: Align families	/galaxy/main/deps/_conda/envs/mulled-v1-c77382b2a3e0d44c8702222f555374548f21046caa59992e83048068f0d6c5ea	mafft	7.221	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-c77382b2a3e0d44c8702222f555374548f21046caa59992e83048068f0d6c5ea	dunovo	2.0.8	Conda	True	
	VCFfilter:		vcflib	8a5602bf07	Tool_Shed_Package	True	
tabix	0.2.6	Tool_Shed_Package	True	
	multiqc	/galaxy/main/deps/_conda/envs/__multiqc@1.0.0	multiqc	1.0.0	Conda	True	
	htseq-count		htseq	0.6.1	Tool_Shed_Package	True	
numpy	1.7.1	Tool_Shed_Package	True	
samtools	0.1.19	Tool_Shed_Package	True	
pysam	0.7.7	Tool_Shed_Package	True	
	MEME, FIMO		graphicsmagick	1.3.20	Tool_Shed_Package	True	
meme	4.11.1	Tool_Shed_Package	True	
	Pathway Image		mechanize	0.2.5	Tool_Shed_Package	True	
	Du Novo: Make families, Du Novo: Make consensus reads	/galaxy/main/deps/_conda/envs/__dunovo@2.0.9	dunovo	2.0.9	Conda	True	
	GEMINI Download		gemini	0.18.1	Tool_Shed_Package	True	
	Map with Bowtie for Illumina, Map with Bowtie for SOLiD		bowtie	0.12.7	Tool_Shed_Package	True	
	Tophat, Tophat2		samtools	0.1.18	Tool_Shed_Package	True	
bowtie2	2.1.0	Tool_Shed_Package	True	
tophat2	2.0.9	Tool_Shed_Package	True	
	Trinity		bowtie	0.12.7	Galaxy_Package	False	
samtools	0.1.18	Galaxy_Package	False	
java	None	None	True	
perl	None	None	True	
trinity	None	None	True	
	Iterative Mapping		biopython	1.61	Tool_Shed_Package	True	
numpy	1.7.1	Tool_Shed_Package	True	
samtools	0.1.18	Tool_Shed_Package	True	
bowtie	0.12.7	Tool_Shed_Package	True	
	StringTie, StringTie	/galaxy/main/deps/_conda/envs/__stringtie@1.3.3	stringtie	1.3.3	Conda	True	
	Du Novo: Correct barcodes		samtools	0.1.18	Galaxy_Package	True	
/galaxy/main/deps/_conda/envs/__bowtie2@2.2.5	bowtie2	2.2.5	Conda	True	
/galaxy/main/deps/_conda/envs/__networkx@1.9	networkx	1.9	Conda	True	
/galaxy/main/deps/_conda/envs/__dunovo@0.8.1	dunovo	0.8.1	Conda	True	
	Krona pie chart		krona	2.5	Tool_Shed_Package	True	
	FastQC, FastQC		FastQC	0.11.4	Tool_Shed_Package	True	
	Naive Variant Caller		numpy	1.7.1	Tool_Shed_Package	True	
pyBamParser	0.0.1	Tool_Shed_Package	True	
pyBamTools	0.0.2	Tool_Shed_Package	True	
	Salmon	/galaxy/main/deps/_conda/envs/__salmon@0.7.2	salmon	0.7.2	Conda	True	
bzip2	None	None	True	
	Convert FASTA to fai file		samtools	0.1.18	Galaxy_Package	False	
	Analyze Covariates		gatk	1.4	Tool_Shed_Package	True	
R	2.11.0	Tool_Shed_Package	True	
	ANNOVAR Annotate VCF, ANNOVAR Annotate VCF		annovar	20140211	Galaxy_Package	True	
	Du Novo: Correct barcodes		samtools	0.1.18	Galaxy_Package	True	
/galaxy/main/deps/_conda/envs/__bowtie2@2.2.5	bowtie2	2.2.5	Conda	True	
/galaxy/main/deps/_conda/envs/__networkx@1.9	networkx	1.9	Conda	True	
/galaxy/main/deps/_conda/envs/__dunovo@0.7.6	dunovo	0.7.6	Conda	True	
	GEMINI load, GEMINI region, GEMINI qc, GEMINI fusions, GEMINI dump, GEMINI mendel_errors, GEMINI set_somatic, GEMINI autosomal recessive/dominant, GEMINI de_novo, GEMINI interactions, GEMINI amend, GEMINI query, GEMINI windower, GEMINI annotate, GEMINI db_info, GEMINI stats, GEMINI actionable_mutations, GEMINI gene_wise, GEMINI burden, GEMINI roh, GEMINI comp_hets, GEMINI lof_sieve, GEMINI pathways		gemini	0.18.1	Tool_Shed_Package	True	
tabix	0.2.6	Tool_Shed_Package	True	
	Du Novo: Align families		mafft	7.221	Tool_Shed_Package	True	
duplex	0.3	Tool_Shed_Package	True	
	VSearch alignment, VSearch clustering, VSearch search, VSearch dereplication, VSearch masking, VSearch shuffling, VSearch chimera detection, VSearch sorting		vsearch	1.9.7	Tool_Shed_Package	True	
	Beta Diversity	/galaxy/main/deps/_conda/envs/__scikit-bio@0.4.2	scikit-bio	0.4.2	Conda	True	
	fastq-join		ea-utils	1.1.2-806	Tool_Shed_Package	True	
	Tophat Fusion Post		blast+	2.2.28	Tool_Shed_Package	True	
bowtie	0.12.7	Tool_Shed_Package	True	
tophat2	2.0.9	Tool_Shed_Package	True	
	Draw variants, Pairs sequenced, Filter SNPs, Inbreeding and kinship, Aggregate Individuals, Close relatives, Per-SNP FSTs, Nucleotide Diversity, Founders sequenced, Remarkable Intervals, Diversity, Prepare Input, Overall FST, Coverage Distributions		gd_c_tools	0.1	Tool_Shed_Package	True	
	MEME		meme	4.11.0	Tool_Shed_Package	True	
	Extract Orthologous Microsatellites		sputnik	1.0	Tool_Shed_Package	True	
	Reheader, MPileup, MPileup, MPileup, RmDup, Stats, BedCov, SAM-to-BAM, SAM-to-BAM, Sort, IdxStats, BAM-to-SAM, Flagstat, Slice, CalMD, Split, Filter SAM or BAM, output SAM or BAM		samtools	1.2	Tool_Shed_Package	True	
	Intersect, Estimate Indel Rates, Get flanks, Base Coverage, Complement, Estimate microsatellite mutability, Subtract, Cluster, Feature coverage, Concatenate, Assign weighted-average, Assign weighted-average, Coverage, Join, Merge, Fetch closest non-overlapping feature, Subtract Whole Dataset		bx-python	0.7.1	Tool_Shed_Package	True	
galaxy-ops	1.0.0	Tool_Shed_Package	True	
	BEAM		beam	None	None	True	
	Du Novo: Correct barcodes		samtools	0.1.18	Galaxy_Package	True	
/galaxy/main/deps/_conda/envs/__bowtie2@2.2.5	bowtie2	2.2.5	Conda	True	
/galaxy/main/deps/_conda/envs/__networkx@1.9	networkx	1.9	Conda	True	
/galaxy/main/deps/_conda/envs/__dunovo@0.7.1	dunovo	0.7.1	Conda	True	
	IWTomics Load, IWTomics Test, IWTomics Plot with Threshold	/galaxy/main/deps/_conda/envs/__bioconductor-iwtomics@1.0.0	bioconductor-iwtomics	1.0.0	Conda	True	
	metagenomeSeq Normalization	/galaxy/main/deps/_conda/envs/mulled-v1-1b6d7f4b1875e64dd0a2597677f7cbf971bfff326c6e9c1334ce3d677d5b9770	bioconductor-metagenomeseq	1.16.0	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-1b6d7f4b1875e64dd0a2597677f7cbf971bfff326c6e9c1334ce3d677d5b9770	bioconductor-biomformat	1.2.0	Conda	True	
	Count GFF Features, Concatenate, Profile Annotations, Mask CpG/non-CpG sites		bx-python	0.7.1	Tool_Shed_Package	True	
	StringTie		stringtie	1.1.0	Tool_Shed_Package	True	
	FastQC:Read QC		FastQC	0.10.1	Tool_Shed_Package	True	
	RNA STAR	/galaxy/main/deps/_conda/envs/mulled-v1-c9a597a010e74b65cc39e1a315ac4c91ee474e7437f09b393086009fa3edec52	star	2.5.2b	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-c9a597a010e74b65cc39e1a315ac4c91ee474e7437f09b393086009fa3edec52	samtools	0.1.19	Conda	True	
	Sequence Logo		numpy	1.7.1	Tool_Shed_Package	True	
weblogo	3.3	Tool_Shed_Package	True	
ghostscript	9.10	Tool_Shed_Package	True	
	Trim Galore!		cutadapt	1.8	Tool_Shed_Package	True	
cutadapt	None	None	True	
	HISAT2		hisat	2.0	Tool_Shed_Package	True	
samtools	1.2	Tool_Shed_Package	True	
	FreeBayes		freebayes	0.9.6_9608597d12e127c847ae03aa03440ab63992fedf	Tool_Shed_Package	True	
samtools	0.1.18	Tool_Shed_Package	True	
	Du Novo: Align families	/galaxy/main/deps/_conda/envs/mulled-v1-5a117175398634d1cb620e7f4973c567c8f25a2c2d9eb033b17121e640848692	mafft	7.221	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-5a117175398634d1cb620e7f4973c567c8f25a2c2d9eb033b17121e640848692	dunovo	2.0.9	Conda	True	
	Select first, Unique, Create text file, Select last, Cut, tac	/galaxy/main/deps/_conda/envs/__coreutils@8.25	coreutils	8.25	Conda	True	
	TopHat		bowtie2	2.2.5	Tool_Shed_Package	True	
tophat	2.1.0	Tool_Shed_Package	True	
	Rank Terms		fisher	0.1.4	Tool_Shed_Package	True	
	Trimmomatic, Trimmomatic	/galaxy/main/deps/_conda/envs/__trimmomatic@0.36	trimmomatic	0.36	Conda	True	
	BWA-MEM, BWA		bwa	0.7.10.039ea20639	Tool_Shed_Package	True	
samtools	1.1	Tool_Shed_Package	True	
	Megablast		blast+	2.2.26+	Tool_Shed_Package	True	
bx-python	0.7.1	Tool_Shed_Package	True	
	MEME, FIMO, FIMO		imagemagick	6.9.3	Tool_Shed_Package	True	
meme	4.11.0	Tool_Shed_Package	True	
	FastQC, FastQC, FastQC	/galaxy/main/deps/_conda/envs/__fastqc@0.11.5	fastqc	0.11.5	Conda	True	
	VCFfilter:, VCFannotate:, VCFgenotype-to-haplotype:, VCFcombine:, VCFhetHomAlleles:, VCFleftAlign:, VCFaddinfo:, VCFannotateGenotypes:, VCF-BEDintersect:, VCFgenotypes:, VcfAllelicPrimitives:, VCFrandomSample:, VCFcommonSamples:, VCFdistance:, VCFcheck:, VCFtoTab-delimited:, VCFbreakCreateMulti:, VCF-VCFintersect:, VCFprimers:, VCFselectsamples:, VCFfixup:		vcflib	86723982aa	Tool_Shed_Package	True	
	FASTQ interlacer, FASTQ joiner, FASTQ Groomer, Combine FASTA and QUAL, Filter FASTQ, FASTQ to FASTA, FASTQ de-interlacer, FASTQ to Tabular, FASTQ Masker, Manipulate FASTQ, FASTQ Summary Statistics, FASTQ splitter	/galaxy/main/deps/_conda/envs/__galaxy_sequence_utils@1.1.1	galaxy_sequence_utils	1.1.1	Conda	True	
	Join two Datasets		python	None	None	True	
	Karyotype Plotting tool		R	2.15.0	Tool_Shed_Package	True	
gtools	3.4.1	Tool_Shed_Package	True	
	Kraken-report, Kraken-filter, Kraken, Kraken-translate, Kraken-mpa-report	/galaxy/main/deps/_conda/envs/__kraken@0.10.6_eaf8fb68	kraken	0.10.6_eaf8fb68	Conda	True	
	Salmon	/galaxy/main/deps/_conda/envs/mulled-v1-a1f40c8f725199402017692f0ee9345282556bcfde2909bd69e10c407932ea3a	bzip2	1.0.6	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-a1f40c8f725199402017692f0ee9345282556bcfde2909bd69e10c407932ea3a	salmon	0.8.2	Conda	True	
	Multi-Join		gnu_coreutils	8.22	Tool_Shed_Package	True	
perl	5.18.1	Tool_Shed_Package	True	
text_processing_perl_packages	1.0	Tool_Shed_Package	True	
	Trimmomatic		trimmomatic	0.32	Tool_Shed_Package	True	
	Search in textfiles	/galaxy/main/deps/_conda/envs/mulled-v1-c67ff3dedf9d4e2994768e8fccd955481d20876b71a51e5dd81f4a4787fbca99	grep	2.14	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-c67ff3dedf9d4e2994768e8fccd955481d20876b71a51e5dd81f4a4787fbca99	sed	4.2.3.dev0	Conda	True	
	SICER		SICER	1.1	Tool_Shed_Package	True	
	Fit HMM		R	2.15.0	Tool_Shed_Package	True	
RHmm	1.5.0	Tool_Shed_Package	True	
	Transpose, Reverse, Datamash		datamash	1.0.6	Tool_Shed_Package	True	
	SnpEff Download, SnpEff available databases, SnpEff	/galaxy/main/deps/_conda/envs/__snpeff@4.3k	snpeff	4.3k	Conda	True	
	cummeRbund		R	3.1.2	Tool_Shed_Package	True	
cummeRbund	2.8.2	Tool_Shed_Package	True	
	MACS2 predictd, MACS2 callpeak		macs2	2.1.0	Tool_Shed_Package	True	
numpy	1.7.1	Tool_Shed_Package	True	
scipy	0.12.0	Tool_Shed_Package	True	
R_3_0_1	3.0.1	Tool_Shed_Package	True	
gnu_awk	4.1.0	Tool_Shed_Package	True	
	Find diagnostic hits, Draw phylogeny, Summarize taxonomy, Find lowest diagnostic rank, Fetch taxonomic representation, Poisson two-sample test		taxonomy	1.0.0	Tool_Shed_Package	True	
	Cuffdiff, Cuffdiff, Cufflinks, Cufflinks, Cuffmerge, Cuffmerge, Cuffcompare, Cuffcompare		cufflinks	2.1.1	Tool_Shed_Package	True	
	Convert Kraken		gnu_awk	4.1.0	Tool_Shed_Package	True	
gb_taxonomy	8d245994d7	Tool_Shed_Package	True	
	HVIS		R	2.11.0	Tool_Shed_Package	True	
bioc_hilbertvis	1.18.0	Tool_Shed_Package	True	
	Merge BAM Files, FASTQ to BAM, Mark Duplicate reads, Add or Replace Groups, Reorder SAM/BAM, SAM to FASTQ, Merge BAM Files, BAM Index Statistics, SAM/BAM Hybrid Selection Metrics, Replace SAM/BAM Header, Estimate Library Complexity, SAM/BAM Alignment Summary Metrics, Insertion size metrics, Paired Read Mate Fixer, SAM/BAM GC Bias Metrics		picard	1.56.0	Tool_Shed_Package	True	
	flagstat, rmdup, SAM-to-BAM, SAM-to-BAM, Pileup-to-Interval, Slice BAM, BAM-to-SAM, MPileup, Filter SAM or BAM, output SAM or BAM		samtools	0.1.18	Tool_Shed_Package	True	
	Create assemblies with Unicycler, Create assemblies with Unicycler	/galaxy/main/deps/_conda/envs/__unicycler@0.4.1	unicycler	0.4.1	Conda	True	
	FASTQ de-interlacer	/galaxy/main/deps/_conda/envs/__galaxy_sequence_utils@1.1.2	galaxy_sequence_utils	1.1.2	Conda	True	
	MACS2 refinepeak, MACS2 randsample, MACS2 bdgcmp, MACS2 filterdup, MACS2 bdgdiff		macs2	2.1.0.20151222	Tool_Shed_Package	True	
numpy	1.7.1	Tool_Shed_Package	True	
scipy	0.12.0	Tool_Shed_Package	True	
	TopHat for Illumina		samtools	0.1.18	Tool_Shed_Package	True	
bowtie	0.12.7	Tool_Shed_Package	True	
tophat	1.4.0	Tool_Shed_Package	True	
	MACS2 bdgbroadcall, MACS2 bdgdiff	/galaxy/main/deps/_conda/envs/mulled-v1-d19c1a9ef33234193fd6ba084e874da12b2650df80e5a52958948dc2eecfbada	macs2	2.1.1.20160309	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-d19c1a9ef33234193fd6ba084e874da12b2650df80e5a52958948dc2eecfbada	gawk	4.1.3	Conda	True	
	Filter	/galaxy/main/deps/_conda/envs/__bamtools@2.4.0	bamtools	2.4.0	Conda	True	
	RAxML		raxml	7.7.6	Tool_Shed_Package	True	
	FreeBayes	/galaxy/main/deps/_conda/envs/mulled-v1-19f61dde9d8a7596b631632a802f6f24b752410a1f7974425fd008b237a638e0	freebayes	1.1.0.46	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-19f61dde9d8a7596b631632a802f6f24b752410a1f7974425fd008b237a638e0	samtools	0.1.19	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-19f61dde9d8a7596b631632a802f6f24b752410a1f7974425fd008b237a638e0	gawk	4.1.3	Conda	True	
/galaxy/main/deps/_conda/envs/mulled-v1-19f61dde9d8a7596b631632a802f6f24b752410a1f7974425fd008b237a638e0	parallel	20170422	Conda	True	
	FIMO		meme	None	None	True	
	Replace Text, Text transformation	/galaxy/main/deps/_conda/envs/__sed@4.2.3.dev0	sed	4.2.3.dev0	Conda	True	
	Trim Galore!	/galaxy/main/deps/_conda/envs/__trim-galore@0.4.3	trim-galore	0.4.3	Conda	True	
	Text reformatting, Replace Text	/galaxy/main/deps/_conda/envs/__gawk@4.1.3	gawk	4.1.3	Conda	True	"""


targets = []
stuff = []

for line in reqs.splitlines():
    if line.startswith('\t'):
        if targets:
            if len(targets) > 1:
                path = None
                for thing in stuff:
                    if thing[0].startswith('mulled-v1-'):
                        if not path:
                            path = thing[0]
                        assert thing[0] == path, '%s %s' % (thing[0], path)
                    else:
                        #print thing
                        pass
                h = 'mulled-v1-%s' % hash_conda_packages(targets)
                if path:
                    assert h == path, '%s %s' % (h, path)
                else:
                    #print '-> %s' % h
                    for i, thing in enumerate(stuff):
                        print 'conda list --name {name} --export > {name}.txt'.format(name=thing[0])
                        if i == 0:
                            op = 'create'
                        else:
                            op = 'install'
                        print 'conda {op} -y --override-channels --channel file:///home/g2main/conda --unknown --offline --name {hash} --file {name}.txt'.format(op=op, name=thing[0], hash=h)
                    print ''
            targets = []
            stuff = []
        path, pkg, ver, src = line.split('\t')[2:6]
    else:
        path, pkg, ver, src = line.split('\t')[0:4]
    if src == 'Conda':
        #print path, pkg, ver
        stuff.append((os.path.basename(path), pkg, ver))
        targets.append(CondaTarget(pkg, ver))
