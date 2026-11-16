---
title: Every JobsOhio grant, in one searchable tool
subtitle: 2,415 payments, $1.35 billion, 1,700 companies, and what happened to them afterward
slug: jobsohio-grants
date: 2026-11-17
section: Data 4 Thought
hero: images/jobsohio-grants-hero-1680x1080.png
hero_alt:
meta_title:
description:
keywords:
schema_type: article
drop_cap: true
heading_spacer: 20px
caption_spacer: 20px
dividers: false
---

# Every JobsOhio grant, in one searchable tool

## Purpose

::: spacer 5px

This visualization on JobsOhio grants has been months in the making. It started as a follow-up to our work [benchmarking JobsOhio performance against other states](https://www.data4thepeople.com/p/jobsohio-post). We started to think more about the underlying strategies for state-level economic development. Specifically, if Ohio has a fixed amount of cash to invest in economic development and job creation, what strategy will provide the greatest return on investment for Ohioans?

To be clear, this visualization doesn't answer that complex guiding question. Rather, its goal initially was to just collect the data on all the grants given out by JobsOhio and classify them into a 2x2 matrix. Was the grant provided to a small or a large business? Was the grant provided to an Ohio-based company, or a company headquartered outside of Ohio? With this data we could at least reverse engineer JobsOhio's strategy. Has it chosen to invest in small local employers within communities, or to attract large corporations to relocate to Ohio?

This was not an easy project, because there is no clean database we could join that had business size or headquarters location. And so, we studied each grant line by line to come up with our best judgement on where the recipient company belonged in our 2x2 matrix.

What we didn't realize was that as we were going through each public grant line by line, we could start to collect additional information, that is arguably even more valuable for those looking to understand how JobsOhio has performed. We were able to find grants given to companies that, after receiving the grant, announced a mass layoff at the funded site, entered bankruptcy or receivership, closed the funded site, or ended the service the grant paid for. We also track separately which companies JobsOhio sued to get its money back. We call each of these a "failed" grant as it did not perform as expected. Note that we cannot determine if any of the grants were successful as JobsOhio doesn't regularly announce when companies have met their hiring targets. But the data to determine if there was a failure is in the public domain through WARN notices, bankruptcy filings, and court dockets. Wherever we can find one of these documents, it is linked so you can click through as part of your research process.

Note another factor we could not capture is when a facility was simply never built at all. This happened with the ethane cracker proposed for Dilles Bottom in Belmont County, where $28,599,868 went to three companies to clear and prepare a site for a plant that was never built. If JobsOhio does not sue the company, we cannot see the failure unless a filing is mandated by the state. If no jobs were ever added, no jobs are eliminated, leaving a blind spot in the tool.

That said, we still believe this is the best free public tool to allow for research on grant performance in JobsOhio available in the public domain. Our goal is not to provide extensive takeaways on the stories living in this tool, but rather to provide this to local journalists and all Ohioans to better be able to ask questions of JobsOhio to gain confidence that our liquor sales dollars (which before JobsOhio was created used to flow through the state's own audited books) are being invested to help improve the lives of Ohioans.

## The tool

::: spacer 5px

Here is the short version. It carries the same figures as the full tool, in a smaller frame.

<iframe src="https://data4thepeople.github.io/JobsOhioSmallBiz/dist/embed.html" height="780" width="100%" style="border:0" title="Where JobsOhio's grant money went"></iframe>

::: spacer 40px

::: blurb If you are going to work from this, use the full version
Every figure in the frame above is in the full tool, but the full tool also lets you filter to any outcome, read the source behind each finding, and see every one of the 76 candidates we checked and threw out, with the reason. **If you are a reporter working from this, use the full version.** Several rows carry caveats that decide whether a number means what it looks like, and those caveats sit on the row rather than in the summary.

**[Open the full tool and the method notes](https://data4thepeople.github.io/JobsOhioSmallBiz/)**
:::

::: spacer 20px

::: blurb Found a broken link or a mistake? Please tell us
This tool has thousands of links in it and twelve years of records behind it. If you are exploring it and a link does not open, a company is in the wrong place, a number looks wrong, or we have missed something you know about, please email us at **[connect@data4thepeople.com](mailto:connect@data4thepeople.com)** and we will fix it. We would rather hear it from you than leave it wrong. Corrections are made in public, with a note saying what changed and when.
:::

## How to use it

::: spacer 5px

Two controls sit at the top and change every number on the page.

**Count** switches between operating businesses only and all recipients. JobsOhio also pays universities, hospitals, local governments, nonprofits and site developers. Those are real grants, but they are not companies, and leaving them in the denominator makes the business picture look different than it is.

**"Small" means under** sets the employee line at 100, 500 or 5,000 workers at the parent company. There is no single legal definition of a small business. The Small Business Administration sets a separate threshold for each of 978 industries. About 500 of those industries are measured by annual revenue rather than headcount at all, and among the ones that do count employees the line runs from 100 to 1,500. We default to 500 because it is the familiar shorthand and because it is the conservative choice: for manufacturing, which is most of what JobsOhio funds, the median SBA threshold is 1,000 employees, so our default counts fewer companies as small than the SBA would.

Below the controls, the table is the part most people will want. You can search a company, a city or a parent, switch between one row per company and one row per payment, and sort any column. Clicking an outcome anywhere on the page filters the table to those companies and explains in a sentence what you are now looking at.

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

One more thing about all of them. **A clause is not a recovery.** The same agreement gives JobsOhio the discretion to decide whether a company complied, whether to demand repayment, how much, and whether to waive it. Across twelve years, $26,040,088 has come back, which is 1.9% of what went out.

### Sued by JobsOhio

JobsOhio's own lawsuit against that company in the Franklin County Court of Common Pleas, where JobsOhio is headquartered, to get grant money back. Hover a row for the case number, what was sought and how the case ended. Suits filed in another county, in federal court or in another state would not appear here, so the count is a floor.

::: divider

## Where this comes from

::: spacer 5px

Every dollar starts with one source: Schedule I of JobsOhio's IRS Form 990, fiscal years 2014 through 2025, taken from the IRS e-file data. Schedule I lists grants over $5,000 on a cash basis, so these are dollars actually paid in a year, not dollars committed. Grants of $5,000 or less are not on it.

That is 2,415 payments to 1,789 payees, traced to 1,700 parent companies and organizations, totaling $1,345,318,862 after $26,040,088 of recorded reversals.

Everything after that is layered on top: SEC filings and Form 5500 plan data for ownership and headcount, JobsOhio's own monthly project reports for the program and the project county, the Ohio WARN register for mass layoffs, federal bankruptcy dockets, and the Franklin County Clerk of Courts for the lawsuits and the grant agreements. Links go to the record, not to a summary of it. Every link was fetched and confirmed to resolve; where nothing resolved, the name is plain text rather than a dead link.

The full method, including every judgement call and every number that moved, is in the repository. So is the data, as plain CSV files you can open in a spreadsheet.

**[Read the full method notes and download the data](https://github.com/Data4ThePeople/JobsOhioSmallBiz)**

## What this tool cannot tell you

::: spacer 5px

We would rather you know the holes than find them later.

**It cannot tell you what worked.** There is no success column, because JobsOhio does not routinely publish whether a company met its hiring targets.

**It cannot see a project that was never built.** A company that takes the money and quietly never breaks ground files no layoff notice, because there were no jobs to eliminate. The Belmont County cracker is the clearest example: $28,599,868 is still out across three companies for a plant that was never built, and not one of the three appears in the failure count. Some of that money did come back. PTTGC America was paid $31,451,981 and repaid $20,000,000, which [The Intelligencer reported in March 2022](https://www.theintelligencer.net/news/top-headlines/2022/03/ptt-global-pays-jobsohio-20m-for-failing-to-move-on-belmont-county-cracker-plant/) it did after failing to make an investment decision on the plant. That single repayment is 77% of all the money this tool reports as returned, and it is the only one in twelve years with a published reason attached.

**The address on the form is where the check went, not where the project was.** About 28.5% of the dollars were mailed to an address outside Ohio, usually a corporate headquarters. Where JobsOhio's project reports name a county, we use that instead.

**The failure count is a floor, not a total.** It counts what we could verify from a document. A failure that produced no filing, no notice and no coverage is invisible to the method.

**Most of the repayment labels rest on an inference rather than a document.** 65% of the money carries "in the standard agreement," which means we read the form and not that company's copy of it. See the section above. It is the single largest caveat in the tool.

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
