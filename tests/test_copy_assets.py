from email.utils import unquote
import os
import pytest
import shutil
import tempfile
from urllib.parse import quote

from moffee.utils.file_helper import (
    copy_assets,
)
from moffee.utils import file_helper


@pytest.fixture
def setup_test_environment():
    temp_dir = tempfile.mkdtemp()

    sample_image_path = os.path.join(temp_dir, "sample.png")
    sample_pdf_path = os.path.join(temp_dir, "document.pdf")

    with open(sample_image_path, "w") as f:
        f.write("This is a test image file.")

    with open(sample_pdf_path, "w") as f:
        f.write("This is a test PDF file.")

    yield temp_dir, sample_image_path, sample_pdf_path

    shutil.rmtree(temp_dir)


@pytest.fixture
def setup_file_with_spaces():
    temp_dir = tempfile.mkdtemp()

    # Create a sample file with a space in its name
    sample_file_name = "sample file with spaces.txt"
    sample_file_path = os.path.join(temp_dir, sample_file_name)
    with open(sample_file_path, "w") as f:
        f.write("This is a sample file with spaces in its name")

    yield temp_dir, sample_file_path, sample_file_name

    shutil.rmtree(temp_dir)


def test_copy_assets_updates_links(setup_test_environment):
    temp_dir, sample_image_path, sample_pdf_path = setup_test_environment
    target_dir = os.path.join(temp_dir, "asset_resources")

    html_doc = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Test Document</title>
        <link rel="stylesheet" href="{sample_pdf_path}">
    </head>
    <body>
        <h1>Test HTML Document</h1>
        <img src="{sample_image_path}" alt="Sample Image">
        <a href="{sample_pdf_path}">Download PDF</a>
    </body>
    </html>
    """

    updated_doc = copy_assets(html_doc, target_dir)

    # Check that the target directory is created
    assert os.path.exists(target_dir)

    # Verify that files have been moved and renamed
    moved_files = os.listdir(target_dir)
    assert len(moved_files) == 2

    # Check if document URLs are updated with new file names
    for moved_file in moved_files:
        assert os.path.join(target_dir, moved_file) in updated_doc


def test_copy_assets_ignores_nonexistent_files():
    temp_dir = tempfile.mkdtemp()
    target_dir = os.path.join(temp_dir, "asset_resources")

    html_doc = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Test Document</title>
        <link rel="stylesheet" href="css/nonexistent.css">
    </head>
    <body>
        <h1>Test HTML Document</h1>
        <img src="images/nonexistent.png" alt="Nonexistent Image">
        <a href="files/nonexistent.pdf">Download Nonexistent PDF</a>
    </body>
    </html>
    """

    updated_doc = copy_assets(html_doc, target_dir)

    # Verify that document URLs remain unchanged
    assert "css/nonexistent.css" in updated_doc
    assert "images/nonexistent.png" in updated_doc
    assert "files/nonexistent.pdf" in updated_doc

    shutil.rmtree(temp_dir)


def test_copy_assets_creates_target_directory():
    temp_dir = tempfile.mkdtemp()
    target_dir = os.path.join(temp_dir, "asset_resources")

    html_doc = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Test Document</title>
    </head>
    <body>
        <h1>Test HTML Document</h1>
        <img src="images/sample.png" alt="Sample Image">
    </body>
    </html>
    """

    # Assuming the image does not exist, but we're checking the creation
    updated_doc = copy_assets(html_doc, target_dir)

    # Check that the target directory is created even if it's empty
    assert os.path.exists(target_dir)

    shutil.rmtree(temp_dir)


def test_copy_assets_ignores_urls_in_text_content():
    temp_dir = tempfile.mkdtemp()
    target_dir = os.path.join(temp_dir, "asset_resources")

    # Create a sample file that exists
    sample_file_path = os.path.join(temp_dir, "sample.txt")
    with open(sample_file_path, "w") as f:
        f.write("This is a sample file")

    html_doc = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Test Document</title>
    </head>
    <body>
        <h1>Test HTML Document</h1>
        <img src="{sample_file_path}" alt="Sample Image">
        <p>This is a paragraph mentioning the file path: {sample_file_path}</p>
        <a href="{sample_file_path}">Download Sample</a>
        <p>Another mention of the file: {sample_file_path}</p>
    </body>
    </html>
    """

    updated_doc = copy_assets(html_doc, target_dir)

    # Check that the target directory is created
    assert os.path.exists(target_dir)

    # Verify that only one file has been moved (the one in the img src)
    moved_files = os.listdir(target_dir)
    assert len(moved_files) == 1

    # Check if document URLs in attributes are updated with new file names
    assert os.path.join(target_dir, moved_files[0]) in updated_doc

    # Check that the file path mentioned in the paragraph text is not changed
    assert sample_file_path in updated_doc

    # Count occurrences of the original file path in the updated document
    # It should appear twice in the text content, and once in the <a> tag
    assert updated_doc.count(sample_file_path) == 2

    shutil.rmtree(temp_dir)


def test_copy_assets_handles_encoded_urls(setup_file_with_spaces):
    temp_dir, sample_file_path, sample_file_name = setup_file_with_spaces
    target_dir = os.path.join(temp_dir, "asset_resources")

    # Encode the file path
    encoded_file_path = quote(sample_file_path)

    html_doc = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Test Document</title>
    </head>
    <body>
        <h1>Test HTML Document</h1>
        <img src="{encoded_file_path}" alt="Sample Image">
        <a href="{unquote(encoded_file_path)}">Download Sample</a>
    </body>
    </html>
    """

    updated_doc = copy_assets(html_doc, target_dir)

    # Check that the target directory is created
    assert os.path.exists(target_dir)

    # Verify that the file has been moved
    moved_files = os.listdir(target_dir)
    assert len(moved_files) == 1

    # Check if document URLs are updated with new file names
    assert quote(os.path.join(target_dir, moved_files[0])) in updated_doc

    # Verify that the encoded URL is no longer in the updated document
    assert encoded_file_path not in updated_doc

    # Verify that the original file name (with spaces) is not in the updated document
    assert sample_file_name not in updated_doc


def test_copy_assets_handles_windows_absolute_paths(monkeypatch, tmp_path):
    windows_path = r"D:\AAAwork\科研\notes\assets\example.png"
    target_dir = tmp_path / "assets"
    copied_paths = []

    monkeypatch.setattr(
        file_helper.os.path,
        "isfile",
        lambda path: path == windows_path,
    )
    monkeypatch.setattr(
        file_helper.shutil,
        "copy2",
        lambda source, target: copied_paths.append((source, target)),
    )

    updated_doc = copy_assets(
        f'<img src="{windows_path}">',
        str(target_dir),
        url_prefix="assets",
    )

    assert len(copied_paths) == 1
    assert copied_paths[0][0] == windows_path
    assert 'src="assets/' in updated_doc
    assert updated_doc.endswith('_example.png"/>')
    assert "D:" not in updated_doc
