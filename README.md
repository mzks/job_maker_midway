# job maker

This tool is used to make job-script for XENONnT MC.

## Simple usage
Edit the header of `job_manager.py`, then,
```
./run.sh
```
All scpripts will be created in `product/<macro name>/` directory.

## Additional information
As written as, this `job_maker.py` replaces sentences of the original macro and shell script.
When you want to add additional options, please edit the if--elif--else parts in the `job_maker_py`.
