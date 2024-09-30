import subprocess
import asyncio
import os
import shutil
import platform
from py2docfx import PACKAGE_ROOT
from py2docfx.convert_prepare.package_info import PackageInfo
from py2docfx.convert_prepare.get_source import get_source
from py2docfx.convert_prepare import pip_utils

REQUIREMENT_MODULES = ["setuptools", "sphinx==6.1.3", "pyyaml", "jinja2==3.0.3", "wheel"]
VENV_DIR = "venv"
VENV_BUFFER = 5
VENV_DELETE_BUFFER = 10
PIP_INSTALL_COMMAND = ["-m", "pip", "install", "--upgrade"]

PIP_INSTALL_VENV_COMMON_OPTIONS = [
    "--quiet",
    "--no-warn-conflicts",
    "--disable-pip-version-check",
]

def install_converter_requirements(executable: str):
    """
    Install setuptools/sphinx/pyyaml/jinja2
    Replacing logic of
    https://apidrop.visualstudio.com/Content%20CI/_git/ReferenceAutomation?path=/Python/InstallPackage.ps1&line=15&lineEnd=35&lineStartColumn=1&lineEndColumn=87&lineStyle=plain&_a=contents
    """
    pip_install_cmd = [executable, "-m", "pip", "install", "--upgrade"]

    pip_install_common_options = [
        "--no-cache-dir",
        "--quiet",
        "--no-compile",
        "--no-warn-conflicts",
        "--disable-pip-version-check",
    ]

    for module in REQUIREMENT_MODULES:
        print(f"<CI INFO>: Upgrading {module}...")
        subprocess.run(
            pip_install_cmd + [module] + pip_install_common_options, check=True
        )

def get_venv_path(venv_num: int) -> str:
    return os.path.join(PACKAGE_ROOT, VENV_DIR, "venv"+str(venv_num))

def get_venv_exe(venv_num: int) -> str:
    return os.path.join(get_venv_path(venv_num), "Scripts", "python.exe")

async def install_converter_requirement_async(executable: str):
    pip_cmd = PIP_INSTALL_COMMAND + PIP_INSTALL_VENV_COMMON_OPTIONS + REQUIREMENT_MODULES
    await(await asyncio.create_subprocess_exec(executable, *pip_cmd)).wait()

async def install_required_packages(
        executable: str, required_package_list: list[PackageInfo], github_token: str, ado_token: str):
    for idx, package in enumerate(required_package_list): # TODO: remove idx
        # TODO: create a git clone async function and use it here, check if it already exists
        # if package.install_type == package.InstallType.SOURCE_CODE:
        #     get_source(package, idx, vststoken=ado_token, githubtoken=github_token)
        package_name, options = package.get_install_command()
        pip_cmd = PIP_INSTALL_COMMAND + PIP_INSTALL_VENV_COMMON_OPTIONS + options + [package_name]
        await(await asyncio.create_subprocess_exec(executable, *pip_cmd)).wait()

async def create_environment(venv_num: int):
    await (await asyncio.create_subprocess_exec("python", "-m", "venv", get_venv_path(venv_num))).wait()

async def prepare_venv(venv_num: int, required_package_list: list[PackageInfo], github_token: str, ado_token: str):
    print(f"<CI INFO>: Creating venv{venv_num}...")
    await create_environment(venv_num)
    print(f"<CI INFO>: Installing converter requirements in venv{venv_num}...")
    await install_converter_requirement_async(get_venv_exe(venv_num))
    print(f"<CI INFO>: Installing required packages in venv{venv_num}...")
    await install_required_packages(get_venv_exe(venv_num), required_package_list, github_token, ado_token)
    print(f"<CI INFO>: venv{venv_num} setup complete.")

async def copy_venv(venv_num: int, new_venv_num: int):
    print(f"<CI INFO>: Copying venv{venv_num} to venv{new_venv_num}...")
    venv_path = get_venv_path(venv_num)
    new_venv_path = get_venv_path(new_venv_num)
    if os.path.exists(venv_path):
        if os.name == 'nt':
            command = f'xcopy /E /I "{venv_path}" "{new_venv_path}"'
        else:
            command = f'cp -r "{venv_path}" "{new_venv_path}"'
        
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if process.returncode == 0:
            print(f"<CI INFO>: venv{venv_num} copied to venv{new_venv_num}.")
        else:
            print(f"<CI ERROR>: Failed to copy venv{venv_num} to venv{new_venv_num}. Error: {stderr.decode()}")

async def remove_environment(venv_num: int):
    venv_path = get_venv_path(venv_num)
    if os.path.exists(venv_path):
        print(f"<CI INFO>: Removing venv{venv_num}...")
        # Create a subprocess to run the shell command for removing the directory
        process = await asyncio.create_subprocess_shell(
            f'rm -rf {venv_path}' if os.name != 'nt' else f'rmdir /S /Q {venv_path}',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if process.returncode == 0:
            print(f"<CI INFO>: venv{venv_num} removed.")
        else:
            print(f"<CI ERROR>: Failed to remove venv{venv_num}. Error: {stderr.decode()}")
