from pathlib import Path
STYLES_DIR=Path(__file__).resolve().parent/"styles"
DATABASE_DIR=Path(__file__).resolve().parent/"database"
print(STYLES_DIR)
WELCOME_TCSS=STYLES_DIR/"WelcomeScreen.tcss"
ONBOARDING_TCSS=STYLES_DIR/"onboardingscreen.tcss"
ONBOARDING_DB=DATABASE_DIR/"onboardingconfig.db"