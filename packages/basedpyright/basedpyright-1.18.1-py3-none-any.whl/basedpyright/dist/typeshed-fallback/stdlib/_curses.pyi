import sys
from _typeshed import ReadOnlyBuffer, SupportsRead
from typing import IO, Any, NamedTuple, final, overload
from typing_extensions import TypeAlias

# NOTE: This module is ordinarily only available on Unix, but the windows-curses
# package makes it available on Windows as well with the same contents.

# Handled by PyCurses_ConvertToChtype in _cursesmodule.c.
_ChType: TypeAlias = str | bytes | int

# ACS codes are only initialized after initscr is called
ACS_BBSS: int
ACS_BLOCK: int
ACS_BOARD: int
ACS_BSBS: int
ACS_BSSB: int
ACS_BSSS: int
ACS_BTEE: int
ACS_BULLET: int
ACS_CKBOARD: int
ACS_DARROW: int
ACS_DEGREE: int
ACS_DIAMOND: int
ACS_GEQUAL: int
ACS_HLINE: int
ACS_LANTERN: int
ACS_LARROW: int
ACS_LEQUAL: int
ACS_LLCORNER: int
ACS_LRCORNER: int
ACS_LTEE: int
ACS_NEQUAL: int
ACS_PI: int
ACS_PLMINUS: int
ACS_PLUS: int
ACS_RARROW: int
ACS_RTEE: int
ACS_S1: int
ACS_S3: int
ACS_S7: int
ACS_S9: int
ACS_SBBS: int
ACS_SBSB: int
ACS_SBSS: int
ACS_SSBB: int
ACS_SSBS: int
ACS_SSSB: int
ACS_SSSS: int
ACS_STERLING: int
ACS_TTEE: int
ACS_UARROW: int
ACS_ULCORNER: int
ACS_URCORNER: int
ACS_VLINE: int
ALL_MOUSE_EVENTS: int
A_ALTCHARSET: int
A_ATTRIBUTES: int
A_BLINK: int
A_BOLD: int
A_CHARTEXT: int
A_COLOR: int
A_DIM: int
A_HORIZONTAL: int
A_INVIS: int
A_ITALIC: int
A_LEFT: int
A_LOW: int
A_NORMAL: int
A_PROTECT: int
A_REVERSE: int
A_RIGHT: int
A_STANDOUT: int
A_TOP: int
A_UNDERLINE: int
A_VERTICAL: int
BUTTON1_CLICKED: int
BUTTON1_DOUBLE_CLICKED: int
BUTTON1_PRESSED: int
BUTTON1_RELEASED: int
BUTTON1_TRIPLE_CLICKED: int
BUTTON2_CLICKED: int
BUTTON2_DOUBLE_CLICKED: int
BUTTON2_PRESSED: int
BUTTON2_RELEASED: int
BUTTON2_TRIPLE_CLICKED: int
BUTTON3_CLICKED: int
BUTTON3_DOUBLE_CLICKED: int
BUTTON3_PRESSED: int
BUTTON3_RELEASED: int
BUTTON3_TRIPLE_CLICKED: int
BUTTON4_CLICKED: int
BUTTON4_DOUBLE_CLICKED: int
BUTTON4_PRESSED: int
BUTTON4_RELEASED: int
BUTTON4_TRIPLE_CLICKED: int
# Darwin ncurses doesn't provide BUTTON5_* constants
if sys.version_info >= (3, 10) and sys.platform != "darwin":
    BUTTON5_PRESSED: int
    BUTTON5_RELEASED: int
    BUTTON5_CLICKED: int
    BUTTON5_DOUBLE_CLICKED: int
    BUTTON5_TRIPLE_CLICKED: int
