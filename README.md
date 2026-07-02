Generated for SkillMantra — IT Certification Academy | https://skillmantraedu.com
SkillMantra Automation
Selenium + Python BDD (Behave) test automation framework for skillmantraedu.com.
Built using the Page Object Model (POM) design pattern with Gherkin feature files, covering navigation, 
homepage, course catalog, and contact form functionality.

#Tech Stack
Language: Python 3.11+
Test Runner / BDD: Behave (Gherkin)
Browser Automation: Selenium WebDriver 4.x
Driver Management: webdriver-manager
Design Pattern: Page Object Model (POM)
Reporting: XML (JUnit-style) generated per feature
Config Management: python-dotenv / config

#project structure
skillmantra_automation/
├── .github/
│   └── workflows/
│       └── tests.yml               # GitHub Actions CI pipeline configuration
├── config/
│   └── config.ini                  # Central configuration file for default settings
├── features/
│   ├── steps/                      # Step definition implementations for Gherkin features
│   │   ├── __init__.py
│   │   ├── contact_steps.py
│   │   ├── courses_steps.py
│   │   ├── home_steps.py
│   │   └── navigation_steps.py
│   ├── contact_form.feature        # BDD Scenarios for Contact Form validation
│   ├── courses_page.feature        # BDD Scenarios for Course Catalog & Filters
│   ├── environment.py              # behave test lifecycle hooks (before/after hooks)
│   ├── home_page.feature           # BDD Scenarios for Hero, cards, and lead forms
│   └── navigation.feature          # BDD Scenarios for Header, Footer & Quick links
├── pages/                          # Page Object Model (POM) classes
│   ├── __init__.py
│   ├── base_page.py                # Base Page class with reusable Selenium wrappers
│   ├── contact_page.py             # Page Object for Contact Page (Locators + Actions)
│   ├── courses_page.py             # Page Object for Courses Page (Locators + Actions)
│   └── home_page.py                # Page Object for Home Page (Locators + Actions)
├── utils/                          # Utility functions and modules
│   ├── __init__.py
│   ├── config_reader.py            # Resolver for config settings (INI & ENV variables)
│   ├── driver_factory.py           # Factory to initialize and manage WebDrivers
│   └── logger.py                   # Centralized logging manager (console + file logger)
├── .env.example                    # Template file for environment variable overrides
├── .gitignore                      # Git configuration to ignore build, env, and report files
├── behave.ini                      # behave framework configuration file
├── LICENSE                         # Repository open-source license
├── README.md                       # Comprehensive framework setup & usage documentation
└── requirements.txt                # Python package dependency list

##Setup
1.Clone the repository
bash   git clone https://github.com/<your-username>/skillmantra_automation.git
   cd skillmantra_automation

2.Create and activate a virtual environment
bash   python -m venv myenv
 myenv\Scripts\activate

3.Install dependencies
bash   pip install -r requirements.txt

##Running Tests

1.Run the full suite:
behave

2.Run a specific feature file:
behave features/contact_form.feature

3.Run tests by tag (e.g. smoke suite only):
behave --tags=@smoke


##To view the Allure- Report
1.allure open allure-report
2.behave -f allure_behave.formatter:AllureFormatter -o allure-results
3.allure open allure-report







