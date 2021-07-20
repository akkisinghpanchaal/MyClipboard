from modes import RunMode

DEV = RunMode.DEV
PROD = RunMode.PROD

# Switch to DEV for testing
# e.g., __CLIPBOARD_MODE__ = DEV
__CLIPBOARD_MODE__ = PROD
__AUTO_SAVE_INTERVAL__ = 10     # in seconds