BUTTON_ALT: int
BUTTON_CTRL: int
BUTTON_SHIFT: int
COLOR_BLACK: int
COLOR_BLUE: int
COLOR_CYAN: int
COLOR_GREEN: int
COLOR_MAGENTA: int
COLOR_RED: int
COLOR_WHITE: int
COLOR_YELLOW: int
ERR: int
KEY_A1: int
KEY_A3: int
KEY_B2: int
KEY_BACKSPACE: int
KEY_BEG: int
KEY_BREAK: int
KEY_BTAB: int
KEY_C1: int
KEY_C3: int
KEY_CANCEL: int
KEY_CATAB: int
KEY_CLEAR: int
KEY_CLOSE: int
KEY_COMMAND: int
KEY_COPY: int
KEY_CREATE: int
KEY_CTAB: int
KEY_DC: int
KEY_DL: int
KEY_DOWN: int
KEY_EIC: int
KEY_END: int
KEY_ENTER: int
KEY_EOL: int
KEY_EOS: int
KEY_EXIT: int
KEY_F0: int
KEY_F1: int
KEY_F10: int
KEY_F11: int
KEY_F12: int
KEY_F13: int
KEY_F14: int
KEY_F15: int
KEY_F16: int
KEY_F17: int
KEY_F18: int
KEY_F19: int
KEY_F2: int
KEY_F20: int
KEY_F21: int
KEY_F22: int
KEY_F23: int
KEY_F24: int
KEY_F25: int
KEY_F26: int
KEY_F27: int
KEY_F28: int
KEY_F29: int
KEY_F3: int
KEY_F30: int
KEY_F31: int
KEY_F32: int
KEY_F33: int
KEY_F34: int
KEY_F35: int
KEY_F36: int
KEY_F37: int
KEY_F38: int
KEY_F39: int
KEY_F4: int
KEY_F40: int
KEY_F41: int
KEY_F42: int
KEY_F43: int
KEY_F44: int
KEY_F45: int
KEY_F46: int
KEY_F47: int
KEY_F48: int
KEY_F49: int
KEY_F5: int
KEY_F50: int
KEY_F51: int
KEY_F52: int
KEY_F53: int
KEY_F54: int
KEY_F55: int
KEY_F56: int
KEY_F57: int
KEY_F58: int
KEY_F59: int
KEY_F6: int
KEY_F60: int
KEY_F61: int
KEY_F62: int
KEY_F63: int
KEY_F7: int
KEY_F8: int
KEY_F9: int
KEY_FIND: int
KEY_HELP: int
KEY_HOME: int
KEY_IC: int
KEY_IL: int
KEY_LEFT: int
KEY_LL: int
KEY_MARK: int
KEY_MAX: int
KEY_MESSAGE: int
KEY_MIN: int
KEY_MOUSE: int
KEY_MOVE: int
KEY_NEXT: int
KEY_NPAGE: int
KEY_OPEN: int
KEY_OPTIONS: int
KEY_PPAGE: int
KEY_PREVIOUS: int
KEY_PRINT: int
KEY_REDO: int
KEY_REFERENCE: int
KEY_REFRESH: int
KEY_REPLACE: int
KEY_RESET: int
KEY_RESIZE: int
KEY_RESTART: int
KEY_RESUME: int
KEY_RIGHT: int
KEY_SAVE: int
KEY_SBEG: int
KEY_SCANCEL: int
KEY_SCOMMAND: int
KEY_SCOPY: int
KEY_SCREATE: int
KEY_SDC: int
KEY_SDL: int
KEY_SELECT: int
KEY_SEND: int
KEY_SEOL: int
KEY_SEXIT: int
KEY_SF: int
KEY_SFIND: int
KEY_SHELP: int
KEY_SHOME: int
KEY_SIC: int
KEY_SLEFT: int
KEY_SMESSAGE: int
KEY_SMOVE: int
KEY_SNEXT: int
KEY_SOPTIONS: int
KEY_SPREVIOUS: int
KEY_SPRINT: int
KEY_SR: int
KEY_SREDO: int
KEY_SREPLACE: int
KEY_SRESET: int
KEY_SRIGHT: int
KEY_SRSUME: int
KEY_SSAVE: int
KEY_SSUSPEND: int
KEY_STAB: int
KEY_SUNDO: int
KEY_SUSPEND: int
KEY_UNDO: int
KEY_UP: int
OK: int
REPORT_MOUSE_POSITION: int
_C_API: Any
version: bytes

def baudrate() -> int:
    """Return the output speed of the terminal in bits per second."""
    ...
