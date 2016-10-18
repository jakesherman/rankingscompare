# rankingscompare

Rank correlation and similarity measures. The following are implemented:

* Spearman's rho (ρ)
* Spearman's Footrule (regular and normalized)
* Kendalls' tau (τ), including tau-a and tau-b
* AP correlation (top-weighted alteration of τ)
* Average overlap

To be implemented:

* tau-c
* Smucker's variant of AP correlation that accounts for ties
* Vigna [2014]'s tau-h, a modified tau-b/AP correlation statistic that 
accounts for ties
* Rank-biased overlap (RBO), proposed by Webber et al. [2010]
* Better handling of data structures containing ordinal data

## Install

```bash
pip install git+https://github.com/jakesherman/rankingscompare.git
```

### To run unit tests

```
git clone https://github.com/jakesherman/rankingscompare.git
cd rankingscompare
python -m unittest tests.tests
```
