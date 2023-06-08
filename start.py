import pygame


# overall class for start screen
class Start:
    def __init__(self, screen):
        pygame.init()
        self.screen = screen
        pygame.display.set_caption('Space exploration!')
        pygame.font.init()
        self.button_font = pygame.font.SysFont("Helvetica", 48)
        self.bg = pygame.image.load("Screen Assets/start.png")
        # scale the text box parts
        self.bg = pygame.transform.scale(self.bg, (self.screen.get_width(), self.screen.get_height()))
        self.input_rect = pygame.Rect(self.screen.get_width() // 2 - 320, self.screen.get_height() - 250, 623, 58)
        self.cursor_rect = pygame.Rect(self.input_rect.x + 5, self.input_rect.y + 5, 2, self.input_rect.height - 10)
        # conditions
        self.active = False
        self.cursor_visible = True
        self.press = False
        # timers
        self.cursor_blink = 0
        self.delete_timer = 0
        self.hold_timer = 0
        self.select_timer = 0
        # string for user input and pos of mouse cursor on text
        self.user_text = ""
        self.selected_pos = 0
        self.select = 0
        self.clock = pygame.time.Clock()

    # calculate where the selected pos is based on the mouse
    def calculate_selected_pos(self, mouse_x):
        char_widths = [self.button_font.size(self.user_text[:i + 1])[0] for i in range(len(self.user_text))]
        for i, char_width in enumerate(char_widths):
            if mouse_x < self.input_rect.x + 5 + char_width:
                return i
        return len(self.user_text)

    def run(self):
        run = True
        while run:
            for event in pygame.event.get():
                # Check if the user clicked the close button or pressed the Escape key
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    exit()
                # Check if the user clicked the input box
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_rect.collidepoint(event.pos):
                        self.active = True
                        self.selected_pos = self.calculate_selected_pos(event.pos[0])
                    else:
                        self.active = False
                # Handle keyboard input
                elif event.type == pygame.KEYDOWN and self.active:
                    if event.key == pygame.K_RETURN:
                        run = False
                    elif event.key == pygame.K_BACKSPACE:
                        # Delete the character to the left of the cursor
                        if self.selected_pos > 0:
                            self.user_text = self.user_text[:self.selected_pos - 1] + self.user_text[self.selected_pos:]
                            self.selected_pos -= 1
                        self.delete_timer = pygame.time.get_ticks() + 300
                    elif event.key == pygame.K_LEFT:
                        # Move the cursor one position to the left
                        if self.selected_pos > 0:
                            self.selected_pos -= 1
                            self.select_timer = pygame.time.get_ticks() + 300
                    elif event.key == pygame.K_RIGHT:
                        # Move the cursor one position to the right
                        if self.selected_pos < len(self.user_text):
                            self.selected_pos += 1
                            self.select_timer = pygame.time.get_ticks() + 300
                    elif self.button_font.size(self.user_text + event.unicode)[0] > self.input_rect.width - 10:
                        # Check if adding the new character would exceed the input box width
                        continue
                    else:
                        # Insert the typed character at the cursor position
                        self.user_text = self.user_text[:self.selected_pos] + event.unicode + self.user_text[
                                                                                              self.selected_pos:]
                        self.select = len(self.user_text)
                        self.selected_pos += 1
                        self.press = True
                        self.hold_timer = pygame.time.get_ticks() + 500
                elif event.type == pygame.KEYUP:
                    self.press = False

            if pygame.key.get_pressed()[pygame.K_BACKSPACE] and self.active:
                # Handle continuous backspace key press
                if self.delete_timer < pygame.time.get_ticks():
                    if self.selected_pos > 0:
                        self.user_text = self.user_text[:self.selected_pos - 1] + self.user_text[self.selected_pos:]
                        self.selected_pos -= 1
                    self.delete_timer = pygame.time.get_ticks() + 50
            if self.press and self.hold_timer < pygame.time.get_ticks():
                # Handle continuous key press for characters
                if len(self.user_text) > 0 and 0 < self.select <= len(self.user_text):
                    if self.selected_pos > len(self.user_text):
                        last_chr = self.user_text[self.selected_pos - 2]
                    else:
                        last_chr = self.user_text[self.selected_pos - 1]

                    if not self.button_font.size(self.user_text + last_chr)[0] > self.input_rect.width - 10:
                        self.user_text = self.user_text[:self.selected_pos] + last_chr + self.user_text[
                                                                                         self.selected_pos:]
                        self.selected_pos += 1
                        self.hold_timer = pygame.time.get_ticks() + 50

            if pygame.key.get_pressed()[pygame.K_RIGHT] and self.select_timer < pygame.time.get_ticks():
                # Handle continuous right arrow key press
                if self.selected_pos < len(self.user_text):
                    self.selected_pos += 1
                    self.select_timer = pygame.time.get_ticks() + 50
            if pygame.key.get_pressed()[pygame.K_LEFT] and self.select_timer < pygame.time.get_ticks():
                # Handle continuous left arrow key press
                if self.selected_pos > 0:
                    self.selected_pos -= 1
                    self.select_timer = pygame.time.get_ticks() + 50

            # Render the screen
            self.screen.blit(self.bg, (0, 0))
            pygame.draw.rect(self.screen, pygame.Color("white"), self.input_rect)

            text_surface = self.button_font.render(self.user_text, True, (0, 0, 0))
            self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y))

            # Handle cursor blinking
            self.cursor_blink += self.clock.get_time()
            if self.cursor_blink >= 500:
                self.cursor_visible = not self.cursor_visible
                self.cursor_blink = 0

            if self.active and self.cursor_visible:
                # Display the cursor at the current cursor position
                cursor_x = self.input_rect.x + 5 + self.button_font.size(self.user_text[:self.selected_pos])[0]
                self.cursor_rect.x = cursor_x
                pygame.draw.rect(self.screen, (0, 0, 0), self.cursor_rect)

            pygame.display.update()
            self.clock.tick(60)

        return self.user_text