def beep() -> None:
    """Emit a short attention sound."""
    ...
def can_change_color() -> bool:
    """Return True if the programmer can change the colors displayed by the terminal."""
    ...
def cbreak(flag: bool = True, /) -> None:
    """
    Enter cbreak mode.

      flag
        If false, the effect is the same as calling nocbreak().

    In cbreak mode (sometimes called "rare" mode) normal tty line buffering is
    turned off and characters are available to be read one by one.  However,
    unlike raw mode, special characters (interrupt, quit, suspend, and flow
    control) retain their effects on the tty driver and calling program.
    Calling first raw() then cbreak() leaves the terminal in cbreak mode.
    """
    ...
def color_content(color_number: int, /) -> tuple[int, int, int]:
    """
    Return the red, green, and blue (RGB) components of the specified color.

      color_number
        The number of the color (0 - (COLORS-1)).

    A 3-tuple is returned, containing the R, G, B values for the given color,
    which will be between 0 (no component) and 1000 (maximum amount of component).
    """
    ...
def color_pair(pair_number: int, /) -> int:
    """
    Return the attribute value for displaying text in the specified color.

      pair_number
        The number of the color pair.

    This attribute value can be combined with A_STANDOUT, A_REVERSE, and the
    other A_* attributes.  pair_number() is the counterpart to this function.
    """
    ...
def curs_set(visibility: int, /) -> int:
    """
    Set the cursor state.

      visibility
        0 for invisible, 1 for normal visible, or 2 for very visible.

    If the terminal supports the visibility requested, the previous cursor
    state is returned; otherwise, an exception is raised.  On many terminals,
    the "visible" mode is an underline cursor and the "very visible" mode is
    a block cursor.
    """
    ...
def def_prog_mode() -> None:
    """
    Save the current terminal mode as the "program" mode.

    The "program" mode is the mode when the running program is using curses.

    Subsequent calls to reset_prog_mode() will restore this mode.
    """
    ...
def def_shell_mode() -> None:
    """
    Save the current terminal mode as the "shell" mode.

    The "shell" mode is the mode when the running program is not using curses.

    Subsequent calls to reset_shell_mode() will restore this mode.
    """
    ...
def delay_output(ms: int, /) -> None:
    """
    Insert a pause in output.

    ms
      Duration in milliseconds.
    """
    ...
def doupdate() -> None:
    """Update the physical screen to match the virtual screen."""
    ...
def echo(flag: bool = True, /) -> None:
    """
    Enter echo mode.

      flag
        If false, the effect is the same as calling noecho().

    In echo mode, each character input is echoed to the screen as it is entered.
    """
    ...
def endwin() -> None:
    """De-initialize the library, and return terminal to normal status."""
    ...
def erasechar() -> bytes:
    """Return the user's current erase character."""
    ...
def filter() -> None: ...
def flash() -> None:
    """
    Flash the screen.

    That is, change it to reverse-video and then change it back in a short interval.
    """
    ...
def flushinp() -> None:
    """
    Flush all input buffers.

    This throws away any typeahead that has been typed by the user and has not
    yet been processed by the program.
    """
    ...

if sys.version_info >= (3, 9):
    def get_escdelay() -> int:
        """
        Gets the curses ESCDELAY setting.

        Gets the number of milliseconds to wait after reading an escape character,
        to distinguish between an individual escape character entered on the
        keyboard from escape sequences sent by cursor and function keys.
        """
        ...
    def get_tabsize() -> int:
        """
        Gets the curses TABSIZE setting.

        Gets the number of columns used by the curses library when converting a tab
        character to spaces as it adds the tab to a window.
        """
        ...

def getmouse() -> tuple[int, int, int, int, int]:
    """
    Retrieve the queued mouse event.

    After getch() returns KEY_MOUSE to signal a mouse event, this function
    returns a 5-tuple (id, x, y, z, bstate).
    """
    ...
def getsyx() -> tuple[int, int]:
    """
    Return the current coordinates of the virtual screen cursor.

    Return a (y, x) tuple.  If leaveok is currently true, return (-1, -1).
    """
    ...
