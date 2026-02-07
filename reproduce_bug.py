import subprocess
import sys


def run_repro():
    print("Running ai-context-core qgis command on mock_qgis_plugin...")
    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "ai_context_core.cli",
                "qgis",
                "--path",
                "mock_qgis_plugin",
            ],
            capture_output=True,
            text=True,
            cwd="/home/jmbernales/qgispluginsdev/ai-context-core/src",
        )
        output = result.stdout + result.stderr
        print("Output:\n" + output)

        if "QGIS Compliance Score: 0.0/100" in output:
            print("\n❌ Reproduced: Compliance Score is 0.0")
            return True
        else:
            # Score is NOT 0.0, which means the profile was loaded!
            print("\n✅ Success: Compliance Score is NOT 0.0")
            return False

    except Exception as e:
        print(f"Error running content: {e}")
        return False


if __name__ == "__main__":
    success = run_repro()
    sys.exit(0 if success else 1)
