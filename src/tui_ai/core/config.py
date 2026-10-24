from pathlib import Path
STYLES_DIR=Path(__file__).resolve().parent.parent/"styles"
DATABASE_DIR=Path(__file__).resolve().parent.parent/"database"
WELCOME_TCSS=STYLES_DIR/"WelcomeScreen.tcss"
ONBOARDING_TCSS=STYLES_DIR/"onboardingscreen.tcss"
MAIN_TCSS=STYLES_DIR/"mainscreen.tcss"
ONBOARDING_DB=DATABASE_DIR/"onboardingconfig.json"
CONFIG_DB=DATABASE_DIR/"config.json"