def getwin(file: SupportsRead[bytes], /) -> _CursesWindow:
    """
    Read window related data stored in the file by an earlier putwin() call.

    The routine then creates and initializes a new window using that data,
    returning the new window object.
    """
    ...
def halfdelay(tenths: int, /) -> None:
    """
    Enter half-delay mode.

      tenths
        Maximal blocking delay in tenths of seconds (1 - 255).

    Use nocbreak() to leave half-delay mode.
    """
    ...
def has_colors() -> bool:
    """Return True if the terminal can display colors; otherwise, return False."""
    ...

if sys.version_info >= (3, 10):
    def has_extended_color_support() -> bool:
        """
        Return True if the module supports extended colors; otherwise, return False.

        Extended color support allows more than 256 color-pairs for terminals
        that support more than 16 colors (e.g. xterm-256color).
        """
        ...

def has_ic() -> bool:
    """Return True if the terminal has insert- and delete-character capabilities."""
    ...
def has_il() -> bool:
    """Return True if the terminal has insert- and delete-line capabilities."""
    ...
def has_key(key: int, /) -> bool:
    """
    Return True if the current terminal type recognizes a key with that value.

    key
      Key number.
    """
    ...
def init_color(color_number: int, r: int, g: int, b: int, /) -> None:
    """
    Change the definition of a color.

      color_number
        The number of the color to be changed (0 - (COLORS-1)).
      r
        Red component (0 - 1000).
      g
        Green component (0 - 1000).
      b
        Blue component (0 - 1000).

    When init_color() is used, all occurrences of that color on the screen
    immediately change to the new definition.  This function is a no-op on
    most terminals; it is active only if can_change_color() returns true.
    """
    ...
def init_pair(pair_number: int, fg: int, bg: int, /) -> None:
    """
    Change the definition of a color-pair.

      pair_number
        The number of the color-pair to be changed (1 - (COLOR_PAIRS-1)).
      fg
        Foreground color number (-1 - (COLORS-1)).
      bg
        Background color number (-1 - (COLORS-1)).

    If the color-pair was previously initialized, the screen is refreshed and
    all occurrences of that color-pair are changed to the new definition.
    """
    ...
def initscr() -> _CursesWindow:
    """
    Initialize the library.

    Return a WindowObject which represents the whole screen.
    """
    ...
def intrflush(flag: bool, /) -> None: ...
def is_term_resized(nlines: int, ncols: int, /) -> bool:
    """
    Return True if resize_term() would modify the window structure, False otherwise.

    nlines
      Height.
    ncols
      Width.
    """
    ...
def isendwin() -> bool:
    """Return True if endwin() has been called."""
    ...
def keyname(key: int, /) -> bytes:
    """
    Return the name of specified key.

    key
      Key number.
    """
    ...
def killchar() -> bytes:
    """Return the user's current line kill character."""
    ...
def longname() -> bytes:
    """
    Return the terminfo long name field describing the current terminal.

    The maximum length of a verbose description is 128 characters.  It is defined
    only after the call to initscr().
    """
    ...
def meta(yes: bool, /) -> None:
    """
    Enable/disable meta keys.

    If yes is True, allow 8-bit characters to be input.  If yes is False,
    allow only 7-bit characters.
    """
    ...
def mouseinterval(interval: int, /) -> None:
    """
    Set and retrieve the maximum time between press and release in a click.

      interval
        Time in milliseconds.

    Set the maximum time that can elapse between press and release events in
    order for them to be recognized as a click, and return the previous interval
    value.
    """
    ...
def mousemask(newmask: int, /) -> tuple[int, int]:
    """
    Set the mouse events to be reported, and return a tuple (availmask, oldmask).

    Return a tuple (availmask, oldmask).  availmask indicates which of the
    specified mouse events can be reported; on complete failure it returns 0.
    oldmask is the previous value of the given window's mouse event mask.
    If this function is never called, no mouse events are ever reported.
    """
    ...
def napms(ms: int, /) -> int:
    """
    Sleep for specified time.

    ms
      Duration in milliseconds.
    """
    ...
