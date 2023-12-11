import hydra

from src.conf import InferenceConfig


@hydra.main(config_path="conf", config_name="inference", version_base="1.2")
def main(cfg: InferenceConfig):
    print("something happens here")


if __name__ == "__main__":
    main()
