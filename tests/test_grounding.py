from appmod.agents.grounding import RepoIndex, grounded_claims, ungrounded_paths


def test_paths_must_exist_or_be_named_by_the_code(tmp_path):
    (tmp_path / "app").mkdir()
    (tmp_path / "app" / "db.py").write_text('import os\nPATH = os.path.join(instance_path, "flaskr.sqlite")\n')
    idx = RepoIndex(tmp_path)
    findings = [{"statement": "app/db.py opens instance/flaskr.sqlite; config in conf/settings.yml",
                 "evidence_class": "OBSERVED"},
                {"statement": "add deploy/k8s/service.yaml", "evidence_class": "INFERRED"}]
    assert ungrounded_paths(idx, grounded_claims(findings, {}, phase=3)) == ["conf/settings.yml"]
    assert ungrounded_paths(idx, grounded_claims([], {"files": ["app/db.py", "lib/ghost.py"]}, phase=1)) \
        == ["lib/ghost.py"]