def newpad(nlines: int, ncols: int, /) -> _CursesWindow:
    """
    Create and return a pointer to a new pad data structure.

    nlines
      Height.
    ncols
      Width.
    """
    ...
def newwin(nlines: int, ncols: int, begin_y: int = ..., begin_x: int = ..., /) -> _CursesWindow:
    """
    newwin(nlines, ncols, [begin_y=0, begin_x=0])
    Return a new window.

      nlines
        Height.
      ncols
        Width.
      begin_y
        Top side y-coordinate.
      begin_x
        Left side x-coordinate.

    By default, the window will extend from the specified position to the lower
    right corner of the screen.
    """
    ...
def nl(flag: bool = True, /) -> None:
    """
    Enter newline mode.

      flag
        If false, the effect is the same as calling nonl().

    This mode translates the return key into newline on input, and translates
    newline into return and line-feed on output.  Newline mode is initially on.
    """
    ...
def nocbreak() -> None:
    """
    Leave cbreak mode.

    Return to normal "cooked" mode with line buffering.
    """
    ...
def noecho() -> None:
    """
    Leave echo mode.

    Echoing of input characters is turned off.
    """
    ...
def nonl() -> None:
    """
    Leave newline mode.

    Disable translation of return into newline on input, and disable low-level
    translation of newline into newline/return on output.
    """
    ...
def noqiflush() -> None:
    """
    Disable queue flushing.

    When queue flushing is disabled, normal flush of input and output queues
    associated with the INTR, QUIT and SUSP characters will not be done.
    """
    ...
def noraw() -> None:
    """
    Leave raw mode.

    Return to normal "cooked" mode with line buffering.
    """
    ...
def pair_content(pair_number: int, /) -> tuple[int, int]:
    """
    Return a tuple (fg, bg) containing the colors for the requested color pair.

    pair_number
      The number of the color pair (0 - (COLOR_PAIRS-1)).
    """
    ...
def pair_number(attr: int, /) -> int:
    """
    Return the number of the color-pair set by the specified attribute value.

    color_pair() is the counterpart to this function.
    """
    ...
def putp(string: ReadOnlyBuffer, /) -> None:
    """
    Emit the value of a specified terminfo capability for the current terminal.

    Note that the output of putp() always goes to standard output.
    """
    ...
def qiflush(flag: bool = True, /) -> None:
    """
    Enable queue flushing.

      flag
        If false, the effect is the same as calling noqiflush().

    If queue flushing is enabled, all output in the display driver queue
    will be flushed when the INTR, QUIT and SUSP characters are read.
    """
    ...
def raw(flag: bool = True, /) -> None:
    """
    Enter raw mode.

      flag
        If false, the effect is the same as calling noraw().

    In raw mode, normal line buffering and processing of interrupt, quit,
    suspend, and flow control keys are turned off; characters are presented to
    curses input functions one by one.
    """
    ...
def reset_prog_mode() -> None:
    """Restore the terminal to "program" mode, as previously saved by def_prog_mode()."""
    ...
def reset_shell_mode() -> None:
    """Restore the terminal to "shell" mode, as previously saved by def_shell_mode()."""
    ...
def resetty() -> None:
    """Restore terminal mode."""
    ...
def resize_term(nlines: int, ncols: int, /) -> None:
    """
    Backend function used by resizeterm(), performing most of the work.

      nlines
        Height.
      ncols
        Width.

    When resizing the windows, resize_term() blank-fills the areas that are
    extended.  The calling application should fill in these areas with appropriate
    data.  The resize_term() function attempts to resize all windows.  However,
    due to the calling convention of pads, it is not possible to resize these
    without additional interaction with the application.
    """
    ...
def resizeterm(nlines: int, ncols: int, /) -> None:
    """
    Resize the standard and current windows to the specified dimensions.

      nlines
        Height.
      ncols
        Width.

    Adjusts other bookkeeping data used by the curses library that record the
    window dimensions (in particular the SIGWINCH handler).
    """
    ...
def savetty() -> None:
    """Save terminal mode."""
    ...

