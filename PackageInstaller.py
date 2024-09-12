import pkg_resources
import subprocess
import sys

class PackageInstaller:
    @staticmethod
    def install(package):
        try:
            dist = pkg_resources.get_distribution(package)
            print("{} ({}) is already installed".format(dist.key, dist.version))
        except pkg_resources.DistributionNotFound:
            print("{} is NOT installed".format(package))
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])