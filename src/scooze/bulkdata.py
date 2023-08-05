import os

import requests
import scooze.enums as enums
import scooze.utils as utils

SCRYFALL_BULK_INFO_ENDPOINT = "https://api.scryfall.com/bulk-data"


def download_bulk_data_file(
    uri: str,
    save_to_file: bool = True,
    file_path: str | None = None,
    save_to_db: bool = False,
) -> None:
    if not save_to_file and not save_to_db:
        # TODO: log error, nothing to do
        return
    if save_to_file:
        # TODO: get default file name if None
        with requests.get(uri, stream=True) as r:
            r.raise_for_status()
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=None):
                    f.write(chunk)


def download_all_bulk_data_files(
    save_to_file: bool = True,
    save_to_db: bool = False,
) -> None:
    if not save_to_file and not save_to_db:
        # TODO: log error; nothing to do
        return

    bulk_metadata = requests.get(SCRYFALL_BULK_INFO_ENDPOINT).json()["data"]
    bulk_files = {t["type"]: t["download_uri"] for t in bulk_metadata}

    # for bulk_type in enums.ScryfallBulkFile.list():
    for bulk_type in [
        "all_cards",
    ]:
        # TODO: check vs existing file, don't overwrite
        if save_to_file:
            bulk_filename = bulk_files[bulk_type]
            local_filename = f"{utils.DEFAULT_BULK_FILE_DIR}/{bulk_type}.json"
            print(f"downloading and writing {bulk_type} file...")
            download_bulk_data_file(
                uri=bulk_filename,
                save_to_file=save_to_file,
                file_path=local_filename,
                save_to_db=save_to_db,
            )


if __name__ == "__main__":
    download_all_bulk_data_files()
