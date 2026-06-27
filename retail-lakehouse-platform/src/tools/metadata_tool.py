from src.metadata.metadata_catalog import MetadataCatalog
from src.metadata.metadata_refresher import MetadataRefresher
from src.metadata.runtime_metrics import RuntimeMetrics


class MetadataTool:

    def __init__(self):

        self.catalog = MetadataCatalog()

        self.refresher = MetadataRefresher()

        self.runtime = RuntimeMetrics()

    # =====================================================
    # Refresh Metadata
    # =====================================================

    def refresh_metadata(

        self,

        table_name,

        layer,

        file_path,

        batch_id,

        owner,

        business_domain,

        source_system,

        primary_key=None,

        foreign_keys=None

    ):

        return self.refresher.refresh(

            table_name=table_name,

            layer=layer,

            file_path=file_path,

            batch_id=batch_id,

            owner=owner,

            business_domain=business_domain,

            source_system=source_system,

            primary_key=primary_key,

            foreign_keys=foreign_keys

        )

    # =====================================================
    # Read Metadata
    # =====================================================

    def get_metadata(
        self,
        table_name
    ):

        return self.catalog.load(
            table_name
        )

    # =====================================================
    # List Tables
    # =====================================================

    def list_tables(self):

        return self.catalog.list_tables()

    # =====================================================
    # Entire Catalog
    # =====================================================

    def get_catalog(self):

        return self.catalog.load_catalog()

    # =====================================================
    # Runtime Metrics
    # =====================================================

    def get_runtime_metrics(self):

        return self.runtime.load()

    # =====================================================
    # Latest Runtime
    # =====================================================

    def latest_runtime(self):

        return self.runtime.latest_batch()

    # =====================================================
    # Table Runtime History
    # =====================================================

    def table_runtime_history(

        self,

        table_name

    ):

        return self.runtime.get_table_metrics(

            table_name

        )