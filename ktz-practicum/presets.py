"""Compatibility catalogue for tests and scripts; all task data lives in JSON."""
from variant_files import load_variants, variants_directory

PRESETS = load_variants(variants_directory())
