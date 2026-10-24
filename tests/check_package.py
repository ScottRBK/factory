"""Check built wheel RECORD entries against the Python packaging standard; no installation."""
import argparse
import base64
import csv
import hashlib
import io
from pathlib import Path
from zipfile import ZipFile


def check_wheel(path: Path) -> None:
    # Arrange: inspect the actual build artifact without importing or extracting its contents.
    with ZipFile(path) as archive:
        names = archive.namelist()
        assert len(names) == len(set(names)), 'Duplicate wheel members'
        files = {item.filename: archive.read(item)
                 for item in archive.infolist() if not item.is_dir()}
    records = [name for name in files if name.endswith('.dist-info/RECORD')]
    assert len(records) == 1, 'Expected exactly one wheel RECORD'
    record = records[0]
    # Act: read the public CSV manifest, not a build-backend implementation detail.
    rows = list(csv.reader(io.StringIO(files[record].decode('utf-8'))))
    assert all(len(row) == 3 for row in rows), 'Malformed wheel RECORD row'
    listed = [row[0] for row in rows]
    # Assert: every member has one entry; digests use SHA-256 and URL-safe Base64 without padding.
    assert len(listed) == len(set(listed)), 'Duplicate wheel RECORD entries'
    assert set(listed) == set(files), 'Wheel RECORD membership differs from archive'
    for name, digest, size in rows:
        if name == record:
            assert digest == size == '', 'Wheel RECORD must not hash itself'
            continue
        expected = base64.urlsafe_b64encode(hashlib.sha256(files[name]).digest()).decode()
        assert digest == 'sha256=' + expected.rstrip('='), f'Invalid wheel checksum: {name}'
        assert size == str(len(files[name])), f'Invalid wheel size: {name}'
    print(f'{path.name}: {len(files) - 1} wheel checksums verified')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('wheel', type=Path, nargs='+')
    for wheel in parser.parse_args().wheel:
        check_wheel(wheel)
