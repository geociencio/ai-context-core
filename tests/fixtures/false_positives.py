def safe_function():
    # This is a comment saying we should not use exec(
    print("This string contains eval( which should not be flagged")

    x = "os.system('rm -rf /')"  # This is just a string variable  # noqa: F841

    return "subprocess.call( is dangerous but not here"
