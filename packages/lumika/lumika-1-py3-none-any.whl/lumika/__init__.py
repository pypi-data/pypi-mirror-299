import logging, os, sys
from subprocess import run, CompletedProcess
from typing import Any
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import WordCompleter

def paint(cont: str) -> str:
    return cont \
        .replace("&bold", "\033[1m") \
        .replace("&underline", "\033[4m") \
        .replace("&italic", "\033[3m") \
        .replace("&blink", "\033[5m") \
        .replace("&reverse", "\033[7m") \
        .replace("&hide", "\033[8m") \
        .replace("&reset", "\033[0m") \
        .replace("&g", "\033[32m") \
        .replace("&r", "\033[31m") \
        .replace("&y", "\033[33m") \
        .replace("&b", "\033[34m") \
        .replace("&m", "\033[35m") \
        .replace("&c", "\033[36m") \
        .replace("&w", "\033[37m") \
        .replace("&0", "\033[0m") \
        + "\033[0m"

logging.getLogger('asyncio').setLevel(logging.WARNING)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(message)s"
)


class ColoredFormatter(logging.Formatter):
    COLORS: dict[str, str] = {
        "DEBUG": "&c",
        "INFO": "&g",
        "WARNING": "&y",
        "ERROR": "&r",
        "CRITICAL": "&m"
    }

    def format(self, record) -> str:
        levelname = record.levelname
        if levelname in self.COLORS:
            levelname = record.levelname.lower()  # Use lowercase
            colored_msg = f"{self.COLORS[record.levelname]}{record.msg}&0"  # Add color
            record.msg = colored_msg
            record.levelname = levelname

        return paint(super().format(record))

logger: logging.Logger = logging.getLogger(__name__)
handler: logging.StreamHandler = logging.StreamHandler()
handler.setFormatter(ColoredFormatter("%(levelname)s: %(message)s"))
logger.handlers = []
logger.addHandler(handler)
logger.propagate = False
autocomplete_words = [
    "cd ", "cm ", "ls ",
    "dir ", "pwd ", "mkdir ",
    "rmdir ", "rm ", "mv ",
    "cp ", "cls ", "cat ",
    "echo ", "type ", "more ",
    "less ", "nano ", "vim ",
    "vi ", "head ", "tail ",
    "touch ", "clear ", "history ",
    "kill ", "tasklist ", "ps ",
    "top ", "htop ", "uname ",
    "hostname ", "df ", "du ",
    "free ", "systeminfo ", "date ",
    "uptime ", "ping ", "tracert ",
    "traceroute ", "ipconfig ", "ifconfig ",
    "netstat ", "nslookup ", "curl ",
    "wget ", "chmod ", "chown ",
    "tar ", "zip ", "unzip ",
    "gzip ", "gunzip ", "apt ",
    "apt-get ", "yum ", "dnf ",
    "brew ", "pip ", "choco ",
    "exit ", "man ", "help ",
    "alias ", "source ", "./ ",
    "python ", "node ", "perl ",
    "ruby ", "whoami ", "sudo ",
    "shutdown ", "reboot ", "get-command ",
    "get-help ", "get-process ", "set-location ",
    "copy-item ", "remove-item ", "start-process ",
    "stop-process ", "invoke-webrequest ", "new-item ",
    "for ", "while ", "if ",
    "&& ", "| ", "> ",
    ">> ", "ca ", "s"
]
history = InMemoryHistory()
completer = WordCompleter(autocomplete_words, ignore_case=True)
session = PromptSession(history=history, completer=completer)

def get(l: list[Any], index: int, default: Any = None) -> Any:
    try:
        return l[index]

    except IndexError:
        l.append(default)

        return get(l, index, default)