if sys.version_info >= (3, 9):
    def set_escdelay(ms: int, /) -> None:
        """
        Sets the curses ESCDELAY setting.

          ms
            length of the delay in milliseconds.

        Sets the number of milliseconds to wait after reading an escape character,
        to distinguish between an individual escape character entered on the
        keyboard from escape sequences sent by cursor and function keys.
        """
        ...
    def set_tabsize(size: int, /) -> None:
        """
        Sets the curses TABSIZE setting.

          size
            rendered cell width of a tab character.

        Sets the number of columns used by the curses library when converting a tab
        character to spaces as it adds the tab to a window.
        """
        ...

def setsyx(y: int, x: int, /) -> None:
    """
    Set the virtual screen cursor.

      y
        Y-coordinate.
      x
        X-coordinate.

    If y and x are both -1, then leaveok is set.
    """
    ...
def setupterm(term: str | None = None, fd: int = -1) -> None:
    """
    Initialize the terminal.

    term
      Terminal name.
      If omitted, the value of the TERM environment variable will be used.
    fd
      File descriptor to which any initialization sequences will be sent.
      If not supplied, the file descriptor for sys.stdout will be used.
    """
    ...
def start_color() -> None:
    """
    Initializes eight basic colors and global variables COLORS and COLOR_PAIRS.

    Must be called if the programmer wants to use colors, and before any other
    color manipulation routine is called.  It is good practice to call this
    routine right after initscr().

    It also restores the colors on the terminal to the values they had when the
    terminal was just turned on.
    """
    ...
def termattrs() -> int:
    """Return a logical OR of all video attributes supported by the terminal."""
    ...
def termname() -> bytes:
    """Return the value of the environment variable TERM, truncated to 14 characters."""
    ...
def tigetflag(capname: str, /) -> int:
    """
    Return the value of the Boolean capability.

      capname
        The terminfo capability name.

    The value -1 is returned if capname is not a Boolean capability, or 0 if
    it is canceled or absent from the terminal description.
    """
    ...
def tigetnum(capname: str, /) -> int:
    """
    Return the value of the numeric capability.

      capname
        The terminfo capability name.

    The value -2 is returned if capname is not a numeric capability, or -1 if
    it is canceled or absent from the terminal description.
    """
    ...
def tigetstr(capname: str, /) -> bytes | None:
    """
    Return the value of the string capability.

      capname
        The terminfo capability name.

    None is returned if capname is not a string capability, or is canceled or
    absent from the terminal description.
    """
    ...
def tparm(
    str: ReadOnlyBuffer,
    i1: int = 0,
    i2: int = 0,
    i3: int = 0,
    i4: int = 0,
    i5: int = 0,
    i6: int = 0,
    i7: int = 0,
    i8: int = 0,
    i9: int = 0,
    /,
) -> bytes:
    """
    Instantiate the specified byte string with the supplied parameters.

    str
      Parameterized byte string obtained from the terminfo database.
    """
    ...
def typeahead(fd: int, /) -> None:
    """
    Specify that the file descriptor fd be used for typeahead checking.

      fd
        File descriptor.

    If fd is -1, then no typeahead checking is done.
    """
    ...
def unctrl(ch: _ChType, /) -> bytes:
    """
    Return a string which is a printable representation of the character ch.

    Control characters are displayed as a caret followed by the character,
    for example as ^C.  Printing characters are left as they are.
    """
    ...
def unget_wch(ch: int | str, /) -> None:
    """Push ch so the next get_wch() will return it."""
    ...
def ungetch(ch: _ChType, /) -> None:
    """Push ch so the next getch() will return it."""
    ...
def ungetmouse(id: int, x: int, y: int, z: int, bstate: int, /) -> None:
    """
    Push a KEY_MOUSE event onto the input queue.

    The following getmouse() will return the given state data.
    """
    ...
def update_lines_cols() -> None: ...
def use_default_colors() -> None:
    """
    Allow use of default values for colors on terminals supporting this feature.

    Use this to support transparency in your application.  The default color
    is assigned to the color number -1.
    """
    ...
