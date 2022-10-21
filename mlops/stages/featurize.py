import argparse


def extract_features(data, output_file):
    with open(output_file, "w") as f:
        f.write("Feature vector!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", help="Path to transformed data", type=str)
    parser.add_argument(
        "--output_file", help="Path to save extracted features", type=str
    )
    args = parser.parse_args()

    extract_features(args.data, args.output_file)
