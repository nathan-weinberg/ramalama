import os
from ramalama.common import get_engine, exec_cmd

file_not_found = """\
RamaLama requires the "%(cmd)s" command to be installed on the host when running with --nocontainer.
RamaLama is designed to run AI Models inside of containers, where "%(cmd)s" is already installed.
Either install a package containing the "%(cmd)s" command or run the workload inside of a container.
%(error)s"""

class StackBase:

    def __not_implemented_error(self, param):
        return NotImplementedError(f"ramalama {param} for '{type(self).__name__}' not implemented")

    def pull(self, args):
        raise self.__not_implemented_error("pull")

    def run(self, args):
        raise self.__not_implemented_error("serve")


class Stack(StackBase):
    """Stack super class"""

    def __init__(self, distro):
        self.distro = distro


    def exists(self, args):
        distro_path = self.distro_path(args)
        if not os.path.exists(distro_path):
            return None

        return distro_path


    def get_distro_path(self, args):
        distro_path = self.exists(args)
        if distro_path:
            return distro_path

        if args.dryrun:
            return "/path/to/distro"

        distro_path = self.pull(args)

        return distro_path


    def build_exec_args_run(self, args, distro_path):
        exec_args = []
        exec_args += [
            f"CONTAINER_BINARY={get_engine()}"
            "llama",
            "stack",
            "run",
            distro_path,
            "--image-type",
            "container",
        ] + args
        return exec_args


    def execute_command(self, distro_path, exec_args, args):
        try:
            if args.dryrun:
                dry_run(exec_args)
                return
            exec_cmd(exec_args, debug=args.debug)
        except FileNotFoundError as e:
            raise NotImplementedError(file_not_found % {"cmd": exec_args[0], "error": str(e).strip("'")})


    def run(self, args):
        distro_path = self.get_distro_path(args)
        exec_args = self.build_exec_args_run(args, distro_path)

        self.execute_command(distro_path, exec_args, args)


def dry_run(args):
    for arg in args:
        if not arg:
            continue
        if " " in arg:
            print('"%s"' % arg, end=" ")
        else:
            print("%s" % arg, end=" ")
    print()
