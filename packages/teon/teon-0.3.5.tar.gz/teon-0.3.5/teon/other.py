import pygame

_key_map = {
    "a": pygame.K_a,
    "b": pygame.K_b,
    "c": pygame.K_c,
    "d": pygame.K_d,
    "e": pygame.K_e,
    "f": pygame.K_f,
    "g": pygame.K_g,
    "h": pygame.K_h,
    "i": pygame.K_i,
    "j": pygame.K_j,
    "k": pygame.K_k,
    "l": pygame.K_l,
    "m": pygame.K_m,
    "n": pygame.K_n,
    "o": pygame.K_o,
    "p": pygame.K_p,
    "q": pygame.K_q,
    "r": pygame.K_r,
    "s": pygame.K_s,
    "t": pygame.K_t,
    "u": pygame.K_u,
    "v": pygame.K_v,
    "w": pygame.K_w,
    "x": pygame.K_x,
    "y": pygame.K_y,
    "z": pygame.K_z,

    "0": pygame.K_0,
    "1": pygame.K_1,
    "2": pygame.K_2,
    "3": pygame.K_3,
    "4": pygame.K_4,
    "5": pygame.K_5,
    "6": pygame.K_6,
    "7": pygame.K_7,
    "8": pygame.K_8,
    "9": pygame.K_9,

    "f1": pygame.K_F1,
    "f2": pygame.K_F2,
    "f3": pygame.K_F3,
    "f4": pygame.K_F4,
    "f5": pygame.K_F5,
    "f6": pygame.K_F6,
    "f7": pygame.K_F7,
    "f8": pygame.K_F8,
    "f9": pygame.K_F9,
    "f10": pygame.K_F10,
    "f11": pygame.K_F11,
    "f12": pygame.K_F12,

    "left shift": pygame.K_LSHIFT,
    "right shift": pygame.K_RSHIFT,
    "left ctrl": pygame.K_LCTRL,
    "right ctrl": pygame.K_RCTRL,
    "left alt": pygame.K_LALT,
    "right alt": pygame.K_RALT,
    "left meta": pygame.K_LMETA,
    "right meta": pygame.K_RMETA,

    "space": pygame.K_SPACE,
    "enter": pygame.K_RETURN,
    "escape": pygame.K_ESCAPE,
    "backspace": pygame.K_BACKSPACE,
    "tab": pygame.K_TAB,
    "caps lock": pygame.K_CAPSLOCK,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,

    "insert": pygame.K_INSERT,
    "delete": pygame.K_DELETE,
    "home": pygame.K_HOME,
    "end": pygame.K_END,
    "page up": pygame.K_PAGEUP,
    "page down": pygame.K_PAGEDOWN,

    "comma": pygame.K_COMMA,
    "period": pygame.K_PERIOD,
    "slash": pygame.K_SLASH,
    "semicolon": pygame.K_SEMICOLON,
    "quote": pygame.K_QUOTE,
    "left bracket": pygame.K_LEFTBRACKET,
    "right bracket": pygame.K_RIGHTBRACKET,
    "backslash": pygame.K_BACKSLASH,
    "minus": pygame.K_MINUS,
    "equals": pygame.K_EQUALS,
    "backquote": pygame.K_BACKQUOTE,

    "numpad 0": pygame.K_KP0,
    "numpad 1": pygame.K_KP1,
    "numpad 2": pygame.K_KP2,
    "numpad 3": pygame.K_KP3,
    "numpad 4": pygame.K_KP4,
    "numpad 5": pygame.K_KP5,
    "numpad 6": pygame.K_KP6,
    "numpad 7": pygame.K_KP7,
    "numpad 8": pygame.K_KP8,
    "numpad 9": pygame.K_KP9,
    "numpad period": pygame.K_KP_PERIOD,
    "numpad divide": pygame.K_KP_DIVIDE,
    "numpad multiply": pygame.K_KP_MULTIPLY,
    "numpad minus": pygame.K_KP_MINUS,
    "numpad plus": pygame.K_KP_PLUS,
    "numpad enter": pygame.K_KP_ENTER,
}

