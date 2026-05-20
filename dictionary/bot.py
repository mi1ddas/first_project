# dictionary/bot.py
from .models import Term
from .services import ExternalDictionaryService

class DictionaryBot:
    COMMANDS = {
        '/start': (
            "👋 Привет! Я IT-словарь бот. Вот что я умею:\n\n"
            "🔍 Просто напиши термин — и я найду определение.\n"
            "📖 Спроси: «что такое Python?» или «объясни алгоритм».\n"
            "⚙️ Введи /help — список всех команд."
        ),
        '/help': (
            "📚 Список команд:\n\n"
            "/start — приветствие и краткая справка\n"
            "/help — эта подсказка\n"
            "/list — показать все термины в базе\n"
            "/about — информация о боте\n"
            "/clear — очистить историю чата\n\n"
            "Или просто напиши любой IT-термин, и я найду определение!"
        ),
        '/about': (
            "🤖 IT-Словарь Бот\n\n"
            "Версия: 1.0\n"
            "Технологии: Python, Django, SQLite, Wikipedia API\n\n"
            "Я помогаю разобраться в IT-терминологии.\n"
            "Если термина нет в базе — ищу в Википедии."
        ),
        '/clear': '__CLEAR__',  
    }

    GREETINGS = [
        'привет', 'хай', 'hello', 'hi', 'здравствуй', 'здравствуйте',
        'добрый день', 'добрый вечер', 'доброе утро', 'салют', 'хей'
    ]

    FAREWELLS = [
        'пока', 'до свидания', 'bye', 'goodbye', 'досвидания',
        'до встречи', 'выход', 'quit', 'exit'
    ]

    THANKS = [
        'спасибо', 'благодарю', 'thanks', 'thank you', 'спс', 'сяб'
    ]

    QUESTION_PREFIXES = [
        'что такое ', 'объясни ', 'расскажи про ', 'расскажи о ',
        'что значит ', 'что означает ', 'что такое ', 'как работает ',
        'покажи ', 'найди ', 'поиск ', 'search ',
    ]

    def get_response(self, user_text: str) -> str:
        text = user_text.strip().lower()

        if not text:
            return "✏️ Напиши что-нибудь! Например, «что такое Python?» или /help"

        if text.startswith('/'):
            return self._handle_command(text)

        if any(text == g or text.startswith(g) for g in self.GREETINGS):
            return "👋 Привет! Напиши термин или команду /help — покажу что умею."

        if any(text == f or text.startswith(f) for f in self.FAREWELLS):
            return "👋 До свидания! Возвращайся, если понадоблюсь."
        if any(text == t or text.startswith(t) for t in self.THANKS):
            return "😊 Пожалуйста! Если ещё что-то нужно — просто напиши."
        query = self._extract_query(text)

        return self._search(query)

    def _handle_command(self, text: str) -> str:
        command = text.split()[0]

        if command == '/list':
            return self._get_term_list()

        if command in self.COMMANDS:
            return self.COMMANDS[command]
        return (
            f"❓ Команда «{command}» не найдена.\n"
            "Введи /help — покажу список доступных команд."
        )

    def _get_term_list(self) -> str:
        terms = Term.objects.all().order_by('word')

        if not terms.exists():
            return (
                "📭 База терминов пока пустая.\n"
                "Добавь первый термин через форму ниже!"
            )
        term_list = '\n'.join([f"• {t.word}" for t in terms])
        return f"📚 Термины в базе ({terms.count()}):\n\n{term_list}"

    def _extract_query(self, text: str) -> str:
        text = text.rstrip('?!.,;:')
        for prefix in self.QUESTION_PREFIXES:
            if text.startswith(prefix):
                return text[len(prefix):].strip()
        return text

    def _search(self, query: str) -> str:
        if not query:
            return "✏️ Напиши термин для поиска."
        term = Term.objects.filter(word__icontains=query).first()

        if term:
            return (
                f"✅ Нашёл в базе!\n\n"
                f"📌 {term.word.upper()}\n\n"
                f"{term.definition}"
            )
        wiki_result = ExternalDictionaryService.get_hint_from_wikipedia(query)

        if wiki_result:
            response = f"🌐 В базе нет, но нашёл в Википедии:\n\n"
            response += f"📌 {wiki_result['title']}\n\n"

            if wiki_result.get('extract'):
                response += f"{wiki_result['extract']}\n\n"

            response += f"🔗 Подробнее: {wiki_result['url']}"
            return response

        return (
            f"🤷 Термин «{query}» не найден ни в базе, ни в Википедии.\n\n"
            "Попробуй переформулировать или добавь его сам через форму ниже."
        )