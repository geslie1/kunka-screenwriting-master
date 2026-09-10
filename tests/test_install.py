import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("installer", Path(__file__).resolve().parents[1] / "scripts/install.py")
installer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.source = self.base / "source"
        self.dest = self.base / "profile" / "skills"
        for name in ("kunka-a", "kunka-b"):
            folder = self.source / name
            folder.mkdir(parents=True)
            (folder / "SKILL.md").write_text(f'---\nname: {name}\ndescription: "Test skill"\n---\nBody\n')

    def test_dry_run_does_not_create_destination(self):
        report = installer.install(self.source, self.dest, dry_run=True)
        self.assertEqual(set(report["actions"].values()), {"install"})
        self.assertFalse(self.dest.exists())

    def test_install_is_repeatable_and_keeps_unrelated_files(self):
        installer.install(self.source, self.dest)
        unrelated = self.dest / "unrelated.txt"
        unrelated.write_text("keep")
        report = installer.install(self.source, self.dest)
        self.assertEqual(set(report["actions"].values()), {"unchanged"})
        self.assertEqual(unrelated.read_text(), "keep")
        self.assertEqual(installer.inventory(self.source / "kunka-a"), installer.inventory(self.dest / "kunka-a"))

    def test_conflict_is_detected_before_installing_other_skills(self):
        target = self.dest / "kunka-b"
        target.mkdir(parents=True)
        (target / "SKILL.md").write_text("user changes")
        with self.assertRaises(ValueError):
            installer.install(self.source, self.dest)
        self.assertFalse((self.dest / "kunka-a").exists())
        self.assertEqual((target / "SKILL.md").read_text(), "user changes")

    def test_update_retains_original_in_backup(self):
        installer.install(self.source, self.dest)
        original = self.dest / "kunka-a/SKILL.md"
        original.write_text("custom text")
        report = installer.install(self.source, self.dest, update=True)
        backup = Path(report["backup"])
        self.assertEqual((backup / "kunka-a/SKILL.md").read_text(), "custom text")
        self.assertNotIn(self.dest, backup.parents)
        self.assertEqual(original.read_text(), (self.source / "kunka-a/SKILL.md").read_text())

    def test_failed_update_restores_all_moved_originals(self):
        installer.install(self.source, self.dest)
        for name in ("kunka-a", "kunka-b"):
            (self.dest / name / "SKILL.md").write_text("custom " + name)
        real_rename = Path.rename

        def failing_rename(path, target):
            if path.parent.name.startswith(".kunka-stage-") and path.name == "kunka-b":
                raise OSError("simulated disk failure")
            return real_rename(path, target)

        with patch.object(Path, "rename", failing_rename):
            with self.assertRaises(OSError):
                installer.install(self.source, self.dest, update=True)
        for name in ("kunka-a", "kunka-b"):
            self.assertEqual((self.dest / name / "SKILL.md").read_text(), "custom " + name)
        self.assertFalse((self.dest / ".kunka-install.lock").exists())

    def test_source_and_target_symlinks_are_rejected(self):
        outside = self.base / "outside"
        outside.write_text("keep private")
        link = self.source / "kunka-a/reference.md"
        link.symlink_to(outside)
        with self.assertRaises(ValueError):
            installer.install(self.source, self.dest)
        link.unlink()
        self.dest.mkdir(parents=True)
        (self.dest / "kunka-a").symlink_to(self.source / "kunka-a", target_is_directory=True)
        with self.assertRaises(ValueError):
            installer.install(self.source, self.dest, update=True)
        self.assertEqual(outside.read_text(), "keep private")

    def test_selection_and_path_traversal(self):
        installer.install(self.source, self.dest, names=["kunka-a"])
        self.assertFalse((self.dest / "kunka-b").exists())
        with self.assertRaises(ValueError):
            installer.install(self.source, self.dest, names=["../outside"])

    def test_lock_prevents_concurrent_install(self):
        self.dest.mkdir(parents=True)
        lock = self.dest / ".kunka-install.lock"
        lock.write_text("other process")
        with self.assertRaises(ValueError):
            installer.install(self.source, self.dest)
        self.assertEqual(lock.read_text(), "other process")
        self.assertFalse((self.dest / "kunka-a").exists())


if __name__ == "__main__":
    unittest.main()
