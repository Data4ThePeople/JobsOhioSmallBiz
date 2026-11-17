---
title: Every JobsOhio grant, in one searchable tool
subtitle: Which grants went to small Ohio businesses, which went to large companies based elsewhere, and which companies failed after taking the money. Free for Ohioans and reporters to search.
slug: jobsohio-grants
date: 2026-11-17T07:30:00-05:00
section: Visualization
hero: images/jobsohio-grants-hero-1680x1080.png
hero_alt: Summary cards from the JobsOhio grants tool, covering 2,415 grants and $1.35 billion to 1,700 companies and organizations, fiscal years 2014 to 2025. Two headline figures: 19% of the dollars went to businesses under 500 employees at the parent company, and 7.8% went to businesses under 100. A grid crossing size with home state, where small means under 500 employees, shows the share of dollars: small Ohio 16%, small elsewhere 2.9%, large Ohio 20%, large elsewhere 61%.
meta_title: JobsOhio Grants Database: Every Award, 2014 to 2025
description: Search every grant JobsOhio paid on its IRS Form 990: 2,415 awards, $1.35 billion, 1,700 companies, by business size, home state and what happened next.
keywords: JobsOhio, JobsOhio grants, Ohio economic development, JobsOhio grant recipients, Ohio business incentives, JobsOhio accountability, Form 990 Schedule I, Ohio economic development transparency
schema_type: dataset
drop_cap: true
heading_spacer: 20px
caption_spacer: 20px
dividers: false
dataset_name: JobsOhio grants, IRS Form 990 Schedule I, FY2014 to FY2025
temporal: 2013-07-01/2025-06-30
spatial: Ohio, United States
measured: Grant dollars paid|USD; Recipient parent employee band; Recipient parent headquarters state; Verified post-grant outcome
sources: https://projects.propublica.org/nonprofits/organizations/452798687 | https://www.jobsohio.com/newsroom/reports-publications | https://jfs.ohio.gov/job-services-and-unemployment/job-services/warn | https://www.sec.gov/edgar
distribution: text/csv|https://raw.githubusercontent.com/Data4ThePeople/JobsOhioSmallBiz/main/data/grants_raw.csv; text/csv|https://raw.githubusercontent.com/Data4ThePeople/JobsOhioSmallBiz/main/data/parents.csv; text/csv|https://raw.githubusercontent.com/Data4ThePeople/JobsOhioSmallBiz/main/data/failures.csv; text/csv|https://raw.githubusercontent.com/Data4ThePeople/JobsOhioSmallBiz/main/data/jobsohio_lawsuits.csv; text/csv|https://raw.githubusercontent.com/Data4ThePeople/JobsOhioSmallBiz/main/data/grant_conditions.csv
credit: Data 4 The People
measurement_technique: Each Schedule I payee traced to its ultimate parent at the time of the grant using SEC filings, Department of Labor Form 5500 data and official releases, then checked for post-grant outcomes against court dockets and Ohio WARN notices.
same_as: https://github.com/Data4ThePeople/JobsOhioSmallBiz
---

# Every JobsOhio grant, in one searchable tool

::: blurb-full If you are a journalist, read this first
**This is a tool built to aid your research. It is not a tool to pull data from and publish without checking it yourself.**

We have validated it as far as we can. The method behind every number is public, down to the judgement calls, and as many findings as possible link to the document they rest on. But there are twelve years and thousands of records in here, and the detail runs deep.

**Before you publish anything from a row in this tool, fact check that grant yourself.** Open the document it links to. Call the company. Ask JobsOhio. Use this to find the story and to know where to look, not as the only source for a number you put in print.

If you find something wrong, email **[connect@data4thepeople.com](mailto:connect@data4thepeople.com)** and we will fix it.
:::

::: spacer 20px

## Purpose

::: spacer 5px

