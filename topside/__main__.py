import surface_main

def run():

    main_system = surface_main.MainSystem()

    while main_system.run:
        try:
            main_system.main_loop()
        except Exception as e:
            # In competition, we should log the exception and continue.  In debug we should crash to fix the issue

            print(f'Exception in main_system.main_loop():\n{e}')


if __name__ == "__main__":
    run()
