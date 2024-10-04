import pygame
pygame.font.init()

class pgUId:
  def __init__(self) -> None:
    pass

  class GUIDisplay:
    def __init__(self, scrollable=False, stacked=False, fill="white") -> None:
      self.fill = fill
      self.elements = []
      self.scrollable = scrollable
      self.stacked = stacked

      self.scroll_y = 0
      self.old_scroll_y = 0

      self.scroll_bar_size = 0
      self.scroll_bar_y = 0

    def clear_elements(self, tag=None):
      if tag is None:
        self.elements = []
      else:
        for element in self.elements:
          if element.tag == tag:
            self.elements.remove(element)
    
    def render(self, screen, screen_width=0, screen_height=0):
      screen.fill(self.fill)

      total_elements_height = sum(element.rect.height for element in self.elements)
      visible_height = screen_height

      if total_elements_height > visible_height:
          scroll_ratio = visible_height / total_elements_height
      else:
          scroll_ratio = 1

      self.scroll_bar_size = max(50, int(scroll_ratio * screen_height))

      y_pos = 0
      for element in self.elements:
          if self.scrollable and total_elements_height > visible_height:
              mouse_buttons = pygame.mouse.get_pressed()

              scroll_bar_background = pygame.draw.rect(screen, "#e2e2e2", (screen_width - 15, 0, 15, screen_height))

              self.scroll_bar_y = max(0, min(self.scroll_bar_y, screen_height - self.scroll_bar_size))

              scroll_bar = pygame.draw.rect(screen, "black", (screen_width - 10, self.scroll_bar_y, 10, self.scroll_bar_size))

              max_scroll = screen_height - self.scroll_bar_size
              self.scroll_y = -(self.scroll_bar_y / max_scroll) * (total_elements_height - visible_height)

              if scroll_bar.collidepoint(pygame.mouse.get_pos()):
                  if mouse_buttons[0]:
                      self.scroll_bar_y = pygame.mouse.get_pos()[1] - (self.scroll_bar_size // 2)

              if scroll_bar_background.collidepoint(pygame.mouse.get_pos()):
                  if mouse_buttons[0]:
                      self.scroll_bar_y = pygame.mouse.get_pos()[1] - (self.scroll_bar_size // 2)

          if self.stacked:
            element.render(screen, x=element.rect.x, y=y_pos, offset_y=self.scroll_y)

            y_pos += element.rect.height
          else:
            element.render(screen, offset_y=self.scroll_y)

  class elements:
    def __init__(self) -> None:
      pass
      
    class Button:
      def __init__(self, texture, clicked_texture, function, x=0, y=0, tag=None, width=None, height=None) -> None:
        self.texture = pygame.image.load(texture)
        self.clicked_texture = pygame.image.load(clicked_texture)
  
        if width is not None and height is not None:
          self.texture = pygame.transform.scale(self.texture, (width, height))
          self.clicked_texture = pygame.transform.scale(self.clicked_texture, (width, height))
        
        self.rect = self.texture.get_rect()
        self.rect.center = (x, y)
        
        self.x = x
        self.y = y

        self.tag = tag
  
        self.function = function
  
        self.clicked = False
        self.current_texture = self.texture

      def pack(self, gui_display):
        gui_display.elements.append(self)

      def config(self, texture=None, clicked_texture=None, tag=None, x=None, y=None):
        if texture is not None:
          self.texture = pygame.image.load(texture)
          self.texture = pygame.transform.scale(self.texture, (self.rect.width, self.rect.height))
        if clicked_texture is not None:
          self.clicked_texture = pygame.image.load(clicked_texture)
          self.clicked_texture = pygame.transform.scale(self.clicked_texture, (self.rect.width, self.rect.height))

        if x is not None:
          self.x = x
        if y is not None:
          self.y = y
        self.rect = self.texture.get_rect()
        self.rect.center = (self.x, self.y)

        if tag is not None:
          self.tag = tag
      
      def update_texture(self, texture):
        self.texture = pygame.image.load(texture)
      
      def check_click(self):
        checks = 0
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
          checks += 1
  
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
          checks += 1
  
        if checks == 2:
          if not self.clicked:
            self.current_texture = self.clicked_texture
            self.clicked = True
            return True
        else:
          self.current_texture = self.texture
          self.clicked = False
          return False
      
      def render(self, screen, x=None, y=None, offset_x=0, offset_y=0):
        if self.check_click():
            self.function()
        
        if x is not None or y is not None:
            if x is not None:
                self.rect.x = x + offset_x
            if y is not None:
                self.rect.y = y + offset_y
                
        screen.blit(self.current_texture, (self.rect.x, self.rect.y))
        
    class Label:
      def __init__(self, text, x=0, y=0, tag=None, font="Arial", font_size=24, color="black") -> None:
        self.x, self.y = x, y

        self.tag = tag
        
        self.font_size = font_size
        self.color = color
        self.font_name = font
        self.font = pygame.font.SysFont(font, self.font_size)
        self.raw_text = text
        self.text = self.font.render(text, True, self.color)
        self.rect = self.text.get_rect()
        self.rect.center = (self.x, self.y)

      def pack(self, gui_display):
        if self in gui_display.elements:
          gui_display.elements.remove(self)
        
        gui_display.elements.append(self)

      def config(self, text=None, font=None, font_size=None, color=None, tag=None, x=None, y=None):
        
        self.font = pygame.font.SysFont(font if font is not None else self.font_name, font_size if font_size is not None else self.font_size)

        self.text = self.font.render(text if text is not None else self.raw_text, True, color if color is not None else self.color)

        if text is not None:
          self.raw_text = text

        if x is not None and y is not None:
          self.x, self.y = x, y
        self.rect = self.text.get_rect()
        self.rect.center = (self.x, self.y)

        if tag is not None:
          self.tag = tag
      
      def update_text(self, text, font=None, font_size=24, color="black"):
        if font is not None:
          self.font = pygame.font.SysFont(font, font_size)
        self.text = self.font.render(text, True, color)
        self.rect = self.text.get_rect()
        self.rect.center = (self.x, self.y)
      
      def render(self, screen, x=None, y=None, offset_x=0, offset_y=0):
        if x is not None or y is not None:
            if x is not None:
                self.rect.x = x + offset_x
            if y is not None:
                self.rect.y = y + offset_y
                
        screen.blit(self.text, (self.rect.x, self.rect.y))

pgUId = pgUId()
