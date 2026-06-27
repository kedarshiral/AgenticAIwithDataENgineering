#!/bin/bash

PROJECT="retail-lakehouse-platform"

mkdir -p $PROJECT

cd $PROJECT || exit

# Root files
touch README.md
touch requirements.txt
touch .gitignore
touch pyproject.toml

# Configs
mkdir -p configs
touch configs/tables.yaml
touch configs/sources.yaml
touch configs/dq_rules.yaml
touch configs/lineage.yaml
touch configs/pipeline.yaml
touch configs/settings.yaml

# Data Lake Layers
mkdir -p data/l0_landing/{customers,orders,products,inventory,marketing,finance}
mkdir -p data/l1_raw
mkdir -p data/l2_curated
mkdir -p data/l3_business
mkdir -p data/metadata
mkdir -p data/audit
mkdir -p data/quarantine

# Source Code
mkdir -p src/{generators,ingestion,transformations,dq,metadata,audit,agents,tools,storage,api,utils}

# Generators
touch src/generators/customers.py
touch src/generators/products.py
touch src/generators/orders.py
touch src/generators/inventory.py
touch src/generators/marketing.py
touch src/generators/finance.py
touch src/generators/generate_data.py

# Ingestion
touch src/ingestion/github_fetcher.py
touch src/ingestion/landing_loader.py
touch src/ingestion/raw_loader.py
touch src/ingestion/watermark_manager.py

# Transformations
touch src/transformations/l1_raw.py
touch src/transformations/l2_curated.py
touch src/transformations/l3_business.py
touch src/transformations/scd_type2.py

# DQ
touch src/dq/dq_engine.py
touch src/dq/null_checks.py
touch src/dq/duplicate_checks.py
touch src/dq/fk_checks.py
touch src/dq/schema_checks.py

# Metadata
touch src/metadata/metadata_catalog.py
touch src/metadata/lineage_catalog.py
touch src/metadata/data_dictionary.py

# Audit
touch src/audit/audit_logger.py
touch src/audit/job_tracker.py

# Agents
mkdir -p src/agents/chat
mkdir -p src/agents/planner
mkdir -p src/agents/rca
mkdir -p src/agents/validator
mkdir -p src/agents/graph

touch src/agents/chat/chat_agent.py
touch src/agents/planner/planner_agent.py
touch src/agents/rca/root_cause_agent.py
touch src/agents/validator/validator_agent.py
touch src/agents/graph/dataops_graph.py

# Tools
touch src/tools/metadata_tool.py
touch src/tools/lineage_tool.py
touch src/tools/dq_tool.py
touch src/tools/audit_tool.py
touch src/tools/approval_tool.py
touch src/tools/notification_tool.py

# Storage
touch src/storage/duckdb_manager.py
touch src/storage/parquet_manager.py

# API
touch src/api/app.py

# Utils
touch src/utils/constants.py
touch src/utils/logger.py
touch src/utils/helpers.py
touch src/utils/file_utils.py

# UI
mkdir -p ui
touch ui/streamlit_app.py

# Scripts
mkdir -p scripts
touch scripts/run_generation.py
touch scripts/run_l0_to_l1.py
touch scripts/run_l1_to_l2.py
touch scripts/run_l2_to_l3.py
touch scripts/run_dq.py
touch scripts/run_metadata_refresh.py

# Tests
mkdir -p tests
touch tests/test_generation.py
touch tests/test_dq.py
touch tests/test_lineage.py
touch tests/test_transformations.py

# Docs
mkdir -p docs
touch docs/architecture.md
touch docs/lineage.md
touch docs/data_dictionary.md
touch docs/agent_design.md
touch docs/interview_notes.md

# Logs
mkdir -p logs

echo "✅ Retail Lakehouse Platform structure created successfully!"
