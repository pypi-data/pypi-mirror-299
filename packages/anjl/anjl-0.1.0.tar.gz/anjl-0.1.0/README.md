# anjl - A neighbour-joining library for Python

`anjl` is a Python package providing implementations of the
[neighbour-joining
algorithm](https://en.wikipedia.org/wiki/Neighbor_joining) of Saitou
and Nei and some associated utilities.

## Installation

```
pip install anjl
```

## Usage

```python
import anjl
```

### Canonical neighbour-joining

```python
help(anjl.canonical_nj)
```

## About

There are implementations of neighbour-joining available in
[BioPython](https://biopython.org/docs/latest/api/Bio.Phylo.TreeConstruction.html#Bio.Phylo.TreeConstruction.DistanceTreeConstructor),
[scikit-bio](https://scikit.bio/docs/dev/generated/skbio.tree.nj.html)
and
[biotite](https://www.biotite-python.org/latest/apidoc/biotite.sequence.phylo.neighbor_joining.html),
but they are relatively slow for larger numbers of nodes. I created
this package to provide faster implementations for use in population
genomics.

Bug reports and suggestions are welcome but I make no promises
regarding support, please be patient and understanding!
