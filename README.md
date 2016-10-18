# ordinary

Measures of association/correlation/similarity for ordinal/rank variables. Basically, in determining the association (correlation) or similarity bewteen two random variables, the variables will be treated as ordinal, so only their rank-order will be examined. The following measures are *non-parametric*. 

```python
import ordinary as or
```

### Properties of measures

* What is being measured? Association/correlation or (dis)similarity? 
* Does the measure natively handle ties? Some measure implicitly consider ties, others do not.
* Are the input variables conjoint/ paired? Classical statistics most often considers conjoint variables, which are often represented in a table, or two equal-length vectors. For conjoint data, each 'item' has a value for both variables. In non-conjoint data, variable 1 may have items that variable 2 does not have, and vice versa. Evaluating search engine results is a problem where the data often is non-conjoint, as some websites returned by one search engine may not be returned by another.
* Is the measure top-weighted? Top-weighted measures give more weight to discrepencies in the higher (1, 2, 3, ...) ranks than the lower ranks (100, 99, 98, ...). 

### Currently implemented

| Name                    | Function               | Measures      | Ties         | Conjoint | Top-weighted|
| ----------------------- |:---------------------- |:-------------:|:------------:|:--------:|:--------|
| Spearman's ρ (rho)      | `or.spearman_rho`      | Correlation   | X            | X        |         |
| Spearman's footrule     | `or.spearman_footrule` | Dissimilarity |              | X        |         |
| Kendall's τ-a         | `or.tau_a`             | Correlation   |              | X        |         |
| Kendall's τ-b         | `or.tau_b`             | Correlation   | X            | X        |         |
| Kendall's τ-c         | `or.tau_c`             | Correlation   |              | X        |         |
| Goodman/Kruskal's gamma | `or.gamma`             | Correlation   |              | X        |         |
| Somers' D               | `or.somers_d`          | Correlation   |              | X        |         |
| AP correlation          | `or.ap_correlation`    | Correlation   |              | X        | X       |
| Average overlap         | `or.average_overlap`   | Similarity    |              |          | X       |

### Which measure should I use?

*Spearman's ρ* and *Kendalls' τ* are the most probably the most popular rank correlation measures (both are methods in R's `stats::cor` function). Spearman's ρ is a non-parametric alternative to Pearson's ρ that does a much better job at handling outliers. It is simply Pearson's ρ on the ranks themselves. Like Pearson's ρ, Spearman's ρ measure the strength of the association between two variables, but instead of measuring the strength of the linear relationship, it measures the strength of the monotonic relationship (does X increase when Y increases, and vice versa). 

Kendalls' τ measures the probability of concordance minus the probability of discordance (if X and Y are random variables, concordance is when Xi > Xj and Yi > Yj or Xi < Xj and Yi < Xj), and **is often preferred over Spearmans' ρ**. Kendall & Gibbons (1990) argue that "...confidence intervals for Spearman’s rS are less reliable and less interpretable than confidence intervals for Kendall’s τ-parameters...". Kendalls' τ also has a nice probabilstic interpretation. τ-b should generally be used, unless you know that your inputs do not contain ties, as τ-b accounts for ties, and gives the same value as τ-a if there are no ties.

If discrepencies for higher ranks are more important than those for lower ranks, use a measure that is top-weighted. AP correlation, proposed by Yilmaz et al. [2008], is a top-weighted variant of τ-a. It's major drawback, however, is that it does not natively handle ties.

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
