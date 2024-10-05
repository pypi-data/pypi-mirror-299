import fire

from dotenv import load_dotenv
load_dotenv()

from cloud_storage_size.rclone import size

def main():
    fire.Fire(size)


if __name__ == "__main__":
    main()
