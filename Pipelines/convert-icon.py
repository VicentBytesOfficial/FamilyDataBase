from PIL import Image
import pathlib

BASE_PATH = pathlib.Path(__file__).parent.parent
png_client_path = pathlib.Path.joinpath(BASE_PATH, "Icons/client.png")
png_server_path = pathlib.Path.joinpath(BASE_PATH, "Icons/server.png")
png_console_path = pathlib.Path.joinpath(BASE_PATH, "Icons/console.png")
ico_client_path = pathlib.Path.joinpath(BASE_PATH, "client.ico")
ico_server_path = pathlib.Path.joinpath(BASE_PATH, "server.ico")
ico_console_path = pathlib.Path.joinpath(BASE_PATH, "console.ico")

img = Image.open(png_client_path)
img.save(ico_client_path, format="ICO", sizes=[(16,16),(32,32),(48,48),(64,64),(128,128)])

img = Image.open(png_server_path)
img.save(ico_server_path, format="ICO", sizes=[(16,16),(32,32),(48,48),(64,64),(128,128)])

img = Image.open(png_console_path)
img.save(ico_console_path, format="ICO", sizes=[(16,16),(32,32),(48,48),(64,64),(128,128)])
