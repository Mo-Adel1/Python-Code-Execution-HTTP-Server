def prompt_for_port(available_port):
    print(f"Available port: {available_port}")
    use_new_port = input(f"Would you like to use port {available_port}? (y/n): ")
    return available_port if use_new_port.lower() == 'y' else None


def handle_no_available_ports():
    print("No available ports found.")
    retry = input("Would you like to try again later? (y/n): ")
    if retry.lower() == 'y':
        print("Retrying in a few seconds...")
    return None
