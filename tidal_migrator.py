import tidalapi
from pathlib import Path
import csv
from typing import List, Set

class TidalMigrator:
    """A class to handle Tidal login and favorites management."""

    def __init__(self) -> None:
        self.session = tidalapi.Session()
        self.obj_main, _ = self.session.login_oauth()
        self.url_main = self.obj_main.verification_uri_complete

    def check_login(self) -> bool:
        """Check if the user has logged in to Tidal."""
        return self.session.check_login()

    def save_favorites_to_csv(self, favorites: List, filepath: Path) -> None:
        """Save new favorites to a CSV file, avoiding duplicates."""
        existing_favorites = self._load_existing_favorites(filepath)
        self._write_new_favorites(favorites, existing_favorites, filepath)

    def _load_existing_favorites(self, filepath: Path) -> Set[str]:
        """Load existing favorites from a CSV file into a set."""
        if not filepath.exists():
            return set()

        with filepath.open("r", newline="") as csvfile:
            reader = csv.reader(csvfile)
            return {row[0] for row in reader}

    def _write_new_favorites(self, favorites: List, existing_favorites: Set[str], filepath: Path) -> None:
        """Write new favorites to CSV file."""
        with filepath.open("a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            for favorite in favorites:
                if str(favorite.id) not in existing_favorites:
                    writer.writerow([favorite.id])

    def save_favorites(self) -> None:
        """Save all favorites categories to their respective CSV files."""
        favorites_dir = Path("tidal-favorites")
        favorites_dir.mkdir(exist_ok=True)
        
        categories = {
            "albums": self.session.user.favorites.albums(),
            "tracks": self.session.user.favorites.tracks(),
            "videos": self.session.user.favorites.videos(),
            "artists": self.session.user.favorites.artists(),
            "playlists": self.session.user.favorites.playlists(),
        }
        
        for category, favorites in categories.items():
            category_path = favorites_dir / f"{category}.csv"
            self.save_favorites_to_csv(favorites, category_path)

    def add_favorites(self, filepaths: List[Path]) -> List[str]:
        """Add favorites from a list of CSV files to Tidal."""
        errors = []
        for filepath in filepaths:
            try:
                favorite_type = self._determine_favorite_type(filepath.name)
                with filepath.open("r", newline="") as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        getattr(self.session.user.favorites, f"add_{favorite_type}")(row[0])
            except Exception as e:
                errors.append(str(e))
        return errors

    def _determine_favorite_type(self, filename: str) -> str:
        """Determine the type of favorite based on the filename."""
        if "albums" in filename:
            return "album"
        elif "tracks" in filename:
            return "track"
        elif "artists" in filename:
            return "artist"
        elif "playlists" in filename:
            return "playlist"
        elif "videos" in filename:
            return "video"
        else:
            raise ValueError(f"Unknown favorite type based on file name: {filename}")
