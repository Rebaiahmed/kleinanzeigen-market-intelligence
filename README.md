# Kleinanzeigen Market Intelligence

**Deutsch:** Ein unabhängiges Open-Source-Projekt für reproduzierbare Analysen und die Bewertung von Preis- und Produktvergleichsverfahren. Die Beispieldaten sind synthetisch und beschreiben keinen realen Markt. [Deutsche Einführung](README.de.md).

This repository provides small, offline tools for evaluating marketplace asking-price estimates and product matching, and summarizing price distributions. It is independently useful without an AnzeigenBoost account. It does not scrape any marketplace.

## What's included

- Asking-price counts, median and linearly interpolated 25th/75th percentiles per category.
- Price prediction MAE, median absolute error, MAPE excluding zero reference prices, and over/underestimate counts.
- Binary matching precision, recall, F1 and confusion counts. Ambiguous examples are held separately, not scored as negatives.
- A small explicitly synthetic dataset and test inputs. **These are examples of code behavior, not a benchmark of any model or real market.**

Python 3.10+ is required; runtime uses only the standard library. From the repository root:

```sh
python -m unittest discover -s tests -v
python -m market_intelligence.cli asking-prices examples/asking-prices.synthetic.json
python -m market_intelligence.cli prices examples/price-predictions.synthetic.json
python -m market_intelligence.cli matching examples/matching-predictions.synthetic.json
```

Each CLI input is a JSON array. Price metric rows contain numeric `reference` and `predicted`; matching rows contain boolean `label` and `predicted`; asking-price rows contain `category` and `asking_price_eur`. Values must be non-negative and finite. Zero-reference rows are excluded from percentage error and counted separately. Undefined classification metrics return JSON null. Examples have fictional values and must not be presented as findings.

## Datasets and research

See [dataset provenance](datasets/README.md) and [research methodology](docs/methodology.md). The included cases demonstrate smartphones, gaming and furniture; vehicles, tools and other categories require appropriately licensed data and have no real observations here. No marketplace dataset or independently verified benchmark results are published. Listing optimization and model comparison are future work; no model calls or API credentials are required by this version.

Architecture: JSON input → offline analysis or metric functions → JSON summary. Separate source/prediction files allow independent inspection. Tests validate formulas and fixture structure. The package does not collect data or make network requests.

## About AnzeigenBoost

[AnzeigenBoost](https://anzeigenboost.de/) is a Chrome extension for sellers on Kleinanzeigen, with listing optimization, competitor comparison, price suggestions, scheduled reposting and selling workflow tools. Availability can vary by account or feature settings. [Chrome Web Store](https://chromewebstore.google.com/detail/noagiapohlenpolcbeghlmngalapbobe) · [Product guides](https://anzeigenboost.de/ratgeber/anzeige-als-vorlage-speichern)

**Want to use these insights when selling on Kleinanzeigen? Explore AnzeigenBoost.**

This is an independent research and engineering initiative by AnzeigenBoost. It is not affiliated with, endorsed by, or operated by Kleinanzeigen. Product and brand names belong to their respective owners.

## Contributing and security

See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md). Share data only when you can document collection, consent, redistribution permission and privacy safeguards. Asking prices are not transaction prices; samples need not represent the overall market. No personal data or live marketplace content should be submitted without documented rights and review.

Original code and synthetic fixtures are released under the [MIT License](LICENSE). No third-party dataset or software is redistributed. Python is a separately licensed runtime.
