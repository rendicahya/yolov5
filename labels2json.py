import json
import pathlib
from tqdm import tqdm
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
    for action in labels_path.iterdir():
        for subdir in action.iterdir():
            data = []

            for txt in subdir.iterdir():
                frame_data = []

                with open(txt, "r") as f:
                    for line in f.readlines():
                        line_casted = list(map(float, line.strip().split()))
                        line_casted[0] = int(line_casted[0])

                        frame_data.append(line_casted)

                data.append({int(txt.stem): frame_data})
            break

        target_file = labels_path.parent / "json" / f"{subdir.name}.json"
        target_file.parent.mkdir(parents=True, exist_ok=True)

        with open(target_file, "w") as f:
            json.dump(data, f)

        break


if __name__ == "__main__":
    main()
