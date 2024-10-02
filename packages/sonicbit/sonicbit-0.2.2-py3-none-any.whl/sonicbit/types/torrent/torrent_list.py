import json
from dataclasses import dataclass
from datetime import datetime
from typing import Dict

from requests import Response
from requests.exceptions import JSONDecodeError

from sonicbit.base import SonicBitBase
from sonicbit.errors import InvalidResponseError, SonicBitError
from sonicbit.types.torrent.torrent import Torrent
from sonicbit.types.torrent.torrent_info import TorrentInfo
from sonicbit.utils import EnhancedJSONEncoder


@dataclass
class TorrentList:
    client: SonicBitBase
    torrents: Dict[str, Torrent]
    info: TorrentInfo
    raw: dict

    @staticmethod
    def from_response(client: SonicBitBase, response: Response) -> "TorrentList":
        try:
            json_data = response.json()
        except JSONDecodeError:
            raise InvalidResponseError(
                f"Server returned invalid JSON data: {response.text}"
            ) from None

        if error_message := json_data.get("message"):
            raise SonicBitError(f"Failed to get torrent list: {error_message}")

        torrents_data = json_data["list"]
        info_data = json_data["info"]

        if torrents_data:
            torrents = {
                key: Torrent(
                    client=client,
                    name=torrent_data["name"],
                    hash=torrent_data["hash"],
                    size=int(torrent_data["sizeBytes"]),
                    progress=int(torrent_data["percentComplete"]),
                    download_rate_value=torrent_data["dlRateValue"],
                    download_rate_unit=torrent_data["dlRateUnit"],
                    upload_rate_value=(
                        torrent_data["upRateValue"]
                        if torrent_data.get("upRateValue", "N/A") != "N/A"
                        else None
                    ),
                    upload_rate_unit=torrent_data.get("uploadRateUnit"),
                    peers_status=torrent_data["peersStatus"],
                    seeds_status=torrent_data["seedsStatus"],
                    date_added=datetime.fromtimestamp(int(torrent_data["t_added"])),
                    is_multi_file=torrent_data["isMultiFile"] == "1",
                    status=torrent_data["status"],
                    is_private=torrent_data["isPrivate"] != "Public",
                    in_cache=torrent_data["in_cache"],
                    deleted=torrent_data.get("deleted", False),
                    deleted_reason=torrent_data.get("deleted_reason"),
                    raw=torrent_data,
                )
                for key, torrent_data in torrents_data.items()
            }
        else:
            torrents = {}

        info = TorrentInfo(
            download_rate=int(info_data["downloadRate"]),
            upload_rate=info_data["uploadRate"],
            size_byte_total=int(info_data["sizeByteTotal"]),
            size_byte_limit=int(info_data["sizeByteLimit"]),
            percent=float(info_data["percent"]),
            max_parallel=int(info_data["max_prallel"]),
            email=info_data["email"],
            ftp=info_data["userftp"],
            plan_name=info_data["package"],
            seedbox_status_up=info_data["seedbox_status_up"],
            hash_list=info_data["hash_list"],
            raw=info_data,
        )

        return TorrentList(client=client, torrents=torrents, info=info, raw=json_data)

    def __str__(self) -> str:
        return json.dumps(self, indent=4, cls=EnhancedJSONEncoder)
