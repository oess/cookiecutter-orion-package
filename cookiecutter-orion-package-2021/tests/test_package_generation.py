import os
import json
from subprocess import check_call


def test_package_creation(cookies):
    project_name = "My test_Project"
    results = cookies.bake(
        extra_context={
            "project_name": project_name,
            "version": "1.0.0",
            "full_name": "Full Name",
            "email": "noreply@eyesopen.com",
        }
    )

    assert results.exit_code == 0, "Failed to generate package"
    assert results.project.basename == project_name.lower().replace(" ", "-").replace("_", "-")
    manifest_path = results.project / "manifest.json"
    assert manifest_path.isfile()
    with open(str(manifest_path), "r") as ifs:
        data = json.load(ifs)
    assert isinstance(data, dict)
    assert data["version"] == "1.0.0"
    assert data["name"] == project_name
    # Verify that there are no style errors out of the box
    check_call(["flake8", str(results.project), "--max-line-length=120"]) 


def test_environment_yaml_creation(cookies):
    project_name = "My_test_Project"
    results = cookies.bake(
        extra_context={
            "project_name": project_name,
            "version": "1.0.0",
            "full_name": "Full Name",
            "email": "noreply@eyesopen.com",
        }
    )

    assert results.exit_code == 0, "Failed to generate package"
    path = results.project
    manifest_path = os.path.join(path, "manifest.json")
    assert os.path.isfile(manifest_path)
    check_call(["inv", "build-environment-yaml"], cwd=path)
    env_path = os.path.join(path, "environment.yml")
    assert os.path.isfile(env_path)
    os.remove(env_path)
    with open(manifest_path, "r") as ifs:
        data = json.load(ifs)
    data["conda_channels"] = ["conda-forge"]
    with open(manifest_path, "w") as ofs:
        json.dump(data, ofs, sort_keys=True, indent=2)
    check_call(["inv", "build-environment-yaml"], cwd=path)
    env_path = os.path.join(path, "environment.yml")
    assert os.path.isfile(env_path)
