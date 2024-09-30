# -*- coding: utf-8 -*-

"""
synthhaku.features.shell
~~~~~~~~~~~~~~~~~~~~~~~~

The synthhaku shell commands.

:copyright: (c) 2021 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""
import asyncio
import contextlib
import pathlib
import re
import shutil
import sys
import tempfile
import typing

import disnake
from disnake import ui
from disnake.ext import commands

from synthhaku.codeblocks import Codeblock, codeblock_converter
from synthhaku.exception_handling import ReplResponseReactor
from synthhaku.features.baseclass import Feature
from synthhaku.flags import Flags
from synthhaku.paginators import PaginatorInterface, WrappedPaginator
from synthhaku.shell import ShellReader
from synthhaku.types import ContextA

SCAFFOLD_FOLDER = pathlib.Path(__file__).parent / "scaffolds"


@contextlib.contextmanager
def scaffold(name: str, **kwargs: typing.Any):
    """
    A context manager that sets up a temporary directory with a scaffold formatted to kwargs.

    This allows it to create temporary projects for different shell tools according to the template.
    """

    source = SCAFFOLD_FOLDER / name

    if not (source.exists() and source.is_dir()):
        raise ValueError(f"{name} is not a valid shell scaffold")

    with tempfile.TemporaryDirectory() as temp:
        temp = pathlib.Path(temp)

        for item in source.glob("**/*"):
            if "__pycache__" in str(item):
                continue

            if item.is_file():
                with open(item, "r", encoding="utf-8") as fp:
                    content = fp.read()

                target = temp / item.relative_to(source)
                target.parent.mkdir(parents=True, exist_ok=True)

                with open(target, "w", encoding="utf-8") as fp:
                    fp.write(content.format(**kwargs))

        yield temp


class ShellFeature(Feature):
    """
    Feature containing the shell-related commands
    """

    class ShellStandardInputModal(ui.Modal):
        """Modal that prompts users for text to provide to stdin"""

        def __init__(
            self, reader: ShellReader, *args: typing.Any, **kwargs: typing.Any
        ):
            super().__init__(
                title="Ввод в стандартный поток",
                components=[
                    ui.TextInput(
                        label="Текст",
                        style=disnake.TextInputStyle.paragraph,
                        custom_id="stdin_content",
                        placeholder="Введите текст для отправки в stdin"
                    )
                ],
                *args,
                timeout=300,
                **kwargs
            )
            self.reader = reader

        async def callback(self, interaction: disnake.ModalInteraction):
            value = interaction.text_values["stdin_content"] or ""

            if self.reader.stdin and self.reader.stdin.writable():
                if sys.platform == "win32":
                    self.reader.stdin.write(f"{value}\r\n".encode("utf-8"))
                else:
                    self.reader.stdin.write(f"{value}\r".encode("utf-8"))
                self.reader.stdin.flush()

                await interaction.response.send_message(
                    content="Sent into stdin", ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    content="Stdin is not writable", ephemeral=True
                )

    @Feature.Command(
        parent="snt",
        name="shell",
        aliases=["bash", "sh", "powershell", "ps1", "ps", "cmd", "terminal"],
    )
    async def snt_shell(self, ctx: ContextA, *, argument: codeblock_converter):  # type: ignore
        """
        Executes statements in the system shell.

        This uses the system shell as defined in $SHELL, or `/bin/bash` otherwise.
        Execution can be cancelled by closing the paginator.
        """

        if typing.TYPE_CHECKING:
            argument: Codeblock = argument  # type: ignore

        async with ReplResponseReactor(ctx.message):
            with self.submit(ctx):
                with ShellReader(
                        argument.content, escape_ansi=not Flags.use_ansi(ctx)
                ) as reader:
                    prefix = "```" + reader.highlight

                    paginator = WrappedPaginator(prefix=prefix, max_size=1975)
                    paginator.add_line(f"{reader.ps1} {argument.content}\n")

                    async def send_standard_input(interaction: disnake.Interaction):
                        await interaction.response.send_modal(
                            self.ShellStandardInputModal(reader)
                        )

                    stdin_button = ui.Button(label="\N{KEYBOARD} Send standard input")
                    stdin_button.callback = send_standard_input

                    interface = PaginatorInterface(
                        ctx.bot,
                        paginator,
                        owner=ctx.author,
                        additional_buttons=[stdin_button],
                    )
                    await self.bot.loop.create_task(interface.send_to(ctx))

                    async for line in reader:
                        if interface.closed:
                            return
                        await interface.add_line(line)

                await interface.add_line(f"\n[status] Return code {reader.close_code}")

    @Feature.Command(parent="snt", name="git")
    async def snt_git(self, ctx: ContextA, *, argument: codeblock_converter):  # type: ignore
        """
        Shortcut for 'snt sh git'. Invokes the system shell.
        """

        if typing.TYPE_CHECKING:
            argument: Codeblock = argument  # type: ignore

        return await ctx.invoke(self.snt_shell, argument=Codeblock(argument.language, "git " + argument.content))  # type: ignore

    @Feature.Command(parent="snt", name="pip")
    async def snt_pip(self, ctx: commands.Context, *, argument: codeblock_converter):  # type: ignore
        """
        Shortcut for 'snt sh pip'. Invokes the system shell.
        """

        if typing.TYPE_CHECKING:
            argument: Codeblock = argument  # type: ignore

        executable: str = "pip"
        location = pathlib.Path(sys.prefix)

        for test in (
                location / "bin" / "pip",
                location / "bin" / "pip3",
                location / "Scripts" / "pip.exe",
                location / "Scripts" / "pip3.exe",
        ):
            if test.exists() and test.is_file():
                executable = str(test)
                break

        return await ctx.invoke(self.snt_shell,
                                argument=Codeblock(argument.language, f"{executable} {argument.content}"))  # type: ignore

    if shutil.which("node") and shutil.which("npm"):

        @Feature.Command(parent="snt", name="node")
        async def snt_node(self, ctx: commands.Context, *, argument: codeblock_converter):  # type: ignore
            """
            Shortcut for scaffolding and executing 'npm run'. Only exists if the executables are detected.
            """

            if typing.TYPE_CHECKING:
                argument: Codeblock = argument  # type: ignore

            requirements = "".join(
                f"npm install {match} && "
                for match in re.findall("// snt require: (.+)", argument.content)
            )

            with scaffold("npm", content=argument.content) as directory:
                return await ctx.invoke(self.snt_shell,
                                        argument=Codeblock("js", f"cd {directory} && {requirements}npm run main"))  # type: ignore

    if shutil.which("pyright"):

        @Feature.Command(parent="snt", name="pyright")
        async def snt_pyright(self, ctx: commands.Context, *, argument: codeblock_converter):  # type: ignore
            """
            Shortcut for scaffolding and executing 'pyright main.c'. Only exists if the executables are detected.
            """

            if typing.TYPE_CHECKING:
                argument: Codeblock = argument  # type: ignore

            with scaffold("pyright", content=argument.content) as directory:
                return await ctx.invoke(self.snt_shell,
                                        argument=Codeblock("js", f"cd {directory} && pyright main.c"))  # type: ignore

    if shutil.which("rustc") and shutil.which("cargo"):

        @Feature.Command(parent="snt", name="rustc")
        async def snt_rustc(self, ctx: commands.Context, *, argument: codeblock_converter):  # type: ignore
            """
            Shortcut for scaffolding and executing 'cargo run'. Only exists if the executables are detected.
            """

            if typing.TYPE_CHECKING:
                argument: Codeblock = argument  # type: ignore

            requirements = "\n".join(
                re.findall("// snt require: (.+)", argument.content)
            )

            with scaffold(
                    "cargo", content=argument.content, requirements=requirements
            ) as directory:
                return await ctx.invoke(self.snt_shell,
                                        argument=Codeblock("rust", f"cd {directory} && cargo run"))  # type: ignore

    if shutil.which("g++") and shutil.which("gcc"):

        @Feature.Command(parent="snt", name="cxx")
        async def snt_gcc(self, ctx: commands.Context, *, argument: codeblock_converter):  # type: ignore
            """
            Shortcut for scaffolding and executing 'c main.c -o main'. Only exists if the executables are detected.
            """

            if typing.TYPE_CHECKING:
                argument: Codeblock = argument  # type: ignore

            with scaffold("c", content=argument.content) as directory:
                return await ctx.invoke(self.snt_shell, argument=Codeblock("c",
                                                                           f"cd {directory} && c main.c -o main && ./main"))  # type: ignore

        @Feature.Command(parent="snt", name="cpp")
        async def snt_cpp(self, ctx: commands.Context, *, argument: codeblock_converter, program_arguments: str = None):
            """
            Shortcut for scaffolding and executing 'g++ main.cpp -o main'. Only exists if the executables are detected.
            """

            if typing.TYPE_CHECKING:
                argument: Codeblock = argument  # type: ignore

            content = argument.content.strip()
            # Проверяем, есть ли разделитель `PROGRAM_ARGS:`
            if 'PROGRAM_ARGS:' in content:
                # Разделяем контент на код и аргументы
                code, args = content.split('PROGRAM_ARGS:', 1)
                code = code.strip()
                program_arguments = args.strip()
            else:
                code = content
                program_arguments = program_arguments or ""

            with scaffold("cpp", content=code) as directory:
                # Компилируем программу
                compile_command = f"cd {directory} && g++ main.cpp -o main"
                # Запускаем программу с аргументами
                run_command = f"./main {program_arguments}"

                # Выполняем компиляцию, затем запуск
                return await ctx.invoke(self.snt_shell,
                                        argument=Codeblock("bash", f"{compile_command} && {run_command}"))  # type: ignore