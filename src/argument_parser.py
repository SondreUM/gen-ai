import argparse

def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", type=str, help="Name of the person", required=True)
    parser.add_argument("-o", "--organization", type=str, help="Organization, or company, the person is affiliated with", required=True)

    return parser