_yek_map = {
    pygame.K_a: "a",
    pygame.K_b: "b",
    pygame.K_c: "c",
    pygame.K_d: "d",
    pygame.K_e: "e",
    pygame.K_f: "f",
    pygame.K_g: "g",
    pygame.K_h: "h",
    pygame.K_i: "i",
    pygame.K_j: "j",
    pygame.K_k: "k",
    pygame.K_l: "l",
    pygame.K_m: "m",
    pygame.K_n: "n",
    pygame.K_o: "o",
    pygame.K_p: "p",
    pygame.K_q: "q",
    pygame.K_r: "r",
    pygame.K_s: "s",
    pygame.K_t: "t",
    pygame.K_u: "u",
    pygame.K_v: "v",
    pygame.K_w: "w",
    pygame.K_x: "x",
    pygame.K_y: "y",
    pygame.K_z: "z",

    pygame.K_0: "0",
    pygame.K_1: "1",
    pygame.K_2: "2",
    pygame.K_3: "3",
    pygame.K_4: "4",
    pygame.K_5: "5",
    pygame.K_6: "6",
    pygame.K_7: "7",
    pygame.K_8: "8",
    pygame.K_9: "9",

    pygame.K_F1: "f1",
    pygame.K_F2: "f2",
    pygame.K_F3: "f3",
    pygame.K_F4: "f4",
    pygame.K_F5: "f5",
    pygame.K_F6: "f6",
    pygame.K_F7: "f7",
    pygame.K_F8: "f8",
    pygame.K_F9: "f9",
    pygame.K_F10: "f10",
    pygame.K_F11: "f11",
    pygame.K_F12: "f12",

    pygame.K_LSHIFT: "left shift",
    pygame.K_RSHIFT: "right shift",
    pygame.K_LCTRL: "left ctrl",
    pygame.K_RCTRL: "right ctrl",
    pygame.K_LALT: "left alt",
    pygame.K_RALT: "right alt",
    pygame.K_LMETA: "left meta",
    pygame.K_RMETA: "right meta",

    pygame.K_SPACE: "space",
    pygame.K_RETURN: "enter",
    pygame.K_ESCAPE: "escape",
    pygame.K_BACKSPACE: "backspace",
    pygame.K_TAB: "tab",
    pygame.K_CAPSLOCK: "caps lock",
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right",
    pygame.K_UP: "up",
    pygame.K_DOWN: "down",

    pygame.K_INSERT: "insert",
    pygame.K_DELETE: "delete",
    pygame.K_HOME: "home",
    pygame.K_END: "end",
    pygame.K_PAGEUP: "page up",
    pygame.K_PAGEDOWN: "page down",

    pygame.K_COMMA: "comma",
    pygame.K_PERIOD: "period",
    pygame.K_SLASH: "slash",
    pygame.K_SEMICOLON: "semicolon",
    pygame.K_QUOTE: "quote",
    pygame.K_LEFTBRACKET: "left bracket",
    pygame.K_RIGHTBRACKET: "right bracket",
    pygame.K_BACKSLASH: "backslash",
    pygame.K_MINUS: "minus",
    pygame.K_EQUALS: "equals",
    pygame.K_BACKQUOTE: "backquote",

    pygame.K_KP0: "numpad 0",
    pygame.K_KP1: "numpad 1",
    pygame.K_KP2: "numpad 2",
    pygame.K_KP3: "numpad 3",
    pygame.K_KP4: "numpad 4",
    pygame.K_KP5: "numpad 5",
    pygame.K_KP6: "numpad 6",
    pygame.K_KP7: "numpad 7",
    pygame.K_KP8: "numpad 8",
    pygame.K_KP9: "numpad 9",
    pygame.K_KP_PERIOD: "numpad period",
    pygame.K_KP_DIVIDE: "numpad divide",
    pygame.K_KP_MULTIPLY: "numpad multiply",
    pygame.K_KP_MINUS: "numpad minus",
    pygame.K_KP_PLUS: "numpad plus",
    pygame.K_KP_ENTER: "numpad enter",
	
    pygame.BUTTON_LEFT: "left mouse",
    pygame.BUTTON_MIDDLE: "middle mouse",
    pygame.BUTTON_RIGHT: "right mouse"
}


class Vec2(pygame.math.Vector2):
	def __init__(self,value = (0,0),value2 = "0"):
		if (isinstance(value,float) or isinstance(value,int)) and (isinstance(value2,float) or isinstance(value2,int)):
			value = (value,value2)
		super().__init__(value[0],value[1])

class Timer:
	def __init__(self, duration, repeat = False, autostart = False, func = None):
		self.duration = duration
		self.start_time = 0
		self.active = False
		self.repeat = repeat
		self.func = func
		if autostart:
			self.activate()

	def activate(self):
		self.active = True
		self.start_time = pygame.time.get_ticks()

	def deactivate(self):
		self.active = False
		self.start_time = 0
		if self.repeat:
			self.activate()

	def update(self):
		if self.active:
			current_time = pygame.time.get_ticks()
			if current_time - self.start_time >= self.duration:
				if self.func: self.func()
				self.deactivate()