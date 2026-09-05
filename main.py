# Pydroid run kivy

from pathlib import Path

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from data.repositories import JsonStatsRepository
from services.quiz_service import QuizService
from services.stats_service import StatsService

from screens.home import HomeScreen
from screens.quiz import QuizScreen
from screens.result import ResultScreen
from screens.stats import StatsScreen
from screens.settings import SettingsScreen

from core.theme import Theme


class RootScreenManager(ScreenManager):
    pass


class VerbMasterApp(App):
    """Application composition root.

    Dependencies are created here and injected into screens/services.
    Screens do not know how persistence works.
    """

    def build(self):
        self.title = "VerbMaster"

        # Load KV
        Builder.load_file(str(self.base_dir / "ui.kv"))

        # Load verbs
        from verbs import verbs as verbs_data

        # Services
        self.stats_repository = JsonStatsRepository(
            self.base_dir / "storage"
        )

        self.stats_service = StatsService(
            self.stats_repository
        )

        self.quiz_service = QuizService(
            verbs_data
        )

        # Root
        root = RootScreenManager()

        # --------------------------------------------------
        # HOME
        # --------------------------------------------------

        root.add_widget(
            HomeScreen(
                name="home",
                verb_count=len(verbs_data),
                stats_service=self.stats_service,
            )
        )

        # --------------------------------------------------
        # QUIZ
        # --------------------------------------------------

        self.question_count = 15

        self.quiz_screen = QuizScreen(
            name="quiz",
            quiz_service=self.quiz_service,
            on_finished=self._show_result,
        )

        self.quiz_screen.set_question_count(
            self.question_count
        )

        root.add_widget(self.quiz_screen)

        # --------------------------------------------------
        # RESULT
        # --------------------------------------------------

        root.add_widget(
            ResultScreen(
                name="result",
                on_home=self.go_home,
                on_retry=self.start_quiz,
            )
        )

        # --------------------------------------------------
        # STATS
        # --------------------------------------------------

        root.add_widget(
            StatsScreen(
                name="stats",
                stats_service=self.stats_service,
                on_home=self.go_home,
                on_practice=self.start_quiz,
            )
        )

        # --------------------------------------------------
        # SETTINGS
        # --------------------------------------------------

        root.add_widget(
            SettingsScreen(
                name="settings",
                on_home=self.go_home,
                on_questions_changed=self.set_question_count,
            )
        )

        self.root = root

        self.refresh_stats()

        return root

    # ======================================================
    # THEME ADAPTERS
    # ======================================================

    def app_theme_surface(self):
        return Theme.SURFACE

    def app_theme_surface2(self):
        return Theme.SURFACE_2

    def app_theme_primary(self):
        return Theme.PRIMARY

    def app_theme_text(self):
        return Theme.TEXT

    def app_theme_secondary(self):
        return Theme.TEXT_SECONDARY

    def app_theme_muted(self):
        return Theme.TEXT_MUTED

    # ======================================================
    # PATH
    # ======================================================

    @property
    def base_dir(self):
        return Path(__file__).resolve().parent

    # ======================================================
    # STATS
    # ======================================================

    def refresh_stats(self):
        if not self.root:
            return

        stats = self.stats_service.get_summary()

        self.root.get_screen("home").set_stats(stats)
        self.root.get_screen("stats").set_stats(stats)

    # ======================================================
    # QUIZ
    # ======================================================

    def start_quiz(self):
        """Start a new quiz using the selected question count."""

        self.quiz_screen.set_question_count(
            self.question_count
        )

        self.quiz_screen.start_quiz()

        self.root.current = "quiz"

    # ======================================================
    # RESULT
    # ======================================================

    def _show_result(self, result):
        self.stats_service.record_quiz(
            result.score
        )

        screen = self.root.get_screen("result")

        screen.set_result(result)

        self.refresh_stats()

        self.root.current = "result"

    # ======================================================
    # NAVIGATION
    # ======================================================

    def show_stats(self):
        self.refresh_stats()
        self.root.current = "stats"

    def show_settings(self):
        self.root.current = "settings"

    def go_home(self):
        self.refresh_stats()
        self.root.current = "home"

    # ======================================================
    # SETTINGS
    # ======================================================

    def set_question_count(self, count):
        self.question_count = int(count)

        if hasattr(self, "quiz_screen"):
            self.quiz_screen.set_question_count(
                self.question_count
            )


if __name__ == "__main__":
    print("START")
    try:
        print("1: creating app")
        app = VerbMasterApp()

        print("2: app created")
        app.run()

        print("3: app finished")

    except Exception as e:
        print("ERROR:", repr(e))

        import traceback
        traceback.print_exc()

        input("Press Enter to exit...")