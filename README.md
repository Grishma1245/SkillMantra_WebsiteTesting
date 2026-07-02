# SkillMantra Selenium BDD Automation Framework

> **Production-grade** test automation for [skillmantraedu.com](https://skillmantraedu.com)
> built with Python 3.11 · Selenium 4.x · behave (Gherkin BDD) · Page Object Model

---

## Table of Contents

1. [Tech Stack](#tech-stack)
2. [Project Structure](#project-structure)
3. [Prerequisites](#prerequisites)
4. [Setup](#setup)
5. [Configuration](#configuration)
6. [Running Tests](#running-tests)
7. [Viewing Reports](#viewing-reports)
8. [CI/CD — GitHub Actions](#cicd--github-actions)
9. [Design Decisions](#design-decisions)
10. [Known Limitations](#known-limitations)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| Browser Automation | Selenium WebDriver 4.x |
| BDD Framework | behave 1.2.6 (Gherkin syntax) |
| Page Object Model | Custom `BasePage` + individual page classes |
| Driver Management | webdriver-manager 4.x (auto-downloads ChromeDriver / GeckoDriver / EdgeDriver) |
| HTML Reporting | behave-html-formatter |
| Allure Reporting | allure-behave + Allure CLI |
| Config Management | python-dotenv + configparser (config.ini) |
| Logging | Python built-in `logging` module |

---

## Project Structure

```
skillmantra_automation/
├── .github/
│   └── workflows/
│       └── tests.yml               ← GitHub Actions CI pipeline
├── features/
│   ├── environment.py              ← behave hooks (lifecycle, screenshots, logging)
│   ├── home_page.feature           ← Hero, stats, cards, lead form scenarios
│   ├── courses_page.feature        ← Catalog, filters, card structure scenarios
│   ├── contact_form.feature        ← Positive/negative/boundary/XSS/contact details
│   ├── navigation.feature          ← Nav links, top bar, footer, WhatsApp widget
│   └── steps/
│       ├── home_steps.py
│       ├── courses_steps.py
│       ├── contact_steps.py
│       └── navigation_steps.py
├── pages/
│   ├── base_page.py                ← Reusable Selenium helpers (safe_click, etc.)
│   ├── home_page.py                ← HomePage POM + all locators
│   ├── courses_page.py             ← CoursesPage POM + all locators
│   └── contact_page.py             ← ContactPage POM + all locators
├── utils/
│   ├── driver_factory.py           ← Chrome / Firefox / Edge WebDriver factory
│   ├── config_reader.py            ← INI + env-var config resolver
│   └── logger.py                   ← Centralised logging (file + console)
├── config/
│   └── config.ini                  ← Default settings (base_url, browser, timeout)
├── reports/                        ← Generated at runtime (screenshots, logs, HTML)
├── .env.example                    ← Environment variable template
├── behave.ini                      ← behave runtime configuration
├── requirements.txt
└── README.md
```

---

## Prerequisites

- **Python 3.11+** — [python.org/downloads](https://python.org/downloads)
- **Google Chrome / Firefox / Edge** installed locally
- **Git** (for cloning and GitHub Actions)
- **Allure CLI** (optional, for Allure HTML report generation locally)
  ```bash
  # macOS/Linux via npm:
  npm install -g allure-commandline --save-dev
  # or via Homebrew (macOS):
  brew install allure
  ```

---

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd skillmantra_automation
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment (optional)

Copy `.env.example` to `.env` and edit values:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|---|---|---|
| `BROWSER` | `chrome` | `chrome`, `firefox`, or `edge` |
| `HEADLESS` | `false` | `true` for headless (CI/no-GUI) mode |
| `BASE_URL` | `https://skillmantraedu.com` | Override for staging/local instance |
| `TIMEOUT` | `20` | Explicit wait timeout in seconds |
| `SCREENSHOT_ON_FAILURE` | `true` | Capture screenshot on step failure |

---

## Running Tests

> All commands below should be run from the `skillmantra_automation/` directory.

### Run the full test suite

```bash
behave
```

### Run only `@smoke` tests (critical-path, fast)

```bash
behave --tags=@smoke
```

### Run only `@regression` tests

```bash
behave --tags=@regression
```

### Run a specific feature file

```bash
behave features/contact_form.feature
```

### Run a specific scenario by name

```bash
behave --name "Submit the contact form with valid data"
```

### Run multiple tags (AND logic)

```bash
behave --tags="@smoke and @contact"
```

### Run in headless mode (no browser UI)

```bash
HEADLESS=true behave --tags=@smoke
# Windows PowerShell:
$env:HEADLESS="true"; behave --tags=@smoke
```

### Run with a different browser

```bash
BROWSER=firefox behave --tags=@smoke
```

### Dry run (validate feature files without executing steps)

```bash
behave --dry-run
```

---

## Viewing Reports

### HTML Report (behave-html-formatter)

Generate while running:

```bash
behave --format=behave_html_formatter:HTMLFormatter --outfile=reports/report.html
```

Open `reports/report.html` in any browser.

### Allure Report

**Step 1:** Run tests with Allure formatter:

```bash
behave \
  --format=allure_behave.formatter:AllureFormatter \
  --outfile=reports/allure-results
```

**Step 2:** Generate and open the HTML report:

```bash
allure generate reports/allure-results --clean -o reports/allure-report
allure open reports/allure-report
```

### Both formats simultaneously

```bash
behave \
  --format=behave_html_formatter:HTMLFormatter --outfile=reports/report.html \
  --format=allure_behave.formatter:AllureFormatter --outfile=reports/allure-results \
  --format=pretty
```

### JUnit XML Reports (CI Integration)

By default, the framework writes standard JUnit-compatible XML test results to:
```
reports/xml/
```
These can be parsed by CI servers like Jenkins or Azure DevOps. You can control this behavior via `behave.ini` (`junit = true/false`) or override it using the `--no-junit` / `--junit` CLI flag.

### Screenshots

Failure screenshots are saved automatically to `reports/screenshots/` with the
scenario name and timestamp in the filename.

### Logs

Run logs are written to `reports/logs/test_run_YYYYMMDD_HHMMSS.log`.

---

## CI/CD — GitHub Actions

The pipeline is defined in [`.github/workflows/tests.yml`](.github/workflows/tests.yml).

### Triggers

| Event | Job | Tags |
|---|---|---|
| Push to `main` / `develop` | Smoke tests | `@smoke` |
| Pull Request to `main` | Smoke tests | `@smoke` |
| Manual (`workflow_dispatch`) | Smoke or Regression | Configurable |

### Artifacts uploaded after each run

| Artifact | Contents | Retention |
|---|---|---|
| `behave-html-report` | `reports/report.html` | 14 days |
| `allure-report` | Full Allure HTML dashboard | 14 days |
| `failure-screenshots` | PNG screenshots from failed steps | 14 days |
| `test-logs` | Python logging output | 14 days |

### Running manually via GitHub UI

1. Go to **Actions** tab → **SkillMantra Automation Suite**
2. Click **Run workflow**
3. Set `tags` (e.g. `@smoke`) and `browser` (e.g. `chrome`)
4. Click **Run workflow**

---

## Design Decisions

### Why `behave` (not pytest-bdd)?

The project spec explicitly requires `behave`. Behave is the canonical Python BDD
framework, provides native Gherkin support, and integrates with
`behave-html-formatter` and `allure-behave` without additional adapters.

### Explicit waits everywhere

The SkillMantra site is rendered via Tailwind + vanilla JS. Dynamic content loads
asynchronously. **All element interactions use `WebDriverWait` + `expected_conditions`.**
Zero `time.sleep()` calls exist anywhere in the framework.

### Locator strategy

Locators are prioritised in this order:
1. `id` attribute (most stable) — where available
2. `name` attribute — for form inputs
3. `placeholder` attribute — for inputs without name/id
4. Structural XPath — using text content and parent/child relationships
5. CSS class chains — using Tailwind classes only when semantically meaningful

All locators reside **exclusively** in Page Object classes. Step definitions
contain zero selectors.

### BasePage `safe_click()` fallback

Standard `.click()` occasionally fails on Tailwind-styled overlapping elements.
`safe_click()` falls back to a JavaScript `arguments[0].click()` automatically,
eliminating `ElementClickInterceptedException` flakiness.

---

## Known Limitations

### 1. Footer "Top Domains" links — anchor-only navigation

The footer "Top Domains" section links point to `#courses` (an anchor fragment on
the homepage), **not** real sub-routes like `/courses/data-science`. This is the
actual site behaviour. Test assertions reflect this reality rather than hardcoding
a false pass against a non-existent route. These are flagged with comments in both
the feature file and step definitions.

### 2. WhatsApp widget — external redirect scope

The "Initialize Secure Chat" button opens `api.whatsapp.com` in a new tab. The
automation test verifies:
- The widget is visible
- Clicking it opens a new tab
- The new tab URL contains `api.whatsapp.com`

Beyond this point, the new tab is an external domain outside the test scope.
The driver switches back to the original tab immediately after verification.
Pre-filled message query parameters in the WhatsApp URL are assumed correct but
not deeply validated (would require WhatsApp account credentials).

### 3. Contact form success message wording

The test asserts for "Transmission Successful" (based on typical SkillMantra
terminology). If the backend changes the confirmation wording, update the
`FORM_SUCCESS_MSG` XPath in `contact_page.py` accordingly.

### 4. HTML5 form validation browser differences

Native HTML5 constraint-validation API messages (`validationMessage`) differ by
browser and OS locale. The contact form step definitions check **both** native
HTML5 validation AND custom error message elements, making them browser-agnostic.

### 5. Contact form `/contact-us` vs `/contact`

Live URL check confirmed the contact page route is `/contact` (not `/contact-us`,
which returns 404). The framework uses `/contact` everywhere.

### 6. WhatsApp chat widget locator fragility

The floating chat widget has no stable `id` attribute. The locator uses a combined
XPath that matches text content (`Core Advisor`, `Chat`) and `href` containing
`whatsapp`. If the widget's text changes, update `WHATSAPP_WIDGET_BTN` in
`home_page.py`.

---

## Contributing

1. Keep all locators inside Page Object classes.
2. Add `@smoke` to any new critical-path scenario.
3. Add `@regression` to all other scenarios.
4. Do not use `time.sleep()` — use `WebDriverWait` exclusively.
5. Run `flake8 .` and `black --check .` before committing.

---

*Generated for SkillMantra — IT Certification Academy | https://skillmantraedu.com*
