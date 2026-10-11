"""Keep the suite off the network. An explicit adjudicator callable still runs."""
import os

os.environ["TAXONOMY_ADJUDICATE"] = "0"
# Empty paths keep the suite from writing cache, review, or quota files under $HOME.
os.environ["TAXONOMY_CACHE_PATH"] = ""
os.environ["TAXONOMY_REVIEW_PATH"] = ""
os.environ["TAXONOMY_QUOTA_PATH"] = ""
