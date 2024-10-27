"""Prepare the state before starting surface main"""
import sys
import os
import argparse

import dependency_injector.containers
from dependency_injector import providers
import surface_main
from utilities import intext
import container

def get_arguments() -> object:
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=False,
                    help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=False,
                    help="ephemeral port number of the server (1024 to 65535)")
    ap.add_argument("-r", "--rov", type=str, required=False,
                    help="the name of the folder containing the rov configuration files")
    return ap.parse_args()

def prepare_arguments(config: dict[str, object]) -> dict[str, object]:
    args = get_arguments()
    results = {}
    if args.ip is None:
        ip = intext("Please provide the IP address of the Raspberry Pi. " +
                    f'Defaults to "{config["ip"]}"').strip()
        if ip == "":
            pass
        else:
            results["ip"] = ip

    if args.port is None:
        port = intext("Please provide the port you want to use. " +
                      f'Defaults to {config["port"]}').strip()
        if port == "":
            pass
        else:
            port = int(port)
            results["port"] = port

    if args.rov is None:
        rov = intext("Please provide the rov you want to use. " +
                     f'Defaults to {config["rov"]}').strip()
        if rov == "":
            pass
        else:
            results["rov"] = rov

    return results

def create_container() -> dependency_injector.containers.Container:
    """Loads configuration and creates all service objects and factories"""
    rov_container = container.Container()

    path = os.path.join(os.path.dirname(__file__), "config", "network.yaml")
    print(f'Loading {path}')
    rov_container.networkconfig.from_yaml(path)

    #Figure out the configuration so far, and load the command line arguments
    arguments = prepare_arguments(rov_container.networkconfig())
    rov_container.networkconfig.from_dict(arguments)


    rov_container.wire(modules=[__name__])

    return container

def run():
    create_container()

    main_system = surface_main.MainSystem(ip, port, rov_directory)

    while main_system.run:
        try:
            main_system.main_loop()
        except Exception as e:
            # In competition we should log the exception and continue.  In debug we should crash to fix the issue

            print(f'Exception in main_system.main_loop():\n{e}')

if __name__ == "__main__":
    run()