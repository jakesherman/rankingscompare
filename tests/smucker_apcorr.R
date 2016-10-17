################################################################################
#
# Mark Smucker did the only implementation that I could find of the AP
# correlation statistic. In Mark D. Smucker, Gabriella Kazai, and Matthew Lease, 
# "Overview of the TREC 2013 Crowdsourcing Track," TREC 2013, the authors 
# mention that AP correlation as it is proposed by Yilmaz et al does not account
# for ties, so Smucker et al. modify the AP correlation statistic to account
# for ties! Cool stuff. Let's check out what they've done.
#
################################################################################

source("http://www.mansci.uwaterloo.ca/~msmucker/software/apcorr.r")

# Two sample vectors to be compared, one consists of only ties
apcorr.nosampling(c(1, 2, 3, 4), c(1, 1, 1, 1))  # -1
apcorr.nosampling(c(4, 3, 2, 1), c(1, 1, 1, 1))  #  1

# These scores don't make any sense! The estimate (1's) shouldn't be correlated
# with the truths, the correlation should be close to 0.
apcorr(c(1, 2, 3, 4), c(1, 1, 1, 1))  #  0.0162222
apcorr(c(4, 3, 2, 1), c(1, 1, 1, 1))  # -0.0052222

# By default 1,000 samples are used, make estimates more precise by using a 
# higher number of samples.
apcorr(c(1, 2, 3, 4), c(1, 1, 1, 1), 10000)  # -0.0013
apcorr(c(4, 3, 2, 1), c(1, 1, 1, 1), 10000)  # -0.0053
