import surface_main


# Set to True to enable debug mode, which will crash the program on exceptions.
debug: bool = True


def run():

    main_system = surface_main.MainSystem()

    while main_system.run:
        # If debug is enabled, we want to hit exceptions so that we can see them.
        if debug:
            try:
                main_system.main_loop()
            except KeyboardInterrupt as e:
                print(f'KeyboardInterrupt in main_system.main_loop():\n{e}')
                main_system.shutdown()
        # If debug is disabled, we want to catch exceptions so that the program doesn't crash.
        else:
            try:
                main_system.main_loop()
            except Exception as e:
                print(f'Exception in main_system.main_loop():\n{e}')


if __name__ == "__main__":
    run()
