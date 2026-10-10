"""Keep the suite off the network. An explicit adjudicator callable still runs."""
import os

os.environ["TAXONOMY_ADJUDICATE"] = "0"
