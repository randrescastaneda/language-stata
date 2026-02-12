// Test file: Verify syntax highlighting for newly added commands
// Open this file in VS Code/Atom with language-stata to check highlighting

// === Tables & Collections (Stata 17-18) ===
collect clear
dtable age gender income, by(treatment)
etable, column(dvlabel)

// === Frames (Stata 16+) ===
frame create myframe
frame change myframe
frames dir
frlink m:1 id, frame(other)
frget var1 var2, from(other)

// === Causal Inference & Treatment Effects ===
teffects ra (y x1 x2) (treatment)
teffects ipw (y) (treatment x1 x2)
didregress (y) (treatment post), group(id) time(year)
hdidregress aipw (y x1 x2) (treatment), group(id) time(year)
xtdidregress (y) (treatment post), group(id) time(year)
xthdidregress aipw (y x1 x2) (treatment), group(id) time(year)
stteffects ra (x1 x2) (treatment), failure(failvar)
telasso y x1 x2 x3, treatment(treat)
mediate (y) (mediator) (treatment)
etregress y x1 x2, treat(treatment)
etpoisson y x1 x2, treat(treatment)
lateffects y x1 x2

// === Lasso & Machine Learning ===
lasso linear y x1-x100
elasticnet linear y x1-x100, alpha(0.5)
sqrtlasso y x1-x100
dsregress y x1 x2, controls(x3-x100)
dslogit y x1 x2, controls(x3-x100)
dspoisson y x1 x2, controls(x3-x100)
poregress y x1-x100
pologit y x1-x100
popoisson y x1-x100
poivregress y (x1 = z1), controls(x2-x100)
xporegress y x1-x100
h2oml gbregress y x1-x100

// === Bayesian Analysis ===
bayes: regress y x1 x2
bayesmh y x1 x2, likelihood(normal({var}))
bmaregress y x1 x2 x3

// === Panel/Longitudinal Data ===
mixed y x1 || group:
melogit y x1 || group:
meprobit y x1 || group:
mepoisson y x1 || group:
menbreg y x1 || group:
mecloglog y x1 || group:
meglm y x1 || group:, family(binomial)
mestreg x1 || group:, distribution(weibull)
metobit y x1 || group:, ll(0)
meintreg y_lower y_upper x1 || group:
meologit y x1 || group:
meoprobit y x1 || group:
menl (y = {b0} + {b1}*x1) || group:
xtheckman y x1, select(x2 x3)
xtdpd y L.y x1, dgmmiv(L.y)
xtdpdsys y L.y x1
xteregress y x1, endogenous(x2)
xtvar y1 y2, lags(1/2)

// === New Estimation Commands ===
arfima y, ar(1) ma(1)
betareg y x1 x2
churdle linear y x1 x2, select(x3) ll(0)
dfactor (y1 = f1, noconstant) (y2 = f1, noconstant)
fmm 2: regress y x1 x2
fracreg logit y x1 x2
gmm (y - {b0} - {b1}*x1), instruments(z1)
gsem (y <- x1 x2)
hetregress y x1 x2, het(x3)
hetprobit y x1, het(x2)
hetoprobit y x1, het(x2)
heckoprobit y x1, select(x2 x3)
heckpoisson y x1, select(x2 x3)
irt 2pl y1 y2 y3
ivregress 2sls y (x1 = z1)
ivpoisson gmm y (x1 = z1)
ivqregress y (x1 = z1), quantile(0.5)
mswitch dr y x1, states(2)
npregress kernel y x1
sem (y <- x1 x2)
sspace (y = f, noconstant) (f = L.f)
ucm y, model(llevel ltrend)
margins, dydx(x1)
marginsplot
power twomeans 10, diff(5) sd(8)

// === Survival Analysis ===
stcrreg x1 x2, compete(failtype == 2)
stintcox x1 x2
stintreg x1 x2

// === Spatial Models ===
spregress y x1 x2, gs2sls
spivregress y (x1 = z1) x2, gs2sls
spxtregress y x1 x2, fe gs2sls

// === Data Management ===
icd10 generate newvar = diagvar, range(A00/B99)
icd10cm generate newvar = diagvar, range(A00/B99)
icd10pcs generate newvar = procvar
putexcel A1 = "Results"
putmata X = (x1 x2 x3)
bcal describe business
zipfile myfiles, saving(archive.zip)
unicode analyze filename
vl create mylist = (x1 x2 x3)
snapshot save

// === Other New Commands ===
collect get r(mean), name(mytable)
discrim lda group, group(y) priors(equal)
candisc group y1 y2
ciwidth onemean, width(5) sd(10)
concordance y x1
contrast group#time
mlexp (y * {b1} * x1 - exp({b1} * x1))
nlsur (y1 = {b0} + {b1}*x1) (y2 = {c0} + {c1}*x1)
mvtest means y1 y2, by(group)
wildbootstrap regress y x1 x2
