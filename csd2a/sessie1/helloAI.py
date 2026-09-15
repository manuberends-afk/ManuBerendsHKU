
import random
import time
import os
import pygame


# ============================================================
# CONFIGURATIE
# ============================================================

SOUND_FOLDER = "Sounds"

INSTRUMENTS = [
    "kick",
    "snare",
    "closedHat",
    "openHat",
    "samba",
    "woodTick",
    "bongo",
    "conga",
]


# ============================================================
# AUDIO
# ============================================================

def initialize_audio():
    pygame.mixer.init(
        frequency=44100,
        size=-16,
        channels=2,
        buffer=512
    )


def load_sounds(instruments):
    """
    Laadt alle WAV-files één keer in het geheugen.
    """

    sounds = {}

    print("\n--- WAV samples laden ---")

    for instrument in instruments:

        filename = os.path.join(
            SOUND_FOLDER,
            instrument + ".wav"
        )

        if not os.path.exists(filename):
            print(f"WARNING: {filename} bestaat niet.")
            continue

        try:
            sounds[instrument] = pygame.mixer.Sound(
                filename
            )

            print(f"Geladen: {filename}")

        except pygame.error as error:
            print(
                f"Fout bij laden van {filename}: "
                f"{error}"
            )

    print()

    return sounds


def play_sound(sounds, instrument):
    """
    Speelt een geladen sample af.
    """

    sound = sounds.get(instrument)

    if sound is not None:
        sound.play()


# ============================================================
# BEAT GENERATION
# ============================================================

def generate_beat(
    length,
    restrictions,
    chance
):
    """
    Genereert één beat.

    restriction:

        1    = altijd hit
        0    = nooit hit
        None = random
    """

    beat = []

    for restriction in restrictions:

        if restriction == 1:
            beat.append(1)

        elif restriction == 0:
            beat.append(0)

        else:
            if random.random() < chance:
                beat.append(1)
            else:
                beat.append(0)

    return beat


def score_beat(beat):
    """
    Geeft een eenvoudige muzikale score.

    Dit is geen echte AI-score.
    Het probeert vooral interessante patronen
    te selecteren.
    """

    if not beat:
        return -100

    length = len(beat)

    hits = sum(beat)

    density = hits / length

    score = 0

    # --------------------------------------------------------
    # Lege beats afstraffen
    # --------------------------------------------------------

    if hits == 0:
        score -= 20

    # --------------------------------------------------------
    # Niet te leeg / niet te vol
    # --------------------------------------------------------

    if 0.20 <= density <= 0.70:
        score += 10

    # --------------------------------------------------------
    # Variatie belonen
    # --------------------------------------------------------

    for i in range(1, length):

        if beat[i] != beat[i - 1]:
            score += 1

    # --------------------------------------------------------
    # Lange runs zoeken
    # --------------------------------------------------------

    longest_run = 0
    current_run = 0
    previous = None

    for value in beat:

        if value == previous:
            current_run += 1
        else:
            current_run = 1

        previous = value

        longest_run = max(
            longest_run,
            current_run
        )

    if longest_run >= 6:
        score -= 5

    if longest_run >= 10:
        score -= 10

    return score


def generate_many_beats(
    length,
    restrictions,
    chance,
    amount_to_keep,
    attempts
):
    """
    Genereert veel unieke beats en bewaart
    alleen de best scorende.
    """

    candidates = {}

    for _ in range(attempts):

        beat = generate_beat(
            length,
            restrictions,
            chance
        )

        key = tuple(beat)

        # Dubbele beat overslaan
        if key in candidates:
            continue

        candidates[key] = {
            "steps": beat,
            "score": score_beat(beat)
        }

    sorted_candidates = sorted(
        candidates.values(),
        key=lambda item: item["score"],
        reverse=True
    )

    return sorted_candidates[
        :amount_to_keep
    ]


# ============================================================
# GUI
# ============================================================

