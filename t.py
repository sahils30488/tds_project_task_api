import subprocess


def A2(prettier_version="prettier@3.4.2", filename="/data/format.md"):
    command = f"npx {prettier_version} --write {filename}"

    try:
        result = subprocess.run(
            command, shell=True, check=True, text=True, capture_output=True
        )
        print("✅ Prettier executed successfully.\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ A2 FAILED: {e}\n{e.stderr}")


# Run the function
A2()
