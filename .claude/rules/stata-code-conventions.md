# Stata Code Conventions for RMEB

**Stata is the primary econometrics language for RMEB. Follow these conventions for all Stata code in slides, labs, and notes.**

---

## Do-File Structure

Every Stata do-file should follow this template:

```stata
/*============================================================
  Title: [Description]
  Course: 经济与商务实证研究方法 (RMEB) 2026 Spring
  Author: [Name]
  Date: [YYYY-MM-DD]
  Purpose: [One-line description]
============================================================*/

clear all
set more off
capture log close

* Set working directory (use relative paths where possible)
* cd "/path/to/project"

* Open log
log using "output/filename_$(current_date).log", replace text

* ============================================================
* 1. Data loading
* ============================================================

* ============================================================
* 2. Data cleaning
* ============================================================

* ============================================================
* 3. Analysis
* ============================================================

* ============================================================
* 4. Output tables and figures
* ============================================================

log close
```

## Key Packages (always check/install)

```stata
* Causal inference
ssc install reghdfe        // High-dimensional FE regression
ssc install csdid          // Callaway-Sant'Anna DID
ssc install eventstudyinteract  // Sun-Abraham DID
ssc install synth          // Synthetic control
ssc install rdrobust       // RD estimation

* Tables and export
ssc install estout         // Formatted regression tables
ssc install outreg2        // Alternative table export
ssc install coefplot       // Coefficient plots

* Structural / Trade
ssc install ppmlhdfe       // PPML with HDFE (gravity)
```

## Standard Errors Convention

```stata
* Panel clustering (default for DID)
reghdfe y d x, absorb(id year) vce(cluster id)

* Two-way clustering (when needed)
reghdfe y d x, absorb(id year) vce(cluster id year)

* Robust only (cross-section)
reg y d x, robust
```

## Output Tables Convention

```stata
* After regressions, use esttab for formatted output
esttab m1 m2 m3 using "tables/table1.tex", ///
    replace booktabs ///
    b(3) se(3) ///
    star(* 0.10 ** 0.05 *** 0.01) ///
    label ///
    title("Main Results") ///
    keep(d) ///
    order(d) ///
    stats(N r2, labels("Observations" "R-squared")) ///
    nonotes addnote("Robust standard errors clustered at X level.")
```

## Figure Conventions

```stata
* Use scheme lean2 or s1color for clean figures
set scheme s1color

* Standard event study plot
coefplot m1, ///
    vertical ///
    yline(0, lcolor(gray) lpattern(dash)) ///
    xline(4.5, lcolor(red) lpattern(dash)) ///
    xtitle("Period relative to treatment") ///
    ytitle("Estimated coefficient") ///
    title("Event Study") ///
    graphregion(color(white)) ///
    bgcolor(white)
graph export "figures/event_study.png", replace width(2000)
```

## Anti-Patterns to Avoid

| Bad | Good |
|-----|------|
| `xtreg y d, fe` | `reghdfe y d, absorb(id year)` |
| `reg y d` without clustering in panel | `reghdfe y d, absorb(id year) vce(cluster id)` |
| String manipulation with `subinstr` | Use `split` or regular expressions |
| `gen new = old[_n-1]` without sort | Always sort first: `sort id year` |
| Hardcoded absolute paths | Use relative paths or globals |
| No seed in simulations | `set seed 12345` at top |
