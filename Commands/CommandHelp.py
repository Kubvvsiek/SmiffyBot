from __future__ import annotations

from typing import TYPE_CHECKING, Awaitable, Callable, Iterable

from nextcord import (
    Color,
    Embed,
    SelectOption,
    SlashApplicationCommand,
    slash_command,
    ui,
    utils,
)

from enums import Emojis
from utilities import CustomCog, CustomInteraction, DiscordSupportButton

if TYPE_CHECKING:
    from bot import Smiffy


class BotCommandsCategory(ui.Select):
    def __init__(self, embed: Embed, embed_description: str) -> None:
        self.default_description: str = embed_description
        self.embed: Embed = embed

        self.cached_categories: dict[str, tuple[str, int]] = {}

        options = [
            SelectOption(
                label="Administracyjne", description="Komendy administracyjne.", emoji="⛔", value="admin"
            ),
            SelectOption(
                label="Ustawienia",
                description="Komendy pozwalające skonfigurować serwer.",
                emoji="🔧",
                value="settings",
            ),
            SelectOption(label="Muzyczne", description="Komendy dotyczące muzyki.", emoji="🔊", value="music"),
            SelectOption(
                label="Ekonomia",
                description="Komendy ekonomii.",
                emoji="<a:amoney:1154533728010383391>",
                value="economy",
            ),
            SelectOption(
                label="Dodatkowe", description="Dodatkowe komendy bota.", emoji="🍀", value="additional"
            ),
            SelectOption(
                label="Levelowanie", description="Komendy dotyczące levelowania.", emoji="✨", value="leveling"
            ),
            SelectOption(label="Bot", description="Komendy dotyczące bota.", emoji="🤖", value="bot"),
            SelectOption(
                label="4Fun", description="Komendy do umilenia sobie czasu.", emoji="😆", value="forfun"
            ),
            SelectOption(label="Menu", description="Powrót do menu komendy.", emoji="🔗", value="menu"),
        ]

        super().__init__(placeholder="Wybierz kategorie komend", options=options)

    @staticmethod
    def get_commands_by_category(bot: Smiffy, category: str) -> Iterable[SlashApplicationCommand]:
        commands: dict[str, SlashApplicationCommand] = {}

        for cmd in bot.get_all_application_commands():
            if cmd.is_global:
                module: str = cmd.parent_cog.__class__.__dict__["__module__"]
                if category in module and isinstance(cmd, SlashApplicationCommand) and cmd.name:
                    commands[cmd.name] = cmd

        sorted_commands: dict[str, SlashApplicationCommand] = dict(sorted(commands.items()))
        return sorted_commands.values()

    @staticmethod
    def format_commands(commands: list[SlashApplicationCommand]) -> tuple[str, int]:
        description: str = ""
        commands_amount: int = 0

        for cmd in commands:
            if cmd.children:
                for sub_command in cmd.children.values():
                    if sub_command.children:
                        for sub_sub_command in sub_command.children.values():
                            commands_amount += 1
                            description += (
                                f"- {sub_sub_command.get_mention()} - {sub_sub_command.description}\n"
                            )
                    else:
                        commands_amount += 1
                        description += f"- {sub_command.get_mention()} - {sub_command.description}\n"
            else:
                commands_amount += 1
                description += f"- {cmd.get_mention()} - {cmd.description}\n"

        return description, commands_amount

    async def callback(self, interaction: CustomInteraction):
        category: str = self.values[0]

        category_callback: Callable[[CustomInteraction], Awaitable] = getattr(self, category)
        await interaction.response.defer()

        await category_callback(interaction)

    async def admin(self, interaction: CustomInteraction):
        if not self.cached_categories.get("admin"):
            commands: list[SlashApplicationCommand] = list(
                self.get_commands_by_category(interaction.bot, "administration")
            )
            description, amount_of_commands = self.format_commands(commands)
            self.cached_categories["admin"] = (description, amount_of_commands)

        else:
            description, amount_of_commands = self.cached_categories["admin"]

        self.embed.title = f"`⛔` Kategoria: Administracyjne ({amount_of_commands})"
        self.embed.description = description

        if interaction.message:
            await interaction.followup.edit_message(embed=self.embed, message_id=interaction.message.id)

    async def settings(self, interaction: CustomInteraction):
        if not self.cached_categories.get("settings"):
            commands: list[SlashApplicationCommand] = list(
                self.get_commands_by_category(interaction.bot, "settings")
            )
            commands = [cmd for cmd in commands if cmd.name != "levelowanie"]

            description, amount_of_commands = self.format_commands(commands)
            self.cached_categories["settings"] = (description, amount_of_commands)
        else:
            description, amount_of_commands = self.cached_categories["settings"]

        self.embed.title = f"`🔧` Kategoria: Ustawienia ({amount_of_commands})"
        self.embed.description = description

        if interaction.message:
            await interaction.followup.edit_message(embed=self.embed, message_id=interaction.message.id)

    async def music(self, interaction: CustomInteraction):
        if not self.cached_categories.get("music"):
            commands: list[SlashApplicationCommand] = list(
                self.get_commands_by_category(interaction.bot, "music")
            )
            description, amount_of_commands = self.format_commands(commands)

            self.cached_categories["music"] = (description, amount_of_commands)
        else:
            description, amount_of_commands = self.cached_categories["music"]

        self.embed.title = f"`🔊` Kategoria: Muzyka ({amount_of_commands})"
        self.embed.description = description

        if interaction.message:
            await interaction.followup.edit_message(embed=self.embed, message_id=interaction.message.id)

    async def economy(self, interaction: CustomInteraction):
        if not self.cached_categories.get("economy"):
            commands: list[SlashApplicationCommand] = list(
                self.get_commands_by_category(interaction.bot, "economy")
            )
            description, amount_of_commands = self.format_commands(commands)

            self.cached_categories["economy"] = (description, amount_of_commands)
        else:
            description, amount_of_commands = self.cached_categories["economy"]

        self.embed.title = f"`💸` Kategoria: Ekonomia ({amount_of_commands})"
        self.embed.description = description

        if interaction.message:
            await interaction.followup.edit_message(embed=self.embed, message_id=interaction.message.id)

    async def additional(self, interaction: CustomInteraction):
        if not self.cached_categories.get("additional"):
            commands: list[SlashApplicationCommand] = list(
                self.get_commands_by_category(interaction.bot, "additional")
            )
            description, amount_of_commands = self.format_commands(commands)

            self.cached_categories["additional"] = (description, amount_of_commands)
        else:
            description, amount_of_commands = self.cached_categories["additional"]

        self.embed.title = f"`🍀` Kategoria: Dodatkowe ({amount_of_commands})"
        self.embed.description = description

        if interaction.message:
            await interaction.followup.edit_message(embed=self.embed, message_id=interaction.message.id)

    async def leveling(self, interaction: CustomInteraction):
        if not self.cached_categories.get("leveling"):
            commands: list[SlashApplicationCommand] = list(
                self.get_commands_by_category(interaction.bot, "settings")
            )
            commands = [cmd for cmd in commands if cmd.name == "levelowanie"]

            description, amount_of_commands = self.format_commands(commands)
            self.cached_categories["leveling"] = (description, amount_of_commands)
        else:
            description, amount_of_commands = self.cached_categories["leveling"]

        self.embed.title = f"`✨` Kategoria: Levelowanie ({amount_of_commands})"
        self.embed.description = description

        if interaction.message:
            await interaction.followup.edit_message(embed=self.embed, message_id=interaction.message.id)

    async def bot(self, interaction: CustomInteraction):
        if not self.cached_categories.get("bot"):
            commands: list[SlashApplicationCommand] = list(
                self.get_commands_by_category(interaction.bot, "client")
            )
            commands = [cmd for cmd in commands if cmd.name != "globalban"]

            description, amount_of_commands = self.format_commands(commands)

            self.cached_categories["bot"] = (description, amount_of_commands)
        else:
            description, amount_of_commands = self.cached_categories["bot"]

        self.embed.title = f"`🤖` Kategoria: Bot ({amount_of_commands})"
        self.embed.description = description

        if interaction.message:
            await interaction.followup.edit_message(embed=self.embed, message_id=interaction.message.id)

    async def forfun(self, interaction: CustomInteraction):
        if not self.cached_categories.get("forfun"):
            commands: list[SlashApplicationCommand] = list(
                self.get_commands_by_category(interaction.bot, "forfun")
            )
            description, amount_of_commands = self.format_commands(commands)

            self.cached_categories["forfun"] = (description, amount_of_commands)
        else:
            description, amount_of_commands = self.cached_categories["forfun"]

        self.embed.title = f"`😆` Kategoria: ForFun ({amount_of_commands})"
        self.embed.description = description

        if interaction.message:
            await interaction.followup.edit_message(embed=self.embed, message_id=interaction.message.id)

    async def menu(self, interaction: CustomInteraction):
        self.embed.title = "`✨` Smiffy - Pomoc"
        self.embed.description = self.default_description

        if interaction.message:
            await interaction.followup.edit_message(embed=self.embed, message_id=interaction.message.id)


