import argparse
import os

# ----- Argparse ------
parser = argparse.ArgumentParser(description="Edit and add Spotify's metadata to each file (.mp3/.wav).")
spotify_playlist = parser.add_argument(
        "-p",
        "--playlist",
        help="Link to your Spotify playlist of interest.")
local_directory = parser.add_argument(
        "-l",
        "--local",
        help="Path to your local music directory.")
library_name = parser.add_argument(
        "-n",
        "--name",
        help="Library name that is associated with your music.")
curate_genres = parser.add_argument(
        "-g",
        "--genres",
        help="Lets you manually curate genres. Otherwise a list of genres associated with the (first) artist will be "
             "provided",
        action=argparse.BooleanOptionalAction)
args = parser.parse_args()

# ------ Handling Exceptions ------
if args.playlist is None:
    raise argparse.ArgumentError(spotify_playlist,
                                 "\n\n> Please use the '-p' or '--playlist' flag. "
                                 "A Spotify playlist link needs to be provided. \n\n" +
                                 parser.format_help())

if args.local is None:
    raise argparse.ArgumentError(local_directory,
                                 "\n\n> Please use the '-l' or '--local' flag. "
                                 "Path to your local music directory needs to be provided. \n\n" +
                                 parser.format_help())


if not os.path.isdir(args.local):
    raise NameError("Path to your local music directory does not exist.")

if len(os.listdir(args.local)) == 0:
    raise FileNotFoundError("There are no files in your local music directory.")

if args.name is None:
    raise argparse.ArgumentError(library_name,
                                 "\n\n> Please use the '-n' or '--name' flag. "
                                 "Give your music library a name. \n\n" +
                                 parser.format_help())
