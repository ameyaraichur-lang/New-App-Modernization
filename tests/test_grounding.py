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


def test_compound_path_tokens_split_on_extension_boundaries():
    from appmod.agents.grounding import path_tokens

    toks = path_tokens({"note": "see auth.py/blog.py and users/articles/doc.go/hello.go"})
    assert toks == ["auth.py", "blog.py", "users/articles/doc.go", "hello.go"]
    assert path_tokens({"note": "Dockerfile/boot.sh"}) == ["Dockerfile", "boot.sh"]
    assert path_tokens({"note": "Gemfile/Gemfile.lock"}) == ["Gemfile", "Gemfile.lock"]


def test_has_path_is_case_insensitive_for_repo_files(tmp_path):
    (tmp_path / "app").mkdir()
    (tmp_path / "app" / "User.php").write_text("class User {}\n")
    idx = RepoIndex(tmp_path)
    assert idx.has_path("app/User.php")
    assert idx.has_path("App/User.php")
