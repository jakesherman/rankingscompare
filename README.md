# rankingscompare

Rank correlation and similarity measures. The following are implemented:

* Spearman's rho (ρ)
* Kendalls' tau (τ)
* AP correlation (top-weighted alteration of τ)

To be implemented:

* Rank-biased overlap (RBO)

## Install

```bash
pip install git+https://github.com/jakesherman/rankingscompare.git
```

## To run unit tests

```
git clone https://github.com/jakesherman/rankingscompare.git
cd rankingscompare
python -m unittest tests.tau_tests
```
