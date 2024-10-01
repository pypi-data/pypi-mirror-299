import argparse
import os

from test_generator.library.errors import ApiGenerationError


def get_scenarios_path(args: argparse.Namespace) -> str:
    current_dir = os.getcwd()
    if not args.scenarios_path:
        raise argparse.ArgumentTypeError('--scenarios-path is required for generating...')
    scenarios_path = os.path.join(current_dir, args.scenarios_path)
    if not os.path.isfile(scenarios_path):
        raise ApiGenerationError(f"{scenarios_path} doesn't exist...")
    return scenarios_path


def get_template_path(args: argparse.Namespace) -> str:
    current_dir = os.getcwd()
    if not args.template_path:
        raise argparse.ArgumentTypeError('--template-path is required for generating...')
    template_path = os.path.join(current_dir, args.template_path)
    if not os.path.isfile(template_path):
        raise ApiGenerationError(f"{template_path} doesn't exist...")
    return template_path


def get_target_dir_path(args: argparse.Namespace) -> str:
    current_dir = os.getcwd()
    if args.target_dir:
        return os.path.join(current_dir, args.target_dir)
    else:
        target_dir_path = os.path.join(current_dir, args.scenarios_path)
        return os.path.dirname(target_dir_path)


def get_yaml_path(args: argparse.Namespace) -> str:
    current_dir = os.getcwd()
    if not args.yaml_path:
        raise argparse.ArgumentTypeError('--yaml-path is required for generating...')
    yaml_path = os.path.join(current_dir, args.yaml_path)
    if not os.path.isfile(yaml_path):
        raise ApiGenerationError(f"{yaml_path} doesn't exist...")
    return yaml_path


def get_interface_path(args: argparse.Namespace) -> str:
    current_dir = os.getcwd()
    if not args.interface_path:
        raise argparse.ArgumentTypeError('--interface-path is required for generating...')
    interface_path = os.path.join(current_dir, args.interface_path)
    if not os.path.isfile(interface_path):
        raise ApiGenerationError(f"{interface_path} doesn't exist...")
    return interface_path


def get_schemas_dir_path(args: argparse.Namespace) -> str:
    current_dir = os.getcwd()
    if not args.schemas_path:
        raise argparse.ArgumentTypeError('--schemas-path is required for generating...')
    schemas_dir_path = os.path.join(current_dir, args.schemas_path)
    if not os.path.isdir(schemas_dir_path):
        raise ApiGenerationError(f"{schemas_dir_path} doesn't exist...")
    return schemas_dir_path
