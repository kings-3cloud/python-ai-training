import importlib.util
from pathlib import Path

PLUGINS_DIR = Path(__file__).parent / "plugins"


def load_plugins():
    """Scan the plugins folder and dynamically import every valid plugin module."""
    plugins = {}
    for plugin_path in sorted(PLUGINS_DIR.iterdir()):
        if plugin_path.suffix == ".py" and not plugin_path.stem.startswith("_"):
            module_name = plugin_path.stem
            spec = importlib.util.spec_from_file_location(module_name, plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "NAME") and hasattr(module, "run"):
                plugins[module_name] = module
    return plugins


def list_plugins(plugins):
    """Print all discovered plugins with their index and display name."""
    if not plugins:
        print("No plugins found.")
        return
    print("\nAvailable plugins:")
    for i, module in enumerate(plugins.values(), 1):
        print(f"  {i}. {module.NAME}")


def run_plugin(plugins):
    """Prompt the user to pick a plugin by number, then execute it."""
    list_plugins(plugins)
    if not plugins:
        return
    choice = input("\nEnter plugin number to run (or 0 to cancel): ").strip()
    try:
        index = int(choice) - 1
        plugin_list = list(plugins.values())
        if index == -1:
            return
        if 0 <= index < len(plugin_list):
            print()
            plugin_list[index].run()
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")


def main():
    plugins = load_plugins()
    while True:
        print("\n=== Plugin Manager ===")
        print("1. List plugins")
        print("2. Run a plugin")
        print("3. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            list_plugins(plugins)
        elif choice == "2":
            run_plugin(plugins)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()

