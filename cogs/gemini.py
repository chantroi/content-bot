from typing import Any, Dict, List, Optional, Union

import discord
from discord.ext import commands
import google.generativeai as genai
from env_config import google_api


class Gemini:
    def __init__(self, model_name: str = "gemini-1.5-flash") -> None:
        genai.configure(api_key=google_api)

        self.generation_config: Dict[str, Any] = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        self.safety_settings: List[Dict[str, str]] = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]

        self.instruction: str = (
            "Mẫu thông tin người dùng: (User: tên)."
            + "Câu trả lời của bạn không được chứa phần thông tin người dùng đó, vì nó chỉ là để giúp cho bạn biết ai đang trò chuyện với bạn, id khác nhau thì là những người dùng khác nhau."
            + "Hãy trả lời chính xác, sát với thực tế, tránh trả lời qua loa sai sự thật.Một số câu hỏi có thể là câu hỏi tư duy nên hãy suy xét kỹ trước khi trả lời."
        )

        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=self.generation_config,
            safety_settings=self.safety_settings,
            system_instruction=self.instruction,
        )
        self.chat = model.start_chat(history=[])

    def send(self, text: str, user: Union[discord.Member, discord.User], file_obj: Any = None) -> str:
        info: str = f"(User: {user})"
        if not file_obj:
            message: List[str] = [text + "\n", info]
        else:
            message: List[Any] = [
                text + "\n",
                info + "\n",
                file_obj,
            ]
        response = self.chat.send_message(message)
        return response.text


class GeminiCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        self.gemini: Gemini = Gemini()

    @commands.slash_command()
    async def pro(self, ctx: discord.ApplicationContext) -> None:
        self.gemini = Gemini("gemini-1.5-pro")
        await ctx.respond("Gemini 1.5 Pro", delete_after=10)

    @commands.slash_command()
    async def flash(self, ctx: discord.ApplicationContext) -> None:
        self.gemini = Gemini("gemini-1.5-flash")
        await ctx.respond("Gemini 1.5 Flash", delete_after=10)

    @commands.slash_command()
    async def model(self, ctx: discord.ApplicationContext, model_name: str) -> None:
        self.gemini = Gemini(model_name)
        await ctx.respond(f"Model: {model_name}", delete_after=10)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        await message.channel.trigger_typing()
        if message.author == self.bot.user:
            return
        if self.bot.user.mentioned_in(message):
            await message.reply(
                self.gemini.send(
                    message.content.replace(f"<@{self.bot.user.id}>", ""),
                    message.author,
                )
            )


def setup(bot: commands.Bot) -> None:
    bot.add_cog(GeminiCommands(bot))
