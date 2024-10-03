from setuptools import setup, find_packages

setup(
    name="blast_embedding",
    version="0.1.0",
    description="A BLAST-like algorithm using embeddings for bioinformatics",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
    "numpy",
    "scipy",
    "gensim",
    "scikit-learn",  # Leave scikit-learn without a pinned version
    "transformers",
    "biopython",
    "torch"
]
)