def use_env(flag: bool, /) -> None:
    """
    Use environment variables LINES and COLUMNS.

    If used, this function should be called before initscr() or newterm() are
    called.

    When flag is False, the values of lines and columns specified in the terminfo
    database will be used, even if environment variables LINES and COLUMNS (used
    by default) are set, or if curses is running in a window (in which case
    default behavior would be to use the window size if LINES and COLUMNS are
    not set).
    """
    ...

class error(Exception): ...

@final
class _CursesWindow:
    encoding: str
    @overload
    def addch(self, ch: _ChType, attr: int = ...) -> None: ...
    @overload
    def addch(self, y: int, x: int, ch: _ChType, attr: int = ...) -> None: ...
    @overload
    def addnstr(self, str: str, n: int, attr: int = ...) -> None: ...
    @overload
    def addnstr(self, y: int, x: int, str: str, n: int, attr: int = ...) -> None: ...
    @overload
    def addstr(self, str: str, attr: int = ...) -> None: ...
    @overload
    def addstr(self, y: int, x: int, str: str, attr: int = ...) -> None: ...
    def attroff(self, attr: int, /) -> None: ...
    def attron(self, attr: int, /) -> None: ...
    def attrset(self, attr: int, /) -> None: ...
    def bkgd(self, ch: _ChType, attr: int = ..., /) -> None: ...
    def bkgdset(self, ch: _ChType, attr: int = ..., /) -> None: ...
    def border(
        self,
        ls: _ChType = ...,
        rs: _ChType = ...,
        ts: _ChType = ...,
        bs: _ChType = ...,
        tl: _ChType = ...,
        tr: _ChType = ...,
        bl: _ChType = ...,
        br: _ChType = ...,
    ) -> None: ...
    @overload
    def box(self) -> None: ...
    @overload
    def box(self, vertch: _ChType = ..., horch: _ChType = ...) -> None: ...
    @overload
    def chgat(self, attr: int) -> None: ...
    @overload
    def chgat(self, num: int, attr: int) -> None: ...
    @overload
    def chgat(self, y: int, x: int, attr: int) -> None: ...
    @overload
    def chgat(self, y: int, x: int, num: int, attr: int) -> None: ...
    def clear(self) -> None: ...
    def clearok(self, yes: int) -> None: ...
    def clrtobot(self) -> None: ...
    def clrtoeol(self) -> None: ...
    def cursyncup(self) -> None: ...
    @overload
    def delch(self) -> None: ...
    @overload
    def delch(self, y: int, x: int) -> None: ...
    def deleteln(self) -> None: ...
    @overload
    def derwin(self, begin_y: int, begin_x: int) -> _CursesWindow: ...
    @overload
    def derwin(self, nlines: int, ncols: int, begin_y: int, begin_x: int) -> _CursesWindow: ...
    def echochar(self, ch: _ChType, attr: int = ..., /) -> None: ...
    def enclose(self, y: int, x: int, /) -> bool: ...
    def erase(self) -> None: ...
    def getbegyx(self) -> tuple[int, int]: ...
    def getbkgd(self) -> tuple[int, int]: ...
    @overload
    def getch(self) -> int: ...
    @overload
    def getch(self, y: int, x: int) -> int: ...
    @overload
    def get_wch(self) -> int | str: ...
    @overload
    def get_wch(self, y: int, x: int) -> int | str: ...
    @overload
    def getkey(self) -> str: ...
    @overload
    def getkey(self, y: int, x: int) -> str: ...
    def getmaxyx(self) -> tuple[int, int]: ...
    def getparyx(self) -> tuple[int, int]: ...
    @overload
    def getstr(self) -> bytes: ...
    @overload
    def getstr(self, n: int) -> bytes: ...
    @overload
    def getstr(self, y: int, x: int) -> bytes: ...
    @overload
    def getstr(self, y: int, x: int, n: int) -> bytes: ...
    def getyx(self) -> tuple[int, int]: ...
    @overload
    def hline(self, ch: _ChType, n: int) -> None: ...
    @overload
    def hline(self, y: int, x: int, ch: _ChType, n: int) -> None: ...
    def idcok(self, flag: bool) -> None: ...
    def idlok(self, yes: bool) -> None: ...
    def immedok(self, flag: bool) -> None: ...
    @overload
    def inch(self) -> int: ...
    @overload
    def inch(self, y: int, x: int) -> int: ...
    @overload
    def insch(self, ch: _ChType, attr: int = ...) -> None: ...
    @overload
    def insch(self, y: int, x: int, ch: _ChType, attr: int = ...) -> None: ...
    def insdelln(self, nlines: int) -> None: ...
    def insertln(self) -> None: ...
    @overload
    def insnstr(self, str: str, n: int, attr: int = ...) -> None: ...
    @overload
    def insnstr(self, y: int, x: int, str: str, n: int, attr: int = ...) -> None: ...
    @overload
    def insstr(self, str: str, attr: int = ...) -> None: ...
    @overload
    def insstr(self, y: int, x: int, str: str, attr: int = ...) -> None: ...
    @overload
    def instr(self, n: int = ...) -> bytes: ...
    @overload
    def instr(self, y: int, x: int, n: int = ...) -> bytes: ...
    def is_linetouched(self, line: int, /) -> bool: ...
    def is_wintouched(self) -> bool: ...
    def keypad(self, yes: bool, /) -> None: ...
    def leaveok(self, yes: bool) -> None: ...
    def move(self, new_y: int, new_x: int) -> None: ...
    def mvderwin(self, y: int, x: int) -> None: ...
    def mvwin(self, new_y: int, new_x: int) -> None: ...
    def nodelay(self, yes: bool) -> None: ...
    def notimeout(self, yes: bool) -> None: ...
    @overload
    def noutrefresh(self) -> None: ...
    @overload
    def noutrefresh(self, pminrow: int, pmincol: int, sminrow: int, smincol: int, smaxrow: int, smaxcol: int) -> None: ...
    @overload
    def overlay(self, destwin: _CursesWindow) -> None: ...
    @overload
    def overlay(
        self, destwin: _CursesWindow, sminrow: int, smincol: int, dminrow: int, dmincol: int, dmaxrow: int, dmaxcol: int
    ) -> None: ...
    @overload
    def overwrite(self, destwin: _CursesWindow) -> None: ...
    @overload
    def overwrite(
        self, destwin: _CursesWindow, sminrow: int, smincol: int, dminrow: int, dmincol: int, dmaxrow: int, dmaxcol: int
    ) -> None: ...
    def putwin(self, file: IO[Any], /) -> None: ...
    def redrawln(self, beg: int, num: int, /) -> None: ...
    def redrawwin(self) -> None: ...
    @overload
    def refresh(self) -> None: ...
    @overload
    def refresh(self, pminrow: int, pmincol: int, sminrow: int, smincol: int, smaxrow: int, smaxcol: int) -> None: ...
    def resize(self, nlines: int, ncols: int) -> None: ...
    def scroll(self, lines: int = ...) -> None: ...
    def scrollok(self, flag: bool) -> None: ...
    def setscrreg(self, top: int, bottom: int, /) -> None: ...
    def standend(self) -> None: ...
    def standout(self) -> None: ...
    @overload
    def subpad(self, begin_y: int, begin_x: int) -> _CursesWindow: ...
    @overload
    def subpad(self, nlines: int, ncols: int, begin_y: int, begin_x: int) -> _CursesWindow: ...
    @overload
    def subwin(self, begin_y: int, begin_x: int) -> _CursesWindow: ...
    @overload
    def subwin(self, nlines: int, ncols: int, begin_y: int, begin_x: int) -> _CursesWindow: ...
    def syncdown(self) -> None: ...
    def syncok(self, flag: bool) -> None: ...
    def syncup(self) -> None: ...
    def timeout(self, delay: int) -> None: ...
    def touchline(self, start: int, count: int, changed: bool = ...) -> None: ...
    def touchwin(self) -> None: ...
    def untouchwin(self) -> None: ...
    @overload
    def vline(self, ch: _ChType, n: int) -> None: ...
    @overload
    def vline(self, y: int, x: int, ch: _ChType, n: int) -> None: ...

class _ncurses_version(NamedTuple):
    major: int
    minor: int
    patch: int

ncurses_version: _ncurses_version
window = _CursesWindow  # undocumented
