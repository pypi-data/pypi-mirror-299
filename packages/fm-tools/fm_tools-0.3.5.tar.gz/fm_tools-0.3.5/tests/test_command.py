# This file is part of fm-actor, a library for interacting with fm-data files:
# https://gitlab.com/sosy-lab/software/fm-actor
#
# SPDX-FileCopyrightText: 2024 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: MIT

import shutil
import sys
from pathlib import Path

import yaml

from fm_tools.fmdata import FmData

YAML_REMOTE = """
name: Goblint
input_languages:
  - C
project_url: https://goblint.in.tum.de/
repository_url: https://github.com/goblint/analyzer
spdx_license_identifier: MIT
benchexec_toolinfo_module: "https://gitlab.com/sosy-lab/software/benchexec/-/raw/main/benchexec/tools/goblint.py"
fmtools_format_version: "2.0"
fmtools_entry_maintainers:
  - sim642

maintainers:
  - name: Simmo Saan
    institution: University of Tartu
    country: Estonia
    url: https://sim642.eu/
  - name: Michael Schwarz
    institution: Technische Universität München
    country: Germany
    url: https://www.cs.cit.tum.de/en/pl/personen/michael-schwarz/

versions:
  - version: "svcomp24"
    doi: 10.5281/zenodo.10202867
    benchexec_toolinfo_options: ["--conf", "conf/svcomp24.json"]
    required_ubuntu_packages: []

"""


def setup_module():
    config = yaml.safe_load(YAML_REMOTE)
    fm_data = FmData(config, "svcomp24")
    target = Path(__file__).parent / "output" / "goblint-svcomp24"
    fm_data.download_and_install_into(target)


def teardown_module():
    target = Path(__file__).parent / "output"
    if target.exists():
        shutil.rmtree(target)


def test_command():
    config = yaml.safe_load(YAML_REMOTE)
    config["benchexec_toolinfo_module"] = "goblint"
    fm_data = FmData(config, "svcomp24")

    command = fm_data.command_line(
        Path(__file__).parent / "output" / "goblint-svcomp24",
        input_files=[Path("example.c")],
        property=Path("example.prp"),
    )
    print(command)


def test_command_with_remote_tool_info_module():
    config = yaml.safe_load(YAML_REMOTE)
    fm_data = FmData(config, "svcomp24")
    ti = fm_data.get_toolinfo_module().resolve()
    ti.resolved = ".goblunt"
    ti._target_location = ti._target_location.rename(ti._target_location.with_stem("goblunt"))
    ti.make_available()

    print(ti)
    print(ti._target_location)
    print(sys.path)
    command = fm_data.command_line(
        Path(__file__).parent / "output" / "goblint-svcomp24",
        input_files=[Path("example.c")],
        property=Path("example.prp"),
    )
    print(command)


if __name__ == "__main__":
    test_command_with_remote_tool_info_module()
