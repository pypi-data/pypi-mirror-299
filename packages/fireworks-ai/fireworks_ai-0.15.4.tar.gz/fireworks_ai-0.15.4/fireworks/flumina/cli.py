from .exec import exec_flumina_script
from .logging import get_logger
from .util import log_time

import argparse
import json
import importlib.resources
import shutil
import sys
import os


def validate_command(args):
    file_path = os.getcwd()

    with log_time(f"Validating fireworks.json"):
        fw_json_path = os.path.join(file_path, "fireworks.json")
        if not os.path.exists(fw_json_path):
            get_logger().error(
                "fireworks.json does not exist in the current directory. Ensure "
                "you have run flumina init in this directory"
            )
            sys.exit(-1)

        with open(fw_json_path, "r") as f:
            loaded_fw_json = json.load(f)
            if loaded_fw_json.get("_is_flumina_model", None) != True:
                get_logger().error(
                    "fireworks.json did not have correct _is_flumina_model. Ensure "
                    "you have run flumina init in this directory"
                )
                sys.exit(-1)

    with log_time(f"Running script {file_path} for validation"):
        script_path = os.path.join(file_path, "flumina.py")
        if not os.path.exists(script_path):
            get_logger().error(
                "flumina.py does not exist in the current directory. Ensure "
                "you have run flumina init in this directory"
            )
            sys.exit(-1)

        exported_mod, _ = exec_flumina_script(script_path)

        if len(exported_mod.path_to_method_name) == 0:
            get_logger().error(
                "Flumina module did not define any endpoint paths. Ensure you "
                "define at least one path with the @path decorator on a method"
            )
            sys.exit(-1)

    print(
        f"Flumina repo validation successful! Now you can upload the model to Fireworks "
        f"with a command like `firectl create model my-model-name {file_path}`"
    )


def flumina_init(args):
    if os.listdir() and not args.allow_non_empty:
        get_logger().error(
            "Tried to initialize Flumina repository in a non-empty directory. "
            "Pass --allow-non-empty to bypass this check"
        )
        sys.exit(-1)

    # Access the file named 'example.txt' inside 'flumina.assets'
    with importlib.resources.open_text(
        "fireworks.flumina.assets", "flumina_py_template.txt"
    ) as f:
        flumina_py_template = f.read()

    cwd = os.getcwd()
    with open(os.path.join(cwd, "flumina.py"), "w") as f:
        f.write(flumina_py_template)

    fireworks_json = {"_is_flumina_model": True}
    with open(os.path.join(cwd, "fireworks.json"), "w") as f:
        json.dump(fireworks_json, f)

    os.mkdir(os.path.join(cwd, "data"))


def _copy_directory_contents(src_dir, dest_dir):
    # Ensure the destination directory exists
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Loop through all files and directories in the source directory
    for item in os.listdir(src_dir):
        src_item = os.path.join(src_dir, item)
        dest_item = os.path.join(dest_dir, item)

        # If it's a directory, recursively copy it
        if os.path.isdir(src_item):
            shutil.copytree(src_item, dest_item, dirs_exist_ok=True)
        # If it's a file, copy it to the destination
        else:
            shutil.copy2(src_item, dest_item)


def flumina_init_from_hf(args):
    # Delegate to flumina_init to set up initial structure
    flumina_init(args)

    # Download specified model from HF hub
    try:
        from huggingface_hub import snapshot_download
    except ImportError as e:
        get_logger().exception("")
        get_logger().error(
            f"Failed to import huggingface_hub. Ensure you have it "
            f"installed, e.g. via pip install huggingface_hub"
        )

    snapshot_download_path = snapshot_download(repo_id=args.model_repo)

    cwd = os.getcwd()
    # Copy contents of snapshot_download_path into /data
    dest_data_dir = os.path.join(cwd, "data")
    _copy_directory_contents(src_dir=snapshot_download_path, dest_dir=dest_data_dir)

    # Best effort to try to detect the correct model class
    model_repo, model_classname = None, None

    model_index_json_path = os.path.join(dest_data_dir, "model_index.json")
    if os.path.exists(model_index_json_path):
        with open(model_index_json_path, "r") as f:
            loaded_model_index = json.load(f)

        if (
            loaded_model_index.get("_diffusers_version", None) is not None
            and loaded_model_index.get("_class_name", None) is not None
        ):
            model_repo = "diffusers"
            model_classname = loaded_model_index["_class_name"]

    # Overwrite flumina.py to contain the HF template
    with importlib.resources.open_text(
        "fireworks.flumina.assets", "flumina_hf_template.txt"
    ) as f:
        flumina_py_template = f.read()

    assert (model_repo is not None) == (model_classname is not None)
    if model_repo is not None:
        flumina_py_template = flumina_py_template.format(
            model_class_import_str=f"from {model_repo} import {model_classname}",
            model_classname_str=model_classname,
        )
    else:
        flumina_py_template = flumina_py_template.format(
            model_class_import_str="",
            model_classname_str="ModelClassname",
        )

    cwd = os.getcwd()
    with open(os.path.join(cwd, "flumina.py"), "w") as f:
        f.write(flumina_py_template)


def flumina_init_addon(args):
    if os.listdir() and not args.allow_non_empty:
        get_logger().error(
            "Tried to initialize Flumina repository in a non-empty directory. "
            "Pass --allow-non-empty to bypass this check"
        )
        sys.exit(-1)

    fireworks_json = {
        "_is_flumina_model": True,
        "_flumina_addon_type": args.addon_type,
    }
    with open("fireworks.json", "w") as f:
        json.dump(fireworks_json, f)


def main():
    # Create the top-level parser
    parser = argparse.ArgumentParser(description="Flumina CLI Tool")
    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        help="The Flumina command to run",
    )

    parser_run = subparsers.add_parser(
        "init", help="Initialize an empty Flumina repository in the current directory"
    )
    parser_run.add_argument(
        "--allow-non-empty",
        action="store_true",
        help="Allow initialization of a Flumina repository in a non-empty folder",
    )
    parser_run.set_defaults(func=flumina_init)

    parser_run = subparsers.add_parser(
        "init_from_hf",
        help="Initialize a Flumina repository from the specified HF repo "
        "in the current directory",
    )
    parser_run.add_argument(
        "model_repo",
        type=str,
        help="The Hugging Face repository name to initialize from",
    )
    parser_run.add_argument(
        "--allow-non-empty",
        action="store_true",
        help="Allow initialization of a Flumina repository in a non-empty folder",
    )
    parser_run.set_defaults(func=flumina_init_from_hf)

    parser_run = subparsers.add_parser(
        "validate", help="Validate the Flumina repo in the current directory"
    )
    parser_run.set_defaults(func=validate_command)

    parser_run = subparsers.add_parser(
        "init_addon", help="Initialize a Flumina addon repo in the current repository"
    )
    parser_run.add_argument(
        "addon_type",
        type=str,
        help="The addon type to initialize. The possible addon types and their schemas are defined by each base model.",
    )
    parser_run.add_argument(
        "--allow-non-empty",
        action="store_true",
        help="Allow initialization of a Flumina repository in a non-empty folder",
    )
    parser_run.set_defaults(func=flumina_init_addon)

    # Parse the arguments
    args = parser.parse_args()

    # Dispatch to the appropriate function based on the command
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