class BeatGeneratorGUI:

    # --------------------------------------------------------
    # Window
    # --------------------------------------------------------

    WINDOW_WIDTH = 1400
    WINDOW_HEIGHT = 900

    TOP_HEIGHT = 180

    LEFT_WIDTH = 180

    CELL_SIZE = 38
    CELL_GAP = 3

    # --------------------------------------------------------
    # Kleuren
    # --------------------------------------------------------

    BG = (25, 25, 30)

    PANEL = (38, 38, 45)

    TEXT = (235, 235, 235)

    MUTED = (155, 155, 165)

    BORDER = (90, 90, 100)

    HIT_COLOR = (65, 170, 90)

    NO_HIT_COLOR = (190, 65, 65)

    RANDOM_COLOR = (70, 105, 170)

    DISABLED_COLOR = (65, 65, 72)

    BUTTON = (70, 75, 90)

    BUTTON_HOVER = (90, 95, 115)

    PLAYHEAD_COLOR = (255, 220, 80)

    # ========================================================
    # INITIALISATIE
    # ========================================================

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode(
            (
                self.WINDOW_WIDTH,
                self.WINDOW_HEIGHT
            ),
            pygame.RESIZABLE
        )

        pygame.display.set_caption(
            "Random Beat Generator"
        )

        self.clock = pygame.time.Clock()

        # ----------------------------------------------------
        # Fonts
        # ----------------------------------------------------

        self.font = pygame.font.SysFont(
            "arial",
            18
        )

        self.small_font = pygame.font.SysFont(
            "arial",
            14
        )

        self.big_font = pygame.font.SysFont(
            "arial",
            28,
            bold=True
        )

        # ----------------------------------------------------
        # State
        # ----------------------------------------------------

        self.running = True

        self.length = 16

        self.amount_to_keep = 20

        self.attempts = 5000

        self.bpm = 120

        # ----------------------------------------------------
        # Random chance per instrument
        # ----------------------------------------------------

        self.chances = {
            instrument: 0.5
            for instrument in INSTRUMENTS
        }

        # ----------------------------------------------------
        # Instrument ON/OFF
        # ----------------------------------------------------

        self.active = {
            instrument: True
            for instrument in INSTRUMENTS
        }

        # ----------------------------------------------------
        # Restricties
        #
        # None = -
        # 1    = hit
        # 0    = geen hit
        # ----------------------------------------------------

        self.restrictions = {
            instrument: [None] * self.length
            for instrument in INSTRUMENTS
        }

        # ----------------------------------------------------
        # Gegenereerde beats
        # ----------------------------------------------------

        self.beats = {}

        # ----------------------------------------------------
        # Playback
        # ----------------------------------------------------

        self.playing = False

        self.play_loop = True

        self.current_beat = 0

        self.current_step = 0

        self.next_step_time = 0

        # ----------------------------------------------------
        # GUI
        # ----------------------------------------------------

        self.buttons = []

        self.scroll_y = 0

        self.status = (
            "Klik op de grid om restricties in te stellen."
        )

        self.sounds = {}

    # ========================================================
    # TEXT TEKENEN
    # ========================================================

    def draw_text(
        self,
        text,
        x,
        y,
        font=None,
        color=None,
        center=False
    ):

        if font is None:
            font = self.font

        if color is None:
            color = self.TEXT

        surface = font.render(
            str(text),
            True,
            color
        )

        rect = surface.get_rect()

        if center:
            rect.center = (
                x,
                y
            )
        else:
            rect.topleft = (
                x,
                y
            )

        self.screen.blit(
            surface,
            rect
        )

        return rect

    # ========================================================
    # BUTTON
    # ========================================================

    def draw_button(
        self,
        text,
        rect,
        action,
        enabled=True
    ):

        mouse_pos = pygame.mouse.get_pos()

        hovered = rect.collidepoint(
            mouse_pos
        )

        if not enabled:

            color = self.DISABLED_COLOR

        elif hovered:

            color = self.BUTTON_HOVER

        else:

            color = self.BUTTON

        pygame.draw.rect(
            self.screen,
            color,
            rect,
            border_radius=6
        )

        pygame.draw.rect(
            self.screen,
            self.BORDER,
            rect,
            1,
            border_radius=6
        )

        self.draw_text(
            text,
            rect.centerx,
            rect.centery,
            center=True,
            color=(
                self.TEXT
                if enabled
                else self.MUTED
            )
        )

        self.buttons.append(
            (
                rect,
                action,
                enabled
            )
        )

    # ========================================================
    # GRID POSITIES
    # ========================================================

    def get_grid_x(self, step):

        return (
            self.LEFT_WIDTH
            + step * (
                self.CELL_SIZE
                + self.CELL_GAP
            )
            + 20
        )

    def get_grid_y(
        self,
        instrument_index
    ):

        return (
            self.TOP_HEIGHT
            + instrument_index * (
                self.CELL_SIZE
                + self.CELL_GAP
                + 12
            )
            + self.scroll_y
        )

    # ========================================================
    # RESTRICTIE WEERGAVE
    # ========================================================

    def restriction_color(
        self,
        value
    ):

        if value == 1:
            return self.HIT_COLOR

        if value == 0:
            return self.NO_HIT_COLOR

        return self.RANDOM_COLOR

    def restriction_text(
        self,
        value
    ):

        if value == 1:
            return "1"

        if value == 0:
            return "0"

        return "-"

    # ========================================================
    # GRID TEKENEN
    # ========================================================

    def draw_grid(self):

        # ----------------------------------------------------
        # Step nummers
        # ----------------------------------------------------

        for step in range(self.length):

            x = self.get_grid_x(
                step
            )

            # Accent bij elke kwartnoot
            if step % 4 == 0:

                pygame.draw.line(
                    self.screen,
                    self.BORDER,
                    (
                        x - 5,
                        self.TOP_HEIGHT - 15
                    ),
                    (
                        x - 5,
                        self.WINDOW_HEIGHT
                    ),
                    1
                )

            self.draw_text(
                step + 1,
                x + self.CELL_SIZE // 2,
                self.TOP_HEIGHT - 28,
                font=self.small_font,
                color=self.MUTED,
                center=True
            )

        # ----------------------------------------------------
        # Instrumenten
        # ----------------------------------------------------

        for instrument_index, instrument in enumerate(
            INSTRUMENTS
        ):

            y = self.get_grid_y(
                instrument_index
            )

            # Buiten scherm
            if (
                y + self.CELL_SIZE
                < self.TOP_HEIGHT
            ):
                continue

            if y > self.WINDOW_HEIGHT:
                continue

            # ------------------------------------------------
            # Instrument naam
            # ------------------------------------------------

            self.draw_text(
                instrument,
                20,
                y + self.CELL_SIZE // 2,
                center=False
            )

            # ------------------------------------------------
            # ON/OFF
            # ------------------------------------------------

            toggle_rect = pygame.Rect(
                120,
                y,
                45,
                self.CELL_SIZE
            )

            toggle_color = (
                self.HIT_COLOR
                if self.active[instrument]
                else self.DISABLED_COLOR
            )

            pygame.draw.rect(
                self.screen,
                toggle_color,
                toggle_rect,
                border_radius=5
            )

            self.draw_text(
                (
                    "ON"
                    if self.active[instrument]
                    else "OFF"
                ),
                toggle_rect.centerx,
                toggle_rect.centery,
                font=self.small_font,
                center=True
            )

            # ------------------------------------------------
            # Random chance
            # ------------------------------------------------

            self.draw_text(
                f"{self.chances[instrument]:.2f}",
                175,
                y + 10,
                font=self.small_font,
                color=self.MUTED
            )

            # ------------------------------------------------
            # Grid
            # ------------------------------------------------

            for step in range(self.length):

                x = self.get_grid_x(
                    step
                )

                rect = pygame.Rect(
                    x,
                    y,
                    self.CELL_SIZE,
                    self.CELL_SIZE
                )

                value = self.restrictions[
                    instrument
                ][step]

                color = self.restriction_color(
                    value
                )

                if not self.active[instrument]:

                    color = (
                        self.DISABLED_COLOR
                    )

                pygame.draw.rect(
                    self.screen,
                    color,
                    rect,
                    border_radius=4
                )

                pygame.draw.rect(
                    self.screen,
                    self.BORDER,
                    rect,
                    1,
                    border_radius=4
                )

                if self.active[instrument]:

                    self.draw_text(
                        self.restriction_text(
                            value
                        ),
                        rect.centerx,
                        rect.centery,
                        font=self.small_font,
                        center=True
                    )

    # ========================================================
    # HEADER
    # ========================================================

    def draw_header(self):

        pygame.draw.rect(
            self.screen,
            self.PANEL,
            (
                0,
                0,
                self.WINDOW_WIDTH,
                self.TOP_HEIGHT
            )
        )

        self.draw_text(
            "RANDOM BEAT GENERATOR",
            20,
            15,
            font=self.big_font
        )

        self.draw_text(
            "Klik:  -  →  1  →  0  →  -",
            20,
            55,
            color=self.MUTED
        )

        # ----------------------------------------------------
        # Instellingen
        # ----------------------------------------------------

        self.draw_text(
            f"Steps: {self.length}",
            20,
            100
        )

        self.draw_text(
            f"Bewaren: {self.amount_to_keep}",
            150,
            100
        )

        self.draw_text(
            f"Pogingen: {self.attempts}",
            280,
            100
        )

        self.draw_text(
            f"BPM: {self.bpm}",
            430,
            100
        )

        # ----------------------------------------------------
        # Buttons
        # ----------------------------------------------------

        self.draw_button(
            "Generate",
            pygame.Rect(
                550,
                85,
                120,
                42
            ),
            "generate"
        )

        self.draw_button(
            "Play",
            pygame.Rect(
                680,
                85,
                100,
                42
            ),
            "play",
            enabled=bool(self.beats)
        )

        self.draw_button(
            "Stop",
            pygame.Rect(
                790,
                85,
                100,
                42
            ),
            "stop"
        )

        self.draw_button(
            "Clear",
            pygame.Rect(
                900,
                85,
                100,
                42
            ),
            "clear"
        )

        # ----------------------------------------------------
        # Legend
        # ----------------------------------------------------

        legend_y = 145

        legend = [
            ("1", self.HIT_COLOR),
            ("0", self.NO_HIT_COLOR),
            ("-", self.RANDOM_COLOR)
        ]

        x = 20

        for label, color in legend:

            pygame.draw.rect(
                self.screen,
                color,
                (
                    x,
                    legend_y,
                    20,
                    20
                ),
                border_radius=3
            )

            self.draw_text(
                label,
                x + 10,
                legend_y + 10,
                font=self.small_font,
                center=True
            )

            x += 35

        self.draw_text(
            self.status,
            150,
            legend_y + 2,
            font=self.small_font,
            color=self.MUTED
        )

    # ========================================================
    # ONDERSTE INFO
    # ========================================================

    def draw_footer(self):

        footer_y = (
            self.WINDOW_HEIGHT - 80
        )

        pygame.draw.rect(
            self.screen,
            self.PANEL,
            (
                0,
                footer_y,
                self.WINDOW_WIDTH,
                80
            )
        )

        self.draw_text(
            "ON/OFF = instrument aan/uit",
            20,
            footer_y + 10,
            font=self.small_font,
            color=self.MUTED
        )

        self.draw_text(
            "SPACE = play/stop    G = generate    R = random restricties    ESC = exit",
            20,
            footer_y + 35,
            font=self.small_font,
            color=self.MUTED
        )

    # ========================================================
    # GENEREREN
    # ========================================================

    def generate(self):

        self.stop_playback()

        self.status = (
            "Beats genereren..."
        )

        pygame.display.flip()

        self.beats = {}

        for instrument in INSTRUMENTS:

            if not self.active[instrument]:
                continue

            self.beats[instrument] = (
                generate_many_beats(
                    length=self.length,
                    restrictions=(
                        self.restrictions[
                            instrument
                        ]
                    ),
                    chance=(
                        self.chances[
                            instrument
                        ]
                    ),
                    amount_to_keep=(
                        self.amount_to_keep
                    ),
                    attempts=self.attempts
                )
            )

        self.current_beat = 0

        self.current_step = 0

        total = sum(
            len(value)
            for value in self.beats.values()
        )

        self.status = (
            f"Klaar: {total} beats gegenereerd."
        )

    # ========================================================
    # PLAYBACK STARTEN
    # ========================================================

    def start_playback(self):

        if not self.beats:

            self.status = (
                "Genereer eerst beats."
            )

            return

        self.playing = True

        self.current_beat = 0

        self.current_step = 0

        self.next_step_time = (
            time.perf_counter()
        )

        self.status = "Playing..."

    # ========================================================
    # PLAYBACK STOPPEN
    # ========================================================

    def stop_playback(self):

        self.playing = False

        if self.status == "Playing...":
            self.status = "Playback gestopt."

    # ========================================================
    # PLAYBACK UPDATE
    # ========================================================

    def playback_update(self):

        if not self.playing:
            return

        now = time.perf_counter()

        if now < self.next_step_time:
            return

        # ----------------------------------------------------
        # Maximum aantal beats
        # ----------------------------------------------------

        max_beats = max(
            (
                len(value)
                for value in self.beats.values()
            ),
            default=0
        )

        if max_beats == 0:

            self.stop_playback()

            return

        # ----------------------------------------------------
        # Speel huidige step
        # ----------------------------------------------------

        for instrument, instrument_beats in (
            self.beats.items()
        ):

            if not instrument_beats:
                continue

            beat = instrument_beats[
                self.current_beat
                % len(instrument_beats)
            ]

            if beat["steps"][
                self.current_step
            ] == 1:

                play_sound(
                    self.sounds,
                    instrument
                )

        # ----------------------------------------------------
        # Volgende step
        # ----------------------------------------------------

        self.current_step += 1

        if self.current_step >= self.length:

            self.current_step = 0

            self.current_beat += 1

            if self.current_beat >= max_beats:

                if self.play_loop:

                    self.current_beat = 0

                else:

                    self.stop_playback()

                    return

        # ----------------------------------------------------
        # Timing
        # ----------------------------------------------------

        seconds_per_quarter = (
            60.0 / self.bpm
        )

        steps_per_quarter = (
            self.length / 4
        )

        seconds_per_step = (
            seconds_per_quarter
            / steps_per_quarter
        )

        self.next_step_time = (
            now + seconds_per_step
        )

    # ========================================================
    # GRID CLICK
    # ========================================================

    def handle_grid_click(
        self,
        mouse_pos
    ):

        for instrument_index, instrument in enumerate(
            INSTRUMENTS
        ):

            y = self.get_grid_y(
                instrument_index
            )

            # ------------------------------------------------
            # ON/OFF
            # ------------------------------------------------

            toggle_rect = pygame.Rect(
                120,
                y,
                45,
                self.CELL_SIZE
            )

            if toggle_rect.collidepoint(
                mouse_pos
            ):

                self.active[
                    instrument
                ] = not self.active[
                    instrument
                ]

                self.beats = {}

                self.status = (
                    instrument
                    + ": "
                    + (
                        "ON"
                        if self.active[
                            instrument
                        ]
                        else "OFF"
                    )
                )

                return

            # ------------------------------------------------
            # Restriction grid
            # ------------------------------------------------

            if not self.active[
                instrument
            ]:
                continue

            for step in range(
                self.length
            ):

                x = self.get_grid_x(
                    step
                )

                rect = pygame.Rect(
                    x,
                    y,
                    self.CELL_SIZE,
                    self.CELL_SIZE
                )

                if rect.collidepoint(
                    mouse_pos
                ):

                    current = (
                        self.restrictions[
                            instrument
                        ][step]
                    )

                    # ----------------------------------------
                    # - -> 1 -> 0 -> -
                    # ----------------------------------------

                    if current is None:

                        new_value = 1

                    elif current == 1:

                        new_value = 0

                    else:

                        new_value = None

                    self.restrictions[
                        instrument
                    ][step] = new_value

                    # Oude beats zijn nu niet meer geldig
                    self.beats = {}

                    self.status = (
                        f"{instrument} "
                        f"step {step + 1}: "
                        f"{self.restriction_text(new_value)}"
                    )

                    return

    # ========================================================
    # BUTTON ACTIES
    # ========================================================

    def handle_button(
        self,
        action
    ):

        if action == "generate":

            self.generate()

        elif action == "play":

            self.start_playback()

        elif action == "stop":

            self.stop_playback()

        elif action == "clear":

            self.stop_playback()

            for instrument in INSTRUMENTS:

                self.restrictions[
                    instrument
                ] = [None] * self.length

            self.beats = {}

            self.status = (
                "Alle restricties gewist."
            )

    # ========================================================
    # KEYBOARD
    # ========================================================

    def handle_key(
        self,
        event
    ):

        # ----------------------------------------------------
        # SPACE
        # ----------------------------------------------------

        if event.key == pygame.K_SPACE:

            if self.playing:

                self.stop_playback()

            else:

                self.start_playback()

        # ----------------------------------------------------
        # G
        # ----------------------------------------------------

        elif event.key == pygame.K_g:

            self.generate()

        # ----------------------------------------------------
        # R
        # ----------------------------------------------------

        elif event.key == pygame.K_r:

            for instrument in INSTRUMENTS:

                if not self.active[
                    instrument
                ]:
                    continue

                for step in range(
                    self.length
                ):

                    self.restrictions[
                        instrument
                    ][step] = random.choice(
                        [
                            None,
                            None,
                            None,
                            1,
                            0
                        ]
                    )

            self.beats = {}

            self.status = (
                "Restricties willekeurig ingevuld."
            )

        # ----------------------------------------------------
        # ESC
        # ----------------------------------------------------

        elif event.key == pygame.K_ESCAPE:

            self.running = False

    # ========================================================
    # EVENTS
    # ========================================================

    def handle_events(self):

        for event in pygame.event.get():

            # ------------------------------------------------
            # Window sluiten
            # ------------------------------------------------

            if event.type == pygame.QUIT:

                self.running = False

            # ------------------------------------------------
            # Resize
            # ------------------------------------------------

            elif event.type == pygame.VIDEORESIZE:

                self.screen = pygame.display.set_mode(
                    event.size,
                    pygame.RESIZABLE
                )

                self.WINDOW_WIDTH = (
                    self.screen.get_width()
                )

                self.WINDOW_HEIGHT = (
                    self.screen.get_height()
                )

            # ------------------------------------------------
            # Keyboard
            # ------------------------------------------------

            elif event.type == pygame.KEYDOWN:

                self.handle_key(
                    event
                )

            # ------------------------------------------------
            # Mouse
            # ------------------------------------------------

            elif event.type == pygame.MOUSEBUTTONDOWN:

                # Scroll omhoog
                if event.button == 4:

                    self.scroll_y += 30

                # Scroll omlaag
                elif event.button == 5:

                    self.scroll_y -= 30

                # Linkermuisknop
                elif event.button == 1:

                    clicked_button = False

                    # Eerst buttons
                    for (
                        rect,
                        action,
                        enabled
                    ) in self.buttons:

                        if (
                            enabled
                            and rect.collidepoint(
                                event.pos
                            )
                        ):

                            self.handle_button(
                                action
                            )

                            clicked_button = True

                            break

                    # Anders grid
                    if not clicked_button:

                        if (
                            event.pos[1]
                            < self.WINDOW_HEIGHT - 80
                        ):

                            self.handle_grid_click(
                                event.pos
                            )

        # ----------------------------------------------------
        # Scroll begrenzen
        # ----------------------------------------------------

        content_height = (
            self.TOP_HEIGHT
            + len(INSTRUMENTS)
            * (
                self.CELL_SIZE
                + self.CELL_GAP
                + 12
            )
            + 30
        )

        visible_height = (
            self.WINDOW_HEIGHT - 80
        )

        if content_height > visible_height:

            max_scroll = -(
                content_height
                - visible_height
            )

        else:

            max_scroll = 0

        self.scroll_y = min(
            0,
            max(
                max_scroll,
                self.scroll_y
            )
        )

    # ========================================================
    # TEKENEN
    # ========================================================

    def draw(self):

        self.screen.fill(
            self.BG
        )

        self.buttons = []

        self.draw_header()

        self.draw_grid()

        self.draw_footer()

        # ----------------------------------------------------
        # Playback playhead
        # ----------------------------------------------------

        if self.playing:

            x = self.get_grid_x(
                self.current_step
            )

            pygame.draw.rect(
                self.screen,
                self.PLAYHEAD_COLOR,
                (
                    x - 2,
                    self.TOP_HEIGHT - 5,
                    self.CELL_SIZE + 4,
                    self.WINDOW_HEIGHT
                    - self.TOP_HEIGHT
                    - 80
                ),
                2
            )

        pygame.display.flip()

    # ========================================================
    # RUN
    # ========================================================

    def run(self):

        self.sounds = load_sounds(
            INSTRUMENTS
        )

        while self.running:

            self.handle_events()

            self.playback_update()

            self.draw()

            # 120 FPS GUI
            self.clock.tick(120)

        pygame.quit()


# ============================================================
# MAIN
# ============================================================

def main():

    initialize_audio()

    app = BeatGeneratorGUI()

    app.run()


if __name__ == "__main__":
    main()
