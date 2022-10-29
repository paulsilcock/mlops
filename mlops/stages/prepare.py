import argparse


def load(path_to_data: str):
    return "raw data!"


def transform(data):
    return "transformed data!"


def save(data, output_path: str):
    with open(output_path, "w") as f:
        f.write(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw_data", help="Path to raw data", type=str)
    parser.add_argument("--output_file", help="Path to save transformed data", type=str)
    args = parser.parse_args()

    raw_data = load(args.raw_data)
    transformed_data = transform(raw_data)
    save(transformed_data, args.output_file)
