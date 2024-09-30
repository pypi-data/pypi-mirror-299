"""
Module for creating a Slurm script.
"""

__author__ = "Thomas Guillod"
__copyright__ = "Thomas Guillod - Dartmouth College"
__license__ = "BSD License"

import os.path
import shutil
import time


class GenError(Exception):
    """
    Exception during the script generation.
    """

    pass


def _write_title(fid, tag):
    """
    Write simulation header.

    Parameters
    ----------
    fid : file
        File descriptor for the script.
    tag : string
        Name of the job to be created.
    """

    # timing
    cmd_time = '`date -u +"%D %H:%M:%S"`'

    # write script header
    fid.write('echo "================================== %s - %s"\n' % (tag, cmd_time))
    fid.write('\n')


def _write_header(fid, tag, failfast, pragmas, filename_log):
    """
    Write the script header.

    Parameters
    ----------
    fid : file
        File descriptor for the script.
    tag : string
        Name of the job to be created.
    failfast : bool
        Switch existing the script after failures.
    pragmas : dict
        Dictionary with the pragmas controlling the Slurm job.
    filename_log : string
        Path of the log file created by during the Slurm job.
    """

    # check pragmas
    if "job-name" in pragmas:
        raise GenError("job name is already set by the script")
    if "output" in pragmas:
        raise GenError("job log is already set by the script")
    if "error" in pragmas:
        raise GenError("job log is already set by the script")

    fid.write('#!/bin/bash\n')
    fid.write('\n')

    fid.write('# ############### Slurm commands\n')
    fid.write('#SBATCH --job-name="%s"\n' % tag)
    fid.write('#SBATCH --output="%s"\n' % filename_log)
    for tag, val in pragmas.items():
        if (tag is not None) and (val is not None):
            fid.write('#SBATCH --%s="%s"\n' % (tag, val))
    fid.write('\n')

    if failfast:
        fid.write('# ############### Bash commands\n')
        fid.write('set -u\n')
        fid.write('set -e\n')
        fid.write('\n')


def _write_summary(fid, tag, filename_script, filename_log):
    """
    Add the different variables to the Slurm script.
    The content of the variables will be added to the log.

    Parameters
    ----------
    fid : file
        File descriptor for the script.
    tag : string
        Name of the job to be created.
    filename_script : string
        Path of the script controlling the simulation.
    filename_log : string
        Path of the log file created by during the Slurm job.
    """

    # get current timestamp
    timestamp = int(time.time())

    # write the job name, log file, and script file
    fid.write('echo "==================== PARAM"\n')
    fid.write(f'echo "JOB TAG      : {tag}"\n')
    fid.write('echo "HOSTNAME     : $HOSTNAME"\n')
    fid.write('\n')

    # write data about the job submission
    fid.write('echo "==================== TIME"\n')
    fid.write(f'echo "DATE GEN     : `date -u +"%D : %H:%M:%S" -d @{timestamp}`"\n')
    fid.write(f'echo "DATE RUN     : `date -u +"%D : %H:%M:%S" -d @$(date -u +%s)`"\n')
    fid.write('\n')

    # write the job id, job name, and the assigned node names
    fid.write('echo "==================== SLURM"\n')
    fid.write('echo "JOB ID       : $SLURM_JOB_ID"\n')
    fid.write('echo "JOB NAME     : $SLURM_JOB_NAME"\n')
    fid.write('echo "JOB NODE     : $SLURM_JOB_NODELIST"\n')
    fid.write('\n')


def _write_envs(fid, envs):
    """
    Handling of the environment variables.

    Parameters
    ----------
    fid : file
        File descriptor for the script.
    envs : dict
        Dictionary of environment variable to be set and exported.
    """

    if envs:
        fid.write('# ############### environment variables\n')
        for var, val in envs.items():
            if (var is not None) and (val is not None):
                fid.write('export %s="%s"\n' % (var, val))
        fid.write('\n')


def _write_commands(fid, commands):
    """
    Add a command to the Slurm script.

    Parameters
    ----------
    fid : file
        File descriptor for the script.
    commands : list
        List of commands to be executed by the job.
    """

    for tmp in commands:
        # extract data
        tag = tmp["tag"]
        cmd = tmp["cmd"]

        # header
        fid.write('echo "==================== RUN: %s"\n' % tag)

        # write command
        for cmd_sub in cmd:
            fid.write('%s\n' % cmd_sub)

        # check status
        fid.write('\n')


def _generate_file(tag, failfast, pragmas, envs, commands, filename_script, filename_log):
    """
    Generate and write a Slurm script or a Shell script.

    Parameters
    ----------
    tag : string
        Name of the job to be created.
    failfast : bool
        Switch existing the script after failures.
    pragmas : dict
        Dictionary with the pragmas controlling the Slurm job.
    envs : dict
        Dictionary of environment variable to be set and exported.
    commands : list
        List of commands to be executed by the job.
    filename_script : string
        Path of the script controlling the simulation.
    filename_log : string
        Path of the log file created by during the Slurm job.
    """

    # write the data
    with open(filename_script, "w") as fid:
        # write pragmas
        _write_header(fid, tag, failfast, pragmas, filename_log)

        # write environment variables
        _write_envs(fid, envs)

        # write script header
        _write_title(fid, tag)

        # write summary of the variables
        _write_summary(fid, tag, filename_script, filename_log)

        # write the commands to be executed
        _write_commands(fid, commands)

        # end script footer
        _write_title(fid, tag)

        # end script footer
        fid.write('# ############### exit script\n')
        fid.write('exit 0\n')
        

def run_data(def_data):
    """
    Generate a Slurm script.

    Parameters
    ----------
    def_data : dict
        Dictionary containing the job definition data.

    Returns
    -------
    filename_script : string
        Path of the script controlling the simulation.
    filename_log : string
        Path of the log file created by during the Slurm job.
    """

    # extract data
    tag = def_data["tag"]
    overwrite = def_data["overwrite"]
    failfast = def_data["failfast"]
    folder = def_data["folder"]
    pragmas = def_data["pragmas"]
    envs = def_data["envs"]
    commands = def_data["commands"]

    # create folder
    try:
        os.makedirs(folder)
    except FileExistsError:
        pass

    # check that the folder exists
    if not os.path.isdir(folder):
        raise GenError("output folder cannot be created")

    # get filenames
    filename_script = os.path.join(folder, tag + ".sh")
    filename_log = os.path.join(folder, tag + ".log")

    # remove previous files (if selected)
    if overwrite:
        try:
            os.remove(filename_script)
        except FileNotFoundError:
            pass
        try:
            os.remove(filename_log)
        except FileNotFoundError:
            pass

    # check that the output files are not existing
    if os.path.isfile(filename_script):
        raise GenError("Slurm file already exists")
    if os.path.isfile(filename_log):
        raise GenError("log file already exists")

    # create the script
    _generate_file(tag, failfast, pragmas, envs, commands, filename_script, filename_log)

    return filename_script, filename_log
