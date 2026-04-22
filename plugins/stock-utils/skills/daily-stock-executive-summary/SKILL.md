---
name: daily-stock-executive-summary
description: Generate an evidence-backed executive summary for the most recent completed U.S. trading session, covering macro drivers, sector rotation, and notable stocks.
---

# Daily Stock Executive Summary

Produce a daily U.S. equity-market briefing using live web research from current market sources.

## Research method

- Use `web` to gather market-moving news, sector context, institutional flow, commodities, Treasury data, and stock-specific context.
- Use the current environment date when it is visible in the conversation or system context. If it is not visible, derive the report window from source publication timestamps and state the date assumption explicitly.

## Preferred sources

- Treat Reuters, Yahoo Finance, and CNBC as primary factual sources for market-moving news, market pulse, and major asset moves.
- Treat Finviz and Reddit(r/stocks) as trend and sentiment checks, not as primary factual sources.
  - Use Reddit only to identify themes, retail sentiment, and disputed narratives. Do not rely on Reddit alone for factual claims.
  - Use Finviz to cross-check sector and industry performance, heat maps, and broad market leadership or weakness.
- If a required datapoint such as the 3-month Treasury yield is missing from the preferred sources, use another primary market-data source or official source for that datapoint and name it in `Sources`.

## Scope

- Default market scope is U.S. equities.
- Interpret "past day" as the most recent completed U.S. trading session.
- If the current date is a weekend or U.S. market holiday, use the latest completed session plus any intervening news that materially changes the outlook.
- Keep all dates explicit and absolute. Do not use vague references like "today" or "yesterday" without also stating the date.

## Research requirements

- Identify the important news from the last day that could change stock-investment decisions.
- Prioritize Reuters Markets, Yahoo Finance, and CNBC for news and market pulse coverage.
- Include institutional flow when available, such as ETF flows, major fund positioning, or large institutional allocation news that matters for the session.
- Include raw material signals that matter for equities, such as oil, natural gas, copper, gold, lithium, steel inputs, or agricultural commodities when relevant.
- Include the U.S. Treasury curve with 3-month, 2-year, and 10-year yields, plus whether each moved up, down, or stayed roughly flat versus the prior close.
- Identify bullish sectors and bearish sectors with a short explanation for each call.
- Use Finviz and r/stocks to cross-check trend and sentiment checks around sector leadership, crowded trades, and retail attention.
- Identify notable stocks that appear undervalued or well priced but still likely to grow. If the evidence is weak, say there is no strong candidate instead of forcing one.

## Output format

Use these exact section headings in order:

1. `Report Window`
2. `Executive Summary`
3. `Important News`
4. `Institutional Flow`
5. `Raw Material Signals`
6. `U.S. Treasury Snapshot`
7. `Bullish Sectors`
8. `Bearish Sectors`
9. `Notable Stocks`
10. `Portfolio Tactics`
11. `Risks And Invalidation`
12. `Sources`

## Section requirements

### Report Window

- State the report date and the exact market window covered.
- Use a format such as `Most recent completed U.S. trading session: April 23, 2026`.

### Executive Summary

- Give a concise top-level read on the session.
- Explain the main drivers before discussing tactics.

### Important News

- List only news that could affect stock investment decisions over the past day.
- Prefer macro policy, central-bank signals, labor and inflation data, major earnings surprises, regulation, geopolitics, and large capital-flow developments.
- Prefer Reuters, Yahoo Finance, and CNBC before lower-signal commentary sources.

### Institutional Flow

- Summarize relevant institutional flow or positioning signals.
- If data is unavailable or stale, say so explicitly.
- Do not infer institutional flow from Reddit sentiment alone.

### Raw Material Signals

- Summarize the commodities that mattered and why those moves matter for equities or specific sectors.

### U.S. Treasury Snapshot

- Report 3-month, 2-year, and 10-year yields.
- Note curve context when relevant, such as steepening, flattening, or inversion changes.

### Bullish Sectors

- Name the sectors that were strongest or have the best near-term setup.
- Give one short rationale per sector.
- Use Finviz sector or industry performance as a cross-check when available.

### Bearish Sectors

- Name the sectors under the most pressure or with the weakest near-term setup.
- Give one short rationale per sector.
- Use Finviz sector or industry performance as a cross-check when available.

### Notable Stocks

- Provide 3 to 5 names at most.
- For each stock, include:
  - ticker and company name
  - why it is notable
  - valuation or pricing context
  - growth or catalyst case
  - key risk
  - stance: `Add`, `Watch`, `Trim`, `Avoid`, `Pyramid`, or `Average Down`
- Use `Pyramid` or `Average Down` only when the evidence is very strong and explicitly explain why.

### Portfolio Tactics

- Turn the facts into non-personalized action ideas.
- Cover when the evidence supports rebalance, pyramid, average down, reducing exposure, rotating into a new sector, or waiting for confirmation.
- Keep the advice tactical and evidence-backed rather than personalized.

### Risks And Invalidation

- Separate facts from inference.
- Label any interpretation clearly as `Inference`.
- State what would invalidate the current read in the next session or next few sessions.

### Sources

- Include a short source list with titles or publishers and links.
- Include the exact sources used, and identify whether each source was used for facts, market pulse, or trend and sentiment checks.

## Style rules

- Distinguish `Facts` from `Inference` whenever judgment is involved.
- Do not invent missing data. If a required input cannot be verified, state the gap plainly.
- Keep the analysis concise but decision-useful.
- Avoid generic investment disclaimers unless the user asks for them.
- Do not provide personalized financial advice.
