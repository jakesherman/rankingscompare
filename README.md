# rankingscompare

Rank correlation and similarity measures. The following are implemented:

* Spearman's rho (ρ)
* Spearman's Footrule (regular and normalized)
* Kendalls' tau (τ), including tau-a and tau-b
* AP correlation (top-weighted alteration of τ)
* Average overlap

To be implemented:

* AP correlation variant that handles ties
* Rank-biased overlap (RBO), proposed by Webber et al. [2010]

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
