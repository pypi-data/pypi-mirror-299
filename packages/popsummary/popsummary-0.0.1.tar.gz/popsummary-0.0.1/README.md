# popsummary
A Python API for interfacing with standardized LIGO-Virgo-KAGRA Rates and Populations results. 

## Description
Hierarchical population inference of gravitational wave sources results in some standard data products. `popsummary` defines a standardized hdf5-based format for these results. The Python API enables reading and writing to this format and depends primarily on `h5py` and `numpy`. 

## Installation
### From Source:
To clone via ssh:
```
git clone git@git.ligo.org:zoheyr-doctor/popsummary.git
```
via HTTPS:
```
git clone https://git.ligo.org/zoheyr-doctor/popsummary.git
```
To install:
```
cd popsummary
pip install .
```

## Usage
See the examples folder for a tutorial notebook and other basic examples in python

## Support
Feel free to leave a git issue if you encounter any issues or have any feature requests. You can tag @zoheyr-doctor and @christian.adamcewicz in the issue. Also see our [wiki page](https://git.ligo.org/zoheyr-doctor/popsummary/-/wikis/home) for more information.

## Contributing
We happily accept merge requests! If you lack the necessary permissions for the library, contact Zoheyr.

## Authors and acknowledgment
### Primary Authors
* Christian Adamcewicz
* Storm Colloms (Reviewer)
* Zoheyr Doctor 

### Contributors
* Colm Talbot
* Tom Callister

## License
For open source projects, say how it is licensed.

## Project status
v0.0.1 is complete and reviewed!
