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

## Manual checks ---------------------------------------------------------------

# The swap near the top results in a lower AP correlation than Kendall tau-a
a <- c(100, 70, 50, 40, 35, 30)
b <- c(45, 55, 40, 10, 20, 3)
cor(a, b, method = 'kendall')  # 0.733
apcorr(a, b)   

## Documentation ---------------------------------------------------------------

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

## Tie-handling ----------------------------------------------------------------

# Carry over the top ranking of a tie
truth <- c(1, 2, 3, 4)
estimate <- c(1, 1, 1, 1)
results <- c()
means <- c()

for (i in 1:1000) {
    permutation <- sample(n)
    truth <- truth[permutation]
    estimate <- estimate[permutation]	 
    result <- apcorr.nosampling(truth, estimate)
    results <- c(results, result)
    means <- c(means, result / i)
}

plot(results)
plot(means)

# Midrank method - average of the ranks
truth <- c(1, 2, 3, 4)
estimate <- c(2.5, 2.5, 2.5, 2.5)
apcorr.nosampling(truth, estimate)

## apcorr.nosampling -----------------------------------------------------------

function( truth, estimate )
{
    # we're going to say that the scores at rank i are for an
    # item with an ID of i.  Thus "ID" means the index into
    # the truth and estimate vectors.
    n <- length(truth) 
    if ( length(estimate) != n )
        stop( "must be same length" )
    truth.order <- order( truth, decreasing=TRUE ) 
    estimate.order <- order( estimate, decreasing=TRUE ) 
    innerSum <- 0
    for ( i in 2:n )
    {
        currDocID <- estimate.order[i] 
        estimate.rankedHigherIDs <- estimate.order[1:(i-1)] 
        # where is the current doc in the truth order?
        currDoc.truth.order.index <- which( truth.order == currDocID )
        truth.rankedHigherIDs <- vector()
        if ( currDoc.truth.order.index != 1 ) # top ranked doc, beware
        {
            truth.rankedHigherIDs <- truth.order[1:(currDoc.truth.order.index-1)]
        }
        C_i <- length( intersect(estimate.rankedHigherIDs, truth.rankedHigherIDs) )
        innerSum <- innerSum + (C_i / (i-1))
    }
    result = 2 / (n-1) * innerSum - 1   
    return( result )
}