def lumika_run(launcher: list[str], cmd: str, verbose: bool = False) -> None:
    log = lambda cont: logger.debug(cont) if verbose else None

    try:
        try:
            with open(".ATOMIC") as file:
                var_list: dict[str, str] = eval("{" + file.read() + "}")

        except FileNotFoundError:
            var_list: dict[str, str] = {}

        full_cmd = [*[l.format(**var_list) for l in launcher], *[c.format(**var_list) for c in cmd.split(" ")]]
        log(f"running '{" ".join(full_cmd)}'")

        result: CompletedProcess = run(full_cmd, capture_output=True, text=True)

    except OSError as err:
        log(f"an internal error occurred in the subprocess of your command. info:")
        logger.error(str(err))

        return

    except KeyError as err:
        logger.error(f"fetch request failed: no variable {str(err)}")

        return

    log("checking for std output:")
    for ln in result.stdout.split("\n"):
        logger.info(ln) if ln != "" else None

    log("checking for std errors:")
    for ln in result.stderr.split("\n"):
        logger.error(ln) if ln != "" else None

    log("process terminated")

def lumika_std() -> None:
    launcher: list[str] = ["pwsh.exe"]

    while True:
        for i, _ in enumerate(launcher):
            if launcher[i] in [
                "pwsh",
                "pwsh.exe"
            ]:
                if get(launcher, i + 1, "-Command") != "-Command":
                    launcher.insert(i + 1, "-Command")

            elif launcher[i] in [
                "cmd",
                "cmd.exe"
            ]:
                if get(launcher, i + 1, "/C") != "/C":
                    launcher.insert(i + 1, "/C")

        launcher.pop(0) if launcher[0] == "" else None

        try:
            cmds: list[str] = session.prompt(HTML(
                f"<ansiyellow><b>LUMIKA</b></ansiyellow>~"
                f"<ansiblue><i>{os.getcwd().replace("\\", "/")}</i></ansiblue>:"
                f"<ansired>{"/".join(launcher)}</ansired>> "
            )).split(";")

            for cmd in cmds:
                cmd = cmd.strip()

                if cmd == "":
                    ...

                elif cmd == "exit":
                    logger.info("exited lumika")

                    return

                elif cmd == "ca":
                    logger.warning("are you sure you want to clear all atomic variables in this directory?")
                    logger.warning("this cannot be undone.")
                    while True:
                        confirm: str = input("y/n: ").lower()

                        if confirm == "y":
                            try:
                                os.remove(".ATOMIC")

                            except FileNotFoundError:
                                ...

                            logger.info("atomic variables cleared")
                            break

                        elif confirm == "n":
                            break

                        else:
                            logger.error("invalid input")
                
                elif cmd.startswith("set "):
                    cmd = cmd.removeprefix("set ")   
                    parts: list[str] = cmd.split("=")

                    if len(parts) == 1:
                        logger.error("too few arguments")
                        return

                    with open(".ATOMIC", "a") as file:
                        file.write(f"\"{parts[0].strip()}\": \"{parts[1].strip().strip("\"")}\",\n")
                
                elif cmd == "set":
                    logger.error("too few arguments")
                
                elif cmd.startswith("verbose "):
                    lumika_run(launcher, cmd.removeprefix("verbose "), True)

                elif cmd == "verbose":
                    logger.error("too few arguments")

                elif cmd.startswith("cm :"):
                    launcher = cmd.removeprefix("cm :").split("/")

                elif cmd.startswith("cm "):
                    for c in cmd.removeprefix("cm ").split("/"):
                        if c == ".." and len(launcher) != 0:
                            pop: str = launcher.pop()

                            if pop == "-Command":
                                launcher.pop()

                            elif pop == "/C":
                                launcher.pop()
                                    
                        else:
                            launcher.append(c)

                elif cmd == "cm":
                    logger.error("too few arguments")

                elif cmd == "reboot":
                    try:
                        logger.info("restarted lumika")

                        return

                    finally:
                        run(["python.exe", "-m", "lumika"])

                elif cmd.startswith("cd "):
                    try:
                        os.chdir(cmd.removeprefix("cd "))

                    except FileNotFoundError:
                        logger.error(f"directory '{cmd.removeprefix('cd ')}' not found in '{os.getcwd()}'")

                elif cmd == "cd":
                    logger.error("too few arguments")

                else:
                    lumika_run(launcher, cmd)

        except KeyboardInterrupt:
            print("^C")

        except EOFError:
            ...

if __name__ == "__main__":
    lumika_std()