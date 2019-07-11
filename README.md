# job maker

This tool is used to make job-script for XENONnT MC.

## Simple usage
Edit the header of `job_maker.py`, then,
```
python job_maker.py
```
All scpripts will be created in `made/<macro name>/` directory.
To submit the jobs,
```
> ./made/<macro name>/throw.sh
```

## Additional information
As written as, this `job_maker.py` replaces sentences of the original macro and shell script.
When you want to add additional options, please edit the if--elif--else parts in the `job_maker_py`.
