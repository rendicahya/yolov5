'''
This script moves the files into their respective directories. For example, these files:

- v_PlayingGuitar_g01_c01_1.txt
- v_PlayingGuitar_g01_c01_2.txt
- v_PlayingGuitar_g01_c01_3.txt
- v_PlayingGuitar_g01_c01_4.txt
- v_PlayingGuitar_g01_c01_5.txt

will be moved into:

- v_PlayingGuitar_g01_c01/1.txt
- v_PlayingGuitar_g01_c01/2.txt
- v_PlayingGuitar_g01_c01/3.txt
- v_PlayingGuitar_g01_c01/4.txt
- v_PlayingGuitar_g01_c01/5.txt
'''
import pathlib

import click


@click.command()
@click.argument(
    "labels-path",
    nargs=1,
    required=True,
    type=click.Path(
        file_okay=False,
        dir_okay=True,
        exists=True,
        readable=True,
        path_type=pathlib.Path,
    ),
)
def main(labels_path):
    for file in labels_path.iterdir():
        action = file.name.split("_")[1]
        dir_name = "_".join(file.name.split("_")[:4])

        (labels_path / action / dir_name).mkdir(parents=True, exist_ok=True)

        if file.name.startswith(dir_name):
            dst_filename = file.name.split("_")[4]
            file.rename(labels_path / action / dir_name / dst_filename)


if __name__ == "__main__":
    main()
