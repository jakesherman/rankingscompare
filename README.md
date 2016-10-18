# ordinary

Measures of association/correlation/similarity for ordinal/rank variables. Currently implemented are the following measures:

| Measure                 | Correlation   | Similarity  | Ties         | Conjoint | Comments|
| ----------------------- |:-------------:| :----------:|:------------:|:--------:|:--------|
| Spearman's ρ (rho)      | X             |             |              | X        | Pearson's rho on the ranks themselves, the quntiessential rank correlation measure |
| Spearman's footrule     |               | X           |              | X        | Sum of the absolute value differences in ranks        |
| Kendall's tau-a         | X             |             |              | X        | Probability of concordance minus probability of discordance        |
| Kendall's tau-b         | X             |             | X            | X        |         |
| Kendall's tau-c         | X             |             |              | X        |         |
| Goodman/Kruskal's gamma | X             |             |              | X        |         |
| Somers' D               | X             |             |              | X        |         |
| Average overlap         |               | X           |              |          | Set-based measure        |


* Spearman's rho (ρ)
* Spearman's footrule (regular and normalized)
* Kendalls' tau (τ), the tau-b and tau-c variants
* AP correlation (top-weighted alteration of τ)
* Goodman - Kruskal Gamma
* Somers' D
* Percent overlap, average overlap

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
