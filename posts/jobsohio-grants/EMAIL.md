# Mailchimp teaser: Every JobsOhio grant, in one searchable tool

Drafted from the post text only. Every number here appears in the post.
Paste each block below into Mailchimp as it is; the fences are not part of
the content.

---

## Subject and preview

```
Every JobsOhio grant, searchable
```
*31 characters.*

```
Twelve years, 2,415 grants, and what happened to the companies after
```
*68 characters. Does not repeat the subject.*

---

## 1. Hero image

`posts/jobsohio-grants/images/jobsohio-grants-hero-email.jpg` (152 KB)

Alt text:

```
Summary cards from the JobsOhio grants tool, covering 2,415 grants and $1.35 billion to 1,700 companies and organizations, fiscal years 2014 to 2025. Two headline figures: 19% of the dollars went to businesses under 500 employees at the parent company, and 7.8% went to businesses under 100. A grid crossing size with home state, where small means under 500 employees, shows the share of dollars: small Ohio 16%, small elsewhere 2.9%, large Ohio 20%, large elsewhere 61%.
```

*The percentages in that alt text are not in the post's text. They are on the
hero image itself, and this is the post's own `hero_alt`, so a reader
clicking through meets the same picture with the same description. Every
number in the email's own prose is in the post: 2,415, $1,345,318,862,
1,700 and 40.*

---

## 2. Headline

```
Every JobsOhio grant, in one searchable tool
```

---

## 3. Body, part one

```
This started with one question. If Ohio has a fixed amount of cash to invest in economic development, what strategy gives Ohioans the greatest return? We cannot answer that. But we could at least work out which strategy JobsOhio has been running.

So we set out to do one narrow thing: take every grant JobsOhio has given out and sort it into a 2x2 matrix. Was the grant provided to a small or a large business? Was it provided to an Ohio-based company, or to a company headquartered outside of Ohio? With that, we could reverse engineer the strategy. Has JobsOhio chosen to invest in small local employers within communities, or to attract large corporations to relocate to Ohio?

This was not an easy project, because there is no clean database we could join that had business size or headquarters location. So we studied each grant line by line, twelve years of them, 2,415 payments and $1,345,318,862 to 1,700 companies and organizations, and came to our best judgement on where each recipient belonged.
```

---

## 4. Chart

`posts/images/04-size-and-home-state.png` (1600x900)

Alt text:

```
A grid crossing business size with home state, showing the share of JobsOhio's grant dollars in each cell. Small companies, under 500 employees at the parent, headquartered in Ohio took 16% of the dollars and are 57% of the companies. Small companies based elsewhere took 2.9% and are 7.2%. Large Ohio companies took 20% and are 8.4%. Large companies based elsewhere took 61% of the dollars and are 27% of the companies. Source: JobsOhio Form 990 Schedule I, fiscal years 2014 to 2025.
```

*The 2x2 itself, at the 500-employee setting the tool opens on, built from the
same data file as the tool by `scripts/48_hero.py --matrix`. The four dollar
shares are also on the post's hero image. The four company shares are in the
email only.*

## 5. Body, part two

```
What we didn't realize was that as we were going through each public grant line by line, we could start to collect additional information, that is arguably even more valuable for anyone trying to understand how JobsOhio has performed.

We were able to find grants given to companies that, after receiving the grant, announced a mass layoff at the funded site, entered bankruptcy or receivership, closed the funded site, or ended the service the grant paid for. We call each of these a "failed" grant, because it did not perform as expected. There are 40 of them.

Note that we cannot tell you which grants succeeded. JobsOhio does not regularly announce when companies have met their hiring targets, so there is no success column to put beside this one. But whether a grant failed is in the public domain, through WARN notices, bankruptcy filings and court dockets. Wherever we could find one of those documents, it is linked, so you can click straight through to it.

That is the point of this work: to organize and present data that has been hiding in the public domain, so we can all ask better questions about how JobsOhio has performed. We are not writing the stories in here. We built the tool so Ohioans and local reporters can.
```

---

## 6. Call to action

```
Open the tool, free, no account:
https://www.data4thepeople.com/p/jobsohio-grants
```