::: dropcap
This visualization on JobsOhio grants has been months in the making. It started as a follow-up to our work [benchmarking JobsOhio performance against other states](https://www.data4thepeople.com/p/jobsohio-post). We started to think more about the underlying strategies for state-level economic development. Specifically, if Ohio has a fixed amount of cash to invest in economic development and job creation, what strategy will provide the greatest return on investment for Ohioans?

To be clear, this visualization doesn't answer that complex guiding question. Rather, its goal initially was to just collect the data on all the grants given out by JobsOhio and classify them into a 2x2 matrix. Was the grant provided to a small or a large business? Was the grant provided to an Ohio-based company, or a company headquartered outside of Ohio? With this data we could at least reverse engineer JobsOhio's strategy. Has it chosen to invest in small local employers within communities, or to attract large corporations to relocate to Ohio?

This was not an easy project, because there is no clean database we could join that had business size or headquarters location. And so, we studied each grant line by line to come up with our best judgement on where the recipient company belonged in our 2x2 matrix.

That said, we still believe this is the best free public tool to allow for research on grant performance in JobsOhio available in the public domain. Our goal is not to provide extensive takeaways on the stories living in this tool, but rather to provide this to local journalists and all Ohioans to better be able to ask questions of JobsOhio to gain confidence that our liquor sales dollars (which before JobsOhio was created used to flow through the state's own audited books) are being invested to help improve the lives of Ohioans.

## The tool

::: spacer 5px

Here is the short version. It carries the same figures as the full tool, in a smaller frame.

<iframe src="https://data4thepeople.github.io/JobsOhioSmallBiz/dist/embed.html?v=1.0" height="780" width="100%" style="border:0" title="Where JobsOhio's grant money went"></iframe>

::: spacer 40px

::: blurb Use the full version, and tell us what you find
Every figure in the frame above is in the full tool, but the full tool also lets you filter to any outcome, read the source behind each finding, and see every one of the 76 candidates we checked and threw out, with the reason. **If you are going to work from this, use the full version.** Several rows carry caveats that decide whether a number means what it looks like, and those caveats sit on the row rather than in the summary.

**[Open the full tool and the method notes](https://data4thepeople.github.io/JobsOhioSmallBiz/)**

Found a broken link, a company in the wrong place, a number that looks wrong, or something we missed? Email **[connect@data4thepeople.com](mailto:connect@data4thepeople.com)** and we will fix it. We would rather hear it from you than leave it wrong. Corrections are made in public, with a note saying what changed and when.
:::

## The part we did not plan on

::: spacer 5px

What we didn't realize was that as we were going through each public grant line by line, we could start to collect additional information, that is arguably even more valuable for those looking to understand how JobsOhio has performed. We were able to find grants given to companies that, after receiving the grant, announced a mass layoff at the funded site, entered bankruptcy or receivership, closed the funded site, or ended the service the grant paid for. We also track separately which companies JobsOhio sued to get its money back. We call each of these a "failed" grant as it did not perform as expected. Note that we cannot determine if any of the grants were successful as JobsOhio doesn't regularly announce when companies have met their hiring targets. But the data to determine if there was a failure is in the public domain through WARN notices, bankruptcy filings, and court dockets. Wherever we can find one of these documents, it is linked so you can click through as part of your research process.

## How to use it

::: spacer 5px

Two controls sit at the top and change every number on the page.

**Count** switches between operating businesses only and all recipients. JobsOhio also pays universities, hospitals, local governments, nonprofits and site developers. Those are real grants, but they are not companies, and leaving them in the denominator makes the business picture look different than it is.

**"Small" means under** sets the employee line at 100, 500 or 5,000 workers at the parent company. There is no single legal definition of a small business. The Small Business Administration sets a separate threshold for each of 978 industries. About 500 of those industries are measured by annual revenue rather than headcount at all, and among the ones that do count employees the line runs from 100 to 1,500. We default to 500 because it is the familiar shorthand and because it is the conservative choice: for manufacturing, which is most of what JobsOhio funds, the median SBA threshold is 1,000 employees, so our default counts fewer companies as small than the SBA would.

Below the controls, the table is the part most people will want. You can search a company, a city or a parent, switch between one row per company and one row per payment, and sort any column. Clicking an outcome anywhere on the page filters the table to those companies and explains in a sentence what you are now looking at.

**Use both table views, not one.** This is the single most useful habit if you are chasing a specific grant, and it is easy to miss.

**By company** is the overview. It rolls every payment up to the parent group that owned the recipient at the time. That is the right unit for asking who got the money, and it is what the charts above count.

**Every payment** breaks that back apart. It shows each line on the Form 990 on its own, with the fiscal year, the payee name exactly as JobsOhio filed it, and the city the check went to.

The second view is where the detail lives, and the detail often changes what a number means. Take McKesson Corporation. By company it is one row, $7,413,235. Search the same name in Every payment and it comes apart into seven payments to two different companies, spanning 2017 to 2023 and four addresses: five to CoverMyMeds, $6,613,235, sent to Columbus and to Twinsburg, and two to McKesson itself, $800,000, one of those to a Jeffersonville address in a different county that JobsOhio's own project reports tie to a different project altogether. Anyone working from the $7,413,235 alone would get all of that wrong.

So: find it by company, then open it by payment before you write anything. If only part of a group's money belongs to an outcome on that row, the company view flags it with a "part" label. Hover that label for both figures and for which company actually failed.

## What the words mean

::: spacer 5px

### Parent company

JobsOhio reports a payee name. The payee is often a subsidiary, a plant-level entity or a holding company. We traced each payee to the company that owned it at the time of the grant, and we size that owner by its worldwide employees. A 60-person plant owned by a 90,000-person multinational counts as large here, because the question is who got the money, not how many people work at one address.

### Evidence grade (A, B, C, D)

Every ownership and size call carries a letter saying how firmly it is established.

- **A** is a filing made under penalty of perjury: an SEC 10-K or Exhibit 21, or an IRS return.
- **B** is an official or semi-official record: a JobsOhio or regional partner release naming the company, or a Department of Labor Form 5500 participant count.
- **C** is the company's own website, a trade directory or a news report. Usually right, but self-reported and not audited.
- **D** is the weakest, and it does not mean we gave up. We still named an owner, almost always from web research: a state business registry, a single local story, a JobsOhio program page, or the company's own site. What we could not do is tie it to a filing or an official record, and for some of these the headcount or the home state is an inference rather than something a source states outright. Most are small private companies and single-purpose development LLCs that file nothing public. Read a D as our best reading of what is available, not as a documented fact.

The worst-case line under the 2x2 matrix shows what happens if every unresolved or low-confidence company were counted the other way, so you can see how much the headline depends on our judgement calls. Both C and D are swept into that worst case.

### Failed

A company we verified did one of four things after taking the money: filed a mass layoff notice for the funded site, entered bankruptcy or receivership, closed the funded site, or ended the subsidized service. Each one is tied to a document where a document exists. "Failed" here is about the grant, not a judgement on the company.

Being bought is not failing. A company that is acquired and keeps operating has not failed; a company that is acquired and shut down has. Four companies that were acquired or divested with the Ohio operation still running came out of the count on that rule, and you can see all four, with the reason, in the rejected candidates view.

We cannot tell you which grants succeeded. JobsOhio does not routinely publish whether a company hit its hiring targets, so there is no success column to put beside this one. Read the failure count as a floor on failure, not as the opposite of a success rate.

### Repayment clause, and what "the standard agreement" means

This is the column most likely to be misread, so it is worth slowing down on.

"Repayment clause" answers a narrow question: does a clause exist that would let JobsOhio demand the money back, and how firmly do we know it exists? It does not say JobsOhio used it, and it does not say any money came back.

Ten of JobsOhio's twelve programs publish no repayment language at all. So we went to the courthouse instead. We pulled 56 signed JobsOhio grant agreements out of Franklin County court files, spanning 2013 to 2023 and covering the Economic Development, Workforce, Revitalization, Research and Development, and Inclusion programs. Every agreement whose remedy clause we could read carries the same Section 9(b)(ii), "Demand Repayment of Grant Funds": "Grantor may demand repayment of all or a portion of Grant Funds disbursed."

That gives three different strengths of answer, and the label tells you which one you have.

**"In this agreement"** is the strong one. This company's own signed contract is in a court file and we read the clause in it. That is 38 companies and about $8 million.

**"In the standard agreement"** is an inference, not a reading. It means this company was paid under one of the programs whose agreements we obtained, and every one of those agreements we could read is identical, so we infer that this company's contract contains the same clause. **We did not see this company's contract.** This is the biggest group in the tool by a wide margin: 987 of the 1,700 companies and about $873 million, which is 65% of all the money. If a single JobsOhio program ever used a different form, or a particular company negotiated a change, this label would be wrong for that company and we would have no way to know. Treat it as a well-supported expectation to check, not as a fact to publish.

**"None found"** means neither. Nothing published and no signed agreement ever obtained. The air service grants to airlines sit here: the guidelines describe how the money goes out and say nothing about what happens if the route ends.

The remaining labels mark payments where the question works differently: **"loan"** (repayable because it is debt, which is not the same as a performance clawback), **"services, not cash"** (JobsOhio paid vendors rather than the company), **"in the guidelines"** (no agreement seen, but the published program terms contain a repayment trigger), and **"program unknown"** (the payment cannot be tied to a program in JobsOhio's own project reports, so there is nothing to read either way).

Put the first three together and 71% of all the dollars went to a recipient whose agreement would let JobsOhio demand the money back. **Read that number with the paragraph above in mind.** Most of it is the inferred group. We read the form for those programs; we did not read those companies' copies of it. The part we can show a signed contract for is about $8 million, which is less than 1% of the money.

One more thing about all of them. **A clause is not a recovery.** The same agreement gives JobsOhio the discretion to decide whether a company complied, whether to demand repayment, how much, and whether to waive it. Across twelve years, $26,040,088 has come back, which is 1.9% of what went out.

**So how do you use this?** If you are chasing one grant, here is what each answer is worth.

- If the row says **"in the standard agreement,"** read it as: to the best of our ability, we believe JobsOhio had the power to try to claw this money back. We did not see this company's contract. It is our best read, not something to publish as fact.
- If the row also shows a **lawsuit**, you can see documentation of JobsOhio actually trying. The case number links to the Franklin County docket, and in most of these the complaint attaches the signed agreement itself, which is the one place the real terms for that company appear.
- For every other grant where the company did not deliver, **we have no public evidence that JobsOhio tried to get Ohio's money back.** Be careful with that sentence. It does not mean JobsOhio did nothing. A demand letter is not filed anywhere public, so one could have gone out years ago and nothing we can reach would show it. Check the returned filter too, because money has come back from companies that were never sued.

None of these is a finding on its own. Each one is a place to start, and the grant needs to be researched on its own before anyone writes about it.

### Sued by JobsOhio

JobsOhio's own lawsuit against that company in the Franklin County Court of Common Pleas, where JobsOhio is headquartered, to get grant money back. Hover a row for the case number, what was sought and how the case ended. Suits filed in another county, in federal court or in another state would not appear here, so the count is a floor.

**Being sued is not a failure, and the two counts do not add together.** They answer different questions. The failure count asks what happened to the company after the money went out. The sued count asks whether JobsOhio went to court about it. JobsOhio has sued 51 companies on the grant schedule, and 3 of those are also in the failure count. The other 48 are companies it sued that did not fail by any test here, and 37 of the 40 failures were never sued at all.

::: divider

## Where this comes from

::: spacer 5px

Every dollar starts with one source: Schedule I of JobsOhio's IRS Form 990, fiscal years 2014 through 2025, taken from the IRS e-file data. Schedule I lists grants over $5,000 on a cash basis, so these are dollars actually paid in a year, not dollars committed. Grants of $5,000 or less are not on it.

That is 2,415 payments to 1,789 payees, traced to 1,700 parent companies and organizations, totaling $1,345,318,862 after $26,040,088 of recorded reversals.

That list is already public. Anyone can read the same returns on [ProPublica's Nonprofit Explorer](https://projects.propublica.org/nonprofits/organizations/452798687). What it gives you is a payee name and a dollar figure, one year at a time. What it does not give you is who owns that payee, how big they are, where they are based, or what happened to them after the check cleared. That is the work in this tool, and it is why we did it by hand.

Everything after that is layered on top: SEC filings and Form 5500 plan data for ownership and headcount, JobsOhio's own monthly project reports for the program and the project county, the Ohio WARN register for mass layoffs, federal bankruptcy dockets, and the Franklin County Clerk of Courts for the lawsuits and the grant agreements. Links go to the record, not to a summary of it. Every link was fetched and confirmed to resolve; where nothing resolved, the name is plain text rather than a dead link.

The full method, including every judgement call and every number that moved, is in the repository. So is the data, as plain CSV files you can open in a spreadsheet.

**[Read the full method notes and download the data](https://github.com/Data4ThePeople/JobsOhioSmallBiz)**

## What this tool cannot tell you

::: spacer 5px

We would rather you know the holes than find them later.

**It cannot tell you what worked.** There is no success column, because JobsOhio does not routinely publish whether a company met its hiring targets.

**It cannot see a project that was never built.** A company that takes the money and quietly never breaks ground files no layoff notice, because there were no jobs to eliminate. That leaves two ways for us to see it, a lawsuit from JobsOhio or a filing the state requires, and if neither happens the money is invisible to this tool. The clearest case is the petrochemical plant proposed for Belmont County.

What we know: JobsOhio paid $48,599,868 to three companies for that site and that project, $20,000,000 came back after the developer failed to make an investment decision, as [The Intelligencer reported in March 2022](https://www.theintelligencer.net/news/top-headlines/2022/03/ptt-global-pays-jobsohio-20m-for-failing-to-move-on-belmont-county-cracker-plant/), and the plant was never built. That leaves $28,599,868 out. None of the three companies appears in the failure count, because none of them did anything the method can detect.

What we do not know: what the site work bought, whether the rest will ever come back, and whether one of the three payments is a loan draw rather than a grant, which would change the total. We also cannot say how many more abandoned projects are in the data, because finding them means checking every commitment JobsOhio made against what was actually built, and nobody has done that.

**The address on the form is where the check went, not where the project was.** About 28.5% of the dollars were mailed to an address outside Ohio, usually a corporate headquarters. Where JobsOhio's project reports name a county, we use that instead.

**The failure count is a floor, not a total.** It counts what we could verify from a document. A failure that produced no filing, no notice and no coverage is invisible to the method.

**Most of the repayment labels rest on an inference rather than a document.** 65% of the money carries "in the standard agreement," which means we read the form and not that company's copy of it. See the section above. It is the single largest caveat in the tool.

**Court links take two clicks, and that is not our bug.** The Franklin County Clerk of Courts makes you accept a disclaimer before it shows you anything, and it throws away the case number when it does. So the first time you click a case in this tool, you will accept the disclaimer and land on the clerk's home page instead of the case. Come back, click the same case again, and it opens. We checked whether we could link around it and we cannot.

**Some ownership calls are judgement.** That is what the A through D grade is for, and the worst-case line under the matrix shows how much the headline would move if we were wrong about all of them.

## Common questions

::: spacer 5px

### Where does JobsOhio's money come from?

JobsOhio is funded by the profits from Ohio's liquor franchise, which the state leased to it in 2013.

### Is JobsOhio subject to public records law?

JobsOhio is a private nonprofit corporation, so it is not a public office under Ohio's public records act. Its IRS Form 990, which is what this tool is built from, is public because federal law requires a nonprofit to disclose it.

### Does "failed" mean the company did something wrong?

No. It means the grant did not produce the lasting result it was paid for. Plants close for reasons that have nothing to do with the grant, and a 2020 layoff notice may say more about the pandemic than about the company.

### Why does the small business share change when I move the slider?

Because "small" has no single legal meaning. Moving the line from 500 to 5,000 employees moves companies across it. Showing you the slider is more honest than picking one number and hiding the choice.

### Can I use this?

Yes. It is free to use and free to republish with credit. If you are a reporter and want the underlying files, they are in the repository, and we are glad to walk you through a specific company. Write to [connect@data4thepeople.com](mailto:connect@data4thepeople.com).

### How do I report a broken link or a mistake?

Please tell us. Email [connect@data4thepeople.com](mailto:connect@data4thepeople.com) with the company name or the page you were on, and what looked wrong. The repository also takes issues. Corrections get made in public with a note saying what changed and when.
