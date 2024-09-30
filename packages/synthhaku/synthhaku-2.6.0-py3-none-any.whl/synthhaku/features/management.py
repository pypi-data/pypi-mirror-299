# -*- coding: utf-8 -*-

"""
synthhaku.features.management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The synthhaku extension and bot control commands.

:copyright: (c) 2021 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""

import itertools
import re
import time
import traceback
import typing
from urllib.parse import urlencode

import disnake
from disnake.ext import commands

from synthhaku.features.baseclass import Feature
from synthhaku.flags import Flags
from synthhaku.math import mean_stddev
from synthhaku.modules import ExtensionConverter
from synthhaku.types import ContextA

from synthhaku.paginators import WrappedPaginator, PaginatorInterface


class ManagementFeature(Feature):
    """
    Feature containing the extension and bot control commands
    """

    @Feature.Command(parent="snt", name="load", aliases=["reload"])
    async def snt_load(self, ctx: ContextA, *extensions: ExtensionConverter):  # type: ignore
        """
        Loads or reloads the given extension names.

        Reports any extensions that failed to load.
        """

        extensions: typing.Iterable[typing.List[str]] = extensions  # type: ignore

        paginator = commands.Paginator(prefix="", suffix="")

        # 'snt reload' on its own just reloads synthhaku
        if ctx.invoked_with == "reload" and not extensions:
            extensions = [["synthhaku"]]

        for extension in itertools.chain(*extensions):
            method, icon = (
                (
                    self.bot.reload_extension,
                    "\N{CLOCKWISE RIGHTWARDS AND LEFTWARDS OPEN CIRCLE ARROWS}",
                )
                if extension in self.bot.extensions
                else (self.bot.load_extension, "\N{INBOX TRAY}")
            )

            try:
                await disnake.utils.maybe_coroutine(method, extension)
            except Exception as exc:  # pylint: disable=broad-except
                if isinstance(exc, commands.ExtensionFailed) and exc.__cause__:
                    cause = exc.__cause__
                    traceback_data = "".join(
                        traceback.format_exception(
                            type(cause), cause, cause.__traceback__, 8
                        )
                    )
                else:
                    traceback_data = "".join(
                        traceback.format_exception(type(exc), exc, exc.__traceback__, 2)
                    )

                paginator.add_line(
                    f"{icon}\N{WARNING SIGN} `{extension}`\n```py\n{traceback_data}\n```",
                    empty=True,
                )
            else:
                paginator.add_line(f"{icon} `{extension}`", empty=True)

        for page in paginator.pages:
            await ctx.send(page)

    @Feature.Command(parent="snt", name="unload")
    async def snt_unload(self, ctx: ContextA, *extensions: ExtensionConverter):  # type: ignore
        """
        Unloads the given extension names.

        Reports any extensions that failed to unload.
        """

        extensions: typing.Iterable[typing.List[str]] = extensions  # type: ignore

        paginator = commands.Paginator(prefix="", suffix="")
        icon = "\N{OUTBOX TRAY}"

        for extension in itertools.chain(*extensions):
            try:
                await disnake.utils.maybe_coroutine(
                    self.bot.unload_extension, extension
                )
            except Exception as exc:  # pylint: disable=broad-except
                traceback_data = "".join(
                    traceback.format_exception(type(exc), exc, exc.__traceback__, 2)
                )

                paginator.add_line(
                    f"{icon}\N{WARNING SIGN} `{extension}`\n```py\n{traceback_data}\n```",
                    empty=True,
                )
            else:
                paginator.add_line(f"{icon} `{extension}`", empty=True)

        for page in paginator.pages:
            await ctx.send(page)

    @Feature.Command(parent="snt", name="shutdown", aliases=["logout"])
    async def snt_shutdown(self, ctx: ContextA):
        """
        Logs this bot out.
        """

        ellipse_character = (
            "\N{BRAILLE PATTERN DOTS-356}"
            if Flags.USE_BRAILLE_J
            else "\N{HORIZONTAL ELLIPSIS}"
        )

        await ctx.send(f"Logging out now{ellipse_character}")
        await ctx.bot.close()

    @Feature.Command(parent="snt", name="invite")
    async def snt_invite(self, ctx: ContextA, *perms: str):
        """
        Retrieve the invite URL for this bot.

        If the names of permissions are provided, they are requested as part of the invite.
        """

        scopes = ("bot", "applications.commands")
        permissions = disnake.Permissions()

        for perm in perms:
            if perm not in dict(permissions):
                raise commands.BadArgument(f"Invalid permission: {perm}")

            setattr(permissions, perm, True)

        application_info = await self.bot.application_info()

        query = {
            "client_id": application_info.id,
            "scope": "+".join(scopes),
            "permissions": permissions.value,
        }

        return await ctx.send(
            f"Link to invite this bot:\n<https://discordapp.com/oauth2/authorize?{urlencode(query, safe='+')}>"
        )

    @Feature.Command(parent="snt", name="rtt", aliases=["ping"])
    async def snt_rtt(self, ctx: ContextA):
        """
        Calculates Round-Trip Time to the API.
        """

        message = None

        # We'll show each of these readings as well as an average and standard deviation.
        api_readings: typing.List[float] = []
        # We'll also record websocket readings, but we'll only provide the average.
        websocket_readings: typing.List[float] = []

        # We do 6 iterations here.
        # This gives us 5 visible readings, because a request can't include the stats for itself.
        for _ in range(6):
            # First generate the text
            text = "Calculating round-trip time...\n\n"
            text += "\n".join(
                f"Reading {index + 1}: {reading * 1000:.2f}ms"
                for index, reading in enumerate(api_readings)
            )

            if api_readings:
                average, stddev = mean_stddev(api_readings)

                text += f"\n\nAverage: {average * 1000:.2f} \N{PLUS-MINUS SIGN} {stddev * 1000:.2f}ms"
            else:
                text += "\n\nNo readings yet."

            if websocket_readings:
                average = sum(websocket_readings) / len(websocket_readings)

                text += f"\nWebsocket latency: {average * 1000:.2f}ms"
            else:
                text += f"\nWebsocket latency: {self.bot.latency * 1000:.2f}ms"

            # Now do the actual request and reading
            if message:
                before = time.perf_counter()
                await message.edit(content=text)
                after = time.perf_counter()

                api_readings.append(after - before)
            else:
                before = time.perf_counter()
                message = await ctx.send(content=text)
                after = time.perf_counter()

                api_readings.append(after - before)

            # Ignore websocket latencies that are 0 or negative because they usually mean we've got bad heartbeats
            if self.bot.latency > 0.0:
                websocket_readings.append(self.bot.latency)

    SLASH_COMMAND_ERROR = re.compile(r"In ((?:\d+\.[a-z]+\.?)+)")

    @Feature.Command(parent="snt", name="help", aliases=["commands"])
    async def snt_help(self, ctx: commands.Context):
        """
        Отправляет интерактивный список всех команд в категории snt.
        """
        
        commands_list = self.get_commands()
        paginator = WrappedPaginator(prefix="# Команды Haku:\n```", suffix="```", max_size=1985)
        for command in commands_list:
            paginator.add_line(f"- {command.name}: {command.help or 'Нет описания'}")
        
        interface = PaginatorInterface(ctx.bot, paginator, owner=ctx.author)
        await interface.send_to(ctx)

    def get_commands(self) -> typing.List[commands.Command]:
        """Returns a list of commands the cog has.

        Returns
        -------
        List[:class:`.Command`]
            A :class:`list` of :class:`.Command`\\s that are
            defined inside this cog.

            .. note::

                This does not include subcommands.
        """
        return [c for c in self.__cog_commands__]
