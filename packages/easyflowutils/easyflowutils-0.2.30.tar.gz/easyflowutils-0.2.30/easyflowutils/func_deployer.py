import os
import subprocess


def deploy_func(func_name, region="europe-west9", source="."):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    command = (
        f"gcloud functions deploy {func_name} "
        f"--gen2 "
        f"--runtime=python312 "
        f"--region={region} "
        f"--source={source} "
        f"--entry-point={func_name} "
        f"--trigger-http "
        f"--allow-unauthenticated"
    )
    subprocess.run(command, shell=True, check=True)
