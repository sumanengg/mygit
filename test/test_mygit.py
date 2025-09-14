"""Test suite for mygit implementation."""

import os
import shutil
import tempfile
import unittest

from mygit import data, base


class TestMyGit(unittest.TestCase):
    """Test cases for mygit core functionality."""

    def setUp(self):
        """Set up a temporary directory for each test."""
        self.test_dir = tempfile.mkdtemp()
        self.old_dir = os.getcwd()
        os.chdir(self.test_dir)
        data.init()

    def tearDown(self):
        """Clean up temporary files after each test."""
        os.chdir(self.old_dir)
        shutil.rmtree(self.test_dir)

    def test_init(self):
        """Test repository initialization."""
        self.assertTrue(os.path.isdir(".mygit"))
        self.assertTrue(os.path.isdir(".mygit/objects"))

    def test_hash_object(self):
        """Test object hashing functionality."""
        # Create a test file
        with open("test.txt", "w") as f:
            f.write("test content")

        # Hash the file content
        with open("test.txt", "rb") as f:
            oid = data.hash_object(f.read())

        # Verify the object exists and content matches
        self.assertTrue(os.path.exists(f".mygit/objects/{oid}"))
        self.assertEqual(
            data.get_object(oid).decode(),
            "test content"
        )

    def test_write_tree(self):
        """Test writing directory tree."""
        # Create some test files
        os.mkdir("sub")
        with open("file1.txt", "w") as f:
            f.write("file1 content")
        with open("sub/file2.txt", "w") as f:
            f.write("file2 content")

        # Write the tree
        tree_oid = base.write_tree()

        # Verify tree was created
        self.assertTrue(os.path.exists(f".mygit/objects/{tree_oid}"))
        tree_content = data.get_object(tree_oid).decode().splitlines()
        
        # Tree should contain both entries
        self.assertEqual(len(tree_content), 2)
        self.assertTrue(any("file1.txt" in line for line in tree_content))
        self.assertTrue(any("sub" in line for line in tree_content))

    def test_commit(self):
        """Test commit creation."""
        # Create and add a test file
        with open("test.txt", "w") as f:
            f.write("test content")

        # Create commit
        commit_oid = base.commit("Initial commit")

        # Verify commit exists
        self.assertTrue(os.path.exists(f".mygit/objects/{commit_oid}"))

        # Check commit content
        commit_data = data.get_object(commit_oid).decode()
        self.assertIn("tree", commit_data)
        self.assertIn("Initial commit", commit_data)


if __name__ == "__main__":
    unittest.main()