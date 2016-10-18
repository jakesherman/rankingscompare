# ordinary

Measures of association/correlation/similarity for ordinal/rank variables. In determining the association (correlation) or similarity bewteen two random variables, the variables will be treated as ordinal, so only their rank-order will be examined. The following measures are *non-parametric*. 

```python
import ordinary as or
```

### Properties of measures

* What is being measured? Association/correlation, or (dis)similarity? Correlation belongs to the domain [-1, 1], whereas (dis)simlarity belongs to the domain [0, 1].
* Does the measure natively handle ties? Some measure implicitly consider ties, others do not.
* Are the input variables conjoint, or paired? Classical statistics most often considers conjoint variables, which are often represented in a table. For conjoint data, each item has a value for both variables. In non-conjoint data, variable 1 may have items that variable 2 does not have, and vice versa. Comparing search engine results is a problem where the data often is non-conjoint, as some websites returned by one search engine may not be returned by another.
* Is the measure top-weighted? Top-weighted measures give more weight to discrepencies in the higher (1, 2, 3, ...) rank than the lower ranks (100, 99, 98, ...). 

### Currently implemented

| Measure                 | Function              | Correlation   | Similarity  | Ties         | Conjoint | Top-weighted|
| ----------------------- |:----------------------|:-------------:| :----------:|:------------:|:--------:|:--------|
| Spearman's ρ (rho)      | `or.spearman_rho`     | X             |             |              | X        |         |
| Spearman's footrule     | `or.spearman_footrule` |               | X           |              | X        |         |
| Kendall's tau-a         | `or.tau_a` | X             |             |              | X        |         |
| Kendall's tau-b         | `or.tau_b` | X             |             | X            | X        |         |
| Kendall's tau-c         | `or.tau_c` | X             |             |              | X        |         |
| Goodman/Kruskal's gamma | `or.gamma` | X             |             |              | X        |         |
| Somers' D               | `or.somers_d` | X             |             |              | X        |         |
| AP correlation          | `or.ap_correlation` | X             |             |              | X        | X       |
| Average overlap         | `or.average_overlap` |               | X           |              |          | X       |

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
