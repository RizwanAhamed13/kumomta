"""Static fixtures only; no candidate or Docker execution."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import docker_contract

BASE = "FROM public.ecr.aws/d3j8x8q7/olympus-base-rust:latest\n"
VALID = BASE + 'WORKDIR /app\nRUN cargo fetch --locked && cargo build --tests --offline\nCMD ["/bin/bash"]\n'

class DockerContractTests(unittest.TestCase):
    def good(self, source):
        self.assertEqual(docker_contract.check(source)["status"], "STATIC_DOCKER_CHECKS_PASS")
    def bad(self, source):
        self.assertEqual(docker_contract.check(source)["status"], "FAIL")
    def test_compile_tests_without_test_command(self):
        self.good(VALID)
    def test_historical_no_run_is_still_test_command(self):
        self.bad(VALID.replace("cargo build --tests --offline", "cargo test --no-run"))
    def test_wrong_workdir_or_default_cmd(self):
        for old, new in [("/app", "/workspace"), ('["/bin/bash"]', '["bash"]')]:
            with self.subTest(new=new):
                self.bad(VALID.replace(old, new))
    def test_missing_fields(self):
        for source in ["", BASE, BASE + "WORKDIR /app\n"]:
            with self.subTest(source=source):
                self.bad(source)
    def test_digest_floating_variables_and_wrong_registry(self):
        for image in ["rust:latest", "public.ecr.aws/d3j8x8q7/olympus-base-rust:v1", "public.ecr.aws/d3j8x8q7/olympus-base-rust:latest@sha256:abcd", "$BASE"]:
            with self.subTest(image=image):
                self.bad(VALID.replace(BASE, "FROM " + image + "\n"))
    def test_multiline_visible_test_command(self):
        self.bad(VALID.replace("RUN cargo fetch --locked && cargo build --tests --offline",
                               "RUN cargo fetch --locked && \\\n cargo test --no-run"))
    def test_exec_form_test_command(self):
        self.bad(VALID.replace("RUN cargo fetch --locked && cargo build --tests --offline",
                               'RUN ["cargo", "test", "--no-run"]'))
    def test_language_test_commands(self):
        for command in ["pytest -q", "python3 -m unittest", "go test ./...", "ctest", "npm run test", "dotnet test", "bash test.sh new"]:
            with self.subTest(command=command):
                self.bad(VALID.replace("cargo fetch --locked && cargo build --tests --offline", command))
    def test_shell_file_test_is_not_test_suite(self):
        self.good(VALID.replace("cargo fetch --locked && cargo build --tests --offline", "test -f Cargo.lock && cargo build --tests"))
    def test_last_stage_must_match(self):
        self.bad(VALID + "FROM public.ecr.aws/d3j8x8q7/olympus-base-rust:latest\n")
        self.good(VALID.replace(BASE, BASE.rstrip() + " AS compiled\n") + "FROM compiled\n")
    def test_comments_and_shell_bash(self):
        self.good("# RUN cargo test\n" + VALID.replace('["/bin/bash"]', "/bin/bash"))
    def test_unsupported_heredoc_is_not_static_pass(self):
        self.bad(VALID.replace("RUN cargo fetch --locked && cargo build --tests --offline", "RUN <<EOF\ncargo build\nEOF"))

if __name__ == "__main__":
    unittest.main()
