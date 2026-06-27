import time

from src.metadata.metadata_generator import MetadataGenerator
from src.metadata.metadata_catalog import MetadataCatalog
from src.metadata.metadata_comparator import MetadataComparator
from src.metadata.schema_versioning import SchemaVersionManager
from src.metadata.runtime_metrics import RuntimeMetrics


class MetadataRefresher:

    def __init__(self):

        self.generator = MetadataGenerator()

        self.catalog = MetadataCatalog()

        self.comparator = MetadataComparator()

        self.version_manager = SchemaVersionManager()

        self.runtime_metrics = RuntimeMetrics()

    # ==========================================================
    # Refresh Metadata
    # ==========================================================

    def refresh(
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

        start = time.time()

        # ---------------------------------------
        # Generate Current Metadata
        # ---------------------------------------

        current_metadata = self.generator.generate(

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

        # ---------------------------------------
        # Load Previous Metadata
        # ---------------------------------------

        previous_metadata = self.catalog.load(
            table_name
        )

        # ---------------------------------------
        # Compare
        # ---------------------------------------

        comparison = self.comparator.compare(

            previous_metadata,

            current_metadata

        )

        # ---------------------------------------
        # Version Management
        # ---------------------------------------

        if previous_metadata is None:

            current_metadata["schema_version"] = 1

        else:

            current_metadata["schema_version"] = (

                previous_metadata["schema_version"]

            )

            if self.version_manager.should_increment(
                comparison
            ):

                current_metadata = (

                    self.version_manager.increment(
                        current_metadata
                    )

                )

        # ---------------------------------------
        # Save Catalog
        # ---------------------------------------

        self.catalog.save(
            current_metadata
        )

        # ---------------------------------------
        # Save Version History
        # ---------------------------------------

        if comparison["changed"]:

            self.version_manager.save_history(
                current_metadata
            )

        # ---------------------------------------
        # Runtime Metrics
        # ---------------------------------------

        execution_time = (

            time.time()

            - start

        )

        self.runtime_metrics.log(

            metadata=current_metadata,

            execution_time=execution_time,

            status="SUCCESS"

        )

        # ---------------------------------------
        # Return Result
        # ---------------------------------------

        return {

            "table_name": table_name,

            "comparison": comparison,

            "schema_version":

                current_metadata["schema_version"]

        }