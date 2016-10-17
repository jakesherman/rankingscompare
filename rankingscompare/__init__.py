# Namespace mgmt:
from rbo import average_overlap, percent_overlap
from spearman import (
    normalized_spearman_footrule,
    spearman_footrule,
    spearman_rho
)
from tau import ap_correlation, tau_a, tau_b
from utilities import to_rank

# Dependencies mgmt:
import sys
dependencies = ['numpy']
for dependency in dependencies:
    try:
        __import__(dependency)
    except ImportError:
        sys.stderr.write('rankingscompare requires: {0}'.format(dependency))