class CommandHelpView(DiscordSupportButton):
    def __init__(self, message_author: int, embed: Embed):
        super().__init__()

        self.message_author: int = message_author
        self.embed: Embed = embed

        if isinstance(embed.description, str):
            self.default_description: str = embed.description
        else:
            self.default_description = ""

        self.add_item(BotCommandsCategory(self.embed, self.default_description))

    async def interaction_check(self, interaction: CustomInteraction):
        assert interaction.user

        if self.message_author == interaction.user.id:
            return True  # Checking if the user who pressed the button is the author of the interaction

        await interaction.send_error_message(
            description="Tylko autor użytej komendy może tego użyć.", ephemeral=True
        )

        return False


class CommandHelp(CustomCog):
    @slash_command(name="pomoc", description="Komenda pomocy", dm_permission=False)
    async def help(self, interaction: CustomInteraction):
        assert interaction.user

        ping, shard = interaction.get_bot_latency()
        commands: int = len(self.bot.get_all_application_commands())

        embed = Embed(
            title="`✨` Smiffy - Pomoc",
            color=Color.dark_theme(),
            timestamp=utils.utcnow(),
            description=f"{Emojis.REPLY.value} **Dzięki tej komendzie możesz sprawdzić wszystkie moje komendy.**"
            f"\n\n- `🏓` Ping: `{ping}ms`\n"
            f"- `🛠️` Shard: `{shard}`\n"
            f"- `🔧` Komendy: `{commands}`",
        )
        embed.set_author(name=interaction.user, icon_url=interaction.user_avatar_url)
        embed.set_thumbnail(url=interaction.guild_icon_url)
        embed.set_footer(text=f"Smiffy v{self.bot.__version__}", icon_url=self.bot.avatar_url)

        await interaction.send(embed=embed, view=CommandHelpView(interaction.user.id, embed))


def setup(bot: Smiffy):
    bot.add_cog(CommandHelp(bot))
