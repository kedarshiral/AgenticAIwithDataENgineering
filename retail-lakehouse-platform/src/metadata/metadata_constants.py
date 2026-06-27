from pathlib import Path


# ==========================================================
# Project Root
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]


# ==========================================================
# Metadata Root
# ==========================================================

METADATA_ROOT = PROJECT_ROOT / "metadata"


# ==========================================================
# Metadata Subdirectories
# ==========================================================

CATALOG_DIR = METADATA_ROOT / "catalog"

HISTORY_DIR = METADATA_ROOT / "history"

RUNTIME_DIR = METADATA_ROOT / "runtime"

LINEAGE_DIR = METADATA_ROOT / "lineage"

REFRESH_LOG_DIR = METADATA_ROOT / "refresh_logs"

SCHEMA_CHANGE_DIR = METADATA_ROOT / "schema_changes"


# ==========================================================
# Metadata Files
# ==========================================================

RUNTIME_METRICS_FILE = (
    RUNTIME_DIR / "runtime_metrics.csv"
)

METADATA_REFRESH_LOG_FILE = (
    REFRESH_LOG_DIR / "metadata_refresh_log.csv"
)

SCHEMA_CHANGE_LOG_FILE = (
    SCHEMA_CHANGE_DIR / "schema_changes.csv"
)

LINEAGE_CATALOG_FILE = (
    LINEAGE_DIR / "lineage_catalog.json"
)


# ==========================================================
# Default Metadata Values
# ==========================================================

DEFAULT_OWNER = "Retail Data Engineering"

DEFAULT_BUSINESS_DOMAIN = "Retail"

DEFAULT_SOURCE_SYSTEM = "GitHub"

DEFAULT_REFRESH_FREQUENCY = "10 Minutes"

DEFAULT_SLA_MINUTES = 10

DEFAULT_DATA_CLASSIFICATION = "Internal"

DEFAULT_SCHEMA_VERSION = 1


# ==========================================================
# Layer Names
# ==========================================================

LANDING_LAYER = "LANDING"

L0_LAYER = "L0"

L1_LAYER = "L1"

L2_LAYER = "L2"

L3_LAYER = "L3"


# ==========================================================
# Metadata Comparison Results
# ==========================================================

NO_CHANGE = "NO_CHANGE"

COLUMN_ADDED = "COLUMN_ADDED"

COLUMN_REMOVED = "COLUMN_REMOVED"

DATATYPE_CHANGED = "DATATYPE_CHANGED"

NULLABILITY_CHANGED = "NULLABILITY_CHANGED"

PRIMARY_KEY_CHANGED = "PRIMARY_KEY_CHANGED"

FOREIGN_KEY_CHANGED = "FOREIGN_KEY_CHANGED"

ROW_COUNT_CHANGED = "ROW_COUNT_CHANGED"


# ==========================================================
# Auto Create Directories
# ==========================================================

for directory in [

    METADATA_ROOT,

    CATALOG_DIR,

    HISTORY_DIR,

    RUNTIME_DIR,

    LINEAGE_DIR,

    REFRESH_LOG_DIR,

    SCHEMA_CHANGE_DIR

]:

    directory.mkdir(
        parents=True,
        exist_ok=True
    )