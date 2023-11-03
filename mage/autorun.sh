#!/bin/sh
mage run_pipeline pokemon_collector
mage start pokemon_mage_orch --host 0.0.0.0 --port 6789