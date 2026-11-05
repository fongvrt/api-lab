# api-lab

API tests for QuickPizza (https://quickpizza.grafana.com) with pytest and requests, for the ITDS362 API testing lab.

## How to install and run

On macOS and Linux:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

In Windows PowerShell:

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest -v
```

The tests need Python 3.10 or newer. A full run sends about 140 requests to the shared QuickPizza site, so run it when you need to, never in a loop. The expected summary is `32 passed, 1 xfailed`. The xfailed test is Defect 1, described in `RESULTS.md`.

To save the output of a full run as an HTML report:

```
pytest -v --html=report.html --self-contained-html
```

## Input domain model for POST /api/ratings

| Characteristic | Blocks | Values in the tests |
|---|---|---|
| C1 Value of stars | below 1, 1 to 5 (base), above 5 | 0, 3, 6 |
| C2 Type of stars | whole number (base), decimal, text, missing | 3, 3.5, "3", no field |
| C3 Pizza | exists (base), does not exist | a new pizza, 999999999 |
| C4 Token | the user's own (base), none, wrong length | from auth, no header, token short |

### Tests that cover each block

All tests are in `test_create_rating.py`. Each non-base test changes one characteristic and keeps the others at their base.

| Characteristic | Block | Value | Covered by |
|---|---|---|---|
| C1 Value of stars | 1 to 5 (base) | 3 | `test_base_choice_is_saved` |
| C1 Value of stars | below 1 | 0 | `test_stars_out_of_range[0]` |
| C1 Value of stars | above 5 | 6 | `test_stars_out_of_range[6]` |
| C2 Type of stars | whole number (base) | 3 | `test_base_choice_is_saved` |
| C2 Type of stars | decimal | 3.5 | `test_stars_of_wrong_type[decimal]` |
| C2 Type of stars | text | "3" | `test_stars_of_wrong_type[text]` |
| C2 Type of stars | missing | no field | `test_stars_missing` |
| C3 Pizza | exists (base) | a new pizza | `test_base_choice_is_saved` |
| C3 Pizza | does not exist | 999999999 | `test_pizza_does_not_exist` |
| C4 Token | the user's own (base) | from auth | `test_base_choice_is_saved` |
| C4 Token | none | no header | `test_token_is_refused[no-header]` |
| C4 Token | wrong length | token short | `test_token_is_refused[token-short]` |
