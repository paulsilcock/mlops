import argparse


def save_model(output_file, model):
    with open(output_file, "w") as f:
        f.write(model)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--features", help="Path to extracted features", type=str)
    parser.add_argument("--model", help="Path to save trained model", type=str)
    parser.add_argument("--epochs", help="Number of training epochs", type=int)

    args = parser.parse_args()

    save_model(
        args.model, f"Model train using {args.features}, for {args.epochs} iterations"
    )
