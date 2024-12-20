from typing import Any, Dict, List, Optional, Union

import discord
from discord.ext import commands
import google.generativeai as genai
from env_config import google_api


class Gemini:
    def __init__(self, model_name: str = "gemini-1.5-flash") -> None:
        genai.configure(api_key=google_api)

        self.current_model = model_name

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

        model: genai.GenerativeModel = genai.GenerativeModel(
            model_name=model_name,
            generation_config=self.generation_config,
            safety_settings=self.safety_settings,
            system_instruction=self.instruction,
        )

        self.chat = model.start_chat(history=[])

    def list_models(self) -> List[str]:
        models: List[Any] = genai.list_models()
        gemini_models = []
        for model in models:
            if "gemini" in model.name.lower():
                # Remove 'models/' prefix from model name
                clean_name = model.name.replace('models/', '')
                gemini_models.append(clean_name)
        
        # Sắp xếp theo version để lấy các model mới nhất
        gemini_models.sort(reverse=True)
        return gemini_models  

    def switch_model(self, model_name: str) -> None:
        self.current_model = model_name
        model: genai.GenerativeModel = genai.GenerativeModel(
            model_name=model_name,
            generation_config=self.generation_config,
            safety_settings=self.safety_settings,
            system_instruction=self.instruction,
        )
        self.chat = model.start_chat(history=[])

    def send(
        self, text: str, user: Union[discord.Member, discord.User], file_obj: Any = None
    ) -> str:
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


class ModelSelect(discord.ui.View):
    def __init__(self, gemini_commands):
        super().__init__()
        self.gemini_commands = gemini_commands
        self.current_page = 0
        self.models = self.gemini_commands.gemini.list_models()
        self.max_page = (len(self.models) - 1) // 25
        
        self.update_select_menu()
        
        # Add navigation buttons if there are multiple pages
        if self.max_page > 0:
            # Previous button
            prev_button = discord.ui.Button(
                style=discord.ButtonStyle.secondary,
                label="◀ Previous",
                custom_id="prev",
                disabled=True
            )
            prev_button.callback = self.prev_page
            self.add_item(prev_button)
            
            # Next button
            next_button = discord.ui.Button(
                style=discord.ButtonStyle.secondary,
                label="Next ▶",
                custom_id="next",
                disabled=False if len(self.models) > 25 else True
            )
            next_button.callback = self.next_page
            self.add_item(next_button)
    
    def update_select_menu(self):
        # Remove old select menu if it exists
        for item in self.children[:]:
            if isinstance(item, discord.ui.Select):
                self.remove_item(item)
        
        # Calculate slice for current page
        start_idx = self.current_page * 25
        end_idx = min(start_idx + 25, len(self.models))
        
        # Create new select menu with current page's models
        select = discord.ui.Select(
            placeholder=f"Choose a model (Page {self.current_page + 1}/{self.max_page + 1})",
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(
                    label=model_name,
                    value=model_name,
                    description=f"Switch to {model_name}"
                )
                for model_name in self.models[start_idx:end_idx]
            ]
        )
        select.callback = self.select_callback
        self.add_item(select)
        
        # Update button states
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                if item.custom_id == "prev":
                    item.disabled = self.current_page == 0
                elif item.custom_id == "next":
                    item.disabled = self.current_page >= self.max_page
    
    async def prev_page(self, interaction: discord.Interaction):
        self.current_page = max(0, self.current_page - 1)
        self.update_select_menu()
        await interaction.response.edit_message(view=self)
    
    async def next_page(self, interaction: discord.Interaction):
        self.current_page = min(self.max_page, self.current_page + 1)
        self.update_select_menu()
        await interaction.response.edit_message(view=self)
    
    async def select_callback(self, interaction: discord.Interaction):
        model_name = interaction.data["values"][0]
        self.gemini_commands.gemini.switch_model(model_name)
        await interaction.response.send_message(f"Switched to model: **{model_name}**", ephemeral=True)


class GeminiCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        self.gemini: Gemini = Gemini()

    @commands.slash_command()
    async def model(self, ctx: discord.ApplicationContext) -> None:
        view = ModelSelect(self)
        current_model = self.gemini.current_model
        await ctx.respond(f"Current model: **{current_model}**\nChoose a model:", view=view)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.bot.user:
            return
            
        # Phản hồi khi được mention hoặc trong kênh có chữ gemini
        if self.bot.user.mentioned_in(message) or "gemini" in message.channel.name.lower():
            await message.channel.trigger_typing()
            await message.reply(
                self.gemini.send(
                    message.content.replace(f"<@{self.bot.user.id}>", ""),
                    message.author,
                )
            )


def setup(bot: commands.Bot) -> None:
    bot.add_cog(GeminiCommands(bot))
